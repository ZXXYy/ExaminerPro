set pagination off
set $cnt=0
set $loop=16705
set $testnum=100000
set $inst_loc=0x12 
set $check_addr=0x0073f7c8
set $finish_addr=0xac
set $finish_brk_addr=0xa8
set auto-load safe-path /

define get-cpu-state
    info registers
end

define get-exception-state
    printf "-------------------%s----------------\n", str
    p /x *regs
end

define dump_state
set $i = 0
   while($i < 3)
     if $i == 2 
        set $real_finish_brk_addr = $inst_loc + $load_addr + ($loop-1)*19*4 + 18*4
        if $pc == $real_finish_brk_addr
            printf "===================FINISH===================\n\n"
            if $expcetion == 0
                get-cpu-state
            end
            if $testnum == $loop
                set $i = $i + 1
            else
                set $sp = $presp
                set $presp = $sp
                set $expcetion = 0
                set logging off
                eval "set logging file ./output_virt/%d.output", $cnt*$testnum+$loop
                set logging overwrite on
                set logging on
                x/x $pc
                x/x $pc + 18*4
                p $loop
                printf "test case: %d\n", $cnt*$testnum+$loop++
            end
        else
            set $expcetion = 1
            get-exception-state
        end
     end
     if $i == 1
        printf "===================inst_location===================\n\n"
        set $pc = $inst_loc + $load_addr + ($loop)*19*4
        set $prepc = $inst_loc + $load_addr + ($loop)*19*4+17*4
        set $presp = $sp
        set logging off
        eval "set logging file ./output_virt/%d.output", $cnt*$testnum+$loop
        set logging overwrite on
        set logging on
        printf "test case: %d\n", $cnt*$testnum+$loop++
        x/x $pc
        x/x $prepc
        set $i = $i + 1
     end
     if $i == 0
        printf "===================do_init_module===================\n\n"
        print mod->core_layout.base
        add-symbol-file kmod/ktemplate.ko mod->core_layout.base
        set $load_addr = mod->core_layout.base
        set $cnt=$cnt+1 
        set $expcetion = 0
        set $i = $i + 1
     end
     continue
   end
end
set pagination off
set $cnt=6
set $loop=76474
set $testnum=100000
set $init_addr=0x68
set $check_addr=0x73f7f4
set $finish_addr=0x73f7f8
set auto-load safe-path /

def get-cpu-state
    info registers
end

def get-exception-state
    p /x *regs
end

def set-testcase-bp
    b inst_location
    commands
        set $pc = $init_addr + $load_addr + ($loop)*19*4
        set $prepc = $init_addr + $load_addr + ($loop)*19*4+17*4
        set $presp = $sp
        set logging off
        eval "set logging file ./output_virt/%d.output", $cnt*$testnum+$loop
        set logging overwrite on
        set logging on
        printf "test case: %d\n", $cnt*$testnum+$loop++
        x/x $pc
        x/x $prepc
        b do_PrefetchAbort
        command
            printf "-------------------pabt----------------\n"
            get-exception-state
            p ifsr
            set addr=$prepc
            set regs->uregs[15]=$prepc
            set $expcetion = 1
            continue
        end
        b do_DataAbort
        command
            printf "-------------------dabt----------------\n"
            get-exception-state
            p fsr
            set $expcetion = 1
            continue
        end
        b my_undef_inst
        command
            printf "-------------------und----------------\n"
            get-exception-state
            set $expcetion = 1
            continue
        end
        b prefetch_success
        command
            set regs->uregs[15]=$prepc+4
            continue
        end
        b data_success
        command
            set regs->uregs[15]=$prepc+4
            continue
        end
        continue
    end
    b prepare_dump
    command
        if $expcetion == 1
            set $pc=$finish_addr + $load_addr
        end
        continue
    end
    b dump_memory
    command
        set $temp=$r3
        set $r3=$prepc
        set $pc=$pc+($loop-1)*8
        continue
    end
    b check_memory
    command
        set $r3=$temp
        printf "===================MEMORY===================\n\n"
        p/x $r1
        continue
    end
    b finish_location
    command
        printf "===================FINISH===================\n\n"
        if $expcetion == 0
            get-cpu-state
        end
        if $testnum == $loop
            continue
        else
            set $sp = $presp
            set $pc = $init_addr + $load_addr + ($loop)*19*4
            set $prepc = $init_addr + $load_addr + ($loop)*19*4+17*4
            set $presp = $sp
            set $expcetion = 0
            set logging off
            eval "set logging file ./output_virt/%d.output", $cnt*$testnum+$loop
            set logging overwrite on
            set logging on
            x/x $pc
            x/x $prepc
            p $loop
            printf "test case: %d\n", $cnt*$testnum+$loop++
            continue
        end
    end
    b testcase_end
    command
        clear do_PrefetchAbort
        clear do_DataAbort
        clear my_undef_inst
        clear prefetch_success
        clear data_success
        continue
    end
end

b do_init_module
command
    print mod->core_layout.base
    add-symbol-file kmod/ktemplate.ko mod->core_layout.base
    set $load_addr = mod->core_layout.base
    set $cnt=$cnt+1 
    set $expcetion = 0
    continue
end

add-symbol-file kmod/ktemplate.ko 0x7f000000
set-testcase-bp

target remote localhost:1234
continue
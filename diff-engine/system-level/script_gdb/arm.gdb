set pagination off
set $cnt=-1
set $loop=0
set $testnum=100000

set $testcase_start_addr=0xac
set $inst_loc_addr=0xf0
set $finish_loc_addr=0xc3600
set auto-load safe-path /

define get-cpu-state
    info registers
end

define get-exception-state
    p /x *regs
end

define set-testcase-bp
    b init_module
    commands
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
    b inst_location
    commands
        set $pc = $inst_loc_addr + $load_addr + ($loop)*3*4
        set $prepc = $inst_loc_addr + $load_addr + ($loop)*3*4
        set $presp = $sp
        set $expcetion = 0
        set logging off
        eval "set logging file ./output_virt/%d.output", $cnt*$testnum+$loop
        set logging overwrite on
        set logging on
        printf "test case: %d\n", $cnt*$testnum+$loop++
        x/x $pc
        x/x $prepc
        continue
    end 
    b prepare_dump
    command
        if $expcetion == 1
            set $pc=$finish_loc_addr + $load_addr
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
            set $pc = $testcase_start_addr + $load_addr
            set $sp = $presp
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
    add-symbol-file ../../test-generator/test_template/system-level/ktemplate_arm.ko mod->core_layout.base
    set $load_addr = mod->core_layout.base
    set $cnt=$cnt+1 
    set $expcetion = 0
    continue
end

add-symbol-file ../../test-generator/test_template/system-level/ktemplate_arm.ko 0x7f000000
set-testcase-bp

target remote localhost:1234
continue
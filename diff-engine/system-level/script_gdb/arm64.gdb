set pagination off
set $cnt=-1
set $loop=0
set $testnum=100000
set $init_addr=0x158
set $testcase_start_addr=0xdc
set $finish_addr=0x1250e8
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
        b do_sp_pc_abort
        command
            printf "test case: %d\n", $cnt*$testnum+$loop
            set addr=$prepc
            set regs->uregs[15]=$prepc
            set $expcetion = 1
            continue
        end
        b do_mem_abort
        command
            printf "test case: %d\n", $cnt*$testnum+$loop
            set $expcetion = 1
            continue
        end
        b do_ptrauth_fault
        command
            printf "test case: %d\n", $cnt*$testnum+$loop
            set $expcetion = 1
            continue
        end
        b do_undefinstr
        command
            printf "test case: %d\n", $cnt*$testnum+$loop
            set $expcetion = 1
            continue
        end
        b data_success
        command
            set regs->pc=$prepc+4
            continue
        end
        continue
    end
    b inst_location
    commands
        set $pc = $init_addr + $load_addr + ($loop)*3*4
        set $prepc = $init_addr + $load_addr + ($loop)*3*4
        set $presp = $sp
        set $expcetion = 0
        printf "test case: %d\n", $cnt*$testnum+$loop++
        x/x $pc
        x/x $prepc
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
        clear do_mem_abort
        clear do_undefinstr
        clear data_success
        clear do_sp_pc_abort
        clear do_ptrauth_fault
        continue
    end
end

b do_init_module
command
    print mod->core_layout.base
    add-symbol-file ../../test-generator/test_template/system-level/ktemplate_arm64.ko mod->core_layout.base
    set $load_addr = mod->core_layout.base
    set $cnt=$cnt+1 
    set $expcetion = 0
    continue
end

add-symbol-file ../../test-generator/test_template/system-level/ktemplate_arm64.ko 0x7f000000
set-testcase-bp

target remote localhost:1234
continue

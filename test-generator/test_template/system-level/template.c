// hello.c
#include <linux/module.h>
#include <linux/kernel.h>
#include <asm/traps.h> 
#include <linux/sched.h>
#include <linux/time.h>
// #include <linux/kgdb.h>
#define NUM_TESTS 1000

MODULE_LICENSE("GPL");
#pragma GCC optimize ("O0")
// instr is undefined instruction value
int undef_instr_handler(struct pt_regs *regs, u32 instr)
{
    // printk(KERN_INFO "get undefined instruction\n");
    __asm__ __volatile__(
        ".global my_undef_inst\n"
        "my_undef_inst:\n"
    );
    // Just skip over to the next instruction.
    regs->pc += 4;

    return 0; // All fine!
}

static struct undef_hook uh = {
    .instr_mask  = 0x0, // any instruction
    .instr_val   = 0x0, // any instruction
    // .cpsr_mask = 0x0, // any pstate
    // .cpsr_val  = 0x0, // any pstate
    .fn          = undef_instr_handler
};
int init_module(void) {
    ktime_t start_tm, end_tm;
    // printk(KERN_INFO "current pid = %d\n", current->pid);
    long long cpu_time_start, cpu_time_end;
    printk(KERN_INFO "current time = %lld\n", current->se.sum_exec_runtime);
    // Lookup wanted symbols.
    register_undef_hook(&uh);
    
    start_tm = ktime_get_boottime_ns();
    cpu_time_start = current->se.sum_exec_runtime;
    #ifdef __aarch64__
    __asm__ __volatile__(
        "stp x0, x1, [sp, #-16]!\n"
        "stp x2, x3, [sp, #-16]!\n"
        "stp x4, x5, [sp, #-16]!\n"
        "stp x6, x7, [sp, #-16]!\n"
        "stp x8, x9, [sp, #-16]!\n"
        "stp x10, x11, [sp, #-16]!\n"
        "stp x12, x13, [sp, #-16]!\n"
        "stp x14, x15, [sp, #-16]!\n"
        "stp x16, x17, [sp, #-16]!\n"
        "stp x18, x19, [sp, #-16]!\n"
        "stp x20, x21, [sp, #-16]!\n"
        "stp x22, x23, [sp, #-16]!\n"
        "stp x24, x25, [sp, #-16]!\n"
        "stp x26, x27, [sp, #-16]!\n"
        "stp x28, x29, [sp, #-16]!\n"
        "str x30, [sp, #-16]!\n"

    );
    __asm__ __volatile__(
        ".global testcase_start\n"
        "testcase_start:\n"
        "mov x0, #0\n"
        "mov x1, #0\n"
        "mov x2, #0\n"
        "mov x3, #0\n"
        "mov x4, #0\n"
        "mov x5, #0\n"
        "mov x6, #0\n"
        "mov x7, #0\n"
        "mov x8, #0\n"
        "mov x9, #0\n"
        "mov x10, #0\n"
        "mov x11, #0\n"
        "mov x12, #0\n"
        "mov x13, #0\n"
        "mov x14, #0\n"
        "mov x15, #0\n"
        "mov x16, #0\n"
        "mov x17, #0\n"
        "mov x18, #0\n"
        "mov x19, #0\n"
        "mov x20, #0\n"
        "mov x21, #0\n"
        "mov x22, #0\n"
        "mov x23, #0\n"
        "mov x24, #0\n"
        "mov x25, #0\n"
        "mov x26, #0\n"
        "mov x27, #0\n"
        "mov x28, #0\n"
        "mov x29, #0\n"
        "mov x30, #0\n"
    );
    #else
    __asm__ __volatile__(
        "push {r0-r12}\n"
        ".global testcase_start\n"
        "testcase_start:\n"
        "mov r1, #0x6007\n"
        "mov r0, #0x13\n"
        "orr r0, r0, r1, LSL #16\n"
        "msr cpsr, r0\n"
        "mov r0, #0\n"
        "mov r1, #0\n"
        "mov r2, #0\n"
        "mov r3, #0\n"
        "mov r4, #0\n"
        "mov r5, #0\n"
        "mov r6, #0\n"
        "mov r7, #0\n"
        "mov r8, #0\n"
        "mov r9, #0\n"
        "mov r10, #0\n"
        "mov r11, #0\n"
        "mov r12, #0\n"
    );
    #endif
    __asm__ __volatile__(
        ".global inst_location\n"
        "inst_location:\n"
        ".global prepare_dump\n"
        "prepare_dump:\n"
        #ifdef __aarch64__
        "str x1, [sp, #-16]!\n"
        #else  
        "push {r1}\n"
        #endif
        ".global dump_memory\n"
        "dump_memory:\n"
        ".global check_memory\n"
        "check_memory:\n"
        #ifdef __aarch64__
        "ldr x1, [sp], #16"
        #else
        "pop {r1}\n"
        #endif
    );
    __asm__ __volatile__(
        ".global finish_location\n"
        "finish_location:\n"
    );
    #ifdef __aarch64__
    __asm__ __volatile__(
        "ldr x30, [sp], #16\n"
        "ldp x28, x29, [sp], #16\n"
        "ldp x26, x27, [sp], #16\n"
        "ldp x24, x25, [sp], #16\n"
        "ldp x22, x23, [sp], #16\n"
        "ldp x20, x21, [sp], #16\n"
        "ldp x18, x19, [sp], #16\n"
        "ldp x16, x17, [sp], #16\n"
        "ldp x14, x15, [sp], #16\n"
        "ldp x12, x13, [sp], #16\n"
        "ldp x10, x11, [sp], #16\n"
        "ldp x8, x9, [sp], #16\n"
        "ldp x6, x7, [sp], #16\n"
        "ldp x4, x5, [sp], #16\n"
        "ldp x2, x3, [sp], #16\n"
        "ldp x0, x1, [sp], #16\n"
    );
    #else
    __asm__ __volatile__(
        "pop {r0-r12}\n"
    );
    #endif
    __asm__ __volatile__(
        ".global testcase_end\n"
        "testcase_end:\n"
    );
    cpu_time_end = current->se.sum_exec_runtime;
    end_tm = ktime_get_boottime_ns();
    printk(KERN_INFO "elapsed time = %lld nsec\n", (end_tm - start_tm));
    printk(KERN_INFO "cpu time = %lld nsec\n ",cpu_time_end-cpu_time_start);
    printk(KERN_INFO "start time = %lld\n", cpu_time_start);
    printk(KERN_INFO "end time = %lld\n", current->se.sum_exec_runtime);
    return 0;
}

void cleanup_module(void) {
    unregister_undef_hook(&uh);
    // printk(KERN_INFO "Goodbye world.\n");
}
#include <mach/mach_init.h>
#include <mach/mach_error.h>
#include <mach/mach_host.h>
#include <mach/vm_map.h>
#include <iostream>
#include <libproc.h>

using namespace std;

#include <sys/sysctl.h>

// int psutil_proc_pidinfo(long pid, int flavor, uint64_t arg, void *pti, int size);
//
// int psutil_proc_pidinfo(long pid, int flavor, uint64_t arg, void *pti, int size) {
//     errno = 0;
//     int ret = proc_pidinfo((int)pid, flavor, arg, pti, size);
//     // if ((ret <= 0) || ((unsigned long)ret < sizeof(pti))) {
//     //     psutil_raise_for_pid(pid, "proc_pidinfo()");
//     //     return 0;
//     // }
//     return ret;
// }

/*
https://opensource.apple.com/source/xnu/xnu-1228/bsd/sys/proc_info.h
struct proc_taskinfo {
    uint64_t        pti_virtual_size;   // virtual memory size (bytes)
    uint64_t        pti_resident_size;  // resident memory size (bytes)
    uint64_t        pti_total_user;        // total time
    uint64_t        pti_total_system;
    uint64_t        pti_threads_user;    // existing threads only
    uint64_t        pti_threads_system;
    int32_t         pti_policy;        // default policy for new threads
    int32_t            pti_faults;        // number of page faults
    int32_t            pti_pageins;    // number of actual pageins
    int32_t            pti_cow_faults;    // number of copy-on-write faults
    int32_t            pti_messages_sent;    // number of messages sent
    int32_t            pti_messages_received; // number of messages received
    int32_t            pti_syscalls_mach;  // number of mach system calls
    int32_t            pti_syscalls_unix;  // number of unix system calls
    int32_t            pti_csw;            // number of context switches
    int32_t            pti_threadnum;        // number of threads in the task
    int32_t            pti_numrunning;        // number of running threads
    int32_t            pti_priority;        // task priority
}

struct proc_threadinfo {
    uint64_t        pth_user_time;      // user run time
    uint64_t        pth_system_time;    // system run time
    int32_t            pth_cpu_usage;      // scaled cpu usage percentage
    int32_t            pth_policy;        // scheduling policy in effect
    int32_t            pth_run_state;      // run state (see below)
    int32_t            pth_flags;          // various flags (see below)
    int32_t            pth_sleep_time;     // number of seconds that thread
    int32_t            pth_curpri;        // cur priority
    int32_t            pth_priority;        //  priority
    int32_t            pth_maxpriority;        // max priority
    char *            pth_name[64];        // thread name, if any
};
*/

void pidtaskinfo(long pid) {
    struct proc_taskinfo pti;
    struct proc_threadinfo pthi;

    proc_pidinfo(pid, PROC_PIDTHREADINFO, 0, &pthi, sizeof(pthi));
    cout << "pth_cpu_usage; " << pthi.pth_cpu_usage << endl;

    // if (psutil_proc_pidinfo(pid, PROC_PIDTASKINFO, 0, &pti, sizeof(pti)) <= 0)
    if (proc_pidinfo(pid, PROC_PIDTASKINFO, 0, &pti, sizeof(pti)) <= 0)
        cout << "error" << endl;
    else
        // cout << (float)pti.pti_total_user / 1000000000.0 << endl;
        cout << (float)pti.pti_total_system / 1000000000.0 << endl;
        // cout << pti.pti_virtual_size << endl;
        cout << pti.pti_resident_size / 1.0E6 << endl;

    // return Py_BuildValue(
    //     "(ddKKkkkk)",
    //     (float)pti.pti_total_user / 1000000000.0,     // (float) cpu user time
    //     (float)pti.pti_total_system / 1000000000.0,   // (float) cpu sys time
    //     // Note about memory: determining other mem stats on macOS is a mess:
    //     // http://www.opensource.apple.com/source/top/top-67/libtop.c?txt
    //     // I just give up.
    //     // struct proc_regioninfo pri;
    //     // psutil_proc_pidinfo(pid, PROC_PIDREGIONINFO, 0, &pri, sizeof(pri))
    //     pti.pti_resident_size,  // (uns long long) rss
    //     pti.pti_virtual_size,   // (uns long long) vms
    //     pti.pti_faults,         // (uns long) number of page faults (pages)
    //     pti.pti_pageins,        // (uns long) number of actual pageins (pages)
    //     pti.pti_threadnum,      // (uns long) num threads
    //     // Unvoluntary value seems not to be available;
    //     // pti.pti_csw probably refers to the sum of the two;
    //     // getrusage() numbers seems to confirm this theory.
    //     pti.pti_csw             // (uns long) voluntary ctx switches
    // );
}

// float CalculateCPULoad(unsigned long long idleTicks, unsigned long long totalTicks);
//
// static unsigned long long _previousTotalTicks = 0;
// static unsigned long long _previousIdleTicks = 0;

// // Returns 1.0f for "CPU fully pinned", 0.0f for "CPU idle", or somewhere in between
// // You'll need to call this at regular intervals, since it measures the load between
// // the previous call and the current one.
// float GetCPULoad()
// {
//    host_cpu_load_info_data_t cpuinfo;
//    mach_msg_type_number_t count = HOST_CPU_LOAD_INFO_COUNT;
//    if (host_statistics(mach_host_self(), HOST_CPU_LOAD_INFO, (host_info_t)&cpuinfo, &count) == KERN_SUCCESS)
//    {
//       unsigned long long totalTicks = 0;
//       for(int i=0; i<CPU_STATE_MAX; i++) totalTicks += cpuinfo.cpu_ticks[i];
//       return CalculateCPULoad(cpuinfo.cpu_ticks[CPU_STATE_IDLE], totalTicks);
//    }
//    else return -1.0f;
// }
//
// float CalculateCPULoad(unsigned long long idleTicks, unsigned long long totalTicks)
// {
//   unsigned long long totalTicksSinceLastTime = totalTicks-_previousTotalTicks;
//   unsigned long long idleTicksSinceLastTime  = idleTicks-_previousIdleTicks;
//   float ret = 1.0f-((totalTicksSinceLastTime > 0) ? ((float)idleTicksSinceLastTime)/totalTicksSinceLastTime : 0);
//   _previousTotalTicks = totalTicks;
//   _previousIdleTicks  = idleTicks;
//   return ret;
// }



int main(){
    // GetCPULoad();
    // cout << psutil_proc_pidtaskinfo_oneshot(342) << endl;
    pidtaskinfo(1283);

    int num;
    size_t size = sizeof(int);
    sysctlbyname("hw.logicalcpu", &num, &size, NULL, 2);

    cout << "num logical cpu: " << num << endl;

    sysctlbyname("hw.physicalcpu", &num, &size, NULL, 2);
    cout << "num physical cpu: " << num << endl;
}

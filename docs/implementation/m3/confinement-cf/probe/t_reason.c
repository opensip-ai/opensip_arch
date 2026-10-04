/* CF-P side test: read the exit reason of a zombie child (PROC_PIDEXITREASONBASICINFO = 25, private flavor). */
#include <libproc.h>
#include <spawn.h>
#include <stdio.h>
#include <sys/proc_info.h>
#include <sys/wait.h>
extern char **environ;
int main(int argc, char **argv) {
    pid_t p; if (posix_spawn(&p, argv[1], NULL, NULL, argv + 1, environ)) return 1;
    siginfo_t si; waitid(P_PID, p, &si, WEXITED | WNOWAIT);
    struct proc_exitreasonbasicinfo b = {0};
    int r = proc_pidinfo(p, 25, 0, &b, sizeof b);
    printf("child si_code=%d si_status=%d exitreason rc=%d namespace=%u code=0x%llx flags=0x%llx\n", si.si_code, si.si_status, r, b.beri_namespace, b.beri_code, b.beri_flags);
    waitpid(p, NULL, 0); return 0;
}

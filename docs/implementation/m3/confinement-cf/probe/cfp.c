/*
 * cfp.c - CF-P confinement-feasibility probe (OpenSIP M3-CF). Throwaway, macOS only.
 * A trivial test child; no provider, no repository bytes. Not product code.
 *
 *   cfp harness <self> <base> <tcp-closed-port-hint ignored> [node]   host side (unconfined)
 *   cfp launch  <api> <profile> <scratch> <closure> <target> argv...  single-threaded launcher
 *   cfp child   <set> <hostpid> <sibpid> <rundir> <tcpport> <udpport>  the confined test child
 *   cfp sleeper                                                        same-user sibling with a canary
 */
#include <sandbox.h> /* only to surface the SDK deprecation diagnostics */
#include <arpa/inet.h>
#include <dirent.h>
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <libproc.h>
#include <mach/mach.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <servers/bootstrap.h>
#include <signal.h>
#include <spawn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/event.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/sysctl.h>
#include <sys/time.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <sys/xattr.h>
#include <unistd.h>

/* Exported by libsystem_sandbox (SDK27 libsystem_sandbox.tbd:42,65-66), declared in no SDK27 header. */
int sandbox_init_with_parameters(const char *profile, uint64_t flags, const char *const parameters[], char **errorbuf);
int sandbox_check(pid_t pid, const char *operation, int type, ...);
extern const char kSBXProfileNoNetwork[]; /* exported (tbd:27-28), no longer declared */

extern char **environ;
static const char *g_self;

/* ------------------------------------------------------------------ child */

static void rep(const char *t, int rc, int err, const char *detail) {
    if (rc >= 0)
        printf("T %-26s ALLOWED %s\n", t, detail ? detail : "");
    else
        printf("T %-26s %s errno=%d(%s) %s\n", t, (err == EPERM || err == EACCES) ? "DENIED " : "FAILED ",
               err, strerror(err), detail ? detail : "");
    fflush(stdout);
}

static int procargs_has(int which, pid_t pid, const char *needle, int *err, size_t *len) {
    int mib[3] = {CTL_KERN, which, pid};
    char buf[65536];
    size_t sz = sizeof buf;
    if (sysctl(mib, 3, buf, &sz, NULL, 0) != 0) { *err = errno; *len = 0; return -1; }
    *len = sz;
    for (size_t i = 0; i + strlen(needle) <= sz; i++)
        if (memcmp(buf + i, needle, strlen(needle)) == 0) return 1;
    return 0;
}

static void env_probe(const char *label, int which, pid_t pid, const char *needle) {
    int err = 0; size_t len = 0;
    int r = procargs_has(which, pid, needle, &err, &len);
    char d[128];
    snprintf(d, sizeof d, "pid=%d bytes=%zu canary=%s", pid, len, r == 1 ? "FOUND" : r == 0 ? "absent" : "n/a");
    rep(label, r < 0 ? -1 : 0, err, d);
}

static void net_tests(int tcpport, int udpport, const char *rundir) {
    struct sockaddr_in a = {.sin_len = sizeof a, .sin_family = AF_INET, .sin_port = htons(tcpport)};
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    int s = socket(AF_INET, SOCK_STREAM, 0);
    rep("net.tcp.socket", s, errno, "");
    if (s >= 0) { int rc = connect(s, (void *)&a, sizeof a); rep("net.tcp.connect.closed", rc, errno, "127.0.0.1 closed port"); close(s); }
    int u = socket(AF_INET, SOCK_DGRAM, 0);
    rep("net.udp.socket", u, errno, "");
    if (u >= 0) { a.sin_port = htons(udpport); ssize_t n = sendto(u, "x", 1, 0, (void *)&a, sizeof a); rep("net.udp.sendto.closed", n < 0 ? -1 : 0, errno, "1 byte to 127.0.0.1 closed port"); close(u); }
    struct addrinfo h = {.ai_family = AF_UNSPEC, .ai_socktype = SOCK_STREAM}, *res = NULL;
    int g = getaddrinfo("example.com", "80", &h, &res);
    char d[160]; int cnt = 0;
    for (struct addrinfo *p = res; p; p = p->ai_next) cnt++;
    snprintf(d, sizeof d, "gai=%d(%s) addrs=%d", g, g ? gai_strerror(g) : "ok", cnt);
    printf("T %-26s %s %s\n", "net.dns.example.com", g == 0 ? "ALLOWED" : "DENIED?", d); fflush(stdout);
    if (res) freeaddrinfo(res);
    int x = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un un = {.sun_family = AF_UNIX};
    { const char *b = strrchr(rundir, '/'); snprintf(un.sun_path, sizeof un.sun_path, "%.*s/%.3s.sock", (int)(b - rundir), rundir, b + 1); }
    if (x >= 0) { int rc = connect(x, (void *)&un, sizeof un); rep("net.unix.connect.listener", rc, errno, "test-created pathname listener"); close(x); }
    const char *svcs[] = {"com.apple.dnssd.service", "com.apple.SystemConfiguration.configd"};
    for (int i = 0; i < 2; i++) {
        mach_port_t p = MACH_PORT_NULL;
        kern_return_t kr = bootstrap_look_up(bootstrap_port, svcs[i], &p);
        printf("T %-26s %s kr=%d %s\n", "mach.lookup", kr == KERN_SUCCESS ? "ALLOWED" : "DENIED?", kr, svcs[i]); fflush(stdout);
        if (p != MACH_PORT_NULL) mach_port_deallocate(mach_task_self(), p);
    }
}

static int wfile(const char *p, int flags, const char *bytes) {
    int fd = open(p, flags, 0600);
    if (fd < 0) return -1;
    ssize_t n = write(fd, bytes, strlen(bytes));
    int e = errno; close(fd); errno = e;
    return n < 0 ? -1 : 0;
}

static void write_tests(const char *rundir) {
    char o[1024], ex[1024];
    snprintf(o, sizeof o, "%s/outside", rundir);
    snprintf(ex, sizeof ex, "%s/existing.txt", o);
    char p[1100];
    rep("wr.in.create", wfile("inside.txt", O_CREAT | O_WRONLY | O_TRUNC, "IN\n"), errno, "cwd=scratch");
    rep("wr.in.mkdir", mkdir("subdir", 0700), errno, "");
    rep("wr.devnull", wfile("/dev/null", O_WRONLY, "x"), errno, "");
    snprintf(p, sizeof p, "%s/new.txt", o);
    rep("wr.out.create", wfile(p, O_CREAT | O_WRONLY | O_EXCL, "NEW\n"), errno, "");
    rep("wr.out.open_trunc", wfile(ex, O_WRONLY | O_TRUNC, ""), errno, "");
    rep("wr.out.append", wfile(ex, O_WRONLY | O_APPEND, "APPENDED\n"), errno, "");
    rep("wr.out.truncate", truncate(ex, 0), errno, "");
    rep("wr.out.chmod", chmod(ex, 0600), errno, "");
    rep("wr.out.utimes", utimes(ex, NULL), errno, "");
    rep("wr.out.setxattr", setxattr(ex, "com.cfp.test", "v", 1, 0, 0), errno, "");
    snprintf(p, sizeof p, "%s/dir", o);
    rep("wr.out.mkdir", mkdir(p, 0700), errno, "");
    snprintf(p, sizeof p, "%s/sl", o);
    rep("wr.out.symlink_create", symlink("x", p), errno, "");
    snprintf(p, sizeof p, "%s/moved.txt", o);
    rep("wr.rename.in_to_out", rename("inside.txt", p), errno, "scratch/inside.txt -> outside");
    rep("wr.symlink.write_through", wfile("link", O_WRONLY | O_APPEND, "VIA-SYMLINK\n"), errno, "scratch/link -> outside/existing.txt");
    int lr = link(ex, "hl");
    rep("wr.hardlink.create", lr, errno, "link(outside/existing.txt, scratch/hl)");
    if (lr == 0) rep("wr.hardlink.write", wfile("hl", O_WRONLY | O_APPEND, "VIA-HARDLINK\n"), errno, "write scratch/hl");
    rep("wr.prelinked.write", wfile("prehl", O_WRONLY | O_APPEND, "VIA-PRELINK\n"), errno, "host-planted scratch/prehl == outside/prelinked.txt");
    snprintf(p, sizeof p, "%s/victim.txt", o);
    rep("wr.rename.out_to_in", rename(p, "stolen.txt"), errno, "outside/victim.txt -> scratch");
    rep("wr.out.unlink", unlink(ex), errno, "");
    char buf[128] = {0};
    snprintf(p, sizeof p, "%s/readable.txt", o);
    int fd = open(p, O_RDONLY);
    ssize_t n = fd >= 0 ? read(fd, buf, sizeof buf - 1) : -1;
    int e = errno; if (fd >= 0) close(fd);
    rep("rd.out.file", n < 0 ? -1 : 0, e, strstr(buf, "cfp-file-canary") ? "canary bytes READ (reads unrestricted)" : "no canary");
}

static void state_tests(void) {
    printf("T %-26s INFO   value=%d\n", "st.sandbox_check", sandbox_check(getpid(), NULL, 0));
    char cwd[1024]; getcwd(cwd, sizeof cwd);
    printf("T %-26s INFO   pid=%d ppid=%d sid=%d pgid=%d cwd=%s\n", "st.ids", getpid(), getppid(), getsid(0), getpgid(0), cwd);
    int t = open("/dev/tty", O_RDWR);
    rep("st.dev_tty", t, errno, "controlling terminal");
    if (t >= 0) close(t);
    char fds[512] = ""; size_t off = 0;
    for (int fd = 0; fd < 4096; fd++) if (fcntl(fd, F_GETFD) != -1) off += snprintf(fds + off, sizeof fds - off, "%d ", fd);
    printf("T %-26s INFO   open=[%s]\n", "st.fds", fds);
    struct sigaction sa; sigaction(SIGPIPE, NULL, &sa);
    sigset_t m; sigprocmask(SIG_BLOCK, NULL, &m);
    struct rlimit rl; getrlimit(RLIMIT_CORE, &rl);
    printf("T %-26s INFO   sigpipe=%s sigusr2_blocked=%d rlimit_core=%llu/%llu\n", "st.signals_rlimit",
           sa.sa_handler == SIG_DFL ? "default" : sa.sa_handler == SIG_IGN ? "IGNORED" : "handler",
           sigismember(&m, SIGUSR2), (unsigned long long)rl.rlim_cur, (unsigned long long)rl.rlim_max);
    for (char **e = environ; *e; e++) printf("E %s\n", *e);
    fflush(stdout);
}

static void env_tests(pid_t host, pid_t sib) {
    env_probe("env.procargs2.self", KERN_PROCARGS2, getpid(), "OPENSIP_PROBE_CLASS=");
    env_probe("env.procargs2.host", KERN_PROCARGS2, host, "CFP_CANARY_HOST=");
    env_probe("env.procargs2.sibling", KERN_PROCARGS2, sib, "CFP_CANARY_SIB=");
    env_probe("env.procargs.host", KERN_PROCARGS, host, "CFP_CANARY_HOST=");
    struct proc_bsdinfo bi;
    int r = proc_pidinfo(host, PROC_PIDTBSDINFO, 0, &bi, sizeof bi);
    rep("env.pidinfo.host", r > 0 ? 0 : -1, errno, "proc_pidinfo PROC_PIDTBSDINFO");
    char path[PROC_PIDPATHINFO_MAXSIZE];
    r = proc_pidpath(host, path, sizeof path);
    rep("env.pidpath.host", r > 0 ? 0 : -1, errno, "");
    r = proc_listpids(PROC_ALL_PIDS, 0, NULL, 0);
    char d[64]; snprintf(d, sizeof d, "bytes=%d", r);
    rep("env.listpids.all", r > 0 ? 0 : -1, errno, d);
}

static void proc_tests(pid_t host, int provider) {
    rep("sig.kill.host.SIGUSR1", kill(host, SIGUSR1), errno, "");
    rep("sig.kill.host.0", kill(host, 0), errno, "");
    rep("sig.kill.self.0", kill(getpid(), 0), errno, "");
    char *err = NULL;
    int rc = sandbox_init("(version 1)(allow default)", 0, &err);
    printf("T %-26s %s rc=%d err=%s\n", "proc.reinit.sandbox_init", rc == 0 ? "ALLOWED" : "REFUSED", rc, err ? err : "(null)");
    if (err) sandbox_free_error(err);
    err = NULL;
    const char *pp[] = {NULL};
    rc = sandbox_init_with_parameters("(version 1)(allow default)", 0, pp, &err);
    printf("T %-26s %s rc=%d err=%s\n", "proc.reinit.with_params", rc == 0 ? "ALLOWED" : "REFUSED", rc, err ? err : "(null)");
    if (err) sandbox_free_error(err);
    fflush(stdout);
    pid_t f = fork();
    if (f == 0) _exit(0);
    rep("proc.fork", f < 0 ? -1 : 0, errno, "");
    if (f > 0) waitpid(f, NULL, 0);
    pid_t sp; char *av[] = {(char *)g_self, "noop", NULL};
    rc = posix_spawn(&sp, g_self, NULL, NULL, av, environ);
    rep("proc.posix_spawn.target", rc ? -1 : 0, rc, "spawn of the TARGET binary itself");
    if (rc == 0) waitpid(sp, NULL, 0);
    char *av2[] = {"true", NULL};
    rc = posix_spawn(&sp, "/usr/bin/true", NULL, NULL, av2, environ);
    rep("proc.posix_spawn.other", rc ? -1 : 0, rc, "/usr/bin/true");
    if (rc == 0) waitpid(sp, NULL, 0);
    rep("proc.setsid", setsid(), errno, "already a session leader (SETSID): EPERM is not Seatbelt");
    if (provider) {
        char *ev[] = {"echo", "EXEC-OTHER-RAN", NULL};
        execve("/bin/echo", ev, environ);
        rep("proc.execve.other", -1, errno, "/bin/echo");
    }
}

static void tool_tests(const char *rundir, char **argv) {
    pid_t g = fork();
    if (g == 0) {
        printf("T %-26s INFO   gc pid=%d pgid=%d\n", "tool.gc.before", getpid(), getpgid(0)); fflush(stdout);
        pid_t s = setsid();
        rep("tool.gc.setsid", s, errno, "Seatbelt has no setsid filter if ALLOWED");
        printf("T %-26s INFO   gc sid=%d pgid=%d\n", "tool.gc.after", getsid(0), getpgid(0)); fflush(stdout);
        _exit(0);
    }
    rep("tool.fork", g < 0 ? -1 : 0, errno, "");
    if (g > 0) waitpid(g, NULL, 0);
    g = fork();
    if (g == 0) {
        char *av[] = {(char *)g_self, "child", "inherit", argv[3], argv[4], (char *)rundir, argv[6], argv[7], NULL};
        execve(g_self, av, environ);
        rep("tool.gc.exec.closure", -1, errno, ""); _exit(1);
    }
    if (g > 0) waitpid(g, NULL, 0);
    g = fork();
    if (g == 0) {
        char *ev[] = {"echo", "GC-EXEC-OUTSIDE-RAN", NULL};
        execve("/bin/echo", ev, environ);
        rep("tool.gc.exec.outside", -1, errno, "/bin/echo outside CLOSURE_ROOT"); _exit(1);
    }
    if (g > 0) waitpid(g, NULL, 0);
}

static int child_main(int argc, char **argv) {
    if (argc < 8) return 2;
    const char *set = argv[2];
    pid_t host = atoi(argv[3]), sib = atoi(argv[4]);
    const char *rundir = argv[5];
    int tcp = atoi(argv[6]), udp = atoi(argv[7]);
    printf("C set=%s exe=%s\n", set, g_self); fflush(stdout);
    if (!strcmp(set, "provider")) {
        state_tests(); net_tests(tcp, udp, rundir); write_tests(rundir); env_tests(host, sib); proc_tests(host, 1);
    } else if (!strcmp(set, "control")) {
        state_tests(); net_tests(tcp, udp, rundir); write_tests(rundir); env_tests(host, sib); proc_tests(host, 0);
    } else if (!strcmp(set, "minimal")) {
        printf("T %-26s INFO   value=%d\n", "st.sandbox_check", sandbox_check(getpid(), NULL, 0));
        net_tests(tcp, udp, rundir);
        rep("wr.in.create", wfile("inside.txt", O_CREAT | O_WRONLY | O_TRUNC, "IN\n"), errno, "cwd=scratch");
        char p[1100]; snprintf(p, sizeof p, "%s/outside/new.txt", rundir);
        rep("wr.out.create", wfile(p, O_CREAT | O_WRONLY | O_EXCL, "NEW\n"), errno, "");
    } else if (!strcmp(set, "link")) {
        char ex[1100]; snprintf(ex, sizeof ex, "%s/outside/existing.txt", rundir);
        rep("lnk.hardlink.out_to_in", link(ex, "hl"), errno, "link(outside/existing.txt, scratch/hl)");
        rep("lnk.hardlink.in_to_in", wfile("a.txt", O_CREAT | O_WRONLY, "A") < 0 ? -1 : link("a.txt", "b.txt"), errno, "link(scratch/a, scratch/b)");
        char d[1100]; snprintf(d, sizeof d, "%s/outside/c.txt", rundir);
        rep("lnk.hardlink.in_to_out", link("a.txt", d), errno, "link(scratch/a, outside/c)");
    } else if (!strcmp(set, "env")) {
        printf("T %-26s INFO   value=%d\n", "st.sandbox_check", sandbox_check(getpid(), NULL, 0));
        env_tests(host, sib);
    } else if (!strcmp(set, "tool")) {
        printf("T %-26s INFO   value=%d\n", "st.sandbox_check", sandbox_check(getpid(), NULL, 0)); fflush(stdout);
        tool_tests(rundir, argv);
    } else if (!strcmp(set, "inherit")) {
        printf("T %-26s INFO   value=%d pid=%d (exec'd grandchild)\n", "inh.sandbox_check", sandbox_check(getpid(), NULL, 0), getpid());
        struct sockaddr_in a = {.sin_len = sizeof a, .sin_family = AF_INET, .sin_port = htons(tcp)};
        inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
        int s = socket(AF_INET, SOCK_STREAM, 0);
        rep("inh.net.tcp.connect", s < 0 ? -1 : connect(s, (void *)&a, sizeof a), errno, "");
        char p[1100]; snprintf(p, sizeof p, "%s/outside/inh.txt", rundir);
        rep("inh.wr.out.create", wfile(p, O_CREAT | O_WRONLY | O_EXCL, "INH\n"), errno, "");
        rep("inh.wr.in.create", wfile("inh-inside.txt", O_CREAT | O_WRONLY | O_TRUNC, "IN\n"), errno, "");
        pid_t f = fork(); if (f == 0) _exit(0);
        rep("inh.fork", f < 0 ? -1 : 0, errno, "tool profile allows fork");
        if (f > 0) waitpid(f, NULL, 0);
    } else if (!strcmp(set, "grouptree")) {
        pid_t g1 = fork();
        if (g1 == 0) { for (;;) pause(); }
        int pfd[2]; pipe(pfd);
        pid_t g2 = fork();
        if (g2 == 0) { setsid(); char c = 1; write(pfd[1], &c, 1); for (;;) pause(); }
        char c; read(pfd[0], &c, 1);
        printf("READY gc1=%d gc2=%d\n", g1, g2); fflush(stdout);
        for (;;) pause();
    }
    printf("C done\n"); fflush(stdout);
    return 0;
}

/* --------------------------------------------------------------- launcher */

static char *slurp(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) return NULL;
    char *b = calloc(1, 65537);
    size_t n = fread(b, 1, 65536, f);
    fclose(f); b[n] = 0;
    return b;
}

/* For sandbox_init (no parameter support): textually replace (param "K") with "V". */
static char *subst(const char *t, const char *k, const char *v) {
    char pat[64]; snprintf(pat, sizeof pat, "(param \"%s\")", k);
    char *out = calloc(1, strlen(t) * 2 + 4096); char *o = out;
    for (const char *p = t; *p;) {
        if (!strncmp(p, pat, strlen(pat))) { o += sprintf(o, "\"%s\"", v); p += strlen(pat); }
        else *o++ = *p++;
    }
    return out;
}

static int launch_main(int argc, char **argv) {
    if (argc < 8) return 2;
    const char *api = argv[2], *prof = argv[3], *scratch = argv[4], *closure = argv[5], *target = argv[6];
    struct rlimit rl = {0, 0}; setrlimit(RLIMIT_CORE, &rl);
    char *err = NULL; int rc = 0, e = 0;
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    if (!strcmp(api, "none")) {
        rc = 0;
    } else if (!strcmp(api, "named")) {
        rc = sandbox_init(kSBXProfileNoNetwork, SANDBOX_NAMED, &err); e = errno;
    } else {
        char *text = slurp(prof);
        if (!text) { printf("L profile unreadable\n"); return 111; }
        if (!strcmp(api, "init")) {
            char *t1 = subst(text, "SCRATCH", scratch), *t2 = subst(t1, "TARGET", target), *t3 = subst(t2, "CLOSURE_ROOT", closure);
            rc = sandbox_init(t3, 0, &err); e = errno;
        } else if (!strcmp(api, "init-raw")) {
            rc = sandbox_init(text, 0, &err); e = errno;
        } else if (!strcmp(api, "initp")) {
            const char *params[] = {"SCRATCH", scratch, "TARGET", target, "CLOSURE_ROOT", closure, NULL};
            rc = sandbox_init_with_parameters(text, 0, params, &err); e = errno;
        } else if (!strcmp(api, "initp-noparams")) {
            rc = sandbox_init_with_parameters(text, 0, NULL, &err); e = errno;
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    long us = (t1.tv_sec - t0.tv_sec) * 1000000L + (t1.tv_nsec - t0.tv_nsec) / 1000;
    printf("L api=%s rc=%d errno=%d apply_us=%ld err=%s sandbox_check=%d\n", api, rc, rc ? e : 0, us, err ? err : "(null)", sandbox_check(getpid(), NULL, 0));
    fflush(stdout);
    if (err) sandbox_free_error(err);
    if (rc != 0) return 111;
    execve(target, argv + 7, environ);
    printf("L execve(%s) failed errno=%d(%s)\n", target, errno, strerror(errno));
    return 112;
}

/* ---------------------------------------------------------------- harness */

static volatile sig_atomic_t g_usr1;
static void on_usr1(int s) { (void)s; g_usr1++; }

static void wtext(const char *p, const char *s, mode_t m) {
    int fd = open(p, O_CREAT | O_WRONLY | O_TRUNC, m); write(fd, s, strlen(s)); close(fd); chmod(p, m);
}

static int closed_port(int type) {
    int s = socket(AF_INET, type, 0);
    struct sockaddr_in a = {.sin_len = sizeof a, .sin_family = AF_INET};
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    bind(s, (void *)&a, sizeof a);
    socklen_t l = sizeof a; getsockname(s, (void *)&a, &l);
    close(s);
    return ntohs(a.sin_port);
}

static void print_outside(const char *o) {
    char ex[1100]; snprintf(ex, sizeof ex, "%s/existing.txt", o);
    struct stat st; char buf[256] = {0};
    if (stat(ex, &st) == 0) {
        int fd = open(ex, O_RDONLY); read(fd, buf, sizeof buf - 1); close(fd);
        for (char *c = buf; *c; c++) if (*c == '\n') *c = '|';
        printf("H post existing.txt mode=%o bytes=\"%s\"\n", st.st_mode & 07777, buf);
    } else printf("H post existing.txt MISSING errno=%d\n", errno);
    snprintf(ex, sizeof ex, "%s/prelinked.txt", o);
    memset(buf, 0, sizeof buf);
    int fd = open(ex, O_RDONLY); if (fd >= 0) { read(fd, buf, sizeof buf - 1); close(fd); }
    for (char *c = buf; *c; c++) if (*c == '\n') *c = '|';
    printf("H post prelinked.txt bytes=\"%s\"\n", buf);
    DIR *d = opendir(o); struct dirent *de; printf("H post outside/ entries:");
    while ((de = readdir(d))) if (de->d_name[0] != '.') printf(" %s", de->d_name);
    printf("\n"); closedir(d);
}

struct run { const char *name, *api, *profile, *set, *target; char *const *targv; int noncanon; };

static pid_t g_sib;
static int g_tcp, g_udp;

static void run_one(const char *base, const char *closure, struct run *r) {
    char rd[1024], sc[1100], o[1100], p[1200], prof[1100];
    snprintf(rd, sizeof rd, "%s/%s", base, r->name);
    snprintf(sc, sizeof sc, "%s/scratch", rd);
    snprintf(o, sizeof o, "%s/outside", rd);
    mkdir(rd, 0700); mkdir(sc, 0700); mkdir(o, 0700);
    snprintf(p, sizeof p, "%s/existing.txt", o); wtext(p, "ORIGINAL\n", 0644);
    snprintf(p, sizeof p, "%s/readable.txt", o); wtext(p, "cfp-file-canary-5be1\n", 0644);
    snprintf(p, sizeof p, "%s/victim.txt", o); wtext(p, "VICTIM\n", 0644);
    snprintf(p, sizeof p, "%s/prelinked.txt", o); wtext(p, "PRELINKED-ORIGINAL\n", 0644);
    char q[1200]; snprintf(q, sizeof q, "%s/prehl", sc); link(p, q);
    snprintf(p, sizeof p, "%s/existing.txt", o); snprintf(q, sizeof q, "%s/link", sc); symlink(p, q);
    int ls = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un un = {.sun_family = AF_UNIX}; snprintf(un.sun_path, sizeof un.sun_path, "%s/%.3s.sock", base, r->name); unlink(un.sun_path);
    bind(ls, (void *)&un, sizeof un); listen(ls, 8); fcntl(ls, F_SETFL, O_NONBLOCK);
    if (r->profile && strcmp(r->api, "named") && strcmp(r->api, "none")) {
        snprintf(prof, sizeof prof, "%s/profile.sb", rd); wtext(prof, r->profile, 0600);
    } else snprintf(prof, sizeof prof, "-");
    char scratch_arg[1100];
    if (r->noncanon && !strncmp(sc, "/private/var/", 13)) snprintf(scratch_arg, sizeof scratch_arg, "%s", sc + 8);
    else snprintf(scratch_arg, sizeof scratch_arg, "%s", sc);

    char hp[16], sp[16], tp[16], up[16];
    snprintf(hp, sizeof hp, "%d", getpid()); snprintf(sp, sizeof sp, "%d", g_sib);
    snprintf(tp, sizeof tp, "%d", g_tcp); snprintf(up, sizeof up, "%d", g_udp);
    char *av[32]; int n = 0;
    av[n++] = (char *)g_self; av[n++] = "launch"; av[n++] = (char *)r->api; av[n++] = prof;
    av[n++] = scratch_arg; av[n++] = (char *)closure; av[n++] = (char *)r->target;
    if (r->targv) { for (int i = 0; r->targv[i]; i++) av[n++] = r->targv[i]; }
    else { av[n++] = (char *)g_self; av[n++] = "child"; av[n++] = (char *)r->set; av[n++] = hp; av[n++] = sp; av[n++] = rd; av[n++] = tp; av[n++] = up; }
    av[n] = NULL;
    char *env[] = {"OPENSIP_PROBE_CLASS=provider", "LANG=C", NULL};

    int in[2], out[2], c3[2], c4[2];
    pipe(in); pipe(out); pipe(c3); pipe(c4);
    posix_spawnattr_t at; posix_spawnattr_init(&at);
    posix_spawnattr_setflags(&at, POSIX_SPAWN_SETSID | POSIX_SPAWN_CLOEXEC_DEFAULT | POSIX_SPAWN_SETSIGDEF | POSIX_SPAWN_SETSIGMASK);
    sigset_t all, none; sigfillset(&all); sigemptyset(&none);
    posix_spawnattr_setsigdefault(&at, &all); posix_spawnattr_setsigmask(&at, &none);
    posix_spawn_file_actions_t fa; posix_spawn_file_actions_init(&fa);
    posix_spawn_file_actions_adddup2(&fa, in[0], 0);
    posix_spawn_file_actions_adddup2(&fa, out[1], 1);
    posix_spawn_file_actions_adddup2(&fa, out[1], 2);
    posix_spawn_file_actions_adddup2(&fa, c3[0], 3);
    posix_spawn_file_actions_adddup2(&fa, c4[1], 4);
    posix_spawn_file_actions_addchdir(&fa, scratch_arg);
    g_usr1 = 0;
    printf("\n=== RUN %s api=%s set=%s target=%s scratch=%s\n", r->name, r->api, r->set, r->target, scratch_arg);
    fflush(stdout);
    pid_t pid; int rc = posix_spawn(&pid, g_self, &fa, &at, av, env);
    close(in[0]); close(in[1]); close(out[1]); close(c3[0]); close(c4[1]);
    if (rc) { printf("H posix_spawn rc=%d\n", rc); return; }
    printf("H spawned pid=%d getsid=%d getpgid=%d (expect both == pid)\n", pid, getsid(pid), getpgid(pid));
    int kq = kqueue(); struct kevent kev;
    EV_SET(&kev, pid, EVFILT_PROC, EV_ADD | EV_ONESHOT, NOTE_EXIT | NOTE_EXITSTATUS, 0, NULL);
    int kr = kevent(kq, &kev, 1, NULL, 0, NULL);
    printf("H kevent register EVFILT_PROC NOTE_EXIT|NOTE_EXITSTATUS rc=%d\n", kr);
    FILE *f = fdopen(out[0], "r"); char line[2048];
    int grouptree = r->set && !strcmp(r->set, "grouptree");
    while (fgets(line, sizeof line, f)) {
        printf("  | %s", line);
        if (grouptree && !strncmp(line, "READY", 5)) break;
    }
    fflush(stdout);
    if (grouptree) {
        pid_t g1 = 0, g2 = 0; sscanf(line, "READY gc1=%d gc2=%d", &g1, &g2);
        int pids[64]; int b = proc_listpids(PROC_PGRP_ONLY, pid, pids, sizeof pids);
        printf("H MX-7 proc_listpids(PROC_PGRP_ONLY,%d):", pid); for (int i = 0; i < b / (int)sizeof(int); i++) if (pids[i]) printf(" %d", pids[i]); printf("\n");
        b = proc_listchildpids(pid, pids, sizeof pids);
        printf("H MX-7 proc_listchildpids(%d): rc=%d ->", pid, b);
        for (int i = 0; i < b; i++) printf(" %d", pids[i]); printf("  (rc is a count of pids)\n");
        struct proc_bsdinfo bi1, bi2;
        proc_pidinfo(g2, PROC_PIDTBSDINFO, 0, &bi2, sizeof bi2);
        printf("H MX-7 gc2 pid=%d ppid=%u pgid=%u start=%llu.%06llu (escaped by setsid)\n", g2, bi2.pbi_ppid, bi2.pbi_pgid, bi2.pbi_start_tvsec, bi2.pbi_start_tvusec);
        proc_pidinfo(g1, PROC_PIDTBSDINFO, 0, &bi1, sizeof bi1);
        printf("H MX-7 gc1 pid=%d ppid=%u pgid=%u\n", g1, bi1.pbi_ppid, bi1.pbi_pgid);
        printf("H MX-7 killpg(%d,SIGKILL) rc=%d (root unreaped)\n", pid, killpg(pid, SIGKILL));
        struct timespec to = {10, 0}; struct kevent ev;
        int ne = kevent(kq, NULL, 0, &ev, 1, &to);
        printf("H MX-7 kevent n=%d fflags=0x%x data=0x%lx (NOTE_EXIT on unreaped root)\n", ne, ne > 0 ? ev.fflags : 0, ne > 0 ? (long)ev.data : 0L);
        siginfo_t si = {0}; int w = waitid(P_PID, pid, &si, WEXITED | WNOWAIT);
        printf("H MX-7 waitid(WNOWAIT) rc=%d si_code=%d(CLD_KILLED=%d) si_status=%d\n", w, si.si_code, CLD_KILLED, si.si_status);
        usleep(200000);
        b = proc_listpids(PROC_PGRP_ONLY, pid, pids, sizeof pids);
        printf("H MX-7 after group kill proc_listpids(PGRP):"); for (int i = 0; i < b / (int)sizeof(int); i++) if (pids[i]) printf(" %d", pids[i]); printf("\n");
        printf("H MX-7 killpg(%d,0) after kill, root zombie: rc=%d errno=%d\n", pid, killpg(pid, 0), errno);
        printf("H MX-7 kill(gc2,0) rc=%d (escaped gc2 still alive if 0)\n", kill(g2, 0));
        struct proc_bsdinfo bi3; int pr = proc_pidinfo(g2, PROC_PIDTBSDINFO, 0, &bi3, sizeof bi3);
        printf("H MX-7 gc2 now ppid=%u (1 = launchd, no subreaper) start-match=%d\n", pr > 0 ? bi3.pbi_ppid : 0,
               pr > 0 && bi3.pbi_start_tvsec == bi2.pbi_start_tvsec && bi3.pbi_start_tvusec == bi2.pbi_start_tvusec);
        if (pr > 0 && bi3.pbi_start_tvsec == bi2.pbi_start_tvsec && bi3.pbi_start_tvusec == bi2.pbi_start_tvusec)
            printf("H MX-7 best-effort kill(gc2,SIGKILL) after start-time check rc=%d\n", kill(g2, SIGKILL));
        usleep(200000);
        printf("H MX-7 kill(gc2,0) after cleanup rc=%d errno=%d\n", kill(g2, 0), errno);
        fclose(f);
    } else {
        fclose(f);
        struct timespec to = {20, 0}; struct kevent ev;
        int ne = kevent(kq, NULL, 0, &ev, 1, &to);
        printf("H kevent n=%d fflags=0x%x data(status)=0x%lx\n", ne, ne > 0 ? ev.fflags : 0, ne > 0 ? (long)ev.data : 0L);
        siginfo_t si = {0}; int w = waitid(P_PID, pid, &si, WEXITED | WNOWAIT);
        printf("H waitid(WNOWAIT) rc=%d si_code=%d si_status=%d; kill(pid,0)=%d (zombie still reserved)\n", w, si.si_code, si.si_status, kill(pid, 0));
    }
    int st = 0; struct rusage ru; pid_t wr = wait4(pid, &st, 0, &ru);
    printf("H wait4 rc=%d exited=%d code=%d signaled=%d sig=%d maxrss=%ld\n", wr, WIFEXITED(st), WEXITSTATUS(st), WIFSIGNALED(st), WTERMSIG(st), ru.ru_maxrss);
    int acc = 0; while (accept(ls, NULL, NULL) >= 0) acc++;
    close(ls); unlink(un.sun_path); close(kq); close(c3[1]); close(c4[0]);
    printf("H post host SIGUSR1 received=%d; unix listener accepted=%d\n", (int)g_usr1, acc);
    print_outside(o);
    fflush(stdout);
}

static int harness_main(int argc, char **argv) {
    if (argc < 4) return 2;
    const char *base = argv[3];
    const char *node = argc > 4 ? argv[4] : NULL;
    char closure[1024]; snprintf(closure, sizeof closure, "%s", g_self);
    *strrchr(closure, '/') = 0;
    signal(SIGUSR1, on_usr1);
    signal(SIGPIPE, SIG_IGN);
    sigset_t m; sigemptyset(&m); sigaddset(&m, SIGUSR2); sigprocmask(SIG_BLOCK, &m, NULL);
    Dl_info di; dladdr((void *)sandbox_init, &di);
    printf("H host pid=%d self=%s closure=%s\n", getpid(), g_self, closure);
    printf("H dlsym sandbox_init=%d sandbox_init_with_parameters=%d sandbox_check=%d sandbox_compile_string=%d sandbox_apply=%d image=%s\n",
           dlsym(RTLD_DEFAULT, "sandbox_init") != NULL, dlsym(RTLD_DEFAULT, "sandbox_init_with_parameters") != NULL,
           dlsym(RTLD_DEFAULT, "sandbox_check") != NULL, dlsym(RTLD_DEFAULT, "sandbox_compile_string") != NULL,
           dlsym(RTLD_DEFAULT, "sandbox_apply") != NULL, di.dli_fname);
    char *sav[] = {(char *)g_self, "sleeper", NULL};
    char *senv[] = {"CFP_CANARY_SIB=cfp-sib-canary-91c2", NULL};
    posix_spawn(&g_sib, g_self, NULL, NULL, sav, senv);
    g_tcp = closed_port(SOCK_STREAM); g_udp = closed_port(SOCK_DGRAM);
    printf("H sibling pid=%d tcp_closed=%d udp_closed=%d\n", g_sib, g_tcp, g_udp);

    char pdir[1100]; snprintf(pdir, sizeof pdir, "%s/provider.sb", closure);
    char tdir[1100]; snprintf(tdir, sizeof tdir, "%s/tool.sb", closure);
    char *provider = slurp(pdir), *tool = slurp(tdir);
    /* variants built by dropping tagged lines */
    char *drop(const char *t, const char *tag);
    char *nolink = drop(provider, ";@link"), *nomach = drop(provider, ";@mach");

    const char *only = getenv("CFP_ONLY");
    char *sysA = calloc(1, strlen(provider) + 256), *sysB = calloc(1, strlen(provider) + 256);
    sprintf(sysA, "%s(deny sysctl-read (sysctl-name \"kern.procargs2\") (sysctl-name \"kern.procargs\"))\n", provider);
    sprintf(sysB, "%s(deny sysctl-read (sysctl-name-prefix \"kern.procargs\"))\n", provider);
    struct run runs[] = {
        {"r01-control-none", "none", NULL, "control", g_self, NULL, 0},
        {"r02-provider-initp", "initp", provider, "provider", g_self, NULL, 0},
        {"r03-provider-init", "init", provider, "provider", g_self, NULL, 0},
        {"r04-named-nonetwork", "named", NULL, "minimal", g_self, NULL, 0},
        {"r05-provider-nolink", "initp", nolink, "provider", g_self, NULL, 0},
        {"r06-provider-nomach", "initp", nomach, "minimal", g_self, NULL, 0},
        {"r07-noncanon-scratch", "initp", provider, "minimal", g_self, NULL, 1},
        {"r08-tool-initp", "initp", tool, "tool", g_self, NULL, 0},
        {"r09-grouptree-tool", "initp", tool, "grouptree", g_self, NULL, 0},
        {"r10-err-syntax", "initp", "(version 1)(allow default)(deny network*", "minimal", g_self, NULL, 0},
        {"r11-err-unknown-op", "initp", "(version 1)(allow default)(deny process-setsid)", "minimal", g_self, NULL, 0},
        {"r12-err-missing-param", "initp", "(version 1)(allow default)(deny file-write* (require-not (subpath (param \"MISSING\"))))", "minimal", g_self, NULL, 0},
        {"r13-err-init-raw-param", "init-raw", provider, "minimal", g_self, NULL, 0},
        {"r17-procargs-deny-name", "initp", sysA, "env", g_self, NULL, 0},
        {"r18-procargs-deny-prefix", "initp", sysB, "env", g_self, NULL, 0},
        {"r19-link-deny-filelink-all", "initp", "(version 1)(allow default)(deny file-link)", "link", g_self, NULL, 0},
        {"r20-link-deny-write-outside", "initp", "(version 1)(allow default)(deny file-write* (require-not (subpath (param \"SCRATCH\"))))", "link", g_self, NULL, 0},
        {"r21-link-deny-filelink-in-scratch", "initp", "(version 1)(allow default)(deny file-link (subpath (param \"SCRATCH\")))", "link", g_self, NULL, 0},
        {"r22-link-deny-filelink-outside", "initp", "(version 1)(allow default)(deny file-link (require-not (subpath (param \"SCRATCH\"))))", "link", g_self, NULL, 0},
        {"r14-initp-null-params", "initp-noparams", "(version 1)(allow default)(deny network*)", "minimal", g_self, NULL, 0},
    };
    for (size_t i = 0; i < sizeof runs / sizeof runs[0]; i++)
        if (!only || strstr(runs[i].name, only)) run_one(base, closure, &runs[i]);
    if (node && (!only || strstr("r15-node", only))) {
        char ncl[1024]; snprintf(ncl, sizeof ncl, "%s", node); *strrchr(ncl, '/') = 0;
        char script[2048];
        snprintf(script, sizeof script,
                 "const fs=require('fs'),net=require('net'),cp=require('child_process');"
                 "console.log('NODE-OK '+process.version+' pid='+process.pid);"
                 "try{fs.writeFileSync('node-in.txt','x');console.log('NODE-WR-IN ok')}catch(e){console.log('NODE-WR-IN '+e.code)}"
                 "try{fs.writeFileSync('%s/r15-node-provider/outside/node-out.txt','x');console.log('NODE-WR-OUT ok')}catch(e){console.log('NODE-WR-OUT '+e.code)}"
                 "try{const r=cp.spawnSync('/bin/echo',['x']);console.log('NODE-SPAWN '+(r.error?r.error.code:'status='+r.status))}catch(e){console.log('NODE-SPAWN threw '+e.code)}"
                 "const s=net.connect(%d,'127.0.0.1');s.on('error',e=>console.log('NODE-NET '+e.code));s.on('connect',()=>{console.log('NODE-NET connected');s.destroy()});",
                 base, g_tcp);
        char *nargv[] = {(char *)node, "-e", script, NULL};
        struct run nr = {"r15-node-provider", "initp", provider, "node", node, nargv, 0};
        run_one(base, ncl, &nr);
        struct run nr2 = {"r16-node-nomach", "initp", nomach, "node", node, nargv, 0};
        snprintf(script, sizeof script, "console.log('NODE-OK nomach '+process.version)");
        run_one(base, ncl, &nr2);
    }
    kill(g_sib, SIGKILL); waitpid(g_sib, NULL, 0);
    printf("\nH done\n");
    return 0;
}

char *drop(const char *t, const char *tag) {
    char *out = calloc(1, strlen(t) + 1), *o = out;
    const char *p = t;
    while (*p) {
        const char *e = strchr(p, '\n'); size_t len = e ? (size_t)(e - p + 1) : strlen(p);
        if (!memmem(p, len, tag, strlen(tag))) { memcpy(o, p, len); o += len; }
        p += len;
    }
    return out;
}

int main(int argc, char **argv) {
    g_self = argv[0];
    if (argc >= 2 && !strcmp(argv[1], "child")) return child_main(argc, argv);
    if (argc >= 2 && !strcmp(argv[1], "launch")) return launch_main(argc, argv);
    if (argc >= 2 && !strcmp(argv[1], "harness")) { g_self = argv[2]; return harness_main(argc, argv); }
    if (argc >= 2 && !strcmp(argv[1], "sleeper")) { for (;;) pause(); }
    if (argc >= 2 && !strcmp(argv[1], "noop")) return 0;
    return 2;
}

// Independent confinement probe. Every attempted effect is reported on stderr.
// Modes:
//   effects OUT OUTSIDE_FILE OUTSIDE_DIR INPUT_DIR PORT  -> attempt reads/writes/links/network/exec
//   escape  INPUTS OUTPUT (VICTIM compiled in)          -> replace output root with symlink
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <dirent.h>
#include <unistd.h>

static void report(const char *what, int rc) {
  fprintf(stderr, "%s=%s\n", what, rc < 0 ? strerror(errno) : "ALLOWED");
}

static int unix_connect(const char *path, int type) {
  int s = socket(AF_UNIX, type, 0);
  if (s < 0) return -1;
  struct sockaddr_un a = {0}; a.sun_family = AF_UNIX;
  strncpy(a.sun_path, path, sizeof a.sun_path - 1);
  int rc = connect(s, (struct sockaddr *)&a, sizeof a);
  int saved = errno; close(s); errno = saved; return rc;
}

static void clear_dir(const char *dir) {
  DIR *d = opendir(dir); struct dirent *e; char p[4096];
  if (!d) return;
  while ((e = readdir(d))) {
    if (!strcmp(e->d_name, ".") || !strcmp(e->d_name, "..")) continue;
    snprintf(p, sizeof p, "%s/%s", dir, e->d_name);
    struct stat st;
    if (lstat(p, &st) == 0 && S_ISDIR(st.st_mode)) { clear_dir(p); rmdir(p); } else unlink(p);
  }
  closedir(d);
}

int main(int argc, char **argv) {
#ifdef VICTIM
  if (argc == 3) { // invoked by the real parent as generator INPUTS OUTPUT
    clear_dir(argv[2]);
    report("rmdir-output-root", rmdir(argv[2]));
    report("symlink-output-root-to-victim", symlink(VICTIM, argv[2]));
    return 0;
  }
#endif
  if (argc != 7 || strcmp(argv[1], "effects")) { fprintf(stderr, "usage\n"); return 2; }
  const char *out = argv[2], *outside = argv[3], *outdir = argv[4], *input = argv[5];
  int port = atoi(argv[6]); char p[4096]; char buf[64];
  int fd = open(outside, O_RDONLY); report("read-outside-file", fd); if (fd >= 0) close(fd);
  snprintf(p, sizeof p, "%s/written-by-child", outdir);
  fd = open(p, O_WRONLY | O_CREAT | O_EXCL, 0644); report("create-outside-file", fd); if (fd >= 0) close(fd);
  fd = open(outside, O_WRONLY | O_APPEND); report("write-existing-outside-file", fd); if (fd >= 0) close(fd);
  snprintf(p, sizeof p, "%s/written-by-child", input);
  fd = open(p, O_WRONLY | O_CREAT | O_EXCL, 0644); report("create-in-read-only-input", fd); if (fd >= 0) close(fd);
  fd = open("/Users/sb/.zshrc", O_RDONLY); report("read-home-dotfile", fd); if (fd >= 0) close(fd);
  fd = open("/private/etc/passwd", O_RDONLY); report("read-etc-passwd", fd); if (fd >= 0) close(fd);
  fd = open("/dev/tty", O_RDWR); report("open-dev-tty", fd); if (fd >= 0) close(fd);
  snprintf(p, sizeof p, "%s/hardlink", out); report("hardlink-outside-into-output", link(outside, p));
  snprintf(p, sizeof p, "%s/symlink", out); report("symlink-in-output", symlink(outside, p));
  fd = open(p, O_RDONLY); report("read-through-symlink", fd); if (fd >= 0) close(fd);
  snprintf(p, sizeof p, "%s/fifo", out); report("mkfifo-in-output", mkfifo(p, 0600));
  snprintf(p, sizeof p, "%s/regular", out);
  fd = open(p, O_WRONLY | O_CREAT, 0644); report("create-regular-in-output", fd); if (fd >= 0) { write(fd, "x", 1); close(fd); }
  report("rmdir-output-root(nonempty expected ENOTEMPTY or EPERM)", rmdir(out));
  report("chmod-output-root", chmod(out, 0700));
  int s = socket(AF_INET, SOCK_STREAM, 0); report("socket-inet", s);
  if (s >= 0) {
    struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    report("tcp-connect-loopback-listener", connect(s, (struct sockaddr *)&a, sizeof a)); close(s);
  }
  s = socket(AF_INET, SOCK_DGRAM, 0);
  if (s >= 0) {
    struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(53); a.sin_addr.s_addr = inet_addr("1.1.1.1");
    ssize_t n = sendto(s, "x", 1, 0, (struct sockaddr *)&a, sizeof a); report("udp-sendto-1.1.1.1:53", (int)n); close(s);
  }
  report("unix-dgram-connect-syslog", unix_connect("/private/var/run/syslog", SOCK_DGRAM));
  report("unix-stream-connect-mDNSResponder", unix_connect("/private/var/run/mDNSResponder", SOCK_STREAM));
  struct addrinfo *res = 0; int g = getaddrinfo("example.com", "80", 0, &res);
  fprintf(stderr, "getaddrinfo-example.com=%s\n", g == 0 ? "ALLOWED" : gai_strerror(g)); if (res) freeaddrinfo(res);
  pid_t pid = fork(); report("fork", pid);
  if (pid == 0) _exit(0);
  if (pid > 0) waitpid(pid, 0, 0);
  pid = fork();
  if (pid == 0) { execl("/bin/sh", "sh", "-c", "exit 0", (char *)0); _exit(127); }
  if (pid > 0) { int st; waitpid(pid, &st, 0); fprintf(stderr, "exec-bin-sh-child-status=%d\n", WIFEXITED(st) ? WEXITSTATUS(st) : -1); }
  report("kill-parent-SIGCONT", kill(getppid(), 0));
  report("kill-pid1", kill(1, 0));
  snprintf(buf, sizeof buf, "done");
  fprintf(stderr, "%s\n", buf);
  return 0;
}

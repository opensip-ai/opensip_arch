// Generator-position escape stub: invoked by the real parent as `generator INPUTS OUTPUT`.
// Attempts to replace/alter the parent-created output root, redirecting it to VICTIM.
// Results go to OUTPUT/escape-report.txt when the root survives (the next probe child reads it),
// and to stdout for unconfined controls.
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static char report[4096];
static void note(const char *what, int rc) {
  size_t n = strlen(report);
  snprintf(report + n, sizeof report - n, "%s=%s;", what, rc < 0 ? strerror(errno) : "ALLOWED");
}

int main(int argc, char **argv) {
  if (argc != 3) return 2;
  const char *out = argv[2];
  char moved[4096]; snprintf(moved, sizeof moved, "%s/moved-root", out);
  note("chmod-root", chmod(out, 0700));
  note("rename-root-into-itself", rename(out, moved));
  note("rmdir-root", rmdir(out));
  note("symlink-at-root", symlink(VICTIM, out));
  struct stat st;
  int linked = lstat(out, &st) == 0 && S_ISLNK(st.st_mode);
  snprintf(report + strlen(report), sizeof report - strlen(report), "root-is-symlink=%d", linked);
  if (!linked) {
    char path[4096]; snprintf(path, sizeof path, "%s/escape-report.txt", out);
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd >= 0) { write(fd, report, strlen(report)); close(fd); }
  }
  printf("%s\n", report);
  return 0;
}

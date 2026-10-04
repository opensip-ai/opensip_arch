/* CF-P side test: the documented SANDBOX_NAMED path of sandbox_init on macOS 27. */
#include <sandbox.h>
#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
extern const char kSBXProfileNoNetwork[], kSBXProfileNoInternet[], kSBXProfileNoWrite[], kSBXProfileNoWriteExceptTemporary[], kSBXProfilePureComputation[];
static void say(const char *s) { ssize_t a = write(1, s, strlen(s)); ssize_t b = write(2, s, strlen(s)); (void)a; (void)b; }
int main(int argc, char **argv) {
    char b[512];
    snprintf(b, sizeof b, "names: NoNetwork=%s NoInternet=%s NoWrite=%s NoWriteExceptTemporary=%s PureComputation=%s\n",
             kSBXProfileNoNetwork, kSBXProfileNoInternet, kSBXProfileNoWrite, kSBXProfileNoWriteExceptTemporary, kSBXProfilePureComputation);
    say(b);
    const char *n = argc > 1 && !strcmp(argv[1], "nointernet") ? kSBXProfileNoInternet : kSBXProfileNoNetwork;
    char *err = NULL;
    say("before sandbox_init\n");
    int rc = sandbox_init(n, SANDBOX_NAMED, &err);
    snprintf(b, sizeof b, "after sandbox_init(%s, SANDBOX_NAMED) rc=%d err=%s\n", n, rc, err ? err : "(null)");
    say(b);
    struct addrinfo *r = NULL; int g = getaddrinfo("example.com", "80", NULL, &r);
    snprintf(b, sizeof b, "getaddrinfo=%d\n", g); say(b);
    return 0;
}

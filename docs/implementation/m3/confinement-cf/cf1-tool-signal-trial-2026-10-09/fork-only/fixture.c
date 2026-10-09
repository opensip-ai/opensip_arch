#include <dlfcn.h>
#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
static int report_fd=-1;
static char who='C';
struct ready_record { char marker; pid_t pid; };
static void saw_signal(int sig) { (void)sig; if(report_fd>=0) { ssize_t rc=write(report_fd,&who,1); (void)rc; } }
static int received(int fd,char expected) { struct pollfd p={fd,POLLIN,0};char c=0;int n=poll(&p,1,500);return n>0&&read(fd,&c,1)==1&&c==expected; }
int main(int argc,char **argv) {
 if(argc>=2&&strcmp(argv[1],"observer")==0) { report_fd=STDOUT_FILENO;who='O';signal(SIGUSR1,saw_signal);puts("ready");fflush(stdout);for(;;) pause(); }
 if(argc!=6) return 2;
 const char *profile=argv[1],*scratch=argv[2],*closure=argv[3];pid_t observer=(pid_t)strtol(argv[4],NULL,10);const char *name=argv[5];int apply=0,checked=0;
 if(strcmp(profile,"none")!=0) {
  typedef int (*init_fn)(const char *,uint64_t,const char *const[],char **);
  typedef int (*check_fn)(pid_t,const char *,int,...);
  init_fn init=(init_fn)dlsym(RTLD_DEFAULT,"sandbox_init_with_parameters");check_fn check=(check_fn)dlsym(RTLD_DEFAULT,"sandbox_check");
  if(!init||!check) { puts("{\"standing\":\"incomplete\",\"reason\":\"symbol-unavailable\"}");return 3; }
  FILE *f=fopen(profile,"rb");if(!f) return 4;char text[8192];size_t n=fread(text,1,sizeof(text)-1,f);if(ferror(f)){fclose(f);return 4;}fclose(f);text[n]=0;
  const char *params[]={"SCRATCH",scratch,"CLOSURE_ROOT",closure,NULL};char *error=NULL;apply=init(text,0,params,&error);if(apply!=0) { printf("{\"standing\":\"incomplete\",\"reason\":\"profile-rejected\",\"applyRc\":%d}\n",apply);fflush(stdout);return 5; }checked=check(getpid(),NULL,0);if(checked!=1) {puts("{\"standing\":\"incomplete\",\"reason\":\"apply-check-failed\"}");return 6; }
 }
 int ack[2],pidpipe[2];if(pipe(ack)||pipe(pidpipe)) return 7;pid_t child=fork();if(child<0)return 8;
 if(child==0) {
  close(ack[0]);close(pidpipe[0]);report_fd=ack[1];who='C';signal(SIGUSR1,saw_signal);pid_t grand=fork();if(grand<0)_exit(9);
  if(grand==0){who='G';signal(SIGUSR1,saw_signal);struct ready_record ready={0};ready.marker='G';ready.pid=getpid();if(write(pidpipe[1],&ready,sizeof(ready))!=(ssize_t)sizeof(ready))_exit(10);for(;;)pause();}
  struct ready_record ready={0};ready.marker='C';ready.pid=grand;if(write(pidpipe[1],&ready,sizeof(ready))!=(ssize_t)sizeof(ready))_exit(11);for(;;)pause();
 }
 close(ack[1]);close(pidpipe[1]);
 // Both writes fit PIPE_BUF. Their order is immaterial: require matching
 // child-announced and grandchild-confirmed identities before signalling.
 struct ready_record data[2];size_t have=0;while(have<sizeof(data)){ssize_t got=read(pidpipe[0],(unsigned char *)data+have,sizeof(data)-have);if(got<=0)return 13;have+=(size_t)got;}
 pid_t grand=0;if(data[0].marker=='C'&&data[1].marker=='G'&&data[0].pid==data[1].pid)grand=data[0].pid;
 else if(data[0].marker=='G'&&data[1].marker=='C'&&data[0].pid==data[1].pid)grand=data[0].pid;
 if(grand<=0)return 14;close(pidpipe[0]);
 errno=0;int rc1=kill(child,SIGUSR1);int err1=errno;int got1=rc1==0?received(ack[0],'C'):0;
 errno=0;int rc2=kill(grand,SIGUSR1);int err2=errno;int got2=rc2==0?received(ack[0],'G'):0;
 errno=0;int rc3=kill(observer,SIGUSR1);int err3=errno;
 printf("{\"name\":\"%s\",\"standing\":\"observed\",\"applyRc\":%d,\"sandboxCheck\":%d,\"childSignal\":{\"rc\":%d,\"errno\":%d,\"received\":%d},\"grandchildSignal\":{\"rc\":%d,\"errno\":%d,\"received\":%d},\"outsideOwnedObserverSignal\":{\"rc\":%d,\"errno\":%d}}\n",name,apply,checked,rc1,err1,got1,rc2,err2,got2,rc3,err3);fflush(stdout);close(ack[0]);char done;ssize_t rc=read(STDIN_FILENO,&done,1);(void)rc;for(;;)pause();
}

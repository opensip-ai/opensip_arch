#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc,char**argv){if(argc!=2)return 2;int s=socket(AF_UNIX,SOCK_DGRAM,0);struct sockaddr_un a={0};a.sun_family=AF_UNIX;strcpy(a.sun_path,"/private/var/run/syslog");errno=0;int u=connect(s,(struct sockaddr*)&a,sizeof(a));int ue=errno;close(s);s=socket(AF_INET,SOCK_STREAM,0);struct sockaddr_in t={0};t.sin_family=AF_INET;t.sin_port=htons(atoi(argv[1]));t.sin_addr.s_addr=htonl(INADDR_LOOPBACK);errno=0;int v=connect(s,(struct sockaddr*)&t,sizeof(t));int ve=errno;close(s);printf("{\"unixResult\":%d,\"unixErrno\":%d,\"tcpResult\":%d,\"tcpErrno\":%d}\n",u,ue,v,ve);return 0;}

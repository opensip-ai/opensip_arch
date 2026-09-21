/* Read-only ABI exploration, not volume/root admission or restart qualification. */
#include <sys/attr.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
static int sample(int fd, const char *label) {
    struct stat before, after;
    struct statfs fs_before, fs_after;
    if(fstat(fd,&before)||fstatfs(fd,&fs_before)) return 4;
    struct attrlist request={0};request.bitmapcount=ATTR_BIT_MAP_COUNT;
    request.commonattr=ATTR_CMN_RETURNED_ATTRS;
    request.volattr=ATTR_VOL_INFO|ATTR_VOL_UUID;
    unsigned char buffer[40]={0};
    errno=0;
    int rc=fgetattrlist(fd,&request,buffer,sizeof(buffer),FSOPT_REPORT_FULLSIZE);
    int saved_errno=errno;
    if(fstat(fd,&after)||fstatfs(fd,&fs_after)) return 5;
    uint32_t h[6];memcpy(h,buffer,sizeof(h));
    int stable=(before.st_dev==after.st_dev && before.st_ino==after.st_ino &&
                memcmp(&fs_before.f_fsid,&fs_after.f_fsid,sizeof(fsid_t))==0);
    printf("{\"sample\":\"%s\",\"callResult\":%d,\"errno\":%d,\"frameBytes\":%u,\"returnedMasks\":[%u,%u,%u,%u,%u],\"deviceInodeFsidStable\":%s,\"device\":%" PRIu64 ",\"uuidBytesHex\":\"",label,rc,saved_errno,h[0],h[1],h[2],h[3],h[4],h[5],stable?"true":"false",(uint64_t)before.st_dev);
    for(size_t i=24;i<40;i++)printf("%02x",buffer[i]);
    printf("\"}\n");
    return 0;
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;
    int fd=open(argv[1],O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_DIRECTORY);
    if(fd<0)return 3;
    int result=sample(fd,"nested-directory");
    struct statfs fs;
    if(fstatfs(fd,&fs)){close(fd);return 6;}
    /* f_mntonname is discovery only; this probe supplies no custody authority. */
    int mountfd=open(fs.f_mntonname,O_RDONLY|O_CLOEXEC|O_NOFOLLOW|O_DIRECTORY);
    if(mountfd<0){close(fd);return 7;}
    int second=sample(mountfd,"discovered-volume-root");
    struct stat a,b;struct statfs fa,fb;
    if(fstat(fd,&a)||fstat(mountfd,&b)||fstatfs(fd,&fa)||fstatfs(mountfd,&fb)){close(mountfd);close(fd);return 8;}
    printf("{\"sameDevice\":%s,\"sameFsid\":%s,\"qualifiedAdmission\":false,\"restartTest\":false}\n",a.st_dev==b.st_dev?"true":"false",memcmp(&fa.f_fsid,&fb.f_fsid,sizeof(fsid_t))==0?"true":"false");
    close(mountfd);close(fd);return result?result:second;
}

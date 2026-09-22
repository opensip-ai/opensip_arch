/* Exploratory SDK/API observation only. Creates only its own temporary file. */
#include <sys/attr.h>
#include <sys/acl.h>
#include <sys/kauth.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void) {
 char path[]="/tmp/opensip-implementation/native-acl-bound411/fixture-XXXXXX";
 int fd=mkstemp(path);if(fd<0)return 1;
 struct attrlist attrs={0};attrs.bitmapcount=ATTR_BIT_MAP_COUNT;
 attrs.commonattr=ATTR_CMN_RETURNED_ATTRS|ATTR_CMN_EXTENDED_SECURITY;
 unsigned char bytes[16384]={0};
 int rc=fgetattrlist(fd,&attrs,bytes,sizeof(bytes),FSOPT_REPORT_FULLSIZE);
 int saved=errno;uint32_t size=0;memcpy(&size,bytes,4);
 attribute_set_t returned={0};attrreference_t ref={0};
 if(rc==0&&size>=4+sizeof(returned)+sizeof(ref)&&size<=sizeof(bytes)){
  memcpy(&returned,bytes+4,sizeof(returned));memcpy(&ref,bytes+4+sizeof(returned),sizeof(ref));
 }
 printf("rc=%d errno=%d buffer=%zu full_size=%u returned_common=0x%x reference_offset=%d reference_length=%u sdk_filesec_header=%zu sdk_ace=%zu sdk_max_entries=%d\n",rc,rc? saved:0,sizeof(bytes),size,returned.commonattr,ref.attr_dataoffset,ref.attr_length,offsetof(struct kauth_filesec,fsec_acl)+offsetof(struct kauth_acl,acl_ace),sizeof(struct kauth_ace),KAUTH_ACL_MAX_ENTRIES);
 struct attrlist volume={0};volume.bitmapcount=ATTR_BIT_MAP_COUNT;
 volume.commonattr=ATTR_CMN_RETURNED_ATTRS;volume.volattr=ATTR_VOL_INFO|ATTR_VOL_CAPABILITIES;
 unsigned char volbytes[64]={0};
 int vrc=fgetattrlist(fd,&volume,volbytes,sizeof(volbytes),FSOPT_REPORT_FULLSIZE);
 int ve=errno;uint32_t vsize=0;memcpy(&vsize,volbytes,4);
 attribute_set_t vreturned={0};vol_capabilities_attr_t caps={0};
 if(vrc==0&&vsize>=4+sizeof(vreturned)+sizeof(caps)&&vsize<=sizeof(volbytes)){
  memcpy(&vreturned,volbytes+4,sizeof(vreturned));memcpy(&caps,volbytes+4+sizeof(vreturned),sizeof(caps));
 }
 printf("volume_rc=%d errno=%d full_size=%u returned_volume=0x%x security_valid=%d security_supported=%d\n",vrc,vrc?ve:0,vsize,vreturned.volattr,!!(caps.valid[VOL_CAPABILITIES_INTERFACES]&VOL_CAP_INT_EXTENDED_SECURITY),!!(caps.capabilities[VOL_CAPABILITIES_INTERFACES]&VOL_CAP_INT_EXTENDED_SECURITY));
 /* No interpretation as empty/absent/admitted ACL. Never emit account/path data. */
 close(fd);if(unlink(path)!=0)return 2;return rc==0?0:3;
}

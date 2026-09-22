/* Read-only observation of four private, owned temporary fixtures. No authority.
 * Joint getattrlist packing follows pinned getattrlist(2) canonical order.
 * No native account UUID, inode, uid, path or raw ACL is printed or saved. */
#include <sys/attr.h>
#include <sys/acl.h>
#include <sys/kauth.h>
#include <sys/stat.h>
#include <sys/vnode.h>
#include <membership.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define CAP (128 + 44 + 128 * 24)
static int take(const unsigned char *b,size_t n,size_t *at,void *out,size_t z){
 if(*at>n||z>n-*at)return -1;memcpy(out,b+*at,z);*at+=(z+3)&~(size_t)3;return 0;
}
static int sample(int fd,int isdir,int hasacl){
 struct stat before,after;if(fstat(fd,&before))return 1;
 struct attrlist a={0};a.bitmapcount=ATTR_BIT_MAP_COUNT;
 a.commonattr=ATTR_CMN_RETURNED_ATTRS|ATTR_CMN_DEVID|ATTR_CMN_OBJTYPE|
 ATTR_CMN_MODTIME|ATTR_CMN_CHGTIME|ATTR_CMN_OWNERID|ATTR_CMN_GRPID|
 ATTR_CMN_ACCESSMASK|ATTR_CMN_FLAGS|ATTR_CMN_EXTENDED_SECURITY|ATTR_CMN_FILEID;
 if(isdir)a.dirattr=ATTR_DIR_LINKCOUNT;else a.fileattr=ATTR_FILE_LINKCOUNT|ATTR_FILE_DATALENGTH;
 unsigned char b[CAP]={0};int rc=fgetattrlist(fd,&a,b,sizeof(b),FSOPT_REPORT_FULLSIZE|FSOPT_PACK_INVAL_ATTRS);int e=rc?errno:0;
 if(fstat(fd,&after))return 2;
 uint32_t full=0;memcpy(&full,b,4);
 printf("fixture=%s_%s rc=%d errno=%d buffer=%zu full=%u ",isdir?"directory":"regular",hasacl?"one_ace":"no_installed_acl",rc,e,sizeof(b),full);
 if(rc||full>sizeof(b)||full<24){printf("unavailable=1\n");return 3;}
 attribute_set_t ret;dev_t dev;fsobj_type_t kind;struct timespec mt,ct;
 uint32_t uid,gid,mode,flags,links;uint64_t ino;off_t size=0;attrreference_t ref;size_t at=4;
 #define TAKE(v) do{if(take(b,full,&at,&v,sizeof(v))){printf("decode_failure=1\n");return 4;}}while(0)
 TAKE(ret);TAKE(dev);TAKE(kind);TAKE(mt);TAKE(ct);TAKE(uid);TAKE(gid);TAKE(mode);TAKE(flags);
 size_t ref_at=at;TAKE(ref);TAKE(ino);TAKE(links);if(!isdir)TAKE(size);
 int complete=(ret.commonattr==(a.commonattr&~ATTR_CMN_EXTENDED_SECURITY)||(ret.commonattr==a.commonattr))&&ret.volattr==0&&ret.dirattr==a.dirattr&&ret.fileattr==a.fileattr&&ret.forkattr==0;
 int mode_perm=(mode&~S_IFMT)==(before.st_mode&~S_IFMT);
 int type_ok=kind==(isdir?VDIR:VREG);
 int joint=(dev==before.st_dev&&ino==before.st_ino&&uid==before.st_uid&&gid==before.st_gid&&mode_perm&&type_ok&&flags==before.st_flags&&mt.tv_sec==before.st_mtimespec.tv_sec&&mt.tv_nsec==before.st_mtimespec.tv_nsec&&ct.tv_sec==before.st_ctimespec.tv_sec&&ct.tv_nsec==before.st_ctimespec.tv_nsec);
 int stable=before.st_dev==after.st_dev&&before.st_ino==after.st_ino&&before.st_mode==after.st_mode&&before.st_uid==after.st_uid&&before.st_gid==after.st_gid&&before.st_nlink==after.st_nlink&&before.st_size==after.st_size&&before.st_flags==after.st_flags&&before.st_mtimespec.tv_sec==after.st_mtimespec.tv_sec&&before.st_mtimespec.tv_nsec==after.st_mtimespec.tv_nsec&&before.st_ctimespec.tv_sec==after.st_ctimespec.tv_sec&&before.st_ctimespec.tv_nsec==after.st_ctimespec.tv_nsec;
 printf("returned_common=0x%x fixed_end=%zu ref_at=%zu ref_offset=%d ref_length=%u complete_metadata=%d common_matches=%d mode_contains_type=%d links_equal=%d size_available=%d size_equal=%d bracket_stable=%d ",ret.commonattr,at,ref_at,ref.attr_dataoffset,ref.attr_length,complete,joint,(mode&S_IFMT)==(before.st_mode&S_IFMT),links==before.st_nlink,!isdir,!isdir&&size==before.st_size,stable);
 if(ret.commonattr&ATTR_CMN_EXTENDED_SECURITY){
  if(ref.attr_dataoffset<0||(size_t)ref.attr_dataoffset>full-ref_at){printf("bad_ref=1\n");return 5;}
  size_t start=ref_at+(size_t)ref.attr_dataoffset;
  if(start<at||ref.attr_length>full-start||ref.attr_length<44){printf("bad_length=1\n");return 6;}
  uint32_t magic,count;memcpy(&magic,b+start,4);memcpy(&count,b+start+36,4);
  printf("acl_present=1 magic_ok=%d count=%u\n",magic==KAUTH_FILESEC_MAGIC,count);
  if(magic!=KAUTH_FILESEC_MAGIC||(count!=KAUTH_FILESEC_NOACL&&count>128)||(hasacl&&count!=1))return 7;
 }else {printf("acl_present=0 omission_not_admitted=1\n");if(hasacl)return 9;}
 struct attrlist v={0};v.bitmapcount=ATTR_BIT_MAP_COUNT;v.commonattr=ATTR_CMN_RETURNED_ATTRS;v.volattr=ATTR_VOL_INFO|ATTR_VOL_CAPABILITIES|ATTR_VOL_ATTRIBUTES;
 unsigned char vb[128]={0};int vr=fgetattrlist(fd,&v,vb,sizeof(vb),FSOPT_REPORT_FULLSIZE|FSOPT_PACK_INVAL_ATTRS);int ve=vr?errno:0;uint32_t vf=0;memcpy(&vf,vb,4);attribute_set_t vs={0};vol_capabilities_attr_t caps={0};vol_attributes_attr_t attrs={0};size_t va=4;
 int parsed=vr==0&&vf<=sizeof(vb)&&take(vb,vf,&va,&vs,sizeof(vs))==0&&take(vb,vf,&va,&caps,sizeof(caps))==0&&take(vb,vf,&va,&attrs,sizeof(attrs))==0;
 printf("volume_rc=%d errno=%d full=%u decoded=%d returned_volume=0x%x acl_cap_valid=%d acl_cap_supported=%d acl_attr_valid=%d acl_attr_native=%d\n",vr,ve,vf,parsed,vs.volattr,!!(caps.valid[VOL_CAPABILITIES_INTERFACES]&VOL_CAP_INT_EXTENDED_SECURITY),!!(caps.capabilities[VOL_CAPABILITIES_INTERFACES]&VOL_CAP_INT_EXTENDED_SECURITY),!!(attrs.validattr.commonattr&ATTR_CMN_EXTENDED_SECURITY),!!(attrs.nativeattr.commonattr&ATTR_CMN_EXTENDED_SECURITY));
 unsigned char shortb[32]={0};int sr=fgetattrlist(fd,&a,shortb,sizeof(shortb),FSOPT_REPORT_FULLSIZE|FSOPT_PACK_INVAL_ATTRS);uint32_t sf=0;memcpy(&sf,shortb,4);
 printf("short_rc=%d supplied=%zu reported=%u refused_truncated=%d\n",sr,sizeof(shortb),sf,sr==0&&sf>sizeof(shortb));
 return complete&&joint&&stable&&sr==0&&sf>sizeof(shortb)?0:8;
}
static int set_acl(int fd){
 uuid_t uuid;acl_t acl=acl_init(1);acl_entry_t ent;
 if(!acl)return -1;
 int ok=mbr_uid_to_uuid(getuid(),uuid)==0&&acl_create_entry(&acl,&ent)==0&&acl_set_tag_type(ent,ACL_EXTENDED_ALLOW)==0&&acl_set_qualifier(ent,uuid)==0&&acl_set_permset_mask_np(ent,ACL_READ_DATA)==0&&acl_set_fd_np(fd,acl,ACL_TYPE_EXTENDED)==0;
 acl_free(acl);return ok?0:-1;
}
int main(void){
 char dir[]="/tmp/opensip-implementation/joint-acl445/fixture-XXXXXX";if(!mkdtemp(dir))return 10;
 int d=open(dir,O_RDONLY|O_DIRECTORY|O_NOFOLLOW);if(d<0){rmdir(dir);return 11;}
 int f=openat(d,"record",O_CREAT|O_EXCL|O_RDWR|O_NOFOLLOW,0600);if(f<0){close(d);rmdir(dir);return 12;}
 int r=sample(f,0,0);if(!r)r=sample(d,1,0);if(!r&&set_acl(f))r=13;if(!r&&set_acl(d))r=14;
 if(!r)r=sample(f,0,1);if(!r)r=sample(d,1,1);
 close(f);int u=unlinkat(d,"record",0);close(d);int v=rmdir(dir);return r?r:(u||v?15:0);
}

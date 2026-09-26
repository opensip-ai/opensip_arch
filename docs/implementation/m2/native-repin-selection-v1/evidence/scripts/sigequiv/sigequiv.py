"""For each native pin that no longer matches, show the installed file equals the
tahoe bottle file after Homebrew's load-command relocation, once both have their
code signatures removed. Output is JSON evidence for the re-pin unit."""
import json,hashlib,os,subprocess,shutil,sys,tempfile
R='/Users/sb/code/opensip-ai/opensip/tools/contracts/'
B=sys.argv[1]
rows={}
d=json.load(open(R+'native-python-profile.json'))
for x in [d['executable'],d['library']]+d['files']+d['nativeLibraries']: rows[x['path']]=(x['sha256'],x['bytes'])
p=json.load(open(R+'python-profile.json'))
for x in [p['executable'],p['library']]+p['files']: rows[x['path']]=(x['sha256'],x['bytes'])
b=json.load(open(R+'build-receipt.json'))
for x in b['tools'].values(): rows[x['path']]=(x['sha256'],x['bytes'])
def sha(f): return hashlib.sha256(open(f,'rb').read()).hexdigest()
def relocate(f):
    out=subprocess.run(['otool','-l',f],capture_output=True,text=True).stdout.split('\n')
    args=[]
    for i,l in enumerate(out):
        l=l.strip()
        if l.startswith('name ') or l.startswith('path '):
            v=l.split(' ',1)[1].rsplit(' (offset',1)[0]
            if '@@HOMEBREW' in v:
                n=v.replace('@@HOMEBREW_PREFIX@@','/opt/homebrew').replace('@@HOMEBREW_CELLAR@@','/opt/homebrew/Cellar')
                cmd=[x.strip() for x in out[max(0,i-2):i]]
                if any('LC_ID_DYLIB' in c for c in cmd): args+=['-id',n]
                elif any('LC_RPATH' in c for c in cmd): args+=['-rpath',v,n]
                else: args+=['-change',v,n]
    if args: subprocess.run(['install_name_tool',*args,f],capture_output=True)
res=[];tmp=tempfile.mkdtemp()
for path,(h,n) in sorted(rows.items()):
    if not os.path.exists(path) or sha(path)==h: continue
    rel=path.split('/opt/homebrew/Cellar/',1)[1]
    src=os.path.join(B,rel)
    a=os.path.join(tmp,'a');c=os.path.join(tmp,'c')
    shutil.copy(src,a);shutil.copy(path,c);os.chmod(a,0o644);os.chmod(c,0o644)
    relocate(a)
    for f in (a,c): subprocess.run(['codesign','--remove-signature',f],capture_output=True)
    res.append(dict(path=path,pinnedSha256=h,pinnedBytes=n,bottleBytes=os.path.getsize(src),
        installedSha256=sha(path),installedBytes=os.path.getsize(path),
        unsignedEqual=open(a,'rb').read()==open(c,'rb').read(),unsignedSha256=sha(c)))
print(json.dumps(res,indent=1))
print('total',len(res),'unsignedEqual',sum(r['unsignedEqual'] for r in res),'pinnedBytes==bottleBytes',sum(r['pinnedBytes']==r['bottleBytes'] for r in res),file=sys.stderr)

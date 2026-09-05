"""Native design probe; not product/platform qualification."""
import argparse,hashlib,json,os,platform,subprocess
from pathlib import Path

def main(report):
    if platform.system()!='Darwin':raise SystemExit('MACOS-ONLY-PROBE')
    target='/usr/bin/true';fd=os.open(target,os.O_RDONLY)
    try:
        identity=os.fstat(fd)
        rows=[]
        for name,command,passed in [('canonical-path',[target],()),('dev-fd-exec',['/dev/fd/'+str(fd)],(fd,))]:
            try:
                p=subprocess.run(command,pass_fds=passed,env={},capture_output=True)
                rows.append({'case':name,'exit':p.returncode,'errno':None,'stderr':p.stderr.decode('utf-8','replace')})
            except OSError as e:rows.append({'case':name,'exit':None,'errno':e.errno,'error':e.strerror})
        build=subprocess.run(['/usr/bin/sw_vers','-buildVersion'],capture_output=True,text=True,check=True).stdout.strip()
        result={'kind':'NATIVE-DESIGN-EXPERIMENT','productQualification':False,'osVersion':platform.mac_ver()[0],'osBuild':build,'architecture':platform.machine(),'target':target,'targetSha256':hashlib.sha256(Path(target).read_bytes()).hexdigest(),'targetMode':oct(identity.st_mode),'checkerSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':rows,'interpretation':'On this host canonical path executes; /dev/fd is not an executable-file-descriptor mechanism. Exact-generation custody requires a separately specified path/lease/identity protocol. This probe does not qualify that replacement.'}
        Path(report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(rows))
    finally:os.close(fd)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',required=True);main(p.parse_args().report)

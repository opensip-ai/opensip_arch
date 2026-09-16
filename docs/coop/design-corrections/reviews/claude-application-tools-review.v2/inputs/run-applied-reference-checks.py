"""Execute all current reference groups only after actual documentation activation."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=a.root.resolve();activation=json.loads((root/'docs/coop/design-corrections/application-activation.v1.json').read_text())
assert activation['implementationAuthorized'] is False and activation['qualificationClaimed'] is False
ref=activation['applicationManifest'];assert hashlib.sha256((root/ref['path']).read_bytes()).hexdigest()==ref['sha256']
command=[sys.executable,'-I','-B',str(Path(__file__).with_name('run-application-reference-suites.py')),'--root',str(root),'--out',str(a.out.resolve()),'--application-manifest-sha256',ref['sha256']]
raise SystemExit(subprocess.run(command).returncode)

"""Child native renderer using only its explicit Python package snapshot.

Run with -I -B -S. This dependency binding is not yet OS confinement.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize:
    raise ValueError('isolated Python without site loading or optimization required')
code=Path(__file__).resolve().parent
packages=code/'python-packages'
manifest=json.loads((code/'python-packages.json').read_bytes())
expected=manifest['files'];actual=[]
for p in sorted(packages.rglob('*'),key=lambda p:p.relative_to(packages).as_posix()):
    if p.is_symlink():raise ValueError('linked Python dependency')
    if p.is_dir():continue
    if not p.is_file():raise ValueError('nonregular Python dependency')
    raw=p.read_bytes();actual.append({'path':p.relative_to(packages).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
if actual!=expected:raise ValueError('Python package snapshot differs')
# -S suppresses .pth/sitecustomize; this is the sole additional module root.
sys.path.insert(0,str(packages))
def module(name):
    path=code/(name+'.py');spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
if len(sys.argv)!=5:raise ValueError('owner, meta, options and fresh output required')
owner,meta,options=[json.loads(Path(p).read_bytes()) for p in sys.argv[1:4]]
guard=module('native_guard');renderer=module('native_renderer')
selected,receipt=guard.admit(owner,meta,options);native=renderer.Renderer(selected)
rust,typescript=native.run()
out=Path(sys.argv[4]);out.mkdir(exist_ok=False)
(out/'native.rs').write_text(renderer.RUST_HELPERS+rust)
(out/'wire.ts').write_text(typescript)
(out/'render-result.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'passed':True,'nativeTypes':receipt['nativeTypes'],'pythonPackageFiles':len(actual),'siteLoading':False}))

import hashlib, json, sys
from pathlib import Path
ROOT = Path('/tmp/opensip-implementation')
SUBJECTS = {
 'm1-presentation-catalog-subject-01': ('22479d58a64e3af8e0d97f25f1dd474c3b582e02f7c130b21ac03e2f9f2815a1', 9),
 'm1-config-disclosure-subject-01': ('446c34f75e36f0ceff7d76f65ca3b932f5905eb83594319db96982e8079514e8', 10),
 'm1-workflow-timing-subject-01': ('be0d10623dc51b2835efec22cd11d73f50932be088313427046f3e985f650376', 8),
 'm1-history-selection-subject-01': ('c4db0337efb63560eb208dcf43cf6fa21b340efe7b33437129cca7ad55e553d9', 8),
}
out = {}
ok = True
for name, (want, count) in SUBJECTS.items():
    mraw = (ROOT / (name + '.json')).read_bytes()
    manifest = json.loads(mraw)
    d = ROOT / name
    actual = sorted(p.relative_to(d).as_posix() for p in d.rglob('*'))
    listed = sorted(f['path'] for f in manifest['files'])
    files_ok = all(len((d/f['path']).read_bytes()) == f['bytes'] and hashlib.sha256((d/f['path']).read_bytes()).hexdigest() == f['sha256'] for f in manifest['files'])
    pins = json.loads((d/'input-pins.json').read_bytes())['files']
    pin_ok = []
    for p in pins:
        raw = Path(p['path']).read_bytes()
        pin_ok.append(len(raw) == p['bytes'] and hashlib.sha256(raw).hexdigest() == p['sha256'])
    extra = {}
    if name == 'm1-workflow-timing-subject-01':
        s = json.loads((d/'successor.json').read_bytes())['parent']
        raw = Path(s['path']).read_bytes()
        extra['successorParentPin'] = len(raw) == s['bytes'] and hashlib.sha256(raw).hexdigest() == s['sha256']
    r = {'manifestSha256': hashlib.sha256(mraw).hexdigest(), 'manifestShaMatches': hashlib.sha256(mraw).hexdigest() == want,
         'exactFileSet': actual == listed, 'fileCount': len(actual), 'countMatches': len(actual) == count,
         'fileHashesMatch': files_ok, 'externalPins': len(pins), 'externalPinsMatch': all(pin_ok), **extra}
    ok = ok and r['manifestShaMatches'] and r['exactFileSet'] and r['countMatches'] and files_ok and all(pin_ok) and extra.get('successorParentPin', True)
    out[name] = r
print(json.dumps({'allOk': ok, 'subjects': out}, indent=2))
sys.exit(0 if ok else 1)

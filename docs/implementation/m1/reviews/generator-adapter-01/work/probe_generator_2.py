"""Second-round reviewer probes (clones under work/m3 only)."""
import json, subprocess, sys
from pathlib import Path
sys.argv = ['x']
import importlib.util
spec = importlib.util.spec_from_file_location('p1', '/tmp/opensip-implementation/m1-generator-adapter-review-01/work/probe_generator.py')
src = Path(spec.origin).read_text().replace("R / 'work/m2' / name", "R / 'work/m3' / name").replace('\nmain()\n', '\n')
p1 = type(sys)('p1'); exec(compile(src, spec.origin, 'exec'), p1.__dict__)
R, OUTS = p1.R, p1.OUTS

# 1. -O removes the only guard in prepare.rust for unselected pattern maps
code = ("import sys;sys.path.insert(0,'%s/work/base/tools/contracts');import prepare as P\n"
        "print(P.rust({'type':'object','properties':{'a':{}},'patternProperties':{'^x':{'type':'string'},'^.+$':{}},'additionalProperties':True}))") % R
for flags in (['-I', '-B'], ['-I', '-B', '-O']):
    p = subprocess.run([sys.executable, *flags, '-c', code], capture_output=True, text=True)
    p1.results.append({'probe': 'O1 prepare.rust unselected pattern map ' + ' '.join(flags), 'exit': p.returncode,
                       'tail': (p.stdout.strip() or p.stderr.strip().splitlines()[-1])[:300]})
    print(json.dumps(p1.results[-1]))

# 2. drop one native library pin only
r = p1.clone('n1'); c = p1.jload(r / 'tools/contracts/generator-closure.json')
c['nativeLibraries'] = [x for x in c['nativeLibraries'] if 'z3' not in x['path']]
(r / 'tools/contracts/generator-closure.json').write_text(json.dumps(c, indent=2) + '\n'); p1.rebind_closure(r)
p1.run('N1 closure drops libz3 pin only (rebound), --write', r, write=True, expect='refuse')

# 3. partial write after failure between destinations
r = p1.clone('w1')
for rel in (OUTS[0], OUTS[6]):
    f = r / rel; f.write_bytes(f.read_bytes() + b'\n')
gen_dir = r / 'crates/contracts/src/generated'; gen_dir.chmod(0o555)
try:
    p1.run('W1 --write with read-only crates generated dir after report.ts', r, write=True, expect='refuse')
finally:
    gen_dir.chmod(0o755)
p1.run('W1b drift check after interrupted write', r, expect='refuse')
leftovers = sorted(str(x.relative_to(r)) for x in r.rglob('.contracts-*'))
p1.results.append({'probe': 'W1c temp leftovers', 'leftovers': leftovers}); print(json.dumps(p1.results[-1]))

# 4. entrypoint cannot authenticate itself
r = p1.clone('s1'); f = r / 'tools/generate_contracts.py'; t = f.read_text()
t = t.replace("raw = checked(root, pin['path'], pin['sha256'])", "raw = local(root, pin['path']).read_bytes()")
t = t.replace("if type(pin['bytes']) is not int or pin['bytes'] != len(raw):", "if False:")
assert t != f.read_text(); f.write_text(t)
g = r / 'tools/contracts/render-types.cjs'; g.write_text(g.read_text() + '\n// unpinned reviewer edit\n')
p1.run('S1 edited entrypoint skips its own closure pins; tampered render-types accepted', r, expect=None)

(R / 'logs/generator-probes-2.json').write_text(json.dumps(p1.results, indent=2) + '\n')

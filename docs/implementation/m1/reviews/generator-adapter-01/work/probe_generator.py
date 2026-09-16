"""Reviewer mutation probes for the contracts-v1 adapter. Operates only on clones
under this review directory; originals are read-only inputs."""
import hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path

R = Path('/tmp/opensip-implementation/m1-generator-adapter-review-01')
BASE = R / 'work/base'
GEN = '/tmp/opensip-implementation/m1-generator-integration-candidate-01/tools/contracts/target/debug/opensip-contract-generator'
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
RUSTFMT = '/opt/homebrew/bin/rustfmt'
PY = '/opt/homebrew/opt/python@3.14/bin/python3.14'
OUTS = ['apps/report/src/generated/report.ts', 'crates/contracts/src/generated/evidence.rs',
        'crates/contracts/src/generated/identity.rs', 'crates/contracts/src/generated/invocation.rs',
        'crates/contracts/src/generated/mod.rs', 'crates/contracts/src/generated/output.rs',
        'crates/contracts/src/generated/protocol.rs', 'providers/typescript/src/generated/protocol.ts']
results = []


def sha(b): return hashlib.sha256(b).hexdigest()
def jload(p): return json.loads(Path(p).read_text())
def jsave(p, v): Path(p).write_text(json.dumps(v, indent=2) + '\n')


def clone(name):
    dst = R / 'work/m2' / name
    if dst.exists():
        subprocess.run(['chmod', '-R', 'u+w', str(dst)]); shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['cp', '-cR', str(BASE), str(dst)], check=True)
    return dst


def rebind_source(root, rel):
    reg = jload(root / 'schemas/registry.json'); new = sha((root / rel).read_bytes())
    for s in reg['sources']:
        if s['sourcePath'] == rel:
            old = s['sourceSha256']; s['sourceSha256'] = new
    rc = reg['recipes'][0]; rc['sourceSha256s'] = sorted(new if x == old else x for x in rc['sourceSha256s'])
    jsave(root / 'schemas/registry.json', reg)


def rebind_options(root):
    reg = jload(root / 'schemas/registry.json')
    reg['recipes'][0]['optionsSha256'] = sha((root / 'tools/contracts/options.json').read_bytes())
    jsave(root / 'schemas/registry.json', reg)


def rebind_closure(root):
    c = jload(root / 'tools/contracts/generator-closure.json')
    for f in c['files']:
        b = (root / f['path']).read_bytes(); f['sha256'] = sha(b); f['bytes'] = len(b)
    (root / 'tools/contracts/generator-closure.json').write_text(json.dumps(c, indent=2) + '\n')
    reg = jload(root / 'schemas/registry.json')
    reg['recipes'][0]['generatorClosureSha256'] = sha((root / 'tools/contracts/generator-closure.json').read_bytes())
    jsave(root / 'schemas/registry.json', reg)


def snapshot(root):
    rows = {}
    for p in sorted(root.rglob('*')):
        if 'node_modules' in p.parts: continue
        if p.is_symlink(): rows[str(p.relative_to(root))] = 'link:' + os.readlink(p)
        elif p.is_file(): rows[str(p.relative_to(root))] = sha(p.read_bytes())
    return rows


def run(name, root, *, write=False, gen=GEN, node=NODE, rustfmt=RUSTFMT, py=PY, flags=('-I', '-B'), env=None, expect=None, note=''):
    before = snapshot(root)
    argv = [py, *flags, str(root / 'tools/generate_contracts.py'), '--root', str(root), '--generator', gen,
            '--node', node, '--rustfmt', rustfmt] + (['--write'] if write else [])
    e = dict(os.environ, TMPDIR=str(R / 'tmp')); e.update(env or {})
    t = time.time(); p = subprocess.run(argv, capture_output=True, text=True, env=e)
    after = snapshot(root)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    err = [l for l in p.stderr.strip().splitlines() if l][-1:] if p.stderr.strip() else []
    row = {'probe': name, 'write': write, 'exit': p.returncode, 'stderrTail': err,
           'stdoutTail': p.stdout.strip().splitlines()[-1:] if p.stdout.strip() else [],
           'stdoutHead': p.stdout.strip().splitlines()[:1], 'filesChangedInRoot': changed,
           'expect': expect, 'note': note, 'seconds': round(time.time() - t, 1)}
    row['matchesExpectation'] = None if expect is None else ((p.returncode == 0) == (expect == 'accept'))
    results.append(row); print(json.dumps(row)); sys.stdout.flush()
    return row


def main():
    # --- source substitution
    r = clone('m01'); p = r / 'schemas/sources/dispatch.v1.schema.json'; p.write_bytes(p.read_bytes() + b' ')
    run('M01 source byte change without registry rebind', r, expect='refuse')

    r = clone('m02'); rel = 'schemas/sources/dispatch.v1.schema.json'; d = jload(r / rel)
    d['description'] = 'reviewer substitution'; (r / rel).write_text(json.dumps(d, indent=2)); rebind_source(r, rel)
    run('M02 consistently rebound source substitution, drift check', r, expect='refuse')
    run('M02b same, --write', r, write=True, expect='accept', note='reviewed-rebind path; expected to regenerate')
    run('M02c recheck after write', r, expect='accept')

    # remote/unsupported refs inside schema keywords prepare.py does not traverse
    o = jload(BASE / 'tools/contracts/options.json')
    disp = next(e for e in o['entryPoints'] if e['ref'].split('#')[0] == jload(BASE / rel)['$id'])
    ptr = disp['ref'].split('#')[1].split('/')[1:]
    for label, kw, val in [('M03 remote $ref under prefixItems', 'prefixItems', [{'$ref': 'https://unregistered.invalid/x.json'}]),
                           ('M03b remote $ref under dependentSchemas', 'dependentSchemas', {'k': {'$ref': 'https://unregistered.invalid/y.json'}}),
                           ('M03c $dynamicRef', '$dynamicRef', 'https://unregistered.invalid/z.json#meta'),
                           ('M03d remote $ref under unevaluatedProperties', 'unevaluatedProperties', {'$ref': 'https://unregistered.invalid/u.json'})]:
        r = clone('m03-' + kw.strip('$')); d = jload(r / rel); node = d
        for t in ptr: node = node[t]
        node[kw] = val; (r / rel).write_text(json.dumps(d, indent=2)); rebind_source(r, rel)
        run(label + ' (--write)', r, write=True, expect='refuse', note='architecture: all transitive refs resolve within registered inputs; entry ' + disp['ref'])

    # --- options / owner / ref substitution
    r = clone('m04'); op = r / 'tools/contracts/options.json'; o2 = jload(op); o2['standing'] += ' x'; jsave(op, o2)
    run('M04 options change without rebind', r, expect='refuse')

    r = clone('m05'); op = r / 'tools/contracts/options.json'; o2 = jload(op)
    ns = o2['owners'][0]; old = ns['module']; new = 'protocol' if old != 'protocol' else 'output'; ns['module'] = new
    for e in o2['entryPoints']:
        if e['ref'].split('#')[0] == ns['schemaId']: e['module'] = new
    jsave(op, o2); rebind_options(r)
    run('M05 owner module substitution rebound (%s %s->%s)' % (ns['namespace'], old, new), r, expect='refuse', note='drift expected; source-map.json still says old module')

    r = clone('m06'); op = r / 'tools/contracts/options.json'; o2 = jload(op)
    import collections
    doc = collections.Counter(e['ref'].split('#')[0] for e in o2['entryPoints']).most_common(1)[0][0]
    same = [e for e in o2['entryPoints'] if e['ref'].split('#')[0] == doc]
    a, b = same[0], same[1]; a['typeName'], b['typeName'] = b['typeName'], a['typeName']
    jsave(op, o2); rebind_options(r)
    run('M06 swap two entrypoint type names (ref substitution) rebound', r, expect='refuse')

    r = clone('m07'); op = r / 'tools/contracts/options.json'; o2 = jload(op)
    den = o2['deniedRefs'][0]; o2['deniedRefs'].remove(den)
    o2['entryPoints'].append({'ref': den, 'typeName': 'Native2' + 'HelloV3Reinstated', 'module': next(x['module'] for x in o2['owners'] if x['schemaId'] == den.split('#')[0])})
    o2['entryPoints'].sort(key=lambda e: e['ref']); jsave(op, o2); rebind_options(r)
    ns_native = next(x['namespace'] for x in o2['owners'] if x['schemaId'] == den.split('#')[0])
    run('M07 reinstate superseded HelloV3 by removing deniedRefs row (namespace %s)' % ns_native, r, write=True,
        expect='refuse', note='only superseded list is self-declared in options')

    r = clone('m08'); reg = jload(r / 'schemas/registry.json'); op = r / 'tools/contracts/options.json'; o2 = jload(op)
    sid = reg['sources'][0]['schemaId']
    for row in [reg['sources'][0], next(x for x in o2['sourceMappings'] if x['schemaId'] == sid)]:
        row['semanticValidatorOwner'] = '../../outside/owner'; row['declaredMajor'] = 7
    jsave(r / 'schemas/registry.json', reg); jsave(op, o2); rebind_options(r)
    run('M08 consistent major/semantic-owner substitution in registry+options (--write)', r, write=True, expect='refuse',
        note='owner path syntax, declared major vs source-map/document not checked')

    r = clone('m08b'); op = r / 'tools/contracts/options.json'; o2 = jload(op); o2['sourceMappings'][0]['semanticValidatorOwner'] = 'x'; jsave(op, o2); rebind_options(r)
    run('M08b owner changed only in options', r, expect='refuse')

    r = clone('m09'); reg = jload(r / 'schemas/registry.json')
    reg['recipes'][0]['outputs'][4]['roles'] = ['carrier', 'shape-validator']
    reg['recipes'][0]['outputs'][0]['roles'] = ['module-index']
    jsave(r / 'schemas/registry.json', reg)
    run('M09 swap roles: mod.rs carrier+shape-validator, report.ts module-index (--write)', r, write=True, expect='refuse')

    r = clone('m10'); reg = jload(r / 'schemas/registry.json')
    row = reg['sources'].pop(next(i for i, s in enumerate(reg['sources']) if s['sourcePath'] == rel))
    (r / 'tools/zz-moved').mkdir(); shutil.move(r / rel, r / 'tools/zz-moved/dispatch.json'); row['sourcePath'] = 'tools/zz-moved/dispatch.json'
    reg['sources'].append(row); jsave(r / 'schemas/registry.json', reg)
    run('M10 source relocated outside schemas/sources (--write)', r, write=True, expect='refuse')

    r = clone('m11'); reg = jload(r / 'schemas/registry.json'); reg['recipes'][0]['sourceSha256s'].pop(); jsave(r / 'schemas/registry.json', reg)
    run('M11 recipe omits one registered source', r, expect='refuse')

    r = clone('m12'); (r / 'schemas/registry.json').write_text((r / 'schemas/registry.json').read_text().replace('"schemaVersion": 1,', '"schemaVersion": 1, "schemaVersion": 1,', 1))
    run('M12 duplicate registry key', r, expect='refuse')

    # --- undeclared output / output set
    for label, rp in [('M13 extra .rs in generated dir', 'crates/contracts/src/generated/extra.rs'),
                      ('M13b hidden file in report generated dir', 'apps/report/src/generated/.contracts-leftover'),
                      ('M13c nested dir in provider generated dir', 'providers/typescript/src/generated/sub/x.ts')]:
        r = clone('m13-' + rp.split('/')[-1]); (r / rp).parent.mkdir(parents=True, exist_ok=True); (r / rp).write_text('x')
        run(label + ' (--write)', r, write=True, expect='refuse')

    r = clone('m14'); reg = jload(r / 'schemas/registry.json'); reg['recipes'][0]['outputs'].pop(4); jsave(r / 'schemas/registry.json', reg)
    run('M14 registry drops mod.rs output row', r, expect='refuse')

    r = clone('m15'); reg = jload(r / 'schemas/registry.json')
    reg['recipes'][0]['outputs'].append({'path': 'providers/typescript/src/generated/zz.ts', 'language': 'typescript', 'roles': ['carrier']})
    jsave(r / 'schemas/registry.json', reg)
    run('M15 registry declares ninth output the generator does not emit', r, expect='refuse')

    r = clone('m16'); f = r / OUTS[6]; tgt = R / 'work/m/m16-outside.rs'; shutil.copyfile(f, tgt); f.unlink(); f.symlink_to(tgt)
    run('M16 output file replaced by symlink to identical bytes', r, write=True, expect='refuse')

    r = clone('m17'); g = r / 'providers/typescript/src/generated'; out = R / 'work/m/m17-outside'; shutil.move(g, out); g.symlink_to(out)
    run('M17 generated directory replaced by symlink', r, write=True, expect='refuse')

    # --- drift and write
    r = clone('m18'); f = r / OUTS[6]; f.write_bytes(f.read_bytes().replace(b'pub', b'pub ', 1))
    run('M18 drift in protocol.rs', r, expect='refuse')
    run('M18b --write restores only drifted file', r, write=True, expect='accept')
    run('M18c recheck', r, expect='accept')

    r = clone('m19'); (r / OUTS[7]).unlink(); run('M19 deleted provider output, --write', r, write=True, expect='accept'); run('M19b recheck', r, expect='accept')

    # --- tool tamper
    tam = R / 'work/m/tampered-generator'; shutil.copyfile(GEN, tam); tam.write_bytes(tam.read_bytes() + b'\0'); tam.chmod(0o755)
    run('M20 generator executable tampered', BASE, gen=str(tam), expect='refuse')
    run('M20b relative node path', BASE, node='node', expect='refuse')
    run('M20c different python interpreter', BASE, py='/usr/bin/python3', expect='refuse')
    rf = R / 'work/m/rustfmt-copy/bin/rustfmt'; rf.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(RUSTFMT, rf); rf.chmod(0o755)
    r = clone('m21'); f = r / OUTS[6]; f.write_bytes(f.read_bytes() + b'\n')
    run('M21 rustfmt identical bytes at relocated path (loader join) with pending --write', r, write=True, rustfmt=str(rf), expect='refuse',
        note='pin passes; dylib resolution differs; must fail before writing')

    r = clone('m22'); f = r / 'tools/contracts/render-types.cjs'; f.write_text(f.read_text() + '\n// x\n')
    run('M22 pinned render-types.cjs tampered without rebind', r, expect='refuse')

    r = clone('m23'); f = r / 'tools/generate_contracts.py'
    f.write_text(f.read_text().replace("raise GenerationError('input digest mismatch: ' + path)", "pass"))
    g2 = r / 'tools/contracts/render-types.cjs'; g2.write_text(g2.read_text() + '\n// x\n')
    run('M23 entrypoint self-verification: edited generate_contracts.py disables digest check', r, expect=None,
        note='demonstrates the entrypoint cannot authenticate itself')

    r = clone('m24'); f = r / 'tools/contracts/render-types.cjs'
    f.write_text(f.read_text().replace("function renderTypes(schema, selectedNames) {", "function renderTypes(schema, selectedNames) { if (selectedNames.length > 100) throw new Error('reviewer failure');"))
    rebind_closure(r); o18 = r / OUTS[6]; o18.write_bytes(o18.read_bytes() + b'\n')
    run('M24 consistently rebound TS stage fails after Rust stage with pending --write', r, write=True, expect='refuse')

    # --- TS package tamper
    ts = lambda root: root / 'tools/contracts/node_modules/.pnpm/typescript@6.0.3/node_modules/typescript'
    r = clone('m25'); f = ts(r) / 'lib/typescript.js'; f.write_bytes(f.read_bytes() + b'\n')
    run('M25 typescript.js tampered', r, expect='refuse')
    r = clone('m25b'); (ts(r) / 'lib/extra.js').write_text('x'); run('M25b extra file in TS package', r, expect='refuse')
    r = clone('m25c'); link = r / 'tools/contracts/node_modules/typescript'; link.unlink()
    link.symlink_to(R / 'work/tsprov/node_modules/.pnpm/typescript@6.0.3/node_modules/typescript')
    run('M25c TS symlink redirected outside tooling workspace to identical bytes', r, expect='refuse')
    r = clone('m25d'); (ts(r) / 'lib/alias.js').symlink_to(ts(r) / 'lib/typescript.js'); run('M25d nested symlink in TS package', r, expect='refuse')
    r = clone('m25e'); nm = r / 'tools/contracts/node_modules'; shutil.move(nm, R / 'work/m/m25e-nm'); nm.symlink_to(R / 'work/m/m25e-nm')
    run('M25e node_modules directory symlinked outside', r, expect='refuse')

    # --- closure self-declaration
    r = clone('m26'); c = jload(r / 'tools/contracts/generator-closure.json'); c['nativeLibraries'] = []
    (r / 'tools/contracts/generator-closure.json').write_text(json.dumps(c, indent=2) + '\n'); rebind_closure(r)
    run('M26 closure drops all native library pins (rebound), --write', r, write=True, expect='refuse',
        note='completeness of library list vs actual loader closure is not derived')
    r = clone('m27'); c = jload(r / 'tools/contracts/generator-closure.json'); c['hostProfile']['scope'] = 'hermetic'
    (r / 'tools/contracts/generator-closure.json').write_text(json.dumps(c, indent=2) + '\n'); rebind_closure(r)
    run('M27 closure claims different host scope', r, expect='refuse')

    # --- ambient interpreter effects
    inj = R / 'work/m/inject'; inj.mkdir(parents=True, exist_ok=True)
    (inj / 'sitecustomize.py').write_text("import sys\nsys.stderr.write('REVIEWER-SITECUSTOMIZE-RAN\\n')\n")
    run('M28 invoked without -I, PYTHONPATH sitecustomize', BASE, flags=('-B',), env={'PYTHONPATH': str(inj)}, expect='refuse',
        note='accepted means ambient code ran inside the verifier')
    run('M28b -O strips assert-based projection guards', BASE, flags=('-I', '-B', '-O'), expect='refuse')

    (R / 'logs/generator-probes.json').write_text(json.dumps(results, indent=2) + '\n')


main()

"""Reviewer-only case copies. Rebinding self hashes is exactly what an attacker with
write access to a checkout could do; these are integrity checks, not trust anchors."""
import hashlib, json, shutil, subprocess
from pathlib import Path

WORK = Path(__file__).resolve().parent
SUBJECT = Path('/tmp/opensip-implementation/m1-generator-adapter-subject-04')
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
GEN = '/tmp/opensip-implementation/m1-generator-build-04/opensip-contract-generator'
BASE = 'base'
PY = '/opt/homebrew/bin/python3'


def pin(raw):
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def case(name, files=None, generator=GEN, options=None, sources=None, closure_mutate=None):
    c = WORK / 'cases' / name
    shutil.rmtree(c, ignore_errors=True)
    shutil.copytree(WORK / BASE, c, symlinks=True)
    if not (files or sources or options is not None or closure_mutate or generator != GEN):
        return c
    for rel, raw in (files or {}).items():
        (c / rel).write_bytes(raw)
    reg_p = c / 'schemas/registry.json'; reg = json.loads(reg_p.read_text())
    if sources:
        smap_p = c / 'schemas/source-map.json'; smap = json.loads(smap_p.read_text())
        for rel, raw in sources.items():
            row = next(r for r in reg['sources'] if r['sourcePath'] == rel); old = row['sourceSha256']
            (c / rel).write_bytes(raw); new = pin(raw); row['sourceSha256'] = new['sha256']
            rec = reg['recipes'][0]
            rec['sourceSha256s'] = sorted(new['sha256'] if x == old else x for x in rec['sourceSha256s'])
            next(r for r in smap['sources'] if r['implementationPath'] == rel)['architectureSource'].update(new)
        smap_p.write_text(json.dumps(smap, indent=2) + '\n')
    if options is not None:
        op = c / 'tools/contracts/options.json'; op.write_text(json.dumps(options, indent=2) + '\n')
        reg['recipes'][0]['optionsSha256'] = pin(op.read_bytes())['sha256']
    cl_p = c / 'tools/contracts/generator-closure.json'; cl = json.loads(cl_p.read_text())
    gpin = pin(Path(generator).read_bytes()); cl['toolchain']['generator'] = gpin
    rp = c / 'tools/contracts/build-receipt.json'; rc = json.loads(rp.read_text())
    if rc['executable'] != gpin:
        rc['executable'] = gpin; rp.write_text(json.dumps(rc, indent=2) + '\n')
    for row in cl['files']:
        row.update(pin((c / row['path']).read_bytes()))
    if closure_mutate:
        closure_mutate(cl)
    cl_p.write_text(json.dumps(cl, indent=1) + '\n')
    reg['recipes'][0]['generatorClosureSha256'] = pin(cl_p.read_bytes())['sha256']
    reg_p.write_text(json.dumps(reg, indent=2) + '\n')
    return c


def outputs(c):
    reg = json.loads((c / 'schemas/registry.json').read_text())
    return [o['path'] for o in reg['recipes'][0]['outputs']]


def snapshot(c):
    return {p: pin((c / p).read_bytes()) if (c / p).exists() else None for p in outputs(c)}


def generate(c, generator=GEN, write=False, timeout=900):
    argv = [PY, '-I', '-B', str(c / 'tools/generate_contracts.py'), '--root', str(c),
            '--generator', str(generator), '--node', NODE] + (['--write'] if write else [])
    r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return {'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr[-4000:]}

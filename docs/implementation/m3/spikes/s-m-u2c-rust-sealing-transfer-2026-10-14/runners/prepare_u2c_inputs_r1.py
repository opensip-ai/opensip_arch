from pathlib import Path
import json, hashlib, os, shutil, subprocess
# U-2c inputs (S-M report plan r3, D-2): for every Rust entry, its accepted DependencySourceSetV1 (U-2b; overlay entry from the
# U-2b follow-on), with each package's extracted tree cloned (copy-on-write) out of the temp-cleaned private Cargo homes into
# this work directory, and every file checked against the package's accepted file manifest. Writes u2c-inputs.json.
W = Path(__file__).resolve().parent; os.setpriority(os.PRIO_PROCESS, 0, 10)
U = Path('/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14'); V = Path('/tmp/opensip-implementation/sm-overlay-metadata-2026-10-14')
C = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
DS = W / 'ds'; assert not DS.exists(); DS.mkdir()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
sets = [(s, U) for s in json.loads((U / 'u2b-sets.json').read_text())['sets'] if s['built']] + [(s, V) for s in json.loads((V / 'u2b-sets-entry8.json').read_text())['sets']]
assert len(sets) == 9
out = []
for s, base in sets:
    slug = s['slug']; setdir = base / 'u2b-sets' / slug; desc = json.loads((setdir / 'descriptor.json').read_text()); assert sha(setdir / 'descriptor.json') == json.loads((setdir / 'observations.json').read_text())['descriptor']['sha256']
    audit = json.loads((base / 'u2b-source-audits' / f'{slug}.json').read_text()); roots = {(r['name'], r['version']): Path(r['root']) for r in audit['rows']}
    mans = {r['packageTuple'][0] + '@' + r['packageTuple'][1]: r for r in json.loads((setdir / 'file-manifest-observations.json').read_text())['rows']}
    pkgs = []
    for p in desc['packages']:
        m = mans[p['name'] + '@' + p['version']]; assert m['fileManifestSha256'] == p['fileManifestSha256']
        listing = json.loads(Path(m['fileManifest']['path']).read_text()); dst = DS / slug / f"{p['name']}-{p['version']}"; dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['/bin/cp', '-cR', str(roots[(p['name'], p['version'])]), str(dst)], check=True)
        for f in listing: assert sha(dst / f['path']) == f['contentSha256'], (slug, p['name'], f['path'])
        mp = W / 'manifests' / slug / f"{p['name']}-{p['version']}.json"; mp.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(m['fileManifest']['path'], mp)
        pkgs.append(dict(name=p['name'], version=p['version'], root=str(dst), manifest=str(mp), fileManifestSha256=p['fileManifestSha256'], files=len(listing), bytes=sum(f['byteLength'] for f in listing)))
    dp = W / 'descriptors' / f'{slug}.json'; dp.parent.mkdir(exist_ok=True); shutil.copyfile(setdir / 'descriptor.json', dp)
    entry = s['entry']; repo = C / entry
    out.append(dict(entry=entry, slug=slug, dependencySourceSetId=s['dependencySourceSetId'], descriptor=str(dp), descriptorSha256=sha(dp), packages=pkgs, files=sum(p['files'] for p in pkgs), bytes=sum(p['bytes'] for p in pkgs), repositoryRoot=str(repo)))
    print(entry, len(pkgs), out[-1]['files'], out[-1]['bytes'], flush=True)
(W / 'u2c-inputs.json').write_text(json.dumps(dict(standing='U-2c INPUTS: ACCEPTED DEPENDENCY-SOURCE SETS WITH CLONED, MANIFEST-CHECKED PACKAGE TREES', entries=out), indent=1) + '\n')

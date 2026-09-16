"""Portable rebuild of the author reference package on a successor source (native-v2 laws).

Explicit inputs only; no historical /tmp path is consulted:
  --source   successor source root (the tree holding docs/coop/design-corrections); root runs this on the FROZEN tree
  --package  the old author package root (package15) whose artifact-manifest.json digest is --package-manifest-sha256
  --overlay  the migration overlay (overlay-manifest.json lists every file with its package15 base digest)
  --out      a fresh output directory (must not exist)
  --source-manifest  optional JSON {"files":[{path,sha256,bytes}]} the source must equal (e.g. a frozen manifest)

Steps (each subprocess receipted under OUT/work/receipts): verify old package and overlay base digests; hash the source
tree; build a constructor tree = package15 + overlay; construct every group FROM INPUTS; assemble OUT/package with the
package15 export groups moved to historical-source38-before-native-v2/; pin the source manifest into verify-package.py;
run verify-package.py (structural + complete semantic closure, map controls, seven query checks) and two author
evidence probes (S2 closure membership, U-4b membership vs the owner's discover/assign functions); compare export ids
with package15; write OUT/package/artifact-manifest.json and OUT/rebuild-report.json. Nothing is written outside OUT.
This is AUTHOR construction and self-consistency evidence, never independent review or acceptance.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys, time

p = argparse.ArgumentParser()
p.add_argument('--source', required=True, type=Path)
p.add_argument('--package', required=True, type=Path)
p.add_argument('--package-manifest-sha256', required=True)
p.add_argument('--overlay', required=True, type=Path)
p.add_argument('--out', required=True, type=Path)
p.add_argument('--source-manifest', type=Path, default=None)
p.add_argument('--python', default=sys.executable)
a = p.parse_args()
SRC, OLD, OV, OUT = a.source.resolve(), a.package.resolve(), a.overlay.resolve(), a.out.resolve()
for label, path in (('--source', SRC), ('--package', OLD), ('--overlay', OV)):
    if OUT == path or OUT.is_relative_to(path) or path.is_relative_to(OUT):
        raise SystemExit('--out must be separate from ' + label)
if OUT.exists():
    raise SystemExit('--out exists; use a fresh directory')
WORK = OUT / 'work'
RECEIPTS = WORK / 'receipts'
RECEIPTS.mkdir(parents=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda path: sha(Path(path).read_bytes())
report = {'standing': 'AUTHOR construction and self-consistency evidence on a successor source; not independent review, '
                      'not acceptance, not qualification. Never supply to a blind consumer.',
          'script': str(Path(__file__).resolve()), 'scriptSha256': fsha(__file__), 'commands': []}


def run(label, argv, timeout=3600):
    out = RECEIPTS / label
    out.mkdir()
    argv = [str(x) for x in argv]
    started = time.time()
    proc = subprocess.run(argv, capture_output=True, timeout=timeout)
    (out / 'stdout.txt').write_bytes(proc.stdout)
    (out / 'stderr.txt').write_bytes(proc.stderr)
    row = {'label': label, 'argv': argv, 'exit': proc.returncode, 'seconds': round(time.time() - started, 1),
           'stdoutSha256': sha(proc.stdout), 'stderrSha256': sha(proc.stderr)}
    (out / 'command.json').write_text(json.dumps(row, indent=2) + '\n')
    report['commands'].append(row)
    print(label, proc.returncode, row['seconds'], flush=True)
    return proc


def walk(root):
    rows = []
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x != '__pycache__')
        for name in sorted(files):
            path = Path(d) / name
            data = path.read_bytes()
            rows.append({'path': path.relative_to(root).as_posix(), 'sha256': sha(data), 'bytes': len(data)})
    rows.sort(key=lambda r: r['path'].encode('utf-8'))
    return rows


# 1. Inputs
raw = (OLD / 'artifact-manifest.json').read_bytes()
if sha(raw) != a.package_manifest_sha256:
    raise SystemExit('old package artifact-manifest digest mismatch')
old_manifest = json.loads(raw)
for row in old_manifest['files']:
    if fsha(OLD / row['path']) != row['sha256']:
        raise SystemExit('old package file digest mismatch: ' + row['path'])
overlay_manifest = json.loads((OV / 'overlay-manifest.json').read_text())
for row in overlay_manifest['files']:
    if fsha(OV / row['path']) != row['sha256']:
        raise SystemExit('overlay file digest mismatch: ' + row['path'])
    base = OLD / row['path']
    if row['package15Sha256'] is None:
        if base.exists():
            raise SystemExit('overlay adds a file the base already has: ' + row['path'])
    elif not base.is_file() or fsha(base) != row['package15Sha256']:
        raise SystemExit('overlay base digest mismatch (not this package): ' + row['path'])
source_files = walk(SRC)
source_manifest_bytes = json.dumps({'files': source_files}, indent=1).encode() + b'\n'
if a.source_manifest is not None:
    wanted = json.loads(a.source_manifest.read_text())['files']
    if [(r['path'], r['sha256'], r['bytes']) for r in wanted] != [(r['path'], r['sha256'], r['bytes']) for r in source_files]:
        raise SystemExit('--source does not equal --source-manifest')
report['inputs'] = {'source': str(SRC), 'sourceFiles': len(source_files), 'sourceManifestSha256': sha(source_manifest_bytes),
                    'package': str(OLD), 'packageManifestSha256': a.package_manifest_sha256,
                    'overlay': str(OV), 'overlayManifestSha256': fsha(OV / 'overlay-manifest.json'),
                    'registeredNativeSchemaSha256': fsha(SRC / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'),
                    'registeredEnumerationPlanSchemaSha256': fsha(SRC / 'docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json')}

# 2. Constructor tree = package15 + overlay
CON = WORK / 'constructors'
shutil.copytree(OLD, CON, ignore=shutil.ignore_patterns('__pycache__'), copy_function=shutil.copy2)
for row in overlay_manifest['files']:
    (CON / row['path']).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OV / row['path'], CON / row['path'])
shutil.copy2(OV / 'overlay-manifest.json', CON / 'overlay-manifest.json')

# 3. Construct every group from inputs
B = WORK / 'build'
PY = [a.python, '-I', '-B']
jobs = [('construct-checkpoint3', 'build-checkpoint3.py', 'checkpoint', []),
        ('construct-normalized', 'build-normalized-examples6.py', 'normalized', []),
        ('construct-rust-selection', 'build-rust-selection-examples.py', 'selection', []),
        ('construct-binding-controls', 'build-binding-controls.py', 'binding', []),
        ('construct-normalization-map-controls', 'build-normalization-map-controls.py', 'map-controls', [])]
failed = []
for label, script, dest, extra in jobs:
    if run(label, PY + [CON / script, '--source', SRC, '--package', CON, '--out', B / dest] + extra).returncode != 0:
        failed.append(label)
if run('construct-semantic-controls', PY + [CON / 'build-semantic-controls.py', '--source', SRC, '--package', CON, '--out', B / 'semantic',
                                              '--positive', B / 'checkpoint/checkpoint3']).returncode != 0:
    failed.append('construct-semantic-controls')
construction_status = {}
for group, path in (('normalized-examples6', B / 'normalized/normalized-examples6/construction.json'),
                    ('rust-selection-examples1', B / 'selection/rust-selection-examples1/construction.json')):
    if path.is_file():
        construction_status[group] = json.loads(path.read_text())
        failed.extend(group + ':' + r['name'] for r in construction_status[group] if not r['constructed'])
report['construction'] = {'failed': failed, 'status': construction_status}
if failed:
    (OUT / 'rebuild-report.json').write_text(json.dumps(report, indent=1) + '\n')
    raise SystemExit('construction failed: %s' % failed)

# 4. Assemble the new package
PKG = OUT / 'package'
shutil.copytree(CON, PKG, ignore=shutil.ignore_patterns('__pycache__'), copy_function=shutil.copy2)
HIST = PKG / 'historical-source38-before-native-v2'
HIST.mkdir()
for name in ['checkpoint3', 'normalized-examples6', 'rust-selection-examples1', 'semantic-controls1', 'binding-controls',
             'query-checks1', 'query-assessment.json', 'source-manifest.json', 'artifact-manifest.json', 'README.md',
             'verify-package.py', 'author-properties.json', 'mixed-universe-view.probe.json']:
    if (PKG / name).exists():
        shutil.move(str(PKG / name), str(HIST / name))
# The historical README/verify-package are the package15 bytes, not the overlay versions.
for name in ['README.md', 'verify-package.py']:
    shutil.copy2(OLD / name, HIST / name)
    shutil.copy2(OV / name, PKG / name)
for group, rel in [('checkpoint3', 'checkpoint/checkpoint3'), ('normalized-examples6', 'normalized/normalized-examples6'),
                   ('rust-selection-examples1', 'selection/rust-selection-examples1'), ('semantic-controls1', 'semantic/semantic-controls1'),
                   ('binding-controls', 'binding'), ('normalization-map-controls1', 'map-controls')]:
    shutil.copytree(B / rel, PKG / group, ignore=shutil.ignore_patterns('__pycache__'))
for name in ['construction-provenance.json']:
    for group, rel in [('checkpoint3', 'checkpoint'), ('normalized-examples6', 'normalized'), ('rust-selection-examples1', 'selection'),
                       ('semantic-controls1', 'semantic')]:
        if (B / rel / name).is_file():
            shutil.copy2(B / rel / name, PKG / group / name)
(PKG / 'source-manifest.json').write_bytes(source_manifest_bytes)
verify_text = (PKG / 'verify-package.py').read_text()
if verify_text.count('__SOURCE_MANIFEST_SHA256__') != 1:
    raise SystemExit('verify-package.py source placeholder missing')
(PKG / 'verify-package.py').write_text(verify_text.replace('__SOURCE_MANIFEST_SHA256__', sha(source_manifest_bytes)))
shutil.copy2(OLD / 'artifact-manifest.json', PKG / 'predecessor-artifact-manifest.json')
package_rows = [r for r in walk(PKG) if r['path'] != 'artifact-manifest.json']
(PKG / 'artifact-manifest.json').write_text(json.dumps(
    {'standing': 'Author reference package migrated to native-v2 laws on a captured successor source; verification and independent review pending.',
     'sourceManifestSha256': sha(source_manifest_bytes), 'predecessorArtifactManifestSha256': a.package_manifest_sha256,
     'files': package_rows}, indent=2) + '\n')

# 5. Verification through the owner named by --source, plus author evidence probes
verify = run('verify-package', PY + [PKG / 'verify-package.py', '--source', SRC, '--out', WORK / 'verification'])
report['verification'] = json.loads((WORK / 'verification/verification.json').read_text()) if (WORK / 'verification/verification.json').is_file() else None
probe = run('probe-native-v2-membership', PY + [CON / 'probe-native-v2.py', '--source', SRC, '--package', PKG, '--out', WORK / 'probe-native-v2.json'])
report['nativeV2Probe'] = json.loads((WORK / 'probe-native-v2.json').read_text()) if (WORK / 'probe-native-v2.json').is_file() else None

# 6. Export id comparison with package15
comparison = []
for group in ['checkpoint3', 'normalized-examples6', 'rust-selection-examples1', 'semantic-controls1', 'binding-controls', 'normalization-map-controls1']:
    new_claims = json.loads((PKG / group / 'claims.json').read_text())
    old_claims = json.loads((OLD / group / 'claims.json').read_text()) if (OLD / group / 'claims.json').is_file() else []
    for claim in new_claims:
        previous = next((r for r in old_claims if r['name'] == claim['name']), None)
        comparison.append({'group': group, 'name': claim['name'], 'runId': claim['runId'], 'exportSha256': fsha(PKG / group / claim['path']),
                           'previousRunId': previous['runId'] if previous else None,
                           'previousExportSha256': fsha(OLD / group / previous['path']) if previous else None,
                           'new': previous is None})
report['exportComparison'] = comparison
report['packageManifestSha256'] = fsha(PKG / 'artifact-manifest.json')
report['passed'] = bool(verify.returncode == 0 and probe.returncode == 0)
(OUT / 'rebuild-report.json').write_text(json.dumps(report, indent=1) + '\n')
print(json.dumps({'passed': report['passed'], 'packageManifestSha256': report['packageManifestSha256']}, indent=1))
raise SystemExit(0 if report['passed'] else 1)

"""Freeze complete reviewed-design application content, never apply it.

Run only after actual design/blind acceptance, assembly, prospective validation,
and inventory generation. Final application acceptance remains a separate act.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, tarfile

p = argparse.ArgumentParser()
for name in ('root', 'stage'):
    p.add_argument('--' + name, type=Path, required=True)
p.add_argument('--version', required=True)
a = p.parse_args(); root = a.root.resolve(); stage = a.stage.resolve()
files = stage / 'files'; support = stage / 'support'; dc = 'docs/coop/design-corrections/'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def safe(rel):
    q = Path(rel)
    assert not q.is_absolute() and '..' not in q.parts
    return q
def load(path): return json.loads(path.read_text())
manifest_name = 'application-subject.' + a.version + '.json'
manifest_path = stage / manifest_name
retained = root / dc / 'reviews' / manifest_name
archive = retained.with_name('application-source.' + a.version + '.tar.gz')
assert not manifest_path.exists() and not retained.exists() and not archive.exists()
app = load(files / dc / 'application.v1.json')
assert app['implementationAuthorized'] is False and app['qualificationClaimed'] is False
assert app['applicationSubject']['path'] == dc + 'reviews/' + manifest_name
for field, verdict in [('independentDesignReview', 'ACCEPT'), ('freshBlindConsumerReview', 'ACCEPT-RECONSTRUCTABLE')]:
    record = app[field]; actual = root / safe(record['path'])
    result = load(actual)
    assert sha(actual) == record['sha256'] and result.get('verdict', result.get('overallVerdict')) == verdict
    assert all(isinstance(result.get(k), list) and not result[k] for k in ('newMustIssues', 'newShouldIssues')), 'Required prerequisite findings unresolved or unaccounted'
validation = load(support / 'staged-reference-checks.v1.json')
assert all(row['exitCode'] == 0 for row in validation['commands'])
assert len(validation['commands']) == 7
assert (support / 'native-recording-delta.v1.json').is_file()
# The complete link/provenance assessment must exist for independent review.
assert (support / 'application-link-assessment.v1.json').is_file()
assert load(support / 'application-link-assessment.v1.json')['unexplainedFailures'] == []
selftest = load(support / 'finalizer-selftest.v1.json')
assert selftest['failed'] == [] and selftest['actualApplicationPerformed'] is False
assert selftest['sourceSha256'] == sha(files / dc / 'finalize-application.v1.py')
# Bind the newly executed current-tool checks before any freeze output is created.
current_tools = load(support / 'current-application-tool-checks.v1.json')
assert current_tools['actualApplicationPerformed'] is False
assert len(current_tools['runs']) == 2
assert {Path(row['command'][3]).name for row in current_tools['runs']} == {'check-review-envelope.v2.py', 'check-retain-public.v1.py'}
assert len({row['path'] for row in current_tools['sourceFiles']}) == len(current_tools['sourceFiles'])
for row in current_tools['sourceFiles']:
    src = support / safe(row['path'])
    assert src.is_file() and sha(src) == row['sha256'] and src.stat().st_size == row['bytes'], 'Current-tool source drift'
for row in current_tools['runs']:
    report = support / safe(row['report'])
    assert row['exitCode'] == 0 and sha(report) == row['reportSha256'], 'Current-tool receipt drift'
    measured = load(report)
    assert measured['failed'] == [] and measured['actualApplicationPerformed'] is False
before = stage / 'before'; before.mkdir(exist_ok=False)
rows = []; before_rows = []
for src in sorted(files.rglob('*')):
    if not src.is_file(): continue
    rel = str(src.relative_to(files)); safe(rel)
    assert rel == 'README.md' or rel.startswith('docs/')
    assert not src.is_symlink() and src.resolve().is_relative_to(files)
    live = root / rel
    assert not live.is_symlink() and live.resolve().is_relative_to(root)
    previous = None
    if live.exists():
        assert live.is_file()
        copy = before / rel; copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(live, copy); previous = sha(copy)
        assert previous == sha(live)
        before_rows.append({'path': rel, 'sha256': previous, 'bytes': copy.stat().st_size})
    rows.append({'path': rel, 'sha256': sha(src), 'bytes': src.stat().st_size, 'beforeSha256': previous})
support_rows = []
for src in sorted(stage.rglob('*')):
    if not src.is_file() or src.is_relative_to(files) or src.is_relative_to(before): continue
    rel = str(src.relative_to(stage)); safe(rel)
    assert not src.is_symlink()
    support_rows.append({'path': rel, 'sha256': sha(src), 'bytes': src.stat().st_size})
manifest = {
    'standing': 'FROZEN FINAL APPLICATION CANDIDATE; requires fresh independent application ACCEPT before activation',
    'implementationAuthorized': False, 'qualificationClaimed': False,
    'pathConventions': {'files': 'relative to package/files/', 'beforeImages': 'relative to package/before/', 'support': 'relative to package/'},
    'retainedManifestPath': dc + 'reviews/' + manifest_name,
    'retainedReviewPath': dc + 'reviews/application-review.' + a.version + '/review.json',
    'files': rows, 'beforeImages': before_rows, 'support': support_rows,
    'postReviewBinding': 'Actual independent ACCEPT and exact manifest/review digests are checked by the reviewed finalizer; activation is written last. No anticipated review hash is part of its own subject.',
    'designSubject': app['designSubject'], 'independentDesignReview': app['independentDesignReview'],
    'freshBlindConsumerReview': app['freshBlindConsumerReview']
}
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
shutil.copyfile(manifest_path, retained)
with tarfile.open(archive, 'w:gz') as tar:
    for src in sorted(stage.rglob('*')):
        if src.is_file(): tar.add(src, arcname=str(src.relative_to(stage)), recursive=False)
print(json.dumps({'manifestSha256': sha(manifest_path), 'manifest': str(retained), 'sourceArchive': str(archive), 'files': len(rows), 'beforeImages': len(before_rows), 'supportFiles': len(support_rows)}))

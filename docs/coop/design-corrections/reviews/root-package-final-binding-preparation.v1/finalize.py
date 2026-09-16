"""Bind a completed, rebuilt AUTHOR package to the formal frozen manifest.

Keep the files-only source projection used by its verifier distinct. Preserve
all former metadata and export bytes. This grants no independent grades.
"""
from pathlib import Path
import argparse, hashlib, json, shutil

p = argparse.ArgumentParser()
p.add_argument('--rebuild', type=Path, required=True)
p.add_argument('--manifest', type=Path, required=True)
p.add_argument('--manifest-sha256', required=True)
p.add_argument('--version', type=int, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = a.manifest.read_bytes()
assert sha(raw) == a.manifest_sha256
subject = json.loads(raw)
members = {r['path']: r for r in subject['files']}
source = Path(subject['snapshotRoot'])
for rel, r in members.items():
    b = (source / rel).read_bytes()
    assert sha(b) == r['sha256'] and len(b) == r['bytes'], rel

report_path = a.rebuild / 'rebuild-report.json'
report = json.loads(report_path.read_bytes())
assert report['passed'] is True and not report['construction']['failed']
expected = {'checkpoint3': 1, 'normalized-examples6': 4,
            'rust-selection-examples1': 2, 'semantic-controls1': 3,
            'binding-controls': 3, 'normalization-map-controls1': 4, 'query': 7}
groups = report['verification']['groups']
assert len(groups) == len(expected)
assert {r['group']: r['count'] for r in groups} == expected
assert all(r['passed'] is True for r in groups)
assert len(report['exportComparison']) == 17
names = {
    'checkpoint3': {'author-ts'},
    'normalized-examples6': {'rust', 'rust-partial', 'syntax-code', 'syntax-data'},
    'rust-selection-examples1': {'rust-bin', 'rust-lib-only'},
    'semantic-controls1': {'severity', 'unrelated-scope', 'collapsed-deficiencies'},
    'binding-controls': {'ts-lawful-default', 'ts-invalid-default-entry', 'ts-lawful-explicit-selection'},
    'normalization-map-controls1': {'ts-map-absent', 'ts-map-level-unmapped', 'ts-map-level-swapped', 'ts-spec-outside-closure'},
}
assert {(r['group'], r['name']) for r in report['exportComparison']} == {
    (g, n) for g, ns in names.items() for n in ns}
probe = report['nativeV2Probe']
assert probe['passed'] is True and len(probe['runs']) == 9
assert probe['unitsVsDiscoveryDisagreements'] == []
positive_groups = {'checkpoint3', 'normalized-examples6', 'rust-selection-examples1'}
assert {(r['group'], r['name']) for r in probe['runs']} == {
    (g, n) for g in positive_groups for n in names[g]
} | {('binding-controls', n) for n in ('ts-lawful-default', 'ts-lawful-explicit-selection')}
for r in probe['runs']:
    assert not r['faults'] and r['unitsVsDiscoveryAgree'] is True
    assert r['membership']['assignMembershipAgrees'] is True
    assert r['membership']['discoverUnitsAgrees'] is True
    assert all(c['mapMember'] is True and c['mapped'] is True for c in r['clones'])

old = a.rebuild / 'package'
prior_raw = (old / 'artifact-manifest.json').read_bytes()
assert sha(prior_raw) == report['packageManifestSha256']
prior = json.loads(prior_raw)
for r in prior['files']:
    b = (old / r['path']).read_bytes()
    assert sha(b) == r['sha256'] and len(b) == r['bytes'], r['path']
projection_raw = (old / 'source-manifest.json').read_bytes()
projection = json.loads(projection_raw)
assert projection['files'] == subject['files']
assert sha(projection_raw) == report['inputs']['sourceManifestSha256']
assert sha(projection_raw) != a.manifest_sha256
assert not a.out.exists()
shutil.copytree(old, a.out)
history = a.out / f'historical-before-formal-binding{a.version}'
history.mkdir()
for name in ['artifact-manifest.json', 'README.md', 'evaluation-residual-author-assessment.json']:
    shutil.copy2(a.out / name, history / name)
assessment_path = a.out / 'evaluation-residual-author-assessment.json'
assessment = json.loads(assessment_path.read_bytes())
assert len(assessment['items']) == 30
assessment['historicalSubjectManifestSha256'] = assessment['subjectManifestSha256']
assessment['subjectManifestSha256'] = a.manifest_sha256
assessment['standing'] = f'Frozen source{a.version}-bound inherited author proposals; every independent grade PENDING. Current evidence hashes are custody, not fresh adjudication or historical repair.'
assessment['sourceSha256'] = members[assessment['source']]['sha256']
for item in assessment['items']:
    assert item['independentGrade'] == 'PENDING' and item['applied'] is False
    for e in item['evidence']:
        before = e['sha256']
        e.update(previousSha256=before, sha256=members[e['path']]['sha256'],
                 resolveAgainst=f'frozen candidate{a.version}',
                 currentIndependentAssessment='PENDING',
                 sourceBytesChanged=before != members[e['path']]['sha256'])
assessment_path.write_text(json.dumps(assessment, indent=2) + '\n')
(a.out / f'formal-source-manifest.v{a.version}.json').write_bytes(raw)
binding = {'standing': 'Formal frozen source binding of completed author reconstruction; independent review, blind reconstruction and application pending.',
           'formalSubjectManifestSha256': a.manifest_sha256,
           'filesOnlySourceProjectionSha256': sha(projection_raw),
           'projectionEqualsFormalFiles': True,
           'rebuildReportSha256': sha(report_path.read_bytes()),
           'rebuiltPackageBeforeMetadataBindingSha256': sha(prior_raw),
           'exportCount': 17, 'queryCount': 7, 'membershipProbeCount': 9,
           'exportsChangedByBinding': False, 'independentGradesGranted': 0}
(a.out / f'source-binding.v{a.version}.json').write_text(json.dumps(binding, indent=2) + '\n')
readme = (a.out / 'README.md').read_text()
(a.out / 'README.md').write_text(
    f'# Frozen source{a.version} author package — independent review pending\n\n'
    f'The formal source manifest and files-only projection are bound separately in source-binding.v{a.version}.json. '
    'The completed rebuild verified 17 Run/control exports, seven query cases and nine membership comparisons. '
    'This metadata binding changes no export or replay helper. All 30 independent residual grades remain PENDING. '
    'Never provide this author package to the blind consumer.\n\n' + readme)
metadata = {'artifact-manifest.json', 'README.md', 'evaluation-residual-author-assessment.json'}
for r in prior['files']:
    if r['path'] not in metadata:
        assert (a.out / r['path']).read_bytes() == (old / r['path']).read_bytes(), r['path']
rows = []
for f in sorted(a.out.rglob('*')):
    if f.is_file() and f != a.out / 'artifact-manifest.json':
        assert not f.is_symlink()
        b = f.read_bytes()
        rows.append({'path': f.relative_to(a.out).as_posix(), 'sha256': sha(b), 'bytes': len(b)})
(a.out / 'artifact-manifest.json').write_text(json.dumps({
    'standing': binding['standing'], 'sourceManifestSha256': sha(projection_raw),
    'formalSubjectManifestSha256': a.manifest_sha256,
    'predecessorArtifactManifestSha256': sha(prior_raw), 'files': rows}, indent=2) + '\n')
print(json.dumps({'package': str(a.out), 'files': len(rows),
                  'packageManifestSha256': sha((a.out / 'artifact-manifest.json').read_bytes()),
                  **binding}, indent=2))

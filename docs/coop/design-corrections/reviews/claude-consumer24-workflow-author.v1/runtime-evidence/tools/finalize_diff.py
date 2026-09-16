"""Full diff, changed-file hashes relative to frozen source38, touched/dependency custody, unexpected-change scan.

usage: python -I -B finalize_diff.py
Does not hash all 12,904 files: changed files are found by mtime newer than the recorded copy receipt plus a name walk
for added/removed paths; every listed changed file is then hashed against the source38 manifest and the parent file.
"""
import difflib, hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
WORK = RT / 'work/source38-work'
PARENT = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
WANT = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
DEPENDENCIES = [
    'docs/coop/design-corrections/foundation/canonical.py',
    'docs/coop/design-corrections/foundation/identity-model.v3.py',
    'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
    'docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py',
    'docs/coop/design-corrections/foundation/check-current-profile.v3.py',
    'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py',
    'docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py',
    'docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/check-comparison-knowledge.v3.py',
    'docs/coop/design-corrections/workflows/check_workflows.v1.py',
    'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
    'docs/coop/design-corrections/workflows/command-inventory.v1.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/detector-manifest.schema.json',
    'docs/coop/design-corrections/check-integration.py',
    'docs/coop/design-corrections/integration-host-model.py',
    'docs/coop/design-corrections/security/check-security-lifecycle.v1.py',
    'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
    'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
    'docs/coop/artifacts/permission-truth-tables.v9.json',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


man_raw = MAN.read_bytes()
listed = {x['path']: x['sha256'] for x in rows(json.loads(man_raw))}
copy_time = (RT / 'receipts/parent-custody-and-copy.json').stat().st_mtime
work_names, modified = set(), []
for d, ds, fs in os.walk(WORK):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), WORK)
        work_names.add(rel)
        if os.stat(os.path.join(d, f)).st_mtime > copy_time:
            modified.append(rel)
added = sorted(work_names - set(listed))
removed = sorted(set(listed) - work_names)
changed = []
diff_chunks = []
for rel in sorted(modified):
    work_sha = sha(WORK / rel)
    parent_manifest = listed.get(rel)
    parent_file = sha(PARENT / rel) if (PARENT / rel).is_file() else None
    row = {'path': rel, 'source38ManifestSha256': parent_manifest, 'source38ParentFileSha256': parent_file, 'workSha256': work_sha,
           'differsFromSource38': work_sha != parent_manifest, 'parentFileMatchesManifest': parent_file == parent_manifest}
    changed.append(row)
    if work_sha != parent_manifest:
        a = (PARENT / rel).read_text(encoding='utf-8').splitlines(keepends=True)
        b = (WORK / rel).read_text(encoding='utf-8').splitlines(keepends=True)
        diff_chunks.extend(difflib.unified_diff(a, b, fromfile='a/' + rel, tofile='b/' + rel))
(RT / 'diffs').mkdir(exist_ok=True)
full = ''.join(diff_chunks)
(RT / 'diffs/source38-to-corrected.diff').write_text(full)
deps = [{'path': rel, 'source38ManifestSha256': listed.get(rel), 'parentFileSha256': sha(PARENT / rel), 'workSha256': sha(WORK / rel),
         'unchanged': listed.get(rel) == sha(PARENT / rel) == sha(WORK / rel)} for rel in DEPENDENCIES]
report = {'parentManifest': str(MAN), 'parentManifestSha256': hashlib.sha256(man_raw).hexdigest(), 'parentManifestOk': hashlib.sha256(man_raw).hexdigest() == WANT,
          'modifiedByMtime': len(modified), 'addedPaths': added, 'removedPaths': removed,
          'changedFiles': [r for r in changed if r['differsFromSource38']],
          'mtimeTouchedButByteIdentical': [r['path'] for r in changed if not r['differsFromSource38']],
          'parentTouchedFilesStillMatchManifest': all(r['parentFileMatchesManifest'] for r in changed),
          'dependencies': deps, 'dependenciesAllUnchanged': all(d['unchanged'] for d in deps),
          'diffPath': str(RT / 'diffs/source38-to-corrected.diff'), 'diffSha256': hashlib.sha256(full.encode()).hexdigest(), 'diffLines': full.count('\n')}
(RT / 'receipts/final-custody-and-diff.json').write_text(json.dumps(report, indent=1) + '\n')
print(json.dumps({k: (v if k not in ('changedFiles', 'dependencies') else len(v)) for k, v in report.items()}, indent=1))
print(json.dumps([(r['path'], r['source38ManifestSha256'][:12], r['workSha256'][:12]) for r in report['changedFiles']], indent=1))

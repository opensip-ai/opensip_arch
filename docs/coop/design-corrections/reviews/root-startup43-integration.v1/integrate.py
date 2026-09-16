"""Finish the existing startup correction handoff; no reviewer assignment or acceptance."""
from pathlib import Path
import hashlib, json, shutil

B = Path('/tmp/opensip-design-corrections')
L = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O = Path(__file__).resolve().parent
A = B/'claude-provider-startup43-correction.v1'
S = A/'work/candidate'
W = B/'claude-provider-wire43-correction.v1/work/candidate'
T = B/'source43-provider-wire-successor.v1/source'
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def census(root):
    return {p.relative_to(root).as_posix(): h(p) for p in root.rglob('*')
            if p.is_file() and not any(x in ('.git','__pycache__') for x in p.relative_to(root).parts)}
assert not (O/'integration.json').exists()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode'] == 0
public = L/A.name/'final-public-artifact-manifest.json'
assert public.is_file()
m = json.loads(public.read_bytes())
parent = json.loads((L/'candidate-subject.v43.json').read_bytes())
P = Path(parent['snapshotRoot'])
stored = 0
for row in m['files']:
    p = A/row['runtimePath']
    assert h(p) == row['sha256'] and p.stat().st_size == row['bytes'], row['runtimePath']
    q = L/A.name/row['retainedPath'] if 'retainedPath' in row else P/row['sameAsSubjectPath']
    assert h(q) == row['sha256'] and q.stat().st_size == row['bytes'], str(q)
    stored += 'retainedPath' in row
wc, sc, tc = census(W), census(S), census(T)
assert wc == tc, 'Preserve unexpected isolated integration changes'
assert set(wc) <= set(sc), 'No source removal authorized'
rows = json.loads((A/'delta/incremental-vs-wire43/files.json').read_bytes())['changed']
actual = {p for p in sc if sc[p] != wc.get(p)}
assert actual == {r['path'] for r in rows}
for r in rows:
    rel = r['path']
    assert wc.get(rel) == r['wire43ParentSha256'] and sc[rel] == r['currentSha256']
    q = T/rel
    if q.exists():
        before = O/'before'/rel
        before.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(q, before)
    q.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(S/rel, q)
assert census(T) == sc
repro = json.loads((B/'root-startup-schema-reproduction.v1/reproduction.json').read_bytes())
for r in repro['rows']:
    assert h(S/r['path']) == r['sha256']
assert h(S/'docs/coop/design-corrections/native/provider_startup_model.v1.py') == '3f75b859b45c4fc6d5e5c8ede642a981d8d83bdf55d8e19ef7c9ffe7d5e8d494'
for v in (9,10,11):
    rel = f'docs/v2/architecture/implementation-normative-inputs.v{v}.json'
    assert h(T/rel) == h(P/rel)
report = {
    'standing': 'Completed actual Claude startup correction integrated exactly into isolated source; no acceptance or readiness. No new agent work assigned.',
    'source': str(T), 'publicManifestSha256': h(public),
    'allPublicRowsVerified': len(m['files']), 'storedPublicRows': stored,
    'reviewSha256': h(A/'review.json'), 'markdownSha256': h(A/'review.md'),
    'incrementalDeltaSha256': h(A/'delta/incremental-vs-wire43/files.json'),
    'incrementalPatchSha256': h(A/'delta/incremental-vs-wire43/unified.patch'),
    'cumulativeDeltaSha256': h(A/'delta/cumulative-vs-frozen43/files.json'),
    'incrementalFiles': len(rows), 'added': sum(r['status']=='added' for r in rows),
    'allAuthorWorkDiffVerified': True, 'integratedFiles': len(sc),
    'schemaAndOrderReproducedExact': True, 'historicalPlanningLayersUnchanged': [9,10,11],
    'readEvidence': ['root-startup-current-read.v1/read.json','root-startup-schema-reproduction.v1/reproduction.json'],
    'rootRead': ['full final author Markdown and JSON','all 49 case outcomes and refusal details via projection','all eight before/after rows with prose-transcription limits','full final startup model and native model/checker incremental patches','full section 0 and 9.7 plus earlier full source edit generator','all nine mutation controls and results'],
    'remaining': ['R-1 advisory closed-world unexamined representation','R-2 observation other unavailable reasons remain post-Analyze','R-3 root planning binding to finish','R-4 host cancellation reduction outside helper','R-5 coverage commitment recomputation outside helper','R-6 Rust Cancelled validation outside helper'],
    'futureReviewGates': 'Independent successor review, original blind-consumer successor review and fresh application review remain queued under latest user instruction.'
}
(O/'integration.json').write_text(json.dumps(report, indent=2)+'\n')
dest = L/O.name
assert not dest.exists()
shutil.copytree(O, dest)
print(json.dumps(report))

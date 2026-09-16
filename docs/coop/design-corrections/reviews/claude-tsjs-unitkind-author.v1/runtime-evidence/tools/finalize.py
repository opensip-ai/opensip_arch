"""Final custody, delta manifest and correction patch. Read-only over LIVE manifest, frozen39 snapshot and the capture.

usage: python -I -B finalize.py
Writes delta-manifest.json, correction.patch and receipts/final-custody.json in this runtime only.
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1')
LIVE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json')
WANT = 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'
WORK = RT / 'work/source'
BEFORE = RT / 'work/before'


def sha(b):
    return hashlib.sha256(b).hexdigest()


raw = LIVE.read_bytes()
manifest = json.loads(raw)
rows = {r['path']: r for r in manifest['files']}
edit_rows = [json.loads(l) for l in (RT / 'receipts/edits.jsonl').read_text().splitlines() if l.strip()]
touched = sorted({r['path'] for r in edit_rows})
last = {}
for r in edit_rows:
    last[r['path']] = r
work_files = {}
for d, ds, fs in os.walk(WORK):
    for f in fs:
        p = Path(d) / f
        work_files[str(p.relative_to(WORK))] = p
new_files = sorted(set(work_files) - set(rows))
missing = sorted(set(rows) - set(work_files))
pycache = sorted(p for p in work_files if '__pycache__' in p or p.endswith('.pyc'))
changed, unexpected = [], []
for rel, row in rows.items():
    p = work_files.get(rel)
    if p is None:
        continue
    data = p.read_bytes()
    if sha(data) != row['sha256'] or len(data) != row['bytes']:
        changed.append(rel)
        if rel not in touched:
            unexpected.append(rel)
delta = []
for rel in touched:
    b = (BEFORE / rel).read_bytes()
    a = (WORK / rel).read_bytes()
    delta.append({'path': rel, 'before': {'sha256': sha(b), 'bytes': len(b)}, 'after': {'sha256': sha(a), 'bytes': len(a)},
                  'beforeEqualsFrozen39Member': sha(b) == rows[rel]['sha256'] and len(b) == rows[rel]['bytes'],
                  'edits': [{'label': r['label'], 'replacements': r['replacements'], 'beforeSha256': r['beforeSha256'], 'afterSha256': r['afterSha256']}
                            for r in edit_rows if r['path'] == rel],
                  'chainEndsAtAfter': last[rel]['afterSha256'] == sha(a)})
chunks = []
for rel in touched:
    chunks.extend(difflib.unified_diff((BEFORE / rel).read_text().splitlines(keepends=True), (WORK / rel).read_text().splitlines(keepends=True),
                                       fromfile='a/' + rel, tofile='b/' + rel))
patch = ''.join(c if c.endswith('\n') else c + '\n\\ No newline at end of file\n' for c in chunks)
(RT / 'correction.patch').write_text(patch)
doc = {
    'standing': 'Exact delta of this runtime capture against frozen candidate39; not applied to LIVE, frozen39 or any other runtime; no pins regenerated.',
    'subject': {'liveManifest': str(LIVE), 'sha256': sha(raw), 'expected': WANT, 'ok': sha(raw) == WANT, 'members': len(rows), 'totalBytes': manifest['totalBytes']},
    'changedFiles': delta,
    'unchangedMembersVerified': len(rows) - len(changed),
    'patch': {'path': 'correction.patch', 'sha256': sha(patch.encode()), 'lines': patch.count('\n')},
    'schemaDocumentsChanged': [p for p in touched if p.endswith('.json')],
    'pinsRegenerated': False,
}
(RT / 'delta-manifest.json').write_text(json.dumps(doc, indent=1) + '\n')
res = {'manifestOk': sha(raw) == WANT, 'captureFiles': len(work_files), 'newFiles': new_files, 'missing': missing, 'pycache': pycache,
       'changedVsFrozen39': sorted(changed), 'unexpectedChanges': unexpected, 'touched': touched,
       'deltaManifestSha256': sha((RT / 'delta-manifest.json').read_bytes()), 'patchSha256': doc['patch']['sha256']}
res['ok'] = res['manifestOk'] and not (new_files or missing or pycache or unexpected) and sorted(changed) == touched and all(d['beforeEqualsFrozen39Member'] and d['chainEndsAtAfter'] for d in delta)
(RT / 'receipts/final-custody.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps(res, indent=1))
sys.exit(0 if res['ok'] else 1)

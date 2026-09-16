"""Final custody, minimal delta and diff for this runtime. Read-only over the capture and the retained v2 runtime.

usage: python -I -B finalize.py
Writes diffs/capture-to-work.diff and receipts/final-custody-and-diff.json (never into the work tree).
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1')
SRC = Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
WORK = RT / 'work/source'
EXCLUDE = 'docs/coop/design-corrections/reviews/'
V2 = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2')
V2_RECORDED = {
    'review.md': '609011cd9d002ce065a934c9ee6d76433a0a3fb00e0442f72e4c17405b1c5c40',
    'review.json': '6dbde41be990515c55d7248d720d7af46f2e6b4da5763b431a10187d7112155b',
    'receipts/final-custody-and-diff.json': 'c8d38d14de17bfeb100a3c2f1e91f88703735172d631306e3e65139059da4f95',
    'diffs/source38-to-v2.diff': 'f5fdab1d758f187ed00622c9b3dba141afbe5bbeb33aa539bacd7c1b5a271600',
    'diffs/v1-to-v2.diff': 'be055eb71388fc5a71a17f4546b0ebe368ca9c802a16f8c451034197e1341fb9',
    'receipts/edits/text-edits.jsonl': '95de12acdc68064580281ecea0ff923929f766a63fcc51439e0f18d5745c3b64',
}
S38_MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def walk(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = Path(d) / f
            out[str(p.relative_to(root))] = sha(p.read_bytes())
    return out


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


def manifest_digest(m):
    return sha(''.join(p + '\t' + h + '\n' for p, h in sorted(m.items())).encode())


copy_receipt = json.loads((RT / 'receipts/source-custody-and-copy.json').read_text())
recorded_full = json.loads((RT / 'receipts/source-full-manifest.json').read_text())
core = copy_receipt['core']

# 1. capture unchanged since the copy (read-only re-hash)
capture_now = walk(SRC)
capture_mismatch = sorted(p for p in set(recorded_full) | set(capture_now) if recorded_full.get(p) != capture_now.get(p))

# 2. retained v2 runtime byte-unchanged: recorded artifacts and its whole work tree against its own final hashmap
v2_artifacts = {rel: {'recorded': h, 'now': sha((V2 / rel).read_bytes()) if (V2 / rel).exists() else None} for rel, h in V2_RECORDED.items()}
v2_artifact_mismatch = sorted(rel for rel, r in v2_artifacts.items() if r['recorded'] != r['now'])
v2_final = json.loads((V2 / 'receipts/final-custody-and-diff.json').read_text())
s38 = {x['path']: x['sha256'] for x in rows(json.loads(S38_MANIFEST.read_bytes()))}
v2_expected = dict(s38)
v2_expected.update({r['path']: r['v2Sha256'] for r in v2_final['changedFilesVsSource38']})
v2_tree_now = walk(V2 / 'work/source38-work')
v2_tree_mismatch = sorted(p for p in set(v2_expected) | set(v2_tree_now) if v2_expected.get(p) != v2_tree_now.get(p))

# 3. minimal delta of this runtime's work copy against the capture core
work_now = walk(WORK)
changed = sorted(p for p in work_now if p in core and core[p] != work_now[p])
new_files = sorted(p for p in work_now if p not in core)
missing = sorted(p for p in core if p not in work_now)
pycache = sorted(p for p in work_now if '__pycache__' in p or p.endswith('.pyc'))
edit_rows = [json.loads(line) for line in (RT / 'receipts/edits/text-edits.jsonl').read_text().splitlines() if line.strip()]
last_after = {}
for r in edit_rows:
    last_after[r['path']] = r['afterSha256']
unexpected = sorted(set(changed) - set(last_after))
chain_broken = sorted(p for p, h in last_after.items() if work_now.get(p) != h)
first_before = {}
for r in edit_rows:
    first_before.setdefault(r['path'], r['beforeSha256'])
before_not_capture = sorted(p for p, h in first_before.items() if core.get(p) != h)


def lines(p):
    return p.read_bytes().decode('utf-8').splitlines(keepends=True)


chunks = []
for rel in changed:
    chunks.extend(difflib.unified_diff(lines(SRC / rel), lines(WORK / rel), fromfile='capture/' + rel, tofile='work/' + rel))
diff = ''.join(x if x.endswith('\n') else x + '\n\\ No newline at end of file\n' for x in chunks)
(RT / 'diffs').mkdir(exist_ok=True)
(RT / 'diffs/capture-to-work.diff').write_text(diff)

res = {
    'capture': str(SRC), 'captureFiles': len(capture_now), 'captureFullManifestDigest': manifest_digest(capture_now),
    'captureFullManifestDigestAtCopy': copy_receipt['sourceFullManifestDigest'], 'captureMismatchSinceCopy': capture_mismatch,
    'excludedPrefix': EXCLUDE, 'coreFiles': len(core), 'coreManifestDigestAtCopy': copy_receipt['coreManifestDigest'],
    'workFiles': len(work_now), 'workManifestDigest': manifest_digest(work_now),
    'retainedV2Artifacts': v2_artifacts, 'retainedV2ArtifactMismatch': v2_artifact_mismatch,
    'retainedV2TreeFiles': len(v2_tree_now), 'retainedV2TreeMismatch': v2_tree_mismatch,
    'changedFiles': [{'path': p, 'captureSha256': core[p], 'workSha256': work_now[p]} for p in changed],
    'newFiles': new_files, 'missingFiles': missing, 'pycache': pycache,
    'editReceiptRows': len(edit_rows), 'unexpectedChanges': unexpected, 'editChainBroken': chain_broken, 'firstEditBeforeNotCapture': before_not_capture,
    'diff': {'path': 'diffs/capture-to-work.diff', 'sha256': sha(diff.encode()), 'lines': diff.count('\n'), 'files': len(changed)},
}
res['ok'] = not (capture_mismatch or v2_artifact_mismatch or v2_tree_mismatch or new_files or missing or pycache or unexpected
                 or chain_broken or before_not_capture or res['captureFullManifestDigest'] != res['captureFullManifestDigestAtCopy'])
(RT / 'receipts/final-custody-and-diff.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) and k not in ('diff',) else v) for k, v in res.items()}, indent=1))
sys.exit(0 if res['ok'] else 1)

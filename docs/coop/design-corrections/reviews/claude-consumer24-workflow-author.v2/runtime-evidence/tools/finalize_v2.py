"""Final custody, hashmaps and diffs for the v2 runtime. Read-only over source38, v1 and the v2 work tree.

usage: python -I -B finalize_v2.py
Writes diffs/source38-to-v2.diff, diffs/v1-to-v2.diff and receipts/final-custody-and-diff.json (never into the work tree).
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2')
V1 = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
PARENT = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
WORK = RT / 'work/source38-work'
V1WORK = V1 / 'work/source38-work'
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
WANT = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
V1_FINAL_WANT_PREFIX = '27e3c03a'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


def walk(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = Path(d) / f
            out[str(p.relative_to(root))] = sha(p.read_bytes())
    return out


def text_lines(p):
    if p is None or not p.exists():
        return []
    return p.read_bytes().decode('utf-8').splitlines(keepends=True)


def unified(paths, old_root, new_root, old_label, new_label):
    chunks = []
    for rel in paths:
        old = old_root / rel if (old_root / rel).exists() else None
        chunks.extend(difflib.unified_diff(text_lines(old), text_lines(new_root / rel),
                                           fromfile=old_label + '/' + rel if old else '/dev/null', tofile=new_label + '/' + rel))
    body = ''.join(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n' for line in chunks)
    return body


man_raw = MAN.read_bytes()
manifest_ok = sha(man_raw) == WANT
s38 = {x['path']: x['sha256'] for x in rows(json.loads(man_raw))}
parent_now = walk(PARENT)
parent_mismatch = sorted(p for p in s38 if parent_now.get(p) != s38[p])
parent_extra = sorted(set(parent_now) - set(s38))

v1_final_raw = (V1 / 'receipts/final-custody-and-diff.json').read_bytes()
v1_final = json.loads(v1_final_raw)
v1_changed = {r['path']: r['workSha256'] for r in v1_final['changedFiles']}
v1_expected = dict(s38)
v1_expected.update(v1_changed)
v1_now = walk(V1WORK)
v1_tree_mismatch = sorted(p for p in v1_expected if v1_now.get(p) != v1_expected[p])
v1_tree_extra = sorted(set(v1_now) - set(v1_expected))

v2_now = walk(WORK)
changed_vs_38 = sorted(p for p in v2_now if s38.get(p) != v2_now[p])
missing_vs_38 = sorted(set(s38) - set(v2_now))
changed_vs_v1 = sorted(p for p in v2_now if v1_expected.get(p) != v2_now[p])
missing_vs_v1 = sorted(set(v1_expected) - set(v2_now))

edit_rows = [json.loads(line) for line in (RT / 'receipts/edits/text-edits.jsonl').read_text().splitlines() if line.strip()]
edited_paths = sorted({r['path'] for r in edit_rows})
last_after = {}
for r in edit_rows:
    last_after[r['path']] = r['afterSha256']
unexpected_v2 = sorted(set(changed_vs_v1) - set(edited_paths))
edit_chain_broken = sorted(p for p in edited_paths if last_after[p] != v2_now.get(p))
new_files = sorted(p for p in v2_now if p not in s38)
pycache = sorted(p for p in v2_now if '__pycache__' in p or p.endswith('.pyc'))

(RT / 'diffs').mkdir(exist_ok=True)
full = unified(changed_vs_38, PARENT, WORK, 'source38', 'v2')
incr = unified(changed_vs_v1, V1WORK, WORK, 'v1', 'v2')
(RT / 'diffs/source38-to-v2.diff').write_text(full)
(RT / 'diffs/v1-to-v2.diff').write_text(incr)

res = {
    'source38ManifestSha256': sha(man_raw), 'manifestOk': manifest_ok, 'source38Paths': len(s38),
    'parentReadonlyMismatch': parent_mismatch, 'parentExtra': parent_extra,
    'v1FinalCustodySha256': sha(v1_final_raw), 'v1FinalCustodyPrefixOk': sha(v1_final_raw).startswith(V1_FINAL_WANT_PREFIX),
    'v1TreeMismatch': v1_tree_mismatch, 'v1TreeExtra': v1_tree_extra,
    'v2Paths': len(v2_now), 'missingVsSource38': missing_vs_38, 'missingVsV1': missing_vs_v1, 'newFilesVsSource38': new_files, 'pycache': pycache,
    'changedFilesVsSource38': [{'path': p, 'source38Sha256': s38.get(p), 'v1Sha256': v1_expected.get(p), 'v2Sha256': v2_now[p]} for p in changed_vs_38],
    'changedFilesV1ToV2': [{'path': p, 'v1Sha256': v1_expected.get(p), 'v2Sha256': v2_now[p]} for p in changed_vs_v1],
    'editReceiptRows': len(edit_rows), 'editedPaths': edited_paths, 'unexpectedV1ToV2Changes': unexpected_v2, 'editChainBroken': edit_chain_broken,
    'diffs': {
        'source38-to-v2.diff': {'sha256': sha(full.encode()), 'lines': full.count('\n'), 'files': len(changed_vs_38)},
        'v1-to-v2.diff': {'sha256': sha(incr.encode()), 'lines': incr.count('\n'), 'files': len(changed_vs_v1)},
    },
}
ok = (manifest_ok and not parent_mismatch and not parent_extra and res['v1FinalCustodyPrefixOk'] and not v1_tree_mismatch and not v1_tree_extra
      and not missing_vs_38 and not missing_vs_v1 and not new_files and not pycache and not unexpected_v2 and not edit_chain_broken)
res['ok'] = ok
(RT / 'receipts/final-custody-and-diff.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
sys.exit(0 if ok else 1)

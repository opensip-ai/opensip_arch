"""Exact-once replacement over this runtime's capture (work/source). Every anchor must occur exactly once in its file and
every file's anchors are checked before ANY file is written (dry pass first). Before-images of first touch are kept in
work/before/, receipts append to receipts/edits.jsonl."""
import hashlib, json, shutil
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1')
ROOT = RT / 'work/source'
BEFORE = RT / 'work/before'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def apply_all(label, edits):
    """edits: list of (rel, [(old, new), ...]). Verifies all anchors first, then writes."""
    staged = []
    for rel, pairs in edits:
        raw = (ROOT / rel).read_bytes()
        text = raw.decode('utf-8')
        for i, (old, new) in enumerate(pairs):
            n = text.count(old)
            if n != 1:
                raise SystemExit('%s: %s anchor %d occurs %d times: %r' % (label, rel, i, n, old[:120]))
            text = text.replace(old, new)
        if rel.endswith('.py'):
            compile(text, rel, 'exec')
        staged.append((rel, raw, text.encode('utf-8'), len(pairs)))
    rows = []
    for rel, raw, new, count in staged:
        keep = BEFORE / rel
        if not keep.exists():
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_bytes(raw)
        (ROOT / rel).write_bytes(new)
        row = {'label': label, 'path': rel, 'replacements': count, 'beforeSha256': sha(raw), 'beforeBytes': len(raw),
               'afterSha256': sha(new), 'afterBytes': len(new)}
        with open(RT / 'receipts/edits.jsonl', 'a') as f:
            f.write(json.dumps(row) + '\n')
        rows.append(row)
    return rows

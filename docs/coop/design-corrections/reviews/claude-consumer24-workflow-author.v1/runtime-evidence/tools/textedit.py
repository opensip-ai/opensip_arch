"""Exact-once text replacement helper shared by the edit scripts. Every old string must occur exactly once."""
import hashlib, json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
ROOT = RT / 'work/source38-work'


def apply(label, rel, pairs):
    p = ROOT / rel
    raw = p.read_bytes()
    text = raw.decode('utf-8')
    for i, (old, new) in enumerate(pairs):
        n = text.count(old)
        if n != 1:
            raise SystemExit('%s: %s replacement %d expected exactly one match, found %d: %r' % (label, rel, i, n, old[:120]))
        text = text.replace(old, new)
    new_raw = text.encode('utf-8')
    p.write_bytes(new_raw)
    row = {'label': label, 'path': rel, 'replacements': len(pairs), 'beforeSha256': hashlib.sha256(raw).hexdigest(), 'afterSha256': hashlib.sha256(new_raw).hexdigest()}
    out = RT / 'receipts/edits'
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'text-edits.jsonl', 'a') as f:
        f.write(json.dumps(row) + '\n')
    return row

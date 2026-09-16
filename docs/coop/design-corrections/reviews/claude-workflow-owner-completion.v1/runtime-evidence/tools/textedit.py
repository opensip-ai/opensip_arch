"""Exact-once text replacement helper for this runtime's work/source copy. Every old string must occur exactly once; a
file is written only after all of its replacements match. Receipts append to receipts/edits/text-edits.jsonl."""
import hashlib, json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1')
ROOT = RT / 'work/source'


def _receipt(row):
    out = RT / 'receipts/edits'
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'text-edits.jsonl', 'a') as f:
        f.write(json.dumps(row) + '\n')
    return row


def apply(label, rel, pairs):
    p = ROOT / rel
    raw = p.read_bytes()
    text = raw.decode('utf-8')
    for i, (old, new) in enumerate(pairs):
        n = text.count(old)
        if n != 1:
            raise SystemExit('%s: %s replacement %d expected exactly one match, found %d: %r' % (label, rel, i, n, old[:160]))
        text = text.replace(old, new)
    new_raw = text.encode('utf-8')
    p.write_bytes(new_raw)
    return _receipt({'label': label, 'path': rel, 'replacements': len(pairs), 'beforeSha256': hashlib.sha256(raw).hexdigest(),
                     'afterSha256': hashlib.sha256(new_raw).hexdigest()})


def edit_json(label, rel, fn):
    """Guarded JSON edit: unmodified bytes must re-serialize identically under a recorded setting."""
    p = ROOT / rel
    raw = p.read_bytes()
    doc = json.loads(raw)
    setting = None
    for ascii_ in (True, False):
        for nl in ('\n', ''):
            if (json.dumps(doc, indent=2, ensure_ascii=ascii_) + nl).encode() == raw:
                setting = (ascii_, nl)
                break
        if setting:
            break
    if setting is None:
        raise SystemExit('round-trip guard refused ' + rel)
    fn(doc)
    new_raw = (json.dumps(doc, indent=2, ensure_ascii=setting[0]) + setting[1]).encode()
    if new_raw == raw:
        raise SystemExit('edit produced no change ' + rel)
    p.write_bytes(new_raw)
    return _receipt({'label': label, 'path': rel, 'json': True, 'beforeSha256': hashlib.sha256(raw).hexdigest(),
                     'afterSha256': hashlib.sha256(new_raw).hexdigest()})

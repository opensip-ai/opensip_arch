"""Assemble review.json: authored per-item account plus the executed receipts it cites (never re-derived by hand).

usage: python -I -B build_review.py
"""
import hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
R = RT / 'receipts'


def load(rel):
    return json.loads((R / rel).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


review = json.loads((RT / 'review.authored.json').read_text())
checks = {}
for label_dir in sorted((R / 'checks').iterdir()):
    for f in sorted(label_dir.glob('*.receipt.json')):
        row = json.loads(f.read_text())
        checks.setdefault(label_dir.name, {})[f.name[:-len('.receipt.json')]] = {k: row.get(k) for k in ('command', 'exitCode', 'seconds', 'checkerSha256', 'stdoutSha256', 'parsed', 'stderrTail')}
    for f in sorted(label_dir.glob('security-lifecycle-unpinned.json')):
        row = json.loads(f.read_text())
        checks.setdefault(label_dir.name, {})['security-lifecycle-unpinned-driver'] = {k: row.get(k) for k in ('standing', 'root', 'checkerSha256', 'counts', 'passed')}
review['executedChecks'] = checks
review['parentCustodyInitial'] = {k: v for k, v in load('parent-custody-and-copy.json').items() if k not in ('parentUnlisted', 'parentMismatch', 'copyNotIndependentOrMismatch')}
review['finalCustodyAndDiff'] = load('final-custody-and-diff.json')
review['editReceipts'] = {'json': load('edits/json-edits.json'), 'text': [json.loads(l) for l in (R / 'edits/text-edits.jsonl').read_text().splitlines() if l.strip()]}
review['identityEffects'] = load('identity-effects.json')
review['residuals'] = load('probes/probe-residuals.final.json')
review['receiptSha256'] = {}
for d, ds, fs in os.walk(R):
    for f in fs:
        p = os.path.join(d, f)
        review['receiptSha256'][os.path.relpath(p, RT)] = sha(p)
review['toolSha256'] = {f: sha(RT / 'tools' / f) for f in sorted(os.listdir(RT / 'tools')) if f.endswith('.py')}
(RT / 'review.json').write_text(json.dumps(review, indent=1, default=str) + '\n')
print(json.dumps({'reviewJsonSha256': sha(RT / 'review.json'), 'checkLabels': sorted(checks), 'changedFiles': len(review['finalCustodyAndDiff']['changedFiles'])}, indent=1))

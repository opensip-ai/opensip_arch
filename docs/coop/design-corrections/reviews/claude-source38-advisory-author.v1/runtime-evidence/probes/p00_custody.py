"""p00: one initial parent custody check of frozen source38, then regular (never hardlinked) working copies.

Verifies the live manifest SHA, every manifest member of candidate-subject.v38 once (bytes and SHA-256), that no
unlisted file exists under docs/, and the completed independent review and root A5 inputs as read-only digests.
Copies docs/ (excluding docs/coop/design-corrections/reviews and __pycache__) into work/baseline and work/edited with
shutil.copy2, then proves every copied file is a distinct inode with st_nlink == 1 and equal bytes.
Output: receipts/p00-custody.json.
"""
import hashlib, json, os, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
WANT = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
REV = Path('/tmp/opensip-design-corrections/claude-independent-design.v38')
A5 = Path('/tmp/opensip-design-corrections/root-consumer24-js-options.v1')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = {'standing': 'initial parent custody and working-copy setup; reference evidence only'}
man_sha = sha(MAN)
out['manifestSha256'] = man_sha
out['manifestVerified'] = man_sha == WANT
man = json.loads(MAN.read_text())
rows = {r['path']: r for r in man['files']}
bad, total = [], 0
for path, r in rows.items():
    p = SRC / path
    if not p.is_file() or p.stat().st_size != r['bytes'] or sha(p) != r['sha256']:
        bad.append(path)
    total += r['bytes']
listed = set(rows)
unlisted = sorted(str(p.relative_to(SRC)) for p in (SRC / 'docs').rglob('*') if p.is_file() and str(p.relative_to(SRC)) not in listed)
out['members'] = {'files': len(rows), 'bytes': total, 'mismatched': bad[:20], 'mismatchCount': len(bad), 'unlisted': unlisted[:20],
                  'unlistedCount': len(unlisted)}
out['reviewInputs'] = {n: sha(REV / n) for n in ('review.md', 'review.json', 'probes/probe_run_termination.py',
                                                  'probes/probe_carrier_sql.py', 'receipts/probe-run-termination.json',
                                                  'receipts/probe-carrier-sql.json')}
out['a5Inputs'] = {n: sha(A5 / n) for n in ('README.md', 'changes.diff', 'changes.json', 'check_reference.py', 'probe.cjs',
                                            'compiler-observations.json', 'compiler-custody.json', 'compiler/lib/typescript.js',
                                            'source/docs/v2/contracts/product-v1/native-evidence.md',
                                            'source/docs/coop/design-corrections/native/native_evidence_model.v2.py')}
cust = json.loads((A5 / 'compiler-custody.json').read_text())
out['a5CompilerMatchesCustody'] = all(sha(A5 / f['path']) == f['sha256'] for f in cust['files'])
a5c = json.loads((A5 / 'changes.json').read_text())
out['a5AfterMatchesChangesJson'] = all(sha(A5 / 'source' / f['path']) == f['afterSha256'] for f in a5c['files'])
out['a5BeforeMatchesSource38'] = all(rows[f['path']]['sha256'] == f['beforeSha256'] for f in a5c['files'])

ignore = shutil.ignore_patterns('__pycache__')


def ign(d, names):
    skip = set(ignore(d, names))
    if Path(d) == SRC / 'docs/coop/design-corrections':
        skip.add('reviews')
    return skip


copies = {}
for tree in ('baseline', 'edited'):
    dst = BASE / 'work' / tree / 'docs'
    if dst.exists():
        raise SystemExit('refusing to overwrite existing ' + str(dst))
    shutil.copytree(SRC / 'docs', dst, ignore=ign, copy_function=shutil.copy2)
    n, links, diff = 0, [], []
    for p in dst.rglob('*'):
        if not p.is_file():
            continue
        rel = str(p.relative_to(dst.parent))
        s, o = p.stat(), (SRC / rel).stat()
        if s.st_nlink != 1 or s.st_ino == o.st_ino:
            links.append(rel)
        if rows.get(rel, {}).get('sha256') != sha(p):
            diff.append(rel)
        n += 1
    copies[tree] = {'files': n, 'hardlinkedOrSameInode': links[:10], 'notManifestEqual': diff[:10], 'notManifestEqualCount': len(diff)}
out['copies'] = copies
expected_excluded = sum(1 for k in rows if k.startswith('docs/coop/design-corrections/reviews/'))
out['excludedReviewMembers'] = expected_excluded
ok = (out['manifestVerified'] and not bad and not unlisted and out['a5CompilerMatchesCustody'] and out['a5AfterMatchesChangesJson']
      and out['a5BeforeMatchesSource38'] and all(not c['hardlinkedOrSameInode'] and not c['notManifestEqualCount'] for c in copies.values())
      and all(c['files'] == len(rows) - expected_excluded for c in copies.values()))
out['allOk'] = ok
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p00-custody.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('reviewInputs', 'a5Inputs')}, indent=1))
sys.exit(0 if ok else 1)

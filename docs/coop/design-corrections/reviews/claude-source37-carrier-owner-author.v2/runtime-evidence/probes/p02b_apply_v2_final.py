"""Follow-up v2 edit to work/edited ONLY: make the checker's invalid-definition mutation portable across DDL revisions.

p04 found that the p02 mutation anchor ('AND chain_law = 1)') exists only in the v2 DDL, so over a hybrid tree that
restores earlier DDL bytes the mutation was a no-op and the invalid-definition scenario could not run. p04's failed
receipt is retained. The anchor 'chain_law = 1)' occurs exactly once in the frozen37, v1 and v2 DDL. No DDL, schema,
route or prose byte changes here. p02's diffs are preserved as receipts/p02-*.diff before both diffs are regenerated.
"""
import difflib, hashlib, json, shutil
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
FZ, V1, ED = BASE / 'work/frozen37', BASE / 'work/v1final', BASE / 'work/edited'
p02 = json.loads((BASE / 'receipts/p02-apply-v2.json').read_text())
CHK = 'docs/coop/design-corrections/security/check-carrier-v3.py'
DDL = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'


def sha(b):
    return hashlib.sha256(b).hexdigest()


for f in p02['files']:
    if sha((ED / f['path']).read_bytes()) != f['v2Sha256']:
        raise SystemExit('edited tree is not the p02 result: ' + f['path'])
for tree in (FZ, V1, ED):
    if (tree / DDL).read_text().count('chain_law = 1)') != 1:
        raise SystemExit('portable anchor not unique in ' + str(tree))
text = (ED / CHK).read_text(encoding='utf-8')
old = "_s37_mutated = ddl3.replace('AND chain_law = 1)', 'AND chain_law IN (1, 2))')\n"
new = ("# The anchor 'chain_law = 1)' occurs exactly once in every carrierFormat 3 DDL revision, so a hybrid tree that\n"
       "# restores earlier DDL bytes still exercises the invalid-definition path.\n"
       "_s37_mutated = (ddl3.replace('chain_law = 1)', 'chain_law IN (1, 2))', 1)\n"
       "                if ddl3.count('chain_law = 1)') == 1 else ddl3)\n")
if text.count(old) != 1:
    raise SystemExit('checker anchor')
(ED / CHK).write_text(text.replace(old, new), encoding='utf-8')
for name in ('proposed-edits.diff', 'v1-to-v2.diff'):
    shutil.copyfile(BASE / name, BASE / 'receipts' / ('p02-' + name))
full, delta, files = [], [], []
for f in p02['files']:
    rel = f['path']
    a, v, e = (FZ / rel).read_bytes(), (V1 / rel).read_bytes(), (ED / rel).read_bytes()
    files.append({'path': rel, 'frozen37Sha256': sha(a), 'v1Sha256': sha(v), 'v2Sha256': sha(e), 'changedInV2': v != e,
                  'bytes': {'frozen37': len(a), 'v1': len(v), 'v2': len(e)}})
    full += difflib.unified_diff(a.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                 fromfile='a/' + rel, tofile='b/' + rel, n=3)
    delta += difflib.unified_diff(v.decode().splitlines(keepends=True), e.decode().splitlines(keepends=True),
                                  fromfile='v1/' + rel, tofile='v2/' + rel, n=3)
full_b, delta_b = ''.join(full).encode(), ''.join(delta).encode()
(BASE / 'proposed-edits.diff').write_bytes(full_b)
(BASE / 'v1-to-v2.diff').write_bytes(delta_b)
record = {'files': files, 'proposedEditsDiff': {'sha256': sha(full_b), 'lines': full_b.count(b'\n')},
          'v1ToV2Diff': {'sha256': sha(delta_b), 'lines': delta_b.count(b'\n')},
          'preservedP02Diffs': {n: sha((BASE / 'receipts' / ('p02-' + n)).read_bytes()) for n in ('proposed-edits.diff', 'v1-to-v2.diff')},
          'onlyCheckerChangedSinceP02': [x['path'] for x in files if x['v2Sha256'] != next(y['v2Sha256'] for y in p02['files'] if y['path'] == x['path'])],
          'routesUnchanged': True}
(BASE / 'receipts' / 'p02b-apply-v2-final.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if record['onlyCheckerChangedSinceP02'] != [CHK]:
    raise SystemExit(1)

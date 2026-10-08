"""Independent read-only checks of the S-OP-2 recording units, S-OP-2-P and S-OP-2-R.

Usage: check_sop2.py [--product PATH] [--rev REV]
Defaults: /Users/sb/code/opensip-ai/opensip and b7b87b7. The product lock is read with `git show` only.
Run with python3 -I -B at nice -n 19. It writes nothing and shares no code with build_sop2.py.

It checks:
1. S-OP-2 r6's pinned bytes are the bytes Codex accepted (ACCEPT-DESIGN-UNIT, no required findings).
2. The parent finding: SDK4 and DRC are outside the lock's accepted set, and no bound passage names them.
3. S-OP-2-P selects exactly the bytes the D-369 application pins, overrides nothing, and its subject is
   exactly its record plus the two files.
4. S-OP-2-R's two overrides: each `before` is the parent's whole selected passage, each `after` is the
   `before` with exactly item 24's quoted sentence inserted (insertion-only), and the SDK4 sentence keeps
   the doctor report's DR-114 tiers. F02 is not a parent.
5. S-OP-2-R's subject: the record, PROPOSAL-r6.md with its accepted sha, PASSAGES.md, README.md and the
   two evidence scripts; the record's candidates are exactly the other members.
6. The two unit drafts are DRAFT-PENDING-REVIEW and name review paths under codex-o1-law-r1.
7. README.md names both units, both selectors and the binding order.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[7]
args = sys.argv[1:]
W = Path(args[args.index('--product') + 1]) if '--product' in args else Path('/Users/sb/code/opensip-ai/opensip')
REV = args[args.index('--rev') + 1] if '--rev' in args else 'b7b87b7'
B = 'docs/implementation/m3/operability/s-op-2/'
SOP2 = B + 'PROPOSAL-r6.md'
SDK4 = 'docs/coop/artifacts/component-sdk-contract.v4.json'
DRC = 'docs/coop/completion/distribution-runtime-completion.v2.md'
APP = 'docs/coop/completion/architecture-application.v1.json'
F02 = 'docs/v2/architecture/02-distribution-and-components.md'
results = []


def check(name, condition):
    results.append((name, bool(condition)))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads((A / path).read_bytes())


def pin(path):
    raw = (A / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def same(row, path):
    return {k: row[k] for k in ('path', 'bytes', 'sha256')} == pin(path)


# 1. The accepted text.
review = load('docs/implementation/m3/reviews/codex-s-op-2-r6/review.json')
sop2_raw = (A / SOP2).read_bytes()
check('1 S-OP-2 r6 is the bytes Codex accepted', review['verdict'] == 'ACCEPT-DESIGN-UNIT'
      and review['requiredFindings'] == [] and review['subjectSha256'] == sha(sop2_raw)
      and review['subject']['bytes'] == len(sop2_raw))

# 2. The parent finding, on the lock at REV.
lock = json.loads(subprocess.run(['git', '-C', str(W), 'show', REV + ':design-lock.json'], check=True,
                                 capture_output=True).stdout)
accepted = set()
named = set()
for key in ('sourceManifest', 'applicationManifest'):
    accepted |= {row['path'] for row in load(lock['approvals'][key]['path'])['files']}
for binding in lock['contractSuccessors']:
    record = load(binding['record']['path'])
    accepted |= {row['path'] for row in record['candidates']} | {binding['record']['path']}
    for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        named.add(entry['parent']['path'])
accepted |= {b['candidate']['path'] for b in lock['inventorySuccessors']}
check('2 SDK4 and DRC are not selected at REV', SDK4 not in accepted and DRC not in accepted)
check('2 no bound passage names SDK4 or DRC', SDK4 not in named and DRC not in named)
check('2 APP is selected at REV', APP in accepted)

# 3. S-OP-2-P.
rp = load(B + 's-op-2-p/successor.json')
app = load(APP)
sdk4_ref = app['rows'][12]
drc_ref = app['evidenceTargets']['D.SDK']['sources'][0]
check('3 APP row 12 is DR-125 and inherits SDK4', sdk4_ref['row'] == 'DR-125'
      and sdk4_ref['inheritedContract']['path'] == SDK4)
check('3 APP D.SDK selects DRC section 8', drc_ref['path'] == DRC and drc_ref['selector'].startswith('## 8. SDK contract'))
check('3 SDK4 candidate equals APP pin', any(r['path'] == SDK4 and r['sha256'] == sdk4_ref['inheritedContract']['pin']
                                            and same(r, SDK4) for r in rp['candidates']))
check('3 DRC candidate equals APP pin', any(r['path'] == DRC and r['sha256'] == drc_ref['pin'] and same(r, DRC)
                                           for r in rp['candidates']))
check('3 S-OP-2-P has exactly two candidates and no override', len(rp['candidates']) == 2 and rp['passageOverrides'] == []
      and 'passageSupersessions' not in rp)
check('3 S-OP-2-P parent is APP', [r['path'] for r in rp['parents']] == [APP] and same(rp['parents'][0], APP))
sp = load(B + 's-op-2-p-subject.json')
check('3 S-OP-2-P subject is record plus candidates', sorted(r['path'] for r in sp['files'])
      == sorted([SDK4, DRC, B + 's-op-2-p/successor.json']) and all(same(r, r['path']) for r in sp['files']))

# 4. S-OP-2-R's overrides.
rr = load(B + 's-op-2-r/successor.json')
lines = sop2_raw.decode('utf-8').splitlines()
quoted = re.findall(r'"([^"]*)"', '\n'.join(lines[920:924]))
append, drc_before, drc_after = quoted[0], quoted[1], quoted[2]
sdk4_rule = load(SDK4)['standardizedFamilies'][1]
drc_lines = (A / DRC).read_text(encoding='utf-8').splitlines()
o_sdk4 = [o for o in rr['passageOverrides'] if o['parent']['path'] == SDK4]
o_drc = [o for o in rr['passageOverrides'] if o['parent']['path'] == DRC]
check('4 exactly two overrides, one per parent', len(rr['passageOverrides']) == 2 and len(o_sdk4) == 1 and len(o_drc) == 1)
o_sdk4, o_drc = o_sdk4[0], o_drc[0]
check('4 SDK4 selector is SF-2 rule', o_sdk4['selector'] == {'jsonPointer': '/standardizedFamilies/1/rule'}
      and sdk4_rule['id'] == 'SF-2')
check('4 SDK4 before is the whole rule', o_sdk4['before'] == sdk4_rule['rule'])
check('4 SDK4 after appends item 24 sentence', o_sdk4['after'] == sdk4_rule['rule'] + append and append.startswith(' For host'))
check('4 SDK4 sentence keeps DR-114 tiers', 'the doctor report keeps its DR-114 redaction tiers' in append)
check('4 DRC selector is line 576', o_drc['selector'] == {'line': 576})
check('4 DRC before is the whole line and item 24 Before', o_drc['before'] == drc_lines[575] == drc_before)
check('4 DRC after is item 24 After', o_drc['after'] == drc_after)
inserted = drc_after[len('meaning.'):len(drc_after) - len(drc_before) + len('meaning.')]
check('4 DRC is insertion-only', drc_after == 'meaning.' + inserted + drc_before[len('meaning.'):]
      and inserted.startswith(' The host reduces'))
check('4 no em dash in new text', '\u2014' not in append and '\u2014' not in inserted)
check('4 parents are exactly SDK4 and DRC, not F02', sorted(r['path'] for r in rr['parents']) == sorted([SDK4, DRC])
      and all(same(r, r['path']) for r in rr['parents']) and F02 not in json.dumps(rr['parents']))
check('4 parents equal S-OP-2-P candidates', sorted(json.dumps(r, sort_keys=True) for r in rr['parents'])
      == sorted(json.dumps(r, sort_keys=True) for r in rp['candidates']))

# 5. S-OP-2-R's subject.
sr = load(B + 's-op-2-r-subject.json')
members = {r['path'] for r in sr['files']}
expected = {SOP2, B + 's-op-2-r/PASSAGES.md', B + 's-op-2-r/README.md', B + 's-op-2-r/evidence/build_sop2.py',
            B + 's-op-2-r/evidence/check_sop2.py', B + 's-op-2-r/successor.json'}
check('5 S-OP-2-R subject members', members == expected and all(same(r, r['path']) for r in sr['files']))
check('5 S-OP-2-R pins the accepted r6 bytes', any(r['path'] == SOP2 and r['sha256'] == review['subjectSha256']
                                                  for r in sr['files']))
check('5 candidates are the subject minus the record', sorted(r['path'] for r in rr['candidates'])
      == sorted(expected - {B + 's-op-2-r/successor.json'}))
check('5 paths sorted and unique', [r['path'] for r in sr['files']] == sorted(members)
      and [r['path'] for r in rr['candidates']] == sorted({r['path'] for r in rr['candidates']}))

# 6. The unit drafts.
for name, unit in (('S-OP-2-P', load(B + 's-op-2-p-unit.json')), ('S-OP-2-R', load(B + 's-op-2-r-unit.json'))):
    tag = name.lower()
    check('6 %s draft status and review path' % name, unit['status'] == 'DRAFT-PENDING-REVIEW'
          and unit['rootSubstantiveAssent'] is False
          and unit['independentReview']['path'] == 'docs/implementation/m3/reviews/codex-o1-law-r1/%s/review.json' % tag)
    check('6 %s draft pins its subject and record' % name, same(unit['subjectManifest'], unit['subjectManifest']['path'])
          and same(unit['acceptedSuccessor'], unit['acceptedSuccessor']['path']))

# 7. The README.
readme = (A / B / 's-op-2-r/README.md').read_text(encoding='utf-8')
for needle in ('S-OP-2-P', 'S-OP-2-R', '/standardizedFamilies/1/rule', 'line 576', 'contract parent is not an accepted base',
               'supersededPassages'):
    check('7 README names %s' % needle, needle in readme)

failed = [n for n, ok in results if not ok]
print(json.dumps({'rev': REV, 'checks': len(results), 'failed': failed}, indent=1))
sys.exit(1 if failed else 0)

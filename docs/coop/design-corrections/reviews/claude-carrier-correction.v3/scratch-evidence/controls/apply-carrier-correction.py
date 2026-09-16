# Control C4 part 1 - apply the minimal carrier correction to the two bound planning inputs.
#
# Reads the frozen inputs read-only. Writes patched copies and unified diffs into scratch only.
# Never modifies an input, Source25, a live repository or product code.
#
# usage: python apply-carrier-correction.py <runtimeRoot>
import difflib
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
INP = os.path.join(ROOT, 'inputs')
PATCHED = os.path.join(ROOT, 'scratch', 'patched')
PATCHES = os.path.join(ROOT, 'scratch', 'patches')
PROPOSAL = os.path.join(ROOT, 'scratch', 'proposal')
os.makedirs(PATCHED, exist_ok=True)
os.makedirs(PATCHES, exist_ok=True)

MD = 'docs/v2/architecture/implementation-boundaries-and-build-plan.md'
PLAN = 'docs/v2/architecture/commit-recovery-plan.v1.json'

report = {'control': 'c4-apply-carrier-correction', 'files': []}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def emit(rel, before_bytes, after_text):
    after_bytes = after_text.encode('utf-8')
    out = os.path.join(PATCHED, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as fh:
        fh.write(after_bytes)
    diff = ''.join(difflib.unified_diff(
        before_bytes.decode('utf-8').splitlines(keepends=True),
        after_text.splitlines(keepends=True),
        fromfile='a/' + rel, tofile='b/' + rel, n=3))
    pname = rel.replace('/', '__') + '.patch'
    with open(os.path.join(PATCHES, pname), 'w', encoding='utf-8') as fh:
        fh.write(diff)
    added = sum(1 for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++'))
    removed = sum(1 for l in diff.splitlines() if l.startswith('-') and not l.startswith('---'))
    report['files'].append({
        'path': rel,
        'beforeSha256': sha(before_bytes), 'beforeBytes': len(before_bytes),
        'afterSha256': sha(after_bytes), 'afterBytes': len(after_bytes),
        'patch': 'scratch/patches/' + pname,
        'addedLines': added, 'removedLines': removed,
    })


# ---- 1. the machine-readable plan: append the 11 planned cases -----------------
plan_before = open(os.path.join(INP, PLAN), 'rb').read()
plan = json.loads(plan_before.decode('utf-8'))
new = json.load(open(os.path.join(PROPOSAL, 'carrier-fault-cases.v1.json'), encoding='utf-8'))

existing_ids = [c['id'] for c in plan['cases']]
assert len(existing_ids) == new['existingCaseCount'], existing_ids
assert len(new['cases']) == new['addedCaseCount']
for c in new['cases']:
    assert c['id'] not in existing_ids, c['id']

CASE_KEYS = ['id', 'checkpoint', 'possibleStoredState', 'initialConclusion',
             'expectedBehavior', 'verificationOwner', 'executionStanding']
assert list(plan['cases'][0].keys()) == CASE_KEYS, list(plan['cases'][0].keys())

for c in new['cases']:
    # Keep the appended rows in exactly the existing closed case shape. The modelProbe
    # citation is deliberately NOT added as a 14th member: the cases array shape is
    # closed and the citations live in scratch/proposal/carrier-fault-cases.v1.json.
    plan['cases'].append({k: c[k] for k in CASE_KEYS})

plan['standing'] = (plan['standing'].rstrip('.') +
                    '. Extended by the carrierFormat 3 correction with cases F38-F48; '
                    'every added case is not-executed.')
plan_after = json.dumps(plan, indent=2, ensure_ascii=False) + '\n'
emit(PLAN, plan_before, plan_after)

# ---- 2. the build plan prose: three anchored edits ----------------------------
md_before = open(os.path.join(INP, MD), 'rb').read()
md = md_before.decode('utf-8')

A1 = 'Do not disable SQL checks or relabel old rows as current.'
A1_NEW = A1 + (
    '\n**COV-03 resolved (proposed, not accepted):** the versioned carrier is\n'
    '`docs/coop/design-corrections/security/carrier-format.v3.md` with DDL\n'
    '`grant-journal.carrier.v3.sql` and dispatch `carrier-dispatch.v3.json`. It adds\n'
    '`carrierFormat` as an axis distinct from `recordSchema` and `stateSchema`, carries TERMINAL as\n'
    'the frozen recordSchema-1 body so schema 3 is not widened, uses the four S8 machine ids, and\n'
    'migrates additively: no constraint disabled and no inherited row rewritten.')

A2 = 'then a new read-only recovery can retry.'
A2_NEW = A2 + (
    ' The exact bounded algorithm, its\n'
    'prefix-anchor cases and the commit-admission gate are\n'
    '`docs/v2/architecture/commit-recovery-readonly.v1.md`. That document also records the executed\n'
    'finding that the v8 witness member `bodySha256` authenticates no interior body under either\n'
    'chain law, so a confirming result is `confirmed-under-retained-custody` and never a\n'
    'cryptographic proof; an unmet anchor is `unknown`, never invalidation.')

for anchor, repl in ((A1, A1_NEW), (A2, A2_NEW)):
    assert md.count(anchor) == 1, anchor
    md = md.replace(anchor, repl)

# regenerate the failure-matrix rows inside the generated block
END = '<!-- END GENERATED COMMIT RECOVERY -->'
assert md.count(END) == 1
rows = ''.join('| %s — %s | %s | %s: %s |\n' % (
    c['id'], c['checkpoint'], c['possibleStoredState'], c['initialConclusion'],
    c['expectedBehavior']) for c in new['cases'])
marker = '\n\n' + END
assert md.count(marker) == 1
md = md.replace(marker, '\n' + rows + '\n' + END)
emit(MD, md_before, md)

report['note'] = (
    'The failure-matrix rows live inside the generated block; they were regenerated from the '
    'appended cases in the same row format the existing F00-F37 rows use. The projects own '
    'generator must be re-run at integration so the block and the JSON stay byte-consistent.')
out = os.path.join(ROOT, 'scratch', 'out', 'c4-patches.json')
with open(out, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(report, indent=1, sort_keys=True) + '\n')
print('WROTE', out)
for f in report['files']:
    print(' ', f['path'], '+%d/-%d' % (f['addedLines'], f['removedLines']))
    print('    before', f['beforeSha256'], f['beforeBytes'])
    print('    after ', f['afterSha256'], f['afterBytes'])

"""Build changed-file-handoff.json with before/after hashes, and the pin-ledger impact."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.dirname(HERE)

OWNED_EIGHT = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
]
FIXTURE = 'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


base = json.load(open(os.path.join(HERE, 'v2-source-baseline.json')))['baseline']
before_rows = {r['path']: r for r in json.load(open(os.path.join(HERE, 'before-images.json')))}
fixture_before = json.load(open(os.path.join(HERE, 'fixture-before-image.json')))[0]

present = {}
for dp, _d, fs in os.walk(SRC):
    for n in fs:
        full = os.path.join(dp, n)
        present[os.path.relpath(full, SRC)] = sha(full)

declared = set(OWNED_EIGHT) | {FIXTURE}
undeclared = sorted(p for p, h in present.items()
                    if p in base and h != base[p]['sha256'] and p not in declared)
new_files = sorted(set(present) - set(base))
missing = sorted(set(base) - set(present))


def row(rel, category, before):
    after = sha(os.path.join(SRC, rel))
    return {'path': rel, 'category': category,
            'beforeSha256': before['beforeSha256'], 'beforeBytes': before['beforeBytes'],
            'afterSha256': after, 'afterBytes': os.path.getsize(os.path.join(SRC, rel)),
            'beforeImage': before['beforeImage'],
            'changed': after != before['beforeSha256']}


owned = [row(rel, 'owned-eight', before_rows[rel]) for rel in OWNED_EIGHT]
fixture = [row(FIXTURE, 'authorized-bounded-fixture-extension', fixture_before)]

# pin ledgers (NOT edited by this author; root seals them)
ledgers = []
for dp, _d, fs in os.walk(SRC):
    for n in fs:
        if 'source-pins' in n:
            ledgers.append(os.path.join(dp, n))
impact = []
for ledger in sorted(ledgers):
    try:
        doc = json.load(open(ledger))
    except Exception:
        continue
    idx = {f.get('path'): f.get('sha256') for f in (doc.get('files') or []) if isinstance(f, dict)}
    broken = sorted(p for p in declared if p in idx and idx[p] != present.get(p))
    unpinned = sorted(p for p in declared if p not in idx)
    if broken or (idx and unpinned):
        impact.append({'ledger': os.path.relpath(ledger, SRC), 'pinnedFiles': len(idx),
                       'brokenByThisAuthor': broken, 'notPinnedYet': unpinned if idx else []})

out = {
    'standing': 'AUTHOR_PENDING_REVIEW. No author acceptance, no root agreement, no application.',
    'authorSourceRoot': SRC,
    'baselineFileCount': len(base), 'currentFileCount': len(present),
    'changedFiles': owned + fixture,
    'undeclaredChanges': undeclared,
    'unexpectedNewFiles': [f for f in new_files if f not in declared],
    'missingFiles': missing,
    'pinLedgersInvalidatedNotEditedByAuthor': impact,
}
json.dump(out, open(os.path.join(RT, 'changed-file-handoff.json'), 'w'), indent=2)

print('baseline', len(base), '-> current', len(present))
print('undeclared', len(undeclared), undeclared[:5])
print('unexpected new', out['unexpectedNewFiles'])
print('missing', len(missing))
for r in owned + fixture:
    print(' ', 'CHANGED' if r['changed'] else 'same   ', r['beforeBytes'], '->', r['afterBytes'], r['path'])
print()
for i in impact:
    print(' ledger', i['ledger'], 'broken', len(i['brokenByThisAuthor']), 'notPinnedYet', i['notPinnedYet'])

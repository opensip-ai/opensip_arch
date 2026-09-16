"""V01 — what exactly changed in the two common schemas and the atom contract, structurally."""
import difflib, json, os

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
R = {}

PAIRS = [
    ('docs/coop/design-corrections/workflows/schemas/common.schema.json', 'workflows-common'),
    ('docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json', 'evaluator3-common'),
]
for rel, tag in PAIRS:
    before = json.load(open(os.path.join(SNAP, rel)))
    after = json.load(open(os.path.join(G, 'source', rel)))
    # structural difference
    def flat(o, path='$', acc=None):
        acc = {} if acc is None else acc
        if isinstance(o, dict):
            for k, v in o.items():
                flat(v, path + '/' + k, acc)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                flat(v, path + '/%d' % i, acc)
        else:
            acc[path] = o
        return acc
    fb, fa = flat(before), flat(after)
    added = {k: fa[k] for k in set(fa) - set(fb)}
    removed = {k: fb[k] for k in set(fb) - set(fa)}
    changed = {k: (fb[k], fa[k]) for k in set(fb) & set(fa) if fb[k] != fa[k]}
    R[tag] = {'addedLeaves': len(added), 'removedLeaves': len(removed), 'changedLeaves': len(changed),
              'added': {k: str(v)[:400] for k, v in added.items()},
              'removed': {k: str(v)[:200] for k, v in removed.items()},
              'changed': {k: {'before': str(v[0])[:300], 'after': str(v[1])[:400]}
                          for k, v in changed.items()}}
    print('\n' + '=' * 92)
    print('%s : +%d leaves, -%d leaves, ~%d changed' % (tag, len(added), len(removed), len(changed)))
    print('=' * 92)
    for k, v in sorted(added.items()):
        print('  ADDED   %s\n          %s' % (k, str(v)[:600]))
    for k, v in sorted(removed.items()):
        print('  REMOVED %s\n          %s' % (k, str(v)[:300]))
    for k, v in sorted(changed.items()):
        print('  CHANGED %s' % k)
        print('    before: %s' % str(v[0])[:340])
        print('    after : %s' % str(v[1])[:340])

json.dump(R, open(os.path.join(OUT, 'v01-schemadiff.json'), 'w'), indent=1, default=str)
print('\nwrote v01-schemadiff.json')

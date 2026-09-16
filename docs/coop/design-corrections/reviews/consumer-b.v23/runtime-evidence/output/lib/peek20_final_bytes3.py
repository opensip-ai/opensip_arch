"""Read-only check that the report's framed identities are the exported ones.

The digests the report quotes that are NOT file hashes are framed content
identities (run/seal/proof/plan/snapshot) and measured per-step-kind
idempotency keys.  This instrument confirms each one is literally present in
the artifact that is supposed to carry it, so "reconciled to the exact final
bytes" covers the identity claims too, not only the file digest table.
Writes nothing.
"""
import json
import os

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def load(rel):
    with open(os.path.join(OUT, rel), encoding='utf-8') as fh:
        return fh.read()


def main():
    review = json.loads(load('blind-review.json'))
    problems = []

    for positive in review['claimedCompletePositives']:
        label = positive.get('runLabel') or positive.get('label') or positive.get('runKey')
        export = positive.get('exportFile') or positive.get('export')
        closure = positive.get('closure', {}).get('file')
        replay = positive.get('freshProcessReplay', {}).get('file')
        bodies = {rel: load(rel) for rel in (export, closure, replay) if rel}
        for key in ('claimedRunId', 'claimedSealId', 'claimedProofId', 'claimedPlanId',
                    'claimedSnapshotId'):
            ident = positive.get(key)
            if not ident:
                continue
            where = [rel for rel, body in bodies.items() if ident in body]
            if not where:
                problems.append('%s %s %s not found in %s'
                                % (label, key, ident[:16], sorted(bodies)))
        print('%-14s export=%s closure=%s replay=%s identities=%d all-present=%s'
              % (label, bool(export), bool(closure), bool(replay),
                 sum(1 for k in ('claimedRunId', 'claimedSealId', 'claimedProofId',
                                 'claimedPlanId', 'claimedSnapshotId') if positive.get(k)),
                 not [p for p in problems if p.startswith(str(label))]))

    keys = review['clauseToCodeAuditHistory']['generation20'][
        'wholePublishedMutationSurface']['measuredKeys']
    mutation = json.loads(load('vectors/indep-mutation-surface.json'))
    body = json.dumps(mutation, sort_keys=True)
    for name, value in sorted(keys.items()):
        present = value in body
        print('mutation key %-24s %s... present in artifact: %s'
              % (name, value[:16], present))
        if not present:
            problems.append('mutation key %s not in artifact' % name)

    print('problems: %s' % (problems or 'none'))


if __name__ == '__main__':
    main()

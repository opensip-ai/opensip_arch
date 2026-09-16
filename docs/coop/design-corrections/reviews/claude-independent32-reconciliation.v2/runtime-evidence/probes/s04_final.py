"""S04 — final: confirm predecessors preserved, both reports agree, emit the final JSON sha/verdict."""
import hashlib, json, os

V2 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2'
V1 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
V32 = '/tmp/opensip-design-corrections/claude-independent-design.v32'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


R = json.load(open(os.path.join(V2, 'review.json')))
md = open(os.path.join(V2, 'review.md'), encoding='utf-8').read()
final = sha(os.path.join(V2, 'review.json'))
print('predecessors preserved:')
for base, tag in ((V1, 'reconciliation.v1'), (V32, 'design.v32')):
    print('   %-20s review.json %s | review.md %s' % (tag, sha(os.path.join(base, 'review.json'))[:16],
                                                      sha(os.path.join(base, 'review.md'))[:16]))
print('   v1 hash recorded in successor lineage:',
      R['recordLineage']['immediateInput']['sha256'][:16],
      '| matches:', R['recordLineage']['immediateInput']['sha256'] == sha(os.path.join(V1, 'review.json')))

ok = {
    'md has the v2 correction section': '## 5. Record-only followup (reconciliation v2)' in md,
    'md names both leftovers': 'V2-01' in md and 'V2-02' in md,
    'md states inherited scope': '"this pass" it means the **v1**' in md,
    'md states no new reads/executions': 'no new reads and no new executions' in md,
    'json verdict ACCEPT': R['verdict'] == 'ACCEPT',
    'json manifest is source32': R['subjectManifestSha256'].startswith('3897e8d1'),
    'json 107 rows': sum(len(R[k]) for k in ('fDispositions', 'evaluationResidualDispositions',
                                             'arDispositions', 'fwDispositions',
                                             'inheritedResidualDispositions',
                                             'scopedReviewOwnerDispositions')) == 107,
    'json v2 corrections list': len(R['correctionsToMyOwnReconciliationV1']) == 3,
}
for k, v in ok.items():
    print('%-42s %s' % (k, 'OK' if v else 'FAIL'))
print('\nFINAL review.json sha256 :', final)
print('FINAL review.md   sha256 :', sha(os.path.join(V2, 'review.md')))
print('VERDICT                  :', R['verdict'])
json.dump({'finalJsonSha256': final, 'finalMdSha256': sha(os.path.join(V2, 'review.md')),
           'verdict': R['verdict'], 'checks': ok},
          open(os.path.join(V2, 'receipts', 's04-final.json'), 'w'), indent=1)
print('\noutput tree:', sorted(os.listdir(V2)))

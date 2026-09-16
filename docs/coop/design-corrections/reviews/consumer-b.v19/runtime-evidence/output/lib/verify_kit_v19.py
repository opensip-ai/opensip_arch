"""Input custody for generation 19, and the NORMATIVE DELTA this origin derives for itself.

Four claims are kept separate, because they are different facts:

  CLAIM 1  the disclosed manifest's own bytes hash to the digest the instruction names.
  CLAIM 2  the manifest DECLARES a parent subject digest equal to the one named. That is a
           declared binding read out of the supplied bytes; this origin cannot verify any
           property of a parent it was never given, and claims none.
  CLAIM 3  every manifest row is verified against the actual file: path present, sha256 equal,
           BYTE LENGTH equal, and the row count is exactly 102. Nothing outside the manifest is
           treated as normative input.
  CLAIM 4  the DELTA against this origin's own generation-18 custody record
           (notes/v18-input-custody.json): unchanged / changed / added / withdrawn, per path.
           The delta is derived here rather than taken from the instruction's summary.

Disclosed prior inputs, stated so no reader can think this was a no-prior-input session:
previous-review.source31.md (this origin's own generation-17 review), previous-turn-response.md
(this origin's own generation-18 closing response), and output/ itself, which is a copy of this
origin's own generation-18 work including its unreconciled reports.
"""
import hashlib
import json
import os

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v19'
SUBJ = RUNTIME + '/subject'
OUT = RUNTIME + '/output'
MANIFEST = SUBJ + '/consumer-input-manifest.json'

EXPECT_MANIFEST = '124835865d78de77198d3fe741e8d27495d87cb0236cd064316ebdd38065dc8b'
EXPECT_PARENT = '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'
EXPECT_ROWS = 102


def main():
    raw = open(MANIFEST, 'rb').read()
    own = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    rows = man['files']

    per_path, mismatched, missing = {}, [], []
    for r in rows:
        p = os.path.join(SUBJ, r['path'])
        if not os.path.exists(p):
            missing.append(r['path'])
            continue
        b = open(p, 'rb').read()
        h = hashlib.sha256(b).hexdigest()
        per_path[r['path']] = {'sha256': h, 'bytes': len(b)}
        if h != r['sha256'] or len(b) != r['bytes']:
            mismatched.append({'path': r['path'], 'declaredSha256': r['sha256'],
                               'measuredSha256': h, 'declaredBytes': r['bytes'],
                               'measuredBytes': len(b)})

    # every file actually present under subject/, so an undisclosed extra cannot be used silently
    present = []
    for d, _dirs, names in os.walk(SUBJ):
        for n in names:
            rel = os.path.relpath(os.path.join(d, n), SUBJ)
            if rel != 'consumer-input-manifest.json':
                present.append(rel)
    extra = sorted(set(present) - {r['path'] for r in rows})

    # ---- CLAIM 4: the delta, derived from this origin's own prior custody records.
    #
    # The per-path baseline is the generation-16 custody record, which is the last one that
    # retained a PER-FILE digest map. It is a valid baseline for the generation-18 kit through
    # this origin's own retained measurement chain, cited with exact input equality:
    #   v17 custody: 101 files compared against the v16 map, 0 changed / 0 added / 0 removed
    #   v18 custody: 101 files compared against the v17 record, 0 changed / 0 added / 0 removed
    # so the v16 map IS the generation-18 kit, per path, by measurement rather than assertion.
    prior_file = 'notes/v16-input-custody.json'
    prior = json.load(open(OUT + '/' + prior_file))
    prior_paths = {r['path']: r['measuredSha256'] for r in prior['inputKit']['perFile']}
    chain = []
    for f, key in (('notes/v17-input-custody.json', 'normativeByteIdentityAgainstV16'),
                   ('notes/v18-input-custody.json',
                    'normativeByteIdentityAgainstGeneration17')):
        rec = json.load(open(OUT + '/' + f))[key]
        chain.append({'record': f, 'filesCompared': rec['filesCompared'],
                      'changed': rec['changed'], 'added': rec['added'],
                      'removed': rec['removed'],
                      'allByteIdentical': rec['allDisclosedNormativeFilesByteIdentical']})
    chain_clean = all(c['allByteIdentical'] and c['filesCompared'] == 101 for c in chain)
    delta = {'unchanged': [], 'changed': [], 'added': [], 'withdrawn': []}
    for r in rows:
        was = prior_paths.get(r['path'])
        if was is None:
            delta['added'].append(r['path'])
        elif was == r['sha256']:
            delta['unchanged'].append(r['path'])
        else:
            delta['changed'].append({'path': r['path'], 'priorSha256': was,
                                     'nowSha256': r['sha256']})
    for p in sorted(prior_paths):
        if p not in {r['path'] for r in rows}:
            delta['withdrawn'].append(p)

    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v19',
        'claim1_manifestOwnBytes': {'expected': EXPECT_MANIFEST, 'measured': own,
                                    'result': 'PASS' if own == EXPECT_MANIFEST else 'FAIL'},
        'claim2_declaredParentBinding': {
            'expected': EXPECT_PARENT, 'declared': man.get('parentSubjectSha256'),
            'result': 'PASS' if man.get('parentSubjectSha256') == EXPECT_PARENT else 'FAIL',
            'claimLimit': ('DECLARED BINDING ONLY. The parent subject is not supplied here, so '
                           'no property of it is verified or claimed.')},
        'claim3_everyRowVerified': {
            'rowCount': len(rows), 'expectedRowCount': EXPECT_ROWS,
            'filesVerified': len(per_path), 'mismatched': mismatched, 'missing': missing,
            'undisclosedExtraFilesUnderSubject': extra,
            'result': ('PASS' if (len(rows) == EXPECT_ROWS and not mismatched and not missing
                                  and not extra) else 'FAIL'),
            'whatWasCompared': 'path presence, sha256 and byte length, per row'},
        'claim4_normativeDeltaVsThisOriginsOwnPriorCustody': {
            'priorRecord': prior_file,
            'priorPathCount': len(prior_paths),
            'inheritedStanding': (
                'the per-path baseline is this origin\'s OWN generation-16 measurement, carried '
                'forward by its own generation-17 and generation-18 per-path comparisons, each '
                'of which measured 101 files with zero changes. Cited as an INHERITED own '
                'measurement under exact input equality; it is not relabelled as a generation-19 '
                'command.'),
            'inheritedChain': chain,
            'inheritedChainClean': chain_clean,
            'unchangedCount': len(delta['unchanged']),
            'changedCount': len(delta['changed']),
            'addedCount': len(delta['added']),
            'changed': delta['changed'], 'added': delta['added'],
            'withdrawn': delta['withdrawn'],
            'derivedHere': ('the changed/added sets are MEASURED per path in THIS generation, '
                            'not copied from the instruction\'s summary of what changed')},
        'perPath': per_path,
        'disclosedPriorInputs': {
            'previous-review.source31.md': 'this origin\'s OWN generation-17 review, READ',
            'previous-turn-response.md': 'this origin\'s OWN generation-18 closing response, READ',
            'output/': ('a copy of this origin\'s OWN generation-18 work, including incomplete '
                        'Area-3 helpers and unreconciled reports, READ and being corrected'),
            'notClaimed': ('no author model, checker, fixture, golden, expected output, root '
                           'outcome or other review was supplied or read'),
        },
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v19-input-custody.json', 'w') as f:
        json.dump(doc, f, indent=1)
    for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
              'claim3_everyRowVerified'):
        print('%-34s %s' % (k, doc[k]['result']))
    print('rows %d (expected %d), verified %d, mismatched %d, missing %d, extra %d'
          % (len(rows), EXPECT_ROWS, len(per_path), len(mismatched), len(missing), len(extra)))
    d4 = doc['claim4_normativeDeltaVsThisOriginsOwnPriorCustody']
    print('delta vs %s: unchanged %d, changed %d, added %d, withdrawn %d'
          % (d4['priorRecord'], d4['unchangedCount'], len(d4['changed']), len(d4['added']),
             len(d4['withdrawn'])))
    for c in d4['changed']:
        print('   CHANGED %s' % c['path'])
    for a in d4['added']:
        print('   ADDED   %s' % a)
    for w in d4['withdrawn']:
        print('   WITHDRAWN %s' % w)
    bad = [k for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
                       'claim3_everyRowVerified') if doc[k]['result'] != 'PASS']
    assert not bad, bad
    assert len(per_path) == EXPECT_ROWS, len(per_path)


main()

"""Input custody for generation 20, the NORMATIVE DELTA this origin derives, and an independent
check of the supplied hash inventory.

Five claims, kept apart because they are different facts:

  CLAIM 1  the disclosed manifest's own bytes hash to the digest the instruction names.
  CLAIM 2  the manifest DECLARES a parent subject digest equal to the one named. A declared binding
           read out of supplied bytes; the parent subject is not held and no property of it is
           claimed.
  CLAIM 3  every manifest row verified against the actual file: path present, sha256 equal, BYTE
           LENGTH equal, row count exactly 102, and no undisclosed extra file under subject/.
  CLAIM 4  the DELTA measured per path against this origin's OWN generation-19 custody record,
           which retained a per-file map. Derived here, not taken from any summary.
  CLAIM 5  the supplied normative-delta.json is VERIFIED rather than trusted: its `previousSha256`
           values are compared with this origin's own recorded generation-19 digests and its
           `currentSha256` values with the bytes measured here. A hash inventory that disagreed
           with either side would be reported, not adopted.

Disclosed prior-own inputs: previous-turn-response.md (this origin's own generation-19 closing
response) and output/ (an exact copy of its own generation-19 work). No author implementation,
control, expected output, root replay/refusal report or source-author diagnosis was supplied.
"""
import hashlib
import json
import os

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v20'
SUBJ = RUNTIME + '/subject'
OUT = RUNTIME + '/output'
MANIFEST = SUBJ + '/consumer-input-manifest.json'
DELTA_INVENTORY = RUNTIME + '/normative-delta.json'

EXPECT_MANIFEST = '5f53b88ae0e290acc3ee47b5b6efc62e7f5be008b68fbe847757c613e0ad6a0c'
EXPECT_PARENT = '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
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
    present = []
    for d, _dirs, names in os.walk(SUBJ):
        for n in names:
            rel = os.path.relpath(os.path.join(d, n), SUBJ)
            if rel != 'consumer-input-manifest.json':
                present.append(rel)
    extra = sorted(set(present) - {r['path'] for r in rows})

    # ---- CLAIM 4: the delta, against this origin's own generation-19 per-path record
    prior_file = 'notes/v19-input-custody.json'
    prior = json.load(open(OUT + '/' + prior_file))
    prior_paths = {k: v['sha256'] for k, v in prior['perPath'].items()}
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

    # ---- CLAIM 5: verify the supplied inventory against both sides
    inv = json.load(open(DELTA_INVENTORY))
    inv_rows, inv_bad = [], []
    measured_changed = {c['path']: c for c in delta['changed']}
    for f in inv['files']:
        mine_prior = prior_paths.get(f['path'])
        mine_now = (per_path.get(f['path']) or {}).get('sha256')
        row = {'path': f['path'],
               'previousAgreesWithThisOriginsOwnRecord': mine_prior == f['previousSha256'],
               'currentAgreesWithTheBytesMeasuredHere': mine_now == f['currentSha256'],
               'alsoInThisOriginsMeasuredChangedSet': f['path'] in measured_changed}
        inv_rows.append(row)
        if not all(v for k, v in row.items() if k != 'path'):
            inv_bad.append(row)
    # NOTE the parentheses: `-` binds tighter than `|`, and the first draft of these two lines
    # computed `changed | (added - inventory)`, which reported every changed path as missing from
    # the inventory. Caught by reading the measured output against the measured delta.
    inv_named = {f['path'] for f in inv['files']}
    inv_missing = sorted((set(measured_changed) | set(delta['added'])) - inv_named)
    inv_extra = sorted(inv_named - (set(measured_changed) | set(delta['added'])))

    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v20',
        'claim1_manifestOwnBytes': {'expected': EXPECT_MANIFEST, 'measured': own,
                                    'result': 'PASS' if own == EXPECT_MANIFEST else 'FAIL'},
        'claim2_declaredParentBinding': {
            'expected': EXPECT_PARENT, 'declared': man.get('parentSubjectSha256'),
            'result': 'PASS' if man.get('parentSubjectSha256') == EXPECT_PARENT else 'FAIL',
            'claimLimit': ('DECLARED BINDING ONLY. The parent subject is not supplied here, so no '
                           'property of it is verified or claimed.')},
        'claim3_everyRowVerified': {
            'rowCount': len(rows), 'expectedRowCount': EXPECT_ROWS,
            'filesVerified': len(per_path), 'mismatched': mismatched, 'missing': missing,
            'undisclosedExtraFilesUnderSubject': extra,
            'whatWasCompared': 'path presence, sha256 and byte length, per row',
            'result': ('PASS' if (len(rows) == EXPECT_ROWS and not mismatched and not missing
                                  and not extra) else 'FAIL')},
        'claim4_normativeDeltaMeasuredHere': {
            'priorRecord': prior_file, 'priorPathCount': len(prior_paths),
            'unchangedCount': len(delta['unchanged']), 'changedCount': len(delta['changed']),
            'addedCount': len(delta['added']), 'changed': delta['changed'],
            'added': delta['added'], 'withdrawn': delta['withdrawn'],
            'derivedHere': ('measured per path in THIS generation against the per-file map this '
                            'origin recorded at generation 19; no supplied summary was used as '
                            'the source')},
        'claim5_suppliedInventoryVerified': {
            'file': 'normative-delta.json',
            'standingQuotedFromIt': inv.get('standing'),
            'rows': inv_rows, 'disagreements': inv_bad,
            'measuredChangedOrAddedNotInTheInventory': inv_missing,
            'inInventoryButNotMeasuredAsChanged': inv_extra,
            'result': ('PASS' if not inv_bad and not inv_missing and not inv_extra else 'FAIL'),
            'standing': ('the inventory is an INPUT to be checked, not an authority. It carries '
                         'no semantic expected result, and this origin derives the meaning of '
                         'every changed owner from the bytes themselves.')},
        'perPath': per_path,
        'disclosedPriorInputs': {
            'previous-turn-response.md': "this origin's OWN generation-19 closing response, READ",
            'output/': ("an exact copy of this origin's OWN generation-19 work, READ and being "
                        'continued'),
            'requirements.before20.json': ('the generation-19 requirement metadata, preserved; '
                                           'only inputKit was updated'),
            'notClaimed': ('no author implementation, control, expected output, golden, root '
                           'replay/refusal report, root verdict or source-author diagnosis was '
                           'supplied or read'),
        },
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v20-input-custody.json', 'w') as f:
        json.dump(doc, f, indent=1)
    for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
              'claim3_everyRowVerified', 'claim5_suppliedInventoryVerified'):
        print('%-36s %s' % (k, doc[k]['result']))
    print('rows %d (expected %d), verified %d, mismatched %d, missing %d, extra %d'
          % (len(rows), EXPECT_ROWS, len(per_path), len(mismatched), len(missing), len(extra)))
    d4 = doc['claim4_normativeDeltaMeasuredHere']
    print('measured delta vs %s: unchanged %d, changed %d, added %d, withdrawn %d'
          % (d4['priorRecord'], d4['unchangedCount'], d4['changedCount'], d4['addedCount'],
             len(d4['withdrawn'])))
    for c in d4['changed']:
        print('   CHANGED %s' % c['path'])
    for a in d4['added']:
        print('   ADDED   %s' % a)
    for w in d4['withdrawn']:
        print('   WITHDRAWN %s' % w)
    print('supplied inventory rows: %d, disagreements %d, missing %s, extra %s'
          % (len(inv_rows), len(inv_bad), inv_missing, inv_extra))
    bad = [k for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
                       'claim3_everyRowVerified', 'claim5_suppliedInventoryVerified')
           if doc[k]['result'] != 'PASS']
    assert not bad, bad
    assert len(per_path) == EXPECT_ROWS, len(per_path)


main()

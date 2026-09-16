"""Input custody for generation 23, the NORMATIVE DELTA this origin derives, and an independent
check of the supplied hash inventory. (The generation-22 verifier's method, pinned to generation 23.)

Five claims, kept apart because they are different facts:

  CLAIM 1  the disclosed manifest's own bytes hash to the digest the instruction names.
  CLAIM 2  the manifest DECLARES a parent subject digest equal to the one named. A declared binding
           read out of supplied bytes; the parent subject is not held and no property of it is
           claimed.
  CLAIM 3  every manifest row verified against the actual file: path present, sha256 equal, BYTE
           LENGTH equal, row count exactly 102, and no undisclosed extra file under subject/.
  CLAIM 4  the DELTA measured per path against this origin's OWN generation-22 custody record
           (notes/v22-input-custody.json perPath). Derived here, not taken from any summary.
  CLAIM 5  the supplied normative-delta.json is VERIFIED rather than trusted: its `previousSha256`
           values against this origin's own recorded generation-22 digests and its `currentSha256`
           values against the bytes measured here.

Disclosed prior-own inputs: previous-turn-response.md (this origin's own generation-22 closing
response), output/ (an exact copy of its own generation-22 work) and requirements.before23.json.
The runtime also holds launcher files that are NOT named as inputs (dispatch.json, launch.py,
process.json, prompt.md, public-events.jsonl); they are listed by name and not opened.
"""
import hashlib
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v23'
SUBJ = RUNTIME + '/subject'
OUT = RUNTIME + '/output'
MANIFEST = SUBJ + '/consumer-input-manifest.json'
DELTA_INVENTORY = RUNTIME + '/normative-delta.json'

EXPECT_MANIFEST = 'e35dc60175ae9741435218614ca1d2aa81a1c69a105358af8af9ce537bde8ea9'
EXPECT_PARENT = 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
EXPECT_ROWS = 102
NOT_INPUTS_LISTED_NOT_OPENED = ('dispatch.json', 'launch.py', 'process.json', 'prompt.md',
                                'public-events.jsonl')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = open(MANIFEST, 'rb').read()
    own = sha(raw)
    man = json.loads(raw)
    rows = man['files']

    per_path, mismatched, missing = {}, [], []
    for r in rows:
        p = os.path.join(SUBJ, r['path'])
        if not os.path.exists(p):
            missing.append(r['path'])
            continue
        b = open(p, 'rb').read()
        h = sha(b)
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

    prior_file = 'notes/v22-input-custody.json'
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
                                     'nowSha256': r['sha256'],
                                     'priorBytes': prior['perPath'][r['path']].get('bytes'),
                                     'nowBytes': r['bytes']})
    for p in sorted(prior_paths):
        if p not in {r['path'] for r in rows}:
            delta['withdrawn'].append(p)

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
    inv_named = {f['path'] for f in inv['files']}
    inv_missing = sorted((set(measured_changed) | set(delta['added'])) - inv_named)
    inv_extra = sorted(inv_named - (set(measured_changed) | set(delta['added'])))

    # S-MISSING-DEP-IS-CUSTODY (V22-D9): every kit document an active module OPENS must resolve to
    # a manifest row; an unresolved one is BLOCKED custody, never an invented recipe
    names = {r['path'] for r in rows} | {'consumer-input-manifest.json'}
    opener = re.compile(r"(_DOC\s*=|load_doc\(|doc_path\(|kitdoc\(|kitjson\(|_reg\(|KIT \+ '/|"
                        r"SUB \+ '/|S\.KIT \+ '/)")
    literal = re.compile(r"""['"]([A-Za-z0-9_./-]+\.(?:json|md))['"]""")
    refs = {}
    lib = OUT + '/lib'
    for n in sorted(os.listdir(lib)):
        if not n.endswith('.py'):
            continue
        for i, line in enumerate(open(os.path.join(lib, n), encoding='utf-8'), 1):
            if not opener.search(line):
                continue
            for m in literal.finditer(line):
                ref = m.group(1).lstrip('/')
                if ref.startswith(('runs/', 'vectors/', 'notes/', 'query/', 'envelopes/',
                                   'traces/', 'checkpoints/', 'blind-review', 'requirements',
                                   'verify-all', 'helper-corrections', 'progress')):
                    continue
                refs.setdefault(ref, []).append('%s:%d' % (n, i))
    resolution, gaps = {}, []
    for ref, sites in sorted(refs.items()):
        cands = [ref, 'docs/coop/design-corrections/' + ref, 'docs/coop/' + ref,
                 'docs/v2/contracts/product-v1/' + ref, 'docs/' + ref]
        hit = next((c for c in cands if c in names), None)
        if hit is None and '/' not in ref:
            by_base = sorted(p for p in names if p.split('/')[-1] == ref)
            hit = by_base[0] if len(by_base) == 1 else None
        resolution[ref] = hit
        if hit is None:
            gaps.append({'reference': ref, 'openedAt': sites[:6]})
    custody_gaps = {
        'rule': 'S-MISSING-DEP-IS-CUSTODY',
        'method': ('every kit document opened by an active library module, found by its opening '
                   'construct, resolved against the verified manifest rows'),
        'documentsOpened': len(refs), 'resolved': sum(1 for v in resolution.values() if v),
        'custodyGaps': gaps,
        'standing': ('an empty array means every essential kit dependency this reconstruction '
                     'reads is held in custody; a non-empty one is BLOCKED input custody for the '
                     'named reference, not a design omission')}

    req_now = json.load(open(RUNTIME + '/requirements.json'))
    req_before = json.load(open(RUNTIME + '/requirements.before23.json'))
    req_diff = sorted(k for k in set(req_now) | set(req_before)
                      if req_now.get(k) != req_before.get(k))

    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v23',
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
                            'origin recorded at generation 22; no supplied summary was used as '
                            'the source'),
            'textualDiffStanding': ('this origin holds no copy of the generation-22 bytes of the '
                                    'changed files, so no textual diff is possible inside this '
                                    'runtime; the meaning of each change is derived from the '
                                    'current bytes against this origin\'s own recorded readings')},
        'claim5_suppliedInventoryVerified': {
            'file': 'normative-delta.json',
            'standingQuotedFromIt': inv.get('standing'),
            'rows': inv_rows, 'disagreements': inv_bad,
            'measuredChangedOrAddedNotInTheInventory': inv_missing,
            'inInventoryButNotMeasuredAsChanged': inv_extra,
            'result': ('PASS' if not inv_bad and not inv_missing and not inv_extra else 'FAIL'),
            'standing': ('the inventory is an INPUT to be checked, not an authority. It carries '
                         'no semantic expected result.')},
        'requirementsMetadata': {
            'topLevelKeysThatDifferFromRequirementsBefore23': req_diff,
            'result': 'PASS' if req_diff == ['inputKit'] else 'FAIL',
            'inputKitNow': req_now.get('inputKit')},
        'custody': custody_gaps,
        'perPath': per_path,
        'disclosedPriorInputs': {
            'previous-turn-response.md': "this origin's OWN generation-22 closing response, READ",
            'output/': ("an exact copy of this origin's OWN generation-22 work, READ and being "
                        'continued'),
            'requirements.before23.json': ('the generation-22 requirement metadata, preserved; '
                                           'only inputKit was updated (measured above)'),
            'notClaimed': ('no author implementation, control, expected output, golden, root '
                           'replay/refusal report, root verdict or source-author diagnosis was '
                           'supplied or read'),
        },
        'runtimeFilesNotNamedAsInputs': {
            'files': [n for n in NOT_INPUTS_LISTED_NOT_OPENED
                      if os.path.exists(os.path.join(RUNTIME, n))],
            'standing': 'present in the runtime, listed by name only, NOT opened or used'},
        'generation21': ('prepared by the launcher and never run: no generation-21 input, output '
                         'or result exists for this origin, so nothing is inherited from it'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v23-input-custody.json', 'w') as f:
        json.dump(doc, f, indent=1)
    for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
              'claim3_everyRowVerified', 'claim5_suppliedInventoryVerified',
              'requirementsMetadata'):
        print('%-36s %s' % (k, doc[k]['result']))
    print('rows %d (expected %d), verified %d, mismatched %d, missing %d, extra %d'
          % (len(rows), EXPECT_ROWS, len(per_path), len(mismatched), len(missing), len(extra)))
    d4 = doc['claim4_normativeDeltaMeasuredHere']
    print('measured delta vs %s: unchanged %d, changed %d, added %d, withdrawn %d'
          % (d4['priorRecord'], d4['unchangedCount'], d4['changedCount'], d4['addedCount'],
             len(d4['withdrawn'])))
    for c in d4['changed']:
        print('   CHANGED %s (%s -> %s bytes)' % (c['path'], c['priorBytes'], c['nowBytes']))
    for a in d4['added']:
        print('   ADDED   %s' % a)
    for w in d4['withdrawn']:
        print('   WITHDRAWN %s' % w)
    print('custody: opened %d, resolved %d, gaps %s'
          % (custody_gaps['documentsOpened'], custody_gaps['resolved'], custody_gaps['custodyGaps']))
    print('supplied inventory rows: %d, disagreements %d, missing %s, extra %s'
          % (len(inv_rows), len(inv_bad), inv_missing, inv_extra))
    bad = [k for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
                       'claim3_everyRowVerified', 'claim5_suppliedInventoryVerified',
                       'requirementsMetadata')
           if doc[k]['result'] != 'PASS']
    assert not bad, bad
    assert len(per_path) == EXPECT_ROWS, len(per_path)


main()

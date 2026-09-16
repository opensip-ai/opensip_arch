"""Input custody for generation 22, the NORMATIVE DELTA this origin derives, and an independent
check of the supplied hash inventory.

Generation 21 was prepared by the launcher and never run; no generation-21 kit custody, output
or result exists for this origin. The prior custody record is therefore this origin's own
generation-20 per-file map, and the delta below is measured against it.

Five claims, kept apart because they are different facts:

  CLAIM 1  the disclosed manifest's own bytes hash to the digest the instruction names.
  CLAIM 2  the manifest DECLARES a parent subject digest equal to the one named. A declared binding
           read out of supplied bytes; the parent subject is not held and no property of it is
           claimed.
  CLAIM 3  every manifest row verified against the actual file: path present, sha256 equal, BYTE
           LENGTH equal, row count exactly 102, and no undisclosed extra file under subject/.
  CLAIM 4  the DELTA measured per path against this origin's OWN generation-20 custody record,
           which retained a per-file map. Derived here, not taken from any summary.
  CLAIM 5  the supplied normative-delta.json is VERIFIED rather than trusted: its `previousSha256`
           values are compared with this origin's own recorded generation-20 digests and its
           `currentSha256` values with the bytes measured here.

Disclosed prior-own inputs: previous-turn-response.md (this origin's own generation-20 closing
response), output/ (an exact copy of its own generation-20 work) and requirements.before22.json.
The runtime also holds launcher files that are NOT named as inputs (dispatch.json, launch.py,
process.json, prompt.md, public-events.jsonl); they were listed by name and not opened.
"""
import hashlib
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v22'
SUBJ = RUNTIME + '/subject'
OUT = RUNTIME + '/output'
MANIFEST = SUBJ + '/consumer-input-manifest.json'
DELTA_INVENTORY = RUNTIME + '/normative-delta.json'

EXPECT_MANIFEST = 'f98d3eb0b7570470cdc85b7033e4558e67d3f66135293aa99897ca7a29951526'
EXPECT_PARENT = 'bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
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

    # ---- CLAIM 4: the delta, against this origin's own generation-20 per-path record
    prior_file = 'notes/v20-input-custody.json'
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
    inv_named = {f['path'] for f in inv['files']}
    inv_missing = sorted((set(measured_changed) | set(delta['added'])) - inv_named)
    inv_extra = sorted(inv_named - (set(measured_changed) | set(delta['added'])))

    # ---- S-MISSING-DEP-IS-CUSTODY (V22-D9): the requirement's observable is `custodyGaps[] with
    # exact path/selector, or empty`, and no generation before this one produced that array --
    # requirement status graded the rule from a manifest hash check. Measured here: every kit
    # document a library module OPENS (a *_DOC constant, or a literal passed to load_doc /
    # doc_path / kitdoc / kitjson / _reg / KIT+ / SUB+) must resolve to a manifest row. An
    # unresolved one is a custody gap to be reported BLOCKED, never an invented recipe.
    # the manifest file itself is held and verified by claim 1; it is not one of its own rows
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

    # requirements.json vs its preserved before-image: only inputKit may differ
    req_now = json.load(open(RUNTIME + '/requirements.json'))
    req_before = json.load(open(RUNTIME + '/requirements.before22.json'))
    req_diff = sorted(k for k in set(req_now) | set(req_before)
                      if req_now.get(k) != req_before.get(k))

    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v22',
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
                            'origin recorded at generation 20; no supplied summary was used as '
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
        'requirementsMetadata': {
            'topLevelKeysThatDifferFromRequirementsBefore22': req_diff,
            'result': 'PASS' if req_diff == ['inputKit'] else 'FAIL',
            'inputKitNow': req_now.get('inputKit')},
        'custody': custody_gaps,
        'perPath': per_path,
        'disclosedPriorInputs': {
            'previous-turn-response.md': "this origin's OWN generation-20 closing response, READ",
            'output/': ("an exact copy of this origin's OWN generation-20 work, READ and being "
                        'continued'),
            'requirements.before22.json': ('the generation-20 requirement metadata, preserved; '
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
    with open(OUT + '/notes/v22-input-custody.json', 'w') as f:
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
    print('supplied inventory rows: %d, disagreements %d, missing %s, extra %s'
          % (len(inv_rows), len(inv_bad), inv_missing, inv_extra))
    bad = [k for k in ('claim1_manifestOwnBytes', 'claim2_declaredParentBinding',
                       'claim3_everyRowVerified', 'claim5_suppliedInventoryVerified',
                       'requirementsMetadata')
           if doc[k]['result'] != 'PASS']
    assert not bad, bad
    assert len(per_path) == EXPECT_ROWS, len(per_path)


main()

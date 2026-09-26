"""Re-check the 458b unit from its committed bytes. Writes check-results.json (deterministic).

Run: python3 -I -B check_cases.py --product <opensip checkout> --packages <dir with jsonschema>
Checks, failing closed on any difference:
  schema     ../schema/platform-profile-set-v2.schema.json equals make_schema.py's mechanical derivation and
             differs from the ref-normalised V1 in exactly the two law-458b places.
  ed25519    the pure-Python RFC 8032 code derives every public key and keyId of profile-roots.json root "2"
             from the public test-only seeds, and re-signs the first V1 admit row byte-identically.
  v1 corpus  the model's V1 shape rule matches all rows of profile-shape-cases.ndjson, and the reference
             verifier order matches `expected` of every row of profile-signature-cases.ndjson (V1-only reader).
  v2 cases   every row of the three ../cases/*.v2.ndjson files is recomputed from the model; every signature
             in the V2 signature file is verified against the root public keys; accessor invariants hold.
Product fixtures are read-only inputs, sha256-pinned in make_cases.py.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
CASES = D.parent / 'cases'
F = 'crates/security/tests/fixtures/'


def rows(path):
    return [json.loads(l) for l in path.read_bytes().splitlines() if l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', required=True, type=Path)
    ap.add_argument('--packages', required=True, type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.packages.resolve()))
    sys.path.insert(0, str(D))
    import ed25519_rfc8032 as ed
    import make_cases as C
    import make_schema as S
    import profile_envelope as E
    import profile_set_v2_model as M
    product = args.product.resolve()
    result = {}

    # schema
    v1, doc = S.derive()
    diffs = S.assert_two_differences(v1, doc)
    assert S.OUT.read_bytes() == (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    result['schema'] = {'sha256': hashlib.sha256(S.OUT.read_bytes()).hexdigest(),
                        'differencesFromV1': ['/' + '/'.join(map(str, p)) for p in diffs]}

    # ed25519 and V1 reproduction
    roots = json.loads(C.read_pinned(product, F + 'profile-roots.json'))
    keys_checked = E.check_root_keys(roots['2'])
    v1_sig = rows(product / (F + 'profile-signature-cases.ndjson'))
    assert hashlib.sha256((product / (F + 'profile-signature-cases.ndjson')).read_bytes()).hexdigest() == \
        '84ed8cc661cfd56905c2fa355a2f2b8faa07f58195badf05309d2fc2077e67b5'
    first = next(q for q in v1_sig if 'admit' in q['expected'])
    stored, envelope = E.sign_envelope(roots['2'], M.decode_metadata(bytes.fromhex(first['stored'])),
                                       [s['keyId'] for s in first['envelope']['signatures']])
    assert stored.hex() == first['stored'] and envelope == first['envelope'], 'first V1 admit row not reproduced'
    v1_sig_mismatch = [q['label'] for q in v1_sig
                       if E.reference_verify(roots[q['root']], bytes.fromhex(q['stored']), q['envelope'], q['corePin'],
                                             q['revoked'], 'v1-only') != q['expected']]
    assert not v1_sig_mismatch, v1_sig_mismatch
    v1_shape = rows(product / (F + 'profile-shape-cases.ndjson'))
    v1_shape_mismatch, v2_valid_in_v1_corpus = [], []
    for q in v1_shape:
        try:
            body = M.decode_metadata(bytes.fromhex(q['hex']))
            valid, valid2 = M.shape_valid(body, 'v1-only'), M.v2_only_shape_valid(body)
        except M.Reject:
            valid = valid2 = False
        if valid != q['valid']:
            v1_shape_mismatch.append(q['label'])
        if valid2:
            v2_valid_in_v1_corpus.append(q['label'])
    assert not v1_shape_mismatch, v1_shape_mismatch
    result['ed25519'] = {'derivedPublicKeysMatched': keys_checked, 'firstV1AdmitRowReSignedByteIdentical': True}
    result['v1Corpus'] = {'shapeRows': len(v1_shape), 'shapeMismatches': 0, 'signatureRows': len(v1_sig),
                          'signatureMismatches': 0, 'v2ValidRowsInV1ShapeCorpus': v2_valid_in_v1_corpus}

    # V2 shape cases
    shape = rows(CASES / 'profile-shape-cases.v2.ndjson')
    for q in shape:
        try:
            body = M.decode_metadata(bytes.fromhex(q['hex']))
            got = (M.v2_only_shape_valid(body), M.shape_valid(body, 'v1-only'))
        except M.Reject:
            got = (False, False)
        assert got == (q['valid'], q['validV1']), q['label']
    labels = {q['label'] for q in shape}
    for need in ('458b:v2:base', '458b:v2:member-absent', '458b:v2:wrong-value:other-string', '458b:v2:wrong-type:null',
                 '458b:v2:on-linux-row:linux-x86_64-gnu', '458b:v2:on-supportedMajors-entry',
                 '458b:v2:on-macos-platform-object', '458b:v2:at-top-level', '458b:v1:with-member', '458b:schema-3:with-member'):
        assert need in labels, need
    assert all(q['validV1'] is False for q in shape if q['label'] != '458b:v1:base-no-member')

    # V2 signature cases
    sig = rows(CASES / 'profile-signature-cases.v2.ndjson')
    verified = attempted = 0
    for q in sig:
        root = roots[q['root']]
        stored = bytes.fromhex(q['stored'])
        for reader, field in (('v1-only', 'expected'), ('v1-or-v2', 'expectedV2')):
            assert E.reference_verify(root, stored, q['envelope'], q['corePin'], q['revoked'], reader) == q[field], (q['label'], field)
        message = E.envelope_message(q['envelope'])
        public = {k['keyId']: bytes.fromhex(k['publicKey']) for k in roots['2']['keys']}
        for s in q['envelope']['signatures']:
            attempted += 1
            verified += ed.verify(public[s['keyId']], message, bytes.fromhex(s['signature']))
    corrupt = sum(len(q['envelope']['signatures']) for q in sig if 'all-corrupt' in q['label']) + \
        sum(1 for q in sig if 'key1-corrupt' in q['label'])
    assert attempted - verified == corrupt, (attempted, verified, corrupt)
    v2_admits = [q['label'] for q in sig if 'admit' in q['expectedV2']]
    assert all('admit' not in q['expected'] for q in sig if q['label'] != '458b:control:v1-body:keys01')
    result['v2SignatureCases'] = {'rows': len(sig), 'signatures': attempted, 'signaturesVerified': verified,
                                  'deliberatelyCorrupt': corrupt, 'v1Admits': 1, 'v2Admits': len(v2_admits)}

    # Refusal spelling against the SELECTED V1 platform corpus (authoritative over the pinned V1 model).
    corpus_raw = C.read_pinned(product, M.SELECTED_CORPUS)
    assert hashlib.sha256(corpus_raw).hexdigest() == M.SELECTED_CORPUS_SHA256
    corpus = [json.loads(l) for l in corpus_raw.splitlines() if l]
    corpus_refusals = {r for q in corpus for r in q['expected']['refusals']}
    fs_rows = fs_match = behavioural = model_errors = 0
    for q in corpus:
        e = q['expected']
        try:
            d = M.V1.platform_admit(q['profileSet'], q['observed'])
        except Exception:
            model_errors += 1  # pinned model raises on non-string observations; the product refuses typed
            continue
        normalised = [M.selected_refusal_spelling(r) for r in d['refusals']]
        if e['refusals'] == [M._INSTALL_ROOT_FS]:
            fs_rows += 1
            fs_match += normalised == e['refusals']
        elif normalised != e['refusals']:
            # Remaining differences are not spellings: the product refuses malformed identities earlier
            # (BUILD_GRAMMAR, OSRELEASE_GRAMMAR, closed kernUuid/dyldCdhash grammar, Ubuntu predicates).
            assert not (normalised and e['refusals'] and normalised[0].split(':')[0] == e['refusals'][0].split(':')[0]
                        and normalised[0].rsplit('_', 1)[0] == e['refusals'][0].rsplit('_', 1)[0]), (q['label'], normalised)
            behavioural += 1
    assert fs_rows == 31 and fs_match == 31, (fs_rows, fs_match)
    result['selectedCorpusRefusalSpelling'] = {
        'corpusRows': len(corpus), 'installRootFsRows': fs_rows, 'installRootFsMatchedAfterNormalisation': fs_match,
        'behaviouralDifferencesNotSpelling': behavioural, 'pinnedModelRaises': model_errors,
        'normalisation': 'NT-TCB-BOOT:INSTALL_ROOT_FS_<fsType> -> NT-TCB-BOOT:INSTALL_ROOT_FS'}

    # V2 platform cases
    plat = rows(CASES / 'platform-admission-cases.v2.ndjson')
    for q in plat:
        for r in q['expected']['refusals']:
            assert r in corpus_refusals, (q['label'], r)
    yields = 0
    for q in plat:
        got = M.projected_decision(q['profileSet'], q['observed'], 'v1-or-v2')
        assert got == q['expected'], q['label']
        if got['matchedInstallAclOmission'] is not None:
            yields += 1
            assert q['profileSet']['profileSetSchema'] == 2 and got['result'] == 'ADMIT' \
                and got['tier'] == 'EXACT-MEASURED' and got['refusals'] == []
    result['v2PlatformCases'] = {'rows': len(plat), 'accessorYields': yields, 'accessorNone': len(plat) - yields}
    result['v2ShapeCases'] = {'rows': len(shape), 'validV2': sum(q['valid'] for q in shape),
                              'validV1': sum(q['validV1'] for q in shape)}
    result['caseFiles'] = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                           for p in sorted(CASES.glob('*.ndjson'))}
    result['standing'] = ('Reference checks over SYNTHETIC fixtures with public test-only seeds. Not the product verifier, '
                          'not a qualification of any boot identity, no Evidence B.')
    raw = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode('utf-8')
    (D / 'check-results.json').write_bytes(raw)
    print(raw.decode())


if __name__ == '__main__':
    main()

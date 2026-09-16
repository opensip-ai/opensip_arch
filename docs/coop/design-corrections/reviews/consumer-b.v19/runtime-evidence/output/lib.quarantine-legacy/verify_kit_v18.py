"""Generation-18 input custody. Written fresh; the previous generation's verifier is
quarantined because its ROOT and its write destination both live in a read-only generation.

Three separate claims, none implying another:

  (1) the held manifest's own SHA-256 equals the value the instruction names;
  (2) the parent digest DECLARED INSIDE that manifest equals the parent value the instruction
      names -- a DECLARED BINDING comparison, never verification of a parent this origin does
      not hold;
  (3) every one of the 101 disclosed normative files re-hashes to its manifest row AND is
      byte-identical to the same path in the generation-17 kit, measured from the per-file
      digests this origin itself recorded then (notes/v17-input-custody.json, which is supplied
      INSIDE this runtime as part of this origin's own copied output).

The instruction states the kit is the exact 101-file kit from 17 with the same manifest and
parent. That statement is not taken on faith: (1)-(3) are measured here, and the measured
result is what the report carries.
"""
import hashlib
import json
import os
import sys

ROOT = '/tmp/opensip-design-corrections/consumer-b.v18'
SUB = ROOT + '/subject'
OUT = ROOT + '/output'
EXPECT_MANIFEST = '4cee77543946d66f2282dcbc7a8621e0b4117d78d37b44cf57a5f0ad3ca5e237'
EXPECT_PARENT = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
SESSION = '79569ae1-10f4-4181-972b-334f7ed2f07a'
ANCESTRY = ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16', 'consumer-b.' + 'v17',
            'consumer-b.' + 'v18']


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    mb = open(SUB + '/consumer-input-manifest.json', 'rb').read()
    man_sha = hashlib.sha256(mb).hexdigest()
    man = json.loads(mb.decode())

    rows, bad, on_disk, listed = [], [], set(), set()
    for d, _dirs, files in os.walk(SUB):
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), SUB)
            if rel != 'consumer-input-manifest.json':
                on_disk.add(rel)
    for f in man['files']:
        listed.add(f['path'])
        p = SUB + '/' + f['path']
        if not os.path.exists(p):
            rows.append({'path': f['path'], 'result': 'MISSING'})
            bad.append(f['path'])
            continue
        h, n = sha(p), os.path.getsize(p)
        ok = h == f['sha256'] and (f.get('bytes') in (None, n))
        rows.append({'path': f['path'], 'result': 'PASS' if ok else 'FAIL',
                     'measuredSha256': h, 'measuredBytes': n,
                     'declaredSha256': f['sha256'], 'declaredBytes': f.get('bytes')})
        if not ok:
            bad.append(f['path'])

    prior, prior_name = None, None
    for cand in ('notes/v17-input-custody.json', 'notes/v16-input-custody.json'):
        try:
            prior = json.load(open(OUT + '/' + cand))
            prior_name = cand
            break
        except Exception:
            continue
    prior_map = {}
    for r in (prior or {}).get('inputKit', {}).get('perFile', []):
        h = r.get('measuredSha256') or r.get('sha256')
        if h:
            prior_map[r['path']] = h
    now_map = {r['path']: r.get('measuredSha256') for r in rows}
    compared = sorted(p for p in now_map if p in prior_map)
    changed = sorted(p for p in compared if prior_map[p] != now_map[p])
    added = sorted(p for p in now_map if p not in prior_map)
    removed = sorted(p for p in prior_map if p not in now_map)

    doc = {
        'consumerId': 'consumer-b.' + 'v18',
        'sessionId': SESSION,
        'sameOriginAncestry': ANCESTRY,
        'ancestryStanding': (
            'one continuous blind consumer origin. Every earlier generation is read-only and '
            'is NOT supplied in this runtime except as this origin\'s own copied output. '
            'Continuation grants no acceptance to any earlier generation: the 17 verdict was '
            'CHANGES_REQUIRED.'),
        'standing': __doc__,
        'disclosedPriorInputs': {
            'previousReviewOfThisOrigin': 'previous-review.source31.md (READ -- it is this '
                                          "origin's own prior review and a disclosed input)",
            'claimThisOriginDoesNotMake': (
                'this origin does NOT claim that no prior review at all was read: its own '
                'generation-17 review was supplied and read. What it claims is that no author '
                'model, root output, expected identifier or result, golden, other origin\'s '
                'review or implementation code was supplied or read.'),
        },
        'inputKit': {
            'manifestPath': 'subject/consumer-input-manifest.json',
            'manifestSha256Measured': man_sha,
            'manifestSha256Expected': EXPECT_MANIFEST,
            'manifestSha256Match': man_sha == EXPECT_MANIFEST,
            'parentSubjectSha256DeclaredInManifest': man.get('parentSubjectSha256'),
            'parentSubjectSha256Expected': EXPECT_PARENT,
            'parentSubjectSha256Match': man.get('parentSubjectSha256') == EXPECT_PARENT,
            'parentVerificationStanding': (
                'DECLARED BINDING ONLY. The parent candidate is not held, so no verification '
                'of it is claimed; only the digest declared inside the held manifest was '
                'compared to the value the instruction names.'),
            'fileCount': len(man['files']),
            'filesVerifiedPass': sum(1 for r in rows if r['result'] == 'PASS'),
            'filesFailed': bad,
            'extraFilesOnDiskNotInManifest': sorted(on_disk - listed),
            'manifestFilesAbsentFromDisk': sorted(listed - on_disk),
            'hashVerification': 'PASS' if (not bad and man_sha == EXPECT_MANIFEST
                                           and man.get('parentSubjectSha256') == EXPECT_PARENT
                                           and not (on_disk ^ listed)) else 'FAIL',
            'perFile': rows,
        },
        'normativeByteIdentityAgainstGeneration17': {
            'measuredFrom': prior_name,
            'filesCompared': len(compared),
            'changed': changed, 'added': added, 'removed': removed,
            'allDisclosedNormativeFilesByteIdentical': not (changed or added or removed),
            'claim': ('MEASURED per path, not accepted on assertion: each of the 101 files '
                      're-hashes to the digest this origin recorded for that path in the '
                      'previous generation.'),
        },
        'consequenceForThisGeneration': (
            'the normative payload is unchanged, so NO Run needs reminting for a changed '
            'clause. Any remint here is caused by a CORRECTION this origin makes, and the '
            'S1/S2 design questions cannot be closed: closing them needs new normative bytes, '
            'and none were supplied.'),
        'notAnOracle': (
            'no author model, checker, reference implementation, root output, expected '
            'identifier, expected result, digest oracle, golden or other origin\'s review was '
            'supplied or read. No live repository and no other /tmp directory was read.'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v18-input-custody.json', 'w') as f:
        json.dump(doc, f, indent=1)
    k = doc['inputKit']
    print('manifest  measured=%s match=%s' % (k['manifestSha256Measured'][:16],
                                              k['manifestSha256Match']))
    print('parent    declared=%s match=%s (declared binding only)'
          % ((k['parentSubjectSha256DeclaredInManifest'] or '')[:16],
             k['parentSubjectSha256Match']))
    print('files     %d/%d PASS  extra=%s missing=%s'
          % (k['filesVerifiedPass'], k['fileCount'],
             k['extraFilesOnDiskNotInManifest'], k['manifestFilesAbsentFromDisk']))
    n = doc['normativeByteIdentityAgainstGeneration17']
    print('byte-identity vs generation 17: compared=%d changed=%s added=%s removed=%s -> %s'
          % (n['filesCompared'], n['changed'], n['added'], n['removed'],
             n['allDisclosedNormativeFilesByteIdentical']))
    print('hashVerification:', k['hashVerification'])
    assert k['hashVerification'] == 'PASS'
    assert n['allDisclosedNormativeFilesByteIdentical']
    assert n['filesCompared'] == 101, n['filesCompared']


main()

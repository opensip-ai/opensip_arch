"""v17 input custody.

Three SEPARATE claims, none of which implies another:

  (1) the held manifest's own SHA-256 equals the value the instruction names;
  (2) the parent digest DECLARED INSIDE that manifest equals the parent value the instruction
      names -- a declared-binding comparison, NOT verification of a parent this origin does
      not hold;
  (3) every one of the 101 disclosed normative files re-hashes to its manifest row AND is
      BYTE-IDENTICAL to the same path in the v16 kit, measured from the per-file digests this
      origin itself recorded in v16 (notes/v16-input-custody.json). Equality of the normative
      bytes is therefore MEASURED here, not accepted because the instruction says so.

What changed between the two generations is then reported as exactly that: the manifest's own
digest and its parent custody row, with the normative payload unchanged.
"""
import hashlib
import json
import os
import sys

ROOT = '/tmp/opensip-design-corrections/consumer-b.v17'
SUB = ROOT + '/subject'
OUT = ROOT + '/output'
EXPECT_MANIFEST = '4cee77543946d66f2282dcbc7a8621e0b4117d78d37b44cf57a5f0ad3ca5e237'
EXPECT_PARENT = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
V16_MANIFEST = '6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6'
V16_PARENT = '1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b'
SESSION = '79569ae1-10f4-4181-972b-334f7ed2f07a'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    mb = open(SUB + '/consumer-input-manifest.json', 'rb').read()
    man_sha = hashlib.sha256(mb).hexdigest()
    man = json.loads(mb.decode())

    rows, bad = [], []
    on_disk = set()
    for d, _dirs, files in os.walk(SUB):
        for f in files:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, SUB)
            if rel != 'consumer-input-manifest.json':
                on_disk.add(rel)
    listed = set()
    for f in man['files']:
        listed.add(f['path'])
        p = SUB + '/' + f['path']
        if not os.path.exists(p):
            rows.append({'path': f['path'], 'result': 'MISSING'})
            bad.append(f['path'])
            continue
        h = sha(p)
        n = os.path.getsize(p)
        ok = h == f['sha256'] and (f.get('bytes') in (None, n))
        rows.append({'path': f['path'], 'result': 'PASS' if ok else 'FAIL',
                     'sha256': h, 'bytes': n,
                     'manifestSha256': f['sha256'], 'manifestBytes': f.get('bytes')})
        if not ok:
            bad.append(f['path'])

    # (3) byte-identity against THIS ORIGIN'S OWN v16 per-file record
    prior = None
    for cand in ('notes/v16-input-custody.json', 'notes/v15-input-custody.json'):
        try:
            prior = json.load(open(OUT + '/' + cand))
            prior_name = cand
            break
        except Exception:
            continue
    prior_map = {}
    if prior:
        for r in prior['inputKit']['perFile']:
            # the v16 record names the MEASURED digest `measuredSha256`; reading the wrong
            # key would have silently compared nothing, so the key is taken explicitly and
            # the comparison count is reported for exactly that reason
            h = r.get('measuredSha256') or r.get('sha256')
            if h:
                prior_map[r['path']] = h
    now_map = {r['path']: r.get('sha256') for r in rows}
    changed = sorted(p for p, h in now_map.items()
                     if p in prior_map and prior_map[p] != h)
    added = sorted(p for p in now_map if p not in prior_map)
    removed = sorted(p for p in prior_map if p not in now_map)
    compared = sorted(p for p in now_map if p in prior_map)

    doc = {
        'consumerId': 'consumer-b.v17',
        'sessionId': SESSION,
        'sameOriginAncestry': ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16',
                               'consumer-b.v17'],
        'ancestryStanding': (
            'one continuous fresh blind consumer origin. The v16 CHANGES_REQUIRED review and '
            'every earlier generation are preserved unmodified; continuation does not '
            'retroactively grant acceptance to any of them.'),
        'standing': __doc__,
        'inputKit': {
            'manifestPath': 'subject/consumer-input-manifest.json',
            'manifestSha256Measured': man_sha,
            'manifestSha256Expected': EXPECT_MANIFEST,
            'manifestSha256Match': man_sha == EXPECT_MANIFEST,
            'parentSubjectSha256DeclaredInManifest': man.get('parentSubjectSha256'),
            'parentSubjectSha256Expected': EXPECT_PARENT,
            'parentSubjectSha256Match': man.get('parentSubjectSha256') == EXPECT_PARENT,
            'parentVerificationStanding': (
                'DECLARED BINDING ONLY. This origin does not hold the parent candidate, so it '
                'claims no verification of it: the only measurement is that the digest '
                'declared inside the held manifest equals the value the instruction names.'),
            'fileCount': len(man['files']),
            'filesVerifiedPass': sum(1 for r in rows if r['result'] == 'PASS'),
            'filesFailed': bad,
            'extraFilesOnDiskNotInManifest': sorted(on_disk - listed),
            'manifestFilesAbsentFromDisk': sorted(listed - on_disk),
            'hashVerification': 'PASS' if (not bad and man_sha == EXPECT_MANIFEST
                                           and man.get('parentSubjectSha256')
                                           == EXPECT_PARENT
                                           and not (on_disk ^ listed)) else 'FAIL',
            'perFile': rows,
        },
        'normativeByteIdentityAgainstV16': {
            'measuredFrom': prior_name if prior else None,
            'filesCompared': len(compared),
            'changed': changed,
            'added': added,
            'removed': removed,
            'allDisclosedNormativeFilesByteIdentical': not (changed or added or removed),
            'claim': ('MEASURED, not accepted on assertion: each of the 101 disclosed files '
                      're-hashes to the same SHA-256 this origin recorded for that path in '
                      'v16.'),
        },
        'whatActuallyChangedBetweenV16AndV17': {
            'manifestOwnDigest': {'v16': V16_MANIFEST, 'v17': man_sha,
                                  'differs': man_sha != V16_MANIFEST},
            'declaredParentDigest': {'v16': V16_PARENT,
                                     'v17': man.get('parentSubjectSha256'),
                                     'differs': man.get('parentSubjectSha256')
                                     != V16_PARENT},
            'normativePayload': 'unchanged (measured above)',
            'consequence': (
                'the kit ancestry/custody row changed while every normative clause this '
                'origin reconstructs stayed byte-identical. So no Run needs reminting for a '
                'changed normative digest this generation -- and any remint that does happen '
                'must be caused by a correction this origin makes, not by the kit.'),
        },
        'notAnOracle': (
            'no author model, checker, export, root output, expected answer, expected digest, '
            'other origin review or candidate snapshot was read. The source31 reference code '
            'named in the instruction is NOT an input and was not accessed.'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v17-input-custody.json', 'w') as f:
        json.dump(doc, f, indent=1)
    k = doc['inputKit']
    print('manifest  measured=%s match=%s' % (k['manifestSha256Measured'][:16],
                                              k['manifestSha256Match']))
    print('parent    declared=%s match=%s (declared-binding only)'
          % ((k['parentSubjectSha256DeclaredInManifest'] or '')[:16],
             k['parentSubjectSha256Match']))
    print('files     %d/%d PASS  extra=%s missing=%s'
          % (k['filesVerifiedPass'], k['fileCount'],
             k['extraFilesOnDiskNotInManifest'], k['manifestFilesAbsentFromDisk']))
    n = doc['normativeByteIdentityAgainstV16']
    print('byte-identity vs v16: compared=%d changed=%s added=%s removed=%s -> %s'
          % (n['filesCompared'], n['changed'], n['added'], n['removed'],
             n['allDisclosedNormativeFilesByteIdentical']))
    print('hashVerification:', k['hashVerification'])
    assert k['hashVerification'] == 'PASS', 'input custody FAILED'
    assert n['allDisclosedNormativeFilesByteIdentical'], 'normative bytes are NOT identical'


main()

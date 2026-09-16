"""v16 input custody: verify the declared manifest and every kit file, and DIFF against the
prior disclosed kit to locate changed normative owners. The prior manifest is read ONLY for
the change diff; no prior byte is used as a current recipe."""
import hashlib
import json
import os

V16 = '/tmp/opensip-design-corrections/consumer-b.v16'
PRIOR = '/tmp/opensip-design-corrections/consumer-b' + '.v15'
SUB = V16 + '/subject'
EXPECT_MANIFEST = '6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6'
EXPECT_PARENT = '1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b'


def main():
    mb = open(SUB + '/consumer-input-manifest.json', 'rb').read()
    man_sha = hashlib.sha256(mb).hexdigest()
    man = json.loads(mb.decode())
    rows, bad = [], []
    for f in man['files']:
        p = SUB + '/' + f['path']
        if not os.path.exists(p):
            rows.append({'path': f['path'], 'result': 'MISSING'})
            bad.append(f['path'])
            continue
        b = open(p, 'rb').read()
        h = hashlib.sha256(b).hexdigest()
        ok = (h == f['sha256'] and len(b) == f['bytes'])
        rows.append({'path': f['path'], 'declaredSha256': f['sha256'], 'measuredSha256': h,
                     'declaredBytes': f['bytes'], 'measuredBytes': len(b),
                     'result': 'PASS' if ok else 'FAIL'})
        if not ok:
            bad.append(f['path'])
    on_disk = set()
    for dp, dn, fn in os.walk(SUB + '/docs'):
        for n in fn:
            on_disk.add(os.path.relpath(os.path.join(dp, n), SUB))
    listed = {f['path'] for f in man['files']}
    old = json.load(open(PRIOR + '/subject/consumer-input-manifest.json'))
    om = {f['path']: f['sha256'] for f in old['files']}
    nm = {f['path']: f['sha256'] for f in man['files']}
    changed = sorted(p for p in (set(om) & set(nm)) if om[p] != nm[p])
    res = {
        'consumerId': 'consumer-b.v16',
        'sameOriginAncestry': ['consumer-b.v14', 'consumer-b.v15', 'consumer-b.v16'],
        'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
        'inputKit': {
            'manifestSha256Measured': man_sha,
            'manifestSha256Expected': EXPECT_MANIFEST,
            'manifestSha256Match': man_sha == EXPECT_MANIFEST,
            'parentCandidateSha256Declared': man['parentSubjectSha256'],
            'parentCandidateSha256Expected': EXPECT_PARENT,
            'parentCandidateSha256Match': man['parentSubjectSha256'] == EXPECT_PARENT,
            'fileCount': len(man['files']),
            'filesVerifiedPass': sum(1 for r in rows if r['result'] == 'PASS'),
            'filesFailed': bad,
            'extraFilesOnDiskNotInManifest': sorted(on_disk - listed),
            'manifestFilesAbsentFromDisk': sorted(listed - on_disk),
            'hashVerification': 'PASS' if (not bad and man_sha == EXPECT_MANIFEST
                                           and man['parentSubjectSha256'] == EXPECT_PARENT
                                           and not (on_disk ^ listed)) else 'FAIL',
            'standing': ('Verifies only the DISCLOSED kit subset. This is explicitly NOT a '
                         'claim of parent whole-candidate verification: only the parent '
                         'digest DECLARED in this manifest was compared to the value the '
                         'instruction names.'),
            'perFile': rows},
        'kitDiffAgainstPriorDisclosedKit': {
            'changedCount': len(changed), 'changed': changed,
            'added': sorted(set(nm) - set(om)), 'removed': sorted(set(om) - set(nm))},
    }
    os.makedirs(V16 + '/output/notes', exist_ok=True)
    with open(V16 + '/output/notes/v16-input-custody.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('manifest match:', res['inputKit']['manifestSha256Match'],
          '| parent match:', res['inputKit']['parentCandidateSha256Match'],
          '| files:', res['inputKit']['filesVerifiedPass'], '/', res['inputKit']['fileCount'],
          '|', res['inputKit']['hashVerification'])
    print('CHANGED (%d):' % len(changed))
    for p in changed:
        print('   ', p)
    print('ADDED:', res['kitDiffAgainstPriorDisclosedKit']['added'])
    print('REMOVED:', res['kitDiffAgainstPriorDisclosedKit']['removed'])
    assert res['inputKit']['hashVerification'] == 'PASS'


main()

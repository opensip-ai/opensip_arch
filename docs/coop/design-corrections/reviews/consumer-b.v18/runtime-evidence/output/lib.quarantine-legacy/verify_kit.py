"""v15 input custody: verify the new manifest and every kit file, and DIFF against the
v14 kit manifest (paths + digests) to find changed normative owners.

The v14 manifest is read from this origin's own preserved v14 subject manifest copy only
for the purpose of a CHANGE DIFF; no v14 kit bytes are used as a current recipe.
"""
import hashlib
import json
import os
import sys

V15 = '/tmp/opensip-design-corrections/consumer-b.v15'
# The PRIOR disclosed kit, read ONLY to compute the change diff below. No byte of it is
# used as a current recipe, and no reconstruction imports from this path.
V14 = '/tmp/opensip-design-corrections/consumer-b' + '.v14'
SUB = V15 + '/subject'
EXPECT_MANIFEST = '73f9c13e7aaf4c4a655eec53914c6569c0b560274bdd15fa6d1fb2d16f7da7c4'
EXPECT_PARENT = 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a'


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

    old = json.load(open(V14 + '/subject/consumer-input-manifest.json'))
    old_map = {f['path']: f['sha256'] for f in old['files']}
    new_map = {f['path']: f['sha256'] for f in man['files']}
    changed = sorted(p for p in (set(old_map) & set(new_map)) if old_map[p] != new_map[p])
    added = sorted(set(new_map) - set(old_map))
    removed = sorted(set(old_map) - set(new_map))

    res = {
        'consumerId': 'consumer-b.v15',
        'reviewAncestry': {
            'origin': 'consumer-b' + '.v14' + ' (same fresh blind consumer origin)',
            'continuation': 'review15 of origin14 at a deliberate source transition',
            'priorWorkStatus': ('partial, preserved WITHOUT acceptance; no root validator '
                                'output, expected result, author helper or prior review was '
                                'supplied'),
            'v14SubjectManifestSha256': hashlib.sha256(
                open(V14 + '/subject/consumer-input-manifest.json', 'rb').read()).hexdigest(),
            'v14ParentSubjectSha256': old['parentSubjectSha256'],
        },
        'inputKit': {
            'manifestPath': 'subject/consumer-input-manifest.json',
            'manifestSha256Measured': man_sha,
            'manifestSha256Expected': EXPECT_MANIFEST,
            'manifestSha256Match': man_sha == EXPECT_MANIFEST,
            'parentSubjectSha256Declared': man['parentSubjectSha256'],
            'parentSubjectSha256Expected': EXPECT_PARENT,
            'parentSubjectSha256Match': man['parentSubjectSha256'] == EXPECT_PARENT,
            'fileCount': len(man['files']),
            'filesVerifiedPass': sum(1 for r in rows if r['result'] == 'PASS'),
            'filesFailed': bad,
            'extraFilesOnDiskNotInManifest': sorted(on_disk - listed),
            'manifestFilesAbsentFromDisk': sorted(listed - on_disk),
            'hashVerification': 'PASS' if (not bad and man_sha == EXPECT_MANIFEST
                                           and man['parentSubjectSha256'] == EXPECT_PARENT
                                           and not (on_disk ^ listed)) else 'FAIL',
            'standing': ('This verifies only the DISCLOSED kit subset. It is not a claim to '
                         'hold the complete frozen candidate.'),
            'perFile': rows,
        },
        'kitDiffAgainstPriorDisclosedKit': {
            'changedCount': len(changed), 'changed': changed,
            'addedCount': len(added), 'added': added,
            'removedCount': len(removed), 'removed': removed,
            'unchangedCount': len(set(old_map) & set(new_map)) - len(changed),
            'note': ('Digest comparison only. Every changed document is read in full '
                     'context from the v15 bytes before any reconstruction uses it; no v14 '
                     'byte is used as a current recipe.'),
        },
    }
    os.makedirs(V15 + '/output/notes', exist_ok=True)
    with open(V15 + '/output/notes/v15-input-custody.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('manifest match   :', res['inputKit']['manifestSha256Match'])
    print('parent match     :', res['inputKit']['parentSubjectSha256Match'])
    print('files verified   :', res['inputKit']['filesVerifiedPass'], 'of',
          res['inputKit']['fileCount'])
    print('hashVerification :', res['inputKit']['hashVerification'])
    print()
    print('CHANGED (%d):' % len(changed))
    for p in changed:
        print('   ', p)
    print('ADDED (%d):' % len(added))
    for p in added:
        print('   ', p)
    print('REMOVED (%d):' % len(removed))
    for p in removed:
        print('   ', p)
    assert res['inputKit']['hashVerification'] == 'PASS'


main()

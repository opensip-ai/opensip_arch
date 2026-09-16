"""Rebind this origin's helper code from the v16 declared input to the v17 declared input.

PATH rebinding ONLY. The semantic fixture metadata is already pinned to explicit,
location-free constants in opensip_fixture.py (the v16 correction V16-D2), so nothing
content-bearing is touched here and the selected graph identities must NOT move because of
this rebind. That is asserted, not hoped for: after the rewrite the identity-bearing document
digests are printed, and relocation_control.py re-measures both halves (no retained byte
contains a runtime-location string; a rebuild under a different output root reproduces the
selected graph identity).

The entire pre-rebind tree is copied to output/lib.before-image.v16/ first.
"""
import os
import shutil
import sys

V17 = '/tmp/opensip-design-corrections/consumer-b.v17'
LIB = V17 + '/output/lib'
BEFORE = V17 + '/output/lib.before-image.v16'
OLD = 'consumer-b' + '.v16'
NEW = 'consumer-b.v17'
# self-exclusions: a rebind must not rewrite its own pinned constants, and the custody
# verifiers must keep naming the generation they actually verified (the v16 defect V15-D1).
SELF_EXCLUDE = {'rebind_v17.py', 'rebind_v16.py', 'rebind_v15.py',
                'diff_json.py', 'diff_text.py',
                'verify_kit.py', 'verify_kit_v16.py', 'verify_kit_v17.py',
                'check_siblings_untouched.py', 'helper_corrections.py'}


def main():
    if not os.path.isdir(BEFORE):
        shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
        print('before-image written:', BEFORE)
    else:
        print('before-image already present:', BEFORE)
    changed = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py') or name in SELF_EXCLUDE:
            continue
        p = os.path.join(LIB, name)
        s = open(p, 'r', encoding='utf-8').read()
        if OLD not in s:
            continue
        open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
        changed.append(name)
    print('path-rebound (%d):' % len(changed), changed)
    residue = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py') or name in SELF_EXCLUDE:
            continue
        if OLD in open(os.path.join(LIB, name), encoding='utf-8').read():
            residue.append(name)
    print('residual v16 references (must be empty):', residue)
    assert not residue
    sys.path.insert(0, LIB)
    import opensip_schema as S
    assert S.KIT == V17 + '/subject', S.KIT
    print('opensip_schema.KIT =', S.KIT)
    import opensip_build as B
    print('identity doc sha =', B.doc_sha(B.IDENTITY_DOC))
    print('native   doc sha =', B.doc_sha(B.NATIVE_DOC))
    import opensip_fixture as FX
    print('fixture namespace (location-free) =', FX.FIXTURE_NAMESPACE)
    assert 'v16' not in FX.FIXTURE_NAMESPACE and 'v17' not in FX.FIXTURE_NAMESPACE, \
        'a generation label leaked into a semantic fixture constant'


main()

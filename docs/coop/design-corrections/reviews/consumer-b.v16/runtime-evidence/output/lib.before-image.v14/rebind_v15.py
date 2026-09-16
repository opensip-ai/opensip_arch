"""Rebind this origin's helper code from the v14 declared input to the v15 declared input.

Discipline:
  * the ENTIRE pre-rebind lib/ tree is copied to output/lib.before-image.v14/ first, so the
    before-image is preserved exactly as the continuation instruction requires;
  * every occurrence of the v14 session root is rewritten to v15, including CONTENT-BEARING
    labels (capability-manifest `profile` strings, component-manifest descriptions), because
    a new build must be bound to the current kit and must not silently reproduce a v14
    identity;
  * after the rewrite, a guard asserts that NO v14 path string remains anywhere in lib/, so
    no old runtime path can survive as a hidden dependency.

Run once. Idempotent.
"""
import os
import shutil
import sys

V15 = '/tmp/opensip-design-corrections/consumer-b.v15'
LIB = V15 + '/output/lib'
BEFORE = V15 + '/output/lib.before-image.v14'
OLD = 'consumer-b.v14'
NEW = 'consumer-b.v15'


def main():
    if not os.path.isdir(BEFORE):
        shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
        print('before-image written:', BEFORE)
    else:
        print('before-image already present:', BEFORE)
    changed = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py'):
            continue
        p = os.path.join(LIB, name)
        s = open(p, 'r', encoding='utf-8').read()
        if OLD not in s:
            continue
        # diff_json.py deliberately reads the prior kit for the CHANGE DIFF only
        if name == 'diff_json.py':
            continue
        n = s.replace(OLD, NEW)
        open(p, 'w', encoding='utf-8').write(n)
        changed.append(name)
    print('rewritten (%d):' % len(changed), changed)
    # guard
    residue = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py') or name in ('rebind_v15.py', 'diff_json.py'):
            continue
        s = open(os.path.join(LIB, name), 'r', encoding='utf-8').read()
        if OLD in s:
            residue.append(name)
    print('residual v14 references (must be empty):', residue)
    assert not residue
    # verify the kit binding actually resolves to the v15 subject
    sys.path.insert(0, LIB)
    import opensip_schema as S
    assert S.KIT == V15 + '/subject', S.KIT
    assert os.path.isdir(S.KIT)
    print('opensip_schema.KIT =', S.KIT)
    import opensip_build as B
    print('identity doc sha (v15) =', B.doc_sha(B.IDENTITY_DOC))


main()

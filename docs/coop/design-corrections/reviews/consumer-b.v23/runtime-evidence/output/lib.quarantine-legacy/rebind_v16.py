"""Rebind this origin's helper code from the v15 declared input to the v16 declared input,
and REMOVE the runtime location from every semantic fixture label.

Two separate jobs, deliberately kept apart:

 1. PATH rebinding -- the KIT/OUT roots and artefact paths must name the v16 declared inputs.
    This is pure runtime plumbing and must not change any identity.

 2. SEMANTIC FIXTURE METADATA -- at v15 this origin rewrote content-bearing labels
    (capability-manifest `profile`, component-manifest `name`/description) from ".v14" to
    ".v15" during the path rebind. That was wrong in principle: it let the RUNTIME LOCATION
    leak into a semantic field and therefore into `capabilityManifestId`, `plan2` and `run3`.
    The v16 instruction states the rule directly -- "Runtime location itself must not become
    evidence of a semantic change: semantic fixture metadata must be chosen explicitly, and
    relocation with the same declared inputs should reproduce selected graph identities."
    Semantic fixture labels are therefore pinned to EXPLICIT, location-free constants in
    opensip_fixture.py and are never derived from the session directory again.

The entire pre-rebind tree is copied to output/lib.before-image.v15/ first.
"""
import os
import shutil
import sys

V16 = '/tmp/opensip-design-corrections/consumer-b.v16'
LIB = V16 + '/output/lib'
BEFORE = V16 + '/output/lib.before-image.v15'
OLD = 'consumer-b' + '.v15'
NEW = 'consumer-b.v16'
SELF_EXCLUDE = {'rebind_v16.py', 'rebind_v15.py', 'diff_json.py', 'diff_text.py',
                'verify_kit.py', 'verify_kit_v16.py'}


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
    print('residual v15 references (must be empty):', residue)
    assert not residue
    sys.path.insert(0, LIB)
    import opensip_schema as S
    assert S.KIT == V16 + '/subject', S.KIT
    print('opensip_schema.KIT =', S.KIT)
    import opensip_build as B
    print('identity doc sha (v16) =', B.doc_sha(B.IDENTITY_DOC))
    print('native  doc sha (v16) =', B.doc_sha(B.NATIVE_DOC))


main()

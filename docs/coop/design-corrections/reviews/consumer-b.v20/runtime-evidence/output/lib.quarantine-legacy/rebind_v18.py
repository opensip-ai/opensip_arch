"""Rebind the ACTIVE helper code to generation 18, and QUARANTINE the legacy tools that
cannot lawfully run here.

Written fresh for this generation. The copied rebind scripts are NOT executed: each hardcodes a
previous generation as its own LIB/BEFORE root, so executing one would write a before-image
into a read-only earlier generation (the V17-D8 defect class). This file instead:

  1. copies the active lib to output/lib.before-image.v17/ INSIDE this runtime, so the
     pre-rebind bytes of this generation's starting point are preserved here;
  2. rewrites `consumer-b.v17` -> `consumer-b.v18` in every ACTIVE module, including every
     writer -- an output root is never exempted from the rebind, which is exactly what went
     wrong in v17;
  3. QUARANTINES the legacy tools whose whole purpose is a generation that is NOT supplied in
     this runtime (the v15/v16/v17 rebinds, the v15/v16 kit verifiers, and the two kit-diff
     tools). Quarantine is structural: they are moved out of the import path so no stage can
     execute them, rather than being silently rewritten into something they were never;
  4. asserts that NO active module still names a foreign generation in a path, and that every
     output/kit root resolves beneath this runtime;
  5. leaves output/lib.before-image.v14 / .v15 / .v16 byte-identical -- they are historical
     evidence, not code.

Semantic fixture metadata is already pinned to explicit location-free constants
(opensip_fixture.py, the v16 correction V16-D2), so nothing content-bearing is touched and the
selected graph identities must not move because of this rebind. relocation_control.py
re-measures both halves afterwards.
"""
import os
import shutil
import sys

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v18'
LIB = RUNTIME + '/output/lib'
BEFORE = RUNTIME + '/output/lib.before-image.v17'
QUAR = RUNTIME + '/output/lib.quarantine-legacy'
OLD = 'consumer-b' + '.v17'
NEW = 'consumer-b.v18'

# tools whose target generation is NOT supplied in this runtime; they can never run correctly
# here and two of them could write into a read-only generation if executed.
QUARANTINE = {
    'rebind_v15.py': 'rebinds v14->v15; writes a before-image into generation 15',
    'rebind_v16.py': 'rebinds v15->v16; writes a before-image into generation 16',
    'rebind_v17.py': 'rebinds v16->v17; writes a before-image into generation 17',
    'verify_kit.py': 'verifies the v15 kit against the v14 kit; neither is supplied here',
    'verify_kit_v16.py': 'verifies the v16 kit; not supplied here',
    'diff_json.py': 'diffs the v14 and v15 kits; neither is supplied here',
    'diff_text.py': 'diffs the v14 and v15 kits; neither is supplied here',
    'progress_v16.py': ('writes progress.v16.json, a HISTORICAL artifact of generation 16; '
                        'running it here would overwrite that history with v18-era content, '
                        'and the rebind had already mangled its ancestry list'),
    'check_siblings_untouched.py': (
        'walks sibling generation trees to compare mtimes. Those trees are NOT supplied in '
        'this runtime and reading them is out of bounds here, so the control cannot run. It '
        'also returned PASS while accepting two known overwrites, which is exactly the '
        'behaviour the instruction forbids. Replaced by history_standing_v18.py.'),
    'audit_v16_writes.py': (
        'walks sibling generation trees for a write census; same out-of-bounds problem, and '
        'its boundary constant is specific to the previous runtime. Its measured finding is '
        'carried forward as a DISCLOSED, UNRESOLVED item by history_standing_v18.py.'),
    'verify_kit_v17.py': ('the previous generation\'s custody verifier: its ROOT and its '
                          'notes/*-input-custody.json write destination are both in that '
                          'generation, which is read-only and not supplied here. Replaced by '
                          'verify_kit_v18.py. Keeping it exempt from the rebind so it stays '
                          'truthful about what it verified is NOT sufficient -- an exempt '
                          'WRITER is still a writer, so it is quarantined.'),
}
# Exemptions from the path rewrite. Two distinct reasons, both learned the hard way:
#
#  (a) the rebind must not rewrite ITS OWN constants, and the previous generation's custody
#      verifier must keep naming the generation it actually verified;
#  (b) GENERATION-LABELLED CONTENT modules. A path rebind is a mechanical text substitution,
#      so it cannot tell a path from a sentence. V17-D1 and V18-D1 are both this defect: the
#      rewrite turned true historical statements false and deleted an ancestry row by renaming
#      it. These modules carry generation labels as DATA (ancestry tables, helper-correction
#      narratives, historical progress records); their own path roots are already bound to this
#      generation and are asserted below, so excluding them is safe and stops the corruption at
#      its source instead of repairing it afterwards.
SELF_EXCLUDE = {'rebind_v18.py', 'census_v18.py', 'verify_kit_v18.py',
                'phase0.py', 'helper_corrections.py', 'progress_v17.py'}
# every excluded module must STILL have its own output/kit roots inside this generation
ROOT_MUST_BE_V18 = ('phase0.py', 'helper_corrections.py', 'progress_v17.py')


def main():
    if not os.path.isdir(BEFORE):
        shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
        print('before-image written (inside this runtime):', BEFORE)
    else:
        print('before-image already present:', BEFORE)

    os.makedirs(QUAR, exist_ok=True)
    moved = []
    for name, why in sorted(QUARANTINE.items()):
        src = os.path.join(LIB, name)
        if os.path.exists(src):
            shutil.move(src, os.path.join(QUAR, name))
            moved.append({'module': name, 'reason': why})
    with open(QUAR + '/WHY-QUARANTINED.txt', 'w') as f:
        f.write('Quarantined by rebind_v18.py. Each tool targets a generation that is NOT '
                'supplied in this runtime, and the three rebind scripts would write into a '
                'read-only earlier generation if executed. They are kept for provenance and '
                'are outside the import path.\n\n')
        for m in moved:
            f.write('%-22s %s\n' % (m['module'], m['reason']))
    print('quarantined (%d):' % len(moved), [m['module'] for m in moved])

    changed = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py') or name in SELF_EXCLUDE:
            continue
        p = os.path.join(LIB, name)
        s = open(p, encoding='utf-8').read()
        if OLD not in s:
            continue
        open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
        changed.append(name)
    print('path-rebound (%d modules)' % len(changed))

    # ---- assertions
    residue = []
    for name in sorted(os.listdir(LIB)):
        if not name.endswith('.py') or name in SELF_EXCLUDE:
            continue
        text = open(os.path.join(LIB, name), encoding='utf-8').read()
        for gen in ('v13', 'v14', 'v15', 'v16', 'v17'):
            tok = 'consumer-b.' + gen
            if tok in text:
                for i, line in enumerate(text.splitlines(), 1):
                    if tok in line:
                        residue.append({'module': name, 'line': i, 'generation': gen,
                                        'text': line.strip()[:120]})
    print('residual foreign-generation references in active code:', len(residue))
    for r in residue:
        print('   %-26s:%-4d %-4s %s' % (r['module'], r['line'], r['generation'],
                                         r['text'][:80]))
    sys.path.insert(0, LIB)
    import opensip_schema as S
    assert S.KIT == RUNTIME + '/subject', S.KIT
    print('opensip_schema.KIT =', S.KIT)
    import opensip_build as B
    print('identity doc sha =', B.doc_sha(B.IDENTITY_DOC))
    print('native   doc sha =', B.doc_sha(B.NATIVE_DOC))
    import opensip_fixture as FX
    assert not any(g in FX.FIXTURE_NAMESPACE for g in ('v14', 'v15', 'v16', 'v17', 'v18')), \
        'a generation label leaked into a semantic fixture constant'
    print('fixture namespace (location-free) =', FX.FIXTURE_NAMESPACE)
    # every residual reference must be PROSE, never a path literal
    bad = [r for r in residue if '/tmp/opensip-design-corrections' in r['text']]
    assert not bad, bad
    print('OK: no active module names a foreign generation PATH')
    # the content-labelled exclusions must still write only beneath THIS generation
    import re
    for name in ROOT_MUST_BE_V18:
        p = os.path.join(LIB, name)
        if not os.path.exists(p):
            continue
        for i, line in enumerate(open(p, encoding='utf-8').read().splitlines(), 1):
            if re.match(r'^\s*(OUT|ROOT|SUB|KIT|REC)\s*=', line):
                assert NEW in line or 'ROOT +' in line or 'os.path' in line, \
                    ('excluded module assigns a root outside this generation',
                     name, i, line.strip())
                print('   root OK  %-24s:%-4d %s' % (name, i, line.strip()[:70]))


main()

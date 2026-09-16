"""History standing and write confinement for generation 18.

This replaces the previous generation's sibling-mtime control, which cannot run here (the
sibling trees are not supplied in this runtime and reading them is out of bounds) and which
returned PASS while ACCEPTING two known overwrites. A control that reports PASS on a known
damaged history is not a control.

What this file measures, and what it refuses to claim:

  MEASURED A  write confinement: every write destination of every ACTIVE module of this
              generation resolves beneath this runtime (from notes/v18-path-census.json), and
              a live probe confirms the output root this process can reach.
  MEASURED B  this generation's own artifact tree: the archived before-images and the
              quarantined legacy tools are present and off the import path.
  CARRIED     the generation-17 disclosure: TWO files under the generation-16 output were
              overwritten by that session (helper-corrections.json and
              notes/siblings-untouched.json), their prior bytes were not retained, and this
              origin cannot restore them.
  NOT CLAIMED any restoration. A root custody restoration may be recorded separately later;
              its outcome is NOT fabricated here, and nothing in this file asserts that the
              earlier generations are now intact.

The returned state is therefore deliberately NOT a bare PASS. It is:
  CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
which is PASS for this generation's confinement and simultaneously an open, unrepaired item
about an earlier generation's history.
"""
import json
import os
import sys

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v18'
OUT = RUNTIME + '/output'

CARRIED_DISCLOSURE = {
    'source': 'generation 17 review and helper-corrections row V17-D8',
    'whatHappened': (
        'two modules were wrongly exempted from that generation\'s path rebind, so their '
        'output root still named the previous generation and they wrote into it'),
    'filesOverwritten': [
        'consumer-b.v16/output/helper-corrections.json',
        'consumer-b.v16/output/notes/siblings-untouched.json',
    ],
    'filesNotTouched': (
        'no Run export, review file, requirement status, checkpoint or vector of any earlier '
        'generation; generations 14 and 15 had zero writes'),
    'priorBytes': 'NOT retained by this origin and NOT restorable by it',
    'status': 'OPEN -- unrepaired, and not repairable from inside this runtime',
    'rootCustodyRestoration': (
        'may be recorded separately by root later. This origin does not know and does not '
        'assert its outcome.'),
    'thisGenerationsPrevention': (
        'the rebind now treats an EXEMPT WRITER as a contradiction: every module that writes '
        'is rebound, and the three rebind scripts, both sibling-walking controls, the previous '
        'custody verifier and the historical progress writer are quarantined off the import '
        'path. The path census asserts zero foreign write destinations in active code.'),
}


def main():
    census = json.load(open(OUT + '/notes/v18-path-census.json'))
    foreign = census['foreignGenerationWriteOrRootAssignments']

    # MEASURED A: confinement, from the census plus a live probe
    probe = os.path.join(OUT, 'notes', '.write-probe')
    with open(probe, 'w') as f:
        f.write('confinement probe\n')
    reachable = os.path.realpath(probe).startswith(os.path.realpath(RUNTIME) + os.sep)
    os.remove(probe)

    # MEASURED B: this generation's own tree shape
    groups = {
        'archivedBeforeImages': sorted(
            d for d in os.listdir(OUT) if d.startswith('lib.before-image.')),
        'quarantineDirPresent': os.path.isdir(OUT + '/lib.quarantine-legacy'),
        'quarantinedModules': sorted(
            f for f in os.listdir(OUT + '/lib.quarantine-legacy')
            if f.endswith('.py')) if os.path.isdir(OUT + '/lib.quarantine-legacy') else [],
    }
    # nothing on the import path may import from a quarantined or archived tree
    bad_imports = []
    lib = OUT + '/lib'
    for n in sorted(os.listdir(lib)):
        if not n.endswith('.py'):
            continue
        t = open(os.path.join(lib, n), encoding='utf-8').read()
        for needle in ('lib.before-image', 'lib.quarantine-legacy'):
            if needle not in t:
                continue
            for i, line in enumerate(t.splitlines(), 1):
                if needle not in line:
                    continue
                stripped = line.strip()
                # a PROSE mention (a comment, a docstring line or a quoted standing sentence)
                # is not an import. The test is the statement form, not the substring: an
                # `import`/`sys.path` STATEMENT that names one of those trees is the defect.
                is_stmt = (stripped.startswith('import ')
                           or stripped.startswith('from ')
                           or ('sys.path' in stripped and '=' not in stripped.split(
                               'sys.path')[0] and 'insert' in stripped)
                           or '__import__' in stripped)
                if is_stmt:
                    bad_imports.append({'module': n, 'line': i,
                                        'text': stripped[:120]})

    confined = (not foreign) and reachable and not bad_imports
    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v18',
        'measuredA_writeConfinement': {
            'foreignWriteOrRootAssignmentsInActiveCode': len(foreign),
            'liveProbeResolvedBeneathThisRuntime': reachable,
            'noActiveModuleImportsAnArchivedOrQuarantinedTree': not bad_imports,
            'badImports': bad_imports,
            'result': 'CONFINED' if confined else 'NOT CONFINED',
        },
        'measuredB_treeShape': groups,
        'carriedDisclosure_generation16NoteOverwrites': CARRIED_DISCLOSURE,
        'priorGenerationsMeasurableHere': False,
        'whyNotMeasurable': (
            'the earlier generation trees are not supplied in this runtime and reading them is '
            'out of bounds, so this generation CANNOT re-measure their integrity. Reporting a '
            'PASS about them would be a claim without evidence.'),
        'state': ('CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE' if confined
                  else 'NOT-CONFINED'),
        'isThisAPass': (
            'PASS for this generation\'s write confinement. NOT a pass for history: the two '
            'generation-16 note overwrites remain OPEN and unrepaired, and this control is '
            'written so that it can never report a clean history by accepting them.'),
    }
    with open(OUT + '/notes/v18-history-standing.json', 'w') as f:
        json.dump(doc, f, indent=1)
    a = doc['measuredA_writeConfinement']
    print('write confinement      :', a['result'],
          '(foreign write rows %d, probe beneath runtime %s, clean imports %s)'
          % (a['foreignWriteOrRootAssignmentsInActiveCode'],
             a['liveProbeResolvedBeneathThisRuntime'],
             a['noActiveModuleImportsAnArchivedOrQuarantinedTree']))
    print('archived before-images :', groups['archivedBeforeImages'])
    print('quarantined modules    :', groups['quarantinedModules'])
    print('carried disclosure     : %d generation-16 files overwritten, status %s'
          % (len(CARRIED_DISCLOSURE['filesOverwritten']), CARRIED_DISCLOSURE['status']))
    print('state                  :', doc['state'])
    assert confined, doc['measuredA_writeConfinement']


main()

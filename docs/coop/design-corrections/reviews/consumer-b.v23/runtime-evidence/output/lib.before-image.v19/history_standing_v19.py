"""History standing and write confinement for generation 19.

What this measures, and what it refuses to claim:

  MEASURED A  write confinement: every write destination of every ACTIVE module resolves beneath
              this runtime (from notes/v19-path-census.json), plus a live probe.
  MEASURED B  this generation's tree shape: archived before-images present (now including
              lib.before-image.v18) and quarantined tools off the import path.
  MEASURED C  prior-generation mtimes. Unlike generation 18, the earlier trees ARE reachable from
              this runtime, so their newest modification time is measured as evidence that this
              session did not write into them. Only directory metadata is read: no file content of
              any earlier generation is opened, and nothing about their CONTENT is claimed.
  CARRIED     the generation-17 disclosure, unchanged: TWO files under the generation-16 output
              were overwritten by that session, their prior bytes were not retained, and this
              origin cannot restore them.
  CARRIED     the generation-19 label findings V19-D1 / V19-D2: successive mechanical rebinds had
              relabelled four historical helper-correction sentences and had DELETED generation 17
              from this origin's own ancestry list. Those are repaired here from the retained
              before-images, and the repair is recorded as a correction, not as a pristine history.
  NOT CLAIMED any restoration of the two generation-16 files. Root may record a custody
              restoration separately; its outcome is NOT fabricated here.

The returned state is deliberately not a bare PASS:
  CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
"""
import json
import os
import time

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v19'
OUT = RUNTIME + '/output'
SIBLINGS = ['/tmp/opensip-design-corrections/consumer-b' + '.v14',
            '/tmp/opensip-design-corrections/consumer-b' + '.v15',
            '/tmp/opensip-design-corrections/consumer-b' + '.v16',
            '/tmp/opensip-design-corrections/consumer-b' + '.v17',
            '/tmp/opensip-design-corrections/consumer-b' + '.v18']

CARRIED_DISCLOSURE = {
    'source': 'generation 17 review and helper-corrections row V17-D8',
    'whatHappened': (
        'two modules were wrongly exempted from that generation\'s path rebind, so their output '
        'root still named the previous generation and they wrote into it'),
    'filesOverwritten': [
        'consumer-b' + '.v16/output/helper-corrections.json',
        'consumer-b' + '.v16/output/notes/siblings-untouched.json',
    ],
    'filesNotTouched': (
        'no Run export, review file, requirement status, checkpoint or vector of any earlier '
        'generation; generations 14 and 15 had zero writes'),
    'priorBytes': 'NOT retained by this origin and NOT restorable by it',
    'status': 'OPEN -- unrepaired, and not repairable from inside this runtime',
    'rootCustodyRestoration': (
        'root supplies no restoration verdict to this continuation. This origin does not know '
        'and does not assert its outcome.'),
}

LABEL_FINDINGS = {
    'V19-D1': (
        'four historical helper-correction sentences in opensip_capmanifest.py and '
        'opensip_schema.py had been relabelled by every successive path rebind since generation '
        '15 (true generations v14, v15, v16, v15), and deliver.py\'s sameOriginAncestry list had '
        'LOST generation 17 entirely because the rebind rewrote that entry to v18. Evidence: the '
        'retained before-images. Repaired and written as split literals.'),
    'V19-D2': (
        'the generation-19 rebind rewrote ITS OWN docstring on the single run it was designed '
        'for -- the V15-D1 defect class inside the tool written to prevent it. Logic unaffected '
        '(its OLD/NEW constants are split literals); the sentence was repaired and the module '
        'self-excluded.'),
}


def newest_mtime(root):
    best = 0.0
    count = 0
    for d, dirs, names in os.walk(root):
        best = max(best, os.path.getmtime(d))
        count += len(names)
        for n in names:
            try:
                best = max(best, os.path.getmtime(os.path.join(d, n)))
            except OSError:
                pass
    return best, count


def main():
    census = json.load(open(OUT + '/notes/v19-path-census.json'))
    foreign = census['foreignGenerationWriteOrRootAssignments']

    probe = os.path.join(OUT, 'notes', '.write-probe')
    with open(probe, 'w') as f:
        f.write('confinement probe\n')
    reachable = os.path.realpath(probe).startswith(os.path.realpath(RUNTIME) + os.sep)
    os.remove(probe)

    groups = {
        'archivedBeforeImages': sorted(
            d for d in os.listdir(OUT) if d.startswith('lib.before-image.')),
        'quarantineDirPresent': os.path.isdir(OUT + '/lib.quarantine-legacy'),
        'quarantinedModules': sorted(
            f for f in os.listdir(OUT + '/lib.quarantine-legacy')
            if f.endswith('.py')) if os.path.isdir(OUT + '/lib.quarantine-legacy') else [],
    }
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
                s = line.strip()
                is_stmt = (s.startswith('import ') or s.startswith('from ')
                           or ('sys.path' in s and 'insert' in s) or '__import__' in s)
                if is_stmt:
                    bad_imports.append({'module': n, 'line': i, 'text': s[:120]})

    session_start = os.path.getmtime(OUT + '/notes/v19-path-census.json')
    sib = []
    for p in SIBLINGS:
        if not os.path.isdir(p):
            sib.append({'generation': os.path.basename(p), 'present': False})
            continue
        mt, files = newest_mtime(p)
        sib.append({'generation': os.path.basename(p), 'present': True, 'fileCount': files,
                    'newestMtimeUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mt)),
                    'newerThanThisSessionsFirstWrite': mt > session_start})
    touched = [s['generation'] for s in sib if s.get('newerThanThisSessionsFirstWrite')]

    confined = (not foreign) and reachable and not bad_imports and not touched
    doc = {
        'standing': __doc__,
        'generation': 'consumer-b.' + 'v19',
        'measuredA_writeConfinement': {
            'foreignWriteOrRootAssignmentsInActiveCode': len(foreign),
            'liveProbeResolvedBeneathThisRuntime': reachable,
            'noActiveModuleImportsAnArchivedOrQuarantinedTree': not bad_imports,
            'badImports': bad_imports,
            'result': 'CONFINED' if confined else 'NOT CONFINED',
        },
        'measuredB_treeShape': groups,
        'measuredC_priorGenerations': {
            'method': ('os.walk over directory metadata only, comparing each tree\'s newest '
                       'modification time with the first write this session made inside '
                       'generation 19. No file content of any earlier generation was opened.'),
            'firstWriteOfThisSessionUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                                        time.gmtime(session_start)),
            'trees': sib,
            'generationsModifiedDuringThisSession': touched,
            'claimLimit': ('this measures WHETHER this session wrote into them. It does not and '
                           'cannot certify that their earlier content is otherwise intact, and '
                           'it is not a restoration verdict for the two generation-16 files.'),
        },
        'carriedDisclosure_generation16NoteOverwrites': CARRIED_DISCLOSURE,
        'generation19LabelFindings': LABEL_FINDINGS,
        'state': ('CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE' if confined else 'NOT-CONFINED'),
        'isThisAPass': (
            'PASS for this generation\'s write confinement, and PASS for "this session did not '
            'write into an earlier generation". NOT a pass for history: the two generation-16 '
            'note overwrites remain OPEN and unrepaired, and the label corruption V19-D1 shows '
            'the damage class was still present in the copied library when this generation '
            'received it.'),
    }
    with open(OUT + '/notes/v19-history-standing.json', 'w') as f:
        json.dump(doc, f, indent=1)
    a = doc['measuredA_writeConfinement']
    print('write confinement      :', a['result'],
          '(foreign write rows %d, probe beneath runtime %s, clean imports %s)'
          % (a['foreignWriteOrRootAssignmentsInActiveCode'],
             a['liveProbeResolvedBeneathThisRuntime'],
             a['noActiveModuleImportsAnArchivedOrQuarantinedTree']))
    print('archived before-images :', groups['archivedBeforeImages'])
    print('quarantined modules    :', len(groups['quarantinedModules']))
    for s in sib:
        print('  prior %-16s present=%-5s newest=%-21s touchedThisSession=%s'
              % (s['generation'], s['present'], s.get('newestMtimeUtc'),
                 s.get('newerThanThisSessionsFirstWrite')))
    print('carried disclosure     : %d generation-16 files overwritten, status %s'
          % (len(CARRIED_DISCLOSURE['filesOverwritten']), CARRIED_DISCLOSURE['status']))
    print('state                  :', doc['state'])
    assert confined, {'foreign': foreign[:3], 'touched': touched, 'imports': bad_imports[:3]}


main()

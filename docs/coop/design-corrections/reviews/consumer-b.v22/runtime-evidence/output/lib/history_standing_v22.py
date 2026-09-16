"""History standing and write confinement for generation 22.

Generation 21 was prepared by the launcher and never run; there is no generation-21 tree for this
origin, so the prior-generation trees measured below are 14..20.

  MEASURED A  write confinement: every write destination of every ACTIVE module resolves beneath
              this runtime (from notes/v22-path-census.json), plus a live probe.
  MEASURED B  tree shape: archived before-images (now including lib.before-image.v20) present and
              quarantined tools off the import path.
  MEASURED C  prior-generation mtimes, by directory metadata only, as evidence that this session
              wrote into none of them. No file content of any earlier generation is opened.
  CARRIED     the generation-17 disclosure, unchanged: TWO files under the generation-16 output
              were overwritten by that session, their prior bytes were not retained, and this
              origin cannot restore them. Root supplies no restoration verdict.
  CARRIED     the label findings V18-D6 / V19-D1 / V19-D2 / V20-D6, and the generation-22 finding
              V22-D1: the generation-20 rebind's bare-label pass had rewritten the V19-D2 sentence
              and the generation-20 audit could not see it. Restored from lib.before-image.v19.
  NOT CLAIMED any restoration of the generation-16 files, and no pristine history.

State: CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
"""
import json
import os
import time

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v22'
OUT = RUNTIME + '/output'
SIBLINGS = ['/tmp/opensip-design-corrections/consumer-b' + '.v14',
            '/tmp/opensip-design-corrections/consumer-b' + '.v15',
            '/tmp/opensip-design-corrections/consumer-b' + '.v16',
            '/tmp/opensip-design-corrections/consumer-b' + '.v17',
            '/tmp/opensip-design-corrections/consumer-b' + '.v18',
            '/tmp/opensip-design-corrections/consumer-b' + '.v19',
            '/tmp/opensip-design-corrections/consumer-b' + '.v20']

CARRIED_DISCLOSURE = {
    'source': 'generation 17 review and helper-corrections row V17-D8',
    'whatHappened': (
        'two modules were wrongly exempted from that generation\'s path rebind, so their output '
        'root still named the previous generation and they wrote into it'),
    'filesOverwritten': ['consumer-b' + '.v16/output/helper-corrections.json',
                         'consumer-b' + '.v16/output/notes/siblings-untouched.json'],
    'filesNotTouched': ('no Run export, review file, requirement status, checkpoint or vector of '
                        'any earlier generation; generations 14 and 15 had zero writes'),
    'priorBytes': 'NOT retained by this origin and NOT restorable by it',
    'status': 'OPEN -- unrepaired, and not repairable from inside this runtime',
    'rootCustodyRestoration': ('root supplies no restoration verdict to this continuation. This '
                              'origin does not know and does not assert its outcome.'),
}

LABEL_FINDINGS = {
    'V18-D6': 'the rebind had relabelled the helper-correction rows; corrected at generation 19',
    'V19-D1': ('four historical helper-correction sentences and a LOST generation-17 ancestry '
               'entry, restored at generation 19 from the retained before-images'),
    'V19-D2': ('the generation-19 rebind rewrote its own docstring; later rebinds are '
               'self-excluded'),
    'V20-D6': ('four hand-written CURRENT declarations had kept an older label; corrected at '
               'generation 20'),
    'V22-D1': ('the generation-20 rebind\'s blanket bare-label pass rewrote the second label of the '
               'V19-D2 sentence to v20, and the generation-20 audit misclassified a two-label '
               'sentence as an ancestry row and never drift-checked it. Detected by the corrected '
               'audit at generation 22, restored from lib.before-image.v19; the generation-22 '
               'rebind rewrites joined labels only in an expected list of read modules.'),
    'generation22Measurement': ('notes/v22-label-history.json: exactly ONE historical drift before '
                                'the rebind (V19-D2) and NONE after it, with every current '
                                'declaration naming generation 22'),
}


def newest_mtime(root):
    best, count = 0.0, 0
    for d, _dirs, names in os.walk(root):
        best = max(best, os.path.getmtime(d))
        count += len(names)
        for n in names:
            try:
                best = max(best, os.path.getmtime(os.path.join(d, n)))
            except OSError:
                pass
    return best, count


def main():
    census = json.load(open(OUT + '/notes/v22-path-census.json'))
    foreign = census['foreignGenerationWriteOrRootAssignments']
    foreign_split = census.get('foreignSplitLiteralRootAssignments') or []

    probe = os.path.join(OUT, 'notes', '.write-probe')
    with open(probe, 'w') as f:
        f.write('confinement probe\n')
    reachable = os.path.realpath(probe).startswith(os.path.realpath(RUNTIME) + os.sep)
    os.remove(probe)

    groups = {
        'archivedBeforeImages': sorted(d for d in os.listdir(OUT)
                                       if d.startswith('lib.before-image.')),
        'quarantineDirPresent': os.path.isdir(OUT + '/lib.quarantine-legacy'),
        'quarantinedModules': sorted(f for f in os.listdir(OUT + '/lib.quarantine-legacy')
                                     if f.endswith('.py'))
        if os.path.isdir(OUT + '/lib.quarantine-legacy') else [],
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
                if (s.startswith('import ') or s.startswith('from ')
                        or ('sys.path' in s and 'insert' in s) or '__import__' in s):
                    bad_imports.append({'module': n, 'line': i, 'text': s[:120]})

    # the first write of THIS session is the generation-22 custody record written before any
    # copied code ran; the census is rewritten by later stages, so it cannot serve as the anchor
    session_start = os.path.getmtime(OUT + '/notes/v22-rebind.json')
    anchor = 'notes/v22-rebind.json (written once, by the single rebind run)'
    sib = []
    for p in SIBLINGS:
        if not os.path.isdir(p):
            sib.append({'generation': os.path.basename(p), 'present': False})
            continue
        mt, files = newest_mtime(p)
        sib.append({'generation': os.path.basename(p), 'present': True, 'fileCount': files,
                    'newestMtimeUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mt)),
                    'newerThanThisSessionsAnchorWrite': mt > session_start})
    touched = [s['generation'] for s in sib if s.get('newerThanThisSessionsAnchorWrite')]

    confined = (not foreign) and (not foreign_split) and reachable and not bad_imports \
        and not touched
    doc = {
        'standing': __doc__, 'generation': 'consumer-b.' + 'v22',
        'measuredA_writeConfinement': {
            'foreignWriteOrRootAssignmentsInActiveCode': len(foreign),
            'foreignSplitLiteralRootAssignmentsInActiveCode': len(foreign_split),
            'liveProbeResolvedBeneathThisRuntime': reachable,
            'noActiveModuleImportsAnArchivedOrQuarantinedTree': not bad_imports,
            'badImports': bad_imports,
            'result': 'CONFINED' if confined else 'NOT CONFINED'},
        'measuredB_treeShape': groups,
        'measuredC_priorGenerations': {
            'method': ('os.walk over directory metadata only, comparing each tree\'s newest '
                       'modification time with a FIXED anchor write this session made inside '
                       'generation 22. No file content of any earlier generation was opened.'),
            'anchor': anchor,
            'anchorWriteUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(session_start)),
            'anchorStanding': (
                'generation 20 anchored on the path census, which every command rewrites, so its '
                'timestamp moved each run and was the one non-substantive difference between '
                'consecutive reports. The rebind record is written once, so the anchor is stable.'),
            'trees': sib, 'generationsModifiedDuringThisSession': touched,
            'generation21': 'never run; no tree exists to measure',
            'claimLimit': ('this measures WHETHER this session wrote into them after the anchor. '
                           'It does not certify their earlier content is otherwise intact, and it '
                           'is not a restoration verdict for the two generation-16 files.')},
        'carriedDisclosure_generation16NoteOverwrites': CARRIED_DISCLOSURE,
        'labelFindingsCarriedForward': LABEL_FINDINGS,
        'state': 'CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE' if confined else 'NOT-CONFINED',
        'isThisAPass': ('PASS for this generation\'s write confinement and for "this session did '
                        'not write into an earlier generation". NOT a pass for history: the two '
                        'generation-16 note overwrites remain OPEN and unrepaired.'),
    }
    with open(OUT + '/notes/v22-history-standing.json', 'w') as f:
        json.dump(doc, f, indent=1)
    a = doc['measuredA_writeConfinement']
    print('write confinement      :', a['result'],
          '(foreign write rows %d, split roots %d, probe beneath runtime %s, clean imports %s)'
          % (a['foreignWriteOrRootAssignmentsInActiveCode'],
             a['foreignSplitLiteralRootAssignmentsInActiveCode'],
             a['liveProbeResolvedBeneathThisRuntime'],
             a['noActiveModuleImportsAnArchivedOrQuarantinedTree']))
    print('archived before-images :', groups['archivedBeforeImages'])
    print('quarantined modules    :', len(groups['quarantinedModules']))
    for s in sib:
        print('  prior %-16s present=%-5s newest=%-21s touchedThisSession=%s'
              % (s['generation'], s['present'], s.get('newestMtimeUtc'),
                 s.get('newerThanThisSessionsAnchorWrite')))
    print('carried disclosure     : %d generation-16 files overwritten, status %s'
          % (len(CARRIED_DISCLOSURE['filesOverwritten']), CARRIED_DISCLOSURE['status']))
    print('state                  :', doc['state'])
    assert confined, {'foreign': foreign[:3], 'touched': touched, 'imports': bad_imports[:3]}


main()

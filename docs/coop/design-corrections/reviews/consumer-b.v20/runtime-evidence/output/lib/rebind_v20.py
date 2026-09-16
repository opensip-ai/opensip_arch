"""Rebind the copied generation-19 library to generation 20 -- written fresh, run ONCE, judged
against notes/v20-path-census.json and notes/v20-label-history.json.

Rules, and why each one exists:

 1. BEFORE-IMAGE. output/lib is copied byte-for-byte to output/lib.before-image.v19 first, so the
    supplied generation-19 library is preserved exactly as received.

 2. PATH FORM ONLY. The old label is rewritten only when the very next character is `/`. That
    separator is what distinguishes a filesystem path from a sentence; V18-D6 and V19-D1 were both
    caused by a rewrite that could not tell them apart. (The constants below are SPLIT literals and
    this module is in its own exclusion list, because at generation 19 the rebind rewrote its own
    docstring -- V19-D2.)

 3. CURRENT DECLARATIONS. A bare previous-generation label that names the generation DOING the work
    (consumerId, ROOT/RUNTIME/CONSUMER constants, this origin's own self-attribution in a docstring
    or an exported synthetic-observation standing) becomes generation 20.

 4. HISTORICAL NARRATIVES AND ANCESTRY ROWS ARE NOT TOUCHED. Generation 19 restored four
    helper-correction sentences from the before-images and its audit reports NO DRIFT at the start
    of this generation; this rebind must keep it that way. The ancestry file is excluded from the
    bare-label pass entirely and GAINS generation 20 by an explicit edit.

 5. QUARANTINE. Tools pinned to an earlier generation's content (its kit digests, its progress
    record, its own rebind/census/label roots) move OFF the import path with a reason. Modules whose
    NAME carries the generation that authored them but whose CONTENT is a law measurement
    (glob_law_v19, repair_selection_v19, programentry_law_v19) are KEPT and rebound: the name is
    authorship history, not a pinned digest.

 6. ASSERTIONS. Afterwards: no active module names a foreign generation PATH, every output root is
    generation 20, the restored historical sentences are still intact, and the ancestry file still
    names generation 19.
"""
import json
import os
import re
import shutil

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = RUNTIME + '/output'
LIB = OUT + '/lib'
BEFORE = OUT + '/lib.before-image.v19'
QUAR = OUT + '/lib.quarantine-legacy'
OLD = 'consumer-b.' + 'v19'
NEW = 'consumer-b.' + 'v20'

QUARANTINE = {
    'census_v19.py': 'superseded by census_v20.py; its RUNTIME root is generation 19',
    'label_history_v19.py': 'superseded by label_history_v20.py',
    'history_standing_v19.py': 'superseded by history_standing_v20.py, which carries the same '
                               'disclosures forward',
    'verify_kit_v19.py': ('pinned to the generation-19 kit digests; generation 20 receives a '
                          'different 102-file kit and needs its own verifier'),
    'progress_v19.py': 'writes progress.v19.json, a historical record of another generation',
    'rebind_v19.py': ('a previous rebind: its own LIB/BEFORE roots are generation 19, so running '
                      'it would write a before-image into a read-only earlier generation '
                      '(defect class V17-D8)'),
}

# historical sentences restored at generation 19 from the before-images; asserted still intact
RESTORED = [
    ('opensip_capmanifest.py', '# HELPER CORRECTION (consumer-b.v14, recorded in '),
    ('opensip_schema.py', 'HELPER CORRECTION (consumer-b.v15): the first draft REPLACED'),
    ('opensip_schema.py', 'HELPER CORRECTION V16-D1 (consumer-b.v16): the walker kept passing'),
    ('opensip_schema.py', '# HELPER CORRECTION (consumer-b.v15): a branch written as a bare '
                          'local'),
]
# files excluded from the BARE-label pass: the ancestry file gains a row by explicit edit, and this
# module must not rewrite its own prose (V19-D2)
BARE_LABEL_EXCLUDED = ('deliver.py', 'rebind_v20.py', 'label_history_v20.py', 'census_v20.py')


def main():
    assert os.path.isdir(LIB)
    if os.path.isdir(BEFORE):
        raise SystemExit('before-image already exists; this rebind runs once only: ' + BEFORE)
    shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
    os.makedirs(QUAR, exist_ok=True)

    report = {'standing': __doc__, 'beforeImage': BEFORE, 'quarantined': [],
              'rewritten': [], 'assertions': []}

    why = os.path.join(QUAR, 'WHY-QUARANTINED.txt')
    lines = [open(why, encoding='utf-8').read().rstrip()] if os.path.exists(why) else []
    lines.append('\n--- generation 20 ---')
    for n, reason in sorted(QUARANTINE.items()):
        src = os.path.join(LIB, n)
        if not os.path.exists(src):
            continue
        shutil.move(src, os.path.join(QUAR, n))
        lines.append('%-26s %s' % (n, reason))
        report['quarantined'].append({'module': n, 'reason': reason})
    open(why, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py'):
            continue
        p = os.path.join(LIB, n)
        s0 = open(p, encoding='utf-8').read()
        s = s0.replace(OLD + '/', NEW + '/')
        paths = s0.count(OLD + '/')
        bare = 0
        if n not in BARE_LABEL_EXCLUDED:
            s, bare = re.subn(re.escape(OLD) + r'(?!/)', NEW, s)
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s)
            report['rewritten'].append({'module': n, 'pathOccurrences': paths,
                                        'bareLabelOccurrences': bare})

    bad_paths, bad_roots = [], []
    # a historical DISCLOSURE may legitimately name an earlier generation's path inside prose: the
    # generation-17 overwrite of two generation-16 files is exactly such a sentence and must stay
    DISCLOSURE_ALLOW = ('overwritten', 'consumer-b.v16/output --', 'TWO files under')
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py'):
            continue
        t = open(os.path.join(LIB, n), encoding='utf-8').read()
        for line in t.splitlines():
            for m in re.finditer(r'consumer-b\.v(\d+)/', line):
                if m.group(1) == '20':
                    continue
                if any(k in line for k in DISCLOSURE_ALLOW):
                    continue
                bad_paths.append('%s: %s' % (n, line.strip()[:90]))
        for m in re.finditer(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|BEFORE|CONSUMER)\s*=.*'
                             r'consumer-b\.v(\d+)', t, re.M):
            if m.group(2) != '20':
                bad_roots.append('%s: %s' % (n, m.group(0).strip()[:80]))
    for fn, sentence in RESTORED:
        t = open(os.path.join(LIB, fn), encoding='utf-8').read()
        report['assertions'].append(
            {'check': 'RESTORED_HISTORICAL_SENTENCE_INTACT:%s' % fn,
             'result': 'PASS' if sentence in t else 'FAIL', 'sentence': sentence[:70]})
    dv = open(os.path.join(LIB, 'deliver.py'), encoding='utf-8').read()
    report['assertions'] += [
        {'check': 'NO_FOREIGN_GENERATION_PATH_IN_ACTIVE_CODE',
         'result': 'PASS' if not bad_paths else 'FAIL', 'detail': bad_paths[:20]},
        {'check': 'EVERY_ACTIVE_OUTPUT_ROOT_IS_THIS_GENERATION',
         'result': 'PASS' if not bad_roots else 'FAIL', 'detail': bad_roots[:20]},
        # the ancestry entries are SPLIT literals ('consumer-b' + '.v19'), which is exactly what
        # keeps a mechanical rewrite away from them, so the check looks for the split form. An
        # earlier draft of this assertion searched for the joined form and failed on a list that
        # was intact -- recorded because a check that reports a false failure is still a defect.
        {'check': 'ANCESTRY_FILE_STILL_NAMES_GENERATION_19',
         'result': 'PASS' if ("'.v19'" in dv or OLD in dv) else 'FAIL',
         'detail': 'the ancestry list must GAIN generation 20, never lose generation 19'},
    ]
    with open(OUT + '/notes/v20-rebind.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('before-image      :', BEFORE)
    print('quarantined       :', [r['module'] for r in report['quarantined']])
    print('rewritten modules :', len(report['rewritten']))
    for a in report['assertions']:
        print('  %-58s %s %s' % (a['check'][:58], a['result'],
                                 json.dumps(a.get('detail'))[:100]
                                 if a['result'] == 'FAIL' else ''))
    fails = [a for a in report['assertions'] if a['result'] == 'FAIL']
    print('FAILED ASSERTIONS:', len(fails))
    raise SystemExit(1 if fails else 0)


main()

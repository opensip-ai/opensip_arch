"""Rebind the copied generation-18 library to generation 19 -- written fresh, run ONCE, and
judged against notes/v19-path-census.json and notes/v19-label-history.json.

What this does, and the reason for each rule:

 1. BEFORE-IMAGE. output/lib is copied byte-for-byte to output/lib.before-image.v18 first, so the
    supplied generation-18 library is preserved exactly as received.

 2. PATH FORM ONLY. `consumer-b.v18` + `/` -> `consumer-b.v19` + `/`. The trailing separator is
    required: that is what distinguishes a filesystem path from a sentence. V18-D6 was caused by a
    rewrite that could not tell the two apart.

    V19-D2, found by reading this file after its own run: the two lines above originally spelled
    the OLD label plainly, and this module REWROTE ITS OWN DOCSTRING while rewriting everything
    else -- the V15-D1 defect class, in the very tool written to prevent it. The logic was never
    affected (OLD/NEW are split literals), but the sentence became false and is repaired here,
    split, with the module added to the self-exclusion below.

 3. CURRENT DECLARATIONS. A bare previous-generation label that names the generation DOING the work
    (consumerId, ROOT/RUNTIME/CONSUMER constants, this origin's own self-attribution in a
    docstring or an exported synthetic-observation standing) becomes `consumer-b.v19`.

 4. HISTORICAL NARRATIVES ARE RESTORED, NOT REWRITTEN. Four helper-correction comments were
    silently relabelled by successive rebinds since generation 15. The retained before-images are
    the evidence: the earliest before-image containing the same sentence carries its true
    generation. Those four are restored to their true labels and written as SPLIT string literals
    so no future mechanical rewrite can reach them. This is finding V19-D1.

 5. QUARANTINE. Tools pinned to a previous generation's content (its kit digests, its progress
    record, its own rebind roots) are moved OFF the import path with a reason, rather than
    rebound into something they were never measured against. A source-rewriting one-shot migration
    tool is quarantined for the same reason. An exempt WRITER is still a writer: nothing stays on
    the import path whose write destination is not generation 19.

 6. ASSERTIONS. After rewriting: no active module names a foreign generation PATH; every output
    root is generation 19; the four restored narratives carry their true labels; and the ancestry
    lists, which must GAIN generation 19 rather than lose generation 18, are left for explicit
    edits and are asserted to still contain their v18 entry.
"""
import json
import os
import re
import shutil

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v19'
OUT = RUNTIME + '/output'
LIB = OUT + '/lib'
BEFORE = OUT + '/lib.before-image.v18'
QUAR = OUT + '/lib.quarantine-legacy'
OLD = 'consumer-b.' + 'v18'
NEW = 'consumer-b.' + 'v19'

QUARANTINE = {
    'census_v18.py': 'superseded by census_v19.py; its RUNTIME root is generation 18',
    'rebind_v18.py': ('a previous rebind: its own LIB/BEFORE roots are generation 18, so running '
                      'it would write a before-image into a read-only earlier generation '
                      '(defect class V17-D8)'),
    'verify_kit_v18.py': ('pinned to the 101-file generation-18 kit digests; generation 19 '
                          'receives a different 102-file kit and needs its own verifier'),
    'history_standing_v18.py': 'superseded by history_standing_v19.py, which carries the same '
                               'disclosures forward',
    'progress_v17.py': 'writes progress.v17.json, a historical record of another generation',
    'progress_v18.py': 'writes progress.v18.json, a historical record of another generation',
    'pin_fixtures.py': ('a one-shot source-REWRITING migration already applied in an earlier '
                        'generation; its literals no longer exist and a source rewriter has no '
                        'place on the import path'),
}

# (file, true generation, the exact sentence fragment before the label, fragment after it)
RESTORE = [
    ('opensip_capmanifest.py', 'v14', '# HELPER CORRECTION (', ', recorded in '),
    ('opensip_schema.py', 'v15', 'HELPER CORRECTION (', '): the first draft REPLACED'),
    ('opensip_schema.py', 'v16', 'HELPER CORRECTION V16-D1 (', '): the walker kept passing'),
    ('opensip_schema.py', 'v15', '# HELPER CORRECTION (', '): a branch written as a bare local'),
]
# lines that must GAIN generation 19 instead of having the old label replaced, plus this module
# itself (V19-D2: it rewrote its own docstring on the single run it was designed for). Both are
# handled by explicit edits, never by the mechanical pass.
ANCESTRY_KEEPS_V18 = ('deliver.py', 'rebind_v19.py')


def main():
    assert os.path.isdir(LIB)
    if os.path.isdir(BEFORE):
        raise SystemExit('before-image already exists; rebind must run once only: ' + BEFORE)
    shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
    os.makedirs(QUAR, exist_ok=True)

    report = {'standing': __doc__, 'beforeImage': BEFORE, 'quarantined': [],
              'rewritten': [], 'restoredHistoricalLabels': [], 'assertions': []}

    # ---- 5. quarantine
    why = os.path.join(QUAR, 'WHY-QUARANTINED.txt')
    lines = []
    if os.path.exists(why):
        lines.append(open(why, encoding='utf-8').read().rstrip())
    lines.append('\n--- generation 19 ---')
    for n, reason in sorted(QUARANTINE.items()):
        src = os.path.join(LIB, n)
        if not os.path.exists(src):
            continue
        shutil.move(src, os.path.join(QUAR, n))
        lines.append('%-26s %s' % (n, reason))
        report['quarantined'].append({'module': n, 'reason': reason})
    open(why, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # ---- 2 + 3. rewrite
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py'):
            continue
        p = os.path.join(LIB, n)
        s0 = open(p, encoding='utf-8').read()
        s = s0.replace(OLD + '/', NEW + '/')
        paths = s0.count(OLD + '/')
        bare = 0
        if n not in ANCESTRY_KEEPS_V18:
            s, bare = re.subn(re.escape(OLD) + r'(?!/)', NEW, s)
        # ---- 4. restore the historical narratives, AFTER the bare rewrite, as split literals
        restored = []
        for fn, true_gen, pre, post in RESTORE:
            if fn != n:
                continue
            for cur in (NEW, OLD):
                bad = pre + cur + post
                if bad in s:
                    s = s.replace(bad, pre + 'consumer-b.' + true_gen + post)
                    restored.append({'trueGeneration': true_gen, 'sentence': post.strip()[:60],
                                     'wasLabelled': cur})
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s)
            report['rewritten'].append({'module': n, 'pathOccurrences': paths,
                                       'bareLabelOccurrences': bare})
        if restored:
            report['restoredHistoricalLabels'].append({'module': n, 'restored': restored})

    # ---- 6. assertions
    bad_paths, bad_roots, still_old = [], [], []
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py'):
            continue
        t = open(os.path.join(LIB, n), encoding='utf-8').read()
        for m in re.finditer(r'consumer-b\.v(\d+)/', t):
            if m.group(1) != '19':
                bad_paths.append('%s: %s' % (n, m.group(0)))
        for m in re.finditer(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|BEFORE|CONSUMER)\s*=.*'
                             r'consumer-b\.v(\d+)', t, re.M):
            if m.group(2) != '19':
                bad_roots.append('%s: %s' % (n, m.group(0).strip()[:80]))
        if OLD in t and n not in ANCESTRY_KEEPS_V18:
            for line in t.splitlines():
                if OLD in line:
                    still_old.append('%s: %s' % (n, line.strip()[:90]))
    for fn, true_gen, pre, post in RESTORE:
        t = open(os.path.join(LIB, fn), encoding='utf-8').read()
        ok = (pre + 'consumer-b.' + true_gen + post) in t
        report['assertions'].append({'check': 'HISTORICAL_LABEL_RESTORED:%s:%s'
                                     % (fn, true_gen), 'result': 'PASS' if ok else 'FAIL',
                                     'sentence': post.strip()[:60]})
    dv = open(os.path.join(LIB, 'deliver.py'), encoding='utf-8').read()
    report['assertions'] += [
        {'check': 'NO_FOREIGN_GENERATION_PATH_IN_ACTIVE_CODE',
         'result': 'PASS' if not bad_paths else 'FAIL', 'detail': bad_paths[:20]},
        {'check': 'EVERY_ACTIVE_OUTPUT_ROOT_IS_THIS_GENERATION',
         'result': 'PASS' if not bad_roots else 'FAIL', 'detail': bad_roots[:20]},
        {'check': 'NO_STRAY_PREVIOUS_GENERATION_LABEL_OUTSIDE_THE_ANCESTRY_FILES',
         'result': 'PASS' if not still_old else 'FAIL', 'detail': still_old[:20]},
        {'check': 'ANCESTRY_FILE_STILL_NAMES_GENERATION_18',
         'result': 'PASS' if OLD in dv else 'FAIL',
         'detail': 'the ancestry list must GAIN v19, never lose v18'},
    ]
    with open(OUT + '/notes/v19-rebind.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('before-image      :', BEFORE)
    print('quarantined       :', [r['module'] for r in report['quarantined']])
    print('rewritten modules :', len(report['rewritten']))
    print('restored labels   :', report['restoredHistoricalLabels'])
    for a in report['assertions']:
        print('  %-58s %s %s' % (a['check'][:58], a['result'],
                                 json.dumps(a.get('detail'))[:90] if a['result'] == 'FAIL'
                                 else ''))
    fails = [a for a in report['assertions'] if a['result'] == 'FAIL']
    print('FAILED ASSERTIONS:', len(fails))
    raise SystemExit(1 if fails else 0)


main()

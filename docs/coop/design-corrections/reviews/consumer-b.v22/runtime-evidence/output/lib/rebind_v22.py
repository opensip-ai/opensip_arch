"""Rebind the copied generation-20 library to generation 22 -- written fresh, run ONCE, judged
against notes/v22-path-census.json and notes/v22-label-history.json.

Generation 21 was never run, so the copy being rebound is generation 20's library.

Rules, and why each one exists:

 1. BEFORE-IMAGE. output/lib is copied byte-for-byte to output/lib.before-image.v20 first, so the
    supplied generation-20 library is preserved exactly as received, INCLUDING the V19-D2 sentence
    as the generation-20 rebind left it (the damaged predecessor is retained, not overwritten).

 2. PATH FORM. `consumer-b.v20` followed by `/` becomes generation 22 in every active module.

 3. CURRENT DECLARATIONS, BY AN EXPECTED LIST. A joined `consumer-b.v20` NOT followed by `/` is
    rewritten only in modules on EXPECTED_JOINED_CURRENT, each of which was read and is a
    consumerId / ROOT-RUNTIME-CONSUMER constant / self-attribution. The generation-20 rebind used a
    blanket bare-label pass with an exclusion list, and that pass rewrote the historical V19-D2
    sentence (V22-D1). A rewrite that lands anywhere else fails an assertion instead.

 4. SPLIT-LITERAL CURRENT DECLARATIONS, BY EXACT LINE. 'consumer-b.' + 'v20' is also the form the
    V20-* helper rows use for their TRUE provenance, so no pattern pass touches it; the four
    current ones (deliver ROOT / consumerId / md header, helper-corrections and phase6_repair
    consumerIds) are replaced by exact source line.

 5. HISTORICAL RESTORATION. The V19-D2 sentence is restored to the exact bytes held in
    lib.before-image.v19, which is where that sentence was authored.

 6. QUARANTINE. Generation-pinned tools move off the import path with a reason.

 7. ASSERTIONS. No active module names a foreign PATH or ROOT, the restored sentence equals its
    before-image, the V20-D6 sentence still says v20, the V20 rows keep generation v20, and the
    four sentences restored at generation 19 are intact.
"""
import json
import os
import re
import shutil

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v22'
OUT = RUNTIME + '/output'
LIB = OUT + '/lib'
BEFORE = OUT + '/lib.before-image.' + 'v20'
QUAR = OUT + '/lib.quarantine-legacy'
OLD = 'consumer-b.' + 'v20'
NEW = 'consumer-b.' + 'v22'

QUARANTINE = {
    'census_v20.py': 'superseded by census_v22.py; its RUNTIME root is generation 20',
    'label_history_v20.py': ('superseded by label_history_v22.py, which also fixes the ancestry '
                             'misclassification that hid the V19-D2 drift (V22-D1)'),
    'history_standing_v20.py': 'superseded by history_standing_v22.py',
    'verify_kit_v20.py': ('pinned to the generation-20 kit digests; generation 22 receives a '
                          'different 102-file kit and has its own verifier'),
    'progress_v20.py': 'writes progress.v20.json, a historical record of another generation',
    'rebind_v20.py': ('a previous rebind: its roots are generation 20 and its blanket bare-label '
                      'pass is the V22-D1 defect'),
}
NEW_TOOLS = ('census_v22.py', 'verify_kit_v22.py', 'label_history_v22.py', 'rebind_v22.py')

# modules whose joined non-path `consumer-b.v20` occurrences were each read and are CURRENT
EXPECTED_JOINED_CURRENT = {
    'status.py', 'phase1.py', 'export_run.py', 'graph_query.py', 'phase6_config.py',
    'phase3_traces.py', 'checkpoint.py', 'phase4.py', 'phase0.py', 'phase10.py',
    'checkpoints_all.py', 'opensip_schema.py', 'peek20_final_bytes2.py', 'relocation_control.py',
    'phase4_modes.py', 'phase8.py', 'opensip_core.py', 'export_pilot.py', 'relation_table.py',
    'phase6_clones.py',
}

SPLIT_CURRENT = {
    'deliver.py': [
        ("ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v20'",
         "ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v22'"),
        ("        'consumerId': 'consumer-b.' + 'v20',",
         "        'consumerId': 'consumer-b.' + 'v22',"),
        ("    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v20')",
         "    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v22')"),
    ],
    'helper_corrections.py': [
        ("    doc = {'consumerId': 'consumer-b.' + 'v20', 'standing': __doc__,",
         "    doc = {'consumerId': 'consumer-b.' + 'v22', 'standing': __doc__,"),
    ],
    'phase6_repair.py': [
        ("    doc = {'consumerId': 'consumer-b.' + 'v20',",
         "    doc = {'consumerId': 'consumer-b.' + 'v22',"),
    ],
}

# V19-D2: authored at generation 19; the generation-20 bare-label pass damaged its second label
V19D2_MARKER = 'rewrote ITS OWN docstring on the single run it was designed'
V19D2_DAMAGED = '"`consumer-b.v18`+`/` -> `' + 'consumer-b.v20' + '`+`/`"'

RESTORED_AT_19 = [
    ('opensip_capmanifest.py', '# HELPER CORRECTION (consumer-b.v14, recorded in '),
    ('opensip_schema.py', 'HELPER CORRECTION (consumer-b.v15): the first draft REPLACED'),
    ('opensip_schema.py', 'HELPER CORRECTION V16-D1 (consumer-b.v16): the walker kept passing'),
    ('opensip_schema.py', '# HELPER CORRECTION (consumer-b.v15): a branch written as a bare '
                          'local'),
]
V20D6_SENTENCE = "the two consumerIds are re-stated as consumer-b.v20 with an in-code note"
DISCLOSURE_ALLOW = ('overwritten', 'consumer-b.v16/output --', 'TWO files under')


def v19d2_true_line():
    t = open(OUT + '/lib.before-image.v19/helper_corrections.py', encoding='utf-8').read()
    lines = t.splitlines()
    for i, line in enumerate(lines):
        if V19D2_MARKER in line:
            return lines[i + 1]
    raise SystemExit('V19-D2 sentence not found in lib.before-image.v19')


def main():
    assert os.path.isdir(LIB)
    if os.path.isdir(BEFORE):
        raise SystemExit('before-image already exists; this rebind runs once only: ' + BEFORE)
    shutil.copytree(LIB, BEFORE, ignore=shutil.ignore_patterns('__pycache__'))
    os.makedirs(QUAR, exist_ok=True)
    report = {'standing': __doc__, 'beforeImage': BEFORE, 'quarantined': [],
              'rewritten': [], 'splitLiteralReplacements': [], 'restorations': [],
              'assertions': []}

    why = os.path.join(QUAR, 'WHY-QUARANTINED.txt')
    lines = [open(why, encoding='utf-8').read().rstrip()] if os.path.exists(why) else []
    lines.append('\n--- generation 22 (generation 21 never ran) ---')
    for n, reason in sorted(QUARANTINE.items()):
        src = os.path.join(LIB, n)
        if not os.path.exists(src):
            continue
        shutil.move(src, os.path.join(QUAR, n))
        lines.append('%-26s %s' % (n, reason))
        report['quarantined'].append({'module': n, 'reason': reason})
    open(why, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    unexpected_joined = []
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py') or n in NEW_TOOLS:
            continue
        p = os.path.join(LIB, n)
        s0 = open(p, encoding='utf-8').read()
        s = s0.replace(OLD + '/', NEW + '/')
        paths = s0.count(OLD + '/')
        joined = len(re.findall(re.escape(OLD) + r'(?!/)', s))
        if joined:
            if n in EXPECTED_JOINED_CURRENT:
                s = re.sub(re.escape(OLD) + r'(?!/)', NEW, s)
            elif n != 'helper_corrections.py':
                unexpected_joined.append({'module': n, 'occurrences': joined})
        for old_line, new_line in SPLIT_CURRENT.get(n, []):
            c = s.count(old_line)
            s = s.replace(old_line, new_line)
            report['splitLiteralReplacements'].append({'module': n, 'line': new_line.strip(),
                                                       'occurrences': c})
        if n == 'helper_corrections.py':
            true_line = v19d2_true_line()
            ls = s.split('\n')
            for i, line in enumerate(ls):
                if V19D2_MARKER in line and V19D2_DAMAGED in ls[i + 1]:
                    report['restorations'].append({'module': n, 'row': 'V19-D2',
                                                   'damaged': ls[i + 1].strip(),
                                                   'restoredFrom': 'lib.before-image.v19',
                                                   'restored': true_line.strip()})
                    ls[i + 1] = true_line
            s = '\n'.join(ls)
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s)
            report['rewritten'].append({'module': n, 'pathOccurrences': paths,
                                        'joinedCurrentOccurrences':
                                        joined if n in EXPECTED_JOINED_CURRENT else 0})

    bad_paths, bad_roots = [], []
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py') or n in NEW_TOOLS:
            continue
        t = open(os.path.join(LIB, n), encoding='utf-8').read()
        for line in t.splitlines():
            for m in re.finditer(r'consumer-b\.v(\d+)/', line):
                if m.group(1) == '22' or any(k in line for k in DISCLOSURE_ALLOW):
                    continue
                bad_paths.append('%s: %s' % (n, line.strip()[:90]))
        for m in re.finditer(r"^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|SUBJ|BEFORE|CONSUMER|V16)\s*=.*"
                             r"consumer-b\.?(?:['\"]\s*\+\s*['\"]\.?)?v(\d+)", t, re.M):
            if m.group(2) != '22':
                bad_roots.append('%s: %s' % (n, m.group(0).strip()[:90]))
    hc = open(os.path.join(LIB, 'helper_corrections.py'), encoding='utf-8').read()
    for fn, sentence in RESTORED_AT_19:
        t = open(os.path.join(LIB, fn), encoding='utf-8').read()
        report['assertions'].append({'check': 'RESTORED_AT_19_INTACT:%s' % fn,
                                     'result': 'PASS' if sentence in t else 'FAIL'})
    report['assertions'] += [
        {'check': 'NO_FOREIGN_GENERATION_PATH_IN_ACTIVE_CODE',
         'result': 'PASS' if not bad_paths else 'FAIL', 'detail': bad_paths[:20]},
        {'check': 'EVERY_ACTIVE_ROOT_IS_THIS_GENERATION',
         'result': 'PASS' if not bad_roots else 'FAIL', 'detail': bad_roots[:20]},
        {'check': 'NO_JOINED_LABEL_OUTSIDE_THE_EXPECTED_CURRENT_LIST',
         'result': 'PASS' if not unexpected_joined else 'FAIL', 'detail': unexpected_joined},
        {'check': 'V19_D2_SENTENCE_EQUALS_ITS_BEFORE_IMAGE',
         'result': 'PASS' if (v19d2_true_line() in hc and V19D2_DAMAGED not in hc
                              and len(report['restorations']) == 1) else 'FAIL'},
        {'check': 'V20_D6_SENTENCE_STILL_NAMES_GENERATION_20',
         'result': 'PASS' if V20D6_SENTENCE in hc else 'FAIL'},
        {'check': 'V20_ROWS_KEEP_GENERATION_20',
         'result': 'PASS' if hc.count("'generation': 'consumer-b.' + 'v20'") == 7 else 'FAIL',
         'detail': hc.count("'generation': 'consumer-b.' + 'v20'")},
        {'check': 'EVERY_SPLIT_LITERAL_CURRENT_DECLARATION_REPLACED_ONCE',
         'result': 'PASS' if all(r['occurrences'] == 1
                                 for r in report['splitLiteralReplacements']) else 'FAIL',
         'detail': report['splitLiteralReplacements']},
    ]
    with open(OUT + '/notes/v22-rebind.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('before-image      :', BEFORE)
    print('quarantined       :', [r['module'] for r in report['quarantined']])
    print('rewritten modules :', len(report['rewritten']))
    print('restorations      :', [(r['row'], r['restoredFrom']) for r in report['restorations']])
    for a in report['assertions']:
        print('  %-58s %s %s' % (a['check'][:58], a['result'],
                                 json.dumps(a.get('detail'))[:140]
                                 if a['result'] == 'FAIL' else ''))
    fails = [a for a in report['assertions'] if a['result'] == 'FAIL']
    print('FAILED ASSERTIONS:', len(fails))
    raise SystemExit(1 if fails else 0)


main()

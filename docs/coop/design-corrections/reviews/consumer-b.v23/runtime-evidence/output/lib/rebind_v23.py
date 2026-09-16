"""Rebind the copied generation-22 library to generation 23 -- written fresh, run ONCE, judged
against notes/v23-path-census.json and notes/v23-label-history.json.

Rules (the generation-22 rebind's, applied to 22 -> 23):

 1. BEFORE-IMAGE. output/lib is copied byte-for-byte to output/lib.before-image.v22 first, so the
    supplied generation-22 library is preserved exactly as received. The two generation-23 tools
    already written into lib (census_v23.py, rebind_v23.py) are not generation-22 bytes and are
    left out of that image.
 2. PATH FORM. `consumer-b.v22` followed by `/` becomes generation 23 in every active module.
 3. CURRENT DECLARATIONS, BY AN EXPECTED LIST. A joined `consumer-b.v22` NOT followed by `/` is
    rewritten only in modules on EXPECTED_JOINED_CURRENT; each occurrence was listed by the
    generation-23 census and read (consumerId / ROOT-RUNTIME-CONSUMER constants / self-attribution /
    the relocation FORBIDDEN list of this runtime). A joined label anywhere else fails an assertion.
 4. SPLIT-LITERAL CURRENT DECLARATIONS, BY EXACT LINE. 'consumer-b.' + 'v22' is also the form the
    V22-* helper rows use for their TRUE provenance, so no pattern pass touches it; the five current
    ones are replaced by exact source line.
 5. QUARANTINE. Generation-22-pinned tools move off the import path with a reason; their
    generation-23 successors are written fresh.
 6. ASSERTIONS. No active module names a foreign PATH or ROOT; no joined label outside the list; the
    V22 rows keep generation 22 and the V20 rows generation 20; the V19-D2 sentence still equals
    its generation-19 before-image; the four sentences restored at generation 19 are intact.
"""
import json
import os
import re
import shutil

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.' + 'v23'
OUT = RUNTIME + '/output'
LIB = OUT + '/lib'
BEFORE = OUT + '/lib.before-image.' + 'v22'
QUAR = OUT + '/lib.quarantine-legacy'
OLD = 'consumer-b.' + 'v22'
NEW = 'consumer-b.' + 'v23'

QUARANTINE = {
    'census_v22.py': 'superseded by census_v23.py; its RUNTIME root is generation 22',
    'label_history_v22.py': 'superseded by label_history_v23.py (adds lib.before-image.v22)',
    'history_standing_v22.py': 'superseded by history_standing_v23.py',
    'verify_kit_v22.py': ('pinned to the generation-22 kit digests; generation 23 receives a '
                          'different 102-file kit and has its own verifier'),
    'progress_v22.py': 'writes progress.v22.json, a historical record of another generation',
    'rebind_v22.py': 'a previous rebind: its roots and before-image are generation 22',
    'preserve_predecessors_v22.py': ('run once at generation 22 to write predecessors.v20; its '
                                     'successor writes predecessors.v22'),
    'stage_launcher_v22.py': ('writes generation-22 stage-log names; superseded by '
                              'stage_launcher_v23.py'),
    'read_graph_v22.py': 'writes notes/v22-read-graph.json; superseded by read_graph_v23.py',
}
NEW_TOOLS = ('census_v23.py', 'rebind_v23.py', 'preserve_predecessors_v23.py',
             'label_history_v23.py')

EXPECTED_JOINED_CURRENT = {
    'audit_claimed_positives.py', 'checkpoint.py', 'checkpoints_all.py', 'export_pilot.py',
    'export_run.py', 'graph_query.py', 'opensip_core.py', 'opensip_schema.py',
    'peek20_final_bytes2.py', 'phase0.py', 'phase1.py', 'phase10.py', 'phase3_traces.py',
    'phase4.py', 'phase4_modes.py', 'phase6_clones.py', 'phase6_config.py', 'phase8.py',
    'relation_table.py', 'relocation_control.py', 'status.py',
}

SPLIT_CURRENT = {
    'deliver.py': [
        ("ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v22'",
         "ROOT = '/tmp/opensip-design-corrections/consumer-b.' + 'v23'"),
        ("        'consumerId': 'consumer-b.' + 'v22',",
         "        'consumerId': 'consumer-b.' + 'v23',"),
        ("    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v22')",
         "    A('# OpenSIP blind consumer design review -- consumer-b.' + 'v23')"),
    ],
    'helper_corrections.py': [
        ("    doc = {'consumerId': 'consumer-b.' + 'v22', 'standing': __doc__,",
         "    doc = {'consumerId': 'consumer-b.' + 'v23', 'standing': __doc__,"),
    ],
    'phase6_repair.py': [
        ("    doc = {'consumerId': 'consumer-b.' + 'v22',",
         "    doc = {'consumerId': 'consumer-b.' + 'v23',"),
    ],
}

V19D2_MARKER = 'rewrote ITS OWN docstring on the single run it was designed'
RESTORED_AT_19 = [
    ('opensip_capmanifest.py', '# HELPER CORRECTION (consumer-b.v14, recorded in '),
    ('opensip_schema.py', 'HELPER CORRECTION (consumer-b.v15): the first draft REPLACED'),
    ('opensip_schema.py', 'HELPER CORRECTION V16-D1 (consumer-b.v16): the walker kept passing'),
    ('opensip_schema.py', '# HELPER CORRECTION (consumer-b.v15): a branch written as a bare '
                          'local'),
]
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
    shutil.copytree(LIB, BEFORE,
                    ignore=shutil.ignore_patterns('__pycache__', *NEW_TOOLS))
    os.makedirs(QUAR, exist_ok=True)
    report = {'standing': __doc__, 'beforeImage': BEFORE, 'quarantined': [],
              'rewritten': [], 'splitLiteralReplacements': [], 'assertions': []}

    why = os.path.join(QUAR, 'WHY-QUARANTINED.txt')
    lines = [open(why, encoding='utf-8').read().rstrip()] if os.path.exists(why) else []
    lines.append('\n--- generation 23 ---')
    for n, reason in sorted(QUARANTINE.items()):
        src = os.path.join(LIB, n)
        if not os.path.exists(src):
            continue
        shutil.move(src, os.path.join(QUAR, n))
        lines.append('%-30s %s' % (n, reason))
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
            else:
                unexpected_joined.append({'module': n, 'occurrences': joined})
        for old_line, new_line in SPLIT_CURRENT.get(n, []):
            c = s.count(old_line)
            s = s.replace(old_line, new_line)
            report['splitLiteralReplacements'].append({'module': n, 'line': new_line.strip(),
                                                       'occurrences': c})
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
                if m.group(1) == '23' or any(k in line for k in DISCLOSURE_ALLOW):
                    continue
                bad_paths.append('%s: %s' % (n, line.strip()[:90]))
        for m in re.finditer(r"^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|SUBJ|BEFORE|CONSUMER|V16)\s*=.*"
                             r"consumer-b\.?(?:['\"]\s*\+\s*['\"]\.?)?v(\d+)", t, re.M):
            if m.group(2) != '23':
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
         'result': 'PASS' if v19d2_true_line() in hc else 'FAIL'},
        {'check': 'V22_ROWS_KEEP_GENERATION_22',
         'result': 'PASS' if hc.count("'generation': 'consumer-b.' + 'v22'") == 13 else 'FAIL',
         'detail': hc.count("'generation': 'consumer-b.' + 'v22'")},
        {'check': 'V20_ROWS_KEEP_GENERATION_20',
         'result': 'PASS' if hc.count("'generation': 'consumer-b.' + 'v20'") == 7 else 'FAIL',
         'detail': hc.count("'generation': 'consumer-b.' + 'v20'")},
        {'check': 'EVERY_SPLIT_LITERAL_CURRENT_DECLARATION_REPLACED_ONCE',
         'result': 'PASS' if all(r['occurrences'] == 1
                                 for r in report['splitLiteralReplacements'])
         and len(report['splitLiteralReplacements']) == 5 else 'FAIL',
         'detail': report['splitLiteralReplacements']},
    ]
    with open(OUT + '/notes/v23-rebind.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('before-image      :', BEFORE)
    print('quarantined       :', [r['module'] for r in report['quarantined']])
    print('rewritten modules :', len(report['rewritten']))
    for a in report['assertions']:
        print('  %-58s %s %s' % (a['check'][:58], a['result'],
                                 json.dumps(a.get('detail'))[:200]
                                 if a['result'] == 'FAIL' else ''))
    fails = [a for a in report['assertions'] if a['result'] == 'FAIL']
    print('FAILED ASSERTIONS:', len(fails))
    raise SystemExit(1 if fails else 0)


main()

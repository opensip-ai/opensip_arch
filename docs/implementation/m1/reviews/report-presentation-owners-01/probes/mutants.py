"""Apply single textual mutants to private copies and run the subject's own check.py.
Killed = check exits nonzero. Subjects are never modified."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/tmp/opensip-implementation')
WORK = HERE.parent / 'runs' / 'mutants'
PY = '/tmp/opensip-implementation/metadata-reference-env/bin/python'

M = [
 # catalogue
 ('CAT-M1', 'm1-presentation-catalog-subject-01', 'catalog.py', "    require(listing in admitted['closure']['tree'], 'CATALOG.CLOSURE-TREE')\n", '', 'drop identity closure.tree association'),
 ('CAT-M2', 'm1-presentation-catalog-subject-01', 'catalog.py', "        require(len(keys) == len(set(keys)), 'CATALOG.DUPLICATE-KEY')\n", '', 'drop duplicate descriptor key refusal'),
 ('CAT-M3', 'm1-presentation-catalog-subject-01', 'catalog.py', "    reference.canonical(data)\n", '', 'drop canonical byte cap of parsed listing'),
 ('CAT-M4', 'm1-presentation-catalog-subject-01', 'catalog.py', "    require(receipt['closureId'] == expected_closure_id, 'CATALOG.SELECTED-CLOSURE')\n", '', 'latest/other-closure fallback in selection'),
 ('CAT-M5', 'm1-presentation-catalog-subject-01', 'catalog.py', "        return {'state': 'unavailable', 'closureId': expected_closure_id, 'reason': 'catalog-not-retained'}", "        return {'state': 'unavailable', 'closureId': expected_closure_id, 'reason': 'no-catalogue-declared'}", 'relabel absence reason'),
 ('CAT-M6', 'm1-presentation-catalog-subject-01', 'catalog.py', "        require(set(keys) <= declared[group], 'CATALOG.UNDECLARED-KEY')\n", "        require(set(keys) <= declared[group] | {k for k in keys if group == 'capabilities'}, 'CATALOG.UNDECLARED-KEY')\n", 'capabilities exempt from declaration index'),
 # configuration
 ('CFG-M1', 'm1-config-disclosure-subject-01', 'disclosure.py', "                row['itemCount'] = len(configuration[group][field])", "                row['itemCount'] = min(len(configuration[group][field]), 1)", 'saturate itemCount'),
 ('CFG-M2', 'm1-config-disclosure-subject-01', 'disclosure.py', "    if digest != admitted_plan['resolvedConfigDigest']:\n        raise DisclosureRefusal('CONFIG-DISCLOSURE.SOURCE-DIGEST')\n", '', 'current-settings fallback: no digest check'),
 ('CFG-M3', 'm1-config-disclosure-subject-01', 'disclosure.py', "        if field not in configuration[group]:\n            row = {'field': key, 'state': 'not-present'}\n", "        if field not in configuration[group] or configuration[group][field] == []:\n            row = {'field': key, 'state': 'not-present'}\n", 'empty collapses to not-present'),
 ('CFG-M4', 'm1-config-disclosure-subject-01', 'disclosure.py', "'planId': plan_id,", "'planId': 'plan2:' + '1' * 64,", 'planId constant (not bound)'),
 # timing
 ('TIM-M1', 'm1-workflow-timing-subject-01', 'timing.py', "    milliseconds = (end_ns - start_ns) // 1_000_000", "    milliseconds = (end_ns - start_ns + 500_000) // 1_000_000", 'round instead of floor'),
 ('TIM-M2', 'm1-workflow-timing-subject-01', 'timing.py', " or outcome == 'abandoned':", ':', 'abandoned may carry measured duration'),
 ('TIM-M3', 'm1-workflow-timing-subject-01', 'timing.py', "    missing = sum(p['duration']['state'] == 'unavailable' for p in projections)\n", "    missing = 0\n    projections = [p for p in projections if p['duration']['state'] != 'unavailable']\n", 'sum silently skips unavailable attempts'),
 ('TIM-M4', 'm1-workflow-timing-subject-01', 'timing.py', "    if start_ns is None or end_ns is None:\n        return unavailable('clock-unavailable')\n", "    if start_ns is None or end_ns is None:\n        return {'state': 'measured', 'milliseconds': 0}\n", 'missing sample becomes zero'),
 # history
 ('HIS-M1', 'm1-history-selection-subject-01', 'history.py', "            or any(not valid_run_id(r) for r in run_ids) or len(set(run_ids)) != len(run_ids)):", "            or any(not valid_run_id(r) for r in run_ids)):", 'duplicates admitted'),
 ('HIS-M2', 'm1-history-selection-subject-01', 'history.py', "        if (type(value) is not dict or value.get('runId') != slot['runId'] or", "        if (type(value) is not dict or", 'lookup may return a different Run'),
 ('HIS-M3', 'm1-history-selection-subject-01', 'history.py', "'current-run' if rid == current_run_id else", "'current-run' if current_run_id is not None and rid[:12] == current_run_id[:12] else", 'prefix equality for current-run'),
 ('HIS-M4', 'm1-history-selection-subject-01', 'history.py', "        if value['state'] == 'unavailable' and value.get('availability') not in ('expired', 'purged', 'corrupt', 'unavailable'):\n            raise HistorySourceRefusal()\n", '', 'unknown availability tokens pass'),
]

results = []
for mid, subject, fname, old, new, desc in M:
    dst = WORK / mid
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT / subject, dst)
    text = (dst / fname).read_text()
    count = text.count(old)
    if count != 1:
        results.append({'id': mid, 'description': desc, 'applied': False, 'matches': count}); continue
    (dst / fname).write_text(text.replace(old, new))
    p = subprocess.run([PY, '-I', '-B', 'check.py'], cwd=dst, capture_output=True, text=True, timeout=300)
    failed = [l.split(' ')[0] for l in p.stderr.splitlines() if l.endswith('... FAIL') or l.endswith('... ERROR')]
    results.append({'id': mid, 'subject': subject, 'description': desc, 'applied': True, 'exit': p.returncode, 'killed': p.returncode != 0, 'failingTests': failed})
(HERE / 'mutant-results.json').write_text(json.dumps(results, indent=2) + '\n')
for r in results:
    print(r['id'], 'applied' if r.get('applied') else 'NOT-APPLIED', 'killed' if r.get('killed') else 'SURVIVED', r.get('failingTests', ''))

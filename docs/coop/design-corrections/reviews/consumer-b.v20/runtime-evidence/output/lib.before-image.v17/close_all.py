"""Close every Run in-process and print the first refusals. Diagnostic driver."""
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_closure as CL

RUNS = [('run_syntax_code_full', 'syntax-code'), ('run_ts_full', 'typescript'),
        ('run_rust_full', 'rust'), ('run_rust_partial', 'rust-partial'),
        ('run_syntax_data', 'syntax-data')]
bad = []
for mod_name, label in RUNS:
    mod = importlib.import_module(mod_name)
    if hasattr(mod, 'graph'):
        g = mod.graph()
    else:
        base = importlib.import_module(mod.BASE) if hasattr(mod, 'BASE') else mod
        g = mod.complete(base.build())
    c = CL.Closure(g['st'])
    rep = c.close_run(g['out']['runId'], label)
    print('%-14s admitted=%-5s passed=%-4d n/a=%-3d refused=%d'
          % (label, rep['admitted'], rep['checksPassed'], rep['checksNotApplicable'],
             rep['checksRefused']))
    seen = set()
    for r in rep['refusals']:
        if r['check'] in seen:
            continue
        seen.add(r['check'])
        print('     REFUSE', r['check'], '|', json.dumps(r['detail'])[:300])
    if not rep['admitted']:
        bad.append(label)
print()
print('runs not admitted:', bad)
sys.exit(1 if bad else 0)

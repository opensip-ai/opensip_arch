"""THE from-scratch command of this origin.

    /tmp/opensip-architecture-review-env/bin/python -I -B \
        /tmp/opensip-design-corrections/consumer-b.v17/output/lib/verify_all.py

It runs every stage in order against the frozen kit and the exported bytes, and exits nonzero
if any stage fails. Nothing here trusts a previous result: each Run is rebuilt, re-exported,
recomputed from its own exported bytes in a FRESH process, and re-controlled.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
PY = '/tmp/opensip-architecture-review-env/bin/python'

STAGES = [
    ('v17 kit custody: manifest, declared parent binding, byte-identity vs v16',
     ['verify_kit_v17.py']),
    ('phase 0 input custody', ['phase0.py']),
    ('phase 1 canonical / H / lexical', ['phase1.py']),
    ('phase 2 capability manifest admission', ['phase2.py']),
    ('phase 3 protocol traces', ['phase3_traces.py']),
    ('phase 4 relation/rung table', ['relation_table.py']),
    ('phase 4 count/class/attempt, code-vs-data, enum-vs-resolution', ['phase4.py']),
    ('phase 4 advertised mode paths', ['phase4_modes.py']),
    ('phase 5 all Runs: export + fresh-process replay + controls',
     ['all_runs.py', 'all']),
    ('phase 5 native annotated-site audit', ['audit_native_sites.py']),
    ('phase 5 native-join negative controls', ['negatives_native.py']),
    ('phase 5 hidden/mismatched input per language', ['negatives_hidden.py']),
    ('phase 5 policy admission controls incl. invalid DISABLED policy',
     ['negatives_policy.py']),
    ('phase 5 enumeration-contract controls (extents, kinds, unavailable bindings)',
     ['negatives_enumeration.py']),
    ('phase 6 configuration graphs', ['phase6_config.py']),
    ('phase 6 clone negatives, JS body through TS, min-resolution',
     ['phase6_clones.py']),
    ('phase 6 repair descriptor / authority / mutation keys', ['phase6_repair.py']),
    ('phase 6 imported-observation boundary + pinned purge', ['phase6_rest.py']),
    ('phase 7 workflows, envelopes, availability', ['phase7.py']),
    ('phase 8 baseline audit and comparisons', ['phase8.py']),
    ('phase 7 invocation step/result join controls', ['negatives_invocation.py']),
    ('phase 9 graph query', ['graph_query.py']),
    ('phase 9 relocation / transport equality', ['relocation_control.py']),
    ('phase 9 helper corrections record', ['helper_corrections.py']),
    ('control: every prior generation (v14/v15/v16) untouched',
     ['check_siblings_untouched.py']),
    ('control: census of any write this generation made under a prior generation',
     ['audit_v16_writes.py']),
    ('phase 10 design-gap identification', ['phase10.py']),
    ('requirement status derivation', ['status.py']),
    ('phase 11 deliverable', ['deliver.py']),
    ('requirement status re-derivation after the deliverable', ['status.py']),
    ('checkpoints for every phase', ['checkpoints_all.py']),
    ('deliverable rewritten against the final status', ['deliver.py']),
    ('progress record', ['progress_v17.py']),
]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows, failed = [], []
    for name, argv in STAGES:
        if only and only not in name and only not in argv[0]:
            continue
        t0 = time.time()
        p = subprocess.run([PY, '-I', '-B'] + [os.path.join(HERE, argv[0])] + argv[1:],
                           capture_output=True, text=True, cwd=HERE,
                           env=dict(os.environ, PYTHONPATH=HERE))
        dt = time.time() - t0
        ok = p.returncode == 0
        tail = (p.stdout or '').strip().splitlines()[-1:] or ['']
        rows.append({'stage': name, 'script': argv[0], 'exit': p.returncode,
                     'seconds': round(dt, 1), 'lastLine': tail[0][:160]})
        print('%-66s exit=%d %5.1fs %s' % (name[:66], p.returncode, dt, tail[0][:70]))
        if not ok:
            failed.append(name)
            print('  STDERR:', (p.stderr or '').strip().splitlines()[-6:])
    with open(OUT + '/verify-all.json', 'w') as f:
        json.dump({'command': ('%s -I -B %s/verify_all.py' % (PY, HERE)),
                   'stages': rows, 'failedStages': failed,
                   'allStagesPassed': not failed}, f, indent=1)
    print()
    print('%d stages, %d failed' % (len(rows), len(failed)))
    if failed:
        print('FAILED:', failed)
        sys.exit(1)


main()

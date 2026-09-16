"""THE from-scratch command of this origin.

    /tmp/opensip-architecture-review-env/bin/python -I -B \
        /tmp/opensip-design-corrections/consumer-b.v20/output/lib/verify_all.py

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
    ('literal path census of every copied module (run BEFORE any copied code)',
     ['census_v20.py']),
    ('generation-label provenance audit against the retained before-images',
     ['label_history_v20.py']),
    ('kit custody: manifest, declared parent binding, measured normative delta',
     ['verify_kit_v20.py']),
    ('write confinement and history standing (carries the open note-overwrite disclosure)',
     ['history_standing_v20.py']),
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
    # the three audit areas of this generation. Each is a NEW derivation written from the
    # published clauses and only then compared with the retained helpers, so it runs over the
    # exported stores AFTER the Runs are built, exported and replayed.
    ('audit area 1: independent enumeration program-binding derivation from the clauses',
     ['indep_enumeration_binding.py']),
    ('audit area 2: independent subject-inventory carrier derivation from the clauses',
     ['indep_subject_inventory.py']),
    ('audit area 2: carrier-pair discriminating controls', ['negatives_carrier.py']),
    ('audit area 3: independent ExecutionInputs receipt/account/outcome derivation',
     ['indep_execution_inputs.py']),
    ('audit area 3: ExecutionInputs discriminating controls (measured first refusals)',
     ['negatives_execution_inputs.py']),
    ('audit area 1: the three programEntry provenances incl. synthesized',
     ['programentry_law_v19.py']),
    ('S2: the portable glob contract, every required example measured',
     ['glob_law_v19.py']),
    ('S1: the unsafe-repair closed-world SELECTION LAW over retained records',
     ['repair_selection_v19.py']),
    ('whole published QUERY surface: 20 operations, actual records, owning-schema admission',
     ['indep_query_surface.py']),
    ('whole published MUTATION surface: records, identities, replay scope and key recipes',
     ['indep_mutation_surface.py']),
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
    ('path census re-run AFTER every stage, so a stage cannot have added a foreign write',
     ['census_v20.py']),
    ('write confinement and history standing re-checked', ['history_standing_v20.py']),
    ('kit custody RE-VERIFIED after reconstruction: every row, hash and size unchanged',
     ['verify_kit_v20.py']),
    ('generation-label provenance re-checked after every stage', ['label_history_v20.py']),
    ('phase 10 design-gap identification', ['phase10.py']),
    ('requirement status derivation', ['status.py']),
    ('phase 11 deliverable', ['deliver.py']),
    ('requirement status re-derivation after the deliverable', ['status.py']),
    ('checkpoints for every phase', ['checkpoints_all.py']),
    ('progress record', ['progress_v20.py']),
    # THE FINAL RECONCILIATION STAGE, and deliberately the last one: verify-all.json is rewritten
    # after EVERY stage, so when this stage runs it reads the record of every preceding stage of
    # THIS run. The one row it cannot contain is its own exit, which is appended after it returns.
    ('final reconciliation: review.md/json against the completed run', ['deliver.py']),
]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows, failed = [], []

    def record():
        with open(OUT + '/verify-all.json', 'w') as f:
            json.dump({'command': ('%s -I -B %s/verify_all.py' % (PY, HERE)),
                       'declaredStageCount': len(STAGES),
                       'stagesRecorded': len(rows),
                       'stages': rows, 'failedStages': failed,
                       'allStagesPassed': not failed,
                       'recordWriteRule': (
                           'rewritten after every stage, so the final reconciliation stage reads '
                           'the record of every preceding stage of this same run; its own exit '
                           'row is appended after it returns')}, f, indent=1)

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
        record()
    record()
    print()
    print('%d stages, %d failed' % (len(rows), len(failed)))
    if failed:
        print('FAILED:', failed)
        sys.exit(1)


main()

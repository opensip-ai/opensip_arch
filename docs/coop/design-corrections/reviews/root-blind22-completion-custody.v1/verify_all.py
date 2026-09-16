"""THE from-scratch command of this origin.

    /tmp/opensip-architecture-review-env/bin/python -I -B \
        /tmp/opensip-design-corrections/consumer-b.v22/output/lib/verify_all.py

It runs every stage in order against the frozen kit and the exported bytes, and exits nonzero
if any stage fails. Nothing here trusts a previous result: each Run is rebuilt, re-exported,
recomputed from its own exported bytes in a FRESH process, and re-controlled.

V22-D8: a stage may only READ an artifact whose producing stage already ran in THIS command.
Generation 20 ran the mutation-surface instrument before the repair-descriptor stage it reads,
the query-surface instrument before the availability vector it reads, and phase 7 before the
baseline audit it reads, so each of them consumed the PREVIOUS command's bytes. READS below is
the measured read graph (every `open(OUT + '/vectors|query|envelopes/...')` of a stage module),
and the command refuses to start if any reader is ordered before its producer.
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
     ['census_v22.py']),
    ('generation-label provenance audit against the retained before-images',
     ['label_history_v22.py', '--expect-current']),
    ('kit custody: manifest, declared parent binding, measured normative delta',
     ['verify_kit_v22.py']),
    ('write confinement and history standing (carries the open note-overwrite disclosure)',
     ['history_standing_v22.py']),
    ('phase 0 input custody', ['phase0.py']),
    ('phase 1 canonical / H / lexical', ['phase1.py']),
    ('phase 2 capability manifest admission', ['phase2.py']),
    ('phase 3 protocol traces', ['phase3_traces.py']),
    ('phase 4 relation/rung table', ['relation_table.py']),
    ('phase 5 all Runs: export + fresh-process replay + controls',
     ['all_runs.py', 'all']),
    # V22-D8: phase4.py and phase4_modes.py open runs/*.store.json; ordered before all_runs.py
    # (as in generations 16-20) they measured the previous command's Run bytes.
    ('phase 4 count/class/attempt, code-vs-data, enum-vs-resolution (over THIS command\'s Runs)',
     ['phase4.py']),
    ('phase 4 advertised mode paths (over THIS command\'s Runs)', ['phase4_modes.py']),
    ('phase 5 native annotated-site audit', ['audit_native_sites.py']),
    ('phase 5 native-join negative controls', ['negatives_native.py']),
    ('phase 5 hidden/mismatched input per language', ['negatives_hidden.py']),
    ('phase 5 policy admission controls incl. invalid DISABLED policy',
     ['negatives_policy.py']),
    ('phase 5 enumeration-contract controls (extents, kinds, unavailable bindings)',
     ['negatives_enumeration.py']),
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
    ('phase 6 configuration graphs', ['phase6_config.py']),
    ('phase 6 clone negatives, JS body through TS, min-resolution (atom level)',
     ['phase6_clones.py']),
    ('independent ATOM LAW (atom contract as frozen for generation 22) over every Run, the '
     'generation-20 predecessors, tamper controls, law vectors and the min-resolution vector',
     ['indep_atom_law.py']),
    ('phase 6 repair descriptor / authority / mutation keys', ['phase6_repair.py']),
    ('whole published MUTATION surface: records, identities, replay scope and key recipes',
     ['indep_mutation_surface.py']),
    ('phase 6 imported-observation boundary + pinned purge', ['phase6_rest.py']),
    ('phase 8 baseline audit and comparisons', ['phase8.py']),
    ('phase 7 workflows, envelopes, availability', ['phase7.py']),
    ('phase 7 invocation step/result join controls', ['negatives_invocation.py']),
    ('whole published QUERY surface: 20 operations, actual records, owning-schema admission',
     ['indep_query_surface.py']),
    ('phase 9 graph query', ['graph_query.py']),
    ('phase 9 relocation / transport equality', ['relocation_control.py']),
    ('phase 9 helper corrections record', ['helper_corrections.py']),
    ('path census re-run AFTER every stage, so a stage cannot have added a foreign write',
     ['census_v22.py']),
    ('write confinement and history standing re-checked', ['history_standing_v22.py']),
    ('kit custody RE-VERIFIED after reconstruction: every row, hash and size unchanged',
     ['verify_kit_v22.py']),
    ('generation-label provenance re-checked after every stage',
     ['label_history_v22.py', '--expect-current']),
    ('phase 10 design-gap identification', ['phase10.py']),
    ('MEASURED read graph of every stage so far (audit-hook logs of this command)',
     ['read_graph_v22.py']),
    ('CLAIMED-POSITIVE AUDIT: every original and supplemental positive re-checked from its final '
     'bytes in a fresh process, with its evidence class', ['audit_claimed_positives.py']),
    ('requirement status derivation', ['status.py']),
    # V22-D11: checkpoints are written BEFORE the draft deliverable, whose digest table reads them
    ('checkpoints for every phase (pre-deliverable)', ['checkpoints_all.py', '--pre-deliverable']),
    ('phase 11 deliverable', ['deliver.py']),
    ('requirement status re-derivation after the deliverable', ['status.py']),
    ('checkpoints for every phase', ['checkpoints_all.py']),
    ('progress record', ['progress_v22.py']),
    ('MEASURED read graph re-checked over every stage before the final reconciliation',
     ['read_graph_v22.py']),
    # THE FINAL RECONCILIATION STAGE, and deliberately the last one: verify-all.json is rewritten
    # after EVERY stage, so when this stage runs it reads the record of every preceding stage of
    # THIS run. The one row it cannot contain is its own exit, which is appended after it returns.
    ('final reconciliation: review.md/json against the completed run', ['deliver.py']),
]

# reader module -> producer modules whose artifacts it opens
_ALL_RUN_READERS = ('indep_enumeration_binding.py', 'indep_subject_inventory.py',
                    'indep_execution_inputs.py', 'repair_selection_v19.py', 'phase6_clones.py',
                    'phase6_rest.py', 'relocation_control.py')
READS = {
    'history_standing_v22.py': ['census_v22.py'],
    'indep_mutation_surface.py': ['phase6_repair.py', 'all_runs.py'],
    'indep_query_surface.py': ['phase7.py', 'phase8.py', 'all_runs.py'],
    'phase7.py': ['phase8.py', 'negatives_policy.py', 'phase6_repair.py', 'phase4.py',
                  'all_runs.py'],
    'negatives_invocation.py': ['phase7.py'],
    'indep_atom_law.py': ['phase6_clones.py', 'all_runs.py'],
    'phase6_repair.py': ['all_runs.py'],
    'phase8.py': ['all_runs.py', 'phase6_repair.py', 'negatives_native.py'],
    'phase4.py': ['all_runs.py'],
    'phase4_modes.py': ['all_runs.py'],
    'graph_query.py': ['all_runs.py'],
    'phase10.py': ['programentry_law_v19.py'],
    'audit_claimed_positives.py': ['census_v22.py', 'verify_kit_v22.py', 'history_standing_v22.py',
                                   'phase0.py', 'phase1.py', 'phase2.py', 'phase3_traces.py',
                                   'relation_table.py', 'all_runs.py', 'phase4.py',
                                   'phase4_modes.py', 'negatives_native.py', 'negatives_hidden.py',
                                   'negatives_policy.py', 'negatives_enumeration.py',
                                   'indep_execution_inputs.py', 'negatives_carrier.py',
                                   'negatives_execution_inputs.py', 'programentry_law_v19.py',
                                   'glob_law_v19.py', 'repair_selection_v19.py',
                                   'phase6_config.py', 'phase6_clones.py', 'indep_atom_law.py',
                                   'phase6_repair.py', 'indep_mutation_surface.py',
                                   'phase6_rest.py', 'phase8.py', 'phase7.py',
                                   'negatives_invocation.py', 'indep_query_surface.py',
                                   'graph_query.py', 'relocation_control.py',
                                   'helper_corrections.py', 'phase10.py', 'read_graph_v22.py'],
    'status.py': ['audit_claimed_positives.py', 'deliver.py'],
    'checkpoints_all.py': ['helper_corrections.py', 'status.py'],
    'progress_v22.py': ['audit_claimed_positives.py', 'deliver.py', 'helper_corrections.py',
                        'history_standing_v22.py', 'indep_atom_law.py', 'phase10.py', 'status.py',
                        'verify_kit_v22.py'],
}
for _m in _ALL_RUN_READERS:
    READS.setdefault(_m, []).append('all_runs.py')
# the deliverable digests every exported artifact, so it reads the output of every producer
READS['deliver.py'] = sorted(({p for v in READS.values() for p in v}
                              | {'audit_claimed_positives.py', 'status.py', 'checkpoints_all.py',
                                 'label_history_v22.py', 'audit_native_sites.py',
                                 'indep_enumeration_binding.py', 'indep_subject_inventory.py',
                                 'read_graph_v22.py'}) - {'deliver.py'})


def order_guard():
    """static half: a reader's LAST occurrence must follow its producer's FIRST occurrence (a
    stage run twice, like status.py, reads the deliverable only on its second run). The measured
    half is read_graph_v22.py, which checks every actual read of every occurrence."""
    first, last = {}, {}
    for i, (_name, argv) in enumerate(STAGES):
        first.setdefault(argv[0], i)
        last[argv[0]] = i
    bad = []
    for reader, producers in READS.items():
        for p in producers:
            if reader not in last or p not in first or first[p] >= last[reader]:
                bad.append({'reader': reader, 'producer': p,
                            'readerStage': last.get(reader), 'producerStage': first.get(p)})
    return bad


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows, failed = [], []
    bad_order = order_guard()
    # fresh receipt directory per command: earlier commands' stage logs are never overwritten
    io_dir = os.path.join(OUT, 'notes', 'v22-stage-io', time.strftime('%Y%m%dT%H%M%S')
                          + ('-only-' + only if only else ''))

    def record():
        # the per-command receipt beside the stage logs is never overwritten by a later command;
        # verify-all.json is the CURRENT command's record
        os.makedirs(io_dir, exist_ok=True)
        for path in (OUT + '/verify-all.json', os.path.join(io_dir, 'verify-all.receipt.json')):
            _record_to(path)

    def _record_to(path):
        with open(path, 'w') as f:
            json.dump({'command': ('%s -I -B %s/verify_all.py' % (PY, HERE)),
                       'stageIoDir': io_dir,
                       'stageLauncher': ('every stage runs as __main__ under '
                                         'stage_launcher_v22.py, whose audit hook logs its opens '
                                         'under output/ (child processes not hooked)'),
                       'declaredStageCount': len(STAGES),
                       'stagesRecorded': len(rows),
                       'stages': rows, 'failedStages': failed,
                       'allStagesPassed': not failed and not bad_order,
                       'readOrderGuard': {'reads': READS, 'violations': bad_order},
                       'recordWriteRule': (
                           'rewritten after every stage, so the final reconciliation stage reads '
                           'the record of every preceding stage of this same run; its own exit '
                           'row is appended after it returns')}, f, indent=1)

    if bad_order:
        record()
        print('READ-ORDER GUARD REFUSED:', json.dumps(bad_order))
        sys.exit(1)
    for index, (name, argv) in enumerate(STAGES):
        if only and only not in name and only not in argv[0]:
            continue
        t0 = time.time()
        p = subprocess.run([PY, '-I', '-B', os.path.join(HERE, 'stage_launcher_v22.py'),
                            str(index)] + argv,
                           capture_output=True, text=True, cwd=HERE,
                           env=dict(os.environ, PYTHONPATH=HERE, OPENSIP_STAGE_IO_DIR=io_dir))
        dt = time.time() - t0
        ok = p.returncode == 0
        tail = (p.stdout or '').strip().splitlines()[-1:] or ['']
        rows.append({'stage': name, 'script': argv[0], 'argv': argv[1:], 'exit': p.returncode,
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

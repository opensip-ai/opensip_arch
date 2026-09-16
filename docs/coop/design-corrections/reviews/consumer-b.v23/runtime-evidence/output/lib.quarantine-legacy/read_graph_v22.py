"""MEASURED read graph of the from-scratch command (generation 22, V22-D8).

verify_all.py carries a static READS table and refuses to start when a reader is ordered before
its producer. A static table can itself be wrong: the generation-22 draft table did not list that
phase4.py and phase4_modes.py open runs/*.store.json, and both were ordered BEFORE the stage that
rebuilds those Runs, so they measured the PREVIOUS command's Run bytes. This stage reads the audit-
hook logs written by stage_launcher_v22.py for every stage of THIS command so far and refuses when:

  ORDER      a stage reads an artifact that no earlier stage (and not the same stage, earlier in its
             own log) wrote in this command, while a LATER stage writes it;
  UNDECLARED a measured stage-to-stage read edge is missing from verify_all.READS;
  UNKNOWN    a stage reads an artifact that no stage of the command writes and that is not a
             declared one-shot retained note (the confinement/rebind/predecessor records written
             once, before the command, by the generation-22 preparation tools).

Child processes are not hooked (disclosed in each log); their reads are not in this graph.
"""
import ast
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
OUT = os.path.dirname(HERE)
# retained one-shot or historical bytes that no stage of the command writes, BY DESIGN: the
# before-images and quarantined legacy tools (read by the census and the label audit), the
# generation-22 rebind record and predecessor copies, this origin's own historical notes of
# generations 14-20 (read as history, never as current results), and the command record itself.
ONE_SHOT_PREFIXES = ('notes/v22-rebind.json', 'notes/v22-command-attempts.json',
                     'predecessors.v20/', 'lib.before-image.',
                     'lib.quarantine-legacy/', 'notes/prior-generation-writes.json',
                     'notes/siblings-untouched.json', 'notes/cp-spec-', 'notes/v14-', 'notes/v15-',
                     'notes/v16-', 'notes/v17-', 'notes/v18-', 'notes/v19-', 'notes/v20-',
                     'previous-turn-response.md', 'verify-all.json', 'notes/v22-stage-io/')


def declared_reads(va):
    """the EFFECTIVE table the command guarded with, as recorded in verify-all.json (the module
    extends its literal READS after the assignment, so parsing the literal alone is incomplete)"""
    return (va.get('readOrderGuard') or {}).get('reads') or {}


def main():
    va = json.load(open(OUT + '/verify-all.json'))
    io_dir = va['stageIoDir']
    # stage logs only (NNN-script.json); the per-command receipt beside them is not a stage log
    logs = sorted((json.load(open(p)) for p in glob.glob(os.path.join(io_dir, '[0-9][0-9][0-9]-*.json'))),
                  key=lambda l: l['stageIndex'])
    writes = {}
    for l in logs:
        for e in l['events']:
            if e['op'] == 'write':
                # a child-process write (post-stage snapshot) has no measured order inside its
                # stage, so it satisfies any read of the same stage (seq -1); an in-process write
                # is ordered by the hook
                seq = -1 if e.get('source') == 'post-stage-snapshot' else e['seq']
                writes.setdefault(e['artifact'], []).append((l['stageIndex'], seq, l['script']))
    declared = declared_reads(va)
    edges, order, undeclared, unknown, one_shot = {}, [], [], [], set()
    for l in logs:
        i, me = l['stageIndex'], l['script']
        for e in l['events']:
            if e['op'] != 'read':
                continue
            a = e['artifact']
            ws = writes.get(a, [])
            earlier = [w for w in ws if w[0] < i or (w[0] == i and w[1] < e['seq'])]
            if earlier:
                prod = earlier[-1][2]
                if prod != me:
                    edges.setdefault((me, prod), set()).add(a)
                continue
            later = [w for w in ws if w[0] > i or (w[0] == i and w[1] > e['seq'])]
            if later:
                order.append({'readerStage': i, 'reader': me, 'artifact': a,
                              'laterWriterStage': later[0][0], 'laterWriter': later[0][2]})
            elif a.startswith(ONE_SHOT_PREFIXES):
                one_shot.add(a)
            else:
                unknown.append({'readerStage': i, 'reader': me, 'artifact': a})
    for (reader, prod), arts in sorted(edges.items()):
        if prod not in declared.get(reader, []):
            undeclared.append({'reader': reader, 'producer': prod, 'artifacts': sorted(arts)[:6]})
    doc = {'standing': __doc__, 'commandStageIoDir': io_dir, 'stagesLogged': len(logs),
           'edges': [{'reader': r, 'producer': p, 'artifacts': sorted(a)}
                     for (r, p), a in sorted(edges.items())],
           'orderViolations': order, 'undeclaredEdges': undeclared,
           'readsOfArtifactsNoStageWrote': unknown,
           'oneShotRetainedNotesRead': sorted(one_shot),
           'result': 'PASS' if not (order or undeclared or unknown) else 'REFUSE'}
    with open(OUT + '/notes/v22-read-graph.json', 'w') as fh:
        json.dump(doc, fh, indent=1)
    print('measured read graph over %d stages: %d edges, %d order violations, %d undeclared, '
          '%d unknown reads' % (len(logs), len(edges), len(order), len(undeclared), len(unknown)))
    for x in order[:20]:
        print('  ORDER', x)
    for x in undeclared[:40]:
        print('  UNDECLARED', x)
    for x in unknown[:20]:
        print('  UNKNOWN', x)
    sys.exit(0 if doc['result'] == 'PASS' else 1)


if __name__ == '__main__':
    main()

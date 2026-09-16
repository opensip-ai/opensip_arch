"""Stage launcher (generation 22): runs ONE stage module as __main__ under a CPython audit hook
that records every open() of a path under this runtime's output/ (lib/ excluded), so the read
graph of the from-scratch command is MEASURED rather than declared (V22-D8).

    python -I -B stage_launcher_v22.py <stageIndex> <script> [args...]

The log is written to $OPENSIP_STAGE_IO_DIR/<stageIndex>-<script>.json after the stage returns
(normally, by SystemExit, or by an exception, which still propagates). Child processes a stage
spawns (the Run builders and fresh-process replays) are NOT hooked, so their READS are not in the
log. Their WRITES are: the output tree's (mtime, size) is snapshotted before and after the stage,
and every created or changed file not already logged by the hook is added as a
`post-stage-snapshot` write, whose order inside the stage is not measured.
"""
import json
import os
import runpy
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
OUT = os.path.dirname(HERE)
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND


def snapshot():
    out = {}
    for dp, dns, fns in os.walk(OUT):
        rel_dp = os.path.relpath(dp, OUT)
        if rel_dp == '.':
            dns[:] = [d for d in dns if not d.startswith('lib') and d != 'predecessors.v20']
        elif rel_dp == 'notes':
            dns[:] = [d for d in dns if d != 'v22-stage-io']
        for f in fns:
            p = os.path.join(dp, f)
            try:
                st = os.stat(p)
            except OSError:
                continue
            out[os.path.relpath(p, OUT)] = (st.st_mtime_ns, st.st_size)
    return out


def main():
    index, script, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    before = snapshot()
    target = os.path.join(HERE, script)
    events, first = [], {}
    state = {'on': True}

    def hook(event, a):
        if event != 'open' or not state['on']:
            return
        path, mode, flags = a
        if not isinstance(path, str):
            return
        state['on'] = False
        try:
            p = os.path.realpath(path)
            if not p.startswith(OUT + os.sep) or p.startswith(HERE + os.sep):
                return
            rel = os.path.relpath(p, OUT)
            if isinstance(mode, str):
                op = 'write' if any(c in mode for c in 'wax+') else 'read'
            else:
                op = 'write' if (flags or 0) & WRITE_FLAGS else 'read'
            if (op, rel) not in first:
                first[(op, rel)] = len(events)
                events.append({'seq': len(events), 'op': op, 'artifact': rel})
        finally:
            state['on'] = True

    sys.argv = [target] + args
    sys.addaudithook(hook)
    outcome = {'kind': 'exception'}
    try:
        runpy.run_path(target, run_name='__main__')
        outcome = {'kind': 'returned'}
    except SystemExit as e:
        outcome = {'kind': 'SystemExit', 'code': e.code if isinstance(e.code, int) else str(e.code)}
        raise
    except BaseException as e:
        outcome = {'kind': 'exception', 'type': type(e).__name__, 'message': str(e)[:300]}
        raise
    finally:
        state['on'] = False
        after = snapshot()
        for rel in sorted(after):
            if after[rel] != before.get(rel) and ('write', rel) not in first:
                first[('write', rel)] = len(events)
                events.append({'seq': len(events), 'op': 'write', 'artifact': rel,
                               'source': 'post-stage-snapshot'})
        d = os.environ.get('OPENSIP_STAGE_IO_DIR')
        if d:
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, '%03d-%s.json' % (int(index), script)), 'w') as fh:
                json.dump({'stageIndex': int(index), 'script': script, 'argv': args,
                           'outcome': outcome, 'events': events,
                           'childProcessesHooked': False}, fh, indent=1)


if __name__ == '__main__':
    main()

"""Locate the per-run varying fields of output/blind-review.json.

Two consecutive fresh-process commands with NO source edit between them
produced different blind-review.json bytes, so some field is per-run rather
than content-derived.  This instrument snapshots the file on first use and, on
the next use, reports exactly which JSON paths differ.  It deliberately writes
under the generation-20 runtime but OUTSIDE output/, so that taking the
diagnostic does not itself perturb the exported artifact tree.
"""
import json
import os
import sys

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v20'
LIVE = os.path.join(RUNTIME, 'output', 'blind-review.json')
SNAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blind-review.snapshot.json')


def flatten(node, path='$', out=None):
    out = {} if out is None else out
    if isinstance(node, dict):
        for key, value in node.items():
            flatten(value, '%s.%s' % (path, key), out)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            flatten(value, '%s[%d]' % (path, i), out)
    else:
        out[path] = node
    return out


def main():
    with open(LIVE, 'rb') as fh:
        live_bytes = fh.read()
    if not os.path.exists(SNAP):
        with open(SNAP, 'wb') as fh:
            fh.write(live_bytes)
        print('snapshot taken (%d bytes). Re-run the command, then run this again.'
              % len(live_bytes))
        return 0

    with open(SNAP, 'rb') as fh:
        snap_bytes = fh.read()
    if snap_bytes == live_bytes:
        print('IDENTICAL BYTES: blind-review.json is reproducible across commands.')
        return 0

    a = flatten(json.loads(snap_bytes))
    b = flatten(json.loads(live_bytes))
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    print('differing leaf paths : %d' % len(changed))
    for key in changed[:60]:
        print('  %s\n      snapshot %s\n      now      %s'
              % (key, repr(a[key])[:110], repr(b[key])[:110]))
    print('paths only in snapshot: %d %s' % (len(only_a), only_a[:10]))
    print('paths only in current : %d %s' % (len(only_b), only_b[:10]))
    return 0


if __name__ == '__main__':
    sys.exit(main())

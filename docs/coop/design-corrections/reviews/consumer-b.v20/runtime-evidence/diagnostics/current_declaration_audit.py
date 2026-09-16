"""Audit every CURRENT self-declaration in the exported artifacts.

The generation-20 rebind rewrites PATH FORM ONLY, which is right for historical
narrative (V18-D6 / V19-D1) but means a hand-written CURRENT declaration -- "who
am I", "what was I given", "what did THIS session do" -- can silently keep a
prior generation's label.  This instrument lists every artifact field whose KEY
marks it as a current self-declaration and whose VALUE names a generation other
than 20, so each one can be judged by reading it.  Writes nothing under output/.
"""
import json
import os
import re

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
GEN = re.compile(r'(?:consumer-b\.)?v(1[4-9])\b|generation[- ](1[4-9])\b')

# Keys that declare something about the CURRENT origin / session / input, as opposed to
# keys that carry history on purpose.
CURRENT_KEY = re.compile(
    r'^(consumerId|generation|currentGeneration|inputKit|thisSession|thisGeneration|'
    r'receiptPrefix|selfId|origin|runtime|outputRoot|writeRoot|sessionId)$')
HISTORY_KEY = re.compile(
    r'ancestry|historic|prior|before|Prior|Before|overwrit|provenance|originalFailure|'
    r'whichReadingWon|disposition|executionStandingWhenFirstRecorded|correction|'
    r'narrative|census|damage', re.I)


def walk(node, path='$', parent_keys=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk(value, '%s.%s' % (path, key), parent_keys + (key,))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from walk(value, '%s[%d]' % (path, i), parent_keys)
    elif isinstance(node, str):
        yield path, parent_keys, node


RETAINED_NAME = re.compile(r'v1[4-9]')


def written_this_session():
    """Artifacts the CURRENT command rewrote, by mtime against this session's first write."""
    with open(os.path.join(OUT, 'notes', 'v20-history-standing.json'), encoding='utf-8') as fh:
        standing = json.load(fh)
    import calendar
    import time
    stamp = standing['measuredC_priorGenerations']['firstWriteOfThisSessionUtc']
    return calendar.timegm(time.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ')) - 60


def main():
    cutoff = written_this_session()
    hits = []
    for base, dirs, names in os.walk(OUT):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'lib', 'lib.before-image.v19')]
        for name in sorted(names):
            if not name.endswith('.json'):
                continue
            # A retained prior-generation artifact declaring its OWN generation is correct;
            # only what this command itself wrote can be a stale current declaration.
            if RETAINED_NAME.search(name) or os.path.getmtime(
                    os.path.join(base, name)) < cutoff:
                continue
            rel = os.path.relpath(os.path.join(base, name), OUT)
            try:
                with open(os.path.join(base, name), encoding='utf-8') as fh:
                    doc = json.load(fh)
            except (ValueError, OSError):
                continue
            for path, keys, value in walk(doc):
                if not GEN.search(value):
                    continue
                leaf = keys[-1] if keys else ''
                if not CURRENT_KEY.match(leaf):
                    continue
                if any(HISTORY_KEY.search(k) for k in keys):
                    continue
                # Census/inventory ROWS carry the generation of the file each occurrence sits
                # in; that is the row's subject, not a self-declaration.
                if any('ccurrence' in k or k in ('rows', 'files', 'trees') for k in keys):
                    continue
                hits.append((rel, path, value[:120]))

    print('current-declaration fields naming a generation other than 20: %d' % len(hits))
    for rel, path, value in hits:
        print('  %-44s %s = %r' % (rel, path, value))


if __name__ == '__main__':
    main()

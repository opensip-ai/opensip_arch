"""Read-only resolution of EVERY digest quoted by the two final reports.

Builds sha256 -> path indexes for this generation's own output tree and for the
supplied subject kit, then classifies every 64-hex digest appearing in
blind-review.json and blind-review.md as: resolves to a current own artifact,
resolves to a supplied input file, a declared manifest/parent digest, a digest
this origin itself disclosed as HISTORICAL (prior-generation bytes), or
unresolved.  Unresolved current-byte claims would mean the reports are stale.
Writes nothing.
"""
import hashlib
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = os.path.join(RUNTIME, 'output')
SUBJECT = os.path.join(RUNTIME, 'subject')
HEX = re.compile(r'[0-9a-f]{64}')


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def index(root):
    out = {}
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
        for name in names:
            path = os.path.join(base, name)
            try:
                out.setdefault(sha(path), os.path.relpath(path, root))
            except OSError:
                pass
    return out


def walk_strings(node, path='$'):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, path + '.' + key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from walk_strings(value, path + '[%d]' % i)
    elif isinstance(node, str):
        yield path, node


def main():
    own = index(OUT)
    kit = index(SUBJECT)
    with open(os.path.join(OUT, 'blind-review.json'), encoding='utf-8') as fh:
        review = json.load(fh)

    # Digests this origin deliberately quotes as prior-generation bytes.
    historical_markers = ('prior', 'Prior', 'before', 'Before', 'v19', 'V19', 'v18', 'V18',
                          'v17', 'V17', 'v16', 'V16', 'ancestry', 'Ancestry', 'historical',
                          'Historical', 'overwritten', 'parent', 'Parent')

    buckets = {'own-artifact': 0, 'supplied-input': 0, 'declared-manifest': 0,
               'disclosed-historical': 0, 'unresolved-current-claim': []}
    manifest_digests = {review['inputKit']['subjectManifestSha256'],
                        review['inputKit']['parentSubjectSha256DeclaredInThatManifest']}

    for jpath, value in walk_strings(review):
        for digest in HEX.findall(value):
            if digest in own:
                buckets['own-artifact'] += 1
            elif digest in kit:
                buckets['supplied-input'] += 1
            elif digest in manifest_digests:
                buckets['declared-manifest'] += 1
            elif any(m in jpath for m in historical_markers):
                buckets['disclosed-historical'] += 1
            else:
                buckets['unresolved-current-claim'].append((jpath, digest[:16]))

    print('== blind-review.json digest resolution ==')
    for key in ('own-artifact', 'supplied-input', 'declared-manifest', 'disclosed-historical'):
        print('  %-24s %d' % (key, buckets[key]))
    unresolved = buckets['unresolved-current-claim']
    print('  %-24s %d' % ('unresolved', len(unresolved)))
    for jpath, digest in unresolved[:25]:
        print('    %s = %s...' % (jpath, digest))

    with open(os.path.join(OUT, 'blind-review.md'), encoding='utf-8') as fh:
        md = fh.read()
    print('== blind-review.md digest resolution ==')
    for digest in sorted(set(HEX.findall(md))):
        where = ('own artifact %s' % own[digest]) if digest in own else (
            'supplied input %s' % kit[digest]) if digest in kit else (
            'declared manifest/parent' if digest in manifest_digests else 'NOT A CURRENT FILE')
        # show the line it sits on, trimmed, so historical quotes are visible
        line = next((l.strip() for l in md.splitlines() if digest in l), '')
        print('  %s... %-28s | %s' % (digest[:16], where, line[:110]))


if __name__ == '__main__':
    main()

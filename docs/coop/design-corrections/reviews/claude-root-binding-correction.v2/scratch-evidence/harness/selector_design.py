"""Design + exhaustive differential proof for the corrected F-04 selectors.

THE STATED LAW is not restated by me: it is the decision procedure the house already
implements identically in two independent places on frozen25 --

  foundation/identity-model.v3.py `ordered()` line 138 / 147:
      child.startswith('/') or '\\\\' in child or '\\x00' in child
      or any(x in ['', '.', '..'] for x in child.split('/'))

  discovery-defaults.py `normalize_explicit_root()` line 77-81:
      spec.startswith('/') or '\\\\' in spec or '\\x00' in spec ... then
      any(seg in ('', '.', '..') for seg in body.split('/'))

Both SPLIT ON '/' and test EXACT segment equality. Neither excludes any other character
(newlines are permitted inside a segment) and neither imposes a per-segment length cap.
identity-schemas.v3 #/$defs/LogicalPath records that the declarative 255-per-segment bound
is a DIFFERENT, explicitly non-equivalent enforcement that applies to two Blob path fields,
so it is deliberately NOT imported here.
"""
import itertools
import json
import re
import sys

NUL = '\\u0000'
BS = '\\\\'
# One segment: not exactly '.' or '..' (decided at the segment boundary, with a STRICT
# end-of-input test rather than '$', which matches before a trailing newline), then one or
# more characters that are not NUL, backslash or '/'.
SEG = '(?!\\.\\.?(?:/|(?![\\s\\S])))[^' + NUL + BS + '/]+'
DIR = '^' + SEG + '(/' + SEG + ')*(?![\\s\\S])'
ROOT = '^(?:|' + SEG + '(/' + SEG + ')*)(?![\\s\\S])'

# v1 (defective) patterns, for the before/after differential
V1_DIR = '^(?!.*(^|/)\\.\\.?(/|$))[^' + NUL + BS + '/]+(/[^' + NUL + BS + '/]+)*(?![\\s\\S])'
V1_ROOT = '^(?:|(?!.*(^|/)\\.\\.?(/|$))[^' + NUL + BS + '/]+(/[^' + NUL + BS + '/]+)*)(?![\\s\\S])'


def law_dir(v):
    """Reference implementation of the STATED law for a non-empty internal directory."""
    if v == '':
        return False
    if v.startswith('/') or '\\' in v or '\x00' in v:
        return False
    return not any(s in ('', '.', '..') for s in v.split('/'))


def law_root(v):
    return v == '' or law_dir(v)


def report(tag, rx_dir, rx_root, corpus):
    d = re.compile(rx_dir)
    r = re.compile(rx_root)
    bad = []
    for v in corpus:
        if bool(d.search(v)) != law_dir(v):
            bad.append(('CanonicalRelativeDirV1', v, bool(d.search(v)), law_dir(v)))
        if bool(r.search(v)) != law_root(v):
            bad.append(('InternalUnitRootV1', v, bool(r.search(v)), law_root(v)))
    return bad


def main():
    alphabet = ['a', '.', '/', '\n', '\\', '\x00']
    corpus = ['']
    for n in range(1, 6):
        for t in itertools.product(alphabet, repeat=n):
            corpus.append(''.join(t))
    extra = ['a\n/../b', 'a\n/./b', 'a/.\n', 'a/..\n', 'a\n/b', 'a/b',
             'crates/foo#bar', '.hidden', 'a/.hidden', '..a', 'a..', 'a b',
             'deep/a/b/c/d', '\n', '\n/\n', '...', 'a/...', '.\n/b', '..\n/b',
             '\r', 'a\r/../b', 'a /../b', 'a/b\n']
    corpus.extend(extra)
    print('corpus size:', len(corpus))
    print()
    print('CORRECTED SEG :', SEG)
    print('CORRECTED DIR :', DIR)
    print('CORRECTED ROOT:', ROOT)
    print()

    v1bad = report('v1', V1_DIR, V1_ROOT, corpus)
    newbad = report('new', DIR, ROOT, corpus)
    print('v1 selectors  : disagreements with the stated law =', len(v1bad))
    print('new selectors : disagreements with the stated law =', len(newbad))
    print()
    seen = set()
    shown = 0
    print('sample v1 disagreements (deduplicated by kind):')
    for sel, v, got, want in v1bad:
        kind = (sel, got, want)
        if kind in seen:
            continue
        seen.add(kind)
        print('   %-24s %-14s regex=%-6s law=%-6s segments=%s'
              % (sel, repr(v), got, want, v.split('/')))
        shown += 1
    for sel, v, got, want in newbad[:20]:
        print('   NEW DISAGREEMENT', sel, repr(v), got, want)

    json.dump({'standing': 'Exhaustive differential of the corrected F-04 selectors against the '
                           'stated law as implemented by identity-model ordered() and '
                           'discovery-defaults normalize_explicit_root.',
               'corpusSize': len(corpus),
               'segPattern': SEG, 'dirPattern': DIR, 'rootPattern': ROOT,
               'v1DirPattern': V1_DIR, 'v1RootPattern': V1_ROOT,
               'v1Disagreements': len(v1bad), 'newDisagreements': len(newbad),
               'v1DisagreementSamples': [{'selector': s, 'value': v, 'regex': g, 'law': w}
                                         for s, v, g, w in v1bad[:40]]},
              open(sys.argv[1], 'w'), indent=1)
    return 0 if not newbad else 1


if __name__ == '__main__':
    raise SystemExit(main())

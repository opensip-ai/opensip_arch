"""P3: search the FROZEN v32 source for published law governing each observed difference."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'

SKIP_DIRS = ('/reviews/', '/.git/')


def corpus():
    for dp, dirs, fs in os.walk(ROOT32):
        if any(s in dp + '/' for s in SKIP_DIRS):
            dirs[:] = []
            continue
        for n in fs:
            if not n.endswith(('.md', '.json', '.py')):
                continue
            p = os.path.join(dp, n)
            if os.path.getsize(p) > 12_000_000:
                continue
            try:
                yield os.path.relpath(p, ROOT32), open(p, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue


FILES = list(corpus())
print('corpus files:', len(FILES))


def search(label, pattern, flags=re.I):
    rx = re.compile(pattern, flags)
    hits = []
    for rel, text in FILES:
        for m in rx.finditer(text):
            ln = text[:m.start()].count('\n') + 1
            line = text.splitlines()[ln - 1].strip()
            hits.append({'file': rel, 'line': ln, 'text': line[:300]})
    print('\n=== %s : %d hits' % (label, len(hits)))
    for h in hits[:14]:
        print('   %s:%d  %s' % (h['file'], h['line'], h['text'][:200]))
    return {'label': label, 'pattern': pattern, 'hitCount': len(hits), 'hits': hits[:60]}


out = {'standing': 'read-only normative search over frozen v32, reviews excluded',
       'corpusFiles': len(FILES), 'searches': []}

# CLASS A: is the account sourceUniverse for a non-supported applicability published?
out['searches'].append(search(
    'A1 account sourceUniverse tied to applicability',
    r'sourceUniverse[^\n]{0,160}(inapplicable|unsupported-typed|unavailable-unselected|unavailable-null)'))
out['searches'].append(search(
    'A2 inapplicable-vcs mentions',
    r'inapplicable-vcs'))
out['searches'].append(search(
    'A3 account universe must equal binding U',
    r"(account|accounts)[^\n]{0,120}sourceUniverse[^\n]{0,120}(equal|must)"))

# CLASS B: precedence between matrix-unsupported and unselected / null universe
out['searches'].append(search(
    'B1 precedence words near applicability',
    r'(precede|precedence|takes priority|first match|ordered before|before the)[^\n]{0,160}(applicab|unsupported|unselected)'))
out['searches'].append(search(
    'B2 unavailable-unselected mentions',
    r'unavailable-unselected'))
out['searches'].append(search(
    'B3 unsupported-typed mentions in contracts only',
    r'unsupported-typed'))

# CLASS D: matrix authority over produced Coverage
out['searches'].append(search(
    'D1 unsupported capability must not mint coverage',
    r'(UNSUPPORTED-TYPED)[^\n]{0,200}'))

json.dump(out, open(os.path.join(HERE, 'p3-normative.json'), 'w'), indent=2)
print('\nWROTE p3-normative.json')

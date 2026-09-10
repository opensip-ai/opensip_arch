"""Broad, CASE-INSENSITIVE rescan for the false causal rationale, tree-wide. My v5 miss came from a
narrow CamelCase pattern, so this matches the concept rather than one spelling. Limit: pattern
matching; absence of a match is not proof of consistency."""
import json, pathlib, re
W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v6/work')
# any assertion tying an inability to decide/branch to the relation being a non-enum string type
RX = re.compile(r'(cannot|can\s*not|unable to|does not)[^.]{0,120}?'
                r'(decide|branch|constrain|distinguish)[^.]{0,160}?'
                r'(not an enum|rather than an enum|canonical\s*identifier|broader string)'
                r'|(not an enum|rather than an enum)[^.]{0,120}?(so|therefore|because)[^.]{0,120}?'
                r'(cannot|no keyword|not decidable)', re.I | re.S)
hits, n = [], 0
for p in W.rglob('*'):
    if not p.is_file() or '/reviews/' in str(p) or p.suffix not in ('.md', '.json', '.py'):
        continue
    try:
        t = p.read_text(encoding='utf-8')
    except Exception:
        continue
    n += 1
    for m in RX.finditer(t):
        hits.append({'file': str(p.relative_to(W)),
                     'excerpt': t[max(0, m.start()-90):m.end()+90].replace('\n', ' ')})
print(json.dumps({'filesScanned': n, 'hits': hits, 'clean': not hits}, indent=1))

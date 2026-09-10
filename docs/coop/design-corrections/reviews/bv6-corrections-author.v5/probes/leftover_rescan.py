"""Re-run the v4 leftover scan for the corrected rationale, tree-wide. Limit: pattern matching finds
copies of a phrase; absence of a match is not proof of consistency."""
import json, pathlib, re
W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v5/work')
PAT = {
 'false-not-an-enum-rationale':
   r'is a CanonicalIdentifier, not an enum|not an enum, so no keyword|because `?relation`? is (a |not )',
 'schema-cannot-decide-normative': r'SCHEMA CANNOT DECIDE',
}
hits = {k: [] for k in PAT}
n = 0
for p in W.rglob('*'):
    if not p.is_file() or '/reviews/' in str(p) or p.suffix not in ('.md', '.json', '.py'):
        continue
    try:
        t = p.read_text(encoding='utf-8')
    except Exception:
        continue
    n += 1
    for k, rx in PAT.items():
        for m in re.finditer(rx, t):
            hits[k].append({'file': str(p.relative_to(W)),
                            'excerpt': t[max(0, m.start()-80):m.end()+80].replace('\n', ' ')})
print(json.dumps({'filesScanned': n, 'remainingHits': {k: v for k, v in hits.items() if v},
                  'clean': [k for k, v in hits.items() if not v]}, indent=1))

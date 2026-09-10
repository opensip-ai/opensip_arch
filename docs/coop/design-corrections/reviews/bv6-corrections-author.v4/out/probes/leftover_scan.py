"""Systematic scan for leftover copies of the claims this patch corrects. Leftover copies in a
SECOND document have been the recurring defect across v1-v3, so the scan is over the whole
non-review source tree rather than the five patched files."""
import json, pathlib, re
W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4/work')
PATTERNS = {
 'one-receipt-domain': r'the one receipt domain|exactly one receipt domain|only receipt2 domain',
 'operational-identities-excluded-rationale': r'operational identities are excluded from content identity',
 'history-only-fields': r'only fields (that )?`?HistoryPayloadV1|which are the only fields',
 'kind-classifies-granularity': r'`?kind`? together with `?qualifiedName`?|kind\b[^.]{0,40}is the SYMBOL granularity',
 'four-generic-rows': r'Among the generic `?mutation`? rows, \*\*four\*\*|four generic rows',
 'dangling-byCommand-pointer': r'x-opensip-mutation-operation-map/byCommand(?![A-Za-z])',
 'causes-stay-with-retained-coverage': r'stay with the producer and (the |with the )?retained Coverage',
 'schema-cannot-decide-because-not-enum': r'because `?relation`? is a CanonicalIdentifier rather than an enum|not an enum, so no keyword',
}
hits = {k: [] for k in PATTERNS}
scanned = 0
for p in W.rglob('*'):
    if not p.is_file() or '/reviews/' in str(p):
        continue
    if p.suffix not in ('.md', '.json', '.py'):
        continue
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        continue
    scanned += 1
    for name, rx in PATTERNS.items():
        for m in re.finditer(rx, txt):
            hits[name].append({'file': str(p.relative_to(W)),
                               'excerpt': txt[max(0, m.start()-70):m.end()+70].replace('\n', ' ')})
print(json.dumps({
 'standing': 'Coauthor leftover-copy scan over the non-review source tree. Pattern matching finds '
             'copies of a corrected phrase; it is not a semantic review and absence of a match is '
             'not proof of consistency.',
 'filesScanned': scanned,
 'remainingHits': {k: v for k, v in hits.items() if v},
 'clean': [k for k, v in hits.items() if not v]}, indent=1))

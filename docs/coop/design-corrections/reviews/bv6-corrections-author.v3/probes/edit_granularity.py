"""Codex note item: a path-only runtime row must not silently satisfy a symbol-keyed target.
Make the granularity classification and any coarsening explicit and uniform across both kinds,
and drop the two now-duplicated map keys."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')

# ---------------------------------------------------------------- 1. the projection
P = W / 'docs/coop/design-corrections/workflows/workflows_model.v1.py'
s = P.read_text(encoding='utf-8')
OLD = """        key = descriptor['subjectKey']
        symbol_granularity = bool(key.get('qualifiedName'))
        matches = []
        for row in payload_subjects:
            if row['path'] != key['logicalPath']:
                continue
            if kind == 'runtime' and 'symbol' in row and row['symbol'] != key['qualifiedName']:
                continue
            matches.append(row)
"""
NEW = """        key = descriptor['subjectKey']
        matches = []
        for row in payload_subjects:
            if row['path'] != key['logicalPath']:
                continue
            # A row that names a symbol answers ONLY that symbol. A row with no symbol is a
            # FILE-level observation: it still matches the path, but the answer is COARSER than the
            # subject key, and that coarsening is reported per target rather than passing silently.
            # HistorySubject never carries a symbol, so every history answer is file-level.
            if kind == 'runtime' and 'symbol' in row and row['symbol'] != key['qualifiedName']:
                continue
            matches.append(row)
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)
OLD2 = """        row = matches[0] if matches else None
        projection[target] = {
            'matched': row is not None,
            'logicalPath': key['logicalPath'],
            'symbolGranularity': symbol_granularity,
            # HistorySubject carries no symbol, so a symbol target is answered at file granularity.
            'granularityWidenedToFile': bool(symbol_granularity and kind == 'history'),
            'observability': row.get('observability') if row and kind == 'runtime' else None,
        }
"""
NEW2 = """        row = matches[0] if matches else None
        answer_granularity = ('symbol' if (row is not None and kind == 'runtime' and 'symbol' in row)
                              else 'file')
        projection[target] = {
            'matched': row is not None,
            'logicalPath': key['logicalPath'],
            'subjectQualifiedName': key['qualifiedName'],
            'answerGranularity': answer_granularity,
            # The answer is coarser than the subject key whenever a keyed subject is answered by a
            # file-level row. Reported, never silent, and identical in form for both kinds.
            'granularityWidenedToFile': bool(row is not None and answer_granularity == 'file'),
            'observability': row.get('observability') if row and kind == 'runtime' else None,
        }
"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)
OLD3 = """    GRANULARITY is preserved, not flattened. Runtime matches on logicalPath and, where the row
    carries `symbol`, on qualifiedName. History has NO symbol field, so a symbol-granularity target
    projects to its FILE and that widening is DISCLOSED per target rather than hidden.
"""
NEW3 = """    GRANULARITY is reported, never silently flattened. Every subjectKey carries a qualifiedName,
    and `subjectKey.kind` has NO closed vocabulary in this contract set, so this projection does not
    classify the TARGET by kind; it reports the granularity of the ANSWER relative to the key. A
    runtime row that names a `symbol` answers only that symbol - a symbol-keyed row for a different
    symbol never matches. A row with NO symbol is a FILE-level observation: it matches on path, but
    `answerGranularity` is `file` and `granularityWidenedToFile` is true, so a path-only row never
    silently passes as a symbol-level answer. HistorySubject carries no symbol at all, so every
    history answer is file-level and is reported as such. The coarsening is disclosed on the outcome
    and a consumer that needs symbol-level evidence can see that it did not get it.
"""
assert s.count(OLD3) == 1
P.write_text(s.replace(OLD3, NEW3), encoding='utf-8')

# ---------------------------------------------------------------- 2. the published law text
Q = W / 'docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json'
d = json.loads(Q.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
proj = d['x-opensip-imported-requirement-law']['targetSubjectProjection']
proj['deterministicProjection'][3] = (
    "4a. RUNTIME MATCH. A RuntimeSubject row matches when its `path` equals "
    "`subjectKey.logicalPath` AND, when that row carries `symbol`, its `symbol` equals "
    "`subjectKey.qualifiedName` - so a symbol-keyed row for a DIFFERENT symbol never matches. A row "
    "with NO symbol is a FILE-level observation: it matches on path but its answerGranularity is "
    "`file` and granularityWidenedToFile is true, so a path-only row NEVER silently passes as a "
    "symbol-level answer."
)
proj['deterministicProjection'][4] = (
    "4b. HISTORY MATCH. HistorySubject has NO symbol field, so a row matches when its `path` equals "
    "`subjectKey.logicalPath`, and every history answer is file-level and reported as such."
)
proj['granularityIsReportedNotClassified'] = (
    "Every subjectKey carries a qualifiedName, and `subjectKey.kind` has NO closed vocabulary in "
    "this contract set, so this projection does NOT classify the target by kind and no kind "
    "vocabulary is invented for it. What it reports is the granularity of the ANSWER relative to the "
    "key: `answerGranularity` is `symbol` only when a symbol-naming row matched, and "
    "`granularityWidenedToFile` marks every file-level answer to a keyed subject. Any coarsening the "
    "imported format cannot avoid - history having no symbol field at all, and a runtime capture that "
    "emitted only file rows - is therefore stated on the outcome rather than absorbed. This "
    "projection adds no capability to either payload format."
)
d['x-opensip-imported-requirement-law']['targetSubjectProjection'] = proj
Q.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ---------------------------------------------------------------- 3. drop the duplicated map keys
R = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
e = json.loads(R.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = e['x-opensip-mutation-operation-map']
# byStepKindReceiptOperation now carries repair-apply with its citations and exclusion flag, and
# receiptIdempotencyKeyByStepKind carries whatIsNotClaimed; the outer copies would only drift.
law.pop('dedicatedStepOperations', None)
law.pop('whatIsNotClaimed', None)
e['x-opensip-mutation-operation-map'] = law
R.write_text(json.dumps(e, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')

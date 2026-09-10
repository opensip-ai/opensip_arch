"""CB7-MUST-1 (4/4): the reference producer construction path in integration-fixtures."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/integration-fixtures.py'
s = P.read_text(encoding='utf-8')

OLD = """    unavailable=None
    if blobs is not None and inventory_paths is not None:
        try:_d,_u,_r=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_d,_u,_r=None,None,None
        if _d=='native.semantic-universe.syntax.v2':
"""
NEW = """    unavailable=None
    if blobs is not None:
        try:_d,_u,_r=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_d,_u,_r=None,None,None
        if _d=='native.semantic-universe.syntax.v2' and inventory_paths is not None:
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

TAIL = """                unavailable=N.syntax_capability_support(_rows,scope_descriptor['relation'],
                    scope_descriptor['resolution'],_paths,_all)
"""
TAIL_NEW = """                unavailable=N.syntax_capability_support(_rows,scope_descriptor['relation'],
                    scope_descriptor['resolution'],_paths,_all)
        # The same question for a universe whose body axis is a CLOSED SUFFIX TABLE (TypeScript):
        # can it read these subjects as a source variant at all? Selected on the dialect FORM in the
        # universe's own registry row - not on a universe id - and only for a relation that joins a
        # body identity, so nothing here claims a suffix table decides symbol capability. A producer
        # that cannot honestly claim a complete examination reports the published unavailable pair,
        # and the Run closure re-derives the same answer from the retained universe record.
        _dialect=((_r or {}).get('languageVersionBinding') or {}).get('dialect')
        _brow=RELATION_REGISTRY.get(scope_descriptor['relation']) or {}
        if (unavailable is None and isinstance(_dialect,dict)
                and _dialect.get('form')=='closed-suffix-table' and 'bodyIdentityJoin' in _brow):
            # Same per-relation subject law as above and as the closure: a `source-path` relation is
            # judged on ALL of this scope's own subjects; a `symbol` relation would need the
            # committed extent, so without one this helper makes no capability claim rather than
            # guessing one.
            if _brow.get('subjectKind')=='source-path':_paths,_all=list(scope_descriptor['subjects']),True
            elif inventory_paths is not None:_paths,_all=list(inventory_paths),False
            else:_paths,_all=None,None
            if _paths is not None:
                unavailable=N.source_variant_capability_support(_dialect,scope_descriptor['relation'],
                    scope_descriptor['resolution'],_paths,_all)
"""
assert s.count(TAIL) == 1
s = s.replace(TAIL, TAIL_NEW)
P.write_text(s, encoding='utf-8')
print('ok')

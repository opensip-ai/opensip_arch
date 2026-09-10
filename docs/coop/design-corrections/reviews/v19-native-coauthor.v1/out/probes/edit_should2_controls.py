"""CB7-SHOULD-2: widen the published law, update the two counting controls, add the new control set."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')

# ---------------------------------------------------------------- 1. the owning published sentence
MD = W / 'docs/v2/contracts/product-v1/native-evidence.md'
m = MD.read_text(encoding='utf-8')
OLD_MD = "it is never truncated. **Four** fields are bounded this way, across **two** record families,"
if OLD_MD not in m:
    OLD_MD = "it is never truncated. **Four** fields are bounded this way, across **two** record families, "
assert m.count("**Four** fields are bounded this way") == 1, 'anchor'
m = m.replace("**Four** fields are bounded this way, across **two** record families",
              "**Seven** fields are bounded this way, across **three** record families")
OLD_TAIL = ("Native ScopeRefusal retains detail, D9 and observed bound fields for the host's closed "
            "termination projection, and is already field-generic, so all four fields use one law and one code: "
            "the remedy class is identical — narrow the selection explicitly, nothing was truncated — which is "
            "why widening it across the second record family adds no public code.")
assert m.count(OLD_TAIL) == 1, 'tail anchor'
NEW_TAIL = ("The **Plan** family contributes the remaining three, and they are reachable by ordinary valid "
            "selections that every earlier bound admits: `nativeContextDigests` has limit128 and carries one "
            "member per DISTINCT admitted native context, so an inventory-only or otherwise narrow capability "
            "selection keeps `requestedCapabilities` far below its own1024 while129 units whose compiler "
            "closure, standard library and effective options differ pass the workspace bound and cannot be "
            "expressed in the Plan; `importIds` has limit256 while the selecting field "
            "`semantic-configuration.evidence.importIds` admits1024, so257 imported evidence records are an "
            "admitted configuration and an unrepresentable Plan; and `semanticClosures` has limit128 while "
            "`policyPackIds` admits128 packs that need not share closures. Those three are accounted "
            "**before plan2 is minted**, on the PROSPECTIVE Plan assembled from an already-admitted request, so "
            "a refusal mints no Plan and no Run for the refused step. They are **not** a retained-record check: "
            "an externally retained Plan over its bound is a corrupt or malformed retained record and keeps its "
            "schema-first refusal and this section's origin-dependent routing, because re-deriving a caller's "
            "remedy from already-committed bytes would misreport a corrupt store as an oversized request. Only "
            "an ACTUAL array over its bound refuses on cardinality; a missing field, null, boolean, number, "
            "string or object is a shape the schema owns and reaches it untouched. When more than one Plan array "
            "overflows at once the subject is the first in the published `$defs/plan` declaration order — "
            "`semanticClosures`, `nativeContextDigests`, `importIds` — so one request always yields one subject "
            "and narrowing makes deterministic progress. "
            "Native ScopeRefusal retains detail, D9 and observed bound fields for the host's closed "
            "termination projection, and is already field-generic, so all seven fields use one law and one code: "
            "the remedy class is identical — narrow the selection explicitly, nothing was truncated — which is "
            "why widening it across the further record families adds no public code, while each field keeps its "
            "OWN remedy wording because what a caller narrows differs per field.")
m = m.replace(OLD_TAIL, NEW_TAIL)
MD.write_text(m, encoding='utf-8')

# ------------------------------------------------------------------------ 2. controls
P = W / 'docs/coop/design-corrections/foundation/check-identity.py'
s = P.read_text(encoding='utf-8')

OLD_C = """check('one-law-serves-four-bounded-fields-across-two-record-families',
      set(N.SCOPE_LIMIT_REMEDY)=={'workspaceRoots','pathPrefixes','excludedPathPrefixes',
                                  'requestedCapabilities'}
      and set(list(M.SCHEMA['$defs']['scope-descriptor']['properties'])) >= {'workspaceRoots',
          'pathPrefixes','excludedPathPrefixes'}
      and 'requestedCapabilities' in M.SCHEMA['$defs']['analysis-spec']['properties'])"""
NEW_C = """check('one-law-serves-seven-bounded-fields-across-three-record-families',
      set(N.SCOPE_LIMIT_REMEDY)=={'workspaceRoots','pathPrefixes','excludedPathPrefixes',
                                  'requestedCapabilities','semanticClosures','nativeContextDigests',
                                  'importIds'}
      and set(list(M.SCHEMA['$defs']['scope-descriptor']['properties'])) >= {'workspaceRoots',
          'pathPrefixes','excludedPathPrefixes'}
      and 'requestedCapabilities' in M.SCHEMA['$defs']['analysis-spec']['properties']
      and set(M.SCHEMA['$defs']['plan']['properties']) >= set(N.PLAN_SELECTION_FIELDS))
# Every remedy is FIELD-SPECIFIC. One shared public code with one shared wording would tell a caller
# that something overflowed and nothing about what to narrow.
check('every-bounded-field-carries-its-own-narrowing-remedy',
      len(set(N.SCOPE_LIMIT_REMEDY.values()))==len(N.SCOPE_LIMIT_REMEDY) and
      all(text and 'truncated' in text for text in N.SCOPE_LIMIT_REMEDY.values()))"""
assert s.count(OLD_C) == 1
s = s.replace(OLD_C, NEW_C)

OLD_P = """check('the-published-law-states-the-widened-meaning-over-four-fields',
      'requestedCapabilities' in _SCOPE_PARA and 'workspaceRoots' in _SCOPE_PARA
      and '**Four** fields' in _SCOPE_PARA and 'two record families' in _SCOPE_PARA
      and 'bounded selection array' in _SCOPE_PARA and 'adds no public code' in _SCOPE_PARA)"""
NEW_P = """check('the-published-law-states-the-widened-meaning-over-seven-fields',
      'requestedCapabilities' in _SCOPE_PARA and 'workspaceRoots' in _SCOPE_PARA
      and '**Seven** fields' in _SCOPE_PARA and 'three** record families' in _SCOPE_PARA
      and 'bounded selection array' in _SCOPE_PARA and 'adds no public code' in _SCOPE_PARA
      and all(field in _SCOPE_PARA for field in N.PLAN_SELECTION_FIELDS))"""
assert s.count(OLD_P) == 1
s = s.replace(OLD_P, NEW_P)
P.write_text(s, encoding='utf-8')
print('ok')

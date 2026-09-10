"""CB7-MUST-1 (1/4): the producer-unit law, structurally parallel to syntax_capability_support."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
s = P.read_text(encoding='utf-8')

ANCHOR = '''PUBLIC_ROUTE_REGISTRY = SCHEMAS["x-opensip-public-route-registry"]
'''
NEW = '''def source_variant_of_path(path: str, table: dict) -> str | None:
    """The SELECTED source variant a path's own suffix denotes, by LONGEST match over the closed
    table, or None when the suffix is outside it.

    The table is READ from the owning registry - identity-schemas
    #/x-opensip-digest-domains/domainSets/native-semantic-universe/<universe>/languageVersionBinding
    /dialect/table - and is never restated here, so the suffix vocabulary has exactly one authority.
    Longest match is the published selectionLaw, which is why `.d.ts` is never read as `.ts`."""
    best, best_variant = None, None
    for suffix, variant in table.items():
        if path.endswith(suffix) and (best is None or len(suffix) > len(best)):
            best, best_variant = suffix, variant
    return best_variant


def source_variant_capability_support(dialect: dict, relation: str, rung: str,
                                      paths: list[str], require_all: bool) -> dict | None:
    """Can a universe whose body axis is a CLOSED SUFFIX TABLE serve `relation@rung` over `paths`?
    None means supported.

    WHAT THIS CLOSES (CB7-MUST-1). `body_language_version` refuses an unlisted suffix with the
    registry's own `onUnknown` - BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN for TypeScript - but that
    refusal is only ever reached when a BODY FACT is being derived. A clones subject-scope over, say,
    `package.json` under a TypeScript universe produces no body at all, so nothing fired and the
    scope could claim `coverage: complete` with no deficiency: a determinate "no clones here" the
    universe never had the capability to establish. That ambiguity reached coverage2 -> view2 ->
    evidence2 -> seal2 -> run2.

    WHY THIS CLASSIFICATION AND NOT THE OTHER READING. The alternative was to treat the unlisted
    suffix like Rust's BODY_LANGUAGE_OWNER_NOT_COMPILED and leave `complete` lawful. That is sound
    for Rust and wrong here, and the difference is real rather than stylistic: OWNER_NOT_COMPILED
    describes a path that IS a Rust source file which no selected target compiles - the universe
    examined it and the answer is a resolution fact about a known language. An unlisted suffix under
    a TypeScript universe is not a TypeScript body in any dialect, so there is nothing the universe
    could have examined for clone bodies. Claiming `complete` would assert a negative from an absent
    capability, which is exactly what the syntax guard already refuses for the third universe. So the
    published pair is the EXISTING `language-tier-unsupported` / `capability-missing` - no new
    deficiency, no new NativeCause, no new DomainDetailCode.

    SHAPE. Deliberately the same as `syntax_capability_support`, because it answers the same
    question about a different closed vocabulary:

    * INVENTORY capabilities are never gated. A snapshot inventories every file it contains, so
      `file`, `package` and `vcs-change` keep their promised meaning on every inventoried path
      including ones no dialect reads.
    * `require_all=True` (a `source-path` scope, whose subjects ARE snapshot paths, and a nonempty
      FACT, whose anchors are the files actually read): EVERY named path must have a registered
      variant, so a MIXED scope cannot hide its unsupported part behind its supported one.
    * `require_all=False` (a `symbol` scope, whose subjects are opaque ids the record associates with
      no path): at least one path of the committed extent must be readable. It never inspects whether
      facts exist, so an EMPTY view is judged on the same evidence as a populated one.
    * An empty path list under `require_all=True` is unsupported, never vacuously true.

    A POSITIVE supported code path is unaffected: `src/a.ts` has a registered variant, so a clones
    scope over it stays eligible for `complete` even when it contains no clone body at all. Absence
    of a body is a finding; absence of a capability is not."""
    capability = relation + "@" + rung
    if capability in INVENTORY_CAPABILITIES:
        return None
    table = (dialect or {}).get("table")
    if not isinstance(table, dict) or not table:
        # No closed suffix table on this universe's body axis, so this law does not own it. Rust's
        # ownership form and any future form keep their own selection law untouched.
        return None
    readable = [source_variant_of_path(p, table) is not None for p in paths]
    if require_all:
        if not paths or not all(readable):
            return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
        return None
    if not any(readable):
        return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
    return None


PUBLIC_ROUTE_REGISTRY = SCHEMAS["x-opensip-public-route-registry"]
'''
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')
print('ok')

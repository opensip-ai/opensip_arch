"""CB7-SHOULD-2: extend the S14 bounded-selection accounting to the Plan's own three arrays."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
s = P.read_text(encoding='utf-8')

OLD = '''# One remedy per bounded selection array. Both are the same remedy CLASS - narrow the selection explicitly,
# nothing was truncated - which is why they share one public code; the wording names the field's own surface.
SCOPE_LIMIT_REMEDY = {
    "workspaceRoots": "narrow the explicit workspace selection; no root was truncated",
    "pathPrefixes": "narrow the explicit path selection; no prefix was truncated",
    "excludedPathPrefixes": "narrow the explicit exclusion selection; no prefix was truncated",
    "requestedCapabilities": ("narrow the analysis explicitly - fewer workspace roots for this invocation, or an "
                             "explicit analysis.capabilities selection - no capability was truncated and the "
                             "product default is unchanged"),
}
'''
NEW = '''# One remedy per bounded selection array. All are the same remedy CLASS - narrow the selection explicitly,
# nothing was truncated - which is why they share one public code; the wording names the field's own surface.
# A field-specific remedy is the point: `field:count>limit` says WHAT overflowed, and only the remedy can say
# what a caller does about THIS field, which differs between a root selection, a capability selection, a rule
# closure set, a per-unit compiler context set and an imported-evidence selection.
SCOPE_LIMIT_REMEDY = {
    "workspaceRoots": "narrow the explicit workspace selection; no root was truncated",
    "pathPrefixes": "narrow the explicit path selection; no prefix was truncated",
    "excludedPathPrefixes": "narrow the explicit exclusion selection; no prefix was truncated",
    "requestedCapabilities": ("narrow the analysis explicitly - fewer workspace roots for this invocation, or an "
                             "explicit analysis.capabilities selection - no capability was truncated and the "
                             "product default is unchanged"),
    "semanticClosures": ("narrow the rule selection explicitly - fewer policy packs, or packs sharing one rule "
                         "closure, for this invocation; no closure was truncated"),
    "nativeContextDigests": ("narrow the analysis explicitly - fewer workspace roots for this invocation; "
                             "no context was truncated, and units that genuinely share one compiler closure, "
                             "standard library and effective options already collapse to one member"),
    "importIds": ("narrow the imported-evidence selection explicitly - fewer evidence.importIds in the resolved "
                  "semantic configuration for this invocation; no import was truncated"),
}

# The Plan's OWN bounded selection arrays, in the order the published `$defs/plan` DECLARES them. The order is
# load-bearing rather than cosmetic: a request may overflow more than one at once, and a caller narrowing a
# selection needs the same first subject every time from the same request. It is read from the schema by the
# drift control beside these, so it cannot silently diverge from the published document.
PLAN_SELECTION_FIELDS = ("semanticClosures", "nativeContextDigests", "importIds")


def plan_selection_bound(field: str) -> int:
    """The published Plan bound, READ from the foundation schema rather than restated here."""
    return IM.SCHEMA["$defs"]["plan"]["properties"][field]["maxItems"]


def admit_plan_selection_cardinality(plan: dict) -> dict:
    """THE PRE-PLAN admission boundary for the Plan's own bounded selection arrays (CB7-SHOULD-2).

    WHY IT WAS NEEDED. `plan.semanticClosures` and `plan.nativeContextDigests` admit 128 members and
    `plan.importIds` 256, and all three are reachable by an ORDINARY VALID selection that every earlier
    boundary admits:

    * `nativeContextDigests` carries one member per DISTINCT admitted native context, and units of one
      language collapse only when their compiler closure, standard library and effective options are
      identical - which co-located units of a real monorepo routinely are not. `scope-descriptor.workspaceRoots`
      admits 1024 roots, and an inventory-only or otherwise NARROW capability selection keeps
      `requestedCapabilities` far below its own 1024 bound, so 129 such units pass the workspace bound and the
      analysis-spec bound and then cannot be expressed in the Plan at all.
    * `importIds` is selected by `semantic-configuration.evidence.importIds`, which admits 1024 - four times
      the Plan's 256 - so an ordinary configuration naming 257 imported evidence records is admitted as a
      configuration and unrepresentable as a Plan.
    * `semanticClosures` carries the rule and enumerator closures a policy selection resolves to;
      `analysis-spec.policyPackIds` and `semantic-configuration.policy.packIds` each admit 128 packs, so a
      selection whose packs do not share closures reaches the same wall.

    In every one of those cases the only outcome was a generic jsonschema `maxItems` ValidationError that
    restates the whole instance and names no field, no count, no limit and no public route - the exact defect
    `admit_requested_capability_cardinality` was added to close for the analysis spec. The bound is NOT widened
    and nothing is truncated or silently downgraded to less analysis: an oversized selection is a REQUEST that
    cannot be expressed, which is request-rejected / exit 2 (`REQUEST.UNSATISFIABLE`, `PROJECT.SCOPE_LIMIT`)
    with the exact `field:count>limit` subject and this field's own narrowing remedy.

    WHERE IT SITS, AND WHAT IT DELIBERATELY DOES NOT TOUCH. This is PRE-PLAN: it runs on a PROSPECTIVE Plan
    assembled from an already-admitted request, before `plan2` is minted, so a refusal mints no Plan and no
    Run for the refused step. It is emphatically NOT a retained-record check. An externally retained Plan whose
    array exceeds its bound is a CORRUPT or malformed retained record, and `admit_run` schema-validates the
    retained Plan exactly as before: that path keeps its schema-first refusal and section 10's origin-dependent
    routing, and is not rewritten into a request-scope refusal. Re-deriving a caller's remedy from bytes that
    were already committed would misreport a corrupt store as an oversized request.

    THE SHAPE RULE IS THE ANALYSIS-SPEC RULE, ON PURPOSE. Only an ACTUAL JSON array over its bound refuses
    here. A missing field, a null, a boolean, a number, a string, an object, and an in-bound array malformed
    some other way are all shapes the SCHEMA owns and are passed through untouched to it - nothing is coerced,
    length-of-a-string is never reported as a member count, and no shape is repaired. Cardinality-first
    therefore applies only where an actual array actually exceeds its bound.

    ORDER. `PLAN_SELECTION_FIELDS` is the published `$defs/plan` declaration order. A request that overflows
    two arrays at once refuses on the first of them in that fixed order, so the same request always yields the
    same subject and a caller narrowing one selection makes deterministic progress."""
    if not isinstance(plan, dict):
        return plan
    for field in PLAN_SELECTION_FIELDS:
        value = plan.get(field)
        if isinstance(value, list):
            limit = plan_selection_bound(field)
            if len(value) > limit:
                raise ScopeRefusal(field, len(value), limit)
    return plan
'''
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

# The producer of `nativeContextDigests` accounts for its own field at the point it produces it.
OLDP = '''    for a in admissions:
        if a["refusals"]:
            raise AdmissionError("NATIVE_CONTEXT_NOT_ADMITTED:" + a["refusals"][0])
    return sorted({a["planNativeContextDigest"] for a in admissions})'''
NEWP = '''    for a in admissions:
        if a["refusals"]:
            raise AdmissionError("NATIVE_CONTEXT_NOT_ADMITTED:" + a["refusals"][0])
    digests = sorted({a["planNativeContextDigest"] for a in admissions})
    # Accounted HERE as well as at the Plan boundary, because this is where the field is PRODUCED: the
    # deduplication above is exactly what decides the count, so the first place the count exists is the first
    # place it can be reported with a field, a count and a limit instead of a generic schema exception.
    admit_plan_selection_cardinality({"nativeContextDigests": digests})
    return digests'''
assert s.count(OLDP) == 1
s = s.replace(OLDP, NEWP)
P.write_text(s, encoding='utf-8')
print('ok')

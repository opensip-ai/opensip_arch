"""CB7-MUST-1: publish the scope-capability law in the OWNING registry and have the model read it."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')

# --- 1. the owning registry ---------------------------------------------------------------
P = W / 'docs/coop/design-corrections/foundation/identity-schemas.v2.json'
s = P.read_text(encoding='utf-8')
ANCHOR = '    "languageVersionBindingLaw": "Normative, and consumed by identity Run closure.'
assert s.count(ANCHOR) == 1
LAW = '''    "scopeCapabilityLaw": {
      "standing": "Normative, and consumed by BOTH the native producer admission boundary and identity Run closure. It states what a COVERAGE claim over a body-dialect relation means under a universe whose dialect form is a closed suffix table. The per-BODY selector (`dialect.onUnknown`) was already total, but it is only reached while a body is being derived, so a scope that produced NO fact was classified by nothing and could claim a determinate `complete` for a path the universe cannot read in any dialect. Coverage is a claim about the EXAMINATION and must not be decided by whether the examination happened to produce output.",
      "appliesToDialectForm": "closed-suffix-table",
      "gate": "Relations carrying a `bodyIdentityJoin` in the relation registry, which is where the dialect axis is consulted at all. Nothing here claims a suffix table decides SYMBOL capability, and no compiler, parser or grammar is executed, ranked or qualified: the only question asked is whether the path's own suffix selects a variant in the table this universe published.",
      "subjectLaw": "The relation registry's own `subjectKind`. A `source-path` relation is judged on ALL of THIS scope's subjects, so a mixed scope cannot hide its unsupported part behind its supported one. Any other subject kind is judged on the committed snapshot inventory, where at least one path must be readable, because the retained record associates an opaque subject id with no path.",
      "emptySubjects": "Unsupported. An empty `source-path` scope is never vacuously supported.",
      "inventoryExempt": "`file@enumerated`, `package@manifest-declared` and `vcs-change@vcs-reported` are never dialect-gated. A snapshot inventories every file it contains, so inventory evidence keeps its promised meaning on every inventoried path including ones no dialect reads.",
      "onUnsupportedScope": {
        "coverage": "unknown",
        "deficiency": "language-tier-unsupported",
        "nativeCause": "capability-missing"
      },
      "onSupportedScope": "Eligible for `complete` even when the scope contains no body at all. An absent body is a finding; an absent capability is not.",
      "notAProofOfAbsence": "An unsupported scope is NOT a finding that no such construct exists. It is the disclosure that this universe never had the capability to look, which is the same principle the syntax universe's grammar-capability law already encodes.",
      "distinctFromOwnerNotCompiled": "Deliberately NOT the treatment `BODY_LANGUAGE_OWNER_NOT_COMPILED` gets. That refusal describes a path which IS a source file of the universe's language and which no selected compilation target owns - the universe examined it and produced a resolution fact about a known language, so `complete` stays lawful there. A suffix outside the table is not a body of this universe in ANY dialect, so there is nothing it could have examined and a determinate answer would assert a negative from an absent capability.",
      "refusals": "A false `complete`, a wrong deficiency and a wrong or null cause each refuse separately and by their own name, at the producer boundary (`native.coverage-source-variant-*`) and at retained Run closure (`COVERAGE_SOURCE_VARIANT_*`).",
      "guardOrder": "Where a universe is owned by a more specific capability law - the compilation-ownership axis, or the syntax grammar-capability registry - that law is applied FIRST at Run closure and keeps its own refusal name. This law is the backstop that makes the set of published universes total; for the syntax universe it is a strictly weaker necessary condition its own registry already implies, because that registry publishes that no data-document suffix appears in the syntax dialect table."
    },
'''
s = s.replace(ANCHOR, LAW + ANCHOR)
P.write_text(s, encoding='utf-8')

# --- 2. the model reads it ----------------------------------------------------------------
Q = W / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
t = Q.read_text(encoding='utf-8')
OLD = '''    capability = relation + "@" + rung
    if capability in INVENTORY_CAPABILITIES:
        return None
    table = (dialect or {}).get("table")'''
NEW = '''    capability = relation + "@" + rung
    if capability in INVENTORY_CAPABILITIES:
        return None
    table = (dialect or {}).get("table")'''
assert t.count(OLD) == 1

# the published pair, READ from the owning registry rather than restated
CONST_ANCHOR = '''def source_variant_of_path(path: str, table: dict) -> str | None:'''
CONST = '''# The scope-capability law for a closed-suffix-table universe, READ from its owning authority
# (identity-schemas #/x-opensip-digest-domains/scopeCapabilityLaw) rather than restated here. The
# disclosure a consumer sees is therefore the one the registry publishes, and a drift control asserts
# it is the SAME pair the syntax universe already discloses - one vocabulary, not two.
SCOPE_CAPABILITY_LAW = IM.DIGESTS["scopeCapabilityLaw"]
SOURCE_VARIANT_UNAVAILABLE_DISCLOSURE = {
    key: SCOPE_CAPABILITY_LAW["onUnsupportedScope"][key] for key in ("deficiency", "nativeCause")}


def source_variant_of_path(path: str, table: dict) -> str | None:'''
assert t.count(CONST_ANCHOR) == 1
t = t.replace(CONST_ANCHOR, CONST)

RET = '''    readable = [source_variant_of_path(p, table) is not None for p in paths]
    if require_all:
        if not paths or not all(readable):
            return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
        return None
    if not any(readable):
        return dict(UNAVAILABLE_CAPABILITY_DISCLOSURE)
    return None'''
RET_NEW = '''    readable = [source_variant_of_path(p, table) is not None for p in paths]
    if require_all:
        if not paths or not all(readable):
            return dict(SOURCE_VARIANT_UNAVAILABLE_DISCLOSURE)
        return None
    if not any(readable):
        return dict(SOURCE_VARIANT_UNAVAILABLE_DISCLOSURE)
    return None'''
assert t.count(RET) == 1
t = t.replace(RET, RET_NEW)
Q.write_text(t, encoding='utf-8')
print('ok')

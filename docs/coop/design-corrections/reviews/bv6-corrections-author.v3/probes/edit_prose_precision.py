"""BV6-V3-IMPORT-BINDING/SEMANTICS prose, and BV6-V3-PRECISION corrections."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')
WF = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
t = WF.read_text(encoding='utf-8')

# ------------------------------------------------- §4: the projection and corrected semantics
OLD4 = """Four limits carry over unchanged and are enforced rather than assumed.
**Satisfied does not mean positive**: `observed-hit` is positive execution
evidence and `observable-unhit` is *bounded negative* evidence, both can satisfy,
and the disclosure records which did. **No imported observation establishes a
universal negative** — one window is not universal non-use — and imported evidence
can never *by itself* establish the native closed world or authorize an unsafe
`delete`/`replace`: that gate stays the evidence Run's own `ClosedWorldV2` (§6).
It may still be an **additional required condition** alongside an
already-established native basis, so it is wrong to say it never affects
applicability; an unsatisfied imported requirement makes an otherwise-eligible
plan inapplicable. **Whole-versus-partial** is the requirement's existing
`completeness`: `complete` needs every plan target supported, `partial-acceptable`
at least one. And **required versus optional** stays where `evidenceUse` puts it —
an optional absence remains the `IMPORT.ABSENT_FOR_PREDICATE` disclosure, is
satisfied *by absence* rather than by evidence, and an unsupplied declaration is
read as **required**, never silently as optional.
"""
NEW4 = """**A repair target is a fingerprint, not a path, and the join is published.**
`RepairPlanDescriptor.targets` are `finding-key2:` **fingerprints**, while
`RuntimeSubject` is keyed by `{path, symbol?}` and `HistorySubject` by `{path}`.
The deterministic projection is
`imported-evidence.schema.json#/x-opensip-imported-requirement-law/targetSubjectProjection`:
each target must be a finding of the evidence Run named by `evidenceRunId` (preview
already refuses one that is not); that `finding-key2` identity is the H identity of
the retained foundation `finding-fingerprint` descriptor, whose retention is
`preimage` and whose bytes are therefore re-hashed at Run closure; and its
`subjectKey` supplies `logicalPath` for file granularity and `qualifiedName` for
symbol granularity. Runtime matches on the path and, where the payload row carries
`symbol`, on the qualified name — so a symbol target is **not** served by another
symbol's row. History has no symbol field, so a symbol target is answered at
**file** granularity and that widening is **disclosed**, not hidden. More than one
matching subject **refuses**: an ambiguous projection is not resolved by choosing
one. A target with no matching subject is unsupported — never satisfied, and never
read as evidence of non-use.

Five limits carry over and are enforced rather than assumed.
**Satisfied does not mean positive**: `observed-hit` is positive execution
evidence and `observable-unhit` is *bounded negative* evidence, both can satisfy,
and the disclosure records which did. **No imported observation establishes a
universal negative** — one window is not universal non-use — and imported evidence
can never *by itself* establish the native closed world or authorize an unsafe
`delete`/`replace`: that gate stays the evidence Run's own `ClosedWorldV2` (§6).
It may still be an **additional required condition** alongside an
already-established native basis, so it is wrong to say it never affects
applicability; an unsatisfied imported requirement makes an otherwise-eligible
plan inapplicable. **Whole-versus-partial** is decided by the requirement's
`completeness` field: `complete` needs every plan target supported,
`partial-acceptable` at least one. That enum already existed, but **this reading of
it for an imported requirement over plan targets is selected here** and was not
previously published. A target that is unobservable or outside the history
collection scope therefore only names the cause *more precisely when the support
test fails* — it does not veto a lawful `partial-acceptable` requirement that has a
supported target. **Bounds are separate from support**: an insufficient observation
window or revision range applies under both completeness values, because it is a
property of the observation rather than of the target count. And **required versus
optional** stays where `evidenceUse` puts it — an optional absence remains the
`IMPORT.ABSENT_FOR_PREDICATE` disclosure and is satisfied *by absence* rather than
by evidence. That declaration reaches the requirement boundary as a **typed
boolean**; a non-boolean refuses, so there is no `unknown` state to default and no
falsy value is read as optional.
"""
assert t.count(OLD4) == 1
t = t.replace(OLD4, NEW4)

# ------------------------------------------------- §6: remove the false schema rationale
OLD6 = """The two vocabularies are **disjoint**, and a cross-plane value — a native
requirement claiming `import-unmapped-only`, or an imported one claiming
`resolution-incomplete` — is refused at admission. The schema alone cannot decide
this, because `relation` is a canonical identifier rather than an enum; it admits
either vocabulary, and the plane check is the admission's. That division is stated
rather than implied.
"""
NEW6 = """The two vocabularies are **disjoint**, and a cross-plane value — a native
requirement claiming `import-unmapped-only`, or an imported one claiming
`resolution-incomplete` — is refused at admission, as is an outcome of the wrong
imported **kind**, such as a history range cause on a runtime relation. This schema
**deliberately leaves the authoritative registry lookup to admission**: it admits
either vocabulary and does not attempt to reproduce the relation registries, which
it could not fetch rows from in any case. That is a design choice about where the
authority lives, not a limitation of JSON Schema — a schema *can* branch on a
property's `const`/`enum` even where the base type is a broader string — and
duplicating a registry as schema conditionals would create exactly the drift this
contract set avoids elsewhere. The division is stated rather than implied.
"""
assert t.count(OLD6) == 1
t = t.replace(OLD6, NEW6)

OLD6B = """  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition and is bound to the payload field that
  grounds it, and each kind reports only the outcomes **its own** payload can
  ground (§4). The requirement record gains no field: plan `targets` supply the
  per-target scope, its existing `completeness` decides whole-versus-partial, and
  `evidenceUse` supplies required-versus-optional.
"""
NEW6B = """  as `common.schema.json#/$defs/ImportedRequirementDeficiency`; every member names
  an already-published import condition and is bound to the payload field that
  grounds it, and each kind reports only the outcomes **its own** payload can
  ground — enforced at **both** the producer and this admission (§4). The
  requirement record gains no field: plan `targets` supply the per-target scope
  through the published fingerprint projection, `completeness` decides
  whole-versus-partial under the reading selected in §4, and `evidenceUse` supplies
  required-versus-optional as a typed boolean. The bounded observation demand is
  owned by the **admitted recipe closure** named by `recipe.closureId` — `RecipeRef`
  carries no such wire field and none is claimed.
"""
assert t.count(OLD6B) == 1
WF.write_text(t.replace(OLD6B, NEW6B), encoding='utf-8')

# ------------------------------------------------- schema description: same correction
P = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
dv = d['$defs']['EvidenceRequirement']['properties']['deficiency']
dv['description'] = dv['description'].replace(
    "THE SCHEMA ALONE CANNOT DECIDE THIS and does not pretend to - `relation` is a "
    "CanonicalIdentifier rather than an enum, so no keyword here can look up which registry it "
    "belongs to, and this oneOf therefore admits either vocabulary on either relation. The plane "
    "check is the admission's, and that limit is stated rather than implied.",
    "THIS SCHEMA DELIBERATELY LEAVES THE AUTHORITATIVE REGISTRY LOOKUP TO ADMISSION: the oneOf "
    "admits either vocabulary on either relation, and admission decides the plane AND the imported "
    "KIND from registry membership. That is a choice about where the authority lives, not a "
    "limitation of JSON Schema - a schema can branch on a property's const/enum even where the base "
    "type is a broader string - and duplicating a registry as schema conditionals would create the "
    "drift this contract set avoids elsewhere. The schema also cannot fetch registry rows.")
dv['x-opensip-vocabulary']['planeDecidedBy'] = (
    "the relation registry the relation belongs to, read at admission by "
    "workflows_model.admit_evidence_requirement, which decides both the PLANE and, for the imported "
    "plane, the per-KIND applicability of the value. The same separation the imported-evidence "
    "evidenceDeclarationRule already makes. This schema deliberately leaves that authoritative "
    "lookup to admission rather than duplicating a registry as conditionals.")
d['$defs']['EvidenceRequirement']['properties']['deficiency'] = dv
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ------------------------------------------------- D9 wording: ENUM, not definition bytes
Q = W / 'docs/coop/design-corrections/workflows/schemas/common.schema.json'
e = json.loads(Q.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
e['$defs']['D9Deficiency']['description'] += (
    " PROVENANCE: this ENUM is unchanged from the inherited D9 exit contract and no member was "
    "added, removed or reordered by any correction in this series. The DEFINITION BYTES of this "
    "$defs entry did change, because this description was added; an earlier handoff said the "
    "definition was byte-unchanged, which was true only of the enum.")
Q.write_text(json.dumps(e, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')

# Presentation catalogue owner correction02

Root continuation addressing actual-Claude presentation review01. Candidate for RP-DO-01, RP-DO-06, RP-DO-07 and RP-DO-08. Not accepted or
integrated. The proposal supplies descriptions and existing applicable recipe
inputs without changing native evidence, policy predicates or repair grants.

## Immutable association and retention

Reserve the unique regular-file path `.opensip/presentation-catalog.v1.json`
inside an already admitted contribution closure. Apply the same association law
as security-and-lifecycle's `.opensip/detector-compatibility.json`: signed
manifest/catalog association, selected platform TreeCommitment, the identical
regular-file Blob in closure.tree, exact length and raw SHA-256, and retained
bytes. A path/digest/tree/platform/closure swap refuses. Present malformed or
nonregular listings refuse; they never downgrade to absence. Absence means no
catalogue. An empty valid catalogue is an explicit empty declaration.

The catalogue is passive data. Reading it performs no repository/component
execution, install, grant or network fetch. It does not introduce a second
signature scheme or a caller-supplied `signatureVerified` assertion. Metadata
association is consumed only after the existing security/closure admission.
The reference dictionaries and supplied declaration sets are preconditions,
not authority-bearing runtime types; the actual host must obtain them from its
admitted immutable registry and retained closure handles.

The listing must NOT embed its containing closureId: that would make closure
identity self-referential. Recipe descriptors use only contributionId, recipeId
and recipeVersion inside the tree. The host adds the containing admitted
closureId when matching the full RecipeRef. Rule descriptors carry the exact
admitted ruleProgramRef, including semanticsMajor and programDigest. Capability descriptions use the separately authenticated native release authority below. A contribution closure cannot declare native capabilities by listing their names. Rule and recipe descriptor keys must exist in that closure's admitted declaration index. Metadata cannot invent
an activated rule, a capability, a supported mode or a recipe.

An associated receipt names closureId, componentManifestDigest, the exact listing
Blob, the complete closure.tree, platform, protocolMajor and trustOrigin (retained-generation, installed-signed-release or
signed-closure-bundle). It carries no authority beyond its already-admitted
parent. Retention follows that exact closure's tree/Blob rules; historical Run
queries use their exact retained closure, never the newest installed catalogue.
If old metadata is not retained, say so. A current descriptor with the same
display name or recipe version cannot fill that historical gap.

The file uses the existing exact JSON canonical owner profile: at most4MiB raw
and canonical bytes,32 containers, exact integer and Unicode rules. Arrays use
the existing canonical-set order and strictly unique descriptor keys; tags use
UTF-8 unique order. There are at most4096 rows in each catalogue group,32 tags
per row,256 Unicode scalar values per name and8192 per description. The total
byte cap applies even when each individual field fits. These are proposed
metadata admission caps, not measured browser or release sizing evidence.

## Descriptions, search and provenance

For capabilities and rules, the report copies the selected descriptor name,
description and tags verbatim as text, accompanied by the receipt. It filters
only the keys selected by the admitted native release/policy registry for that
Run. A capability description neither expands the native capability×mode matrix
nor resolves coverage limitations. Rule descriptions do not change policy AST,
program identity, severity, gating, waiver or evidence use. Search and tag/source
filters describe this embedded metadata population only.

A new core release must supply descriptors for every built-in capability, rule
and recipe that it exposes in this report catalogue, checked against the exact
compiled declaration index during build/admission. Optional older contribution
closures may lack the listing; that honest state is not permission to omit new
core metadata. Supplying the core catalogue and its completeness gate is required
implementation work, not satisfied by this schema/reference proposal.

## Recipe target bounds and applicable parameters

The selected RepairPreviewParams already define the applicable inputs:
`evidenceSource` (exact Run or earlier workflow step), `recipe` (full RecipeRef),
and `targets` (1–4096 distinct finding fingerprints). There is no generic recipe
keyword-argument object in this profile. This proposal does not invent one.

Each recipe descriptor supplies its name/description/tags, a
`finding-fingerprints` `targetBounds` record with limits copied from the selected target
schema, and human descriptions for exactly `evidenceSource` and `targets`.
The report shows the full host-bound RecipeRef separately, along with the actual
admitted selected inputs when viewing a particular preview. Recipe-specific applicability comes from the existing admitted RepairPlanDescriptor at preview; the generic bounds do not claim to select applicable recipes. The descriptions
explain those existing selectors and parameters; they cannot introduce flags,
defaults, constraints, executable validation, or a new selection algorithm.
The host still validates the actual RepairPreviewParams and the recipe's owned
evidence/precondition/edit-scope requirements. Additional recipe parameters in
a future profile require their own owned execution and identity succession.

This resolves the catalogue gap for the parameters applicable to the selected
product profile. It does not promise arbitrary configuration from the prototype.
Independent review must assess that interpretation against R06 rather than
silently treating an empty parameter list as full delivery.

## Report and security duties

Names, descriptions and parameter descriptions refuse C0/C1 controls, U+061C, U+200E/U+200F, U+2028 through U+202E, and U+2066 through U+2069. Tags retain the selected CanonicalIdentifier grammar. Admitted text remains inert, including markup-looking characters. The renderer must apply its existing HTML/script-context escaping
and CSP rules; a catalogue never supplies HTML, executable hooks or remote
assets. Public authored description text is distinct from repository-declared
configuration and secrets (RP-DO-04 remains a separate security redaction owner).

Report carrier successors must add the receipt and selected descriptor records,
replace the four feature-state placeholders, preserve exact source identities,
and apply the existing bounded exploration prefix/disclosure policy. Unknown
descriptor rows remain explicit; loss of a catalogue never becomes absence of a
rule/capability/recipe. All report bytes, generator source maps, owner selectors,
coverage rows, core build metadata and tests require coordinated acceptance and
integration. This candidate is not a delivered browser catalogue.

## Correction02: singular native release authority

This adds a **proposed authenticated release association**, not a claim that the
old contribution index already owns capabilities. The same authenticated release
input that supplies ReleaseCapabilityRegistryV1 supplies exactly one presentation
closureId for a registry digest and platform. That release-owned association is
retained with the Run's native release context. It is never derived from a caller
catalogue, file path, package name, current installed release or a declaration set
provided by an extension. The designated closure must belong to the admitted
Run Plan.semanticClosures; if supplying descriptions introduces a new closure,
that closure must be selected before Plan identity is minted. No extra closure
may be injected into an already retained Plan.

The reference joins the registry's existing schema, canonical SHA-256, registered
capability/mode cells, Run-selected digest, one designated closureId, selected
semantic closure membership and same platform. A capability description key must
be declared by that release, and its listing must be in the designated closure.
A second closure with contradictory text is refused even if it is independently
signed and declares the same key. Rules and recipes in other closures remain
possible, but those closures must have no capability declaration or description.
The selected report includes the registry digest and exact immutable closure
receipt. Its selected keys must be declared and must occur in the admitted Run's
selection. Its expected capability authority must match exactly.

The reference's selection dictionary models trusted retained host custody. It
does not authenticate the registry or derive Plan membership from actual Run
closure. Product implementation must construct private admitted handles, retain
the release association, and bind the report's existing CapabilityCatalogV1
registry source to it. Caller-provided copies of these dictionaries are not
accepted runtime authority. This release-association addition and its retention
must receive independent review and source selection before integration.
Historical Runs lacking the retained association disclose unavailable metadata;
existing identities and historical bytes are never rewritten.

## Correction02: source and descriptor states

The retained-source lookup returns exactly retained, not-retained or corrupt.
Missing/purged/expired retained bytes are not-retained; invalid content, an
association mismatch or a corrupt retained source is corrupt/refused. A retained
catalogue receipt is required for retained state. A valid admitted closure whose
**both** delivery tree and closure.tree omit the reserved path has
`no-catalogue-declared`; it is not a retention failure. A tree disagreement
refuses. Present-but-invalid bytes never downgrade to no-catalogue-declared.

Every selected key is unique, declared in the admitted index and selected by the
Run. Missing a descriptor for such a key in a retained listing yields
`descriptor-not-declared`. Metadata absence does not imply capability, rule or
recipe absence. The projection includes the complete receipt with tree,
platform and protocolMajor; the final report byte budget must include it.

## Root evidence and limits

The corrected reference passes 16 test groups over twelve pinned sources. Added
cases exercise two competing closures, registry/Plan/platform substitutions,
Run-selected-key checks, undeclared capabilities, all missing-data states,
delivery-tree omission and hostile text controls. These are synthetic host
contexts; actual signature, release/Run admission, retained lookup and browser
rendering remain implementation duties.

The previous review's CAT-M3 removes the canonical-size check after parsing.
The check remains. Under this exact codec, canonical serialization is no longer
than admitted raw JSON: insignificant whitespace and optional escapes can only
shrink, integers have their unique spelling, and canonical JSON uses minimal
escaping. The raw 4 MiB cap therefore already enforces this particular size
bound. A surviving deletion is not, by itself, a reachable size bypass. Root
will disclose that redundant guard instead of inventing a changed codec fixture
to claim a behavioral kill. CAT-M6 (undeclared capabilities) now has a dedicated
permanent counterexample. Independent review should confirm this classification.

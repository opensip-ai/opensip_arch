# Presentation catalogue owner proposal

Root candidate for RP-DO-01, RP-DO-06, RP-DO-07 and RP-DO-08. Not accepted or
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
admitted ruleProgramRef, including semanticsMajor and programDigest. Capabilities
use their declared capabilityId inside that same closure. Every descriptor key
must exist in that closure's admitted declaration index. Metadata cannot invent
an activated rule, a capability, a supported mode or a recipe.

An associated receipt names closureId, componentManifestDigest, the exact listing
Blob and trustOrigin (retained-generation, installed-signed-release or
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

## Recipe selectors and applicable parameters

The selected RepairPreviewParams already define the applicable inputs:
`evidenceSource` (exact Run or earlier workflow step), `recipe` (full RecipeRef),
and `targets` (1–4096 distinct finding fingerprints). There is no generic recipe
keyword-argument object in this profile. This proposal does not invent one.

Each recipe descriptor supplies its name/description/tags, a
`finding-fingerprints` selector with limits copied from the selected target
schema, and human descriptions for exactly `evidenceSource` and `targets`.
The report shows the full host-bound RecipeRef separately, along with the actual
admitted selected inputs when viewing a particular preview. The descriptions
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

All names, descriptions and tags remain inert text, including markup-looking
characters. The renderer must apply its existing HTML/script-context escaping
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

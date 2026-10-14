# B1A-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS**

Subject manifest: `c86c2aa060f60fc7a2d48a9aa03f3a0a35ab26ee50b7ee9f7112e63470e93b7a` (449 bytes; one member). Rehashed the manifest and 11221-byte PLAN-r1.md; the member hash is `1068bcb363c764063b96b63020503ab5221035d6e81aa97875117103da99932e`. Both match. Product HEAD is the requested `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean; architecture HEAD is `0deeb0d32fbb6562b975114f806d0c3f49892b3a`.

## Required findings

### B1A-PLAN-R1-RF-01 — Profile admission has no specified typed authority

Locations: §1 ResolverInputV1.release and §3, line 84.

The plan says profiles and capability availability come from an admitted input whose type is NE's ReleaseCapabilityRegistryV1. The actual accepted schema, in native-evidence.schemas.v2.json, defines an array of capability-declaration rows, with capabilityId and languageModes. It has no profiles collection or profile-membership representation. NE:1014–1023 and AQ:55–77 give it capability-availability authority; AQ also describes the matrix-defined default profile. PCM's test/reference registry is a different object with separate profiles, capabilities, packs and waivers.

As written, the profile lookup needed for CONFIG_PROFILE_UNREGISTERED cannot be implemented from the named type alone. Define the host-internal typed input and the trusted source of profile/default admission separately from the accepted capability-availability rows, or identify the unresolved prerequisite. Do not extend the accepted release schema or invent release-specific profile content under this implementation plan.

### B1A-PLAN-R1-RF-02 — Host-built flags are omitted from exhaustive host-invariant routing

Location: §4, lines 88–93.

MB item 4 explicitly says an invalid compiled default, environment layer **or host-built flags document** is a host invariant. AQ §1 likewise distinguishes invalid external input from invalid host-generated internal layers. The plan lists only invalid compiled defaults, missing defaults and invalid resolved semantics in its host-invariant bullet; generic schema/allowlist/path failures are listed as CONFIG.INVALID external refusals.

A typed FlagLayerV1 limited to workspaceRoots does not by itself prove that a vector is nonempty or a logical path is valid. Specify whether this is an already-validated type with host-invariant construction failure, or validate its invariants in the resolver and route failures to the existing X12 row 4. Add a negative control and retain external-carrier CONFIG.INVALID behavior. No new public code is necessary.

### B1A-PLAN-R1-RF-03 — Flag invariance conflicts with workspace-root semantics

Location: §6, line 110.

The digest control says “flag-only selections” leave the digest unchanged. The plan's only M3 configuration flag is --workspace-root, mapped to discovery.workspaceRoots by MB item 2. This semantic leaf is in the digest; changing its winning valid value must change the digest. Invariance is appropriate for the non-configuration flags MB item 6 excludes, or for moving the same winning value between layers, but not for every flag-only configuration change.

Narrow the invariance claim to excluded selector/authorization/presentation flags and add an explicit workspace-root sensitivity case. Keep provenance-only invariance and allowedScopes order sensitivity.

## Findings that passed

The intended product scope matches MB:875: pure pipeline, resolved semantic/operational values and provenance, digest, registries, vectors, remedy and X12 order. Carrier custody/capture, installation access, terminal-mode computation and the environment structural check remain B1-b work. The constant-empty environment does not introduce a seventh input. The input boundary needs the profile and flags refinements above, rather than moving B1-b mechanics into B1-a.

The §2 prerequisite is real. RegisteredSchemas::from_sources requires exactly its 48 SOURCE_PINS in order, with whole-document lengths/hashes and IDs, then compiles the selected documents. The product generation registry has 40 sources; the admission registry and admission source map have 48. PCS and the preview configuration carrier are absent from the current runtime set. verify_design.admission_sources requires the complete admission registry to be byte-identical to the accepted architecture copy named by registryArchitectureSource.

The current accepted copy is rust3-identity-materialization-r1/admission-registry.json, 17170 bytes, SHA-256 `a85500ef669bbbfe7e8993e3ad738f5f364ce048131c5d7aaeb143bc00669335`, byte-equal to the product registry. A separately reviewed successor copy adding the two exact schema IDs is a sound design prerequisite; the existing materialization successor demonstrates that form. Sorting and source-map/pin coverage are enforced. Rejecting a hand-written substitute or widening the private Program API is consistent with the pinned shared mechanism.

PCS is 10262 bytes, SHA-256 `591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d`, ID urn:opensip:product-configuration:2. The preview carrier ID is urn:opensip:preview-configuration:1. PCS, PCM and its checker match their canonical-path entries in candidate-subject.v45.json.

The classification vocabulary matches DRC:588–589. Reviewed mapping plus exhaustive leaf drift checking is consistent with FW-13. Capability IDs and per-mode NOT-SELECTED cells come from NCM; CINV flags are generated with source pins and a check mode. The existing generated Native2FrameworkRecognitionResultV1RecognizerId exists and can be reused without a new list. The empty waiver registry and release authentication boundary are appropriate; the profile input remains the required clarification above.

The profile reference refusals can map to existing CONFIG.INVALID with the stated subjects; no CONFIG.PROFILE_* generated detail exists. The existing X12 host-invariant shape remains available. `refusalsNoNewCode` is true for the selected code vocabulary; RF-02 concerns incomplete routing, not a need for a new code.

Using accepted PCM for byte expectations is correct. Its checker contains the AQ:183–187 cases, and its code confirms the normalization, provenance exclusion and five-section digest recipe. MB-only behavior must retain the plan's explicit no-PCM-vector label; PCM is reference evidence, not authority to override layer allowlists or release shapes. Schema-one projection remains governed by MB item 11 and HFC §3. The planned per-step, layer, CI, schema-one, remedy and O-4 controls are useful; test coverage is not accepted until the incorrect flag invariant and missing internal-flags refusal case are corrected.

The plan chooses no S-OP-5 field or release content, claims no authentication, writes no code, makes no binding and changes no law. Its B-S10-before-product sequence preserves separate review, lock and inventory work. No product qualification follows.

## Review boundaries

Used read-only file/source reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, generators, model/checker scripts or lane were run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, the stage nor control files was edited. Only this review directory's REVIEW.md and review.json were written.

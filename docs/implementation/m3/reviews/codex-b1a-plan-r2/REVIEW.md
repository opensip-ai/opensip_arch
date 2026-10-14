# B1A-PLAN-r2 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: one.

Subject manifest: `46917474b9fa21fe53ef277975b501fdde1f8785af282b438f22bdbe867c29f1` (642 bytes; two members). Rehashed both members. PLAN-r1.md is byte-identical to the round-1 subject; PLAN-r2.md is 15719 bytes, SHA-256 `9073131bbe12af09101b9327912b9d99940ae5a6821c10c78454112ebc75c636`. Verified product HEAD `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean, and architecture HEAD `0deeb0d32fbb6562b975114f806d0c3f49892b3a`.

## Findings resolved

**B1A-PLAN-R1-RF-01:** The resolver no longer takes a capability-availability registry as a combined profile source. The accepted ReleaseCapabilityRegistryV1 shape remains unchanged and owned by its admission/authentication unit. Unavailability is disclosed rather than used to narrow or reject the required request. The profile spelling is the contract-named `default`, drift-checked against AQ; no release-specific profile schema or content is invented. Compiled defaults are supplied through the trusted internal layer, separately from availability.

AQ §1.1 and NE §1.4 fix default capability selection by the matrix, including UNSUPPORTED-TYPED cells, rather than by the available release rows. The plan's signed-profile input supplies values through that existing contract boundary; it grants no authority for a signed release to narrow the required default selection. Its capability membership/cell checks and later availability disclosure retain their separate owners.

**B1A-PLAN-R1-RF-02:** Defaults and flags now undergo the same admission stages as carriers, with the internal/external origin determining their public refusal row. Invalid internal layers route to the existing host-invariant shape. The plan explicitly covers empty workspaceRoots, malformed flag paths and unknown default keys with negative controls; it separates M4's prior flag-syntax refusal. The constant-empty environment is retained. No new code is needed.

**B1A-PLAN-R1-RF-03:** Invariance is limited to excluded selector/authorization/presentation flags, operational fields and provenance-only moves. Changing the winning workspaceRoots through --workspace-root is explicitly sensitive. Canonical-set permutations remain invariant, allowedScopes order remains significant, and the five semantic sections remain present.

## B-S10 and implementation scope

The admission prerequisite remains real: runtime RegisteredSchemas uses the complete pinned admission set, not the smaller generation set. The current product has 48 admission sources and 40 generation sources; the eight admission-only entries include enumeration-plan-v1. verify_design requires the admission registry to match its selected architecture copy and requires generation/admission source-map coverage and pins.

The expanded B-S10 plan uses the existing full-materialization precedent: accepted registry and exact changed-product copies, generated contracts/closure and check evidence, followed by byte-exact product materialization and separate binding. PCS receives its MB-required generation row; preview v1 is explicitly admission-only. No schema ID, release schema or private Program API is changed to bypass the pin boundary. B-S10 remains a separately reviewed design unit; this acceptance does not bind its future bytes or certify unrun generation.

The remaining scope still matches MB:875: pure eleven-step configuration resolution, semantic/operational partition, provenance, digest, generated/drift-checked registries, PCM vectors, remedy and X12 order. Carriers/custody, installation access, mode observation and environment structural enforcement remain B1-b work. The input consumes captured bytes and host-built layers without introducing filesystem or environment authority.

The two DRC classes, exhaustive PCS-leaf coverage, pinned NCM capability/cell generation, CINV flags, existing recognizer enum and empty waiver registry retain MB item 8's source and refusal discipline. Profile reference refusals map to CONFIG.INVALID with explicit subjects; internal faults retain X12's host-invariant row. The exhaustive match adds no public code.

PCM remains the accepted oracle for representable byte vectors; the plan explicitly labels MB-only cases with no PCM vector rather than inventing reference expectations. Together with the corrected controls, the retained layer, per-step, CI, schema-one, pack-admission-order, remedy and O-4 tests cover the required plan-level controls. Actual execution and exact implementation acceptance remain future work.

## Non-blocking observation

**B1A-PLAN-R2-NBO-01:** In §2, the retained “B1-a then adds” summary says “their rows in registry.json, source-map.json, admission-source-map.json and admission-registry.json”. Align this wording with the new explicit rule: PCS uses both generation and admission paths; preview v1 uses admission only. This is non-blocking because the new explicit admission-only statement settles the intended selection, and B-S10's actual materialization is independently reviewed before binding.

## Scope and boundaries

The plan writes no code, makes no binding, changes no law and selects no S-OP-5 field, release content or B1-b mechanics. No authentication, qualification or completed implementation is inferred.

Used permitted read-only file/source reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, generator, PCM/checker or lane was run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, stage nor control files was edited. Only this directory's REVIEW.md and review.json were written; round-1 artifacts were not modified.

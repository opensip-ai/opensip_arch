# Source44 successor review: ACCEPT

**Verdict: ACCEPT.** There is no MUST issue, no SHOULD issue and no blocker. This is source-level acceptance only: it grants no blind reconstruction, application, readiness, implementation authorization or product qualification. The builder finished with no gaps, and no child command is still running.

**Deliverables:**
- `/private/tmp/opensip-design-corrections/claude-independent-design.v44/review.json`, sha256 `33a5c2ce1e92d072a73d88c6e97bae693f75186e5e291b07b5e1258dc5d5c0a8`
- `/private/tmp/opensip-design-corrections/claude-independent-design.v44/review.md`, sha256 `01380c1d5b22ef895da23e32b5cddbd04c611c655810c9febd9b624227501882`

## Subject
- **Manifest and archive:** manifest `e873c8db…` and archive `c21d0491…` match the header; `verifiedManifest` is true. All 12,919 members (738,157,930 bytes) match on my copies.
- **Parent and delta:** parent43 `db43ee76…` is declared and verified, and the delta is exactly 24 changed, 6 added, 0 removed.
- **Pins:** every pin in all five ledgers matches (16 changed, 5 added).
- **Copies:** all three working copies re-verified unchanged after the last probe run.

## Focus A: provider wire
- **Handshake fields:** TypeScript Hello/HelloAck (major 2) keep every inherited delivery.v2 member and add only the token array and `identityVersions`. Rust Hello/HelloAck (major 3) keep every rust v2 member plus the three registered ones.
  - Supersession is narrow: exactly three registered definitions, named in §0.
  - The artifact majors (1 and 2) are superseded selectors in §0, not a contradiction.
- **Limits and contract digest:** the TypeScript map is exactly the 10 delivery.v2 limits; the Rust map is 24 rust v2 limits plus the 8 from §9.3, 32 in all. The contract digest is the raw SHA-256 of the artifact bytes; a canonical-JSON digest would differ.
- **Joins and tokens:** descriptor and Plan-identity joins, sorted signed-row tokens and `identityVersions` echoes were each tested field by field with independent oracles. The wire probe ran 130 rows with 0 failures, and every refusal follows a working positive case.
- **FactBatch:** TypeScript FactBatchV1 (commitment recomputed independently), Rust FactBatchV2 and negotiated V3 share one candidate CBOR projection.
  - The occupancy gate skips junk, wrong-commitment and cross-language batches that the wire law refuses, so a skipped batch is not validated.
  - Apart from its docstring and delivery label, the gate behaves exactly as in source43.
  - Earlier generic "FactBatchV2" readings are described as ambiguous under the old bytes, not relabelled as reader bugs.

## Focus B: provider startup
The startup probe ran 162 rows (151 checks, 11 observations) with 0 failures.
- **OpenUniverse and UniverseAccepted:** correlation fields, handshake joins and the universe key (recomputed independently) behave as published. Native-context and repository-resolution applicability per language is correct.
- **Derived modes:** includes empty dependency custody and prepared and imported-descriptor preparations. `NativeContextVerified` joins hold.
- **Pre-Analyze native-context mismatch:** the payload, phase, correlation, clean zero-exit/EOF versus faults, and the host-derived provider-unavailable coverage all check out.
- **Coverage and cancellation:** `Coverage` vs `CoverageV3` frame names, whole-payload vs entry schemas, and the inserted cancellation interval are correct.
- **`rustCommitHash`:** the 64-hex Plan/handshake/universe chain needs no join with the 40-hex toolchain field.
- **Contradiction check:** no cross-owner field or route contradiction was found. The registered `UnavailableReasonV3` enum looked like one, but it is an unused list of added reasons and the published per-language enums are consistent with it.

## Issues and dispositions
- **ADV44-01 (new advisory, non-blocking).** Planning layer v12 binds the new TypeScript order table but not the Rust `protocol3-transitions.v1.json`, whose normative OpenUniverse state-update text changed.
  - No normative content is lost: the changes restate law already bound through native-evidence §9 and the startup schema, and the transition rules are unchanged.
- **ADV42-01: retained advisory.** Selector lines are byte-identical and the capture-join measurements are unchanged; routing to `crates/host/src/analysis.rs` is correctly scoped.
- **S40-01 and ADV40-01:** remain resolved.
- **OBS43 and older ids:** each has a current disposition; there are 34 in total.
- **OBS44-01…11 (not defects).** These cover:
  - the reference comparison;
  - root runs executed from a working tree;
  - the reference's trusted host inputs, including planned stages converted verbatim and universe members not re-joined to a Plan;
  - inherited cancel and exit asymmetries;
  - stage-stream and coverage commitments not recomputed;
  - the registered superseded definitions;
  - the root clarification's before-bytes, which were not diffable;
  - the renamed gate label;
  - the package verification differing from root only in package identity and file count.

## Package21
- **Manifests:** formal44 and the files-only projection are distinct objects with equal members. The rebuild used package15 plus the native-v2 overlay on frozen v44. Packages 16–20 are preserved.
- **Metadata binding:** it changed no export store or current replay-helper byte.
- **Exports and RunIds:** all 17 exports are byte-equal to package20, and the measured RunIds equal source43. Identities are unchanged and nothing was reminted.
- **Tool runs:** 7 queries and 9 membership probes pass, and the probe runs 34/34.
- **Limits:** the four TypeScript map negatives are executed. The Rust map negative and the partial and/or/not helper are unexercised, count/all are unimplemented, and two-binding qualification is incomplete. All 30 grades stay PENDING.

## Checks and rows
- **Reference groups:** all six groups and 17 children pass (native 477/477). Every group output is byte-equal to root and codex; 15 of 17 children are too, and the remaining two differ only in path fields.
- **Planning and inventory:** both pass (322 mappings, 198 files, 20 packages). v8–v11 are byte-identical to source43.
- **Scope probes:** the ten ported probes match my source43 receipts, apart from the policy probe's copy-identity row.
- **Rows:** 107 rows, 53 new-44 and 54 unchanged-43. Every unchanged-43 row names its governing owners, and those owners are checked byte-identical. Every row has `appliedByThisReview` and `finalApplicationOutcomeGranted` set false.
- **TCB-SCOPE-01:** assessed once with 13 dependent rows; not rejected.
- **Retained obligations:** 32 gates and 54 recovery cases stay unperformed, and condition 5 is not met. D9 remains a mandatory future implementation obligation. Final application needs a new, different Claude origin.

## Limitations (disclosed in the review)
- **Cases file:** `native-cases.v2.json` was read only by named ranges plus a structured listing of its startup cases. Its full 6,274-line diff was not read, though all 477 cases executed.
- **Unintended search sighting:** one search surfaced file names and one signature line from snapshot-internal historical review copies, including a folder named `blind-corrections-author.v1`. None was opened or used.
- **Failed attempts:** three first attempts were preserved and not counted: reference comparison, package probe and wire probe.
- **Denied commands:** some shell commands were denied and replaced with direct reads or individual runs.

# CODEX2 Review — D2b-4a Rust3 base receive unit r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### D2B4A-R1-RF-1 — Enforce the examined-universe subject-count echo before publication

The base receiver does not compare `CoverageResultV3.entry.examinedUniverse.subjectCount` with the subject inventory in the corresponding host-supplied stage context. `Rust3Receiver::new` extracts each stage's requested keys but discards `analysisDomain.subjects.len()`, `RequestedKey` carries only `subjectScopeCommitment`, and `entry_echoes` checks only `examinedUniverse.subjectScopeCommitment`. The selected `ExaminedUniverseV1` schema accepts any `uint64` subject count.

A worker can therefore change `subjectCount`, recompute the frame's received-entry `coverageCommitment`, and pass schema admission, `entry_echoes`, the commitment check, accounting, and P3T. The resulting `CoverageV3` is published even though its examined-universe echo disagrees with the immutable host context. The same shared helper leaves post-Analyze `Unavailable` and `BudgetExhausted` terminal coverage exposed. This is a pre-publication D2b-4a duty: accepted LD-D2B-15 assigns PER-KEY-SCOPE2's worker echo to contextual admission, the duty table says `examinedUniverse` must equal the requested context, and the retained native law requires `examinedUniverse.subjectCount == len(D.subjects)` so a narrower claimed partition is detected.

Retain the expected base-stage subject count from `analysisDomain.subjects` and require every normal and terminal coverage entry's `examinedUniverse.subjectCount` to equal it before accounting, table matching, or publication. A successor should include a well-shaped wrong-count control with a recomputed correct coverage commitment for `CoverageV3`, the corresponding terminal path coverage, and a compiled runtime mutation that removes this comparison; each must be caught at contextual admission.

## Frozen-subject integrity

The requested `subject.json` SHA-256 is exact: `a8501ba45200456f4ec6bad8bf59d5434fadd67f429c9c6e89908e9a050e2c70`. All 481 declared members are present and unique, with exact byte counts and SHA-256 values and no undeclared frozen-subject members. The 20 candidate paths match `product-map.json` and the named worktree byte for byte. The worktree and product main are at parent `ca6f5be9ded80c50a143b2f219258c95c80db2e6`; the architecture checkout is at `278d1a27b4cea095b37eed09e7109d8a98be7696`. The frozen Rust provider protocol bytes equal the accepted raw authority.

## Review assessment

The remaining reviewed mechanisms are consistent with the scoped receive-side authority: strict Rust3 profile/depth/envelope selection, all 26 frame selectors and 13 worker conversions, exact Hello and recursive startup echoes, retained framePrecheck/T016/T020 checks, checked sequence and live counters, ProviderFault's joint observation window, Cancelled send-phase correlation, relation-payload restrictions, candidate/anchor/occupancy admission, response and full-wrapper spool accounting, received-slice commitment provenance, and fail-closed publication ordering. The selected owner evaluator and derived schema-work bound retain the raw source pin gate and do not add an unrelated transport cap. The single `BTreeMap::from` census row is an ordinary selector-map construction, so the conservative 452-to-453 census update does not mint identity authority.

The archived final source pins cover all 20 paths. The current base/candidate suites report 270/81 versus 317/86 tests with equal empty failure sets; full component, identity, docs, operability, Clippy, design, diff, repository, public-binding, and ten compiled runtime-mutation evidence is preserved. Those controls do not mutate or assert `examinedUniverse.subjectCount`, so they do not close D2B4A-R1-RF-1. The older cross-worktree stale-artifact compile failure is correctly superseded by dedicated-target evidence. The whole-workspace CLI guard failure is inherited and outside this unit; the separately accepted but unintegrated CLI repair is not relied on here.

D2b-4b's builders, schedule, sender, participant and limits, D2b-4c's FA-2/reference-scope/successor work and replay, H's semantic admissions, production integration, the additive inventory/description/status successors, and product qualification remain outside this verdict.

## Non-blocking observations

None.

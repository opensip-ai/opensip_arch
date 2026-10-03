# CODEX2 review — M3 unit plan r1

**Verdict: REQUIRED-FINDINGS.** The major M3 responsibilities have owners and most open-choice recommendations are sound. Acceptance requires enforcing the pre-law/report prerequisites, assigning the actual bundled preview pack, reconciling O7 timing and deriving the critical path from the repaired graph.

Reviewed `docs/implementation/m3/M3-PLAN.md`, 28,398 bytes, SHA-256 `65bf6ac57a663707a2eea47fba7e293c595daa3ac9e703b1e4ed511d38496830`, against product `eb0d503`. This is a method review of the planning record, not an acceptance of any successor law. Operability r2 is pinned to `PLAN-r2.md`; the live `PLAN.md` advanced to r3 during inspection.

## C2-M3-R1-01 — Gate M3-L on all protocol-freeze prerequisites (P1)

**Location:** [m3/M3-PLAN.md:74](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:74); related lines 76, 130, 134.

M3-L depends only on M3-S, and S depends only on the medium subset of T2. Q0 is an independent lane filled when a reviewer is free. The recommended start can therefore accept L before the complete T2 manifests, harness design, exploratory-envelope design and catalog draft required before protocol fixation.

**Evidence:**

- [m3/M3-PLAN.md:22](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:22): The plan itself summarizes the full pre-protocol obligations.
- [m3/M3-PLAN.md:75](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:75): S requires only medium T2.
- [m3/M3-PLAN.md:76](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:76): L lists only S as its dependency.
- [m3/M3-PLAN.md:115](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:115): Q0 is scheduled in the lane that fills reviewer gaps.
- [analysis-quality/PLAN.md:480](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:480): The accepted quality plan requires pinned T2 including multi-repo and Python, harness design and rule-catalog draft before the M3 provider protocol is fixed; its dependencies include D3, D13 and the D2 draft.
- [operability/PLAN-r2.md:333](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r2.md:333): The provisional operability schedule also requires the S-OP-2 vocabulary draft and applicable SDK join before the protocol law.

**Fix:** Add an explicit M3-L acceptance gate for completed M3-T2 manifests (including multi-repo and Python), M3-Q0 and the required D3/D13/D2-draft dispositions, alongside S. Record the operability vocabulary/SDK prerequisites at the same gate. Drafting L and probing the compiler can remain parallel; accepting the law must wait for the gate. Update the recommended start and lane priorities accordingly.

## C2-M3-R1-02 — Approve the spike's evidence carrier and runner before measurement (P1)

**Location:** [m3/M3-PLAN.md:74](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:74); related lines 75, 132, 133.

M3-S emits an exploratory envelope and is tagged Q6, but its only prerequisite is medium T2. Its envelope definition and runner are owned by Q0, and the owner sign-offs that block those uses are only listed later as open actions. Following the proposed order can produce the spike's report before the accepted quality plan allows that report or Q6 measurement.

**Evidence:**

- [m3/M3-PLAN.md:74](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:74): Q0 owns the exploratory envelope and D12 runner.
- [m3/M3-PLAN.md:75](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:75): S measures startup/sealing/replay, records an exploratory envelope and names Q6, but depends only on medium T2.
- [analysis-quality/PLAN.md:419](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:419): The separate exploratory envelope binds observations, versions, corpus/harness identities and metric definitions, and has explicitly non-qualifying standing.
- [analysis-quality/PLAN.md:534](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:534): D12 blocks Q6 measurement.
- [analysis-quality/PLAN.md:535](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:535): D13 blocks M3 exploratory reports.

**Fix:** Make the applicable Q0 envelope design and D13 approval prerequisites to S's report, and D12 runner approval a prerequisite to samples reported as Q6. A preliminary toolchain feasibility probe can run earlier if separately scoped and labelled; distinguish it from the measured INC-7 evidence used to accept L and revise the estimate.

## C2-M3-R1-03 — Separate and implement the mandatory M3 preview pack (P1)

**Location:** [m3/M3-PLAN.md:79](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:79); related lines 85, 86, 149.

M3-I combines X12c with a non-authoritative draft catalog, says the product pack stays at M5, and depends on H. J2/J3 do not depend on I. X12c is required M3 work consisting of the actual bundled preview pack, not just its contract row. With the current empty registry, real pack admission and Plan construction cannot succeed, so the guarded host pipeline lacks a mandatory input and an explicit implementation/acceptance dependency.

**Evidence:**

- [m3/M3-PLAN.md:57](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:57): The product bundled-pack registry is empty.
- [m3/M3-PLAN.md:85](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:85): I owns 'X12c's pack row' within a non-authoritative evaluator/catalog unit; the product pack is said to stay at M5.
- [m3/M3-PLAN.md:86](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:86): J performs configuration, Plan construction, evaluation and durable publication but lists no I/preview-pack prerequisite.
- [policy-admission-x12/PROPOSAL.md:125](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/policy-admission-x12/PROPOSAL.md:125): Pack admission runs before provider spawn, snapshot, Plan construction or evaluation; the Plan builder takes its policy from an AdmittedPack.
- [policy-admission-x12/PROPOSAL.md:191](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/policy-admission-x12/PROPOSAL.md:191): X12c requires opensip.preview.typescript.pack:1 and its bundled bytes, frozen preview rule IR, and a policy-language successor if its rule needs an unavailable relation or atom.
- [policy-admission-x12/PROPOSAL.md:198](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/policy-admission-x12/PROPOSAL.md:198): Placeholder/contentless bundling and a test registry reachable from release are forbidden substitutes.
- [cli-enablement-x11/PROPOSAL.md:77](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/cli-enablement-x11/PROPOSAL.md:77): The M3 successor inherits X12c, X12d and finalization of a real Run.
- `opensip@eb0d503:crates/evaluator/src/policy.rs:1086` (pinned source): Named admission returns NotBundled when no matching row exists.
- `opensip@eb0d503:crates/evaluator/src/policy.rs:1399` (pinned source): check_plan_pack refuses an unbundled Plan policy ID.

**Fix:** Split X12c's preview-rule freeze/contract successor and bundled-byte/registry implementation from the broader exploratory catalog. Explicitly assign the code and self-checks, retain any conditional policy-language successor, and gate real Plan/pipeline demonstrations on the admitted preview pack plus X12d. Keep the broader product catalog at M5. Avoid introducing a dependency cycle through H/C4: the preview-pack definition/bundling prerequisite must not require completed live fact production.

## C2-M3-R1-04 — Resolve O7 at the stated owner-decision gate (P1)

**Location:** [m3/M3-PLAN.md:32](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:32); related lines 76, 166.

The summary requires O7 before the protocol law, but the owner-decisions section permits L and F/G to proceed before O7 and moves the block to X. Unchanged wire frames do not establish that the owner's confinement choice can be deferred: that choice can affect process launch, permitted workloads, runtime closures and containment controls. The plan contains two incompatible schedules.

**Evidence:**

- [m3/M3-PLAN.md:32](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:32): O1 and O7 are to be decided before the protocol law.
- [m3/M3-PLAN.md:166](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:166): The recommendation explicitly says O7 does not block L or F/G and blocks only X.
- [operability/PLAN-r2.md:300](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r2.md:300): The provisional plan leaves the threat-posture decision to the owner and says it is needed before M3 providers ship.
- [operability/PLAN-r2.md:333](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN-r2.md:333): Its milestone table puts the owner's O7 decision before the M3 provider protocol law.

**Fix:** Preserve O7 as an explicit pre-L owner-decision prerequisite under the incorporated operability schedule and carry the decision's effects into D/F/G and their controls. If the lead proposes a later gate, resolve that scheduling change explicitly with the owner and the operability plan before adopting it; do not infer permission to defer it merely from unchanged wire contracts. Follow the subsequently accepted operability revision.

## C2-M3-R1-05 — Recompute the critical path from the actual dependency graph (P2)

**Location:** [m3/M3-PLAN.md:79](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:79); related lines 83, 105, 107, 128.

The asserted 14-subunit path is not a dependency path through the table: P0 jumps directly to C1 despite C depending on B; C2 jumps to G1 despite G depending on all of C and on D. C3/C4 and the supervisor join are missing. H and J also have law/producer prerequisites not represented. The serial count and 3–6 week calculation therefore lack a graph that supports them.

**Evidence:**

- [m3/M3-PLAN.md:79](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:79): C depends on B and L and is deliberately kept together because Plan binds its four parts.
- [m3/M3-PLAN.md:83](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:83): G depends on the complete C unit and D.
- [m3/M3-PLAN.md:84](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:84): H requires C4 and a first producer.
- [m3/M3-PLAN.md:86](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:86): J requires the producer units and carries J1's successor law.
- [m3/M3-PLAN.md:105](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:105): The proposed path omits B, C3/C4 and D before G1.
- [m3/M3-PLAN.md:107](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:107): The path is counted as 14 serial subunits with one law.
- [m3/M3-PLAN.md:128](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:128): The wall-clock estimate is derived from this path.

**Fix:** After repairing the preceding prerequisite edges, draw or tabulate the subunit DAG with joins, separating law acceptance, code prerequisites and final demonstration prerequisites. Recompute the longest path under stated duration assumptions, including the host/discovery branch, complete input admission, supervision, preview-pack work and test/harness joins. Parallel prerequisites need not all become serial steps; show which branch determines each join. Mark any estimate that cannot yet be recomputed as provisional rather than retaining the unsupported serial count.

## Nonblocking observations

**C2-M3-R1-N01 — Make imported prepared-mode fixtures and host checks explicit.** The library-level dependency-source import and externally prepared inert sets are sound M3 choices; neither requires moving the public import/native-prepare commands from M5. C3 names PO-0 alone, however. Spell out PO-1 pre-Plan staleness handling, PO-2 failed rows, PO-3 declared provenance/import identity, and PO-4 generated-file bindings/bounds, with the appropriate host/provider split. Name the harness recipe that produces, pins and regenerates the imported sets. Q6 must distinguish prepared core-analysis from first use and preparation-invalidating edits; missing preparation can be reported as unavailable or low yield. Sources: [product-v1/native-evidence.md:1833](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:1833); [product-v1/native-evidence.md:1853](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:1853); [product-v1/native-evidence.md:2535](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2535); [analysis-quality/PLAN.md:340](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:340).

**C2-M3-R1-N02 — Distinguish late adjudication from a late exploratory report.** X depends on all units, including M. Therefore a delayed M run/report delays X. An exploratory report can instead complete with unclear or INSUFFICIENT-EVIDENCE outcomes while more expert adjudication remains pending. Clarify that as the intended reason human labeling need not delay exit; do not turn exploratory Q2 into a qualification threshold at M3. Sources: [m3/M3-PLAN.md:91](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:91); [m3/M3-PLAN.md:190](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/M3-PLAN.md:190); [analysis-quality/PLAN.md:236](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:236); [analysis-quality/PLAN.md:419](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:419).

**C2-M3-R1-N03 — Name the remaining discovery/corpus preparation outputs.** T2/B broadly cover FW-14 and the discovery section, so this is a clarification rather than an established missing unit. Name FW-14's reproducible workarounds, manual-correction counts and positive/negative fixtures as reviewable outputs. B2's U-0..U-4 list should also explicitly preserve U-8 admitted boundaries and U-9 zero-config syntax fallback. Sources: [architecture/implementation-coverage.v1.json:8129](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/implementation-coverage.v1.json:8129); [product-v1/native-evidence.md:816](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:816); [product-v1/native-evidence.md:879](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:879).

**C2-M3-R1-N04 — Refresh operability references when its revision is accepted.** During this inspection operability/PLAN.md advanced from r2 to r3. This review pins the request's r2 to PLAN-r2.md; r3 still preserves the O7-before-law schedule. The existing promise to follow the accepted revision is appropriate. When rebasing, refresh the unit/successor list and source lines; r3 adds S-OP-12 for the cancellation/commit join. Sources: [operability/PLAN.md:378](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:378); [operability/PLAN.md:415](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/operability/PLAN.md:415).

## Coverage and recommendations checked

- The seven routed gates are preparation responsibilities at M3; qualification remains M6. BP:895 supports preparing G14 closures/refusal tests now while component installation remains M5.
- The missing grants, process, component and syntax modules have assigned implementation units (B3, D1-D4, E1-E3); no further hard missing-module gap was established.
- The stub providers and missing rustc-dev component are correctly identified at eb0d503. A feasibility probe before committing to compiler integration is appropriate; compatibility was not tested in this review.
- D15 correctly carries an X2 successor for the existing single-layout Git rule.
- Library-level user-named dependency import and declared external inert prepared sets are appropriate M3 routes while public commands remain M5.
- X11 creator/order/RequestId/backup-status work, X12d before X5, re-commit debt and the resume/repair writer are explicitly carried into M3. Complete CLI delivery, residency, Python support selection and AL2023 qualification stay at their stated later milestones.

The lane division is useful, and serializing lead run sets is appropriate while the crash matrix is active. The required findings concern the joins between those lanes and the evidence needed to finish them.

## Verification boundary

The subject hash matched the request before and after inspection. Accepted AQP r4 hash: `6daa6bd836ec851faff5d1cfe29727de8a99140183b8e91e0a6880fd633419b6`. Requested provisional OPP r2 hash: `a65ea9c7ff8da4315d9649d0fd79cfb81bfc773fe36dd2244e40d9e3d5ac814b`.

This review used static reads, including pinned `git show` reads at `eb0d503`, and two read-only supporting inspectors. No product code, build, test, spike, benchmark or project verification script ran. The real runtime home and 413 fixture were not accessed. No commit was made. The only output files are this review and its JSON counterpart in the requested `/tmp` directory.

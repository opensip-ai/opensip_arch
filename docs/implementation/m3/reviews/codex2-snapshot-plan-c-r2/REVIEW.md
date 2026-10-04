# CODEX2 — M3-C r2 law review

**Verdict: REQUIRED-FINDINGS.** Three corrections remain: distinguish pre-execution enumeration checks from inventory admission; cover X2's marker read in the capture rule; and separate archive-processing counters from protocol source-data counters.

Subject: `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, 102,443 bytes, SHA-256 `bf44ffe2680a33d729fc71580a0a1abd80d87eca959c92b42967dde339915070`. The preserved r1 subject matches the reviewed `ff9a5e8d…` bytes. All supplied pins match. Product inspection used Git objects at `30c5db1c1d2410135c5579f3a01ba6d152328bfb`; the checkout was not changed.

No repository edits, commits, delegation, product builds, cargo, tests or product-code execution occurred. The real home and the 413 fixture were not accessed. All writes are under this review directory. Scratch scripts use only the standard library for hashes and arithmetic; reading a reference implementation is not executing it.

## Required findings

### C2-R1 — Step 14 calls full enumeration admission before its output inputs exist

**Location:** PROPOSAL.md:655, 669; C4-T17 at :696.

Step 11 now correctly constructs the complete spec after the snapshot, imports, contexts and universes. However, step 14 adds `admit_enumeration` “before any provider.” That function takes more than a Plan and PlanId: `inventories` is a required argument (`enumeration-contract.v1.md:164`). It admits actual `SubjectInventoryV1` outcomes, not just the Plan's selection parameter.

The contract requires one inventory for every expected `(cellOrdinal, programOrdinal, kind)` (:111–121). IE:1464–1470 distinguishes the pre-execution selected locators from provider-attributed symbol declarations and examined paths. The reference function documents its inventory-join purpose at `enumeration_model.v1.py:584–612`, checks the inventory records at :854–889, and refuses every missing expected record at :1007–1009. Item 18 requires the imports-cell symbol inventories, so this is not a candidate-only, zero-inventory case.

With an available native program, step 14 cannot supply those outputs before its provider runs. An empty list refuses structurally; invented complete-empty inventories or fake unavailable outcomes would misstate the work performed. Having PlanId available is necessary but insufficient.

**Fix:** Keep `check_plan_pack` and the checks over Plan/parameter/context/binding inputs at the pre-execution boundary. Define their limited scope explicitly rather than calling the inventory-requiring admission function there. Perform full `admit_enumeration` after expected inventories have been produced/admitted, before evaluation, and again through Run closure/replay. Preserve origin-sensitive fault routing for those later inputs. Add a control with a nonempty available imports-cell symbol population that reaches execution without placeholder inventories and closes only with the actual admitted inventories.

### C2-R2 — The capture session starts after an existing project-file read

**Location:** PROPOSAL.md:72–86, 94–96, 643–649, 891.

The new session opens after X2 admission, “before the first project-file read,” and covers every such read. At the reviewed product commit, X2 admission already reads `.opensip/project-id.v1`: `project_admission.rs:872` calls `observe_marker`, whose :604 reads its bytes. `MarkerObservation::Present` retains the decoded project ID and metadata (:536–545, :612–615), not the raw capture handed to C1.

The law also expressly says the walk inventories `project-id.v1` (:891), because the current discovery rule does not prune `.opensip`. Thus the file is read once before the session and again when C1 inventories it. B1/B2/C2 session reuse does not cover that earlier X2 read. Moving the session earlier without a stated security interface would also contradict its required admitted-root/tracking prerequisite.

X2's operational status does not resolve this automatically: a file the law explicitly inventories is subject to its one-read rule. X2 owner rechecks additionally read the marker again (`project_admission.rs:797,818`), so the blanket source-read prohibition needs a precise boundary with those operational checks. The related B draft records `.opensip` treatment as a decision for C1; no exclusion can be assumed from that draft.

**Fix:** Decide the boundary explicitly. For an inventoried marker, retain and hand off X2's exact admitted marker capture/observation into the session, then reuse it under re-observation rather than performing a new source capture. Alternatively, define and successor-gate a lawful discovery disposition that keeps operational marker bytes outside the source inventory, while retaining any applicable project/config joins. State how mandatory X2 rechecks relate to the source-read rule. Name the required X2/B/C interface changes and gate them. Extend C1-T24 to an already registered project with a present marker, including a mutation across admission and sealing; pin every inventoried path's capture provenance, including X2.

### C2-R3 — Archive work is charged as if it were protocol file data

**Location:** PROPOSAL.md:429–435, 490.

The profile counts all decompressed tar bytes against the set's remaining `maxDependencySourceTotalBytes` and each physical header block against the same entry count used for files. Those are different quantities from the protocol's source entries and data bytes. NE:2876–2878 describes manifest entries and sealed data totals; NE:1663–1664 and NEM:1874 define file count and total bytes from logical files. Tar headers, long-name payloads, padding and end blocks do not become dependency files or their content.

An in-profile long-path file has both an `L` header and a regular-file header. A collection with 500,001 such files has 1,000,002 physical entry headers while remaining below the protocol's 1,000,000 logical-file bound. Small/empty files can keep its decompressed byte count well below 8 GiB. Conversely, a source set exactly at the 8 GiB logical-content limit necessarily has a larger tar representation. Charging that framing to the remaining protocol byte budget refuses a semantically within-bound source set. “One long name and one header per file” derives a two-header allowance, not a one-header allowance.

The law currently calls this a set-bound breach that refuses the whole import. It does not identify it as a separate decoder resource limit or an outside-profile package omission. That ambiguity must not be left to the implementer.

**Fix:** Keep the protocol counters exact: regular logical files and their content bytes, accumulated over the set. Define separate bounded counters for inflated stream bytes, physical control/header records, padding/end scanning and any compressed input work. Derive the regular/long-name header allowance from the logical file bound, or publish an independent stricter decoder limit and its precise refusal/omission disposition. Include boundary controls distinguishing content from framing and long-name records from files. This does not require unbounded decoding or general tar support.

`arithmetic_checks.json` contains counter arithmetic only. No large archive was generated or decoded.

## Disposition of the r1 findings and r2 questions

| Item | Decision |
|---|---|
| **C-R1: spec order** | The complete-spec placement at step 11 is repaired. Snapshot/closure/native binding inputs precede construction, and neither parameter contains its parent Plan/spec identity. The new step-14 full admission needs C2-R1. |
| **Selection precheck** | Lawful as a field-only, non-minting check. Item 18 adds the pack's imports capability before it; step 11 retains identical rows. C4-T18 covers refusal agreement, including malformed/oversized/unregistered selections. Authoritative complete-record admission and NE:4278 origin routing must remain distinct. |
| **C-R2: Cargo forms** | GNU magic/version, gzip FNAME, regular files, long-name records and effective-path validation repair the original incompatible format restriction. The inspected published writer supports these forms. No further ordinary emitted member type was identified within the law's logical-path restrictions, but this is not verification of pinned Cargo 1.95.0; R6 and C3-T6a remain implementation obligations. Counter/disposition precision needs C2-R3. |
| **Outside-profile but checksum-matched** | Sound as missing source: omit the entire undecodable package, retain the disclosed reason, and let activated-package DS-6 completeness govern. The raw bytes remain authenticated; an archive-format/header error is not a lock-checksum mismatch. No partial manifest/source tree may be supplied to feature resolution or admission. Inactive omitted packages must not incorrectly make activated completeness incomplete. The adapter's missing-package failure remains NE:1789–1791's incomplete branch. |
| **C-R3: observation** | Resolved. All six members, wrapper-kind equality, canonical hashing/retention and negative controls now match NE:2708 and the workflow schema. |
| **C-R4: schedule** | The principal 29-day A and 28-day B figures are correct under their stated day-zero, K2, O2 and serialized X9-completion conditions. X12d no longer claims unconditional zero delay. See the small branch/counterfactual corrections below. |
| **C4 split** | Sound: C2c is a pure supplied-input library, and C4 orchestrates its runtime minting after C3 inputs exist. C4a may implement non-prepared Plans before C4c; C4c implements the prepared branch before Plan minting rather than augmenting an existing Plan. J2 and G4 wait for the prepared wiring. |
| **C-N1** | B1/B2/C2 capture reuse, changed-entry refusal and leftover-capture refusal are useful and coherent. X2's prior operational-marker capture still needs C2-R2. |
| **C-N2/C-N3** | Absorbed: corpus counts are risk estimates; S-R must specify identity/retention/bounds; L acceptance replaces unchanged draft text; NIJ-1/X-2 and R3 are explicit predecessor gates. |
| **Regressions** | The diff preserves the accepted walk extent, suffix read set, VCS fail-closed meaning, signed closure path, same-core detector, null-self-reference identity join, inert/explicit PO rules, no-execution harness rules, release-pack X12d amendment and L consistency. The new issues concern the expanded capture/admission/profile rules, not reversals of those decisions. |

The checksum-matched omission branch is a lawful conservative source-availability result; the law must reconcile its `undecodable:…` diagnostic with item 13's general `missing:…` wrapper omissions when implementing the canonical wrapper. Both may be disclosed, but one must not replace the required DS-6 package-key missing record.

## Nonblocking observations

- **C2-N1 — Correct secondary schedule details.** The rejected alternative at :880 says C2c waiting for C3b makes C4a start on day 13 and produces 30 days in A but 29 in B. With both variants' C4a starting at 13, both finish the host chain at 30 under correspondingly shifted slack conditions. Also the table carries old F1/G1a day-10 and downstream F2/G3/G4 days. If M3P's full C1/C2 row integration edges are retained, C1b/C1c finish at 8, so F1/G1a finish at 11, G3 at 16 and G4 at 19. Either update those branch days or explicitly narrow their prerequisites to the interfaces they actually need and carry that change in M3P-C. These adjustments fit the existing host-chain slack; the scratch full-row calculation still gives 29/28.

- **C2-N2 — Keep producer compatibility evidence concrete at C3a.** R6 acknowledges the unpinned `latest` source limitation. Make its pinned Cargo/tar source comparison and C3-T6a's retained fixture provenance part of C3a's review evidence, with UTF-8 truncation at the 100-byte header boundary as well as an ASCII long path. H-DEP's pin-time report then establishes actual corpus exposure. This law review establishes neither pinned-producer qualification nor T2 archive coverage.

Published-source checks used [Cargo's package writer](https://docs.rs/cargo/latest/src/cargo/ops/cargo_package/mod.rs.html), [tar's builder](https://docs.rs/tar/latest/src/tar/builder.rs.html) and [GNU header construction/metadata](https://docs.rs/tar/latest/src/tar/header.rs.html), read on 2026-10-04. They corroborate the archive forms; they do not substitute for R6.

`input_checks.json` records supplied pins and supplemental inspected context. `arithmetic_checks.json` records planning assumptions and archive-counter examples. Contract successors still need their own `ACCEPT-DESIGN-UNIT`; X12d and code units need `ACCEPT-UNIT` and `inventoryCandidateAssessment`. This verdict is not acceptance of draft L or of any implementation unit.

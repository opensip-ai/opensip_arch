# CODEX2 Review — CI-3L Source Preflight r2

## Verdict

**PREFLIGHT-CLEAR**

This verdict clears the corrected frozen source for the owning implementation package. It is source preflight only: it does not accept, integrate, or qualify CI-3L, and it does not replace the complete corrected owning lane or its final mutation evidence.

## Closure of the round-1 findings

### CI3L-PRE-R1-RF-1 — Closed

The CI-T28 launch oracle no longer obtains the primitive prices under test from production cost helpers. Its local reference expressions independently construct:

- descent as `{objects: 3, edges: 3, bytes: name + 1 + 4 * size_of::<Level>()}`;
- a status read as `{objects: 0, edges: 1, bytes: max(144, size_of::<Metadata>())}`; and
- a regular no-follow open as `{objects: 0, edges: 2, bytes: max(144, size_of::<Metadata>())}`.

The archived C probe source is independently limited to `sizeof(struct stat)`, its recorded source hash matches the frozen member, and its frozen SDK result is 144 bytes. The reference measures the Rust type sizes directly rather than importing the production price functions. The final owning lane still has to compile and run that probe on its supported host and require equality before treating the prices as evidence; the archived result alone is not ABI qualification.

The remaining production-helper imports in earlier CI-T22 controls are outside the corrected CI-T28 reference enumerator and do not reintroduce the round-1 shared-oracle defect.

### CI3L-PRE-R1-RF-2 — Closed

The independent expected resolver now stops when lookup `S + 1` finds a link, before joining, recording, charging, or allocating another hop. The new cyclic launch control uses a hand-built two-link model on an actually opened and pinned capability and independently requires:

- lookup comparisons `a:2`, `b:1`, `a:2`;
- exactly two one-byte hop temporaries;
- refused-prefix `E = {objects: 2, edges: 6, bytes: 2}`;
- `B = {objects: 2, edges: 10, bytes: 2}`;
- equality between production and independently enumerated `B-hat`; and
- both componentwise inequalities, with zero reads and zero binding observations.

Production `resolve` performs the same stop immediately after the last permitted lookup and before computing `joined_length` or charging the next temporary. The direct cycle control remains as a second check of the `S`-temporary limit.

### CI3L-PRE-R1-RF-3 — Closed

`joined_length_parts` checks the parent, separator, and target additions and returns `TreeReadFailure::Budget(WorkBudgetError::Arithmetic)` on overflow. `resolve` propagates that result with `?`, while `launch_pre_bound` returns `None` when the corresponding bound arithmetic cannot be represented. The new boundary control covers each overflowing addition, both legal maximum-length cases, an ordinary joined length, the exact propagation expression, and the later `Budget(Closed)` latch result. No unreachable oversized manifest execution is claimed.

## Source assessment

The complete seven-path candidate remains coherent with CI-A3 r4 and the accepted CI law and plan:

- the requested-kind check is charged before lookup and refuses an empty kind after exactly one edge;
- lexical resolution uses the retained component-ordered index, performs at most `S + 1` lookups, and allocates at most `S` charged hop strings;
- file and directory members are re-observed through retained, single-component, no-follow handles; files are mode/length/digest checked, and directories are mode/identity checked;
- the launch spelling is charged before allocation, composed once, observed by final-component no-follow `lstat`, and bound to the verified member's kind and `(device, inode)` before becoming the result path;
- every launch failure, including `Budget`, is latched across later launch and transfer calls before charge or observation; a latched budget becomes `Budget(Closed)`;
- the returned `LaunchMember` borrows the capability, and the pinned generation remains owned by that capability; and
- the two new platform observations check support before charge, charge before one native call, retain typed absence/not-directory/I/O outcomes, and add no retry or fallback.

The store-path copy rejects relative or NUL-containing spellings before charge, charges its exact owned record before allocation, and stores the already funded byte buffer as a path. The launch conversion likewise turns the already funded and re-observed buffer into its result path without adding identity, provenance, spawn, factory, or publication authority. Custody checks, the disclosed same-principal binding window, and the accepted CI-2/CI-3 mechanisms remain unchanged.

The operability comparison against product `c436c2cc98837c8771a6e9a9a00cbc3874cc1d29` changes only `mintAudit.rows`: one count-1 `from` call for `installation::store_path` and one count-1 `from` call for `retained_tree::launch_inner`. There are no removed rows. `schemaVersion`, `standing`, ordinary `rows`, termination files, test-support modules, and all other audit content are unchanged, so the upstream D3b-2 rows remain intact.

## Package and evidence review

The frozen subject manifest is 5,784 bytes with SHA-256 `3c76ce4a30aa9db9c58c103e236dd855bb2a08ef07d0cc83f3dffd9a90c19ba9`. All 32 declared members match their byte counts and SHA-256 values, with no undeclared or missing stage member. All nine authority copies match their staged pins and architecture commit `45bb0a72cf9c85458cf982aeb3e3abcb4532782f`. The product lock and all seven parent pins match product commit `c436c2cc98837c8771a6e9a9a00cbc3874cc1d29`; every candidate pin matches its archived product member. The diff covers exactly the seven mapped paths and introduces no path or dependency.

The frozen initial report is tied to the reviewed seven source pins and records 97 lifecycle tests, 15 focused platform controls, and warning-denied all-target Clippy passing. I did not rerun them, as required by the request. These initial checks do not establish unit acceptance. The corrected final owning lane must still perform the ABI check, complete source and structural checks, the full required test/security evidence, and all 24 mutation variants. The superseded round-1 lane is not reusable as final evidence, and its matching 14-failure/7-ignored security baseline and candidate sets are not waived.

## Non-blocking observations

### CI3L-PRE-R2-NBO-1 — Re-establish the native ABI value in the final lane

Compile and run the archived C `sizeof(struct stat)` probe with the final supported-host SDK and require its result to equal the reference constant before accepting the CI-T28 price comparisons. A mismatch requires correcting the reference and rerunning the affected evidence.

### CI3L-PRE-R2-NBO-2 — Final acceptance evidence remains outstanding

Run the complete corrected owning lane and all 24 final mutation variants against these exact source pins. Preserve explicit treatment of the 14-failure/7-ignored security baseline and candidate results; neither the initial checks nor the superseded round-1 lane establishes a passing security baseline or unit acceptance.

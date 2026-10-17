# CI-PLAN-r1 implementation-plan review

Verdict: **REQUIRED-FINDINGS** — two required findings, two non-blocking observations. This reviews a plan and accepts no implementation code.

## Subject and verification

The corrected REQUEST.md pins the observed 380-byte manifest, SHA-256 `bb4d73dc567deb39c038528af95371fe9c5ccb048e01895d23425972e8c3bb52`. The earlier request hash differed; the request was re-read after its correction and the mismatch is resolved. Its sole member matches: PLAN-r1.md, 18,233 bytes, SHA-256 `320feee0f8f4f784021ab88af7895ed1cdb9bf7f7a7dbb9fd7f45305e58cc223`.

Live product `3742822e2823c3a7624aca3fea11220a46cffa16` and architecture `4088af763254018d6a3e70ef7b95c58b17ae8cc9` match the manifest bases. The accepted PROPOSAL.md body, after its acceptance note, is byte-identical to the reviewed r5 law. Read the plan, law/previous-review context, named platform/lifecycle/security APIs, discovery closure, companion source-binding recipe, C1b stale-receipt rules and O1-a package policy.

Only reading, hashing, JSON parsing and Git queries were used. No Cargo, rustc, build, test, lane, shared lane lock, network, private fixture, installation directory, key/private test key, held tree, T2/cache/held-out material, other pane or delegation was accessed. Neither repository was edited. Only the requested two review artifacts were written.

## Required findings

### CIPLAN-R1-RF-1 — Price the selected FileLock wrapper’s full native call sequence

P2; `docs/implementation/m3/component-install/PLAN-r1.md:53`.

LD-CIP-1 selects FileLock::try_acquire for P-6, but that API calls try_acquire_retaining, which performs file.metadata(), fcntl(F_GETFD), and flock(LOCK_NB) in locks.rs before returning a guard. LAW B_open prices the pin’s fopen/status followed by only one P-6 flock edge. The earlier fopen status does not eliminate the helper’s additional metadata read, and the CLOEXEC fcntl is another call. A wrapper charged as the law’s single flock therefore omits the helper’s status cost and one additional native-call edge. This is a mechanism-specific mismatch, not a request for allocator/RSS accounting.

Required change: Select a concrete P-6 implementation whose actual calls and published recipe agree. Either implement the one-attempt native lock/guard in the new module over the already admitted close-on-exec file, or explicitly account for FileLock’s additional status and fcntl checks and reconcile the selected recipe/allowance with LAW. Keep the no-retry, ownership, busy and release semantics. Add an independent call-log control that records every acquisition call and proves its complete cost is funded before execution; do not rely on the caller’s prior kind check to pay for calls repeated inside FileLock.

### CIPLAN-R1-RF-2 — Choose a constructible and correctly scoped standalone barrier receipt

P2; `docs/implementation/m3/component-install/PLAN-r1.md:47`.

The plan implements P-3 solely in component_tree.rs using public filesystem APIs and forbids edits to file_effects.rs to preserve the companion receipt. LAW P-3 returns FileBarrierReceipt, but the existing type in filesystem/file_effects.rs has private file and byte_len fields and exposes only byte_len/is_for readers. There is no public constructor for a successful standalone barrier; the existing producer writes, reads back, compares and barriers the complete borrowed buffer. A sibling top-level module cannot construct that existing receipt. An unrestricted constructor would also let a standalone flush claim the old type’s broader read-back guarantee without its producer. Thus the public-only/outside-bound-sources path is not yet concrete.

Required change: Specify P-3’s return type and trusted producer explicitly. A new opaque receipt in component_tree.rs may witness only the standalone barrier on its exact retained handle, leaving V1’s byte verification with its existing owner and leaving the existing stronger FileBarrierReceipt unchanged; reconcile that choice explicitly with LAW’s P-3 interface. Alternatively name the necessary existing-type producer/API change and re-plan its companion snapshot-source impact before the census freeze. Add controls for exact handle binding and barrier failure, and never expose a caller-asserted receipt constructor or reuse the whole-buffer writer as a substitute.

## Non-blocking observations

### CIPLAN-R1-NBO-1 — Use branch-contiguous post-order rather than a global depth sort

`docs/implementation/m3/component-install/PLAN-r1.md:59`.

LD-CIP-4’s phrase orders the committed rows deepest first should mean a branch-contiguous post-order. A global sort by descending depth can visit leaves in different sibling branches before their directories and then reopen those directories later, exceeding LAW’s once-per-directory step-4 descent count. Building a separate sorted row index would also introduce owned storage beyond the stated borrowed-input strategy.

Suggested change: Specify a manifest-driven depth-first post-order with a retained current-branch stack, each directory entered once and finalized after its descendants. Price any auxiliary ordering storage if one is introduced. Add mixed-depth sibling branches to CI-T22 and assert no re-entry or readdir.

### CIPLAN-R1-NBO-2 — Make the stop rule explicitly cover either receipt’s full bound-input set

`docs/implementation/m3/component-install/PLAN-r1.md:87`.

The plan correctly lists companion snapshotSources beyond discovery CLOSURE and forbids editing them, but the subsequent stop-and-re-plan sentence says closure-file edit. Read narrowly as discovery CLOSURE, that would miss snapshot-only inputs such as file_effects.rs and snapshot_seal.rs. Passing regenerated-output --check and preserving the old receipt file’s bytes alone also does not establish receipt freshness.

Suggested change: Say any change to a bound input of either receipt (including tools, reference-loading sources and snapshotSources/anchors) triggers the receipt-specific re-plan rule. Keep --check results distinct from public binding-freshness evidence, and use a current accepted baseline when freshness is needed. This makes the explicit prohibition and CI-PT-4 consistent.

## Requested dispositions and question rulings

1. **Split, dependency order and file ownership:** CI-1’s pure streaming codec, CI-2’s lifecycle installation row/platform helpers/location, CI-3’s retained capability and CI-4’s J1 command are the right owners. CI-2 correctly waits for C2a-1’s ordinary-reader bridge/candidate; C2a-3 correctly binds CI-3. CI-4 remains dependent on J1 and its termination composition. Lifecycle→security is permitted by the O1-a package-policy row, though not yet present in Cargo.toml.

   **Q1:** share one concrete CI-2/CI-3 package and lane/review, with separate control ownership. CI-2’s successful re-install no-op already needs CI-3’s full reader and its fixtures use the same installed generations. Joint review resolves that coupling without claiming CI-2 standalone completion before the required read controls exist. CI-1 can land first, followed by the joint package after C2a-1, then C2a-3 binding and CI-4/J1. Separate implementation commits are possible, but an early partial commit must not be presented as full CI-2 acceptance.

2. **Prior NBO answers:** LD-CIP-4 now expressly forbids readdir in finalization and uses authenticated committed rows; NBO-1 above makes its once-per-directory post-order precise. LD-CIP-5 restores R’s exact authenticated canonical-length derivation before acquisition and chooses one exactly reserved hand-encoded record buffer, with canonical equality as a test oracle. LD-CIP-6 selects regular-file access mode at build time before the charged open, qualifies it, and prohibits failure-triggered reopen or barrier retry. These answer the three law-review observations.

3. **New platform module and P-7:** a module patterned after custody_entry, using retained public File access and narrowly allowed unsafe native effects, can keep new mechanisms outside the bound source sets. The equal published status-price expression and CI-PT-1 source equality are allowed by LAW. New code is not proven harmless merely by being outside a closure; native behavior, costs and tests still need review. The selected P-6 wrapper and P-3 receipt cannot yet satisfy the claimed implementation/cost boundaries as written (RF-1/RF-2).

4. **Fixture forwarders:** lifecycle’s nondefault crash-matrix/scenario-fixtures forwarders to the existing security features, and the exact joint predicate on fixture-only APIs, are appropriate. The tests must actually enable the dependency feature needed to reach security’s fixture emitter/builders; cfg(test) in lifecycle alone does not make security a test build. Release source pins must preserve the predicate and the existing crash-matrix release rejection. No new root/key or production fixture authority follows.

5. **Single bridge:** LD-CIP-7 correctly reuses C2a-1’s trust-owned authenticated release/body/TreeCommitment view. CI adds no parallel trust admission, signature check or evidence constructor. CI-2 waits if the bridge is not ready.

6. **Receipt impacts:** the new codec/platform/lifecycle/command files and the stated lib.rs/Cargo/location edits are outside the named discovery closure and snapshotSources, so the claimed unchanged impacts are feasible subject to RF-2’s concrete receipt choice. The plan now identifies the companion’s anchored/session sources, including file_effects.rs, not just discovery CLOSURE. Every lane must check the actual changed-file set against both binding closures; regenerate/check output assertions and receipt-byte equality do not independently establish freshness. NBO-2 tightens the already stated prohibition/stop rule. No held-out read or ad hoc refresh is authorized by this implementation plan.

7. **X-CI-1:** LD-CIP-9 gives it the lead owner and an explicit earlier-of gate: before first-party release qualification or production enablement of CI-4. A sourced installation profile remains a separate X-CI-1-a unit, using the selected 2× derivation or explicit law revision. A new WorkLedger constructor changes work_ledger.rs, bound by both receipts; it therefore belongs in a reviewed census interval with fresh baseline, frozen final inputs, pre-run review, authorized blind refresh and post-run review. Reusing the interim profile by call is distinct from editing it and grants no qualification.

8. **Controls/mutations/checks:** all CI-T1 through CI-T26 are assigned, including staged versus published verification, no-op/corruption, pin/transfer/ephemeral cases, fixed archive codec/capacity cases, crash prefixes, actual custody pricing, handle limits and funded publication suffix. CI-PT-1 through CI-PT-4 cover the added plan assertions. The mutations target meaningful failure paths and ownership boundaries. Base/candidate crate suites, serial platform tests, warning-denied all-targets Clippy, rustfmt, environment/operability/source pins, package edges, census checks and verify_design are appropriate future acceptance checks. Add RF-1’s complete native call accounting and RF-2’s constructible exact-handle barrier receipt controls. No such lane was run for this review.

   **Q2:** accept macOS-first implementation/qualification consistent with the existing platform staging. This does not qualify Linux or every S8 row. Unimplemented targets must fail closed through the existing typed unsupported-platform route, with no silent barrier/access-mode fallback; future target enablement needs its own native access-mode/barrier/custody controls. The law’s platform lookup table remains unchanged.

The plan can proceed to acceptance once the two selected mechanism/API mismatches are resolved on pinned bytes. Its production, census and qualification gates remain separate from that acceptance.

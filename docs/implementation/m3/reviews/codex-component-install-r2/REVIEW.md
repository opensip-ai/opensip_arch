# Component release installation and tree custody — CI r2 review

Verdict: **REQUIRED-FINDINGS** — five required findings and one non-blocking observation. This reviews the proposed law only; no code, binding or qualification is accepted.

## Subject and verification

The 770-byte manifest has SHA-256 `42fff5ee7288c0895c239a03f2e67b81954c0569824070e3c6cc5c80c928313e`. All three members match their pinned lengths and hashes. PROPOSAL-r2.md is 37,632 bytes, SHA-256 `e514ee2634b855ba79ab6a677b776bd424aea411116e1aa6fa187b6d4be8e7f8`; r1 and the input memo remain unchanged. Live product HEAD `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture HEAD `a87c1234b26544e65cd2d36b613f218da41b4e86` match the manifest bases.

Read the subject, prior request/verdict, and relevant authority and primitive source. Rehashed the pinned PKG v14 dependency (`8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c`) and confirmed its archiveProfile.byteAlgorithm.goldenAndNegativeCases has 15 members. Verified the snapshot read envelope/buffer recipe, ledger limits/failure latch, selected publication/barrier interfaces, and the existing budget termination/detail registration. No Cargo, rustc, builds, tests, lanes, lane lock, network, private fixture, installation directory, keys, held trees, T2/cache/held-out material, other panes or delegation were used. Neither repository was edited.

## Required findings

### CI-R2-RF-1 — Reconcile the store layout with same-parent publication

P1; `docs/implementation/m3/component-install/PROPOSAL-r2.md:105`.

The selected create_private_directory_stage_accounted / publish_exclusive_accounted primitive retains one parent and renames only between two single-component names in that parent (directory_publication.rs:258-268, 407-428, 468-487). A stage created under <store>/.staging/ therefore publishes as <store>/.staging/<closure2-hex>, not the required top-level <store>/<closure2-hex>. Passing ../<closure2-hex> is rejected. Its publication.parent_directory() also names .staging/, so the selected final barrier would flush the wrong parent for a hypothetical cross-parent move. The proposed transaction cannot implement its published layout using the selected primitive.

Required change: Choose a consistent layout and primitive. For example, stage as a private prefixed sibling directly under the store and have GC census those inert siblings; or explicitly select and review a cross-parent publication extension with both original parent bindings and required durability obligations. Update locations, generation lookup, inert-stage exclusion, GC and CI-T19 together. Do not introduce an unreviewed raw rename outside the selected publication boundary.

### CI-R2-RF-2 — Define staged verification separately from published admission

P2; `docs/implementation/m3/component-install/PROPOSAL-r2.md:109`.

Step 3 invokes item 6 structural/byte verification while files are still 0600 and tree directories 0700. Item 6 requires installed modes 0400/0500 and directories 0500, which are applied only in step 4. Its opening path also requires generation.json association and a pin.lock, neither of which exists until step 4. Thus reuse of the published verifier is underspecified and, read literally, refuses valid staged files before finalization. No explicit final installed-mode/record verification is selected before publication.

Required change: Define an internal stage-verification phase that checks authenticated archive metadata, exact tree structure and bytes against the intentional staging modes without constructing RetainedTree. After creating the association record and pin file and finalizing modes, verify the final publication prerequisites before rename. Keep the production RetainedTree constructor strict. Add a normal nested-file installation control that passes both phases and controls rejecting wrong final modes and association before publication.

### CI-R2-RF-3 — Make final metadata durable after applying it

P1; `docs/implementation/m3/component-install/PROPOSAL-r2.md:110`.

Step 4 barriers each payload and generation.json before changing its mode, and barriers each tree directory before setting it to 0500. A barrier cannot establish durability of a later chmod; flushing the generation directory does not establish durability of arbitrary descendant inode metadata. pin.lock is created without a selected file barrier. A crash after successful publication can therefore leave a generation whose final modes or pin-file state were never covered by the claimed durable sequence. Read verification is a useful fail-closed fallback but does not justify the assertion at line 118 that all contents were made durable before their name could exist.

Required change: Order final file/record mode changes before their final file barriers and final directory mode changes before their final directory barriers, using retained handles and bottom-up ordering. Explicitly cover creation and required state of pin.lock and the tree container. If a new charged streaming-file barrier primitive is needed, name that implementation obligation: FileBarrierReceipt is a receipt, and the existing write_new_regular_accounted writes a complete borrowed buffer at offset zero rather than exposing a standalone streaming flush. Update the cost model and CI-T19 to include crashes after metadata changes and final barriers. Preserve uncertain-publication and refuse-never-repair behavior.

### CI-R2-RF-4 — End the act on a lost exclusive-publication race

P2; `docs/implementation/m3/component-install/PROPOSAL-r2.md:115`.

The proposal runs existing-generation verification after publish returns LostRace. The selected publish_exclusive_accounted explicitly closes the work scope on every publication failure, including LostRace, and states that the loser route ends the act under law 467 item 7 (directory_publication.rs:417-428). Continuing the same operation through item 6 cannot charge on that closed scope. Creating a fresh scope/ledger would bypass the selected failure latch and does not authorize admission of the winner.

Required change: Preserve the full-verification no-op for a generation observed before staging, but make LostRace leave the stage inert and end the current act with the owning existing route. A later explicitly initiated operation may verify the existing generation under fresh ordinary admission. Alternatively propose an explicit law-467 successor; this law cannot silently change the selected primitive failure boundary. Add a control proving no winner verification, ledger reset or implicit retry occurs after LostRace.

### CI-R2-RF-5 — Publish a computable cost bound and protect post-rename work

P2; `docs/implementation/m3/component-install/PROPOSAL-r2.md:90`.

LD-CI-11 lists charged operation categories but does not define the complete cost function promised as an exact pre-acquisition cost. Actual archive read attempts vary within their envelope, stage creation prices eight entropy candidates, verification includes filesystem/ACL work, and cleanup depends on the failure prefix. Several newly selected operations (pin creation/locking, mode changes, link creation, enumeration/transfer and cleanup) have no published numeric cost or named existing cost function here. A conservative deterministic bound can solve this, but actual execution cost is not determined by signed tree bytes alone. Separately, CI-T22 promises that exhaustion at every priced step publishes nothing, yet the parent barrier is charged after rename. A Budget refusal there cannot undo the already visible name. No reservation or other protected funding is selected for that suffix. Before-step-5 outcomes also omit the budget route, although item 8 defines it.

Required change: Define a checked deterministic admission-bound recipe, using explicit existing cost functions and published prices for new operations, bounded attempt counts, representation allocations, final verification and relevant branch/suffix work. Distinguish this bound from actual charged execution and compare it with remaining allowance. Fund/reserve all mandatory publication/post-publication work before rename using the accepted ledger mechanism, so a budget shortfall prevents rename. State the post-rename outcome if a failure still occurs, rather than claiming the generation was never published. Align LD-CI-5, item 8 and CI-T22, and add near-exhaustion controls immediately before rename and at the parent-barrier boundary. Cleanup after a latched failure may simply stop and leave an inert stage; it must not reset the ledger.

## Non-blocking observation

**CI-R2-NBO-1 — Describe where authenticated modes are retained** (`docs/implementation/m3/component-install/PROPOSAL-r2.md:44`). Item 1 says each authenticated mode is retained exactly in the generation record, but item 5 defines generation.json as a closed object with no modes or TreeCommitment. The authenticated manifest evidence already supplies these modes, so duplicating them is unnecessary for the proposed full verification. Say the authenticated modes remain in retained manifest/TreeCommitment evidence and are checked against archive headers; generation.json carries only the listed association fields. If modes are instead added to the record, update its closed schema and association rule explicitly.

## Disposition of round 1 and lead decisions

- **RF-1: addressed in the reader design.** The authenticated selected-platform TreeCommitment supplies authority for the full path/type/link/mode/length/digest check. Extras and missing entries have distinct failures; generation.json is association only. CI-T17 includes the symlinked entrypoint and empty-directory cases. The staged verification phase still needs the RF-2 correction above.
- **RF-2 / LD-CI-10: mode selection accepted.** 0400/0500 files, 0500 tree directories, private 0700 custody containers, 0600 staging files, 0700 staging directories and no symlink chmod resolve the unreadable/untraversable examples. Bottom-up finalization is appropriate. The sequencing and durability defects are separate required changes.
- **RF-3 / LD-CI-5: partially addressed.** Explicit file/directory/parent barriers, uncertain-publication recovery, inert stages, full read verification and no automatic replacement/retry are the right structure. The selected layout, metadata ordering, LostRace continuation and budget suffix are not yet implementable as written (RF-1, RF-3, RF-4, RF-5).
- **RF-4 / LD-CI-9: addressed at law level.** Shared flock pins taken under the fence protect the fence-to-lease handoff, with exclusive non-blocking GC probes and busy meaning retain. ER10a also runs under the read-session fence (J1 item 6); apply the same acquisition requirement there. No pin file may be created by an ephemeral read. A present generation with a missing/invalid pin file must fail rather than recreate it. Pin acquisition/descriptor inheritance must preserve the stated process lifetime, and the bounded call prices belong in RF-5’s model. The transfer streams verified bytes to a noncommitting sink until final success. The owner retains manifest/descriptor from authenticated inputs, and Run releases the origin only after owning every required preimage. Replay remains independent of WS current-trust pivot resolution.
- **RF-5: addressed.** NotInstalled is typed pre-draw data to C2a/C4a/J2. The durable detail requires RTC committed-Run authority; X-8 explicitly gates required-cell composition. No placeholder is minted, cell dropped or ephemeral detail introduced. Missing/corrupt promised-tree causes remain distinct.
- **RF-6 / LD-CI-11: partially addressed.** Finite scope/profile selection, bounded reads, no write retries, separate signed capacities/disk failures and the registered law-468 budget route are appropriate. The full computable pricing/funding obligation is still open (RF-5).
- **NBO-1 / LD-CI-6: addressed for an ordinary preexisting generation.** CI-T1 now names the exact 15 cases and separates codec/metadata capacity from feasible signed installation. Full existing-generation verification is required before the no-op reports installed. This does not authorize continuation after a failed publication attempt (RF-4).

## Question rulings

**Q8.** Accept owner-only installed access for the private per-user M3 store. Files may receive owner execute exactly when the authenticated mode has any execute bit; directories receive owner traversal as the explicit usable-mode policy. No group/other rights or symlink mode operation is needed. Preserve authenticated archive modes separately. RF-2/RF-3 concern phase and durability, not this mode selection.

**Q9.** Accept snapshot_profile() as an explicit interim finite installation policy under X-CI-1; it is not evidence of installation census coverage or release qualification. A new release census is not inherently required before CI-2 solely to select this existing cap. CI-2 still requires the complete admission-bound/pricing and publication-funding controls in RF-5, with X-CI-1 given a named owner and disposition; do not infer R10a’s separate profile from this selection.

**Q10.** Name inert-stage census/removal as an explicit obligation of the existing GC owner, under the fence and bounded GC work. Bind its location to the RF-1 layout correction. GC never resumes/adopts a stage or admits it as a generation; no automatic repair/retry is authorized. Detailed removal implementation stays with GC, while CI supplies the recognition/exclusion and custody prerequisites.

## Other accepted scope preserved

No additional regression identified in LD-CI-1 through LD-CI-4, LD-CI-7 and LD-CI-8 or the prior Q1–Q7 rulings: one host-platform release, authenticated ordinary-reader evidence, identical raw artifact/archive digests for uncompressed profile 1, the closed platform-token lookup used only for artifact selection, offline no-follow regular-file acquisition, signed archive/capacity checks, private store custody and refuse-never-repair remain selected. The pinned archiveProfile adoption remains an explicit narrow new selection; PKG’s other members and DR-120 standing do not change. The lifecycle–security edge is explicitly owed rather than asserted to exist. No additional total-byte constant, public code, key/root, network transport, update/migration policy or qualification is supplied by this law.

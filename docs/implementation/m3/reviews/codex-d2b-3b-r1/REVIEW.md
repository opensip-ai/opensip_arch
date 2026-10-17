# D2B-3b-r1 review

**Verdict: REQUIRED-FINDINGS.** One required finding; no non-blocking observations. Product qualification: false.

Subject manifest: `c7aed6170f989af695acded21dccecece268651ca340da0065422758b4a031e7` (13,589 bytes, 56 members).

## D2B3B-R1-RF-1 — Latch snapshot read failures before returning them (P2)

At `crates/components/src/provider_protocol/ts2/send.rs:1122-1124`, `source.read` errors are converted to `SendRefusal::Source` and propagated with `?`, without calling `self.refuse`. `send_next` also propagates the `realize_next` error directly. Consequently, the transcript is still open after this failure.

A concrete public-API sequence is: accept Hello, OpenUniverse and SnapshotManifest; fail the first chunk's snapshot read once; restore the source; call `send_next` again. The failed read has advanced neither cursor nor slot, and has not set `refused`, so the chunk can now be accepted. Alternatively, `cancel()` can still produce an accepted Cancel after the Source refusal. The same omission occurs on a later chunk. This contradicts SCOPE's explicit snapshot-read-failure termination rule and the send module's public Source/refusal contract. The participant's separate `host_fault` latch protects that wrapper, but does not repair the exported sender.

The last case in `every_divergence_refuses_before_writing` checks only that the first call returns Source. It omits the `ended` assertion used for the preceding refusals, so the passing control does not establish its claimed termination behavior.

Latch the refusal before returning a source I/O error, including direct use of `realize_next`, and audit equivalent public failure exits. In particular, `cancel()` also returns its pre-Hello divergence through `?` without the latch used by `admit_cancel`. Preserve the already accepted prefix and make every later sender operation refuse rather than resume or read the source again.

Add controls for a one-shot source error at the first and a later chunk, restore the source, and assert `next_slot` and `cancel_payload` are absent and `realize_next`, `send_next`, `admit`, `cancel` and `admit_cancel` return `AfterRefusal`. A counting source should establish that the later calls perform no additional read. This finding follows directly from the code; no Rust build or test was run during this review.

## Subject and authority checks

Independently rehashed every manifest member, all twelve source authority pins, the recorded product lock, all six archived/worktree candidate files and the three existing parent files. The worktree is detached at product `5de9fd4740ea17018d0bd3fbff9496c94ddacda9`, and its modified/untracked paths match the map. The product lock remains inventory v226/contracts 176. No dependency changes are present.

Read the accepted plan's builder/sender allocation and amendments, carrier parameters, reference planner/sender, implementation and controls. The schedule follows the reference's slot order and greedy chunk sizes, excludes the 40-byte prefix from envelope-payload accounting, binds chunk payloads without `bytes`, places the content digest on each last chunk, and reserves the maximal Cancel at the final possible sequence. The sender independently walks file entries and counts realized chunks; its admission compares frame order, sequence, chunk coordinates, seal count, closed schema, exact size and payload digest before updating accepted sent state. It hashes the actual accepted chunk bytes and checks the last-chunk entry digest. RF-1 concerns an error exit before those admission checks.

The builders carry the selection's capability array without repair; read the Hello's limits and identity versions from schema constants; recompute the TypeScript universe identity; build the manifest digest and checked seal aggregates; project selected stages, Analyze-relative ordinals, dependencies and the two budget forms; and reconstruct subject-scope and requested-domain commitments. Per-key scope2 values remain C4's admitted input. The declared early entry-bound refusal and UTF-8/path/schema checks are consistent with this unit's allocation. The census-bearing capability is explicitly refused pending D2b-3c.

The normal Cancel admission uses deterministic-CBOR byte equality, exact sent-state nullability, next sequence, one-use state and the reserve, and closes the transcript after acceptance. T2O's broader ability to accept a START Cancel is not used by the sender. The participant queues one frame, checks host transitions through a copy of the actual table run, and performs at most one fd0 write or bounded fd1 read per call. Context/request joins cover the receiver's correlation values, manifest files/totals, stages, budgets and keys. Admitted transitions alone produce progress. Verified terminals mint the existing terminal-output token once. Sender/source/host-pipe failures map to HostFault, while worker admission/framing failures map to Fault; the sole supervisor arm triggers the corresponding host cause.

D2b-3a's NBO-1 is accurately carried as a historical overview correction without rewriting its reviewed package. NBO-2 is resolved by a lawful Coverage envelope whose depth is exactly seven and which the receiver admits at T2-13; the eight-container counterpart is refused by the reader with Depth.

## Validation evidence and boundaries

Independently ran only the two permitted commands. Operability source checking passes with 114 rows and no findings. The duty-table checker passes: 30 rows cover all 55 carrier admission IDs exactly once, and all 19 TS2 builder/sender IDs are named in the implementation. Its name-presence check supplements the semantic review; it is not by itself proof that the duties are implemented correctly.

Inspected the pinned lane and runner without rerunning builds, generators or tests. Components has 101 base passes with nine existing handshake failures versus 125 candidate passes and no failures. All nine differing tests pass the six recorded isolated runs (three per side), supporting the comparison's 15 new passing tests; this does not establish a passing parallel base suite. Identity remains 72/72 and contracts 0/0. The fixture record is present for both sides. Focused TS2 tests pass 31/31, comprising the existing sixteen and new fifteen.

All eleven mutations have actual focused-test failures and are caught. Recorded rustfmt, warning-denied all-targets Clippy, environment exceptions, operability, unchanged 19-file census closure and verify_design pass. The new production implementation adds no mint authority, environment read, dependency or `let _ =`. The receiver's existing admission behavior is preserved by the small host-event extraction.

The three new paths still need a separately reviewed inventory successor. D2b-3c retains FA-2, replay and final TS2 controls; Rust3 retains its own codec units. D3b owns the cancellation trigger/hook, D4 the context/source/session factory, C4 the Plan inputs and pre-spawn call/refusal routing, and C1 the sealed snapshot custody. There is no production caller, provider supervision or fact admission in this unit, and no product-qualification claim.

Only the two requested review files were written. Neither repository nor worktree/control file was edited. No network, prohibited private material, T2 store/cache, pane or delegated agent was used.

# C1C-0-r2 review

**Verdict: ACCEPT-UNIT**

Subject manifest: `docs/implementation/m3/snapshot-plan-c/c1c-0-r2-subject.json`, 15,582 bytes, SHA-256 `3c9447301b151ed4d18faa7bf34f522ebefd297bfdd756f1c84e54880d5db43a`.

No required findings or non-blocking observations.

## Subject and scope

Rehashed all 67 manifest members successfully. Independently checked all 17 product-map rows against the candidate and archived bytes, the 16 existing-file parents against product commit `caa71e2fd481977d066d67465add64f4393334f9`, and every source.json authority and product-lock pin. The detached candidate HEAD matches that base, and its changed/untracked paths exactly match the map. There is one new path: `crates/security/src/snapshot_read_set.rs`. The nine archived Rust files and the discovery census tool match round 1 byte for byte; this is the first submitted review of the unit.

Acceptance covers the preparatory library unit under C1c plan r4 and M3-C r8 items 1 and 3. It does not complete C1c, supply the layout/read set, integrate the candidate, refresh the receipts, or qualify the product.

## Implementation assessment

- **Pruned-tree capture:** the validated path and rule temporaries are charged before use; outside-dependency paths, VCS segments and exact custody anchors refuse before filesystem opens. The retained root and directories above the outermost dependency anchor receive S3 custody judgment. At and below that anchor, the opener uses the existing charged no-follow observation/open/identity-comparison helpers. The final regular file receives no configuration-marker custody or marker-size ceiling. Symlinked components refuse, and the replacement control exercises the shared file identity check. `capture_pruned` uses the session's existing one-read implementation and returns a kept capture without rereading it; an unreached capture remains a leftover.
- **Authorization rule:** `classify_path` is unchanged. The new crate-private, pure rule checks the full authorized path plus descendant, reusing the existing dependency, VCS, Cargo-output and custody-anchor definitions. It accounts for both first-party and dependency-tree Cargo roots, distinguishes nested packages from separately authorized paths, and preserves the specified lookalikes. The public `ReadAuthorization` wrapper maps the private verdicts correctly. Its temporary-allocation charge covers the segment vector, Cargo prefixes and possible custody anchor before invoking the rule.
- **Walk evidence:** Cargo keys already charged at insertion remain in `known` and move into opaque `WalkEvidence`; there is no new key copy. Retaining sibling roots cannot change classification because Cargo lookups compare only path ancestor prefixes. Member roots are copied only after an `owned(member.len())` charge. The host retains the resulting evidence, and `walk_snapshot` keeps its previous signature through the shared implementation. The model pins the move/copy sites and refuses `known.remove`.
- **Marker observation:** dependency Cargo-root detection uses charged, descriptor-relative no-follow metadata observation. Only a regular `Cargo.toml` counts; no content is read.
- **Rules and inventory:** no added production environment read, mint-census call or `let _ =` was found. Security `lib.rs` is appended only. The one new source path needs the separately planned additive inventory successor.

## Accounting and receipt interval

The discovery tool changes only its whole-file `discovery_rule.rs` CLOSURE pin. Independent JSON comparisons show only the declared closure changes in the discovery records, closure/tool changes in the workspace ledger, and pins plus the five `allMountsAsMembers` rows in the snapshot census. Those five rows add respectively 2/8/2/2/2 objects and 291/1165/310/310/289 bytes, with no edge increase; all still pass 2x. Walk predictions change only for the member case (+1 object, +129 bytes); session predictions and existing opener cases remain unchanged, with three exact pruned-opener cases added.

The permitted retention helper independently reproduced the archived result: the worst-case member copies add 64 objects and 1,056,768 bytes, giving r9 totals of 776,740 objects, 6,218,464 edges and 2,539,929,154 bytes. Every coordinate satisfies the fixed caps' 2x rule.

The permitted receipt helper independently reproduced the archived cumulative record. For each receipt, main's bytes equal both the accepted `0772eb7` refresh and C1b-0's recorded baseline. The batch-so-far delta is exactly C1b-0's generator-closure binding change; C1c-0's own delta names exactly its affected inputs; the cumulative delta is their union. Both receipts remain byte-identical, and all ten held-out rows per receipt render stale with outstanding held-out margin.

Read-only inspection confirms the C1b batch is open and has no recorded freeze/pre-run/refresh key. The integration script requires that state, refuses overlapping main changes since the lane base, and records the before-freeze join in its assent and publication record. The script was not run. A future freeze or overlapping change remains subject to those integration preconditions.

## Validation and boundaries

Independently ran only the four expressly permitted checks: snapshot model `--check`, operability source census (114 rows, no findings), retention evidence and receipt-specific evidence. All passed; both helper outputs exactly match the archived JSON. Helper output temporarily used the two authorized review filenames, now replaced by the final review artifacts.

Inspected the archived lane rather than rerunning it. Raw test logs agree with the comparison record: host 411 to 412 passes with the same 8 failures; security 1,187 to 1,198 passes with the same 14 failures. Focused suites pass: walk 25, rule 12, census 7, session 30 with 1 ignored. Warning-denied all-targets Clippy passes; new/base-clean Rust files are formatted, while the append-only lib.rs retains its existing formatting debt. Archived model/census checks, FW-01, environment checks, operability, closure classification and verify_design pass. All 14 mutation logs show the expected test/model rejection, without a compilation failure substituting for detection.

No repository, worktree or control file was edited. No Cargo, rustc, build, lane, integration script, network request, private fixture, installation, held tree, T2 store/entry/overlay or cache access was performed. Only REVIEW.md and review.json were written in the requested directory.

# C1B-1-r2 review

**Verdict: ACCEPT-UNIT.** C1B1-R1-RF-1 is resolved. No required findings or non-blocking observations. Acceptance covers the submitted Git-read unit; sealing, production composition, inventory integration and the batch's blind refresh remain owed.

## Subject and exact bytes

Independently verified the 26,380-byte manifest, SHA-256 `cf7b38a4e378e1920c61be713df4f789b2f4b1a155ca25060db09ed023011b8e`, and all 111 member lengths/hashes. All match.

The candidate worktree is detached at the exact lane/product base `274dccc5eced53828f444fa44e62cdeffabc2d0c`. Verified all 13 candidate and archived product-map entries and every existing-file parent pin against that commit. The changed/new path set is exactly the mapped set, including three new snapshot_vcs paths. Verified the source record's product lock, 14 authority pins and prior subject/review pins. Rehashed all 67 members of the historical r1 package: unchanged.

Compared r2's product bytes with r1's. snapshot_vcs.rs, snapshot_source.rs and snapshot_ledger_model.py are unchanged. The operative revision removes proof-construction allocations and adds its controls/harness coverage, with dependent source pins regenerated. Thus the earlier reviewed closed parser, member walk, read pricing and record encoding remain the same implementation, not newly substituted logic. Independently checked that base-dirty git_tracking.rs and lib.rs retain their full base byte prefixes and only append.

## C1B1-R1-RF-1 disposition

**Resolved.** RepositoryProof::retained no longer collects a component vector or calls the allocating label helper. components_prefix borrows the first requested number of path components directly from the retained chain spelling. is_dot_git_label checks the candidate label's exact length, prefix and /.git suffix in place. These reproduce X2's existing label construction without allocating an ancestor spelling or concatenated label.

The zero-component case matches X2's empty prefix plus /.git; the full component count uses the whole borrowed spelling. Intermediate counts stop at the corresponding slash. Chain identity and the Untracked-with-positive-repository-count precondition are retained. Indices are still scanned from the selected root upward, so the first matching repository is the innermost. The proof now borrows the metadata sample from the same TrackingObservation for the proof lifetime; no copied label or metadata ownership is introduced.

SnapshotRoot::from_operation still obtains the proof from the operation's own namespace subject, chain and tracking observation. It accepts no caller-selected repository path or substitute sample. NoRepository still lends its own chain for W. The revised proof path and its helpers contain no allocation or native operation requiring a new model charge. The model and its derivation therefore need no additional proof-allocation term.

Observed::vcs now constructs the subject and lent root inside the charged test scope. Moving that work into the scope would not by itself detect an uncharged allocation; the new source control and direct inspection supply the allocation check. The control covers RepositoryProof's implementation and both helpers, repository_proof and from_operation, and checks the borrowed sample field. The new nested-repository test verifies the actual retained index and commit across three nested repositories, at repository roots, between them and forty levels below the innermost.

The proof-allocation mutation fails the new source control; the shortened-prefix mutation fails repository-selection controls. The archived void attempt's uncaught label-prefix/length mutant is disclosed and excluded from the final 13-mutation claim. Its removal is consistent with the evidence model: the observation has no longer repository-label candidate under a chain prefix that would distinguish that proposed weakening. It does not hide a failing final control.

## Retained behavior and earlier rulings

No regression was found in the unchanged VCS reader. HEAD remains restricted to the detached lowercase-hex form or one refs/ symbolic target. A second symbolic level refuses. Loose refs take precedence over packed refs; ref directories are opened segment by segment with no-follow handling and only the current directory retained. packed-refs uses the closed header/peel grammar and strictly ascending names, which rejects duplicates without per-line allocation. UTF-8 and long-component refusals retain the declared restricted subset; unborn is a refusal, never a null commit.

Custody precedes each read, volume checks remain tied to the admitted home/root evidence, and the enclosing .git metadata is compared with X2's sample. Member reach uses borrowed segments from the NoRepository proof's W, checks markers on the required path and verifies the member .git device. Member failures preserve their indexed member projection; cross-root, unobserved/member and placement preconditions remain Internal. Budget remains typed WorkFailure::Budget rather than a VCS observation or an unborn result.

**R1 Q1 remains applied.** LD-C1B1-5 explicitly records the accepted adjustment: stable files over 4 MiB fail S3 custody before reading; exactly 4 MiB is read subject to the shared budget and parsed; oversized remains available for growth after judgment. No cap increase or custody bypass is introduced.

**R1 Q2 remains applied.** LD-C1B1-8 keeps the complete VCS derivation separate from per-entry census pricing under r9's conditional-margin regime. All non-row work shares the same remaining margin. Passing output checks and unchanged receipt bytes still do not establish fresh blind margin.

## Model, derivation and receipt evidence

Executed only the four expressly permitted checks. The model --check verifies the snapshot, session and VCS vector outputs. The live operability source check reports passed, 114 rows and no findings, including the unchanged mint audit. The live VCS derivation matches the archived JSON exactly:

- D* = 226 is reproduced; the next directory exceeds the edge margin.
- The model's H* = 1,363,957 differs openly from the plan's 1,048,575. The omitted owned HEAD-target copy and post-judgment status read explain the reduction; both are absent from the unchanged reader.
- At the plan coordinates, the model term is 173,706 objects, 2,164,854 edges and 1,577,723,559 bytes, no larger than the plan term in any coordinate.
- The record maximum remains 1,573,798 bytes. The model's next HEAD byte exceeds the byte margin.

The nine native exact-charge cases, borrowed-segment reach prices and canonical-record controls are present; the lane reports them passing. The read/model sources are unchanged from the reviewed r1 implementation. The vector-moves record confirms unchanged walk/openers/session predictions and nine VCS cases.

The permitted receipt-specific checker also matches its archive and reports allPassed. Its output was temporarily directed to the permitted REVIEW.md path, then replaced with this review; no third review output was created. It confirms each receipt independently: bytes equal the 0772eb7 refresh baseline and recorded baseline pins; batch-so-far equals C1b-0 plus C1c-0; the unit's own delta is the expected git_tracking/tool/source delta; cumulative changes equal the union; and both receipts' bytes remain unchanged. Each regenerated record renders ten public held-out-status rows stale, with heldOutMargin outstanding. No held-out corpus, store, overlay or cache was read.

Independently compared the five regenerated product JSON outputs against the base: differences are source/tool pin leaves only. This establishes accurate stale rendering and binding accounting, not renewed receipt freshness. The unit still belongs to the open, unfrozen C1b batch, with its reviewed pre-run freeze and single refresh after C1b-2 still owed.

## Recorded lane and scope limits

Inspected the final checks, underlying mutation logs and focused results. All final check rows pass. Security increases from 1,257 to 1,281 passing tests with the same 14 pre-existing failures; host remains 412 passing with the same eight pre-existing failures. No isolated flaky adjustment was needed. These are equal-failure-set comparisons, not all-green full suites.

The focused VCS run has 24 passes; tracking/snapshot-source has 41. Recorded warning-denied all-targets Clippy on host/security, permitted-file rustfmt, append-only checks, derivation, model/vector checks, census checks, FW-01, environment exceptions, operability and verify_design pass. verify_design reports productQualification false. All 13 final mutations reach test failures; none is counted from a compile failure.

The candidate introduces no environment read, let-underscore discard or new mint-census call. The existing native/read helpers are exposed by append without altering their base implementation. The three new paths need the separately reviewed additive inventory successor before integration. No production caller is added. C1b-2 still owes sealing/schema records, J2 owns route composition, and the batch refresh remains outstanding.

Only REVIEW.md and review.json were written in the requested review directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build or lane was run. No network, prohibited private fixture/key/installation material, held trees, T2 material, other pane or delegation was used. Only the four explicitly permitted project checks were executed.

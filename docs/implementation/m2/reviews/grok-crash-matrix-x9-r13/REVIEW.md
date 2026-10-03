# X9 r13 — ACCEPT

r13 records what X9-5's development runs produced, and it raises the timing guard to the limit X9-3 measured. The diff against accepted r12 is those decisions. Each one follows the owning law and the product at `b999ae34ed567a010bd789488512884fa38df05b`. No other row, point placement, runner, host order, required-runs file, or census changes.

Subject `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md` is 134335 bytes, sha256 `f373415ea1a7bb812b12d70e345a35562e54e4ee547034e1ecfab6a4b87d23cc`. The preserved snapshot is the accepted r12: `PROPOSAL-r12.md`, 123524 bytes, sha256 `341075762e8cf515267e24c8a38ea4e2ba58368487893e83a7c1f9c0917b3337`. The diff is 179 lines in nine hunks: the title, the r12 acceptance stamp, the r12 timing-guard sentence, the r13 header, the F01, F32 and F40 cells, the item 11 timing sentence, and the item 12 X9-5 line. Product main is clean. No product cargo. The real home was absent. The development runs and the two timings are the lead's report; this review judges the decisions against the law and that commit.

Pins matched `hashes.txt`: `recovery_capture.rs` 36509 bytes, `9d670909…`; `carrier_operation.rs` 11315 bytes, `6cea2e97…`; `commit_session.rs` 61705 bytes, `94a6969f…`. `journalContiguity` is an existing operational reason. It is absent from `public-detail-registry.json` and `diagnostic-routes.json`, and `recovery_location.rs` carries it in the operational record.

## The candidate child's one REV

The candidate child opens a `CommitSession`, writes the candidate, then ends before `prepare_commit`. The X9-5 child takes the end-path settlement reserve and then calls `refused().finish()`. That is X3d item 3 step 0, the same funding `prepare_commit` uses, stopped before step 1.

`refused` latches the gate and keeps a reserve that was taken (`commit_session.rs`). `finish` owes a REV when the gate is latched, and a CLN only when the seal is `WithoutEvidence`. This end is `Seal::Absent`, so the owed list is the one REV. `open` has drawn the ExecutionId, so the settle arm runs and appends that REV at seq 1. The floor is still INIT at lastSeq 0. There is no ledger, no attempt row, no SEAL and no object. r10's stop rule looks for a ledger or an attempt row, so the REV does not trip it.

A refusal that never took the reserve appends nothing. That is `open`'s own refusal, and a reserve that itself fails. The host rows' starting state is the funded end, which succeeds. Every host row runs this child first, including F01 and F53, and the census runs do the same. X8 r5's B1, B2 and B4 are the same funded path: one REV and no CLN after a latched refusal that had already reserved.

## F01's two variants

A replay refusal returns inside `finalize` before `admit` (X5 r3 item 3). That invocation adds no journal record. `normalizedSha256` before and after the finalize child is the same. The carrier already holds the candidate child's REV; "unchanged" is measured across the finalize child.

A substituted target or a substituted inventory replays, is admitted, opens, and is refused at X3d item 3 step 1 on the invariant row. `prepare_commit` has already taken the reserve, so `finish` appends one REV. The ledger stays absent. There is no attempt row and no SEAL. The carrier gains exactly that record, which is why the development post-state was `[REV, REV]`: the candidate's REV, then the finalize child's. These are X8c's B1 and B2. Once that session is inside `prepare_commit`, step 1 cannot return without the funded REV.

## F40's latch variant, landed only

r12 holds F39 at `x3c.evidence.commit.before#1`, the first point after admission where the shared monitor is released and the gate is already state 1. A point takes one action. The latch script cannot hold there and also inject `fail-before` there. The landed injection is `fail-after` at `x3c.evidence.commit.after#1`. The variant therefore runs F12's landed ladder with the latch observed, and the timing guard applies because the script arms the tick.

The latch combined with a not-landed injection is covered by F40 without the latch, which still runs both landed and not landed, and by X4's in-process gate-trace test, which runs every interleaving of latch and admission. Holding at `.after` cannot pair with the not-landed injection, which is `fail-before` at `.before`. Moving `x4.gate.admit.after` stays rejected, as r12 rejected it for this script.

## Distinct R2 after a committed Run

A host row whose scripted phase leaves a committed Run sends R2 the distinct variant r12 defined, built by the candidate child from the same session and written beside the candidate. It stays inputs only. `replay_run` stays the only `ReplayedRun` constructor.

Where no revocation stands, R2 is Committed: F12's landed variant, F16, F17, and F40 without the latch. Where the latch stands, R2 is refused at admission under C5, and the exact row stays unscored: F39 and F40's latch variant. Scoring R2 as the same Run would repeat r12's F13 finding, `Refused(Invariant)` at staging, and would leave "the next writer proceeds" untested on a row whose attempt committed.

F32's `…987` variant is in the same set because that attempt commits. R2 then meets `CarrierCapacityExhausted` at `capacity`, which is `prepare_commit` step 3, before staging. `seal_fits` is `tail <= SEAL_CEILING`, and `SEAL_CEILING` is `9007199254740987`. After the SEAL takes `…988`, the next prepare sees a tail above that ceiling. The RunId is never staged, so the distinct variant leaves the row's existing exhaustion outcome as it stands.

## The revoked subject

`CommitSession::core_closure` is the receipt's selected core, `operation.selected_core().0`, taken from the installation's authenticated inventory. The candidate child and the later finalize child admit the same installation, so the string is the same one the finalize observer compares. The candidate child writes it under the run's scratch root, and the publisher child reads it. That is r12's subject, on the host order, where the session that holds it is the candidate child's. The accepted-store constant remains the wrong subject.

## F32 `…987`

The planted tail is `(1, 9007199254740987)`. `plant_committed_tail_for_tests` lifts `gj3_append_laws`, inserts one RA at that seq, and reinstalls the trigger. Below it the generation holds the candidate child's REV at seq 1. Owner §2 requires sequence contiguity `1..t` before any confirmation. Capture enforces it as `COUNT(*) != tail` (`recovery_capture.rs`), and that verdict is `JournalContiguity`, rendered as `unknown-quarantine-condition:journalContiguity`. The count is a handful of rows. The tail is `9007199254740987`.

`committed_tail` checks a missing TERMINAL only when the newest generation is above the first. Generation 1 with a gap is a lawful tail for the writer. The start reads that tail, the witness and the floor (X3b item 9) and does not walk `1..t`. `seal_fits(…987)` is true, so the attempt commits and its SEAL takes `…988`. Recovery of that ExecutionId is the quarantine. It is a fixture property. A lawful generation is contiguous, and the standing is a quarantine condition.

R3 stays unscored. The sweep reads the ledger. The `…988` variant still writes no ledger: `seal_fits` fails before `store_root`, so recovery stops at `unknown-custody` `ledger-missing` and then `unknown-attempt-unobserved`, and never captures the carrier.

The rejected fill is a contiguous journal through `9007199254740986`, about 9×10¹⁵ rows, which item 6 does not plant. The sentence writes that predecessor as "986" without the ellipsis the same decision uses for `…987`. Restoring the ellipsis changes no row. A journal of 986 rows would leave this tail gapped, and it is not the technique.

F43 is unchanged. Its mutation deletes `seq >= journalSeq` and leaves a contiguous prefix, so capture's count matches the new tail and the existing hazard rule applies: unavailable-busy, or the F22 condition, and never uncommitted. The sentence records that a planted tail is a fixture and that a lawful generation is contiguous. The F43 cell is untouched, with the rest of X9-3.

## The timing guard at 5,000 ms

X4 charges 10 s from the earliest instant of the previous successful read to the admission-boundary sample. The guard measures the parent's monotonic clock from the writer's first `x4.observer.tick` hold to the hold at the admission point. That window is the writer's own work: the attempt row, about 40 objects each barriered by `F_FULLFSYNC`, the SEAL and its witness, and the checkpoints. The parent and the publisher stay outside it.

X9-3 measured 2,845 ms on F44 and 2,893 ms on F45. Both sit above 2,000 ms, so the r12 limit makes those lawful runs a `HARNESS-ERROR`. 5,000 ms is half of X4's bound and about 1.7× the measurements (2,845×1.7 is 4,836; 2,893×1.7 is 4,918). A run that passes is at most 5 s, so the 10 s stall stays at least 5 s away, and an `OBSERVER.FAIL_STOP` still never passes as a run. A limit near 10 s would accept a run whose awake time approaches that stall. Narrowing the window to the main thread's held time would stop measuring the awake time the freshness bound charges.

The measurement, the window, the record member, and its exclusion from the repetition comparison stay as r12 set them. The r12 sentences keep "2000" and "2 s", each with the r13 note, which is the established note pattern. The checker's limit, its test, and the run record's constant belong to X9-3.

## What this review leaves to X9-5

These calls are the unit's, and r13 does not make them law: the F32 transcription read X3b item 4a case 2 as OPEN; the substituted-target candidate retains the closure's blobs; F01 and F53 run no ladder; the publication is a publisher child under the scripted clock; R1 for F16, F17 and F39 is `committed-historically:*`. The current publisher still receives the fixture child's closure string. r13 requires the candidate session's `core_closure`. That is the unit's change to make.

## Nothing else

The r12 acceptance stamp is the record of that acceptance. Runners, host order, the required-runs file, and the census stay as r11 and r12 left them. X9-2's rows and X9-3's rows are untouched. No accepted outcome of any other law changes, and there is no new public code, row, or detail.

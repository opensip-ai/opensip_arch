# X9 r4 and X6 r4

Claude Opus 5.5 leads. Grok is the single reviewer. Law review only. No product cargo. Git was read-only, against `/Users/sb/code/opensip-ai/opensip` at `a36da7c`. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Two verdicts. X9 r4 amends two decisions. X6 r4 records them and the G1 line X9 r3 left for X6's next revision. Every accepted sentence of each predecessor survives. The lines that differ from the snapshot are the title, the `r3 ACCEPTED` stamp already carried on the working law, and r4 text marked `r4`, `(r4)` or `**r4 (record):**`.

| Law | Verdict | `noAcceptedOutcomeChanged` | Subject | Preserved snapshot |
|---|---|---|---|---|
| X9 r4 | ACCEPT | true | `crash-matrix-x9/PROPOSAL.md`, 74438 bytes, `4b387bbd7a08d901007ec50b811474b1f776f02b92f58c77812dc46e4091cd80` | `PROPOSAL-r3.md`, 62835 bytes, `1f270548777b3234f0188ecb3496cedcef718a30bcb46d0b07832a4be6a0b04a` |
| X6 r4 | ACCEPT | true | `carrier-recovery-x6/PROPOSAL.md`, 25257 bytes, `20df341c567b1120192ef767f2b6036d5355701dd4cc0bf0d7f330394d638d09` | `PROPOSAL-r3.md`, 23197 bytes, `e57aef34213341ec97ef5ca9e7515bccf0469c6b1e3416d9b0c6883c9054f700` |

Both snapshots match the `subjectSha256` of the reviews that accepted them (`grok-record-x3d-r7-x7-r6-x9-r3` for X9 r3, `grok-recovery-x6-r3-x7-r4-x9-r2` for X6 r3). All fifteen `hashes.txt` rows match, including X8 r3's `PROPOSAL.md` at 44323 bytes, `78db818650b37004fab991a7f308d046da06005e0f30fea257258d3993565128`, which this revision does not edit. Product `a36da7ce495b49c2d82ad31a9ecef707e6de9909` is the crash-matrix support commit.

`noAcceptedOutcomeChanged` is true for X9 because the only outcome changes are the two lead decisions: the three driver entries, and `check-unit`. The X8 cross-reference and the G1 sentence are consequences of the first decision. X8's bytes stay. X6 records those decisions and changes no X6 outcome.

## X9 r4 — ACCEPT

The header states an amendment under the owner's standing direction of 2026-09-30, found while starting X9-2, changing two things. The r3 status paragraphs, including "G1 is open", stay where r3 put them.

### The three driver entries

Item 6 adds exactly three functions on security's `crash_matrix_support`, forwarded unchanged by storage and host:

- `operation(at, root) -> Result<ProjectOperation, InstallationTermination>` runs the census composition: `ordinary_writer::admit_with` over a signed test tree and `HomeSource::Fixture`, root admission and first registration when the root is unregistered, then `begin_operation` with APPEND-WRITE. It returns that `ProjectOperation`.
- `recovery_admission(at, request) -> Result<RecoveryAdmission, RecoveryRefusal>` produces the read receipt, allocates recovery's ledger as `admit` does, and returns `recovery_admission::admit_on` over `HomeSource::Fixture`.
- `settlement_sweep(at) -> Result<SettlementSweep, InstallationTermination>` runs the same fixture writer admission, then returns `settlement_sweep::admit_on`.

At `a36da7c` the privacy facts hold. `OrdinaryWriteAdmission::begin_operation` is `pub(crate)` at `ordinary_writer.rs:220`. `admit_ordinary_writer` is `pub(crate)` at line 493 and calls `admit_with`. `admit_with` is `pub(super)` at line 506. `RecoveryAdmission::admit` is the public constructor and passes `HomeSource::Native`. `admit_on` is `pub(super)`. `SettlementSweep::admit` is `admit_on(admit_ordinary_writer()?)`, and that `admit_on` is `pub(super)`. Storage's matrix target cannot call any of these. The census function `operation` in `crash_matrix_census.rs` reaches the writer and `begin_operation` because it is inside security. X8 r3's `scenario::operation` is the other accepted route, and it is X8b's.

The constraints keep the entries test-only, non-minting, and on the one site list. They sit in the pinned support module, so they add no cfg site. They call existing items. The fixture gates named are already on X9-1's list under the joint predicate: `HomeSource::Fixture`, `DurableWriteGate::for_tests`, `InitialInstallationAttempt::for_tests`, the synthetic V2 profile set, and `Image::Injected`. A callee may be widened within security at most to `pub(crate)`. That is the width `crash_matrix_support` needs for today's `pub(super)` helpers, and it is short of `pub`. The entries are compiled only under `cfg(all(feature = "crash-matrix", target_os = "macos"))`, which is the support module's existing cfg, so `scenario-fixtures` alone does not compile them. Item 2's release `compile_error!` still refuses a release build that turns the feature on. The caller passes `SyntheticInstallation`, a root path, and the public inert `RecoveryRequest`. The entry accepts no receipt, gate, guard, monitor, clock, session, permit, or `ReplayedRun`, and it returns the production composition's result.

The signature of `operation` names `InstallationTermination` on the error side. That is the signature X8 r3 item 4 gives `scenario::operation`. `begin_operation` in Rust returns `OperationRefusal`, whose `row()` is `OperationRow`. The amendment adopts X8's named result. The value returned on success is the `ProjectOperation` `begin_operation` returns.

One call to any of the three per process is X1 r1 items 1 and 7: one attempt, one receipt, one entry. The fixture seams used here take a fresh flag per call, so the support module's own flag is what enforces the limit, and a second call refuses on the invariant row with no effect. `publish_revocation` refuses, without writing, after such a call. Item 11 already has the parent publish and the child hold the operation, in different processes. `RecoveryAdmission::admit` and `SettlementSweep::admit` stay the only production constructors, which is X6 r3 items 2 and 7 and is what X6 r4 records.

The rejected alternatives are the ones that would miss the constraints: a callback that hands the same types to a closure, a home override on the production entries (a new site, and still no synthetic receipts), and waiting for X8b, which covers only the operation. The forbidden-substitute list keeps the old authority-type bullet and adds the r4 exceptions and the four new bullets. The other forbidden substitutes are unchanged.

X8 r3 items 4b and 4e still say `crash_matrix_support` returns no authority type. The header says that sentence is read, from r4 on, with this exception. X8 is not edited. `scenario::operation` stays under `scenario-fixtures`, the three entries stay under `crash-matrix`, neither surface calls the other, and there is still one site list.

G1's r3 paragraph stays. The r4 header says the matrix half now has a lawful route and X9-2 closes G1 for its own rows. X8b's ordinary-lane half is outside that sentence.

The header's sentence that the census reaches all three admissions names `InstallationAt::writer` and `begin_operation`. That is the operation composition, and the census drives it. The same census workload does not call recovery or the sweep; X9-1's review already recorded that X9-3 censuses those. Item 6 specifies recovery and the sweep from `admit` and `admit_on`, which is the composition those entries need. The header sentence is broader than the census. It does not change the three entries.

The header cites `recovery_admission.rs` lines 484–509 for `admit` always taking `HomeSource::Native`. `admit` passes `HomeSource::Native` at line 345. Lines 484–509 are `admit_on`, whose match takes `Native` in one arm and `Fixture` under the joint predicate in the other. The decision uses the facts that hold: public `admit` passes `Native`, and the fixture form is `pub(super) admit_on`. The range is a citation slip.

### The per-unit check

`tools/check_crash_matrix.py` `check`, at this commit, refuses a run whose `product.commit` is not the `--commit` argument or whose `worktreeClean` is not `true`, and it refuses the same pair on `matrix.json`'s product. It also refuses when any census-derived kill-set point has no process-death run. A unit reviewed uncommitted, covering its own rows, cannot meet either bar. That is what X9-2 found.

`check-unit` is a new command, added by X9-2, with tests. It names X9-2, X9-3, X9-4, or X9-5 and takes the required-runs rows whose case is in that unit's item 12 list. On two lead run sets it requires one run per subset row and no other run; `check`'s per-run check, with the one difference that `product.commit` is the stated base commit and `worktreeClean` may be false; a census of registered scopes with matching durability; a kill set equal to the one derived from that census; every killed point inside that kill set; release absence; limits L1 through L10; and repetition agreement on `normalizedSha256` (trust store included), every child's trace digest, and the census. Full kill-set coverage is not required. The unit's review subject manifest binds the reviewed bytes. The run records do not.

The clean-commit difference applies to both places the checker stores it: the run's `product` and `matrix.json`'s `product`. Leaving the matrix product on the strict pair would still refuse every uncommitted unit. X9-6's `check` paragraph is unchanged, and the forbidden substitute still forbids a matrix pass on a dirty worktree or on another commit. The r4 clause says `check-unit` is not that pass. Relaxing `check` itself, and skipping the checker until X9-6, stay rejected.

Item 12's halves share a case id. F39, F40, F12, and F53 are named from more than one unit, and C5 is the ladder outcome on F18, F19, and F38, which are already X9-4's cases, rather than a `required-runs` case id. A case named in a unit's bullet contributes every required-runs row of that case to that unit's subset. Overlap means each such unit checks those rows. X9-6 still checks the full file, with full coverage, on a clean committed tree.

No mechanism, point, kind, scope, label, evidence member, row, expected value, limit, or other forbidden substitute changes. No other law's accepted outcome changes.

## X6 r4 — ACCEPT

The header says the revision is record-only. It changes no API, admission step, standing, row, sweep write, test obligation, or forbidden substitute of r3, and no accepted outcome of any other law. The r3 paragraph survives, with `r3 ACCEPTED by Grok on 2026-10-04.` inserted before `Not code.`

Two records, each matching X9 r4 and the G1 line, and each stopping there.

- **Production constructors.** Item 2's read-entry bullet keeps `RecoveryAdmission::admit` as the production constructor and keeps the crate-private receipt form. The r4 note says X9's test-only `recovery_admission` runs that form over the synthetic installation. Item 7 step 1 keeps `admit_ordinary_writer` and records that `SettlementSweep::admit` stays the only production constructor, with X9's `settlement_sweep` running `admit_on` after the fixture writer admission. Both notes say the entries are test-only, add no admission step and no home override, and keep one entry per process. That is X9 r4 item 6 and X1 item 7. X6 does not take the operation entry, which is not an X6 constructor.
- **Item 11.** The fixtures bullet stays: in-process tests still use X3b's and X3c's fixtures and X4T-0. The fresh-process sentence stays, and the note says those runs, already X9's, take their fixtures and the recovery and sweep entries from `crash_matrix_support`, at X9-2 and X9-3. That is the one-line amendment X9 r3 G1 owed, and it matches X6b's deferral of admission and `recover` to those units. The in-process tests are unchanged.

## Anything else

Nothing else is wrong. The acceptance stamps are the allowed exception. No accepted sentence is deleted. The worktree was not committed.

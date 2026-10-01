# Replay join inventory123

Adds exactly four files to inventory122 (unit X3d-2, selected at product 933e78b, with D1's thirty-nine overrides joined to its projection):
- crates/evaluator/src/unavailable_evidence.rs
- crates/host/src/fact_admission_tests.rs
- crates/host/tests/refusal/cases/host_run_candidate_unnameable.rs
- crates/host/tests/refusal/cases/evaluator_replayed_second_prepare_commit.rs

`crates/host/src/fact_admission.rs` is not added. It is already a planned row of the parent, so it is kept by value (see "Changes to existing rows").

It keeps all 918 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 922 planned files.

**No new edge.** The host already depends on the evaluator (declared and resolved since before inventory119). `check_package_edges --lane host` passes against both inventory122 and inventory123, with 20 declared and 20 resolved edges.

The rows are unit X5a, one combined evaluator and host unit (law X5 r3 item 9). It covers items 2 to 5f and 8:
- `replay_candidate`, `RunCandidateInputs`, `ReplayRefusal` and `REPLAY_LIMITS`;
- the two-step mapping into the host projection `InstallationTerminationV1`, with its remedies;
- the evaluator's `ReplayError::unavailable_evidence`;
- the tests;
- law X8 r3 item 3's owner rows for this unit (group E's `ReplayedRun` reuse, and group C's unnameable `RunCandidateInputs` from X5 r3 item 5f).

The files:
- **unavailable_evidence.rs (validator).** A new private evaluator module, re-exporting `UnavailableEvidence` from the crate root. It holds the exhaustive, wildcard-free descent of item 5a over twenty-four error types, and its `cfg(test)` module.
- **fact_admission_tests.rs (test).** It is included as `fact_admission.rs`'s `cfg(test)` module, as `configuration_tests.rs` is for `configuration.rs`. It runs on the synthetic replay corpus `crates/host/tests/fixtures/replay-fixtures.json` (101 cases), with no scratch installation.
- **The two `refusal/cases` files (fixture).** Only X8a's driver compiles them, against the plain `cargo check -p opensip-host` surface. In each, the control compiles and the misuse fails with exactly one error, carrying the annotated code, fragment and line:
  - **Group C** (E0603, "module `fact_admission` is private"): `RunCandidateInputs` cannot be named outside the host. This pins X3d r6 item 11's "a `RunCandidate` in place of `ReplayedRun`" under X8's export rule.
  - **Group E** (E0382, "use of moved value: `replayed`"): a `ReplayedRun` passed to a second `prepare_commit`.

  Census rows are added for unit X5a. `RunCandidateInputs` has no inherent function, and nothing `cfg(test)` returns one, so no group F case is owed.

**Changes to existing rows.** Every row stays by value. Where a lock inheritance row overrides a row, the text judged here is the effective description. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/evaluator/src/lib.rs`: declares `unavailable_evidence` and re-exports `UnavailableEvidence`. The description stays true.
- `crates/host/src/lib.rs`: declares the private `fact_admission` module (`#[allow(dead_code)]` until X7a, as `configuration` is). The description stays true.
- `crates/host/src/fact_admission.rs`: the planned row's description ("Own host admission of provider candidates, Coverage and occupancy joins against the selected source/context before evaluation; protocol framing alone grants no fact authority.") is M3's job for this module (X5 item 1). It is out of date by omission: it does not name the M2 replay join that the file now holds.
- `crates/host/src/doctor_ingress.rs`: `row_remedy` gains the replay join's three details (`evidence.missing`, `evidence.regeneration-mismatch`, `EVALUATION.INPUT_REFUSED`), each taking `fact_admission`'s route remedy (judgment call 4). The effective description lists the remedies by owner up to X12, so it is out of date by omission.
- `crates/host/tests/admission_tests.rs` (X8a's driver): the two census rows for unit X5a and the header note. The effective description lists the census rows by unit up to X3d-1, so it is out of date (already by X3d-2's rows).

**Order.** This successor's parent is the inventory the real product lock selects: inventory122 (unit X3d-2) at product 933e78b. VD1's tooling landed at 96dd114, and D2 was bound at 933e78b, both with no inventory change. The lead assigned the number 123. It sits below inventory124 (X6a, in flight, also on inventory122). Succession is by the lock's parent pin, not by number. No earlier candidate of this unit exists.

`evidence/build_v123.py` reads the parent from the lock (by default the product checkout's `design-lock.json`, or a lock path given as its one argument). Its PRIOR table maps inventory122 to the successor record that bound its fifty-five rows. It checks each row against the lock's inheritance before carrying it. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory123. Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory122 stay bound by stable file path:
- the sixteen carried from inventory81 onward;
- D1's thirty-nine, joined at inventory122.

Only their candidate selectors move, by the four inserted rows.

**D2.** Contract successor D2 is bound at product 933e78b: four `passageSupersessions` on inventory122. As D2's README ("After selection") and law VD1 item 3 require, both the builder and the projection helper fold each bound supersession into its row's inheritance entry:
- the `before` stays the raw row text;
- the effective description becomes D2's `after`;
- the count stays 55.

The four folded rows are:
- `crates/identity/src/store_lineage.rs`;
- `crates/security/src/custody/installation_session.rs`;
- `crates/security/src/custody/read_premise.rs`;
- `crates/security/src/initial_installation.rs`.

The candidate was first built at 96dd114, before D2 bound. It was rebuilt on 933e78b before review, with no other change, so no earlier candidate was reviewed.

As a negative check, the unfolded record (built from 96dd114's lock) fails the real verify_design under 933e78b's lock: "inventory passage inheritance differs from reviewed ancestor meaning". The folded record passes.

`verify_projection.py` is inventory124's helper (itself inventory122's), with its comment updated and the supersession fold added (under 933e78b's lock, it refuses the unfolded record). It runs against the real lock at 933e78b: 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` appends inventory123 in memory over the worktree's lock (933e78b) and replaces the lock's fifty-five inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.

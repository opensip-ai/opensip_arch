I've written owner corrections for A37-01 through A37-04 in a disposable copy only. The owner's carrier validator passes 201/0 on the corrected copy, up from 87/0 on baseline, with 114 new checks. This is not acceptance: all 54 product recovery cases (F00–F53) are still not executed, and the new checks are in-memory SQLite reference controls, not durability testing.

**A37-01, lowercase-hex grammar.**
- **Change:** every hex column in the v3 journal DDL and the private attempt-custody DDL now checks the whole hex part, not just the first character.
- **Evidence:** replaying the review's probe, every non-hex or uppercase value that baseline admitted is now refused.
- **Historical scope:** the frozen v1/v2 carrier bytes are unchanged and keep the weak check. That limit is disclosed, not repaired: historical rows are read only as history and can never satisfy a schema-3 SEAL join. The earlier v3 bytes were never instantiated, so they are corrected in place.

**A37-02, first_generation at publication and {A,B} resume.**
- **DDL:** the append trigger refuses any row while no `carrier_format` row exists. A new CHECK makes `first_generation` exactly 1 on a fresh install and at least 2 after migration.
- **Act C (fresh or resuming {A,B}):** in the publishing transaction it verifies the seven definitions, an empty `grant_journal_v3`, and that any surviving witness names the admitted project. If any check fails, nothing is published.
- **Published carriers:** a new row-level check refuses any v3 row below `first_generation`.
- No new objects; the seven object names are unchanged.

**A37-03, project binding mismatch vs migration corruption.** I kept each route consistent with existing S12, the frozen v8 witness law ("witness names another carrier") and the D9 code maps.

| Phase | Observation | Route |
|---|---|---|
| Writer/maintenance open or act C | Carrier's own digest or witness names another project | operational-failed / 4 / `LEDGER.CORRUPT` / `ledger-corrupt`, no detail, nothing written |
| Writer/maintenance open or act C | Partial objects, invalid definitions, rows before publication, broken generation boundary | same class and code, detail `MIGRATION.CORRUPT` |
| Read-only recovery | The association names another carrier | existing `binding-unusable`: request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED` |
| Read-only recovery | Association matches, but the carrier's binding or footprint is wrong | quarantine row (`LEDGER.CORRUPT`, no detail), only with stable observations, otherwise busy |

`MIGRATION.CORRUPT` is never used on a read-only path.

**A37-04, F46 and F51.**
- **F46 (`unknown-carrier-incompatible`):** operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, no detail. Associations are only written with a committed v3 SEAL, so one naming an older generation is a contradiction between two records. That puts it with the existing unknown-custody row; it never becomes "not committed" or a confirmation. This is my selection among existing rows, and root decides whether to keep it.
- **F51 (split-brain):** `MIGRATION.CORRUPT` at a writer or maintenance open (the existing generation-boundary check). On read-only recovery it is the quarantine row, otherwise busy. It is re-detected at every open and never merged.
- **Where recorded:** rows added to S12, the read-only §1 table, carrier-format §8.1 and the dispatch JSON. The recovery-plan case records are unchanged, so the generated build-plan failure table doesn't move.

Interrupted migration is preserved: every check re-reads the current bytes (no cached verdict), refusals write nothing, a lawful {A}/{A,B} prefix stays resumable, and no route grants authority.

**How the controls were proven:**
- **Discrimination:** running the new validator with the old DDL restored produces 25 failures; restoring the old S12 and read-only table produces 5. Only the new checks fail in either case.
- **R1/R2 compatibility:** all nine routes are valid under both the current StepTermination schema and the R1/R2-tightened one. I did not extend R1/R2. The new request-rejected code check covers only the carrier route and asserts no global partition, so `finding.show`'s exit-2 route is untouched.
- **Kept failure:** the first probe replay crashed on the corrected copy because the review's exact format row is now refused and the probe didn't catch that. The corrected replay (p01b) records it instead.

**Other advisories:**
- **A37-07:** current-standing notes added to carrier-format, the read-only doc, carrier-migration and store-instance-lineage (current plan is F00–F53), without relabelling the Source25 history. The build-plan lines are yours.
- **Not touched:** A37-05, A37-06, A37-08 and S37-01..03 are not mine.

**Report of changed files for root (drift computed, checkers not run):**
- **Changed:** 9 files: the v3 SQL, carrier-format, carrier-migration, carrier-dispatch, check-carrier-v3, attempt-custody schema, commit-recovery-readonly, store-instance-lineage, security-and-lifecycle.
- **Bindings that drift until rebind:**
  - the candidate37 manifest pins all 9 files;
  - normative-inputs v5 binds 8 (all but the checker);
  - 8 planning coverage sources;
  - planning section S12 changes value, and S13–S16 shift line numbers only;
  - 5 source-pins ledgers each list all 9.
- **Unchanged:** generated planning inputs, all pin ledgers, and the frozen source.
- **Consequence:** pin checks, the planning checker and package verification will report drift until rebind.

**Limits not covered above:**
- **Not simulated:** witness and floor timing, act B atomicity (rows were injected with a disclosed trigger-lift harness), and the historical C1–C18 measurements.
- **Wording not discriminated:** the widened text inside the two existing S12 rows isn't tested; their class, exit and code are unchanged.
- **Whole-carrier swap:** a swap with a consistent foreign witness stays in the already-disclosed undetectable class.

All subprocesses ran in the foreground and have finished.

Files are in `/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1/` (probes and receipts are in the same folder):
- `review.md` (`ad694331…`)
- `review.json` (`e83f6a77…`)
- `proposed-edits.diff` (`806c785e…`, 1097 lines; before/after hashes in `review.json`)

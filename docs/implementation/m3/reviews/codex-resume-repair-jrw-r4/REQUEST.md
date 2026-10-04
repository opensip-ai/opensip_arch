Codex review: J-RW r4, the resume/repair writer law. This is a **law and contract-soundness** review, round 4. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No test or matrix run of any kind.** No cargo, builds, product tests, SQLite fixtures, wraparound loops, lead sets or crash-matrix runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them, at low priority, as in earlier rounds.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until it is accepted.
- **The subject:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, law J-RW r4. It is the subject of `subjectSha256`.
- **The diff base:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r3.md`, r3's exact bytes (`9aa30410…`), the subject of your round-3 review.
- **Your round-3 review,** in `docs/implementation/m3/reviews/codex-resume-repair-jrw-r3/`: `review.json`, `REVIEW.md` and `sql-source-census.json`. It raised two required findings at P2 (JRW-R3-01, JRW-R3-02).
- **X4T** is now cited at its accepted **r12** snapshot (`m2/trust-admission-x4t/PROPOSAL-r12.md`, `cf566db7…`; accepted in `m2/reviews/grok2-x4t-f2-r1`). Every X4T line J-RW cites is r12's. r3's r11 cites map to the same r12 passages, as listed in r4's short names.
- **Records** r4 notes as landed (context only):
  - J1 r5 (`m3/host-pipeline-j/PROPOSAL-r5.md`, `4ccb2320…`), `:815`;
  - M3-PLAN r9 (`m3/M3-PLAN-r9.md`, `72bc7a13…`), `:284`.
- **One pin outside both repositories:** the bundled SQLite amalgamation (SQ-SRC), unchanged since round 3:
  - `/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/libsqlite3-sys-0.38.2/sqlite3/sqlite3.c`;
  - 9,507,037 bytes, sha256 `0a409f1633283fa31a9126b11fbfd64a1991c5d30defad07e5745d4667f5e23d`.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main **`d2c00a9`**, read-only.
  - **What changed since `cd5958b`.** The product integrated X4-F2 (`988f6ed`), X3a-2 and other units. Of the files J-RW cites, only three changed:
    - `crates/security/src/trust/floor_publication.rs` changed only after line 944, so every r3 cite in it holds. r4's new cites, `:938-1001` (`fenced_first_read`), `:961-1000`, `:977-995`, `:993` and `:995`, are **re-checked at `d2c00a9`**;
    - `crates/security/src/trust/current_trust_admission.rs`: `:95`, `:100`, `:101` and `:107` are unchanged. r4's new cites, `:243-289` (`Admission`, `ClockedRefusal`, `into_view`) and `:1113-1125` (the clocked return), are **re-checked at `d2c00a9`**;
    - `Cargo.lock`: `rusqlite` 0.40.2 moved to `:322-323`. `libsqlite3-sys` 0.38.2 is unchanged at `:168-169`.
  - **Everything else J-RW cites** is the same at `cd5958b` and `d2c00a9`.
  - **The integrated test** `floor_publication_tests.rs:801-852` is cited as source only, not run.

**Scope.** r4 answers the two round-3 findings and re-pins. It should change nothing else of substance. Diff r3 against r4: every change should belong to a row of the "r4 changes and review responses" table, or to the re-pins.

## What r4 changes

1. **JRW-R3-01:** the DDL breakdown is corrected to 7 tables, 1 explicit index and 18 triggers.
   - **Where:** the r3 response row, item 3.3 (now with a per-fragment table) and RW-C17.
   - **The census:** RW-C17's census now enumerates the selected statements by kind and name.
   - **Unchanged:** k = 26, the per-fragment totals, RW-C5, its stop rule and the N-L0 fallback. No product DDL change is asked for.
2. **JRW-R3-02, lead decision LD-16:** C-TRUST and C-TDIR are composed with X4T r12's clocked write-ahead.
   - **Authority.** They are authorized on that path on the publication's own authority: the authenticated closure and the pending write the admission carries.
   - **What follows.** The completed publication returns X4T r12's clocked continuation refusal unchanged, at the same precedence. No view and no lease follow.
   - **Unchanged:**
     - earlier authentication and time refusals, and report-only reads, stay effect-free;
     - the non-reference proof and the fence;
     - the N-T2a/N-T2b mappings.
   - **Rejected:** a successful-view gate.
   - **Updated:** item 2, items 3.5 and 3.6, item 4's T terminals, RW-C14, RW-C15, J4d, the forbidden substitutes and new X-RW-13.
   - **New controls:** RW-C18 and RW-C19.
   - **RW-S5** becomes X4T r13, after r12, keeping r12's clock and write-ahead rules.

## Decide

1. **JRW-R3-01.**
   - Is 7/1/18 correct everywhere, with k = 26 and the per-fragment totals unchanged?
   - Does RW-C17 now enumerate the statements `selected_ddl()` actually selects?
   - Are RW-C5, its stop rule and the fallback unchanged?
2. **JRW-R3-02.**
   - Does item 2's clocked-path authorization compose exactly with X4T r12 (X4T:170-175, :205) and with X4-F2 as integrated at `d2c00a9`?
   - Does completion rest on the authenticated closure and pending write, return the unchanged clocked refusal at its precedence, and manufacture no view or lease?
   - Are earlier refusals and report-only reads still effect-free?
   - Is the non-reference proof still sound on the clocked path?
   - Do RW-C18 and RW-C19 cover completion followed by the refusal, and the native, custody, non-prefix and budget failures, each on its own row?
   - Is RW-S5 correctly placed after r12?
3. **Re-pins.** Do r4's X4T r12 line maps and its `d2c00a9` product cites hold?
4. **Scope.** Does r4 change anything else in r3?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. J4's sub-units each need their own inventory-unit review, and RW-S1 to RW-S6 each need their own review. Do not commit.

Codex review: J-RW r2, the resume/repair writer law. This is a **law and contract-soundness** review, round 2. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-resume-repair-jrw-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine. Do not run any lead set or SQLite fixture.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them, at low priority, as in round 1.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until it is accepted.
- **The subject:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, law J-RW r2. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r1.md`, r1's exact bytes (`0002c005…`), the subject of your round-1 review.
- **Your round-1 review**, copied into arch: `docs/implementation/m3/reviews/codex-resume-repair-jrw-r1/{review.json,REVIEW.md}`. Three required findings (JRW-R1-01 to -03) and three non-blocking observations (NB-01 to -03).
- **Changed pins since round 1.** Every law is now cited by its accepted snapshot, never by another law's live `PROPOSAL.md`.
  - **X3c is accepted at r8** by GROK2, with no findings (`m2/ledger-blob-x3c/PROPOSAL-r8.md`, `ba638efb…`; `m2/reviews/grok2-ledger-blob-x3c-r8`). J-RW's X3c joins are rechecked against it (X-RW-9). r1 was judged against r7.
  - The other laws are cited by their snapshots: X3b r10, X4T r11, X4B r5, X3d r8, X6 r4, OPP r3. Their line numbers equal r1's live-file lines, except OPP's, which shift by 2.
  - The X9 evidence census traces are now pinned.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90`, read-only. Main is now `0ceb9ad` (I1-L), which changes no file under `crates/`. Every cited product line is the same at `3e64266`, `e093e90` and `0ceb9ad`.

**Scope.** r2 answers the six round-1 items and re-pins. It should change nothing else of substance. Diff r1 against r2: every change should belong to a row of the "r2 changes and review responses" table, or to the re-pinned citations.

## What r2 changes

1. **JRW-R1-01: L-UNC gains a creation-history discriminator** (item 3.3).
   - **The cookie.** The schema cookie, `PRAGMA schema_version` (header offset 40), must be 0. The cited SQLite sources:
     - pragma.html#pragma_schema_version: "SQLite automatically increments the schema-version whenever the schema changes", and "the VACUUM command is considered a schema change";
     - fileformat2.html §1.3.9: "incremented whenever the database schema changes";
     - c3ref/c_dbconfig_defensive.html: defensive mode disables "PRAGMA schema_version=N" and "PRAGMA writable_schema=ON".
   - **Defensive mode in the product.** Every product ledger connection runs in defensive mode (`crates/storage/src/ledger_store.rs:125-133`).
   - **The guarantee.** r1's categorical "never held evidence" claim is replaced by the stated guarantee and its threat model. Forgery by a same-uid raw-byte writer is outside it, as it is outside X3c item 2's own check.
   - **The pins.** RW-C5 pins both positive crash views, and the CREATE, INSERT, DROP and VACUUM counterexample with five other committed-history fixtures as negatives.
   - **The fallback.** If a positive view fails, C-LEDGER is withdrawn, RW-L1 becomes neighbour N-L0, and L11 stays open, narrowed. New: N-L2, RW-N11. Carried into RW-S3 and X-RW-9.
2. **JRW-R1-02: C-REG's join is closed** (item 3.4, clause 3). Either N and the marker are both positively absent, or N is complete and the marker is absent, exact or P-PREFIX.
   - A present marker of any form, with N absent, is never the join.
   - The join is decided before any effect.
   - New: neighbour N-R9 (`marker-custody` / `identity-contradiction`), control RW-C16, and RW-N10 (three variants). Carried into RW-S1 and RW-S2.
3. **JRW-R1-03: new state RW-T3 and completion C-TDIR** (item 3.6).
   - **The completion.** A `may_create` trust directory (`trust/floor_publication.rs:406-414`), left without its zero-rights allow, is completed by C-ACL at `parent_dir`, under the fence, before `write_dependency`. The fenced read admits the same view as today: the successor bucket is never probed (X4T:120).
   - **The census.** The predecessor directory occurs at storage `dependency/create.after#6` (`census-trace.txt:112`) and host `#5` (`census-trace-a.txt:40`, `-b.txt:40`). It is in no kill set.
   - **The enumeration.** Item 1 now enumerates every `create.after` occurrence in both pinned censuses.
   - **New:** neighbour N-T2, controls RW-C15, and X9 rows RW-D1, RW-K10 and RW-N12. J4d and RW-S5 gain the step.
   - **L11** is retired by X9 r17 only on evidence: J4e's lead set passing every RW row, and J4c's pins holding. Otherwise it stays open, narrowed.
4. **The non-blocking observations:**
   - **NB-01:** the byte-preservation rule is scoped, with C-LEDGER as the named exception.
   - **NB-02:** N-R4 and N-T1 now say "neither exactly equal nor a strict prefix".
   - **NB-03:** the "39" example is replaced by the pinned census's seven. The 39 came from security's own X9-1 self-census table (`crash_matrix_census.rs:826`).
5. **Your request-item notes.**
   - **Item 7:** J4c no longer depends on J4a.
   - **Item 2:** your finding that IE needs no passage successor is recorded, and R1 is closed (X-RW-1).

## Decide

1. **JRW-R1-01.** Does L-UNC (item 3.3) now exclude every committed-history state reachable through SQLite's ordinary interfaces? Is its stated threat model correct and complete? Do RW-C5's positive and negative pins, the stop rule and N-L0's fallback keep the safety bias if the bundled engine's views differ? Are RW-S3 and X-RW-9 consistent with it?
2. **JRW-R1-02.** Is clause 3 exactly item 4's registration states under X2:238-247, `first_registration.rs:2260-2293` and REG:70-76? Are N-R9's rows the actual existing rows? Is the join decided before any effect?
3. **JRW-R1-03.**
   - Is RW-T3 specified completely: location, authorization, predicate, barriers and neighbours?
   - Is C-TDIR reachable without relaxing required trust admission?
   - Is item 1's enumeration of both pinned censuses complete?
   - Do RW-D1, RW-K10, RW-N12 and the conditional L11 retirement satisfy X9's rules (X9 r16 at `:146-153`, `:170`, `:920`, `:1079`, `:1236`)?
4. **The observations.** Do NB-01 to NB-03's edits do what you asked, without changing a rule?
5. **X3c r8.** Are J-RW's X3c joins sound against accepted r8: item 2 untouched, CL-3 met, the RC/RW sections and integration order (X-RW-9)?
6. **Scope.** Does r2 change anything else in r1?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. J4's sub-units each need their own inventory-unit review, and RW-S1 to RW-S6 each need their own review. Do not commit.

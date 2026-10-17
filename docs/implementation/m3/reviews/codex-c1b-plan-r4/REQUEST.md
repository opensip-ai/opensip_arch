# Review request: C1B-PLAN-r4 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, lanes or the evidence scripts.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1802 bytes, SHA-256 `c462ecae40f662794297b253972d1d8df9bfdcbec668ce83e7be7892de025025`, 8 members:
  - `c1b/PLAN-r4.md`, the subject;
  - `c1b/r4-evidence/vcs_term_r4.py` and `.output.json`, r4's derivation;
  - `c1b/r4-evidence/vcs_term_feasibility.py` and `.output.json`, r3's term as written, which C1b-1 ran before its model change, and where it stopped;
  - `c1b/PLAN-r3.md`, `PLAN-r2.md` and `PLAN-r1.md`, history and unchanged.

  Rehash all of them.
- **Bases:** product main `caa71e2` and architecture `9cf1c10d`, as the manifest names.
- **Your round 3:** `codex-c1b-plan-r3` (ACCEPT, with C1BPLAN-R3-NBO-1), at `docs/implementation/m3/reviews/codex-c1b-plan-r3/` in the architecture repository.

## Why there is a round 4

r3 is accepted. C1b-1, implementing it, ran LD-C1B-6's derivation before writing its model term. The term as r3 states it does not fit r9's caps by r9's 2× rule, so C1b-1 stopped, as LD-C1B-6 requires. r4 is the lead's revision. It changes only LD-C1B-6's pricing, adds the typed-refusal placement and one LD-C1B-2 clarification, and adds two controls and one mutation. r9's caps are unchanged.

## Authority

As in rounds 1 to 3, and also:
- **The r9 law record:** `docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md`, §5, especially :175-197: the 2× rule, the guarantee at :188, and the typed-refusal regime at :191-197. Its evidence is `c1a-r9/evidence/option3_r2.output.json`.
- **The law:** `snapshot-plan-c/PROPOSAL.md`:261, "Exhaustion is `WORK.BUDGET_EXHAUSTED`, never truncation".
- **The cost constants:** the product's `tools/security/discovery_census.py` (`costs`, `CLOSURE`) and `tools/security/discovery_member_model.py` (`read_envelope`), at `caa71e2`.
- **Git's documented formats,** as cited in the r4 table: gitrepository-layout(5), for `HEAD` and `refs/heads/name`, and git-symbolic-ref(1). The local copies are under `/Library/Developer/CommandLineTools/usr/share/man/` (man5/gitrepository-layout.5 and man1/git-symbolic-ref.1).

## What to review

`PLAN-r4.md` opens with an r4 changes table that quotes the r3 text it replaces. Judge:
1. **The exact-format pricing** (LD-C1B-6). `HEAD` and the loose ref are priced at their exact formats, not at 4 MiB: the loose ref is 41 bytes, and `HEAD` is `ref: ` + the target + LF, or 40 hex + LF, citing the Git documents. `packed-refs` stays at 4 MiB. The read caps remain the Q1 refusal bound. Also **Q7**: whether the read caps should stay at `INDEX_CAP`.
2. **The derived bounds:** D* = 226 ref directories and H* = 1,048,575 `HEAD` bytes per repository. Check that:
   - they are derived and not set;
   - they are not product constants;
   - `vcs_term_r4.py` prices what LD-C1B-6 lists, under each owner's pricing: the member reach, the `.git` reopen, `HEAD`, the directories, the loose ref, `packed-refs`, the retained values and the record allocation;
   - its outputs support the numbers, including that one more of either fails.
3. **The placement, and Q6.** Judge whether placing work past D* and H*, and the extra reads of files outside their closed forms, in r9's typed-refusal regime is consistent with r9 (`RECORD-r9.md`:188-197). **Confirm whether any law-record revision is needed.** Judge also the reduced margin r4 states for r9's guarantee.
4. **The LD-C1B-2 clarification:** `ENAMETOOLONG` on a target component refuses `ref-name`, never absent.
5. **The added controls and mutation** (§4, §5).
6. **No regression** in what rounds 1 to 3 found sound.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q6": "...", "Q7": "..."}}`, with ids `C1BPLAN-R4-RF-n` / `C1BPLAN-R4-NBO-n`. Q6's ruling must say whether a law-record revision is needed.

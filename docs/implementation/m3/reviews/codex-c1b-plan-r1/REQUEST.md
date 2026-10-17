# Review request: C1B-PLAN-r1 (the VCS observation plan, M3-C r8 item 4 with VCS-1 and M3-B successor S4), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 383 bytes, SHA-256 `427ba6eeca4ea1e0fc85ac2f1ea7add3bc30f9bb7211286d054c438d159b5888`, 1 member: `snapshot-plan-c/c1b/PLAN-r1.md` (the subject). Rehash it.
- **Bases:** product main `23b3871` and architecture `3b4171a8`, as the manifest names.

## Authority

- **The law:** M3-C r8 item 4 (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`:323-347), with C1-T15 to C1-T17; item 6's order; item 2's one snapshot ledger; the units table's C1b row and gates (:1173, :1181).
- **VCS-1:** `snapshot-plan-c/vcs-1-r1/CONTRACT.md`, as IE:546's added passage.
- **B-S2 (S4):** `config-discovery-b/b-s2/README.md` and its fragment `schemas/identity-schemas.v3.b-s2-additions.json`.
- **X2 r9:** `docs/implementation/m2/project-root-x2/PROPOSAL.md`:22 and :157, and M3-B item 21 (`config-discovery-b/PROPOSAL.md`:904).
- **The M3-C r9 law record:** `snapshot-plan-c/c1a-r9/RECORD-r9.md`, whose caps are conditional on C1a4.
- **The product as integrated on main:**
  - `crates/host/src/snapshot_seal.rs`;
  - `crates/security/src/snapshot_source.rs`;
  - `crates/security/src/custody/git_tracking.rs` and `operation_handoff.rs`;
  - `crates/security/src/discovery_export.rs`;
  - `crates/security/src/custody/workspace_declarations.rs`;
  - `crates/evaluator/src/run_links.rs` and `import_joins.rs`;
  - `tools/security/discovery_census.py`.

## What to review

The plan is round 1. Judge:
1. **The split** (C1b-0 materialization with its blind refresh, C1b-1 the Git reads, C1b-2 sealing), its order, and its dependencies on C1a4 and C1c (LD-C1B-6, LD-C1B-9).
2. **Each lead decision:**
   - LD-C1B-1: the lending carries the proof of the innermost repository, built only from X2's own observation over its own chain;
   - LD-C1B-2: the closed forms of `HEAD`, the ref name, the loose ref and `packed-refs`, the one-level symbolic rule, and the unborn refusal;
   - LD-C1B-3: `AdmittedBoundaries` as the member set;
   - LD-C1B-4: per-read custody and the `.git` evidence recheck;
   - LD-C1B-5: member reach;
   - LD-C1B-6: the snapshot ledger, the bounded VCS term, and r9's caps held, never raised;
   - LD-C1B-7: the blind refresh;
   - LD-C1B-8: typed refusals;
   - LD-C1B-10: the constant `dirty`.
3. **Fidelity to item 4, VCS-1 and S4:**
   - no Git object read;
   - no environment or global configuration read;
   - `dirty: true` for every Git case;
   - schema 3 exactly when there is an admitted member;
   - single-root bytes unchanged;
   - nothing beyond X2 r9's grant except item 4's `HEAD`, refs and `packed-refs`.
4. **Sourcing:** every bound and constant cited by file and line, with nothing invented. In particular, judge Q1's recommended reuse of X2's 4 MiB per-record ceiling for the three Git files.
5. **The controls and mutations** against C1-T15 to C1-T17 and B-S2's "Controls owed by C1b".
6. **The open questions** Q1 to Q4: give an answer or a ruling for each.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "openQuestionRulings": {"Q1": "...", "Q2": "...", "Q3": "...", "Q4": "..."}}`, with ids `C1BPLAN-R1-RF-n` / `C1BPLAN-R1-NBO-n`.

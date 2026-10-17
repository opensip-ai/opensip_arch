# Review request: M3-C r9, the law record of item 2 (the snapshot ledger's caps), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-m3c-r9-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, the T2 cache or any held-out material. The census evidence is the lead's run over the lead-readable entries only; judge its method and its recorded output, and do not re-run it.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries. You may also run the record's model-only scripts with `python3 -I -B` from the product checkout `/Users/sb/code/opensip-ai/opensip`, passing explicit product, architecture, packages-root (`/Users/sb/code/opensip-ai/opensip`), sealing (`evidence/c1a3-snapshot_seal.rs`) and, for the option script, census (`evidence/census-r2.json`) arguments. The scripts are:
  - `evidence/term_a_r2.py`
  - `evidence/option3_r2.py`
  - `evidence/term_a_discovery_bound.py`
  - `evidence/captures_term.py`

  They read the product's models, the accepted vectors, the pinned sealing copy and recorded census output, and no corpus. `evidence/term_a_r2.py` and `evidence/option3_r2.py` should reproduce their recorded outputs byte for byte.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a-r9-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 4602 bytes, SHA-256 `6bfde0782224ae7f800044ea9b559fa1146fbc01066da7629a2f7616506498cf`, 21 members: `docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md` (the subject, 29463 bytes, SHA-256 `f360d1aa9eb5b68c5ef36d1250548b60424f4c204673c73ff10ac51906d39b29`) and its evidence. Rehash every member.
- **Bases:** as the manifest names: product main `e937dac74c8e529fee3efb6f84439d05280e48ea`, architecture `27bb4ec8164aad77aeb11aa1e7b6fa24e9c3c769`.
- **The census tool** `evidence/snapshot_ledger_census.py` is a byte copy of the C1a4 candidate `/Users/sb/code/opensip-ai/opensip-c1a4/tools/security/snapshot_ledger_census.py` (not on main). `evidence/term_a_r2.py` loads that copy for the descriptor recipe.
- **The sealing input** `evidence/c1a3-snapshot_seal.rs` is a byte copy of C1a3 r2's candidate `/Users/sb/code/opensip-ai/opensip-c1a3/crates/host/src/snapshot_seal.rs`: 16400 bytes, SHA-256 `7ad4593b5bc9632cce677e978ce1a385b8d0dbb7303bc391a5ad47fad5be71a0`. C1a3 is in its lane and not yet accepted; this review does not accept it.
- **Round 1:** your `codex-m3c-r9-r1` (`REVIEW.md` and `review.json` in `/tmp/opensip-implementation/reviews/codex-m3c-r9-r1/`), REQUIRED-FINDINGS against the 16096-byte record. Round 1's census evidence is kept in `evidence/r1/`.

## Authority

- **M3-C r8** (`docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md`), item 2 ("Ledger") and item 5.
- **The C1a plan r6** (`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r6.md`; your `codex-c1a-plan-r6`): RF-1 (the r9 gate), RF-2 (term (a)), RF-3 (the non-circular blind protocol), and the r5 rule.
- **The charge models on main:** `tools/security/snapshot_ledger_model.py`, `tools/security/discovery_census.py` and `tools/security/discovery_member_model.py`, with C1a1's and C1a2's native-verified vectors.
- **The native sources on main** that the record cites: `crates/security/src/snapshot_walk.rs`, `crates/security/src/custody/discovery_rule.rs`, `crates/security/src/custody/discovery_walk.rs` and `crates/security/src/custody/workspace_declarations.rs`.
- **The owner's held-out protocol** (`docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`) and M3-B's discovery caps (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`), as precedent.

## What to review

This is a law record: it changes item 2's caps and their derivation. Judge each of the following.

1. **Round 1's findings**, each against the record's "r2 changes" table and the section it names:
   - **M3CR9-R1-RF-1** (§1): is the row bound now derived from the snapshot's own rules (LogicalPath and the 4 MiB descriptor), with no discovery depth and no new snapshot depth limit? Is the regression case (§1.4) priced correctly?
   - **M3CR9-R1-RF-2** (§1, §2, §4): are the member terms bounded by M3-B's limits as built, are they gone under (b′), and is the census's finding of no admitted member sound?
   - **M3CR9-R1-RF-3** (§4, §8): is the lower bound a valid proof of over-item-5 for each of the five, and is the reference installation's lack of directory-custody rows a valid premise?
   - **M3CR9-R1-NBO-1 to NBO-3:**
     - the sealing pin and its re-pin to C1a3 r2;
     - full-ledger margins;
     - the dearer-branch wording and the feasible refusal example.
2. **The lead's decision** (§1.5, §5, §6). Judge these:
   - Do `evidence/option3_r2.py`'s (a) and (b′) faithfully model the code changes §6 states?
   - Is the reuse argument for (a) exact?
   - Is (b′) behaviour-preserving for every caller of `classify_path`?
   - Are §6's model terms and vector changes complete?
   - Are 2^21 objects, 2^24 edges and 2^33 bytes correctly derived by the r5 rule, and rightly made conditional on C1a4 landing (a) and (b′)?
   - Are the alternatives (§5) rightly recorded and declined?
3. **The census closure and the blind refresh** (§6): `crates/security/src/custody/discovery_rule.rs` is pinned in `tools/security/discovery_census.py`'s closure, so C1a4 makes the held-out receipt stale. Is a reviewed blind refresh the right consequence, and is it correctly kept separate from C1a4's own blind validation?
4. **The finding for M3-B** (§7). Is discovery's member-classification undercharge real? Check the cited classification sites, the charge, and the absence of any other charge. Does (b′) correct it with no change to discovery's charges?
5. **The census method** (§4): lead-readable only, integrity-verified through `tools/security/discovery_census.py`'s own path, conservative pricing separate from eligibility, ids and counts only in the evidence.
6. **What r9 supersedes** (§9): is the list complete, including the product files C1a4 changes?
7. **The record's own questions** (§10).

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `M3CR9-R2-RF-n` / `M3CR9-R2-NBO-n`. Also give, for each round-1 finding id, whether it is resolved, in `review.json` as `"roundOneFindings": {"M3CR9-R1-RF-1": "RESOLVED" | "OPEN", ...}` covering all six ids.

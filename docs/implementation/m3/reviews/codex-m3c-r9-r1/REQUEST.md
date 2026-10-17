# Review request: M3-C r9, the law record of item 2 (the snapshot ledger's caps), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-m3c-r9-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, the T2 cache or any held-out material. The census evidence is the lead's run over the lead-readable entries only; you judge its method and its recorded output, and you do not re-run it.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; and running, with `python3 -I -B` from the product checkout `/Users/sb/code/opensip-ai/opensip`, the record's model-only scripts `evidence/term_a.py`, `evidence/term_a_discovery_bound.py` and `evidence/captures_term.py`, which read the product's models and no corpus.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a-r9-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 2718 bytes, SHA-256 `243c91b2440d4084055fd7bd0675645313fadabb108736d5f9681f4028161eb3`, 12 members: `c1a-r9/RECORD-r9.md` (the subject) and its evidence. Rehash every member.
- **Bases:** as the manifest names. The census tool `evidence/snapshot_ledger_census.py` is a byte copy of the C1a4 candidate's `tools/security/snapshot_ledger_census.py` (worktree `/Users/sb/code/opensip-ai/opensip-c1a4`, not on main).
- **C1a3's sealing charges** are read from its candidate, `crates/host/src/snapshot_seal.rs` in `/Users/sb/code/opensip-ai/opensip-c1a3` (in its lane; not yet reviewed).

## Authority

- **M3-C r8** (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`), item 2 ("Ledger", :246-300) and item 5;
- **the C1a plan r6** (`c1a/PLAN-r6.md`; your `codex-c1a-plan-r6`): RF-1 (the r9 gate and what it settles), RF-2 (term (a)), RF-3 (the non-circular blind protocol), and the r5 rule;
- **the charge model** `tools/security/snapshot_ledger_model.py` and `tools/security/discovery_census.py` on main, with C1a1's and C1a2's native-verified vectors;
- **M3-B's discovery caps** (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`:1210 and the status board's record), as precedent.

## What to review

This is a law record: it changes item 2's caps and their derivation. Judge:
1. **The two findings** (§1): that item 5's 100,000 rows cannot fit r8's 2^20 objects under the built charge model, and that RF-2's componentwise (a) reproduces the adversarial supremum in bytes. Are they correct, from the model's own coefficients?
2. **Q1's refutation** (§2): that the snapshot walk's listing work is not bounded by the discovery walk's charges (the depth gap, and the per-name classification factor).
3. **The recommendation** (§5): caps from the item-5-bounded terms plus the lead-readable census maximum, doubled and rounded up to powers of two (2^22 objects, 2^25 edges, 2^33 bytes), with listing work beyond them refused `WORK.BUDGET_EXHAUSTED`. Is that a faithful reading of item 2's "the recipe's charge for item 5's maximum population, with a 2× margin" (:257), and of RF-2? Are the rejected alternatives (2^37 bytes, a', r8's caps, the census alone) rightly rejected?
4. **Pre-walk captures** (§3) and **the over-item-5 classification and margin coverage** (§6).
5. **The census method:** lead-readable only, integrity-verified through `discovery_census.py`'s own path, no boundary applied and every blob new (both conservative), and ids and counts only in the evidence.
6. **What r9 supersedes** (§7): is the list complete?
7. **The record's own questions** (§8).

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `M3CR9-R1-RF-n` / `M3CR9-R1-NBO-n`.

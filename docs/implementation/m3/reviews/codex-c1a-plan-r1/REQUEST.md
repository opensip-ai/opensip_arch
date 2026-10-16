Codex review: the C1a implementation plan r1 (M3-C items 1, 2, 5 and 6: the snapshot walk, candidate blob custody, the capture session, sealing and bounds, and the snapshot ledger's caps and T2 margins). A **plan review**, round 1. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-c1a-plan-r1.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test or generator run (reading, hashing and `git show` / `git diff` are fine). Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store or T2 cache. No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/snapshot-plan-c/c1a-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `93b715a831340641ccb9a4f805176a7716c0f0ca6da0e50598cba455cda9e216`. It pins `snapshot-plan-c/c1a/PLAN-r1.md`.
- **Bases:** product `808ad6476fb848f84e732ee233a47229370081f4` (clean), architecture `43402bbc8543b0e4f265bcb4fd482c1c113f562c`.

## Authority

- **Law M3-C r8,** `snapshot-plan-c/PROPOSAL.md`: section A items 1, 2, 5 and 6, with controls C1-T1 to T11 and T17 to T27; the units table row C1a ("`snapshot.rs`: the capture session, walk, reads into custody, sealing, bounds (items 1, 2, 5, 6)"; "B2; S-B for the public projection only"); and the successor gates.
- **M3-J1 r7** item 5.4(a) and (b), on custody location and the lease.
- **M3-B r10** item 12 and the shared discovery rule. The product's `crates/security/src/custody/discovery_rule.rs`, `discovery_walk.rs`, `discovery_scan.rs`, `project_chain.rs`, `operation_handoff.rs` and `discovery_export.rs`.
- **The census and its blind receipt:**
  - `tools/security/discovery_census.py`, including `CLOSURE` and line 85's `work_ledger.rs` pin;
  - B2-b4 plan r6 section 2.5 (`config-discovery-b/b2-b4/PLAN-r6.md`);
  - the B3-b plan r2's amendment A1, the planned staleness, with B3-b2a's re-pin at `58d450c`.
- **The identity contract:** identity-v3 `$defs/snapshot`, `source-inventory` and `vcs-observation`; `crates/identity/src/descriptors.rs:538`; `canonical.rs:5`; `work_ledger.rs:185-245` (`discovery_profile`, `with_limits`).

## Decide

1. **Fidelity to the law.**
   - Does the plan implement items 1, 2, 5 and 6, and every C1a control, without adding or dropping a rule?
   - Is anything in C1a's row missing, or misplaced into C1b, C1c or J?
2. **LD-C1A-1, the split (Q1).** Security walks, judges custody and opens descriptors; host reads, custodies and seals. Is this faithful to "`snapshot.rs` holds the only source-read site" (C1-T2)?
3. **The snapshot ledger and the census (Q2, LD-C1A-7).** Is a `snapshot_profile` constructor required (could `with_limits` or `discovery_profile` serve)? Is the planned receipt staleness, with the census re-pin at C1a1 and the reviewed blind refresh in C1a4 under B2-b4 plan r6 section 2.5, acceptable? Are the pricing recipe and cap derivation (C1a4) a sound reading of item 2's r4 text?
4. **LD-C1A-2 to 6:**
   - the extent never copied;
   - one read through a reused buffer, with before and after samples;
   - custody location taken from the caller;
   - `kind: none` only, with `SnapshotVcsPending` until C1b (Q3);
   - the empty read set until C1c.
5. **The carrier join.** Is building `ProjectCarrierObservation` from the B1 resolver input's project carrier right? Is the seven-row table complete?
6. **Sequencing, checks and mutations.** Are the four steps' order, the lanes and the planned mutations adequate, and is any risk unaddressed?
7. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1APLAN-R1-RF-n` / `C1APLAN-R1-NBO-n`.

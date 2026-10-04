CODEX2 review: M3-C r1, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run is using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests or estimates, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The subject is untracked in arch until acceptance.
- `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the law. It is the subject of `subjectSha256`.

**The unit.** M3-C is a row of the accepted M3 plan (`docs/implementation/m3/M3-PLAN.md:163`). The row has four parts:
- **C1:** `snapshot.rs`, exact read-set bytes under custody, and `snapshot2` (IE:179).
- **C2:** native contexts and closure admission (NE:1430-1645; BP:699-713), with synthetic signed closures for tests.
- **C3:** dependency sources and prepared outputs: DS-1..DS-6 (NE:1646-1698), with a library-level import of user-named sources (DS-5, NE:1688); PO-0..PO-4 (NE:1803-1870); and a harness recipe for prepared sets.
- **C4:** `plan.rs`, `plan2` (IE:182), the prospective-Plan bounds (NE:4276), and X12d (X12:192).

**The governing records:**
- M3-PLAN r4, accepted;
- M3-I1 r2, accepted (`preview-pack-i1/PROPOSAL.md`; LD-10 at I1:428, and item 8 at I1:390-396);
- X12 r3, accepted (`docs/implementation/m2/policy-admission-x12/PROPOSAL.md`);
- EC1 (`docs/implementation/m2/core-evaluator-closure-ec1/README.md`).

M3-L r1 (`provider-protocol-l/PROPOSAL.md`) is a gated **draft**. The law states its consistency with L's INC items (item 20), and L's acceptance is part of this law's gate.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `30c5db1`, read-only.

## What the law decides

1. **The snapshot (items 1 to 6).**
   - **Bytes:** one read, and the bytes hashed are the bytes retained and analyzed.
   - **The walk:** the reach of the discovery rule, not narrowed by scope; S3 custody; `O_NOFOLLOW` reads with an inode recheck and no retry; symlinks and special files neither followed nor inventoried; unrepresentable names refused; `.gitignore` not honoured.
   - **`node_modules`:** a package-granular read set restricted by a closed suffix table.
   - **VCS:** HEAD resolved from refs only, and `dirty: true` read as "cleanliness not established".
   - **Bounds:** 100,000 rows, the 4 MiB descriptor and 8 GiB in total. The estimate that the 4 MiB cap holds about 27,000 rows is flagged, with a likely identity successor (S-R).
2. **Closures and contexts (items 7 to 10).**
   - **Admission:** one signed path, with a role-to-kind table (CR-1).
   - **Tests:** synthetic signed closures that go through the production admission path.
   - **The bundled pack's detector closure (I1 LD-10):** **the core detector closure**, which is the authenticated core descriptor with `kind: detector`, as EC1 does for `evaluator`. It joins the seal's evaluator closure.
   - **Import roles:** core adapter and import-producer projections for the in-core importer (CRC-1).
   - **Contexts:** minted by the host before PlanId and admitted by the same functions that Run closure re-runs. `baseCfg` is closure data.
3. **Dependency sources and prepared outputs (items 11 to 15).**
   - **The importer:** library-only `imports.rs` for the `dependency` and `prepared` kinds, with no command.
   - **DS rules:** DS-2 deterministic `.crate` extraction, and DS-1, DS-3 and DS-4 as published.
   - **The launch gate:** unified features come only from bundled `cargo metadata` through the adapter. That adapter is a tool launch under the D law and is unavailable before O7 and D1.
   - **Self-references:** null in every M3 record. The Plan joins its delivering import by identity, and native-input imports enter `plan.importIds` through that join, never through the configuration (NIJ-1).
   - **Prepared sets:** `imported-descriptor` only, in explicit mode only.
   - **Harness recipes:** H-DEP, H-NM and H-PREP, with prepared sets declarative only. T2 prepared-mode measurement waits for M5.
4. **The Plan (items 16 to 19).**
   - **Members and order:** a source for every member, and the pre-Plan order.
   - **Bounds:** NE:4276-4280, exactly.
   - **The pack citation:** including the `imports`-cell symbol inventories in the enumeration plan.
   - **X12d:** wired into replay; the pin tests amended; the corpus regenerated onto the **release** preview pack (with the reason the test pack cannot work); an X9 matrix rerun.

## Decide

1. **Snapshot soundness against IE §3, SL S3 and NE §1.4.**
   - Do items 1 to 6 discharge "exact read-set bytes under custody" (CH14:495; SL:313-315; IE:548-593)?
   - Is a walk that scope does not narrow consistent with IE:341-351 and L:153?
   - Is the `node_modules` suffix rule a lawful read set under IE:552-592 and SL:266-279?
   - Is item 4's `dirty` reading acceptable (reviewer question V2)?
   - Check item 5's size arithmetic and its T2 examples against T2M.
2. **Closure admission and the detector closure.**
   - Is item 7's role-to-kind table a sound host-vocabulary decision under SL:21-60 and BP:701-709?
   - Is item 9's core detector closure lawful under COMP:9, IE:272-285, IE:1508-1512 and WS:277-316 (V1)?
   - Does it discharge I1 LD-10's obligations (I1:41, I1:428)?
   - Is the rejection of LD-10's one-document tree sound?
   - Are the core adapter and import-producer projections sound and adequately confined (R1)?
3. **Imports.**
   - Is item 13's identity join (null self-references; native-input imports outside the configuration's `evidence.importIds`) consistent with IE:179, IE:181, IE:220-221, IE:1370-1373, AQ:51 and NE §7 (V3)?
   - Is the circularity argument correct?
   - Is X-2 (`acquisitionSourcePath` in identity against WS:1539-1541) a real tension?
4. **The DS, PO and launch rules.**
   - Do items 12 and 14 implement DS-1..DS-6 and PO-0..PO-4 faithfully?
   - Is treating the `cargo metadata` adapter as a D-law tool launch, outside L item 2, consistent with L:119-147, L:494-506 and NE:2499-2500?
   - Is "explicit mode only" a sound reading of PO-1 at M3?
5. **The harness recipes and the no-execution rule.** Does item 15 keep M3P:355 and Q0:688-692, and Q0 §10's "only networked step"? Is the deferral of T2 prepared mode the necessary consequence?
6. **The Plan and X12d.**
   - Are item 16's member sources and the pre-Plan order correct against IE:182, IE:1360-1377, IE:1416-1425 and X12 items 8 and 9?
   - Is item 17 an exact implementation of NE:4276-4280?
   - Is item 19's deviation from X12:192 (the release pack rather than the test pack) correctly argued from `policy.rs:1361-1367` and `:1412`?
7. **Consistency with M3-L (item 20).** Does any C decision contradict L items 1 to 17, especially items 3 and 4 (cache keys bind the Plan; changed-scope reuse needs an identity successor)?
8. **Successors and units.**
   - Is the successor list complete?
   - Is the unit breakdown sound, waiting for X9-6, P0, L and I1?
   - Is the critical-path claim (C2 split in parallel; X12d beside H) correct against M3P:202-231?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The contract successors this law lists (CRC-1, CR-1, NIJ-1, VCS-1, S-B, S-R, T2-DEP) will need `ACCEPT-DESIGN-UNIT` reviews of their own. X12d and the C code units are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.

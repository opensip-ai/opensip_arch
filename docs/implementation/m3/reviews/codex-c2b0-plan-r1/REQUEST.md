# Review request: C2B0-PLAN-r1 (the C2b-0 implementation plan: the `node_modules` layout; M3-C r8 items 3 and 10), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2b0-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2b0-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 578 bytes, SHA-256 `e06858bb1c3f11495516f26a5e4fdc8ec552e672b98b3573bb307fdab40eb43c`, 2 members:
  - `c2b/PLAN-r1.md` (the subject);
  - `c2b/C2B-GATING-r1.md` (the prior gating record, context only).

  Rehash both.
- **Bases:** as the manifest names (product `3d1d771`).
- **Related, in review separately:** the C1c plan r2 (`snapshot-plan-c/c1c/PLAN-r2.md`). This plan depends on its C1c-0 interface (LD-C1C-2, LD-C1C-5, LD-C1C-12) and states that it is revised if that review changes it.

## Authority

- M3-C r8 (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`):
  - item 3 (:302-321), especially step 1 (:305) and the last bullet (:311);
  - item 1's capture-session rules (:207-226);
  - item 2 (:271-279);
  - item 6 (:377-393);
  - item 10's TypeScript list (:564-571);
  - the Units table (:1182, :1184);
  - and the r9 law record's caps.
- NE's `ResolvedNodeModulesLayoutV1` (`docs/v2/contracts/product-v1/native-evidence.md`:1399-1419, :1490), and its schema (`opensip/schemas/sources/native-v2.schema.json`:6971-7016).
- IE:548-593 and SL:266-279.
- The reference model's consumer side (`docs/coop/design-corrections/native/native_evidence_model.v2.py`:2811-2813, :2925-2943).
- The evaluator's `inspect_typescript_universe` (`opensip/crates/evaluator/src/native_universe.rs`:142, :235-252).
- The C1b plan r3 (accepted) for the census batch rules.

## What to review

1. **The split.** Does a layout-only C2b-0 satisfy the law's C1c edge "C1a; C2b's layout" (`PROPOSAL.md`:1182), so that C1c-1 is not held behind C2a? Is the gating record's finding right: the layout needs no manifest-admitted closure, while C2b's context half needs C2a?
2. **The walk:**
   - LD-C2B0-1, the ancestor chain inside the project;
   - LD-C2B0-2, package directories, scoped names, and the `.`-prefixed exclusions including `.pnpm`;
   - LD-C2B0-3, nesting;
   - LD-C2B0-4, links observed with `readlinkat`, resolved lexically, targets reached by the no-follow opener, and every `realPath` itself a row.

   NE says only "as the resolver walks it" (NE:1404) and publishes no derivation, so these are lead decisions. Judge whether they are a faithful, deterministic and sufficiently closed reading of Node's resolution for npm, nested-npm, pnpm and workspace-link layouts.
3. **The manifest** (LD-C2B0-5): one capture through the session, reused for first-party targets; `contentSha256`; `name` and `version` by the identity JSON reader within its existing 4 MiB `MAX_BYTES`, with no new cap.
4. **Exclusions** (LD-C2B0-6): the walk's own `SnapshotExtent` and `read_set_path` applied first.
5. **Ledger and census** (LD-C2B0-7): the lead's choice of the snapshot ledger, which the law leaves unnamed for C2's reads (Q5), with C2b-0 owning a layout model term under r9's fixed caps, and the receipt-specific census accounting.
6. **Refusals, admission and agreement** (LD-C2B0-8 to LD-C2B0-10), including returning `None` rather than an empty layout.
7. **Controls and mutations** (§4, §5): adequate for lead-authored vectors with no reference oracle?
8. **Rule on Q1 to Q5.**

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2B0PLAN-R1-RF-n` / `C2B0PLAN-R1-NBO-n`.

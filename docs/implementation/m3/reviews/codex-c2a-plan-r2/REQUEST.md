# Review request: C2A-PLAN-r2 (the C2a implementation plan: closure admission and the core role closures; M3-C r8 items 7, 8 and 9), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, **signing keys or private test keys**, held trees, any T2 store or the T2 cache. Cite fixture signers by their source names; never open key material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 957 bytes, SHA-256 `2e7166af52e6ef2812489ba3f292835e7f52c005fc502eac3ea5e099f82587c8`, 4 members:
  - `c2a/PLAN-r2.md` (the subject);
  - `c2a/PLAN-r1.md` (history);
  - `c2a/X-C2A-1-r1.md` (the cross-law memo, context: the input to the component-delivery law, not under review as law);
  - `c2b/C2B-GATING-r1.md` (context).

  Rehash all four.
- **Bases:** as the manifest names (product `b753854`). Since round 1's `3d1d771`, product moved only by D2b-0b's generation and its lock, which touch no file the plan cites.
- **Your round 1:** `codex-c2a-plan-r1` (REQUIRED-FINDINGS: RF-1 to RF-5, NBO-1, NBO-2, Q1 to Q4 rulings), at `/tmp/opensip-implementation/reviews/codex-c2a-plan-r1/`.

## Authority

As in round 1. In addition:
- C2PM-1 (`snapshot-plan-c/c2pm-1-r2/`: CONTRACT.md, `closure-protocol-routes.json`, `materialization-map.json`, `successor.json`) and its integrated body materialization (`c2pm-body-r1/`);
- NE:1493-1499;
- J1's `ExecutionIdReservations` (`host-pipeline-j/PROPOSAL.md`:250) and J-C10b, with M3-D's D4-T1;
- E's item 14a and E3-T13 and E3-T14 (`syntax-e/PROPOSAL.md`:710-711);
- CRC-1's LD-4 (`crc-1/README.md`:147).

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **RF-1** (LD-C2A-4, LD-C2A-11):
   - C2PM-1 as authority and dependency;
   - mandatory authenticated presence;
   - the guards in C2PM-1's deterministic order;
   - the role support table;
   - the exact integer copy;
   - the origin-sensitive routes with the full failure envelope;
   - no inference from `compatibility.providerProtocol`.

   Is the split between what `c2pm-body-r1` already materialized and what C2a still owes right?
2. **RF-2** (LD-C2A-5, LD-C2A-12, §2): the unadmitted `ClosureCandidate` versus the `AdmittedClosure` that only C2a-3's whole retention yields. The compiler and stdlib are covered by NE:1493-1499, the fixture uses the same verifier, and C2a-1 and C2a-2 do not unblock successful C2b-1 admission.
3. **RF-3** (LD-C2A-1): admission completes inside R10a and ER10a before they return. Check the order (trust read, D4, C2a), that selection and retention come after the draw, and the J-C10b and D4-T1 reservation controls.
4. **RF-4** (LD-C2A-3, LD-C2A-10):
   - the count predicate on constructed input;
   - the upstream 100,000-entry manifest cap;
   - the 4 MiB descriptor bound;
   - R10a's scope as the ledger;
   - the published pre-allocation costs and the aggregate across components.
   Q5 asks which profile R10a's scope uses.
5. **RF-5** (LD-C2A-8): is the field-use matrix complete and correctly owned, with CRC-2's mirror rule and the symbol-inventory and candidate-result exclusions?
6. **NBO-1 and NBO-2:** the closed platform join to the same release's artifact token; the existing C2-T9 vectors named.
7. **The Q rulings applied:** the Q3 interim (not installed versus a retained-tree failure keeping its cause; no X-8 resolution; no ephemeral detail); the Q4 shared fixture module under exactly the joint predicate.
8. **The memo** `X-C2A-1-r1.md`, as context: does it state the gap correctly against X4B, 463h and SL:35-38?
9. **Rule on Q5 and Q6.**

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2APLAN-R2-RF-n` / `C2APLAN-R2-NBO-n`.

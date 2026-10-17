# Review request: D2B-3a-r1 (the TS2 codec's receive side, D2b plan r3 with amendments A1 and A2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-3a-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, generators or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, and these read-only commands, run in the candidate worktree:
  - `python3 -I -B tools/check_operability.py source --repository .`;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-3a-r1/evidence/check_d2b3a_duty_table.py . /Users/sb/code/opensip-ai/opensip_arch /dev/stdout`;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-3a-r1/evidence/check_d2b3a_dlv_records.py . /Users/sb/code/opensip-ai/opensip_arch /dev/stdout`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-3a-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 26486 bytes, SHA-256 `a53b885883c9db386e877a5e0d8a767e85527e59126cfd43294a327127e32ab2`, 111 members, including the proposed plan amendment `supervisor-d/d2b/PLAN-r3-A2.md`. Rehash every member.
- **Bases:** product `01769e93db878836612d9e3d483a054f7ad1da94` and architecture `8fde46bb981e1304a79aa997ed154cdc4435632a`.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b3`, detached at the product base. Its edited and new paths are frozen as `d2b-3a-r1/product/` copies, with their parent and candidate pins in `product-map.json`.
- **Read first:** `PLAN-r3-A2.md`, then `d2b-3a-r1/SCOPE.md`, the code, the tests, and `evidence/` (the lane of record `d2b3a-checks-r1/`, its runner, and the two checks).

## Authority

- **The law:** M3-D r5 items 10 and 11 (`supervisor-d/PROPOSAL-r5.md`).
- **The plan:** D2b plan r3 (`supervisor-d/d2b/PLAN-r3.md`, accepted, `codex-d2b-plan-r3`) and amendment A1 (`PLAN-r3-A1.md`, accepted with D2b-0 r2): section 0, LD-D2B-2, LD-D2B-3, LD-D2B-12, LD-D2B-15, LD-D2B-18, section 3 and section 4.
- **The wire sources:**
  - the carriers (`schemas/wire/native-carriers-v1.json`: `records`, `protocols.typescript-semantic`, `admission`, `commitmentMap`);
  - DLV (`docs/coop/artifacts/delivery.v2.json`);
  - the handshake and startup schemas and their laws (`schemas/sources/handshake-v1.schema.json`, `startup-v1.schema.json`);
  - T2O (`crates/components/data/typescript-protocol2-order.v1.json`);
  - the fact-plane registries (`fact-plane.v1.json`, `relation-payload-schemas.v2.json`).
- **The integrated dependencies:** D2b-1 (the reader, `ReceivedBytes`, the commitments), D2b-2 (the table engine), D2b-0 and D2b-0b (the successor schemas' admission and generated carriers), and D3a-1 (`ProcessEvent`).

**Amendment A2 is proposed with this unit.** Judge it as an amendment to the accepted plan's text. A2-1 splits D2b-3 and D2b-4 into three parts each; A2-2 adds the descriptor fields to LD-D2B-15's context; A2-3 allocates the mutations. Accepting this unit accepts A2. A verdict with required findings against A2 rejects both.

## What to review

1. **A2:** its reasons, each quoted passage and its replacement, A2-2's source (the handshake law's `typescriptDescriptorBinding` rule and `TypeScriptHelloAckV2`'s description), and that the law and the carriers are unchanged.
2. **Steps 7 to 10 and their order**, and that every refusal precedes the table and any published payload.
3. **LD-D2B3-1:** the carrier interpreter, the interpreter's fail-closed load, and the DLV comparison.
4. **LD-D2B3-2:** whether piecewise admission of Coverage, post-Analyze Unavailable and BudgetExhausted is equivalent to whole-document admission under the asserted precondition.
5. **The contextual admission,** frame by frame (SCOPE's table): each rule against its source, in particular LD-D2B-18's HelloAck gate with A2-2's fields, DISPATCH-STAGE-CORRELATION's counters, FP-CANDIDATE with LD-D2B3-4's registry sources, ANCHOR-WIRE-SPAN, PER-KEY-SCOPE2, and the terminals' coverage.
6. **The commitments:** each recomputed over received bytes under its `commitmentMap` row, and the provenance control's sufficiency.
7. **LD-D2B3-3 to LD-D2B3-10:**
   - the `GeneratedJson` re-export and contracts' public API;
   - the vendored copies and their pins;
   - the floats in `fact-plane.v1.json` and the member read;
   - the depth bounds (7 and 1) and their recomputation;
   - the context's shape;
   - the reused schema budget;
   - the relation payload profile;
   - the `Participant` placement;
   - the `unresolved-edge` layer observation.
8. **The duty table:** that section 3 lists every carriers admission id once, and that every TS2 row it gives received-frame admission is implemented here.
9. **The controls:**
   - the lane: equal failure sets and the new passing tests (components 17), rustfmt, Clippy, the two checks, the operability census, the environment exceptions, the census-closure check and verify_design;
   - eight mutations, each caught.
10. **No regression,** and nothing assigned to D2b-3a left unowned.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "amendmentA2": "ACCEPT" | "REJECT", "subjectManifestSha256": "a53b885883c9db386e877a5e0d8a767e85527e59126cfd43294a327127e32ab2", "requiredFindings": [...], "nonBlockingObservations": [...], "productQualification": false}`. Use ids `D2B3A-R1-RF-n` and `D2B3A-R1-NBO-n`. `ACCEPT-UNIT` requires an empty `requiredFindings` list and `amendmentA2: "ACCEPT"`.

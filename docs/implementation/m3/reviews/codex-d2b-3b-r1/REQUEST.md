# Review request: D2B-3b-r1 (the TS2 codec's send side and participant, D2b plan r3 with amendments A1 and A2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-3b-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, generators or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, and these read-only commands, run in the candidate worktree:
  - `python3 -I -B tools/check_operability.py source --repository .`;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-3b-r1/evidence/check_d2b3b_duty_table.py . /Users/sb/code/opensip-ai/opensip_arch /dev/stdout`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-3b-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13589 bytes, SHA-256 `c7aed6170f989af695acded21dccecece268651ca340da0065422758b4a031e7`, 56 members. Rehash every member.
- **Bases:** product `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` and architecture `dc96415fa99b2df4849dbf3920e9d45739f1ed05`.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b3b`, detached at the product base. Its edited and new paths are frozen as `d2b-3b-r1/product/` copies, with their parent and candidate pins in `product-map.json`.
- **Read first:** `d2b-3b-r1/SCOPE.md`, then the code, the tests, and `evidence/` (the lane of record `d2b3b-checks-r1/`, its runner, and the duty-table check).

## Authority

- **The law:** M3-D r5 items 10 to 15 (`supervisor-d/PROPOSAL-r5.md`).
- **The plan:** D2b plan r3 (`supervisor-d/d2b/PLAN-r3.md`, accepted, `codex-d2b-plan-r3`) with amendment A1 and amendment A2 (both accepted; A2 with D2b-3a r1): A2-1's D2b-3b row, LD-D2B-7, LD-D2B-9, LD-D2B-15, LD-D2B-18's sender half, section 3's builder and sender rows, section 4's RF-2 builder and sender controls, and A2-3's mutation.
- **The wire sources:**
  - the carriers (`schemas/wire/native-carriers-v1.json`: `protocols.typescript-semantic.frames`, the host records, `admission` REQUEST-WIRE-ACCOUNTING and HOST-SEND-SCHEDULE with their `params`, `commitmentMap`);
  - the reference sender and planner, trial 07's `tools/sender_ref.py` and `tools/representability.py` (HOST-SEND-SCHEDULE's `params.reference`);
  - DLV (`docs/coop/artifacts/delivery.v2.json`: `closedHostToWorkerFrames`, `stageRequestProjection` and its `budgetProjection`, `coverageDomain`, `commitments.domains`, CoverageKeyV1, CancelV1);
  - the handshake and startup schemas (`TypeScriptHelloV2`, `TypeScriptProtocolLimitsV1`, `IdentityVersionsV1`, `TypeScriptOpenUniverseV2`, startup `universeIdentity`);
  - T2O (`crates/components/data/typescript-protocol2-order.v1.json`).
- **The integrated dependencies:** D2b-3a (the receiver, its carrier interpreter, its `DispatchContext`), D2b-1 (framing, the encoder, the commitments), D2b-2 (the table engine), and D3a-1 and D3a-2 (`Participant`, `ParticipantStatus`, `ProcessEvent`).

## What to review

1. **The builders:** each of the seven host frame families built from the Plan's values and closed-checked, and each value against its source: the Hello's tokens and constants, OpenUniverse's recomputed `universeKey`, the manifest and seal from the sealed inventory, and Analyze's projection, budget, subject scope, keys and commitments.
2. **The schedule constructor** (REQUEST-WIRE-ACCOUNTING; LD-D2B-9): against its `params` and the reference planner. Check the slot binding, the greedy chunk sizing in closed form, the chunk digests over the payload without `bytes`, the entry and frame bounds through the carriers' route, and the reserved maximal Cancel.
3. **The sender** (HOST-SEND-SCHEDULE): against its `params` and `sender_ref.py`. Check that realization is independent of the planner, that every slot member is compared before sent state, the chunk content over the bytes sent, and the refusal ending the transcript.
4. **The Cancel law** (LD-D2B-7; CANCEL-NULLABILITY): once, never before the Hello slot, `user-interrupt` only, the exact echo of the sent state compared by deterministic-CBOR bytes, at the next sequence, nothing after it.
5. **The participant** (A2-1; LD-D3A-3):
   - the yield contract;
   - the T2O gate (LD-D2B3B-6);
   - the context and request joins (LD-D2B3B-5);
   - progress from admitted transitions only (item 15);
   - the terminal output minted once;
   - the status mapping, including R1's `ParticipantStatus::HostFault` and its one `apply_step` arm in `supervisor.rs`.
6. **The lead decisions** LD-D2B3B-1 to LD-D2B3B-12, and D2b-3a r1's two non-blocking observations as SCOPE carries them (NBO-1's base; NBO-2's depth witness, now a lawful Coverage frame).
7. **The duty table:** every TS2 row section 3 gives the builder or the sender is implemented here and named.
8. **The controls:**
   - the lane: equal failure sets and the new passing tests (components 15), with D3a's fixture record written on both sides, rustfmt, Clippy, the duty-table check, the operability census, the environment exceptions, the census-closure check and verify_design;
   - the mutations, each caught.
9. **No regression,** and nothing assigned to D2b-3b left unowned.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "c7aed6170f989af695acded21dccecece268651ca340da0065422758b4a031e7", "requiredFindings": [...], "nonBlockingObservations": [...], "productQualification": false}`. Use ids `D2B3B-R1-RF-n` and `D2B3B-R1-NBO-n`. `ACCEPT-UNIT` requires an empty `requiredFindings` list.

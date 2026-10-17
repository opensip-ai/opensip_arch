# D2B-PLAN-r3 review

Verdict: **ACCEPT**. No required findings or non-blocking observations.

## Exact subject

Independently verified the 752-byte manifest SHA-256 `d9b2a082c8a7b157c915c9df38039956d47b23806dcff7f608cea527dc99d1f8` and all three members:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `d2b/PLAN-r3.md` | 42177 | `52ea93fb7737168225f13c099b4dfa5725c52609d8412ffa3fcb0813f437c3b1` |
| Historical `d2b/PLAN-r2.md` | 37546 | `86431605d32213a2b86788d01c806613973321edede141e6167c0f0ac4ad3f79` |
| Historical `d2b/PLAN-r1.md` | 11905 | `35a2da79401936e7ef06700f9318a8dbb3ec8e9b3caed4aa4383f264e44c2801` |

Both historical plans retain their prior reviewed bytes. Compared the complete r2/r3 diff and checked the revised text against NE §9.1, the FA-2 and RUST3-LIM sections, M3-D r5 items 10–11, and the product wire carriers.

The named bases are historical: live architecture HEAD is `0272078ece3de70e4d6e0bd62712acfccca45609` and product HEAD is `41f6cae7c03e975b16db52a9b5f4d015e7468682`. Git comparisons confirm no changes from the requested bases to the relevant architecture authority paths or product schemas/contracts. This movement does not alter the plan subject or the authorities used here.

## Round-2 findings

**D2BPLAN-R2-RF-1 resolved.** LD-D2B-18 requires exact Hello/HelloAck token-array equality for both protocols and all tokens, including the optional census, reference-scope and target-attribution tokens. An omitted offered token or an added unoffered token faults at HelloAck before OpenUniverse or source disclosure; the session cannot continue by treating the token as absent. The sender takes the Hello array from the admitted selection. This agrees with NE §9.1's exact sorted-array echo and signed-selection boundary.

LD-D2B-16 and -17 now use both exact arrays to select their negotiated variants. The lawful historical branch exists only when both arrays omit the token. Section 4 separately controls census omission/addition in each protocol and reference-scope/target-attribution omission/addition in Rust, plus the eight lawful independent Rust token combinations. The previous “negotiated off” control is withdrawn. Payload mismatch controls and before-writing sender refusals remain explicit.

**D2BPLAN-R2-RF-2 resolved.** Section 4 now partitions controls by the owner and refusal point already assigned in §3 and LD-D2B-12:

- Schema admission, step 8: FactBatch cardinalities zero and 4,097, and other shape/count violations. The product's four historical/V3 FactBatch carriers all impose 1..4096 facts or candidates.
- Builder or sender, before writing: request stage ordinal, exact Plan-stage bytes, absent-versus-null preservation, and selected-stage projection.
- Contextual admission, step 9: schema-valid worker stage/Analyze correlation, batch/candidate counters and T020 stage/observed mismatches, before table matching.

The blanket claim that every control passes schema validation is gone. Earlier checks are not bypassed and every refusal still precedes publication. LD-D2B-15's retained prechecks and contextual counters remain in force without moving host construction checks into worker admission.

## Observations and regression check

**D2BPLAN-R2-NBO-1 addressed.** LD-D2B-17 now distinguishes the 256-subject inline cap from F-1's oversized Analyze envelope. It correctly attributes the latter to LD-D2B-9's exact schedule sizing and C4's pre-spawn refusal. The new at-or-below-256 oversized-inline control is separate from the existing 257-subject constructor refusal.

**D2BPLAN-R2-NBO-2 addressed.** OWNER-PATTERN-EVALUATION now names the startup carriers, occupancy-companion schema and transitive external wire schemas reached by D2b's checks, with H's relation-payload and the Plan evidence consumers retained. This fills the prior consumer-allocation omission.

Independently compared §3 with the product admission list: all 55 carrier admission IDs appear exactly once. The r3 changes preserve the earlier accepted allocations and mechanisms: separate received commitment preimages and full encoded spool accounting; reader-only received-byte provenance; immutable dispatch context and live counters; successor-specific controls and H's clean-settlement boundary; schedule construction and C4's refusal ownership; strict successor-aware CBOR depth and NFC controls; table/overlay data replay; protocol-specific anchor order; restricted sender Cancel; and D3's process-observation ownership. The five-subunit order and immediate reviewed blind refresh after materialization are unchanged.

The revision adds no shared provider semantic type, wire normalization, invented response bound, fact admission or qualification claim. The remaining questions Q1–Q3 retain the satisfactory boundaries recorded in the round-2 review, with the two required control corrections now applied.

## Scope

Acceptance is of this implementation plan. It does not accept future materialized schemas, codec implementations, lanes, refreshed blind receipts, supervision, D2 completion or product qualification. Each subunit retains its own review and verification obligations.

Used only read-only inspection, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, lanes, network, other panes or delegation. No private fixture, installation, signing key, held tree, T2 store or cache was accessed. Neither repository, worktrees nor control files were edited. Only the two requested review files were written.

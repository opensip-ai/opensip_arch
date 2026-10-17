# D2b plan r1 review

Verdict: **REQUIRED-FINDINGS** — three required findings and three nonblocking observations.

This is a plan review only. The 380-byte subject manifest hashes to `b1f997d76f25ee5154c3b2e9bda09f3417573714bdf74b5f68fafb06b004414f`. Its sole member, `d2b/PLAN-r1.md`, is 11,905 bytes and hashes to `35a2da79401936e7ef06700f9318a8dbb3ec8e9b3caed4aa4383f264e44c2801`. Both pins verify. Architecture HEAD is the requested `2894884ef33b0434a7c09029d2f727cf5f7a2524`; product HEAD is the clean requested `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`.

## Required findings

### D2BPLAN-R1-RF-1: Separate received commitment preimages from the encoded spool entry

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:68`.

LD-D2B-3 requires the spool entry to be asserted equal to received payload sub-slices. RPP limitPolicy.candidateSpoolAccounting instead requires a newly encoded closed map {analysisOrdinal,stageId,candidate}; that wrapper is not the received candidate sub-slice, candidate array or envelope. A literal equality check rejects valid batches, while substituting slice length undercharges the spool. The next sentence also describes stream commitments only over candidate bytes and only at Coverage or Complete, although coverage commitments use CoverageResultV3 entries and post-Analyze Unavailable/BudgetExhausted also carry coverage-stream commitments.

Required change: Specify separate representations: retain exact received candidate and coverage-entry encodings for the corresponding owner commitment recipes; construct each spool-entry map from the validated value and charge its complete deterministic-CBOR encoding before append. Any byte-equality assertion compares the re-encoded candidate to its candidate slice, not the whole spool entry. Bind each stage, stream and terminal field to commitmentMap, including the terminal coverage arrays. Add controls distinguishing spool wrapper bytes, fact versus coverage preimages, and terminal commitments.

### D2BPLAN-R1-RF-2: Include stateful payload admission between schema validation and table matching

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:89`.

The proposed check order ends with a closed payload schema followed by the transition table, without assigning the retained contextual admission duties. P3T plus its overlay is deliberately not the complete payload validator: the overlay explicitly retains rust2 framePrecheck and T016/T020 payload guards. In particular DISPATCH-STAGE-CORRELATION requires the requested C-2 stageId, Analyze-relative ordinal, analysisOrdinal and expected batch/candidate counters. A well-typed batch with another stageId or a replayed batchIndex can pass the closed schema and P3-23/T2-12. Trial 07 is not sufficient coverage for this gap: admission-vectors.json explicitly exempts DISPATCH-STAGE-CORRELATION, TS2-STAGE-PROJECTION and RUST3-PLAN-STAGE-BYTES as inherited M2 duties.

Required change: Assign D2b-3/-4 the retained per-frame contextual admission, with a supplied immutable dispatch/request context and live per-direction/per-stage counters. Explicitly place the retained prechecks and payload guards before matching, apply the applicable carrier admission joins and owner semantics without performing H fact admission, and preserve typed failure before publication. Add integration controls for wrong current stage/Analyze ordinal, duplicate or skipped batch/candidate ordinals, and retained Plan-stage byte equality; do not treat replay of the scoped corpus as proof of these exempt obligations.

### D2BPLAN-R1-RF-3: Plan successor-aware codec behavior and new controls beyond materialization

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:55`.

FA-2 and RUST3-LIM are assigned schema materialization in D2b-0, but D2b-3/-4 are described only as the codecs with T4/T5. Their normative wire duties and successor-specific controls are not stated. X-FA2-D requires the token-gated Analyze/Complete versions, Analyze census request and D-empty request commitments from the Plan, wire refusals/bounds, and deferral of the symbol-key wrapper commitment check to H at settlement. X-RL-D requires StageRequestV3 and host-constructed RustSubjectScopeV1 under its token, mismatch refusal and the retained token-absent inline path. Trial 07 carriers contain neither symbol-census-v1 nor subject-scope-reference-v1, so its 353 admission vectors cannot establish these new branches.

Required change: Add an explicit allocation of X-FA2-D and X-RL-D behavior to D2b-3/-4 and the C4/H interfaces. Cover the independent negotiated token combinations, both token/shape mismatch directions, old no-token payloads, FA-2 complete/over-bound census handling and its typed scope-limit handoff without manufacturing a provider fault, D-empty versus returned census commitments with the H settlement boundary, and reference-scope count/commitment reconstruction. Pin and adapt the successors own vectors alongside trial 07, retaining historical controls rather than treating historical replay as complete successor conformance.

## Decisions and reviewer questions

**Q1 / LD-D2B-1:** The five-way split and stated order are reasonable. `discovery_census.py` includes `tools/contracts/generator-closure.json` in `REFERENCE_PRODUCT`, so materialization that changes the closure invalidates the current blind receipt. The immediate pre-run review, mechanical blind refresh and post-run review before other census-dependent lanes correctly handle that dependency. Acceptance of this plan would not itself accept the future materialization or receipt.

**Q2 / LD-D2B-11:** Exporting an NFC predicate from identity is appropriate. Identity already owns the pinned `unicode-normalization =0.1.24` dependency, and components permits identity/contracts edges. This avoids adding a new normalization owner or dependency. Pin the actual reference Unicode database version as well as comparing vector results: finite text vectors alone do not establish a Unicode-version pin. No normalization or silent repair of wire text is allowed.

**Q3 / LD-D2B-2 and LD-D2B-8:** A depth bound derived from the complete closed wire schema graph is reasonable, subject to NBO-1. Leaving TS2's absent aggregate response limit explicit is correct; do not import Rust3 totals or invent a TS2 protocol fault. Rust3's frame, aggregate, candidate-count and full spool-entry bounds retain their separate checked-accounting duties.

**LD-D2B-3:** Requires RF-1's correction. Received bytes are authoritative for wire commitments; the spool is a different, constructed accounting record.

**LD-D2B-4:** Byte-vendored tables and overlay, declared match order, pre-match law, state updates, stage-dependent transitions and total fallback are the right approach. They do not replace the retained contextual frame admission in RF-2. The five P3 overlay vectors are present in trial 07.

**LD-D2B-5 and LD-D2B-6:** Phase-selected TS2 Unavailable agrees with the carrier's documented outcome-equivalent precheck, with the trace difference stated. The explicit ZeroExit/Eof/process-fault input preserves the named D3 observation boundary and does not authorize reordering frames.

**LD-D2B-7:** The protocol distinctions match T2O, P3T and the Rust overlay; distinguish table capability from sender permission as NBO-2 explains.

**LD-D2B-9:** Exact schedule consumption and send-side rechecks are appropriate. C4 owns pre-spawn planning/refusal; its integration must supply the immutable schedule consumed by D2b, not merely a measured inline Analyze size. The cited schedule binds the entire canonical send sequence, chunk coordinates, payloads, digests and reserved Cancel.

**LD-D2B-10:** Using `encode_cve1` for Rust anchor ordering is appropriate. It does not make CVE1 a CBOR decoder. TS2 keeps its distinct CBOR-byte anchor order.

**LD-D2B-12:** Framing length, digest, strict decoding, envelope and negotiated shape checks are sound in principle; RF-2 supplies the missing contextual admission before table matching. Zero-length CBOR input is TRUNCATED in the retained decoder.

**LD-D2B-13:** Rebasing the FA-2/RUST3-LIM schema materialization onto RCA-1's current handshake is appropriate. Preserve RCA-1 and independently review every materialization difference, registry/source-map/admission update and regenerated carrier; the old after-hashes are not a replacement for that review.

**LD-D2B-14:** Trial 07 is the correct retained scoped reference. Its admission file contains 353 cases grouped under 31 rules; decoder probes are separate. It explicitly exempts several inherited duties and its carriers contain neither new successor token. Preserve its historical scope and add RF-2/RF-3 controls rather than claiming full codec conformance from this replay alone.

## Fidelity and boundaries

The proposed 40-byte framing, 67,108,864-byte pre-allocation payload bound, checked arithmetic, separate TS2/Rust3 CBOR profiles, construction-time dispatch, hand-written conversion to carriers, data-driven tables, exact identity/limits echoes and reject-before-disclosure are consistent with M3-D items 10 and 11 in principle. The plan keeps fact admission, Coverage minting and supervisor implementation with their owners. Separate codecs and the absence of a shared semantic frame type are appropriate. Canonical re-encoding is a validation comparison, not permission to rewrite forwarded bytes; the later D5 hostile dual-channel controls still owe byte-for-byte preservation, including late frames and split input.

The required findings concern concrete preimage correctness and obligations missing from the implementation/control allocation. They do not request a common semantic type, new protocol limits, a new terminal or any qualification claim.

## Nonblocking observations

### D2BPLAN-R1-NBO-1: Define the depth computation over the complete successor-aware wire closure

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:65`.

The schema-derived bound is a reasonable answer to Q3, provided it includes inherited carrier records, transitive external schema references, negotiated variants and the two successor schemas, rather than just the three named source schemas. D2b-1 precedes D2b-0, so state when its computed constant is updated and rechecked after materialization. Distinguish container depth from byte-string contents; the embedded relation-payload CBOR reader needs its own applicable schema-depth check. Add a deepest-valid case and a one-level-over refusal.

### D2BPLAN-R1-NBO-2: Distinguish abstract TS2 Cancel permission from the selected host send schedule

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:74`.

T2O permits Cancel in START and the TS2 payload admits host-shutdown. However, the cited carrier HOST-SEND-SCHEDULE is marked appliesTo=both and states after-Hello, exact echo, user-interrupt only. Keep those table/payload capabilities distinct from what the host sender may actually emit under LD-D2B-9; D3 choosing a reason must also respect the consumed schedule. Any intended widening needs the relevant owner decision, rather than silently weakening the sender contract.

### D2BPLAN-R1-NBO-3: Use an observable control for received-byte provenance

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r1.md:122`.

For canonically validated input, re-encoding the same value produces identical bytes by construction. A mutant that merely swaps received sub-slices for that equivalent re-encoding cannot be killed by digest-result assertions alone. State the instrumentation or structural verification that observes the actual input provenance; retain separate black-box mutants for wrong wrapper, order, domain or value class.

## Review method

Read and compared the plan with M3-D r5 items 10–11, NE section 9, DLV/RPP, P3T/overlay/T2O, product source schemas and wire carriers, FA-2/RUST3-LIM materialization maps and implementing-owner obligations, trial 07 data/reference source, package dependencies and the census reference binding. Used only read-only inspection, JSON parsing, hashing and Git queries. No build, test, generator, lane, network or delegation was used. No private fixture, installation, signing key, held-out store or T2 cache was accessed. Only the two requested review files were written; neither repository was edited.

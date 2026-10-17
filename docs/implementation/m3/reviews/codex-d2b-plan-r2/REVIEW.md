# D2B-PLAN-r2 review

Verdict: **REQUIRED-FINDINGS** — two required corrections to the new controls; two nonblocking observations.

The three round-1 required findings are addressed in substance. The remaining corrections preserve the protocol's exact-echo handshake and make the new controls agree with the plan's own schema/admission/builder boundaries.

## Subject verification

Verified the 566-byte manifest SHA-256 `8ace57e56ef41b62aeb7d37af1fec25ebe4d424b40f449f4b64aaf088209b40b` and both members:

- PLAN-r2.md: 37,546 bytes; SHA-256 `86431605d32213a2b86788d01c806613973321edede141e6167c0f0ac4ad3f79`.
- Historical PLAN-r1.md: 11,905 bytes; SHA-256 `35a2da79401936e7ef06700f9318a8dbb3ec8e9b3caed4aa4383f264e44c2801`, unchanged from round 1.

Architecture HEAD is the requested `2894884ef33b0434a7c09029d2f727cf5f7a2524`; product HEAD is `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`.

## Required findings

### D2BPLAN-R2-RF-1: An omitted capability echo faults; it cannot negotiate the token off

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r2.md:224`.

The FA-2 controls require a case with the census token offered without its HelloAck echo and label that outcome negotiated off. NE section 9.1 requires exact token-array equality in both protocols, and FA-2 retains that handshake. A Hello containing symbol-census-v1 followed by a HelloAck omitting it must fault before any OpenUniverse/source disclosure. Accepting the exchange and switching to historical payloads would silently weaken the signed selection and contradict the unchanged exact-echo rule.

Required change: Replace the negotiated-off outcome with PROVIDER.PROTOCOL_VIOLATION before disclosure, for TS2 and Rust3. Keep the lawful token-absent historical branch only when both exact arrays omit the token. Make explicit that all optional tokens retain exact echo, including the Rust reference-scope token; test both omission and unoffered addition without continuing the session.

### D2BPLAN-R2-RF-2: Give each new control the refusal point assigned by the plan

Location: `docs/implementation/m3/supervisor-d/d2b/PLAN-r2.md:222`.

Section 4 says every RF-2 control passes the closed schema and refuses at contextual admission. That cannot hold for all the listed controls. Every TS2/Rust3 FactBatch carrier, historical and V3, declares 1..4096 facts/candidates: zero or 4097 entries fails the closed payload schema at LD-D2B-12 step 8, before admission step 9. In addition, planStage byte equality and request stageOrdinal construction are assigned to the host builder by section 3, rather than to received-worker-frame admission. The blanket expected phase conflicts with the revised check order and the otherwise sound ownership table.

Required change: Partition these controls by owner and refusal point: shape/count-bound violations at schema admission, host request projection/Plan-stage mismatches in the builder or sender before writing, and well-shaped worker stage/Analyze/batch/candidate correlation and T020 mismatches at contextual admission. Keep the before-publication guarantee. Do not bypass earlier schema checks or move host checks into worker admission merely to satisfy the current test wording.

## Round-1 findings and reviewer questions

**RF-1 / Q1: representations and accounting.** LD-D2B-3 now separates received commitment preimages, a constructed spool entry, and the candidate-only byte-equality assertion. Each commitment field follows commitmentMap's domain and value class, including post-Analyze Unavailable/BudgetExhausted coverage-stream rows. Fact and CoverageResultV3 encodings remain distinct; array heads are generated from the counts while elements preserve received encodings and order.

The spool uses the full deterministic-CBOR map `{analysisOrdinal, stageId, candidate}`. Full wrapper bytes and the running candidate-count bound are checked before allocation/append, with checked arithmetic and whole-Analyze refusal. This follows RPP's candidateSpoolAccounting; it does not charge only a candidate slice or re-read the source. The planned full-wrapper, count/spool boundary and wrong-domain/value-class/order controls address the earlier gap.

The reader-only ReceivedBytes constructor, borrowing from retained payload storage, and pointer-range provenance assertion are a reasonable observable for the proposed re-encoding mutant. Implementation review must also verify lifetimes/backing storage and that the actual hashing path consumes those views. The assertion is a structural control, not a proof that arbitrary future code is trustworthy.

**RF-2 / Q2: contextual admission and ownership.** LD-D2B-15 adds the immutable dispatch/request context, live direction/stage counters, retained framePrecheck/T016/T020 checks and wire joins before table matching. The new stage, Analyze ordinal, batch/candidate counter and budget controls cover duties explicitly exempted from trial 07. RF-2 above corrects their claimed test phase; the contextual checks themselves are appropriately assigned.

Independently compared section 3 with the product carrier admission list: all 55 IDs appear exactly once, with no missing or duplicate IDs. Host payload construction, schedule sizing and sending belong to D2b's builders/senders; C4 invokes them at the specified Plan-time boundary and owns pre-spawn selection/refusal. Dependency/prepared set admissions remain with their owners. D4 supplies the admitted context; D3 supplies process observations.

FP-CANDIDATE's wire coordinates/correlations and strict RELATION-PAYLOAD-CBOR decoding appropriately belong to D2b. This does not mint fact2 or replace H's registered relation/rung validation, retained restrictions, snapshot joins and conversion to foundation C. M3-H r3 item 6 explicitly separates D2b's CBOR decoding from H's registered-selector validation and C encoding. Preserve a decoded-value handoff so H does not need a second CBOR decoder. H's retained payload/record validation remains authoritative; the generic wire event grants no fact authority.

**RF-3 / Q3: successor duties.** LD-D2B-16 now covers FA-2's negotiated Analyze/Complete versions, owed/null census request, D-empty commitments, complete/over-bound returns, terminal behavior and typed handoff. Symbol-key commitments depending on the final census are deferred to H at clean settlement, rather than being rejected early against the request key. Census over-bound and projected-record/descriptor overflow retain the subject-scope owner's scope-limit route; they do not manufacture a provider fault. Full locator/state/extent admission remains with the enumeration owner at H settlement; the wire row-path membership check is distinct from that full extent equality.

LD-D2B-17 covers every negotiated Rust StageRequestV3, all three independent token combinations, both token/shape mismatch directions, the host's rebuilt subject count/commitments, the historical inline path and worker input-rejected observations. The full-envelope schedule bound is necessary on that inline path as NBO-1 explains. Missing signed capability for a Plan that needs it remains C4's capability-missing/no-spawn decision, not a codec-chosen fallback.

The successors' own vectors are now pinned and replayed alongside the explicitly historical trial-07 corpus. This addresses the original absence of successor-specific behavior and controls. RF-1 above fixes the new handshake-control regression.

## Prior observations and unchanged decisions

The depth bound now covers the whole successor-aware wire closure, is computed after D2b-0, is passed into D2b-1's iterative reader, and has deepest-valid/one-over controls. Embedded relation CBOR gets its own bound; byte strings do not add outer container depth.

Read-side abstract Cancel capability is explicitly separated from sender permission. Both host senders follow the selected HOST-SEND-SCHEDULE: one after-Hello Cancel, exact correlation echo, user-interrupt only. TS2 table capability does not widen that schedule. This resolves the prior Cancel observation.

Unicode versions are now separately pinned. The locally available unicode-normalization 0.1.24 tables declare `(16, 0, 0)`; querying the declared Python 3.14.6 reference interpreter reports unicodedata version `16.0.0`. Vector agreement remains an additional control, with no normalization/repair fallback. Exporting the predicate/version from identity stays within the permitted dependency ownership.

The five-subunit order and immediate reviewed blind refresh after schema materialization remain sound. The unchanged generator closure is a census reference input, so the planned materialization/refresh sequence must remain contiguous before other census-dependent lanes.

No regression was found in byte-vendored tables/overlay, phase-selected TS2 Unavailable, D3 process-event ownership, leaving TS2's missing aggregate response bound explicit, protocol-specific anchor ordering, RCA-1-based materialization review, or trial 07's bounded historical scope. These remain plan commitments; no future materialization, implementation, blind receipt or qualification is accepted by this review.

## Nonblocking observations

**D2BPLAN-R2-NBO-1 — Attribute the inline Analyze frame-size gap to schedule sizing** (`docs/implementation/m3/supervisor-d/d2b/PLAN-r2.md:148`). The statement that refusing more than 256 inline subjects closes RUST3-LIM F-1 is imprecise. F-1 is an oversized inline Analyze even at or below the subject cap, due to repeated rows, stages and path lengths. LD-D2B-9 already supplies the correct full-envelope sizing and pre-spawn schedule refusal. Cite that mechanism here and include an at-or-below-256 oversized-inline control, distinct from the 257-subject cap case.

**D2BPLAN-R2-NBO-2 — Name the occupancy and transitive schema consumers in the pattern allocation** (`docs/implementation/m3/supervisor-d/d2b/PLAN-r2.md:174`). OWNER-PATTERN-EVALUATION explicitly scopes the occupancy-companion schema in the wire consumer as well as evidence/startup and the H relation-payload consumer. The table currently names D2b startup checks, H relation payloads and the Plan evidence schema. State that D2b applies the selected pattern semantics to its occupancy companion and transitive external wire schemas too; listing the carrier admission ID once should not be mistaken for covering only the startup root.

## Boundaries

Used read-only inspection, hashing, JSON parsing, Git queries and a read-only Unicode-version query of the declared reference interpreter. No architecture semantic reference, product build/test/generator or lane was run. No repository, worktree or control file was edited. No network, other pane, delegation, installation, private 413 fixture, signing key, held tree, T2 store or cache was used. Only the two requested review files were written.

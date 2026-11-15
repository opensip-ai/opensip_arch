# ERRATUM C8-ASSEMBLY-LEDGER-E1 r5: what pays for the Run's assembly between Plan admission and the mint (erratum to M3-C r8/r9 item 2 "Ledger" and to the J3d-TS composition's builder, seam 3.26)

**Status: PROPOSED (r5).** Not law until both reviewers (Codex, Claude) accept it at the same hash. Author: Claude
claude-opus-5-5/medium, U4 C8-LEDGER-1's worker, for the lead, R2-DEEP (preflight: `ROUTE-OK R2-DEEP claude
claude-opus-5-5/medium`). Written under lead decision A (`LC/stack-fix-1/LEAD-DECISIONS.md`:6-32) as corrected, with
rulings E-1 to E-8 (:160-197) and E-9 (:240-246), and the lead's r3 ruling (every required finding of both U4E verdicts
upheld), on `LC/stack-fix-1/PLAN.md` section 3A. It answers Codex C8-CX-R1 (`stack-review/packets/codex-C-c8/VERDICT.md`:12-24),
Claude C8 RF-4 and RF-5 (`stack-review/packets/claude-B-c8/VERDICT.md`:72-97) and Codex B's Q67 advisory
(`packets/codex-B-j3d/VERDICT.md`:89). Code references are to `opensip-stack-all` at `3363fa39` (`crates/host/src/`
unless named otherwise); ARCH at `6014f8bd`. r1 (sha256 `091a3c69…`), r2 (sha256 `81907111…`), r3 (sha256 `e5e5a398…`) and r4 (sha256 `b7ff5243…`) are left untouched.

**Changes from r4 (by the lead, from the two r4 verdicts, `stack-review/packets/{claude,codex}-U4E/VERDICT-r4.md`;
nothing else differs):** (1) Codex U4E-r4-R1: basis (1) for the planned-program count P requires an INJECTION from
the distinct planned programs into distinct stages, not only that every program has some stage; (2) Codex
U4E-r4-R2: the provider-returns paragraph no longer asserts a one-frame overshoot (a step may complete several
frames) and rests on the exclusion of a breached session's returns; basis (3) says what makes it a number (Claude
A-R4-1; Codex section 3(b)); (3) Claude RF-R4-1 and Codex section 3(c): statement 6 names the ADOPTED successor
law, M4-LAW-RECORD-r2, with its retained conditions, and cites the accepted plan only for the definitions of
*T*sound and *L*max; the r4 note that called the plan "the adopted snapshot law revision" was wrong and is
corrected below.

**Changes from r3 (by the lead, Claude Fable 5.2; nothing else differs):** (a) the pre-check's two keys take the
composition's existing prefix, `j3d-ts.assembly-precheck:capture-entries` and `j3d-ts.assembly-precheck:retained-bytes`,
and are confirmed; (b) r3's Open 2 (no located cap on the planned-program count P) becomes a third check the
implementing unit must make before the join's limit is set, in a stated order of bases (lead ruling E-10), and is
removed from Open; (c) r3's Open 3 is closed: the premise names Codex U4E-R3 used are defined in the accepted
plan `ARCH/docs/implementation/m3/snapshot-plan-c/c2b/law-revision-r4/PLAN.md`:36-63 (an accepted PLAN, not law;
the adopted successor is M4-LAW-RECORD-r2: see "Changes from r4"), and statement 6 names them.

**Changes from r2 (by the lead's r3 ruling on the U4E verdicts, `stack-review/packets/{claude,codex}-U4E/VERDICT.md`;
nothing else differs):** (i) statement 1 says no ledger is opened for the reread or the seeding and that the Plan
ledger, itself on the snapshot profile's limits, pays none of statements 1-3 (Claude RF-5; Codex section 2); (ii)
statement 2's opening no longer says the pre-check "changes no outcome": it says which outcomes change and that
passing it is not replay admission (Claude RF-1; Codex section 3); the proof gains its two missing links, the seal
encoding the descriptor from the session's rows and fact admission discarding only what it inserted (RF-2); the
entries comparison is said to be unable to fire on a sealed capture and is kept as a defence (RF-3); the refusal
carries a key into the operational record, and MJ row 36 and X5's structural row are listed as amended (RF-4); the
pass is prepaid from `capture_count()` and itemized, once, before `produce` (A-3, A-7); its order against cancellation
is stated (A-8); (iii) statement 3 covers the producer's remaining work and states an auditable charge contract: a
written itemization in all three dimensions, the three seeding phases by name, prices from the lent lengths, probes
that validate and do not prove (Codex U4E-R1; Claude RF-6); (iv) statement 4 corrects the universes and config graphs
to the planned-program count, writes ruling E-9 in with Claude's four corrections, replaces the common "one visit, no
copy, linear" claim with each phase's true bound, computes the join's limit from the enforcing constants, and cites
the accepted schema selectors (Claude RF-7, A-9, A-10, A-1, A-2; Codex U4E-R2 and section 5); (v) statement 6 makes a
lawful repository that would end on row 21 a host defect under LD-DEC-5 items 1, 4 and 8, with the census as the
sizing check owed before command-line wiring, and lists M3C:261's census obligation as deferred with that gate (Claude
RF-8; Codex U4E-R3; A-4); (vi) statement 7 gains the cumulative-scope, independently observed coverage and scoped
boundary controls, and the reviewers' replacement controls (Codex U4E-R4; Claude RF-1, RF-2, RF-3, RF-6, A-6, Q7);
(vii) statement 5 says reuse keeps the binding of digest to retained bytes (Codex section 9); (viii) Open 2 is
replaced (E-9 is written in), and a new Open 2 names the planned-program count, for which no cap enforced before the
join was located (E-4, E-5); R-2 gains A-12's note. The advisories not applied are listed at the end.

**What it amends (the files are not edited):**
- M3-C (`ARCH/docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, = **M3C**; r8 with the r9 note, M3C:5), item 2
  "Ledger" (M3C:251-261), which names only the walk. This adds the producer's work, the reread and the seeding to the
  same ledger.
- M3C:261's census obligation is **deferred, not removed**, as statement 6 says; its gate is LD-DEC-5 item 8 (before
  analysis is wired to the command line).
- MJ row 36 (`host-pipeline-j/PROPOSAL.md`:808) and X5 item 5's structural row (X5 `PROPOSAL.md`:79) are also taken
  by statement 2's host pre-check, which is not a replay refusal.
- The J3d-TS composition's interim Q67 arrangement ("C8 opens its own snapshot-profile ledger for `produce`",
  `LC/j3d-ts/QUESTIONS.md`:1193), which is withdrawn.

## Old

M3C:251: "The walk is charged to one **snapshot ledger** per invocation. It is created after discovery and never
recreated after a failure". M3C:256: "every copy, metadata sample and ACL capture is charged under its existing owner's
pricing;". The platform owner: "the one snapshot ledger an invocation creates, once, after discovery. ... a failed
snapshot ledger is never replaced, and exhaustion is never truncation." (`crates/platform/src/work_ledger.rs`:272-276).
No adopted sentence assigns or exempts the assembly's cost (PLAN.md:243-245). At `3363fa39`: `produce` runs on a second,
fresh snapshot-profile ledger (`durable_run.rs`:178-179) beside the capture's (:527); the producer parses, indexes and
copies outside any seeding entry point (`fact_admission/inventory_inputs.rs`:102-105, :143-227, :230-235); the seeding
takes no ledger (`run_custody.rs`:107, :242, :415) and copies, re-hashes and parses input-sized records (:51-53,
:200-202, :163, :252, :426, :399, :453-456); and both retained size limits are checked only at replay
(`finalization.rs`:546), after the repository has been held in memory twice (`inventory_inputs.rs`:168;
`run_custody.rs`:200-201).

## New

1. **One snapshot ledger for the snapshot work.** Capture, the inventory-inputs producer and custody assembly share the
   invocation's one snapshot ledger, the ledger the capture was charged on (`durable_run.rs`:527, lent as
   `Ledgers.snapshot`, `analysis/compose.rs`:424), preserving its cumulative usage and failure latch. The producer's
   sealed reads (`inventory_inputs.rs`:106-115) are charged on it before each read. No ledger is opened for the reread
   or the seeding: `produce`'s own ledger (`durable_run.rs`:179) is removed, and the invocation keeps exactly the
   discovery, snapshot and Plan ledgers it opens today (`durable_run.rs`:526, :527, :542). The Plan ledger, though
   built on the snapshot profile's limits (`PlanLedger::profile`, `plan_ts2.rs`:3619-3624; ruling R-20, "the Plan's work
   scope borrows the snapshot's profile", :3609), is a separate, Plan-owned scope, unchanged, and pays none of
   statements 1-3; equal profiles do not identify those scopes. The sealed source borrows the snapshot ledger
   (`analysis/source.rs`:103-107 owns one today). A refusal latches it.
2. **The size pre-check, once, before `produce`.** It never refuses a Run that replay would admit, so it prevents no
   commit: E and B below are lower bounds of what replay counts, so an E or B over its limit makes replay admission
   impossible for a candidate holding these sealed blobs. A Run it refuses ends on the row replay's own size refusal
   takes. The only outcomes it changes are those of Runs that are over a retained limit and that, without it, would
   have ended on another row before replay (an earlier refusal or an interruption); such a Run now ends on this row
   instead. Passing it is not replay admission (closure trees, objects and other bytes can still cross a limit later),
   and this is not a claim that an otherwise malformed candidate would have the same first replay diagnostic. A
   refusal of the funding of its own pass is separate and takes row 21. It runs inside `with_after_plan`, before
   `produce` (`durable_run.rs`:175-179); no cancellation probe runs between the Plan's return and that point today
   (`analysis/compose.rs`:441-450), and this erratum adds none.
   From the sealed session's inventory only (`session.inventory()`, each capture's `sha256` and `bytes`, as
   `analysis/source.rs`:90-92 reads them; no content read), it computes over the rows' DISTINCT digests:
   - **E**, the number of distinct digests, compared with X5's "100 000 capture entries"
     (`ARCH/docs/implementation/m2/replay-join-x5/PROPOSAL.md`:133; `REPLAY_LIMITS.capture_entries`,
     `fact_admission.rs`:56). *Lower bound:* the session's rows are the descriptor's (sealing encodes `sourceInventory`
     from `session.inventory()`, row for row, `snapshot_seal.rs`:563-567, on a sealed session); every sealed row is read
     and its blob kept (`inventory_inputs.rs`:150-169; the rows are exactly the sealed inventory, :171-173); every kept
     blob enters the custody keyed by digest (`run_custody.rs`:200-202); the custody is handed on
     (`durable_run.rs`:198); until the join only fact admission writes into it, inserting only into vacant entries and
     discarding only entries it inserted (`fact_admission/candidates.rs`:758-763, :852-860, :266-273;
     `fact_admission/views.rs`:167-178, :181-188; `execution_capture.rs`:271, :297-300, :1086-1090, :1095-1105), so no
     seeded blob leaves it; the join only adds (`durable_run.rs`:707-729), and the candidate is the joined maps
     (:691-696); replay counts all the candidate's objects plus blobs (identity `closure.rs`:1519-1523 via evaluator
     `replay.rs`:175 and `fact_admission.rs`:109). So E never exceeds what replay counts. On a sealed capture E cannot
     exceed the limit (the seal's row bound, `snapshot_seal.rs`:45, :519, equals it); the comparison is kept as a
     defence.
   - **B**, the sum of `bytes` over the distinct digests, compared with "268 435 456 retained bytes (256 MiB)" (erratum
     X5-E1 Part A, `ARCH/docs/implementation/m3/errata-2026-11-13/ERRATUM-X5-E1.md`:36, adopted by `ADOPTION-X5-E1.md`;
     `REPLAY_LIMITS.retained_bytes`, `fact_admission.rs`:57). *Lower bound:* replay counts the bytes of every blob it
     READ, once per digest (identity `closure.rs`:1533-1537, :1581-1590, via `replay.rs`:275), and it reads every
     source blob: replay's walk runs on the capturing inputs (`replay.rs`:175-177; evaluator `full_walk.rs`:300-301),
     starts at the Run (`closure.rs`:649), follows the Run's `snapshotId` (schema `"pattern": "^snapshot2:..."`,
     `schemas/sources/identity-v3.schema.json`:1494-1497; `closure.rs`:819-823), walks every item of
     `sourceInventory` (schema :215, :2822-2828; `closure.rs`:827-837), and each item's `sha256` is a `raw-artifact`
     digest with the default `preimage` retention (schema :154-160; `closure.rs`:884-888, :900-903), so `blob` is
     called (:681-683), which marks it read (:102-110). A replay that does not finish this walk refuses. The
     descriptor's rows are the session's (`snapshot_seal.rs`:563-567, as above), and each row's `bytes` equals its
     blob's length (checked at `inventory_inputs.rs`:164). So B never exceeds what replay counts. B is the control that
     distinguishes distinct from raw totals: a raw byte sum over duplicate contents would refuse Runs replay admits.
   - The fixed parts (closure trees, Plan and seal records, object frames) are left out of both sums; leaving them
     out keeps each bound sound.

   If E or B exceeds its limit (`>`, as `with_read_capture` and the byte total do), the Run ends before anything is
   read or allocated for the producer, the reread or the seeding, on the row replay's refusal takes today (E-1):
   `Capture(Limit)`, X5 item 5's structural row, operational-failed, exit 4, `PROVIDER.PROTOCOL_VIOLATION`,
   `provider-protocol`, detail `EVALUATION.INPUT_REFUSED` (X5 `PROPOSAL.md`:79, :87: "the same row `Structure(Limit)`
   and `Capture(Limit)` already take"; MJ row 36, `host-pipeline-j/PROPOSAL.md`:808; "The existing route stays: a
   replay cap crossing takes the structural row", `ADOPTION-X5-E1.md`:9). Its observation carries the key
   `j3d-ts.assembly-precheck:capture-entries` or `j3d-ts.assembly-precheck:retained-bytes` into the operational record (U3b
   ruling 4(a): "the observations of rows 21, 22, 29 and 36 carry the child's refusal key into the operational
   record.", `LC/stack-fix-1/LEAD-DECISIONS.md`:116), with E or B and the limit, as X5:79's "with the exact diagnostic
   retained separately"; no subject.

   **The pass is charged** (E-3): on the snapshot ledger, prepaid before the pass from `session.capture_count()`
   (O(1); "How many captures the session holds, reached or not", `snapshot.rs`:929-932), an upper bound on the rows,
   because `inventory()` filters `origin.is_some()` over every capture (`snapshot.rs`:1135-1139). The price covers one
   visit per capture (the seal prices this pass as `capture_pass_cost(session.capture_count())`,
   `snapshot_seal.rs`:426, :450), one distinct-set insert per row (a keyed search over at most `capture_count`
   32-byte keys plus one node allocation, worst case, without first finding the distinct count), checked addition for
   B, and the set's destruction; all of it is charged before `SealedRows::of` (`inventory_inputs.rs`:106-108), with
   checked arithmetic, and the function is published with its itemization (statement 3's form). This is flags ruling
   F-1 ("The map's iteration is prepaid from its length ... No price may be paid from a later charge.",
   `LC/j3d-ts/discovery-flags/RULINGS-STACK-FIX-1.md`:17-20). Its exhaustion is statement 3's row 21.
3. **The producer's and the seeding's work is paid by precharge on the same ledger.** All remaining
   composition-owned preparation and custody-construction work before fact admission is funded on statement 1's
   snapshot ledger. This includes `ProducedInventoryInputs` construction and extent preparation (the snapshot and
   enumeration-plan parses, `inventory_inputs.rs`:102-105; the row loop's index, path and row-value copies and
   digest checks, :143-169; the stage-map check and extent derivation, :174-216; the accessor's recomputation of the
   extent, :230-235, called at `durable_run.rs`:199), every remaining parse, validation or hash, row/path/value copy,
   index/set/vector operation, canonicalization, closure check and custody insertion, and the three seeding phases,
   `seed_run_custody`, `seed_caller_records` and `seed_closures` (`run_custody.rs`:107, :242, :415). Avoidable work is
   removed first (statement 5). Reads and other operations already funded by their owners (the sealed reads, charged
   by `SealedSource`, `analysis/source.rs`:184; `SealedRows::of`'s own charges, :83-93) are identified, so that coverage
   is complete and is not inferred from being inside a scope.
   - **The charge contract.** Each phase (the producer's preparation, and each seeding phase) is charged once, before
     it runs, by a reviewed `WorkCost` function over quantities the host holds before that phase: lengths held in
     O(1), or totals from a pass itself prepaid as statement 2's is (a closure's tree lengths). The price is taken from
     the LENT lengths, duplicates included: `records.tree` may be longer than the descriptor's `tree`, because the
     comparison dedups only for itself (`run_custody.rs`:399-408) and every lent entry is then copied (:454-456). It
     is a source-derived upper bound, in each of the ledger's three dimensions (objects, edges, bytes), over all
     admissible inputs of the pinned implementation (the lent records included, at their lent lengths), its worst-case
     comparisons and growth, its failures and the destruction of what it built included, written as a numbered
     itemization beside the price as `discover_units_cost`'s is ("Each term is a row of the itemization (`price`
     module, rows `D1`..`D18`)", `discovery.rs`:2199-2200), under the existing owners' pricing (no new uncalibrated
     scalar replaces owned-record allocation and operation prices). The implementing unit publishes each phase's exact
     boundaries, size inputs, checked arithmetic and per-dimension derivation. Adversarial allocation and work probes
     VALIDATE it (`discovery_price_tests.rs`:1-11); passing probes alone is not its proof, and what the probes cannot
     observe rests on the itemization ("Edges are not observable here (no counting hook for comparisons or visits):
     they rest on the derivation.", :10-11). This is E1a 3.6's form: "a closed function of quantities known before the
     work" and "An unmetered precharge has a source-derived bound over all admissible inputs of the pinned
     implementation; adversarial allocation probes validate it, including failures and destruction."
     (`ARCH/docs/implementation/m3/errata-2026-11-14c/ERRATUM-DISCOVERY-FLAGS-E1a.md`:361, :364-366).
   - The charge precedes the first covered operation; its failure is the typed, latching ledger failure, and nothing
     unfunded continues after it.
   - *Why a precharge and not per-step pricing* (decision A point 4): this copying is what the by-reference custody of
     the scale direction (LD-DEC-15) is expected to remove, so the simplest sound charge is the right investment.
   - Exhaustion is MJ row 21: "Discovery or snapshot ledger exhausted | operational-failed / 4 |
     `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED`" (`host-pipeline-j/PROPOSAL.md`:793).
4. **After the mint: charged to no ledger, bounded by caps enforced before it.** The join (`durable_run.rs`:702-730), the
   attempt progress (`analysis/compose.rs`:258-299, :307-342) and the derivation vectors (:633-639) are charged to no
   ledger, as replay is (X5 `PROPOSAL.md`:69: "Replay is bounded by `ReplayLimits` ... Replay is not charged to X1's
   attempt ledger"; in code, "replay is charged to no ledger", `fact_admission.rs`:35-36), as fact admission is ("They
   are charged to no operation ledger: replay's precedent (X5:45).", M3-H `fact-admission-h/PROPOSAL.md`:753) and as
   derivation is proposed to be ("In memory, charged to no ledger, like replay", `host-pipeline-j/j3d-delivery-r1/README.md`:67;
   D1 is PROPOSED and is cited for its form only). Each phase states its work and peak live storage in terms of a
   population derived from caps enforced before the phase ((g1)'s statement of work and storage, README:79-81, with
   the upstream caps of decision A point 5, `LEAD-DECISIONS.md`:25-28, in place of (g1)'s local limits where they
   suffice). The bounds differ by phase; no common "one visit, no copy, linear" claim is made:
   - *Attempt progress.* Population: the Plan's stages S, "`exec-plan2`, at most **1024 stages**" (WS,
     `ARCH/docs/v2/contracts/product-v1/workflows-and-surfaces.md`:87-88), enforced at Plan admission
     (`crates/plan-priced/src/plan_stages.rs`:18; refused at `plan.rs`:574). Every event must be a Plan stage (:267,
     :284) and a repeat refuses (:270, :287), so there are at most S + 1 event checks; each scans a Plan stage list
     (`provider_stages` is a vector, `contains`, :267; `inventory_stages.iter().any`, :284) of at most S entries, plus
     bounded set operations: O(S^2) work, O(S) storage. No local limit is needed beyond S's cap.
   - *Derivation vectors.* O(S) bounded copies of the Plan's stage maps (:637-638), O(S) storage.
   - *The join.* For J minted entries and C entries already in the custody, it performs keyed lookups and inserts in
     maps of size at most C + J, compares a held value against at most the minted value of the same key, then moves
     the minted value in (:711-728). Its population is the following parts, each capped before the join:
     - **C1 source blobs:** at most 100,000 ("**rows:** more than 100,000 inventory rows", M3C:351), enforced at the seal
       (`snapshot_seal.rs`:519); distinct digests are at most rows.
     - **C2 Plan and seal records:** a fixed set of 16 (13 in `seed_run_custody`, 3 in `seed_caller_records`,
       `run_custody.rs`:120-219, :242-282); stage specs at most 1,024 (as above; the zip is length-checked at
       `run_custody.rs`:147); native context frames at most 128 distinct ("`nativeContextDigests` (128)", M3C:1058;
       counted distinct at `plan_sets.rs`:26-39), the inserted frames' set being required to equal
       `nativeContextDigests` (`run_custody.rs`:318-323); schemas at most 128 (`#/$defs/analysis-spec/properties/parameters`,
       `"maxItems": 128`, `ARCH/docs/coop/design-corrections/foundation/identity-schemas.v3.json`:2195-2198; enforced at
       `plan_spec.rs`:18). **Universes and config graphs:** the inserted ones are the distinct `universe` digests the
       enumeration plan's bindings name (`run_custody.rs`:329-343), found in vectors of "One entry per planned program
       ... Two programs that minted one context lend that frame twice (identical bytes)." (`plan_ts2.rs`:2941-2945;
       pushed once per retained program, :3019-3021). Their count is therefore at most the planned-program count P,
       not 128: index alignment (`run_custody.rs`:307-309) equates three vector lengths only, and the 128 cap is on
       distinct contexts. Raw native-vector processing (one frame copy per program, :322-323; a linear `position`
       search per bound universe, :341) is O(P) copies and O(P x bound universes) comparisons, proved separately from
       the distinct custody count and priced in `seed_run_custody`'s precharge (statement 3). No cap on P enforced
       before the join was located by this text's author. The implementing unit establishes one before the join's
       limit is set, taking the first of these bases it can show at an enforcing line (lead ruling E-10): (1) it
       exhibits, at the enforcing producer, an injection from the distinct planned programs counted by P into
       distinct stages of the admitted Plan, accounting for universe and stage deduplication and for retained
       programs no worker serves; then P <= S <= 1,024 by `crates/plan-priced/src/plan_stages.rs`:18. Showing only
       that every program is associated with some stage is insufficient. If this injection cannot be proved, it
       proceeds to basis (2); (2) P is at most the unit bound discovery enforces
       times the programs one unit can yield, each with its constant and line; (3) P is at most what the Plan
       ledger admits, since each program's admission is charged on it before the program is taken
       (`plan.rs`:724-731), to be used only if (1) and (2) cannot be shown and stated as such; the unit then
       names a strictly positive minimum charge per accepted program in one named ledger dimension, the fixed Plan
       profile cap and the ledger's non-resetting accumulation, and states P <= floor(cap / minimum charge); this
       use spends nothing of the Plan ledger on statements 1-3. If none can be
       shown, the unit stops and reports; it does not set the limit.
     - **C3 closures:** descriptors and manifests at most 128 + 4 ("`semanticClosures` (128)", M3C:1058;
       `plan.rs`:318-320; the four of `run_custody.rs`:437-441); tree blobs at most 100,000 per closure
       (`#/$defs/closure/properties/tree`, `"maxItems": 100000`, `identity-schemas.v3.json`:290-292, equal to the
       product schema's :290-292), enforced by `IdentityCandidate::from_json`'s schema admission
       (`identity/src/descriptors.rs`:592-597; `maxItems` at identity `schema.rs`:881) at `run_custody.rs`:374-383.
     - **C4 records fact admission and execution-input construction write into the custody** (lead ruling E-9, as
       corrected). Their count is bounded through bytes. It includes every object and blob they can add: per admitted
       fact candidate a payload blob and a fact object (`fact_admission/candidates.rs`:807, :852-860); view and scope
       records (`fact_admission/views.rs`:165-180); inventory records, of provider returns, of host inventory stages
       and of unavailable bindings (`execution_capture.rs`:1431-1441, :1446-1450, :1461-1468, :1472-1480); bound
       target-attribution blobs (:1581-1583); the execution-input record (:1592-1611); and, once per join,
       `RELATION_PAYLOAD_SCHEMAS` (`candidates.rs`:949).
       - *Provider returns:* the implementing unit proves that only TS2 session returns satisfying the aggregate
         response bound can reach fact admission and the joined custody. The bound is `TS2_RESPONSE_BYTES`
         ("**1,073,741,824 B** provisional", M3-D `supervisor-d/PROPOSAL.md`:546), tested by the supervisor after each
         participant step at `components/src/supervisor.rs`:3687-3694. A step may include several frames
         (`components/src/provider_protocol.rs`:195-218; `provider_protocol/ts2/participant.rs`:618-650, :734-735); no
         one-frame overshoot is assumed. If every session that breaches the bound has all its returns excluded before
         fact admission, this aggregate bound may be used for the retained per-session population. If any
         breached-session return can be admitted, the unit stops and reports until a bound on the admitted population
         and its enforcing point are established. Any transient-step overshoot or spool-storage bound that is needed
         is derived separately from the actual batching and read-buffer behaviour. TS2 has no
         `maxCandidateSpoolBytes`; that limit is Rust3's (`release_limits.rs`:23; `rust3/accounting.rs`:39, :165). The
         retained custody count is derived from the applicable aggregate byte and frame populations and proved
         positive minimum serialized sizes, including independent per-frame and per-stage records, per-candidate
         materialization and the separately enforced number of sessions (one per planned universe,
         `analysis/compose.rs`:478-480); each constant, multiplier and enforcing line is named; a candidate count
         alone does not bound records that can exist with zero candidates.
       - *Host inventory stages:* at most (inventory stages, one per bound universe in the composer's map,
         `inventory_inputs.rs`:174-178) x (entries per candidate) x (rows + packages), since each stage admits file
         and package candidates over the extent (`fact_admission/stage.rs`:1054-1073), plus their inventory records;
         not "the sealed inventory (100,000 rows)".
       - *Other host-generated records* (unavailable-binding inventories, the execution-input record, fixed per-stage
         and per-invocation records) are bounded by the sealed rows and the admitted Plan's stage, binding and locator
         populations, with their multiplicity.

       The implementing unit names each enforcing line, its owning accepted reference and each multiplier. If any
       byte, frame or count bound is not enforced before admission of what it bounds, that is a finding against its
       owning producer (the spool), not something the join's limit can cover: the unit stops and reports.
     - **M1 minted subjects and predicate blobs:** each costs one step of the evaluator's local budget before it is
       inserted (`composition.rs`:251, :739; `step`, :42-45), the owner budget of "20 000 000 steps" (X5
       `PROPOSAL.md`:131; `fact_admission.rs`:28-31, passed at `analysis/compose.rs`:616).
     - **M2 findings, fingerprints and parameter blobs:** at most 3 x 100,000 (each finding adds at most one
       fingerprint object and one parameter blob). The accepted output arrays are bounded at 100,000
       (`#/$defs/proof-bundle/properties/predicateProofs` and `/findingIds`, `"maxItems": 100000`,
       `identity-schemas.v3.json`:1190-1192, :1277-1279), and "Array/C-byte output bounds are separately enforced;
       overflow refuses with EVALUATION.OUTPUT_BOUND_EXCEEDED / OUTPUT.SERIALIZATION_FAILED (operational-failed,
       faultCause=output-serialization), never truncation or a successful empty Run." (evaluator composition contract
       v3, `ARCH/docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`:38); the estimator
       enforces it before output construction (evaluator `budgets.rs`:96-98 via `composition.rs`:816-821).
     - **M3 the proof bundle, evidence, seal and Run:** 4 (`composition.rs`:1008; `replay.rs`:471-477).
     - **Minted bytes:** each minted record encodes to at most 4 MiB ("Maximum descriptor is 4 MiB", IE,
       `ARCH/docs/v2/contracts/product-v1/identity-and-evidence.md`:117; identity `canonical.rs`:489). An encoded
       bound is not by itself a peak-heap bound for parsed values and map nodes.

     **The join's local limit.** The join is guarded by a local limit equal to the sum of C1-C4 and M1-M3, computed
     from the named enforcing constants themselves, not restated as numbers (so that raising an upstream cap cannot
     make the join refuse lawful Runs), and counting shared or duplicated records conservatively. The implementing
     unit states explicit work and peak-live-allocation bounds for the join, including map nodes, parsed-value
     overhead, key comparisons and cleanup, and checks the guard before the allocations it protects. Only a limit
     implied by all these earlier caps may use row 2 (host invariant, as today, `durable_run.rs`:687-689) for an
     impossible crossing; an arbitrary limit must not hide a missing earlier cap as a host invariant. Until C2's P
     (by one of its three bases) and C4's multipliers are named, the derivation is incomplete, the limit is not set, and the join is not
     reviewable as bounded.
   - *Why this suffices* (D1's reason): D1 rejects appeal to replay's limits for derivation because derivation
     AMPLIFIES what replay admitted ("a witness reached through many parents is parsed once per path", README:74-75).
     These phases do not reparse or recurse per path: progress is quadratic in a capped S, the vectors copy O(S), and
     the join visits each minted entry once over maps whose population is the capped sum above.
5. **The avoidable work is removed first** (a requirement on the implementation, not pricing):
   - *Hash once.* A digest already verified is used, not recomputed: source blobs (`inventory_inputs.rs`:164;
     `run_custody.rs`:51-53 via :200-202); stage specs (:155, :158); semantic grant (:167, :170); configuration
     (:257, :260); capability manifest (:265, :268); waivers (:277, :280); native frames (:318, :323; :328, :342-343);
     closure trees (:399, :454-455). Reuse keeps the binding between the verified digest and the exact retained bytes
     it was verified over; it is not permission to trust a digest apart from its custody.
   - *Parse once.* `plan2` (`run_custody.rs`:44 via :124, :163, :252, :426); the snapshot descriptor
     (`inventory_inputs.rs`:102; `run_custody.rs`:44 via :179-185, :188); the enumeration plan
     (`inventory_inputs.rs`:104; `run_custody.rs`:327); a closure descriptor (:374, :387). The parse that remains is
     funded by statement 3.
   - *Move where one owner is possible.* The source blobs are not held twice (`inventory_inputs.rs`:168;
     `run_custody.rs`:200-201) where one owner can hold them; the Plan-record copies (:134, :142, :170) stay copies
     (`planned` is borrowed through `run_planned`, `analysis/compose.rs`:449-461). Recorded item R-1 governs.
6. **The census.** M3C:261 extends the T2 census to "the snapshot ledger's object, edge **and byte** caps". Those caps
   are now 2^25 objects, 2^34 edges and 2^41 bytes ("the successor snapshot caps of C2b plan r4 M4 (M4-LAW-RECORD-r2:
   2^25 objects, 2^34 edges, 2^41 bytes)", `ARCH/docs/implementation/m3/snapshot-plan-c/c2b/m5/descriptions-r1/
   README.md`:5; `crates/platform/src/work_ledger.rs`:23-31). They were derived for the walk ("payload is streamed into
   custody through a fixed, reused chunk buffer", M3C:255), while each sealed read is charged the range it asks, clipped
   to the row (`analysis/source.rs`:180-184), which is the whole row because `produce` asks for whole rows
   (`inventory_inputs.rs`:113). The implementing unit records the added costs of statements 1-3 and refreshes the
   snapshot census, keeping the premises of the adopted successor caps, M4-LAW-RECORD-r2 (accepted by `LC/c2b-m4/M4-ACCEPTED.md`;
   adopted by C2b M5, `snapshot-plan-c/c2b/m5/descriptions-r1/README.md`:5): its selected *T*sound variant with the
   conditions it retains, its *L*max envelope and its VCS and ACL premises (`LC/c2b-m4/M4-LAW-RECORD-r2.md`), with
   *T*sound and *L*max as defined in the accepted plan (`snapshot-plan-c/c2b/law-revision-r4/PLAN.md`:36-63), and
   M3C:259's margin ("with a 2× margin"); naming these premises does not widen the fit that law claims (it does not
   claim that every item-5 layout fits); the census must cover statements
   1-3 for every Run statement 2 does not refuse (B at most 268,435,456, rows at most 100,000). Until that evidence is
   accepted, the adequacy of the extended budget is unverified and no claim is made that the ledger covers the
   documented supported population: this is a disclosed limit recorded in the milestone record with its row (21), as
   interim standing, not a waiver. By LD-DEC-5 items 1, 4 and 8 a lawful repository that exhausts the ledger is a host
   defect ("A budget or limit crossing on a lawful input is a host defect and stays on the host-fault route until the
   budget is re-sized or an upstream bound refuses the input earlier.", `LC/decisions/LD-DEC-5-user-caused-host-fault/
   DECISION.md`:54-55): the census is the item-4 sizing check for this ledger (:64-68), owed before analysis is wired
   to the command line (item 8, :76-79); where it shows such a repository can exhaust the ledger, the concrete sizing
   defect is recorded and the fix is re-sized caps or an earlier bound, by a law amendment with cross-vendor review
   ("not a softer exit code", :68); disclosure alone does not satisfy the census. Exhaustion takes row 21 in the
   interim, never truncation or a newly softened public row.
7. **Controls the implementing unit delivers:**
   - for each charge of statements 1-3 (the pre-check pass; the producer's preparation; each sealed read; each seeding
     phase's precharge), on a nontrivial source set (several files, a duplicate content, an empty file) with two
     closures and two stages: with the exact budget set on the lent snapshot ledger after the walk (a narrowing test
     constructor, as `PlanLedger::limited_for_tests` is, `plan_ts2.rs`:3627-3640) the run passes, and at one short it
     refuses `WORK.BUDGET_EXHAUSTED` on row 21, its operational key retained through the actual projection and
     finalization boundary, not only a helper's exit class;
   - **cumulative scope:** start with the capture ledger carrying nonzero prior usage; run the size check, the
     producer's preparation and reread, and the seeding with a budget that admits each phase separately but not their
     cumulative cost; require refusal before the first operation the remaining balance cannot fund; verify cumulative
     usage, the unchanged ledger identity and failure latch, and that no fresh profile, replacement ledger or retry
     permits continuation. A negative mutation that opens a fresh producer or seeding ledger makes the control fail. A
     source guard checks that the durable path calls `WorkLedger::snapshot_profile()` exactly once outside
     `PlanLedger::profile`, and that `ProducedInventoryInputs::produce` and `SealedSource` take the lent ledger by
     borrow;
   - **independently observed coverage:** observe the complete phase windows (the producer's parsing, index and
     extent construction, every seeding entry point, and destruction) and compare independently counted
     allocations, bytes and work with the published charge under exact, one-short, refusal and adverse populations,
     including a lender that lends duplicate tree entries (the precharge follows the lent lengths). Negative mutations
     that remove a charge, or add a covered parse or copy without raising its price, make the relevant control fail.
     Each work dimension established by the itemization rather than measured probes is named;
   - no work after a refusal: after a one-short refusal no further read, hash, parse, copy or custody insert (counted),
     and the custody is not handed on (`durable_run.rs`:198 not reached);
   - **the pre-check, scoped:** called on supplied rows (helper level; a pass there is not a claim that a whole
     candidate replays): E = 100,000 and B = 268,435,456 are not refused; one over each is refused on X5's structural
     row with its key; rows whose raw byte sum exceeds 268,435,456 while their distinct sum equals it are not refused;
     duplicates that push the row count past the seal's cap are synthetic here. Through the composition, B one over
     refuses with a read counter on the sealed source (the seam of `analysis/source.rs`:195-196) showing zero content
     reads and no producer or seeding allocation before it;
   - **no false positive:** on complete valid candidates (including ambient keys, shared digests and empty blobs),
     independently computed distinct source totals are compared with replay's capture behaviour; and on each
     milestone fixture's committed Run, every sealed source digest is in the replayed evidence's blobs
     (`CapturedEvidence::blobs`, identity `closure.rs`:1505) and the evidence's `byte_length` (:1509) is at least B;
     the control fails if replay stops reading any source blob;
   - **row equivalence, scoped:** on inputs whose only refusal is the size (nothing else refuses before replay), the
     outcome of the pre-check's refusal equals replay's own refusal with the pre-check disabled in a test build (small
     candidates with injected smaller limits where needed). Funding-refusal and malformed-candidate precedence are
     tested separately;
   - every refusal of statements 1-4 reaches its row through the composition's projection (with U3), each tested;
   - statement 4: each upstream population premise and the resulting join guard at its boundary (exact sum, one
     over), plus a mutation that removes or bypasses an earlier enforcement; every protected allocation is preceded by
     its guard; the progress and vector-copy bounds are checked separately. These cannot be built until the
     derivation of C2's P and C4 is complete.
8. **Not changed:** the walk's pricing and caps; the discovery and Plan ledgers (the Plan ledger's use of the snapshot
   profile's limits under R-20 included); replay, its limits and rows (X5 item 5; X5-E1 Part B stays not adopted,
   `ADOPTION-X5-E1.md`:9); cancellation and refusal precedence other than statement 2's; fact admission's
   owner-specific routes; finalization's budget (X7 `finalization-x7/PROPOSAL.md`:244-250, "**No second ledger** is
   opened, and no fresh admission is created.").

## Rejected

- **A-2, everything on the snapshot ledger.** The ledger lives inside the lend closure (`durable_run.rs`:500-566, :527)
  while the progress and join run after it (:604, :687), and row 21 would then cover post-mint work.
- **A-3, local limits only.** The seeding is input-sized custody construction; Codex C asks for "an explicit funded
  scope (or a documented conservative precharge covering the entire work)" (`codex-C-c8/VERDICT.md`:22).
- **A-4, a new run-assembly ledger profile.** A second budget beside the snapshot's is what RF-4 withdrew, and it needs
  a new profile, caps and row.
- **The attempt ledger.** "**Rejected:** charging replay to the attempt ledger, which would let pure semantic work
  exhaust the owner caps meant for native custody work." (X5 `PROPOSAL.md`:69); "**Charging admission to the attempt
  ledger.** Pure semantic work would exhaust caps meant for native custody work (X5:45)." (M3-H `PROPOSAL.md`:760).
- **An approximate pre-check** (raw row totals, or totals including the fixed parts): it could refuse a Run replay
  admits (E-2).

## Open (for the lead; not settled here)

1. **The structural row names the provider for a host sizing limit** (statement 2). An existing adopted oddity
   (X5-E1 Part B, not adopted); for the owner's post-M3 list (E-1). Not changed here.

## Recorded (owed elsewhere)

- **R-1 one owner of the source blobs** (statement 5): the U4 stop condition governs (`SnapshotBytes`,
  `RetainedInputs`); C8-LEDGER-1a reports what blocks one owner (E-7).
- **R-2 the participants' sealed reads.** `SealedSource` gives each J-zeta participant "its own ledger"
  (`analysis/source.rs`:101-102); no production launch exists. Out of scope; owed with the launch seam (E-8). Once
  `SealedSource` borrows its ledger (statement 1), the participants' launch must lend one too; no exemption for them is
  adopted here.

## Advisories not applied

- **Claude A-5** (the code comment at `work_ledger.rs`:272-276 is already false because of R-20): not this erratum's
  text to fix, as the reviewer says; statement 1 now states the true position. Passed to the lead for the owner list.

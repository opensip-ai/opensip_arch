# Codex review: SM-REPLAY-SIZED-r1, round 2

**Verdict: ACCEPT.** No required findings or nonblocking observations. **SM-REPLAY-SIZED-R1-RF-01 is resolved.** Acceptance covers the exact retained workload-sized synthetic replay/scaling evidence and its separately pinned rows variant. It establishes no real SM-9 bound, real-workload outcome or gate closure.

## Subject and custody

Stage: `/tmp/opensip-implementation/sm-replay-sized-r1-stage`.

Manifest: `subject.json`, 117,933 bytes, SHA-256 `99ada5464c5747ab050eb0c1fae4f7276935a02ae13a2cf4f7996591a09118a2`. All **512 members** independently rehashed and matched their declared sizes and digests. Bases remain clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `a208594febcad2e08439f379a50bb4e78b473ca9`.

## Round-1 finding resolution

REPORT.md now describes synthetic replay scaling scenarios at each workload row's source count. It explicitly withdraws the earlier sizing claim as a bound, explains why a real rule may emit zero findings, and states that monotone synthetic medians do not order real graph shape, predicate work or retained bytes.

The current audit removes `EDIT_TARGET_MS`, the measured-sample threshold comparison, the inferred F statement and `lowerBoundAssumption`. Its workload rows now use `syntheticScenarioMedianMs/MaxMs/MinMs` and `boundsRealWorkloadSM9=false`, with no `SM9LowerBound*` timing or target-classification member. Current checks have no editTargetMs, inference or lowerBoundAssumption. The legacy aggregate `SM9LowerBoundOnly` is explicitly false; it is a withdrawal marker, not a bound assertion. Historical references to the rejected claim are labelled as history.

The corrected decision was checked against the named control-state decision's correction record. It keeps the historical native release replay boundary, withdraws one-fact/finding/fingerprint-per-source sizing as a bound, and establishes no outcome. The report accurately quotes the correction. Any proposed future real-graph/work-dominance approach remains follow-up work under the owning laws; this acceptance changes no S-M sequencing or gate authority.

All fourteen rows leave (A)/(B) unestablished. No F/T number or formal outcome is derived or recorded. The corrected record does not treat an illustrative synthetic timing as the corresponding workload's SM-9.

## Historical preservation and diff scope

The original 116,787-byte manifest is preserved as `history/round1-subject.json`, SHA-256 `8db34d129e7458c3eb11c4f4fdf7582e8967496a6a7628d809671904729adcf0`. Rechecked all 507 original member pins against unchanged current members or their exact historical copies.

Only the report, audit and derived checks change among shared old paths. The round-1 freeze script is replaced by a round-2 freeze script; its exact original bytes are retained in history. The five history members preserve the original report, audit, checks, freeze script and subject. All raw series, stdout/stderr, packet archive/index, generators, schema, image, variant source/build/converter and runners remain byte-identical to round 1. The prior review directory was not modified.

## Audit reproduction

Ran exactly the expressly permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-replay-sized-2026-10-13/audit_sized_replay_r1.py`

It exited0 and reproduced the frozen round-2 output **exactly**: 17,195 bytes, SHA-256 `46617e5e3244f1a131da0c022ba662dc5c4e76e451a37693cd2509bf7dc8c639`. The external audit and its data inputs match the stage. No replay image or experimental runner was invoked.

The revised audit's numerical series summaries agree with round 1; only interpretation and labels change. Napi retains distinct TS193 and Rust239 source-count scenarios, the overlay is279, and Express remains its141 synthesized-program-root scenario. No edit-target comparison is performed.

## Closed pieces, schema and variant

The two closed generators remain byte-identical to the accepted native-spike copies. Raw and selected packet193 equal the accepted packet bytes. The selected schema exactly matches native-v2 at `2fbb75c^` and `37581132`; the schema-difference record retains only its previously disclosed source-path difference.

The closed image retains its accepted `e82a4e2f…` digest. Series1 completed exactly the nine whole packets fitting the unchanged4MiB parse_json cap. The first size678 child retains its empty stdout and ByteLimit panic at main.rs:9, before replay. Other larger sizes were not presented as completed series1 sets. No parser, traversal, replay or output bound was raised.

The separate rows variant still changes only input loading. Its replay registry/retained construction, limits and timed `replay_run` body are identical to the closed main. Cargo.toml changes only product dependency roots; Cargo.lock equals the accepted lock. The release build recipe, retained first-build records and unchanged image pins remain as reviewed. The staged rows image equals its built executable: 5,553,280 bytes, SHA-256 `7635c002b2ed877f89582360b6eae54e8de1a6c91811a4f188b083919609fc24`.

The audit rehashes the historical product export against git ls-tree37581132. Independently checked 1,082 exported files against Git blob bytes and file/symlink/executable modes. The historical native release boundary is disclosed; current-head replay cost is not claimed measured.

## Packets and independent series checks

All42 regular packet-archive members match the index membership, byte sizes and SHA-256 values. No extra, duplicate or nonregular member was accepted. Archive members were read directly without extraction. For all fourteen sizes, row inputs reassemble to exactly the selected packet's consumed runId/objects/blobs values; ignored documentary top-level keys remain disclosed. Each row stays under the unchanged cap; largest is1,776,379 bytes.

Independently checked every successful child stdout against its result row, empty stderr, priority readback10, fullReplayPassed and findings=count. All completed sets have three warmups and seven measured runs. Replay medians/maxima and whole-process medians recompute exactly.

Series1 has nine completed sets/90 successful children plus the retained refused size678 child. Series2 has **fourteen sets/140 successful full-replay children**. Object/blob populations match on overlapping sizes. Their previously observed median ratios remain approximately0.96513–1.03585: descriptive agreement, not statistical equivalence or real-workload dominance. Series2 synthetic medians remain monotone; no extrapolation or target inference follows.

## Standing and boundaries

Synthetic packets remain synthetic observations, not compiler fact volumes, findings from the named repositories or native admission evidence. The lead macOS host is preliminary, not D12. Fresh process creation is recorded but page-cache resets are not; no Q0 cold/warm reset is claimed. Product37581132 is explicitly the measured implementation, with current-head source/schema differences disclosed.

`lowerBoundEstablished=false`, `realWorkloadInference=false`, `comparedWithEditTarget=false`, `workloadsWhereANotEstablished=14`, `SM9FigureComplete=false`, `FComputed=false`, `TComputed=false`, `outcomeRecorded=false`, `SMComplete=false`, `LG1Met=false`, `effectiveL=false` and `productQualification=false` are the actual checked standing. No SM9 placeholder is filled. Product/lock/inventory187/contracts161 remain unchanged; O7/D3/D13 remain closed; L-G1 and remaining product duties stay open.

Only read-only hashing, JSON/source inspection, Git queries and the expressly permitted audit were performed. Its allowed output rewrite was byte-identical. No image, generator, converter, runner, Cargo, tests, lane, compiler, network, other pane or delegation was used. No private413 fixture, installation directory, signing keys or held-tree content was read. No repository, stage, working input or control file was edited. Only the requested REVIEW.md/review.json were otherwise written; the round-1 review remains untouched. Nothing was pushed. Exact lead assent and fresh design/implementation verification before publication remain separate lead work.

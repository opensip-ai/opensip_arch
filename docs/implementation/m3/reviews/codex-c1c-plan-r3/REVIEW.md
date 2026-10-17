# C1C-PLAN-r3 review

**Verdict: REQUIRED-FINDINGS.** Two required findings; no nonblocking observations.

## Subject verification

Verified the 761-byte manifest, SHA-256 `4ebb6fd9db35799dbf61b1ac717d2658e1ae971299a4aa879c132a285a1cff66`, and all three members. PLAN-r3.md is 42,023 bytes, SHA-256 `852df6d8b70353a51e4e4ef218dc074d2aa8f12a61bbcd73e281530ce85dded3`. PLAN-r2.md remains 33,396 bytes / `682088c37c89adf1ca846f91b7caf27b4264cea66876c13c3ad19ae8aaae8186`; PLAN-r1.md remains 22,877 bytes / `b9c040834b12535cd88f0ea4c6bbf9c2682c5a1507d1fb14dc13698e3ad01eb4`, matching the earlier reviews.

The manifest bases are product `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and architecture `2d169666ee5c28eedea5e43083b7968b6ba80e9f`. Live HEADs have advanced to product `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture `bd77891d106cd40a0e9e33962aee7e9e4ada7505`. Git inspection confirmed the inspected product snapshot_walk.rs, discovery_rule.rs, snapshot_source.rs, host snapshot.rs and snapshot_ledger_model.py are byte-identical to their declared-base versions. The review is of the pinned plan and declared authority, not an implicit rebase.

## Required findings

### C1CPLAN-R3-RF-1 (P2): Account for C1c-0 evidence retention in its own charge model

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r3.md:138`.

LD-C1C-13:171-175 now assigns C1c-0 the charged WalkEvidence return and charged retention of the walk's member roots. These run as part of CaptureSession::walk, on the snapshot ledger, even before C1c-1 exists. At the declared base, snapshot_walk.rs keeps only the incremental known Cargo-root set and removes entries on frame exit (:225-226); it returns only SnapshotWalkReport. Retaining the complete Cargo-root evidence and member-root set is a new storage/ownership obligation. Yet LD-C1C-9:138 still requires only pin regeneration and claims C1c-0 adds no snapshot-ledger charge because C2 captures use their caller's ledger. That explanation does not cover the changed snapshot walk. LD-C1C-8 prices the evidence only in C1c-1's later term and gate. Thus the plan gives C1c-0 contradictory pricing duties and can leave its native/model soundness and cap evidence stale until a later unit.

Required change: Resolve the ownership and charge change before C1c-0 acceptance. If retention adds charges, C1c-0 must own the corresponding model/anchor changes, regenerated soundness vectors and applicable r9 fixed-cap evidence, plus its recipe/pin receipt impact. C1c-1 then extends that accepted recipe with its own read-set work. If an implementation can instead retain everything by already-priced moves/borrows with zero incremental charge, specify that mechanism and require an exact charge/model equivalence control in C1c-0; do not simultaneously promise new charged retention and pins-only changes. Update the split, LD-C1C-8/9/13 and checks consistently.

### C1CPLAN-R3-RF-2 (P2): Allow rows authorized by overlapping layout directories

Location: `docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r3.md:99`.

The new allocation-free guard requires each ReadSet row to lie below exactly one retained admitted realPath. Neither the layout schema nor IE:567-583 requires the directory set to be prefix-free; IE authorizes a row through a qualifying listed prefix. The plan itself prices traversal of overlapping directories at LD-C1C-8:120. For retained realPaths node_modules/a and node_modules/a/subpackage, the row node_modules/a/subpackage/x.ts lies below both, and neither relative suffix crosses another node_modules segment. It is a permitted read, reused once by the session, but the new exactly-one guard rejects it as Internal. Identical-path deduplication does not eliminate these distinct overlapping prefixes. Round two's guard required a qualifying layout row, not unique coverage.

Required change: Require at least one eligible retained authorization satisfying the suffix and exclusion rules. Alternatively assign each row a deterministic unique authorization during charged preparation without rejecting otherwise permitted overlapping directories, and check that assignment at sealing. Preserve the per-layout-row manifest digest joins and single capture. Add an overlapping-realPath control where both prefixes qualify and the shared file is inventoried once, plus the existing nested-node_modules negative and separately authorized positive controls.

## Round-two dispositions

**C1CPLAN-R2-RF-1: authorization semantics addressed.** LD-C1C-5 now applies non-dependency exclusions to the full authorized path plus descendant. First-party Cargo roots come from the session-retained walk derivation; dependency-tree Cargo markers are observed during reach and descent, including above an independently listed nested package. Exact root/member .opensip anchors use the shared custody-state rule, and VCS segments are excluded throughout. Allowed target/non-anchor-.opensip lookalikes remain eligible. The new controls cover target/node_modules/a, a package inside another package's Cargo output whether or not its enclosing package is listed, root/member custody anchors and a no-open/no-origin-change spy.

LD-C1C-13 improves evidence provenance: opaque WalkEvidence is obtained from the session's own walk; retained member roots must equal the supplied extent's member roots; dependency-tree Cargo.toml status uses charged fstatat with no-follow observations, regular-file kind only and no content read. These are appropriate operational observations. Their pricing must be reconciled at the earlier sub-unit as R3-RF-1 requires. The same-root extent remains an explicit composition precondition; the opaque type does not replace that precondition.

**C1CPLAN-R2-RF-2: addressed.** LD-C1C-9 explicitly assigns every sub-unit to an open reviewed interval before freeze, or a new interval at integration. C1c-1 owns a new interval after either a closed C1b batch or separately refreshed C1c-0, with its pre-run review, frozen-input blind refresh and post-run review before dependent reliance. Receipt deltas use a fresh accepted baseline; unchanged discovery stays current in the stated no-new-closure-change cases. Earlier refreshes do not cover later recipe edits.

**C1CPLAN-R2-NBO-1: preparation/check split addressed, with the new guard regression in R3-RF-2.** LD-C1C-7 now retains the charged authorized set, verdicts and excluded prefixes, and sealing performs borrowed comparisons without source reads, new strings or charges. LD-C1C-8 explicitly includes retained evidence and Cargo observations in the full cumulative derivation. The added source-pin/ledger-delta and injected-excluded-row controls are appropriate. Allocation-free checking does not require exactly-one prefix coverage; that added restriction must be corrected.

## Retained requirements

The shared-rule API remains separate from discovery's outermost classifier; ordinary and pnpm descendants are admitted, and a further exact node_modules segment needs its own row. Discovery semantics and vectors remain unchanged while the whole-file rule closure is re-pinned. Boundaries and ignorePaths apply from the walk's own admitted extent before descent, reach/origin changes and admission; excluded required manifests remain leftovers. Captures remain read-once, with enumerating-parent observation comparisons and no retry. Per-layout-row digest joins survive identical-realPath deduplication; first-party workspace-link manifests retain Walk origin.

The preparatory C1c-0/C2b/C1c-1 integration order, custody split, raw case-sensitive suffix set, safe filtering of unread names, no-follow/special-file rules, no-layout identity preservation, side-record origin outside identity, and joint item-5 bounds remain. Typed refusals and separate Budget failure remain. The full C1c-1 gate includes walk, session, sealing, accepted VCS work and read-set work, synthetic/native soundness and boundary controls, and r9's unchanged caps with its 2x rule. Per-layout entry bounds are not misrepresented as a global layout bound; non-row/setup/overlap excess is explicitly in the typed-refusal regime.

Receipt evidence remains separate from generated-output checks, with exact per-receipt changes, no fabricated staleness, failure on bad pins/malformed or missing artifacts/output differences, and final freshness for every receipt. C2b's obligations during an open interval and C1b's shared-sealing-file rebase/anchor requirements are retained. The existing no-layout census is not represented as measured installed-layout evidence. No code, live refresh, production caller, qualification or completion is accepted by this review.

## Review boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, lanes, network, panes or delegation. No private fixture, installation directory, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.

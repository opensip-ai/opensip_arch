# D2B-0b-r1 review

**Verdict: ACCEPT-DESIGN-UNIT. Product code assessment: ACCEPT-UNIT.** No required findings or nonblocking observations.

This accepts the pinned generation successor and its product changes. It does not bind or integrate them, complete the separate blind refresh, accept a codec or establish product qualification.

## Subject and pins

Verified the 28,499-byte manifest, SHA-256 `aaf13eaa41e82b74b531b624cd290e4455b3bf9b707640a86df9953a7b6821ac`, and every one of its 121 members. Its membership is exactly successor.json plus that record's candidates. All nine live worktree candidates were checked against the parent/candidate/archive records in product-map.json; all nine parent byte counts and hashes match product base `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a`. No new product path exists.

The successor's seven parents match exact accepted design-lock inputs/candidates or successor records: the five prior generator inputs and FA-2/RUST3-LIM. The source record's authority pins also verify. Product worktree HEAD and architecture HEAD match `3d1d771ecc5a8772d57f8393ce09cc82ce5f025a` and `2d169666ee5c28eedea5e43083b7968b6ba80e9f` respectively. preparation.json records an earlier preparation base; the lane of record, frozen product-map parents and determinism evidence use the requested final product base.

## Pattern-profile assessment

`patternProfileByM1Method: true`.

Read the M1 source and compared its translator syntax tree with the preparer's: identical apart from comments/positions. The recursive visitor is identical after accounting for the explicit accumulator parameter. The template matches M1's exact table rendering. No hand-written translation replaces that method.

Read-only JSON inspection confirms the old 28 sources collect exactly the old 66 profile patterns; the candidate's 30 sources collect exactly 67. Every profile source pin verifies. The only added row is SubjectIdV1's pattern, with identity translation. All old rows remain unchanged, and the candidate table is the exact template rendering of the profile rows plus the same three pre-existing outside-profile entries. All 69 prior table entries are unchanged; the new table has 70. Preserving the three pre-existing entries without pretending they belong to the reproducible profile is appropriate for this narrow extension.

The pinned differential uses Python re.search reference results and Node RegExp with the u flag, over the M1 values plus the targeted SubjectId cases. The lane records 67 patterns × 1,336 values = 89,512 comparisons, zero mismatches. Its table equality checks cover the connection between the translations tested and the selected runtime table. This is finite selected-pattern evidence, not a generic equivalence claim for Python and ECMAScript regular expressions.

## Generator rows and carriers

The two new source-map rows point to the exact accepted FA-2 and RUST3-LIM schema bytes. Namespace/module choices are SymbolCensus1/protocol and RustSubjectScope1/protocol; declared major, reference profile, semantic owner and standing match the stated decisions and existing conventions. Existing source-map, owner and source-mapping rows are preserved.

All 20 symbol-census definitions and all five rust-subject-scope definitions have exactly the expected entry points and names. No new Root or provider entry point is added. Common-v4 has all 64 definitions and no root entry point; graph-query-v4 likewise has no root entry point. Native-v2's three omitted definitions are the denied handshake/limits definitions; it is not a no-root precedent. These precedents support definition-level selection here. Because neither new annotation-bearing root is converted, the selected runtime annotation set needs no change. This resolves A1's annotation question while preserving its generated-carrier obligation.

`existingCarriersUnchanged: true` means existing carrier/type definitions are preserved, not that the two changed output files are byte-identical:

- protocol.rs adds 919 lines and removes none.
- report.ts adds the expected new material and replaces exactly four old lines: registry digest, generator-closure digest, selectedSchemaBytes and selectedSchemaEntryPoints. The runtime pattern table gains its single entry. No existing type definition changes.
- All eight output pins match the worktree. The other six outputs, including the TypeScript provider protocol, are byte-equal to the base.

The lane's generation-check.json reports a deterministic check re-run with 43 sources, 883 entry points and no differing output. No generation was re-run by this reviewer.

## Closure, recipe and binding

Independently verified all 352 candidate closure file pins. The closure adds exactly the two successor sources and re-pins exactly source-map.json, options.json, pattern-profile.json and patterns.ts. Registry source hashes, options digest and generator-closure digest match their actual inputs. Existing providerEntryPoints and deniedRefs are unchanged.

The package contains the exact product generator-closure bytes that the public generator requires to be selected by an accepted design unit. The reviewed successor's candidate membership supplies that closure input after binding. Before binding, the archived public-generator invocation refuses at that acceptance check with exactly `generator closure is not selected by an accepted design unit`; it does not claim a completed public generation run.

The sole operability-exception change is generated protocol.rs's into-call count, 99 to 110. The repinner uses mint_inventory(), preserves every other audit row, and follows B-S10 commit c019e9e's generated-count precedent. The permitted live operability check passes with 114 rows and no findings. This is generated conversion accounting, not a new hand-written mint authority.

## Census and refresh

`censusChecksPass: true; blindRefreshSeparate: true`.

The archived discovery census, workspace ledger and snapshot census checks all pass. Their checked-in records and the blind discovery receipt are byte-equal to the product base. No discovery cost-closure file changed.

The permitted live stale-receipt checker confirms that candidate-versus-base bindings differ in exactly one reference row: generator-closure.json changes from 68,468 bytes / `796701ea87e7ff7db1b029c8c0eea043e550e9cd5f0daf234637fae927291acb` to 68,832 bytes / `e09d7bfee34fa260c9c040ce351153eb74e2f03eaf7e783ced61047e3455d868`. The receipt was already stale on the base in its closure and tool bindings from C1a4. All ten held-out rows render stale and heldOutMargin is outstanding. This is public receipt/record evidence; no T2 store or held-out contents were accessed.

Passing generated-output checks are correctly separate from freshness. A1's reviewed blind refresh remains explicitly owned by the separate follow-up unit, with pre-run and post-run review; combining it physically with C1a4 requires frozen final inputs and the governing review protocol. Earlier receipts do not cover later changes. D2b-3/4 remain downstream of D2b-0b and its required refresh ordering. No remaining generation obligation is left unowned.

## Lane assessment

Attempt 3 is the lane of record. Its raw suite logs match the summaries and identical failure-name sets on both sides:

| Suite | Base/candidate passing | Base/candidate failing |
| --- | ---: | ---: |
| contracts | 0 / 0 | 0 / 0 |
| components | 43 / 43 | 0 / 0 |
| identity | 72 / 72 | 0 / 0 |
| host | 409 / 409 | 8 / 8 |
| storage | 137 / 137 | 33 / 33 |
| evaluator | 47 / 47 | 0 / 0 |

The host/storage failures are pre-existing, not a wholly green suite claim. The lane records passing warning-denied all-targets Clippy, report TypeScript lane, FW-01, environment exceptions, operability, unchanged discovery closure and design preflight. The edited generated Rust file is base-dirty under rustfmt and excluded under the declared policy, rather than represented as format-clean.

The generator TypeScript lane refuses for the same package.json tool-policy pin on base and candidate. The runner compares that reason; this is a preserved pre-existing refusal, not a passing generator TypeScript lane. The generator's separate deterministic pipeline check passes.

Each of the four mutation logs reaches its named detector and expected refusal: missing pattern entry at validate; altered C1 translation at the differential; wrong namespace at ownership/unique-name validation; omitted entry point at prepare. Attempts 1 and 2 remain void history and are not substituted for attempt 3 evidence.

The permitted live verify_design invocation also passes, with productQualification false. No unaddressed regression was identified within this generation-only scope.

## Review boundaries

Only read-only inspection, hashing, JSON/source parsing and Git queries were used, plus the three explicitly permitted live commands: operability source, verify_design and check_d2b0b_census_stale.py with /dev/stdout. No Cargo, rustc, build, generator or lane was run. No network, other panes, delegation, private fixture, OpenSIP installation, signing keys, held trees, T2 stores or cache were accessed. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.

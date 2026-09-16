# Independent Grok review: history-native delta01

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-history-native-delta-subject-01`
**Manifest SHA-256:** `c87231a09082032f9b7c61ece2d13a7b31ab596478027f45e9940db95bbcb224`
**Members:** 403
**Verdict:** **ACCEPT WITHIN STATED DELTA SCOPE**

Closes history-selection02 **S1** (retained `run.show` must require `items`) through history03, joint13, generation03, codec03, and native04 report reader. Scope is this source-to-generated delta, not design-unit or product selection.

Parent **history02** remains ACCEPT WITH S1 should-fix. Native-integration03 remains ACCEPT; this delta does not reopen native S1. Historical compile04 `TS5112` (no `--ignoreConfig`) is preserved evidence, not this execution.

## Custody

Verified before and after. Frozen subject not executed against. `history03/` is byte-identical to `m1-history-selection-subject-03` (88/88). Declared external pins (history03 manifest, native04/generation03/codec03 checkpoints, fixtures) **0 fail**.

| Check | Result |
| --- | --- |
| Manifest | `c87231a0…b224` matches declared |
| Files | 403 listed = 403 walk |
| After | frozen hash unchanged |

## S1 correction

Standalone history candidate still uses URI `urn:opensip:product-v1:workflows:evaluator3:graph-query:3`. Independently: history02 candidate **still accepts** a retained `run.show` with no `items` member. history03 then-branch adds `"required":["items"]` and **refuses** omitted and empty retained items; unavailable/expired/purged/corrupt empty `items` still admit. Old bytes must not be relabeled as typed `RunShowItemV1`. Composed dispatch uses **query4** in the generated reader.

Producer/consumer Python is unchanged; schema refusal precedes `items[0]`. Deleting `required:["items"]` from the candidate schema makes `check_query.py` fail `retained-missing-items-schema-refuses` (independently reproduced).

## Reproduction (private copy)

- history03 `fullcheck.py`: build/check/query/budget/mutants all exit 0. **18** selection groups, **18** query groups (14 inherited + 4 missing/empty/multiple-items), **12/12** inherited mutants.
- Two fresh `assemble_eight.py` runs (`fresh01`, `fresh02`): **8/8** byte-identical to each other and to `eight-j`. **7** outputs match accepted native03 (all 6 Rust + provider TS). Only `apps/report/src/generated/report.ts` changes.
- Strict `tsc` 6 `--ignoreConfig --exactOptionalPropertyTypes --module Node16`: exit 0; compiled JS matches frozen `compiled04`.
- `check-consumer04.cjs`: **71** checks (64 inherited shapes, dense report round-trip, default **4 MiB** `parseExact` BYTE_LIMIT vs report-profile parse, unselected roots, stale inventory/profile).
- `check-history13.cjs`: **17** checks. Predecessor generated registry still admits omitted retained items (negative control). New registry refuses omitted/empty/multiple/untyped retained items; empty unavailable states admit. Fit `sourceStep` **0n** admits; `0.0`/`-0`/`0e0` refuse lexically; boolean and JS number `0` refuse at exact-type boundary.

No new Rust execution claimed.

## Independent probes

Schema-level (not generic float-integer JSON Schema): history02 hole vs history03 required `items`; unavailable empty still valid. Generated exact decoder: Fit floats refuse before schema; JS `0` is `EXACT_JSON_TYPE_REQUIRED`. Default envelope 4 MiB/32 vs report development-caps.6 preserved by consumer BYTE_LIMIT on `parseExact`.

## Must-fix / should-fix

None in this delta scope. History02 S1 is **closed here**, not waived on the original unit.

## Remaining

Store/CLI/browser; source selection of query4/common4/report reader; host `close_run` custody. Not product or milestone qualification.

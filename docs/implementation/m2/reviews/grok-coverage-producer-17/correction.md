# Correction: coverage-producer-17 source-review report facts

**Not fresh-blind.** Original `report.md` / `report.json` preserved (`f6fdeee2…8593` / 7311, `ea139b48…b79a` / 5783). No source edits. Root remains lead. Root independently read selected I order; **no source fix in trial 17 is required.**

Two report citations were wrong. Neither is a producer-code finding. **Source verdict remains `NO-REQUIRED-FINDINGS`.**

## 1. Dependency paragraph mislabeled the 16 subject pin

Completed `report.md` line 21 wrote:

> capability-support-16 subject `6539a71f…be28`

That truncated suffix is **body-identity-15**, not 16.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/body-identity-15/subject.json` | 51854 | `6539a71f9b7a5b8f437fe5e20788e02b3bccfe45cae44642b79cd2666fc15956` |
| `docs/implementation/m2/trials/capability-support-16/subject.json` | 53521 | `b3d1c76c78cf7d6ae43b4673b90d2458f01c8139bbf818076f2bd88d9a16be28` |

The trial’s own `dependency-pins.json` already listed 16 as `b3d1c76c…be28` / 53521. The 232-file delta vs frozen 16 is unchanged. Only the review prose truncated the wrong sibling pin.

## 2. FullRun identity comparison is before 16 guards and totality

Completed `report.md` line 55 wrote:

> FullRun still: producer **before** the three 16 guards and inventory totality; then coverage-identity comparison

Selected `identity_model.py` `619d6e3c…41e6` / 158555, `open_run_closure` per-`coverageIds` loop:

| Line | Call |
| --- | ---: |
| 1934 | `admit_coverage_result_v3` (this owner) |
| 1936 | `COVERAGE_PRODUCER_ADMISSION` if not ADMIT |
| **1937** | **`COVERAGE_ADMITTED_IDENTITY`** if `admitted['coverageId'] != cid` |
| 1938 | `coverage_dialect_prerequisite` |
| 1939 | `syntax_capability_prerequisite` |
| 1947 | `coverage_source_variant_prerequisite` |
| 1948 | `coverage_inventory_totality` |

Producer still precedes the 16 guards. Coverage-identity comparison is **1937, before** 1938–1947 and 1948. Public D9 routing remains a later host surface.

`report.json` `law.producerBefore16GuardsInFullRun` stays true as a producer-vs-guards statement; it did not encode the inverted identity-comparison clause. That clause existed only in `report.md`.

Trial 17 implements the producer boundary only. It does not walk `view.coverageIds`. Reordering FullRun composition is identity’s later job, not a 17 source change.

## requiredFindings

None. Verdict unchanged.

## Scope

No product files created here. Original reports not rewritten. No live/frozen/history edits, no commit/push.

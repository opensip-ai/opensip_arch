# Independent Grok review: report-projection08 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-report-projection-subject-08`
**Manifest SHA-256:** `be85df13b84789295e4ed4b63153bfbb4589885fba22bfd883d661f97776f033`
**Members:** 21
**Verdict:** **CHANGES REQUIRED**

This is the historical 21-file author-08 freeze. Later corrections (fit-interruption01, required-output01 / L02 selection, history-selection02, presentation-catalog02, evidence-design02, joint10/13) are **not** this unit and do **not** rewrite this verdict. This is not a final source-unit review.

## RF-1 — Q-FIT-1 (required; not waived)

`fit/primary/signal-before-required-render` is a **run** carrier, query **completed**, committed Run `run3:408b3e80…`. It omits `advisoryReport`. Planned query request is placeholder `run3:bbbb…` / `prj1-aaaa…`, not the sealed Run/project.

Unchanged `report_model.static_parity_text` raises `KeyError('advisoryReport')`. Independently reproduced (same bytes as `docs/implementation/m1/audits/fit-interruption-parity-01`).

`interruption_controls` adds `len(formats)` for each of 36 scenarios → **144 declared renderer rows**. That function never calls `static_parity_text`. The two other fit interruption goldens (failure carriers, query cancelled/skipped) do render (527 B / 804 B). Settled `review-P1-fit-run-without-advisory-report` is a different join (`J-ENV-FIT-CARRIER`). Q-FIT-1 is the interrupted completed-query path.

Contract §2.2 still treats this as an open omission permission. Workflows 1135 says a missing required parity field is `DELIVERY.REQUIRED_FAILED`. L02 output-failure cannot excuse this deterministic missing member.

**Later correction is not this freeze.** `m1-fit-interruption-subject-01` proposes `sourceStep` binding, retained completed page, and `unavailable-query-result`. Those files are absent here. Joint10 still has Q-FIT-1 `reference-composed-review-pending`. Do not grant Q-FIT-1 acceptance on these 21 bytes.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. Architecture/product/historical bytes untouched.

| Check | Result |
| --- | --- |
| Manifest | `be85df13…f033` matches declared and adjacent copy |
| Files | 21 listed = 21 walk (`subject-files.json` lists 20 excluding itself) |
| Pins | **96/96 files**, **3/3 listings** |
| After | frozen hash unchanged |

## Reproduction (private copy)

`TMPDIR=<scratch> python -I -B check.py --architecture ARCH --subject-strict --out …` **exit 0**, `passed: true`, `productQualification: false`.

- Alias probe: all three spellings `UNPINNED-LOAD`
- Unattributable-path (RPR6-1): five events `UNATTRIBUTABLE-PATH-EVENT`, cwd restored
- envelope6 `/allOf/19/then` restores envelope5 exactly; envelope5 still unaccepted (`45de2b0a…789d`)
- inventory5 additive over v4 (json renderer 6, `--baseline`, fit parity fields)
- metadata 43/43 through envelope5 and envelope6; in-process historical checker 43/28
- interruption07 bound, `integrationApproved: false`; 36 scenarios + negatives; **rendererRows 144 are counts**
- L02 regression: 4,167,140 B spec; 4,231,826 / 8,463,605 B accounts; schema/join/host accept; exact codec `BYTE_LIMIT`; lossy forms refused
- 22 aggregate, 68 delivery, 47 envelope (14 accept / 11 SCHEMA-ENV / 22 host), 194 report (30 accept / 29 SCHEMA)
- coverage overlay 323 rows, K01 workaround none
- RPR6-2 fabricated skipped detail `J-ENV-INTERRUPTION-DETAIL` / `J-LEDGER-SKIPPED`
- RPR6-3 analyze `--baseline` accept; ephemeral+baseline `J-LEDGER-MODE`

Passing this checker does **not** accept the Q-FIT-1 path.

## Inherited joins independently confirmed (do not accept the parent)

| Topic | This freeze |
| --- | --- |
| Interruption07 | Conditional parent only. Run-carrier / availability / recorded-error joins hold on the 36 scripted goldens. Does **not** accept envelope5. |
| Error accumulation | `recorded_failure_details` excludes skipped and cancelled; envelope6 empty `errors: []` when none |
| Absolute audit custody | Relative/dir_fd opens refused before content |
| Baseline grammar | `--baseline PATH` variants; ephemeral+baseline refused |
| Coverage K01 | Closed by accepted coverage-prerequisite unit `48035089…`; overlay on v3 |
| Feature owners | 11 RP-DO blockers still open; later history/catalog/evidence/history03 S1 **not adopted** |

## Later vs original (must not be conflated)

| Later unit | Relation to this freeze |
| --- | --- |
| fit-interruption01 | Proposed Q-FIT-1 correction; **not in these 21 files** |
| required-output01 + L02-policy-selection | Policy later selected; this freeze still `open-owner-decision`; source not promoted |
| history-selection02 / catalog02 / evidence-design02 / joint10–13 | Combined successors; this original-unit review is not that final source review |

## Must-fix / should-fix

**Must-fix: RF-1 Q-FIT-1** as above. Required owner succession is the later fit-interruption laws (completed retained page or `unavailable-query-result` with actual outcome), parent builders/fixtures, and actual `static_parity_text` (and renderer) on every interruption golden — not a format-count.

**Should-fix:** none separately. L02 in this freeze is an honest open obligation, not a silent capacity claim.

## Remaining

Envelope5/6 source selection; RequestContext custody; composite entry points at real delivery; all renderer formats including SARIF; 11 feature blockers; C01/C02 pending joint/source selection; P01/X01; L01; AUDIT-G10. Joint13/history03 S1 belong to a later exact source-unit review.

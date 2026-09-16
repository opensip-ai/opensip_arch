# Independent review: report projection author-05 (`m1-report-projection-subject-05`)

**Verdict: CHANGES REQUIRED** for the narrow carrier unit: one blocking finding and two required.

**Scope.**
- No report design, runtime, browser, generator, platform or release acceptance.
- The 11 report-feature design blockers, AUDIT-G10, RP-OBL-C01/K01/L01 and RP-DO-12 stay open.
- The root check is still running, so nothing here claims success on its behalf.

## Custody

**Subject identity:**

| Item | Value |
|---|---|
| Outer manifest | `a9f6c22a9b2af9487fc9683fdef76c58e391f5a6f64e2f8b09bfa75d288de2a4` |
| Inner `subject-files.json` | `0d6a4154…f45dbf` |
| envelope5 | `45de2b0a…dd789f7b1dbc7b3a9b72e9c350b9a39a37` (unchanged) |

**Before review:** 18/18 files matched as an exact set, and 79/79 pins plus 2/2 listings re-hashed with no drift. The after-verification is in `work/after-verification.json`.

**Strict run.** I copied exactly the 18 declared files to `work/closure` and ran `TMPDIR=work/tmp python -I -B -X pycache_prefix=work/pyc-prefix check.py --architecture ARCH --subject-strict --out work/strict-check-result.json`.

It exited **0** and printed `declared-out writes observed: 1`. It reproduced:

| Item | Count |
|---|---|
| Report cases (accepts) | 162 (27) |
| Envelope cases | 22 |
| Aggregate cases | 22 |
| Delivery goldens | 48 |
| Pending interruption goldens | 8 |
| Static parity goldens | 16 |
| Metadata cases | 43 |
| Coverage rows | 323 |
| Pins / listings | 79 / 2 |
| Source compiles | 20 |
| Child processes | 0 |
| `documentMaxBytes` | 27,827,987 |

## Closure of review04

| Item | Status | Independent basis |
|---|---|---|
| RPR4-1 page law | Closed, with residual RPR5-2 | See "Page law" below. |
| RPR4-2 skipped steps | Closed, with residual RPR5-1 | See "Skipped steps" below. |
| RPR4-3 C01 | Closed as tracking, with residual RPR5-3 | Register integration obligation, not adopted; C01 on 13 coverage rows; 8 pending goldens not counted as delivered; envelope5 unchanged. |
| A1 alias | Closed | PoCs C1–C9: case and symlink aliases of unpinned files and listings refused; pinned aliases re-hashed; a forged cache is ignored by the enforced loader; out aliases refused. Residual: RPR5-A1. |
| A2 pre-hook / counter | Closed | Trace: no TMPDIR opens before pin verification; writes only to out and the demonstration directory; out never read. |
| A3 codec | Closed as obligation | RP-OBL-L01, non-blocking. |
| A4 label | Closed | Renamed `graphDescriptorNotRetainedSubjectsHostAsserted`. |
| A5 R05 | Closed | RP-DO-02 holds no row open. |
| A6 workaround | Recorded as owner duty | RP-OBL-K01 (M0/M1 valid, M6 refused). |
| A7 standing | Closed | Obligations are proposals to owners. |
| A8 / A9 | Open | RP-DO-12; generator not run. |

**Page law.** The model now joins total = produced, page position, cursor and continuation, and the author's G4–G6 are refused.
- **Positives:** my own oracle sets are all lawful — exact 107 by 50, capped at 60 by 25, exactly-at-cap, single page and empty.
- **Mutants:** of 132 context mutants, every contradiction is refused. The only accepted mutants are host-unprovable relabels on continued pages, plus caller-supplied position shifts that the document cursor join covers.

**Skipped steps.** I **executed** the owner model `run_invocation` on 6 fit scenarios: skip after rejection or fault, D1, and SIGINT/SIGTERM before render. The subject aggregate matches 6/6, and every owner skip record passes `J-LEDGER-SKIPPED`.

## Required findings

### RPR5-1 (blocking): host `requirement` / `dependsOn` enables a fake aggregate switch

**The gap.** Admission joins step *kinds* only. Requirement, `dependsOn` and `dependencyGate` are checked neither against the owner DAG law (`workflows-and-surfaces.md:95-98`; `validate_dag`, `WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL`) nor against a builtin step specification. inventory5 carries none of these fields.

Since the aggregate excludes optional and skipped steps, these host fields decide D9.

**Probe S1.** Relabelling each failed required step optional, with the envelope set to the recomputed aggregate, is **accepted in 6 of 6 bases**. Every case switches the aggregate to success and violates the owner DAG law:

| Base | Aggregate switch |
|---|---|
| `default-degraded` | policy-failed → success |
| `fit-after-commit-query-failure` | operational-failed → success |
| `fit-after-commit-query-refused` | request-rejected → success |
| `fit-analysis-rejected-query-skipped` | request-rejected → success |
| `audit-baseline-rejected-comparison-skipped` | request-rejected → success |
| `review-brief-failure` | operational-failed → success |

**Probe S2.** Also dropping the dependency edges, which satisfies the generic DAG law, still **admits 4** switches.

**Correction:**
- Bind builtin HTML command step requirement, `dependsOn` and gate to an owner-published specification.
- At minimum, enforce `validate_dag`.
- Add S1 and S2 as refusal cases.

### RPR5-2 (required): the page law narrows owner-admitted lower-bound pages

**The rule.** `page_law` requires a reached cap for lower-bound, and requires rows beyond `position+items` for any cursor. That is an eager-prefix reading.

**The owner fixture.** The pinned owner reference model `query_surface_projection.v3.py:620-645` has a **positive** "graph-lower-bound-prefix-intermediate-page" case:

| Field | Value |
|---|---|
| total / produced | 2 / 2 |
| Basis / coverage | lower-bound, truncated-page |
| Rows | 2 |
| Cursor | present |
| visitedNodes | 4, far below the caps |

**Probes.**
- **P3:** that shape is refused (`lower-bound without a reached produced/visited cap`).
- **P4:** the same lazy first page in audit-full slot 0 refuses the whole document with `J-GRAPH-COUNT`. The graph panel is required, so required delivery fails.

A cursor plus a `not-embedded` continuation still discloses incompleteness, so accepting the shape reopens no silent cut.

**Correction:** get the query owner's statement on `producedItems` for lower-bound pages, then either admit lazy lower-bound cursor pages or have the owner correct the fixture. Record the result as a case.

### RPR5-3 (required): `J-ENV-INTERRUPTION-DETAIL` refuses genuine earlier details

**The rule.** It refuses *any* `errors` beside an interrupted `kind=failure` envelope, without a ledger or observation join.

**Why that is too broad.**
- Owner prose (`:1340-1344`) says failure `errors` are the actual step detail.
- Root correction02 (read-only, not adopted) states that nonempty-error forms "may retain earlier real step failures".

**Probes.**
- **Owner model:** executing analysis rejected `CONFIG.INVALID` → query skipped → SIGINT before render gives aggregate `{interrupted, SIGINT}` with no Run.
- **I1:** an envelope with that termination and `errors` = the real recorded `CONFIG.INVALID` is envelope5-schema-valid but **refused**.
- **I1:** a review-brief envelope carrying its real `evidence.missing` detail plus SIGTERM is also refused.
- **Control:** `kind=run` interrupted is unaffected.

**Correction:** refuse only details that are not recorded step details of this invocation, or leave the refusal to the successor's ledger join. Add a genuine earlier-detail case that is accepted or pending, not refused.

## Advisories

- **A1:** the scratch exemption bypasses aliases. PoC C11: a symlink in an active scratch directory read an unpinned file, within the mkdtemp window and trusted-host claim. Resolve realpath before exempting.
- **A2:** `page_law` does not bind cursor position itself (admission binds first pages only). Relabels of capped continued pages remain host-unprovable, so keep the owner-response assertion.
- **A3:** RP-OBL-L01 is correctly non-blocking. RP-OBL-K01 is necessary, because the accepted coverage fails independently of this report. Neither waives a feature.
- **A4:** C01 tracking is adequate and envelope6 is not adopted. After RPR5-3, tie the invented-detail pending golden to a ledger.
- **A5:** the before-settle `runId` is required-only, matching the owner model. Profile workflows were not exercised.
- **A6:** hard links, native extensions and TOCTOU are outside the stated claim.
- **A7:** RP-DO-12 and G01 are open.

## Limits

- Owner-model runs covered fit-shaped records I authored (6 scenarios) only.
- Graph probes used the mock owner and my own oracle, not the product engine.
- I do not decide the eager versus lazy `producedItems` ambiguity.
- Hard links and native extensions were not tested.
- No writes were made outside this directory.
- Correction02 was read for its policy only; I did not review it.
- No completed root check was available, and author responses and sessions were not read.

## After-verification

See `work/after-verification.json`: outer, inner and envelope5 SHAs, 18/18 exact set, 79 pins and 2 listings, closure copy unchanged, and no `__pycache__`. No commit or push was made.

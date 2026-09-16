# v27 successor delta + focused evidence review — progress

Origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b` (same as the source26 review). Output confined to
`/tmp/opensip-design-corrections/claude-independent-design.v27`. No input modified. The separate
blind consumer work was never read or touched.

## COMPLETE

- [x] **p00** snapshot27 verification — manifest `a1ae88ef…`, archive `adb78633…`, 12893/12893 files,
      736,295,158 bytes, 0 extras; parent `c9a6c26a…` == the source26 subject I reviewed
- [x] **p01/p02/p03** 26→27 delta derived by me — 1 added, 0 removed, 19 changed, +17,818 bytes
- [x] **p04/p05** planning layer 2 provenance; five pin ledgers digest-only
- [x] **REQUIRED CORRECTION** — read all 253 lines of
      `foundation/provider-target-attribution-return.schema.v2.json` (13 schemaKeys, ~40 joinKeys).
      v26 report left unaltered; correction recorded as C-1 in the v27 report
- [x] **pM1** hint-space 24/24, boundaries (2 probe defects preserved), routes, weighting → M-1 RESOLVED
- [x] **pS** S-1/S-2/S-3 and A-1/A-2/A-3 re-measured → all RESOLVED
- [x] **p06** author package 213/213 verified, binds exact27
- [x] **pE** all 13 exports re-executed: 7 positives ADMIT/ADMIT, 3 controls ADMIT→REFUSE replay,
      binding invalid-default REFUSED, lawful-default + single-explicit ADMITTED
- [x] **pF/pF2/pF3** from-scratch build in a fresh arbitrary dir, no helper overlay; blob delta
      explained and proven inert by mutual replay; no export repaired
- [x] **pG** evaluator3 launcher on 27 — 1242 pins, 0 changed/missing, 16/16 exit 0
- [x] **pH** remaining contract/reference groups in a verified disposable copy — 0 frozen deviations
- [x] **pI3/pI4** F-01…F-14 located (named `review.json` ABSENT; rows live in `review.md`
      `$.report.findings`, hyphenated) and read in full
- [x] **pJ** F-row remedies measured against frozen package + snapshot27
- [x] **pK/pK2/pK3/pK4** F-04 internal-root: schema, U-0 prose, executed admission, guard wiring,
      control coverage (0 of 27 checkers → advisory A-4)
- [x] **pL** I ran the package's four portable probes myself on source27 — all exit 0; 8/8 query
      outputs regenerate byte-identical; PASS 7; properties pass; mixed-universe refuses
- [x] **pM/pM2** §5 citation verified at the raise sites; TCB-13 list independently re-derived by
      reading (classifier said 14 and was wrong on three rows)
- [x] **pN** all 30 residual rows bound to frozen27 — 0 mismatches of any kind
- [x] **pO** row-custody measurement (4 rows keep no original → advisory A-5); v26 maps loaded
- [x] **pP** 123/8/3 charter handoff — ids identical to frozen charter, 123 PENDING, no waiver
- [x] **review.json** — 30 + 16 + 15 + 27 + 5 + 14 = 107 dispositions, each individually reasoned
      (all four inherited maps re-decided for 27; no generic copying; distinctness asserted)
- [x] **review.md**

## Verdict

**ACCEPT.** All required actions complete; no unresolved MUST or SHOULD. M-1, S-1, S-2, S-3 and
A-1/A-2/A-3 all resolved in 27. New: 0 MUST, 0 SHOULD, 3 advisories (A-4, A-5 inherited; A-6
package-only).

Grants no application grade, activation, blind acceptance or implementation authorization. 28
condition-2 obligations retained, 32 gates unperformed (condition 5 NOT MET), 54 recovery cases
unexecuted, D9 successor obligation carried forward, 30 residuals closed by nobody here.

## Failed probes, preserved honestly (all mine, none a design fault)

1. `pM1_boundaries.py` — wrong kwargs to `buffer_fact_batch_occupancy`; `public_observation` missing
   `diagnostic_bytes`. Two TypeErrors.
2. target-attribution fixture missing `packageManifestPath` → a refusal caused by my fixture.
3. `pK2` first run passed the membership wrapper where `admit_unit_roots` takes the unit list → all
   nine cases wrongly refused `units:not-a-list`.
4. `pK3` computed guard precedence against the *definition* line of `_unit_for_cell`, returning a
   wrong `False`; corrected in `pK4`.
5. `pP_handoff` selected the 185-char `standing` string over the 8-row `standingRules` list.
6. First `assess-author-query.py` invocation used `--source/--package` instead of `--input`; exit 2.
7. `pJ` regexes initially missed the F-12 and F-07 remedies, which are in README:9; corrected by
   reading the README rather than by widening the pattern.

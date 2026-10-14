# Review request: SM-RUST-SITE-CENSUS-r1, round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-rust-site-census-r2/`).

## Boundaries

Do not edit either repository, the stage, the producer directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store`;
- re-running the read-only audit: `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-rust-site-decomposition-2026-10-13/audit_sm_rust_site_census_r1.py`. It rewrites `site-census-checks-r1.json` in `/tmp/opensip-implementation/sm-rust-site-decomposition-2026-10-13`, and must reproduce it byte-for-byte.

## Round 2

Your round 1 (`/tmp/opensip-implementation/reviews/codex-sm-rust-site-census-r1/`) raised SM-SITE-R1-RF-01: the declaration aggregates summed the `.expanded` subset into its base. It also raised NBO-01: `extern crate` items carry a count only.
- **The audit.** It now excludes every `.expanded` key from the base relation totals and the per-subject distributions. It reports the expanded subset separately, for first-party and dependency crates.
- **The report.** It states the subset semantics and the `extern crate` wording.
- **What did not change.** The driver, the image, the runs, `site-census-r1.json` and the runner are byte-identical to round 1. Round 1's audit output is kept under `history/`.

Confirm the finding is resolved. Confirm also that the members shared with round 1's stage (`/tmp/opensip-implementation/sm-rust-site-census-r1-stage`) are unchanged, except for the audit, its output, the report and the freeze script.

## Subject

- Stage: `/tmp/opensip-implementation/sm-rust-site-census-r2-stage`
- `subject.json`: 3832 bytes, SHA-256 `c08a29106c1b8e223c22b8e7a8f88f32751456285b95911d0beb541c6b9fe612`, 16 members. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `4bb9e62e39ce99d21cc629369e3c04179e6529c1`.
- The authority is M3-L r6 item 9, "When SM-11 to SM-14 are filled" (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`; your review `codex-provider-protocol-l-r6`).

## What to review

1. **The variant.** `producer/driver.rs` must differ from the closed `producer/closed-driver-source.rs` only by the extern/mod lines, the named `TyCtxt`, and the one `site_walk::emit(tcx)` call placed after the closed timing event. Compare the closed source with `docs/implementation/m3/spikes/s-m-actual-framed-analysis-series-2026-10-10/closed-driver-source.rs`.
2. **The walk.** Read `producer/site_walk.rs`. Does each counted kind mean what `REPORT.md` says it means? Are sites never presented as candidates? Is the attribution of macro-expanded sites correct?
3. **The build.** `build.json` and the build logs: the closed recipe, the pinned sysroot, and the image pin. The image must equal `compiled-image/site-driver`.
4. **The runner.** `run_sm_rust_site_census_r1.py`:
   - it uses the unchanged closed executor and observer, which it pin-checks against the series' committed copies;
   - it runs two times per entry;
   - it checks the population against the accepted pilots;
   - it checks determinism;
   - it holds the lane.

   Check `site-census-r1.json` for consistency: 354 compiler children, populations and determinism.
5. **The audit.** Re-run it. Check:
   - the subject recipe, and that S matches RUST3-LIM's recorded counts;
   - the overlay S;
   - the store-byte equality of mapped subjects;
   - the separation of first-party and dependency crates;
   - the label-only relation grouping, against NE:590-601;
   - that no quotient or value is derived.
6. **Scope.** Against item 9: nothing is invented, and no SM-11, SM-13 or SM-14 value or completeness is claimed. The fixed byte overheads are explicitly not supplied here.

Product, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed, and only L-G1 remains open. Native admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "c08a29106c1b8e223c22b8e7a8f88f32751456285b95911d0beb541c6b9fe612",
  "roundOneFindingResolved": true,
  "expandedSubsetsNotAddedToBase": true,
  "closedDriverOnlyVariantDiff": true,
  "closedExecutorObserverUnchanged": true,
  "compilerChildren": 354,
  "allPopulationsRepeated": true,
  "allSiteCountsDeterministic": true,
  "subjectCountsMatchRust3Lim": true,
  "workloadsWithExactCoverage": 0,
  "sitesLabelledNotCandidates": true,
  "ownedParametersChosen": false,
  "SM11QuotientsDerived": false,
  "SM13ValueDerived": false,
  "SM14ValueDerived": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.

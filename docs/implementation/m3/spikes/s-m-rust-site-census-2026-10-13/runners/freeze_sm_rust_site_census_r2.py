from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze the outside-product S-M Rust site census r1 (S-M-round input to M3-L r6 item 9's SM-11/SM-13/SM-14 decomposition) for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-rust-site-decomposition-2026-10-13'; S = B / 'sm-rust-site-census-r2-stage'; Q = B / 'reviews/codex-sm-rust-site-census-r2'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-rust-site-census-2026-10-13'
assert not S.exists() and not Q.exists()
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): out = S / PREFIX / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, out); assert pin(out) == pin(src)
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
build = json.loads((W / 'producer/build.json').read_text()); census = json.loads((W / 'site-census-r1.json').read_text()); checks = json.loads((W / 'site-census-checks-r1.json').read_text())
assert pin(build['executable']) == {k: build[k] for k in ['bytes', 'sha256']} and census['wrapperPin']['sha256'] == build['sha256']
closed = A / 'docs/implementation/m3/spikes/s-m-actual-framed-analysis-series-2026-10-10'
assert (W / 'producer/closed-driver-source.rs').read_bytes() == (closed / 'closed-driver-source.rs').read_bytes()
# Re-run the read-only audit and require byte-identical output.
out = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(W / 'audit_sm_rust_site_census_r1.py')], capture_output=True, text=True); assert out.returncode == 0, out.stderr
assert json.loads((W / 'site-census-checks-r1.json').read_text()) == checks
assert all(r['rust3LimAgrees'] in (True, None) for r in checks['workloads']) and checks['workloadsWithExactCoverage'] == [] and checks['allPopulationsRepeated'] and checks['allSiteCountsDeterministic']
assert all(r['firstPartySitesOutsideSubjects'] == [] for r in checks['workloads'])
for n in ['driver.rs', 'site_walk.rs', 'closed-driver-source.rs', 'build_site_driver_r1.py', 'build.json', 'build.log', 'sha-build.log']: cp(W / 'producer' / n, 'producer/' + n)
cp(build['executable'], 'compiled-image/site-driver')
for n in ['run_sm_rust_site_census_r1.py', 'audit_sm_rust_site_census_r1.py', 'site-census-r1.json', 'site-census-checks-r1.json', 'census-run.log']: cp(W / n, n)
cp(B / 'freeze_sm_rust_site_census_r2.py', 'runners/freeze_sm_rust_site_census_r2.py'); cp(W / 'site-census-checks-r1-round1.json', 'history/site-census-checks-r1-round1.json')
rows = checks['workloads']
table = '\n'.join(f"| {r['ordinal']} | {r['id']} | {r['subjectCountS']} | {r['rust3LimRecordedS'] if r['rust3LimRecordedS'] is not None else 'no row'} | {r['firstPartySubjectsWithSites']} | {r['units']['firstPartyAnalysed']} / {r['units']['firstPartyUnavailable']} | {r['units']['dependencyAnalysed']} |" for r in rows)
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M Rust site census r1

This is an outside-product experiment. It supplies the S-M round's inputs to M3-L r6 item 9 ("When SM-11 to SM-14 are filled"). It produces no SM-11, SM-13 or SM-14 value.

## What ran

- **The driver.** It is a variant of the closed framed driver (`s-m-actual-framed-analysis-series-2026-10-10/closed-driver-source.rs`, `43315ea6…`). `producer/driver.rs` differs from the closed source in exactly three places:
  - an `extern crate rustc_hir;` and `mod site_walk;` pair;
  - `after_analysis` names its `TyCtxt`;
  - one `site_walk::emit(tcx);` call, placed after the closed `after_analysis` timing event, so the closed interval excludes the walk.
- **The walk.** The new module `producer/site_walk.rs` counts compiler **sites** per source file of the local crate:
  - local definitions by `DefKind`;
  - `use` items, with their resolution categories, and `extern crate` items, as a count only;
  - expressions, and expressions with a type in typeck results;
  - call and method-call sites, with their resolution, and method receivers that are trait objects or type parameters;
  - path expressions and paths, with resolution;
  - field expressions, closures and bodies.

  Macro-expanded sites count at their call site, in their base kind. They are **also** counted in a `<kind>.expanded` key, which is a subset of the base kind and never added to it.
- **The build.** It uses the closed recipe: bare rustc from the pinned 1.95 rustc-dev sysroot, at nice 10 under the lane lock. The image is `{build['sha256'][:8]}…`, {build['bytes']} bytes, at `compiled-image/site-driver`.
- **The runs.** The unchanged closed graph executor and root observer ran over the nine accepted prepared entries of the framed analysis series. Each entry ran twice, for {census['compilerChildren']} compiler children in all. Every unit's standing repeated the accepted pilot population: `allPopulationsRepeated` {checks['allPopulationsRepeated']}. Site counts were identical across both runs: `allSiteCountsDeterministic` {checks['allSiteCountsDeterministic']}. No timing statistic is claimed.

## What the audit derives

`audit_sm_rust_site_census_r1.py` is read-only. Its output is `site-census-checks-r1.json`.

- **Subject counts.** It computes the subject count S by RUST3-LIM's recipe: non-empty regular `.rs` blobs of the verified T2 store tree, with overlays taken by mount. For every repository with a row, S equals RUST3-LIM's recorded count. The overlay `mr-rs-medium-serde-json`, which has no row, gets S = 279 (208 + 71).
- **Subject mapping.** Every first-party site file is mapped to a subject, and its bytes must equal the store file. No first-party site falls outside a subject.
- **Dependency crates.** Sites in dependency crates are reported separately. They are not workload subjects.
- **Relation grouping.** Site kinds are grouped by the relation@rung they are **offered for** (NE:590-601, M3L-R6-NBO-01). The grouping is a label, not an emission recipe. Base totals exclude every `.expanded` key. The macro-expanded subset is reported separately per relation (`...ExpandedSubsetByRelation`).
- **Round 2 (Codex SM-SITE-R1-RF-01).** Round 1's audit summed the `.expanded` subset into the declaration totals, because the `def.` prefix matched both keys. Round 2 corrects only that derived aggregation. The driver, runs and raw observations are unchanged. Round 1's audit output is kept as `history/site-census-checks-r1-round1.json`.

| Ord | Workload | S | RUST3-LIM S | Subjects with sites | First-party units analysed / unavailable | Dependency units analysed |
|---|---|---|---|---|---|---|
{table}

## What this does not supply

- **Coverage.** No workload has exact coverage. Most first-party code sits in units that the closed executor marks unavailable before launch: build scripts, proc macros, non-library targets, and their dependants. So, under item 9's rule, no SM-11 per-subject quotient is derived.
- **Owned parameters.** No stage, requested key, emission factor, census symbol kind or batching is chosen. These parameters remain with their owners: G3 for emission, census kinds and batching, and C4a for stages and keys.
- **Fixed byte overheads.** This unit does not supply the fixed overheads for SM-13 (b) to (e), and it states no SM-13 or SM-14 value.
- **Scratch.** No scratch is measured.
- **Scope.** There is no native admission or product change. Full S-M is not complete, L-G1 is not met, L is not in effect, and nothing is qualified.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-RUST-SITE-CENSUS-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], roundOneFindingResolved=True, expandedSubsetsNotAddedToBase=True, closedDriverOnlyVariantDiff=True, closedExecutorObserverUnchanged=True, compilerChildren=census['compilerChildren'],
                allPopulationsRepeated=True, allSiteCountsDeterministic=True, subjectCountsMatchRust3Lim=True, workloadsWithExactCoverage=0, sitesLabelledNotCandidates=True,
                ownedParametersChosen=False, SM11QuotientsDerived=False, SM13ValueDerived=False, SM14ValueDerived=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-RUST-SITE-CENSUS-r1, round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the producer directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store`;
- re-running the read-only audit: `nice -n 10 python3 -I -B {W}/audit_sm_rust_site_census_r1.py`. It rewrites `site-census-checks-r1.json` in `{W}`, and must reproduce it byte-for-byte.

## Round 2

Your round 1 (`/tmp/opensip-implementation/reviews/codex-sm-rust-site-census-r1/`) raised SM-SITE-R1-RF-01: the declaration aggregates summed the `.expanded` subset into its base. It also raised NBO-01: `extern crate` items carry a count only.
- **The audit.** It now excludes every `.expanded` key from the base relation totals and the per-subject distributions. It reports the expanded subset separately, for first-party and dependency crates.
- **The report.** It states the subset semantics and the `extern crate` wording.
- **What did not change.** The driver, the image, the runs, `site-census-r1.json` and the runner are byte-identical to round 1. Round 1's audit output is kept under `history/`.

Confirm the finding is resolved. Confirm also that the members shared with round 1's stage (`/tmp/opensip-implementation/sm-rust-site-census-r1-stage`) are unchanged, except for the audit, its output, the report and the freeze script.

## Subject

- Stage: `{S}`
- `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- Bases: product `{git(P, 'rev-parse', 'HEAD')}` (clean), architecture `{git(A, 'rev-parse', 'HEAD')}`.
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

   Check `site-census-r1.json` for consistency: {census['compilerChildren']} compiler children, populations and determinism.
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
{json.dumps(expected, indent=2)}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of SM-RUST-SITE-CENSUS-r1.'); st['SMRustSiteCensusFrozenSubject'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

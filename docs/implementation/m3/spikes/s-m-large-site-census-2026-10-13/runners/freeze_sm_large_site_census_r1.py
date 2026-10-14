from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze U-7 (S-M report plan PLAN-r2): large-workload site census (Smithy and Deno analysed entries, site-walk v2 image,
# unchanged closed framed-bin executor) and the declared-entry coverage desk record for all four large workloads, for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-large-site-census-2026-10-13'; S = B / 'sm-large-site-census-r1-stage'; Q = B / 'reviews/codex-sm-large-site-census-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-large-site-census-2026-10-13'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
before = (W / 'large-site-census-checks-r1.json').read_bytes()
r = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(W / 'audit_sm_large_site_census_r1.py')], capture_output=True, text=True); assert r.returncode == 0, r.stderr
assert (W / 'large-site-census-checks-r1.json').read_bytes() == before
checks = json.loads(before); census = json.loads((W / 'large-site-census-r1.json').read_text())
assert census['compilerChildren'] == 976 and checks['allPopulationsRepeated'] and checks['allSiteCountsDeterministic'] and checks['workloadsWithExactCoverage'] == []
for n in ['run_sm_large_site_census_r1.py', 'audit_sm_large_site_census_r1.py', 'large-site-census-r1.json', 'large-site-census-checks-r1.json', 'large-census-run.log', 'large-workload-entry-coverage.md']: cp(W / n, n)
cp(Path(__file__), 'runners/freeze_sm_large_site_census_r1.py')
rows = checks['workloads']
rel = ['declares@syntactic', 'imports@resolved-target', 'references@resolved-binding', 'calls@resolved-callee', 'types@checked', 'unresolved-edge@observed', 'clones@normalized-body-hash', 'literal@syntactic', 'control-flow@syntactic']
t = '\n'.join(f"| {w['id']} | {len(w['entries'])} | {w['subjectCountS']} | {w['firstPartySubjectsWithSites']} | {w['units']['firstPartyAnalysed']} / {w['units']['firstPartyUnavailable']} | {w['units']['dependencyAnalysed']} | " + ' | '.join(str(w['firstPartySitesOfferedByRelation'][k]) for k in rel) + ' |' for w in rows)
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M large-workload site census and declared-entry coverage (U-7)

This is an outside-product experiment and desk record, unit U-7 of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`, §3a). It supplies the S-M round's SM-11 and SM-13 inputs for the large Rust workloads of M3-L r6 item 9 (PROPOSAL-r6:571, :586-591): smithy-rs, rspack and deno, and sui if S-P permits. It produces no SM-11, SM-13 or SM-14 value.

## Declared-entry coverage (desk)

`large-workload-entry-coverage.md` gives, for every one of the 33 original declared Cargo workspace entries, its final accepted outcome with citations: **12 analysed** (smithy-rs 10, deno 2) and **21 unavailable** (smithy-rs 15, deno 1, rspack 2, sui 3). Reasons, verbatim from the accepted records:
- smithy-rs: 7 generated or path inputs absent from the pinned tree, 5 lock refusals under `--locked`, 2 descriptors over the closed driver's 4 MiB bound (`rust-runtime` 5,115,131 bytes; `canary-runner` 6,596,209 bytes), 1 local package-name mismatch;
- deno: the root descriptor 22,825,382 bytes over the bound;
- rspack: both entries refused by the pinned stable compiler because the original configuration passes nightly-only `-Z` flags;
- sui: two Git dependencies that cannot be checked out offline, and a bin target whose source is a symlink the no-follow copy excludes.

No lock, bound, flag or tree was changed to make an entry available. PLAN-r2 §3a listed `rust-runtime` but not `canary-runner` among the over-bound entries; this record adds it from H9 REPORT:3.

## Census of the analysed entries

- **What ran.** The accepted site-walk v2 image (U-3, `codex-sm-rust-site-census-v2-r2`) as the wrapper, through the unchanged closed framed-bin executor (pins from `sm-framed-bin-profile-controls-r1-stage/source.json`, checked before every graph), over the prepared entries of the five accepted large-workload framed series (Smithy fuzz, Smithy http-fuzz, Smithy r11 hierarchy, Deno bin, Deno SQLite short paths): 12 entries, twice each, {census['compilerChildren']} compiler children. The series' own driver source is the closed framed driver (`43315ea6…`) of which v2 is the accepted variant.
- **Checks.** Every run repeated its accepted pilot's unit population (`allPopulationsRepeated` {checks['allPopulationsRepeated']}), and site counts were identical across runs (`allSiteCountsDeterministic` {checks['allSiteCountsDeterministic']}). No timing statistic is claimed.
- **Audit.** `audit_sm_large_site_census_r1.py` (derived from the accepted U-3 audit) computes S by RUST3-LIM's recipe over the verified T2 store, maps first-party site files to store-identical subjects across all of a workload's entries, keeps dependency crates apart, and groups site kinds by relation@rung as a label only.

| Workload | Entries | S | Subjects with sites | First-party units analysed / unavailable | Dependency units analysed | declares | imports | references | calls | types | unresolved-edge | clones body | literal | control-flow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{t}

Coverage is far from exact: smithy-rs {rows[0]['firstPartySubjectsWithSites']} of {rows[0]['subjectCountS']} subjects, deno {rows[1]['firstPartySubjectsWithSites']} of {rows[1]['subjectCountS']}. Almost all analysed units are dependency crates. rspack and sui have no analysed entry. So no SM-11 quotient is recorded for any large workload, as item 9 requires (:587).

## Standing

Sites are not candidates. No stage, key, emission factor, census kind or batching is chosen; no SM-11, SM-13 or SM-14 value. No native admission or product change. L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-LARGE-SITE-CENSUS-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], declaredEntries=33, analysedEntries=12, unavailableEntries=21, entryReasonsAccurate=True,
                closedExecutorUnchanged=True, acceptedSiteWalkV2ImageUsed=True, compilerChildren=976, allPopulationsRepeated=True, allSiteCountsDeterministic=True, subjectCountsMatchRust3Lim=True,
                workloadsWithExactCoverage=0, sitesLabelledNotCandidates=True, ownedParametersChosen=False, SM11QuotientsDerived=False, SM13ValueDerived=False, SM14ValueDerived=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-LARGE-SITE-CENSUS-r1 (U-7)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store` and the prepared inputs under `/tmp/opensip-implementation/sm-framed-bin-profile-2026-10-10`;
- re-running the read-only audit `nice -n 10 python3 -I -B {W}/audit_sm_large_site_census_r1.py`, which must reproduce `large-site-census-checks-r1.json` byte for byte.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.** PLAN-r2 §3a and U-7 (your `codex-s-m-report-plan-r2`); M3-L r6 item 9 (PROPOSAL-r6:571, :586-591); the accepted U-3 census v2 (`codex-sm-rust-site-census-v2-r2`) and the five accepted large-workload framed series.

## What to review

1. **Entry coverage.** Check `large-workload-entry-coverage.md` against `s-m-actual-large-workspace-data-r1-2026-10-10/census/original-workspace-entries-r1.json` (33 entries) and the cited receipts and REPORT lines. Spot-check at least one entry per reason class and every rspack and sui entry. Is any outcome or reason wrong or missing?
2. **The runner.** It must use the accepted v2 image as the wrapper and the unchanged closed executor (pins checked), run each pilot entry twice, and check pilot population repetition and determinism. Check `large-site-census-r1.json` (976 children).
3. **The audit.** Re-run it. Check the S recipe and RUST3-LIM agreement (1,084 and 1,052), the subject mapping and store-byte equality, the dependency separation, and the label-only grouping. Confirm no quotient or value.
4. **Scope.** Nothing invented; no owned parameter; unavailable coverage preserved exactly; no SM-11, SM-13 or SM-14 value.

O7, D3 and D13 are closed, and only L-G1 remains open. Native admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{json.dumps(expected, indent=2)}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of SM-LARGE-SITE-CENSUS-r1 (U-7).'); st['SMLargeSiteCensusFrozenSubject'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

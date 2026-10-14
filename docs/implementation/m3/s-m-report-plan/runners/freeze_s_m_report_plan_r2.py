from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Round-2 freeze of the S-M report plan (PLAN-r2 for Codex SM-REPORT-PLAN-R1-RF-01/-RF-02/-NBO-01; PLAN-r1 retained) (lead plan record: definitions S-M's report fixes under M3-L r6 item 9, and units owed) for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 's-m-report-plan-2026-10-13'; S = B / 's-m-report-plan-r1-stage'; Q = B / 'reviews/codex-s-m-report-plan-r2'; R1 = B / 'reviews/codex-s-m-report-plan-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/s-m-report-plan'
assert not Q.exists() and json.loads((R1 / 'review.json').read_text())['verdict'] == 'REQUIRED-FINDINGS'
if S.exists(): S.rename(B / 's-m-report-plan-r1-stage-round1')
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] in (None, str(R1))
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
assert not (A / PREFIX).exists()
for n in ['PLAN-r1.md', 'PLAN-r2.md', 'make_plan_r2.py', 'gap-inventory-2026-10-13.md']: out = S / PREFIX / n; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / n, out)
out = S / PREFIX / 'runners/freeze_s_m_report_plan_r2.py'; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(Path(__file__), out); shutil.copyfile(B / 's-m-report-plan-r1-stage-round1/docs/implementation/m3/s-m-report-plan/runners/freeze_s_m_report_plan_r1.py', S / PREFIX / 'runners/freeze_s_m_report_plan_r1.py')
r1sub = json.loads((B / 's-m-report-plan-r1-stage-round1/subject.json').read_text())
for f in r1sub['files']: assert hashlib.sha256((S / f['path']).read_bytes()).hexdigest() == f['sha256'], f['path']
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='S-M-REPORT-PLAN-r1', round=2, productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], round1FindingsResolved=True, plan1RetainedUnchanged=True, largeWorkloadsCovered=True, D9NoExtrapolatedTerm=True, definitionsWithinItem9Authority=True, citationsAccurate=True,
                D1SyntheticSizeRuleLawful=True, D1NotPresentedAsBound=True, D2MatchesContractDefinition=True, ownedParametersChosen=False,
                placeholderFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: S-M-REPORT-PLAN-r1, round 2

This is round 2. Round 1 (`{R1}`) returned REQUIRED-FINDINGS on `SM-REPORT-PLAN-R1-RF-01` and `-RF-02`, with `-NBO-01`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests, any driver or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only file reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `{S}`
- `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- Bases: product `{git(P, 'rev-parse', 'HEAD')}` (clean), architecture `{git(A, 'rev-parse', 'HEAD')}`.
- The record under review is `{PREFIX}/PLAN-r2.md`. `PLAN-r1.md` (your round-1 subject, unchanged) and `make_plan_r2.py` (the exact r1-to-r2 edit) are beside it. The gap inventory beside it is a research aid, not under review for its derived numbers; the plan must cite accepted records for anything it relies on.

## Context

M3-L r6 item 9 (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`, about :540-:630) lists S-M's figures and says "Unless S-M's report fixes it otherwise" (:548). This plan is the lead's record of the definitions S-M's report fixes (D-1 to D-9), with reasons and rejected alternatives, and the measurement units still owed (U-1 to U-6). It follows your round-1 finding `SM-REPLAY-SIZED-R1-RF-01` (`docs/implementation/m3/reviews/codex-sm-replay-sized-r1/`): D-1 keeps the replay series as definition-bound synthetic SM-9 under item 9's own "Synthetic and labelled" wording, not as a bound on real replay.

## What to review

0. **Round-1 findings.** Are RF-01, RF-02 and NBO-01 resolved by PLAN-r2's changes table, D-9, §3a with U-7, and D-1? Is PLAN-r1.md byte-identical to the round-1 subject? Are §3a's figures and citations accurate?
1. **Authority.** Is each definition within what item 9 leaves to S-M's report, and does none choose a parameter that a later unit owns (G3 emission, census kinds, batching; C4a stages and keys; PROPOSAL-r6:627)?
2. **D-1.** Is the size rule (one fact, finding and fingerprint per analysed source: TS distinct configured files, express 141 roots, Rust S) a lawful reading of :563 "of the size SM-2 and SM-4 imply. Synthetic and labelled"? Is the label adequate, and is it consistent with your round-1 finding? Is the narrowing of the control-state correction accurate?
3. **D-2.** Check the dependency-source set against `docs/v2/contracts/product-v1/native-evidence.md` (NE:612, :1687, :1693-1694, :1706-1707, :2863-2864), `snapshot-plan-c/ds4-p1-r1/CONTRACT.md:5`, `snapshot-plan-c/PROPOSAL-r7.md:600` and the cited spikes. Is the conclusion that the accepted Rust map transfers are not SM-7 correct?
4. **D-3 to D-9.** Are the reasons sound and the cited lines accurate (`harness/DESIGN.md` §9.2; the cited spike REPORT lines)? Is anything that over- or under-states a figure labelled as such?
5. **Units.** Are U-1 to U-6 sufficient for S-M's report under D-1..D-9, and is U-1 a new variant rather than a modification of a closed executor?
6. **Scope.** No placeholder filled, no F, T or outcome, no change to L or to any closed piece or accepted record.

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

The lead will give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex round-2 review of S-M-REPORT-PLAN-r1.'); st['SMReportPlanFrozenSubjectRound2'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

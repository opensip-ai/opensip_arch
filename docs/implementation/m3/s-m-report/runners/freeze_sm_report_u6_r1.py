from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze the S-M report (U-6) for Codex.
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u6'); S = B / 'sm-report-u6-r1-stage'; Q = B / 'reviews/codex-sm-report-u6-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; PREFIX = 'docs/implementation/m3/s-m-report'
assert not S.exists() and not Q.exists() and not (A / PREFIX).exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == ''
for n in ['S-M-REPORT.md', 'sm-report-data.json', 'assemble_sm_report.py', 'render_sm_report.py', 'assemble.log']: cp(W / n, n)
cp(Path(__file__), 'runners/freeze_sm_report_u6_r1.py')
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-REPORT-U6-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], everyFigureAtItsStanding=True, definitionsD1toD9Applied=True, componentStatisticsRecomputedFromRaw=True, correctSourcesPerRowAndReset=True,
                FTPerItem9AndD3D4=True, targetsAndOutcomeRulesCorrect=True, everyHoldingOutcomeRecorded=True, D1ConditionalityAndSensitivitiesStated=True, largeWorkloadsMatrixAccurate=True,
                placeholderFilled=False, LChanged=False, ownerQuestionsRaisedHere=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-REPORT-U6-r1 (the S-M report, U-6)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading, Git queries and in-memory archive reading. You may also read the index-pinned working copies the assembler names:
- U-1's series under `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/`;
- U-5b's SM-4 result under `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b/sm4/`.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - M3-L r6 item 9 (`provider-protocol-l/PROPOSAL-r6.md`): figures, workloads, statistic, "Derived figures", outcomes (A) to (C), and the SM-11 to SM-14 two-part rule.
  - The S-M report plan r3 (`s-m-report-plan/PLAN-r3.md`), D-1 to D-9 and §3a.
  - The analysis-quality plan's targets (`analysis-quality/PLAN.md` §5.2 table and §5.3 decision).
  - Every accepted S-M record the data pins: SM-1/SM-3 ready, cohort, synthesized, typed sealing, transfer, replay sized, static-profile, SM-6, rust-scope, sui-scope, census v2, U-1, U-2c, U-4a, U-4b, U-5a, U-5b and U-7.

## What to review

1. **Figures.**
   - Is each SM-1 to SM-14 at its accepted standing, with the correct source per row and reset?
   - Are the component statistics recomputed correctly from raw runs (median and max of the 7 measured)?
   - Are D-3 (R8 entry sums; SM-3 twice; SM-9 once), D-4 (express synthesized; the start over-count stated) and D-5 (U-1 for the changed rows; static-profile for hyper) applied?
2. **F, T and outcomes.**
   - Are F and T as item 9 defines them, as sums of component medians, with the sums of maxima beside?
   - Are the targets and outcome rules right? (B) is warm F > 2 s; (C) is cold T > 30 s or warm T > 8 s; (A) is neither.
   - Is every holding outcome recorded, with D-1 conditionality, preliminary standing and the sensitivities stated (without SM-9, without the double-counted start, sums of maxima) and not substituted?
3. **Other figures and §3a.** Are SM-6, SM-8, SM-10, SM-11 (no quotient), SM-12, SM-13 (decomposition only), SM-14 (formula), S_eff (first term only) and the large-workload matrix accurate to their records?
4. **Scope.**
   - Is it true that no placeholder is filled, L is unchanged, and no owner question is raised here (that is the delta round's)?
   - Are full S-M, L-G1 and effective L left open?

O7, D3 and D13 are closed, and only L-G1 remains open.

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
write(Q / 'status.json', dict(unit='SM-REPORT-U6-r1', reviewer='codex', pane='w5:p1', subject=sp, state='prepared'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files)), indent=1))

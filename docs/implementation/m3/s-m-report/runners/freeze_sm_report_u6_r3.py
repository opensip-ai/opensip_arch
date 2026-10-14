from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze ROUND 3 of the S-M report (U-6) for Codex (SM-U6-R2-RF-01 complete SM-14 subject map; NBO-01 entry counts).
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u6'); S = B / 'sm-report-u6-r3-stage'; Q = B / 'reviews/codex-sm-report-u6-r3'; S1 = B / 'sm-report-u6-r1-stage'; Q1 = B / 'reviews/codex-sm-report-u6-r1'; S2 = B / 'sm-report-u6-r2-stage'; Q2 = B / 'reviews/codex-sm-report-u6-r2'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; PREFIX = 'docs/implementation/m3/s-m-report'
assert not S.exists() and not Q.exists() and not (A / PREFIX).exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == ''
r1v = json.loads((Q1 / 'review.json').read_text()); assert r1v['verdict'] == 'REQUIRED-FINDINGS' and [f['id'] for f in r1v['requiredFindings']] == ['SM-U6-R1-RF-01', 'SM-U6-R1-RF-02']
r2v = json.loads((Q2 / 'review.json').read_text()); assert r2v['verdict'] == 'REQUIRED-FINDINGS' and [f['id'] for f in r2v['requiredFindings']] == ['SM-U6-R2-RF-01']
for n in ['S-M-REPORT.md', 'sm-report-data.json', 'assemble_sm_report.py', 'render_sm_report.py', 'assemble.log']: cp(W / n, n)
for a, b in [('S-M-REPORT-r1.md', 'round1-S-M-REPORT.md'), ('sm-report-data-r1.json', 'round1-sm-report-data.json'), ('assemble_sm_report_r1.py', 'round1-assemble_sm_report.py'), ('render_sm_report_r1.py', 'round1-render_sm_report.py')]: cp(W / a, 'history/' + b)
assert (S / PREFIX / 'history/round1-S-M-REPORT.md').read_bytes() == (S1 / PREFIX / 'S-M-REPORT.md').read_bytes() and (S / PREFIX / 'history/round1-sm-report-data.json').read_bytes() == (S1 / PREFIX / 'sm-report-data.json').read_bytes()
cp(S1 / 'subject.json', 'history/round1-subject.json')
for a, b in [('S-M-REPORT-r2.md', 'round2-S-M-REPORT.md'), ('sm-report-data-r2.json', 'round2-sm-report-data.json'), ('assemble_sm_report-r2.py', 'round2-assemble_sm_report.py'), ('render_sm_report-r2.py', 'round2-render_sm_report.py')]: cp(W / a, 'history/' + b)
assert (S / PREFIX / 'history/round2-S-M-REPORT.md').read_bytes() == (S2 / PREFIX / 'S-M-REPORT.md').read_bytes() and (S / PREFIX / 'history/round2-sm-report-data.json').read_bytes() == (S2 / PREFIX / 'sm-report-data.json').read_bytes()
cp(S2 / 'subject.json', 'history/round2-subject.json')
cp(Path(__file__), 'runners/freeze_sm_report_u6_r3.py'); cp(B / 'freeze_sm_report_u6_r1.py', 'runners/freeze_sm_report_u6_r1.py'); cp(B / 'freeze_sm_report_u6_r2.py', 'runners/freeze_sm_report_u6_r2.py')
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-REPORT-U6-r3', round=3, productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], r2rf01SM14SubjectMapComplete=True, rf01AllFiguresPinnedAndRenderedFromData=True, rf02SM5PopulationsAndSM12MaxRssCarried=True, timingFTOutcomesUnchangedFromRound1=True, everyFigureAtItsStanding=True, definitionsD1toD9Applied=True, componentStatisticsRecomputedFromRaw=True, correctSourcesPerRowAndReset=True,
                FTPerItem9AndD3D4=True, targetsAndOutcomeRulesCorrect=True, everyHoldingOutcomeRecorded=True, D1ConditionalityAndSensitivitiesStated=True, largeWorkloadsMatrixAccurate=True,
                placeholderFilled=False, LChanged=False, ownerQuestionsRaisedHere=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-REPORT-U6-r3 (the S-M report, U-6, round 3)

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

## Round 3

Round 2 (`{Q2}`, your REQUIRED-FINDINGS) raised SM-U6-R2-RF-01: SM-14's subject-count map lacked rspack and Sui. It also raised NBO-01, on the entry lists printed in the large-workload table. Confirm:
- **RF-01.** `otherFigures.SM14.S` now holds all 12 workloads, built from the SM-12 subject-count records. The assembler asserts complete coverage and equality with every census count, and Sui's conditional standing is kept.
- **NBO-01.** The large-workload table renders entry counts.
- **Unchanged.** Everything else in `otherFigures`, and the timing components, F, T and outcomes, equal round 2's.
- **History.** The round-2 report, data, scripts and subject are kept under `history/`.

## Round 2 (resolved; recheck for consistency only)

Round 1 (`{Q1}`, your REQUIRED-FINDINGS) raised two findings: RF-01 on the unpinned other-figure sources, and RF-02 on the missing SM-5 populations and SM-12 maxima and peak RSS. Confirm:
- **RF-01.** `sm-report-data.json` → `otherFigures` materializes SM-5 populations, SM-6, SM-8, SM-10, SM-11, SM-12 (Sui included), SM-13 and SM-14, the S_eff first term and the large-workload matrix from pinned records (`pins`). The renderer reads only that file.
- **RF-02.** SM-5's per-row repository and dependency populations are given against their sourced bounds, with D-9's separate parts and no dependency-descriptor bound. SM-12's actor medians, maxima and peak RSS are given for every workload, Sui included, with the labels and pending fields stated.
- **Unchanged.** The timing components, F, T and outcomes equal round 1's.
- **History.** The round-1 report, data, scripts and subject are kept under `history/`.

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
write(Q / 'status.json', dict(unit='SM-REPORT-U6-r3', round=3, reviewer='codex', pane='w5:p1', subject=sp, state='prepared'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files)), indent=1))

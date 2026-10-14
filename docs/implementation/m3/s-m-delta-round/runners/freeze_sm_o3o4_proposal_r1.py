from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze the lead's O3/O4 owner-decision proposal (from the accepted S-M report) for Codex review before it goes to the owner.
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/sm-delta'); S = B / 'sm-o3o4-proposal-r1-stage'; Q = B / 'reviews/codex-sm-o3o4-proposal-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; PREFIX = 'docs/implementation/m3/s-m-delta-round'
assert not S.exists() and not Q.exists() and not (A / PREFIX).exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == ''
o = S / PREFIX / 'O3-O4-PROPOSAL-r1.md'; o.parent.mkdir(parents=True); shutil.copyfile(W / 'O3-O4-PROPOSAL-r1.md', o)
o = S / PREFIX / 'runners/freeze_sm_o3o4_proposal_r1.py'; o.parent.mkdir(parents=True); shutil.copyfile(Path(__file__), o)
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-O3-O4-PROPOSAL-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], factsMatchAcceptedReport=True, optionsMatchLText=True, recommendationsReasonedAndNotImposed=True, deltaRoundSequenceCorrect=True, reviewerSubstitutionRecorded=True,
                ownerDecisionRecorded=False, ownerAssentInferred=False, placeholderFilled=False, LChanged=False, LG1Met=False, effectiveL=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-O3-O4-PROPOSAL-r1 (lead proposal for owner questions O3 and O4)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run anything. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only file reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - M3-L r6 (`provider-protocol-l/PROPOSAL-r6.md`): item 9's outcomes and "What the S-M delta round records"; "Open questions" O3 and O4; "What reopens it" (trigger 1, and the r6 reviewer rule); "What depends on O7, S-M, FA-2 and RUST3-LIM".
  - The accepted S-M report (`docs/implementation/m3/s-m-report/`, your `codex-sm-report-u6-r3` ACCEPT) and its `sm-report-data.json`.
  - The analysis-quality plan (`analysis-quality/PLAN.md` §5.2 and §5.3; AQP:372).

## What to review

This proposal goes to the owner, who decides. Review it for accuracy and fitness, not for the owner's choice.
1. **Facts.** Does every number and statement in §1 match the accepted report and its data? Recompute the "without SM-9" figures, the cold and warm misses, the SM-9 growth, and the warm-fixture note against AQP §5.2's column label and D-7.
2. **Options.** Do O3-a and O3-b, and O4-a to O4-c, match L's O3 and O4 text? Is O4-a a legitimate answer to "whether to revisit the budgets or the staging" (a revisit that keeps both, with a re-test gate)? Are no values invented for O4-b?
3. **Recommendations.** Are they reasoned from the evidence, with D-1 conditionality and preliminary standing respected, and not presented as decided?
4. **Sequence.** Is §4 correct: the owner's answers, then the S-M delta round (r7) carrying them; Codex as the owner-named substitute reviewer under L's r6 rule; L-G1 met on acceptance; no protocol change?
5. **Scope.** Is it true that no owner decision is recorded or inferred, no placeholder is filled and L is unchanged?

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{json.dumps(expected, indent=2)}
```

After an ACCEPT, the lead publishes the proposal (architecture only) and puts O3 and O4 to the owner. Nothing is pushed.
""")
write(Q / 'status.json', dict(unit='SM-O3-O4-PROPOSAL-r1', reviewer='codex', pane='w5:p1', subject=sp, state='prepared'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files)), indent=1))

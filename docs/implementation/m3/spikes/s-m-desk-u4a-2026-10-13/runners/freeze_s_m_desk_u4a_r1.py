from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze the S-M desk record U-4a (SM-8 under D-6, S_eff first term under D-9) for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 's-m-desk-u4a-2026-10-13'; S = B / 's-m-desk-u4a-r1-stage'; Q = B / 'reviews/codex-s-m-desk-u4a-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-desk-u4a-2026-10-13'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
before = (W / 'u4a-desk-records.json').read_bytes()
out = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(W / 'derive_u4a.py')], capture_output=True, text=True); assert out.returncode == 0, out.stderr
assert (W / 'u4a-desk-records.json').read_bytes() == before
for n in ['derive_u4a.py', 'u4a-desk-records.json', 'REPORT.md']: o = S / PREFIX / n; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / n, o)
o = S / PREFIX / 'runners/freeze_s_m_desk_u4a_r1.py'; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(Path(__file__), o)
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='S-M-DESK-U4A-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], derivationReproduces=True, sm8FollowsD6=True, sm8Rows=6, sEffFirstTermFollowsD9=True, sEffRows=12,
                noExtrapolatedCeiling=True, placeholderFilled=False, SEffFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: S-M-DESK-U4A-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, Node, tests, any driver or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing and Git queries;
- re-running the read-only derivation `nice -n 10 python3 -I -B {W}/derive_u4a.py`. It rewrites `u4a-desk-records.json` in `{W}` and must reproduce it byte for byte.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.** The accepted S-M report plan, `docs/implementation/m3/s-m-report-plan/PLAN-r2.md` (your `codex-s-m-report-plan-r2` ACCEPT): D-6, D-9 and U-4. U-4 is split, and the report states the split.

## What to review

1. **SM-8.** Does the derivation apply D-6 exactly? Check:
   - it reads only measured runs, ordinals 3-9;
   - it reads the correct committed evidence files;
   - the maximum covers every configuration's retained calls, incomplete configurations included;
   - the per-configuration cross-check holds;
   - express uses the synthesized program.

   Spot-check at least two rows by hand. Is the granularity label adequate?
2. **S_eff's first term.** Are the values copied exactly from the accepted sealing `checks.json` files for all 12 Rust workloads? Check the bound standing. Confirm that no ceiling is extrapolated and that the D-2 dependency part is marked owed.
3. **Split and scope.** Is the U-4a/U-4b split sound? Confirm that no placeholder, S_eff, F, T or outcome is recorded.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of S-M-DESK-U4A-r1.'); st['SMDeskU4aFrozenSubject'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

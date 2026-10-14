from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze U-5a (S-M report plan PLAN-r2, D-7): the Q0 §9.2 cold-reset series over the TS-row F and T components, for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-cold-ts-2026-10-13'; S = B / 'sm-cold-ts-r1-stage'; Q = B / 'reviews/codex-sm-cold-ts-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache')
CTL = C / 'control-2026-10-06'; SP = A / 'docs/implementation/m3/spikes'
PREFIX = 'docs/implementation/m3/spikes/s-m-cold-ts-2026-10-13'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
before = (W / 'cold-ts-checks.json').read_bytes()
r = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(W / 'audit_cold_ts.py')], capture_output=True, text=True); assert r.returncode == 0, r.stderr
assert (W / 'cold-ts-checks.json').read_bytes() == before; checks = json.loads(before); assert checks['allDiffsConfined']
# Bulky raw evidence (cohort evidence/, sealing per-run stdout and inputs) goes into one deterministic LFS-tracked archive.
def bulky(rel): return rel.startswith('cohort/evidence/') or (rel.startswith('sealing/') and (rel.endswith('.stdout') or rel.endswith('-input.json')))
members = []; plain = []
for p in sorted(W.rglob('*')):
    if not p.is_file(): continue
    rel = p.relative_to(W).as_posix()
    (members if bulky(rel) else plain).append((rel, p))
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for rel, p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(rel); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(raw))
out = S / PREFIX / 'raw-evidence.tar.xz'; out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(lzma.compress(buf.getvalue(), preset=9)); assert out.stat().st_size < 100 * 2**20
write(S / PREFIX / 'raw-evidence-index.json', dict(archive='raw-evidence.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=rel, **pin(p)) for rel, p in members]))
for rel, p in plain:
    o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, o)
o = S / PREFIX / 'runners/freeze_sm_cold_ts_r1.py'; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(Path(__file__), o)
assert not [p for p in S.rglob('*') if p.is_file() and p.stat().st_size > 100 * 2**20]
# Accepted warm values, information only.
def warm():
    w = {}
    w['SM-1'] = json.loads((SP / 's-m-sm1-ready-closure-2026-10-09/results.json').read_text())['medianStartToReadyNanos']
    for x in json.loads((SP / 's-m-sealing-typed-2026-10-09/checks.json').read_text())['workloads']: w[('sealing', x['id'])] = x['medianNanos']
    for x in json.loads((SP / 's-m-transfer-2026-10-09/results.json').read_text())['workloads']: w[('transfer', x['id'])] = x['medianTransferNanos']
    for x in json.loads((SP / 's-m-ts-cohort-2026-10-09/results.json').read_text())['workloads']: w[('cohort', x['id'])] = x['medianWholeProcessNanos']
    for x in json.loads((SP / 's-m-ts-synthesized-2026-10-10/results.json').read_text())['workloads']: w[('synthesized', x['id'])] = x['medianWholeProcessNanos']
    for x in json.loads((SP / 's-m-replay-sized-2026-10-13/sized-replay-results-r2.json').read_text())['sets']: w[('replay', f"replay-{x['count']}")] = x['medianReplayNanos']
    return w
WARM = warm(); lines = []
for name, c in checks['components'].items():
    for s in c['series']:
        k = 'SM-1' if name == 'sm1' else (name, s['workload']); wv = WARM.get(k)
        lines.append(f"| {name} | {s['workload']} | {s['medianNanos'] / 1e6:.3f} | {s['maxNanos'] / 1e6:.3f} | {wv / 1e6:.3f} |" if wv else f"| {name} | {s['workload']} | {s['medianNanos'] / 1e6:.3f} | {s['maxNanos'] / 1e6:.3f} | n/a |")
table = '\n'.join(lines)
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M cold-reset series for the TS-row components (U-5a)

This is an outside-product measurement, unit U-5a of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`, D-7 and U-5). It applies Q0 §9.2's **cold** reset (`harness/DESIGN.md:798-801`) to every F and T component of the six TS rows:
- SM-1 (TS start);
- SM-5 sealing (all 13 read sets, Rust repository-only parts included);
- SM-7 transfer (repository-only sets);
- SM-2 (the configuration cohort, and the express synthesized program under D-4);
- SM-9 at the six TS row sizes under D-1 (141, 193, 678, 936, 1,159, 1,381).

The Rust rows' cold series (U-5b) follow U-1 and U-2, which change Rust SM-4, SM-5 and SM-7. This unit fills no placeholder, computes no F or T and records no outcome.

## The cold reset

`cold_reset.py` runs before **every** run, warmups included, as the first statement of each runner's measured loop and before any timestamp, so no reset work is timed. It does three things:
1. **OpenSIP state.** It deletes the project's OpenSIP state. None is ever created: `Application Support/OpenSIP` is asserted absent.
2. **Disposable caches.** It replaces them with a fresh, empty, private 0700 per-run TMPDIR under the set's TMPDIR, deleting the previous run's first.
3. **Page cache.** It records the OS page-cache state with `vm_stat`: raw output, page size, and file-backed, purgeable and free pages. The page cache is never claimed flushed.

The caller then starts a new process. The label is **"cold OpenSIP state, page cache recorded"**. `cold-reset-records.json` in each component directory holds one record per child, in order.

## The runners

`build_cold_runners.py` copies each accepted runner byte for byte into its own directory, so its outputs never overwrite accepted evidence. It makes only these insertions:
- the `cold_reset` import;
- one `_cr.reset(env,T)` as the first statement of the single measured loop;
- `_cr.write(...)` before the lane is released.

The replay variant also restricts its sizes to the six TS row sizes and redirects its outputs. `ACCEPTED-RUNNER-SOURCE` names each accepted runner. The audit checks every diff (`allDiffsConfined` {checks['allDiffsConfined']}).

Recipes are otherwise unchanged: 3 warmups and 7 measured runs, the lane held, priority 10, and the accepted inputs and pins.

**First sealing attempt.** It omitted the probe's sibling `control-template.json`, so its first child exited before any measurement. It is retained as `sealing-attempt0-missing-control-template/` and `run_all-attempt0.log`. The rebuild copies the file; nothing else changed.

## Results (lead macOS, preliminary, not D12; ms)

Accepted warm medians are shown for information only; no ratio or claim is drawn.

| Component | Workload | Cold median | Cold max | Accepted warm median |
|---|---|---:|---:|---:|
{table}

**Evidence.** Bulky raw evidence (the cohort's per-run evidence, and sealing's per-run outputs and inputs) is in `raw-evidence.tar.xz`; `raw-evidence-index.json` pins every member.

## Standing

- **Host and label.** Lead macOS host, preliminary, not D12. The page cache was never flushed, only recorded.
- **Values.** No F, T, outcome or placeholder.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-COLD-TS-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], coldResetMatchesQ0=True, resetBeforeEveryRunUntimed=True, allDiffsConfined=True, oneResetRecordPerChild=True,
                pageCacheRecordedNotFlushed=True, recipesOtherwiseUnchanged=True, attempt0Retained=True, archiveMatchesIndex=True, FComputed=False, TComputed=False, outcomeRecorded=False,
                placeholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-COLD-TS-r1 (U-5a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Node, the compiler, Cargo, any runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing and Git queries;
- reading the archive members without extracting them to a shared location;
- re-running the read-only audit `nice -n 10 python3 -I -B {W}/audit_cold_ts.py`, which must reproduce `cold-ts-checks.json` byte for byte.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - PLAN-r2, D-7 and U-5 (your `codex-s-m-report-plan-r2`).
  - Q0 §9.2 (`docs/implementation/m3/harness/DESIGN.md:796-807`).
  - The accepted component spikes named in each `ACCEPTED-RUNNER-SOURCE`.

## What to review

1. **The reset.**
   - Does `cold_reset.py` implement §9.2's cold reset: OpenSIP state deleted or absent, disposable caches deleted, a new process, and the page-cache state recorded and never claimed flushed?
   - Is the fresh per-run TMPDIR a sound reading of "the disposable analyzer caches"?
2. **Placement.**
   - In every cold runner, is the reset the first statement of the measured loop, before any timestamp?
   - Is it called once per child, warmups included?
   - Is the transfer control launch outside the loop correctly left alone?
3. **The diffs.** Each cold runner against its accepted runner. Confirm:
   - only the stated insertions are present, plus the replay size restriction and output redirect;
   - no recipe, input, bound or pin is changed.
4. **Records and series.** Check:
   - one record per child, in order;
   - medians and maxima recomputed;
   - the replay children replay fully with `findings == count`;
   - the retained attempt 0 and its cause.
5. **The archive.** Members against `raw-evidence-index.json`.
6. **Scope.** No F, T, outcome or placeholder. The warm column is information only.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of SM-COLD-TS-r1 (U-5a).'); st['SMColdTsFrozenSubject'] = sp; write(CTL / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files), archive=pin(out)), indent=2))

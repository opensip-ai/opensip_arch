from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze U-5b (PLAN-r3 D-7, U-5: Q0 9.2 cold-reset series over the Rust-row F and T components) for Codex. Raw per-child
# evidence and the 37 MB SM-4 result go into raw-evidence.tar.xz (index pinned); everything else is copied as is.
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b'); S = B / 'sm-cold-rust-r1-stage'; Q = B / 'reviews/codex-sm-cold-rust-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06'); SP = A / 'docs/implementation/m3/spikes'
PREFIX = 'docs/implementation/m3/spikes/s-m-cold-rust-2026-10-14'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == ''
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
def raw_member(p):
    r = p.relative_to(W).as_posix()
    return 'evidence' in r.split('/')[1] if r.count('/') >= 2 else (r.startswith('sm3/') and (r.endswith('.stdout') or r.endswith('.stderr'))) or r == 'sm4/bsabsent-static-profile-series-cold-rust.json'
files = sorted(p for p in W.rglob('*') if p.is_file()); raw = [p for p in files if raw_member(p)]; plain = [p for p in files if not raw_member(p)]
for p in plain:
    o = S / PREFIX / p.relative_to(W); o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, o); assert pin(o) == pin(p)
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for p in raw:
        b = p.read_bytes(); info = tarfile.TarInfo(p.relative_to(W).as_posix()); info.size = len(b); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(b))
out = S / PREFIX / 'raw-evidence.tar.xz'; out.write_bytes(lzma.compress(buf.getvalue(), preset=9))
write(S / PREFIX / 'raw-evidence-index.json', dict(archive='raw-evidence.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=p.relative_to(W).as_posix(), **pin(p)) for p in raw]))
o = S / PREFIX / 'runners/freeze_sm_cold_rust_r1.py'; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(Path(__file__), o)
ck = json.loads((W / 'cold-rust-checks.json').read_text()); c = ck['components']; ms = lambda v: f'{v / 1e6:.3f}'
NAMES = {'sm3': 'SM-3', 'replay': 'SM-9 (D-1)', 'sm4': 'SM-4', 'sm5': 'SM-5', 'sm7': 'SM-7'}
table = '\n'.join(f"| {NAMES[n]} | `{s['workload']}` | {ms(s['medianNanos'])} | {ms(s['maxNanos'])} | {ms(s['warmMedianNanos'])} |" for n in ['sm3', 'sm5', 'sm7', 'replay', 'sm4'] for s in c[n]['series'])
r8 = ck['R8TwoEntryChildren']
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M cold-reset series for the Rust-row components (U-5b)

This is an outside-product measurement, unit U-5b of the accepted S-M report plan r3 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`, D-7 and U-5). It applies Q0 §9.2's **cold** reset (`harness/DESIGN.md:798-801`) to every F and T component of the eight Rust rows (item 9: F = SM-3 + SM-5 + SM-7 + SM-9; T = F + SM-4):
- **SM-3:** Rust start.
- **SM-5:** two parts in one span (the U-2c r2 runner).
- **SM-7:** with every NE §9.2 dependency field (the U-2c r3 runner).
- **SM-9:** at the eight Rust row sizes under D-1 (71, 98, 192, 208, 239, 279, 301, 808). These are synthetic source-count scenarios with no real-workload bound.
- **SM-4:** the U-1 static-profile whole graph with build-script outputs absent, the series D-5 assigns to the rows U-1 changes.

U-5a (`s-m-cold-ts-2026-10-13`) covered the TS rows. This unit fills no placeholder, computes no F or T and records no outcome.

## The cold reset

`cold_reset.py` is U-5a's accepted file, byte for byte. Before **every** run, warmups included, as the first statement of the measured loop and before any timestamp, it does three things:
1. **OpenSIP state.** It checks that the project's OpenSIP state is absent; none is ever created.
2. **Disposable caches.** It replaces them with a fresh, empty, private 0700 per-run TMPDIR under the set's TMPDIR, deleting the previous run's first.
3. **Page cache.** It records the OS page-cache state with `vm_stat`. The page cache is never claimed flushed.

The label is **"cold OpenSIP state, page cache recorded"**. Each component directory's `cold-reset-records.json` holds one record per child, in order.

**SM-4 note.** The compiler children run with their constructed command environment and inherit no TMPDIR, so the per-run TMPDIR is the parent runner's only. Every run already writes a fresh output root. For SM-4, the reset therefore contributes the state-absent check and the page-cache record.

## The runners

`build_cold_rust_runners.py` copies each accepted runner byte for byte into its own directory, with U-5a's insertions only:
- the `cold_reset` import;
- one reset as the first statement of the single measured loop;
- `_cr.write(...)` before the lane is released.

There are two runner-specific redirections, each asserted:
- **SM-4.** The runner (U-1's `run_bsabsent_static_profile_series_r1.py`) has no `env`/`T` in its loop. The reset takes a placeholder dict and the series root, and the result goes to this directory.
- **Replay.** It is restricted to the eight Rust sizes, and its outputs go to this directory.

The SM-5 and SM-7 sources are the **published** U-2c runners (`codex-sm-u2c-r2` ACCEPT). `ACCEPTED-RUNNER-SOURCE` names each source and its hash. The audit checks every diff (`allDiffsConfined` {ck['allDiffsConfined']}).

Recipes are otherwise unchanged: 3 warmups and 7 measured runs, the lane held, priority 10, and the accepted inputs and pins. A read-only preflight confirmed, before any run, that every pinned input under `/tmp` was intact after the 2026-10-14 temp cleanup (`LD-WORKDIR-TMP-EROSION`).

## Results (lead macOS, preliminary, not D12; ms)

The warm medians (accepted SM-3, replay r2, U-1, and U-2c SM-5 r2 and SM-7 r3) are shown for information only. No ratio or claim is drawn.

| Figure | Workload | Cold median | Cold max | Warm median |
|---|---|---:|---:|---:|
{table}

**Controls carried by the runners.**
- **SM-4.** Every entry's population, read sets and metadata repeat across its ten runs, and its analysed and incomplete units and new analyses equal U-1's.
- **SM-5.** Every child's repository part reproduces the accepted typed shape, and every shape equals U-2c's.
- **SM-7.** Snapshot manifests, dependency manifests and seals equal U-2c's. The positive control passes and all 20 refusal controls refuse.
- **Replay.** Every replay passes, with one finding per source.

**R8 (`mr-rs-medium-serde-json`), two entry children (D-3).** Medians summed and maxima summed:
- SM-4: {ms(r8['SM4']['medianSumNanos'])} / {ms(r8['SM4']['maxSumNanos'])};
- SM-5: {ms(r8['SM5']['medianSumNanos'])} / {ms(r8['SM5']['maxSumNanos'])};
- SM-7: {ms(r8['SM7']['medianSumNanos'])} / {ms(r8['SM7']['maxSumNanos'])}.

## Current interpretation

Each copied runner writes its accepted runner's `standing` text verbatim into its result, including the replay runner's withdrawn lower-bound wording. U-5a's round-1 finding covered exactly this. `cold-rust-interpretation.json` is the current interpretation for all five components:
- **Label.** Each is labelled "cold OpenSIP state, page cache recorded".
- **Inherited text.** The inherited `standing` is marked obsolete.
- **Replay.** It carries `SM9LowerBoundOnly=false` and the D-1 synthetic label.

The audit (`audit_cold_rust.py`, read-only, output `cold-rust-checks.json`) requires that record.

## Evidence

All raw child records are in `raw-evidence.tar.xz`, with its index pinned. They are the SM-3 child stdout/stderr, the replay, SM-5 and SM-7 evidence directories, and the 37 MB SM-4 result. The run logs are `run_all-1.log` and `run_all-2.log`, with each component's `run.log`.

## Standing

- **What this is.** Cold-reset inputs for the S-M report (U-6).
- **What it is not.** No F, T or outcome is computed, and no placeholder is filled.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-COLD-RUST-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], coldResetModuleEqualsU5a=True, allDiffsConfined=True, oneResetRecordPerChild=True, pageCacheRecordedNeverClaimedFlushed=True,
                sm5Sm7FromPublishedU2c=True, controlsReproduceWarmPopulations=True, statisticsRecomputed=True, r8TwoEntryChildrenSums=True, currentInterpretationRecorded=True, replayNotALowerBound=True,
                FComputed=False, TComputed=False, outcomeRecorded=False, placeholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-COLD-RUST-r1 (U-5b: Rust-row cold-reset series)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries; reading the archive in memory or extracting it into a fresh directory under your own temporary space; reading the working directory `{W}` and the accepted runners each `ACCEPTED-RUNNER-SOURCE` names, including U-1's warm series at `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json` (pinned in U-1's `large-records-index.json`).

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - S-M report plan r3: D-7 (`PLAN-r3.md:102-106`), U-5 (`:126`), D-1, D-3 and D-5.
  - Item 9's F and T (`provider-protocol-l/PROPOSAL-r6.md`, "Derived figures").
  - U-5a (`s-m-cold-ts-2026-10-13`, your accepted round 2: the method, `cold_reset.py`, and the inherited-standing interpretation rule).
  - U-1 (`s-m-u1-build-script-outputs-absent-2026-10-13`), the replay sized series (`s-m-replay-sized-2026-10-13`), SM-3 (`s-m-sm3-ready-2026-10-09`) and U-2c (`codex-sm-u2c-r2`).

## What to review

1. **Method.**
   - Is `cold_reset.py` byte-equal to U-5a's?
   - Does each cold runner differ from its accepted runner only by the import, one reset as the first statement of the measured loop (before any timestamp), the write before lane release, and the declared SM-4 and replay redirections?
   - Are the SM-5 and SM-7 sources the published U-2c runners (SM-7 r3)?
   - Is the SM-4 note on TMPDIR and child environments accurate?
2. **Records.** Is there one reset record per child, in order, with state absent, a fresh empty per-run TMPDIR and a recorded page cache, and no flush claim?
3. **Controls.**
   - Do the SM-4 populations equal U-1's?
   - Do the SM-5 shapes and the SM-7 manifests and seals equal U-2c's, with the SM-7 controls present?
   - Do the replays pass, with one finding per source, at exactly the eight Rust sizes?
4. **Statistics.** Recompute medians, maxima and the R8 two-entry sums from the raw records, and check them against `cold-rust-checks.json` and `REPORT.md`. Are the warm figures informational only?
5. **Interpretation and scope.**
   - Does `cold-rust-interpretation.json` correctly supersede each inherited `standing`, with the replay's D-1 synthetic label and no lower bound?
   - Is it true that no F, T, outcome, placeholder fill or gate claim is made?

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
write(Q / 'status.json', dict(unit='SM-COLD-RUST-r1', reviewer='codex', pane='w5:p1', subject=sp, state='prepared'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files), raw=len(raw), review=str(Q)), indent=1))

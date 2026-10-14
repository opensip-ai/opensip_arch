from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze U-1 (S-M report plan) together with the PLAN-r3 D-5 delta it needs, for Codex.
B = Path('/tmp/opensip-implementation'); V = B / 'sm-command-data-bsabsent-2026-10-13'; PL = B / 's-m-report-plan-2026-10-13'
S = B / 'sm-u1-r1-stage'; Q = B / 'reviews/codex-sm-u1-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-u1-build-script-outputs-absent-2026-10-13'; PLAN = 'docs/implementation/m3/s-m-report-plan'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel, prefix=PREFIX): o = S / prefix / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
assert not (A / PLAN / 'PLAN-r3.md').exists()
before = (V / 'u1-checks-r1.json').read_bytes()
r = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(V / 'audit_u1_r1.py')], capture_output=True, text=True); assert r.returncode == 0, r.stderr
assert (V / 'u1-checks-r1.json').read_bytes() == before; checks = json.loads(before)
# PLAN-r3 delta beside the accepted r1/r2.
for n in ['PLAN-r3.md', 'make_plan_r3.py']: cp(PL / n, n, PLAN)
# Producer variant: the two changed files, their accepted parents, controls.
cp(V / 'producer/src/cargo/core/compiler/experimental_command_data.rs', 'producer-variant/src/cargo/core/compiler/experimental_command_data.rs')
cp(V / 'producer/src/cargo/util/context/experimental_command_data.rs', 'producer-variant/src/cargo/util/context/experimental_command_data.rs')
cp(V / 'parent-experimental_command_data.rs', 'producer-variant/parent/compiler-experimental_command_data.rs'); cp(V / 'parent-util-context-experimental_command_data.rs', 'producer-variant/parent/util-context-experimental_command_data.rs')
for n in ['run_bsabsent_controls_r1.py', 'command-data-bsabsent-controls-r1.log', 'command-data-bsabsent-checks-r1.json', 'variant-image.json']: cp(V / n, 'producer-variant/' + n)
# Collection, maps (index archived), executor variants, series, audit.
for n in ['prepare_bsabsent_packets_r1.py', 'bsabsent-command-data-packets-r1.json', 'run_bsabsent_command_data_attempts_r1.py', 'bsabsent-command-data-attempts-r1.json', 'bsabsent-command-data-attempts-r1-progress.json', 'attempts-run.log',
          'prepare_bsabsent_source_maps_r1.py', 'cargo_lint_spelling_graph_execution_bsabsent.py', 'framed_profile_graph_execution_bsabsent.py',
          'run_bsabsent_static_profile_series_r1.py', 'attempt0-run_bsabsent_static_profile_series_r1.py', 'sp-series-run.log', 'sp-series-run-attempt0-no-instrumented-interval.log',
          'run_bsabsent_framed_series_r1.py', 'series-run.log', 'audit_u1_r1.py', 'u1-checks-r1.json']: cp(V / n, n)
att = json.loads((V / 'bsabsent-command-data-attempts-r1.json').read_text())
for rr in att['results']:
    cp(rr['unitCommandData']['path'], f"collection/{rr['ordinal']}/unit-command-data.json"); cp(rr['graph']['path'], f"collection/{rr['ordinal']}/unit-graph.json")
big = ['bsabsent-command-source-maps-r1.json', 'bsabsent-static-profile-series-r1.json', 'bsabsent-framed-series-r1.json']
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for n in big:
        raw = (V / n).read_bytes(); info = tarfile.TarInfo(n); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(raw))
out = S / PREFIX / 'large-records.tar.xz'; out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(lzma.compress(buf.getvalue(), preset=9)); assert out.stat().st_size < 100 * 2**20
write(S / PREFIX / 'large-records-index.json', dict(archive='large-records.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=n, **pin(V / n)) for n in big]))
cp(Path(__file__), 'runners/freeze_sm_u1_r1.py')
rows = checks['series']
t = '\n'.join(f"| {r['ordinal']} | {r['id']} | {len(r['newlyConstructedCommands'])} | {r['analysedUnits']} | {r['incompleteUnits']} | {', '.join(u['name'] for u in r['newlyAnalysed'] if u['firstParty']) or '—'} | {r['medianWholeGraphMs']:.1f} | {r['maxWholeGraphMs']:.1f} | {r['acceptedStaticProfileMedianMs']:.1f} |" for r in rows)
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M U-1: SM-4 coverage with build-script outputs absent

This is an outside-product experiment, unit U-1 of the S-M report plan. It runs with the PLAN-r3 delta to D-5 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`), which is submitted with this unit. Item 9 says no build script or proc-macro runs, and the expansion that depends on them is disclosed as unavailable (PROPOSAL-r6:558). U-1 analyses what can be analysed under that rule, preserves what cannot, and fills no SM-4 value.

## What blocked the build-script-only libraries

The block was not in an executor. The accepted static command-data producer spreads unavailability through every dependency edge. For axum, serde and serde_json, every blocker is a build-script unit, and Cargo's static `prepare_rustc` never reads build-script outputs; only `OUT_DIR` is set statically.

## The variants

None of these modifies an accepted piece.

### Producer variant (`producer-variant/`)

- **Clone.** A copy-on-write clone of the accepted producer, with exactly two files changed (the audit checks every other file).
- **`compiler/experimental_command_data.rs`.**
  - Unavailability does not spread through build-script units (custom-build targets and run-custom-build units); every other block is unchanged.
  - A unit constructed only because of this keeps Cargo's own `prepare_rustc` command, with `OUT_DIR` and `*_OUT_DIR` removed and recorded in `removedEnvironmentKeys`.
  - Its standing is `actual-static-cargo-command-data-build-script-outputs-absent`.
- **`util/context/experimental_command_data.rs`.** It only adds the control `command_data_build_script_only_consumer_constructed_with_outputs_absent`.
- **Controls.** All four `command_data_` controls pass (`run_bsabsent_controls_r1.py`, the accepted check recipe).
- **Image.** The variant test image is pinned in `variant-image.json`. It is 78 MB and is not staged; it is retained at its path, and the accepted image is unchanged.

### Collection and maps

- **Packets.** Fresh packets come from the accepted packet recipe, with only the destination changed.
- **Collection.** Collection over the nine entries succeeded. Each graph equals the accepted graph once the packet root is normalised.
- **Unchanged commands.** Every command the accepted producer constructed is unchanged, once packet roots and producer image paths are normalised.
- **New commands.** The new commands are exactly the units blocked only through build scripts (`collection/`, `u1-checks-r1.json`).
- **Maps.** Source maps were rebuilt with the accepted recipe for the new roots. File counts and bytes equal the accepted maps.

### Executor variants

- **Static-profile variant.** `cargo_lint_spelling_graph_execution_bsabsent.py` is the accepted static-profile executor, with build-script edges excluded from launch, blocking, externs and `-L`, and a per-unit `buildScriptOutputsAbsent` flag. Build-script units stay unavailable and never run.
- **Framed variant.** `framed_profile_graph_execution_bsabsent.py` applies the same change to the framed executor.

## Series (lead macOS, preliminary, not D12)

**Static-profile path (the SM-4 series under PLAN-r3 D-5).** `run_bsabsent_static_profile_series_r1.py` runs the closed static-profile driver (`c8cde6df…`) through the variant: 3 warmups and 7 measured runs per entry, lane held, priority 10. The audit checks:
- populations, read sets and metadata repeat across the ten runs;
- every unit the accepted series analysed is still analysed.

| Ord | Workload | New commands | Analysed units | Incomplete units | New first-party analysed | Whole-graph median ms | max ms | Accepted static-profile median ms |
|---|---|---:|---:|---:|---|---:|---:|---:|
{t}

**Why first-party coverage barely moves.** Most newly launched first-party libraries end incomplete, as item 9 requires them to be preserved:
- **`serde_core`** stops at `include!(concat!(env!("OUT_DIR"), "/private.rs"))`. The file its build script generates is unavailable, so every dependant stays incomplete, including `axum`, `axum_extra`, `serde` and `serde_json`.
- **`serde_derive_internals`** reads `src/mod.rs` outside the prepared map. That source path is not in the pinned regular-file tree.

The new first-party analyses are napi's `napi_sys` and `napi_derive_backend`. Many dependency crates also become analysable (libc, mio, httparse and others), which raises whole-graph time.

**Metadata.** Metadata embeds each packet's registry root path (54 times in hyper's; the variant root is 9 bytes longer, matching the size difference). So byte equality with the accepted series is impossible by construction, and the control is population and repetition.

## Retained history

- **Framed-path run.** `run_bsabsent_framed_series_r1.py` and its records (in `large-records.tar.xz`) ran the framed executor variant first. Its whole graph is dominated by per-child map streaming (accepted napi 43,195.6 ms), which is why PLAN-r3 rejects it for SM-4.
- **Overlap during that run.** The lead's r79 status integration overlapped two of its napi **warmups**. Measured samples were unaffected, and none of it is used for SM-4.
- **First static-profile attempt.** It ran entry 0's ten graphs, then stopped because the plain driver reports no instrumented interval. Its runner copy and log are retained; the rerun treats that interval as absent.

## Standing

- **Execution.** No build script or proc-macro ran, and nothing was trimmed or rebounded.
- **Values.** No SM-4 value, F, T or outcome is recorded; the S-M report (U-6) takes these spans under D-5.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefixes=[PREFIX, PLAN], files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], planR3D5DeltaSound=True, producerVariantConfinedAndControlled=True, acceptedPiecesUnchanged=True,
                collectionEqualsAcceptedModuloRoots=True, newCommandsExactlyBuildScriptBlocked=True, executorVariantsConfined=True, seriesControlsHold=True, incompleteUnitsPreserved=True,
                noBuildScriptOrProcMacroExecuted=True, historyRetained=True, SM4ValueRecorded=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1 (U-1, with PLAN-r3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run Cargo, the compiler, any image, driver, runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading `{V}`, the accepted producer at `{B}/sm-command-data-2026-10-10`, the T2 store and the retained raw outputs named in the records;
- re-running the read-only audit `nice -n 10 python3 -I -B {V}/audit_u1_r1.py`, which must reproduce `u1-checks-r1.json` byte for byte.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - The accepted S-M report plan PLAN-r2 (your `codex-s-m-report-plan-r2`), and the PLAN-r3 delta (D-5 only) submitted here.
  - M3-L r6 item 9 (PROPOSAL-r6:558).
  - The accepted static-profile, framed and command-data series and controls named in the report.

## What to review

1. **PLAN-r3.** Is the D-5 change from the package-context series to the static-profile series sound? Check the ~1% agreement and the reasons. Is the corrected account of where the libraries were blocked accurate? Is the framed series rightly rejected for SM-4? Is everything else in PLAN-r2 unchanged (`make_plan_r3.py`)?
2. **Producer variant.**
   - Is the diff confined to the stated filter change, the OUT_DIR removal and the label, plus the one added control?
   - Is any other producer file changed?
   - Is the accepted producer and its image unchanged?
   - Do the controls pass?
   - Does the variant construct commands only with build-script outputs absent, and run no build script?
3. **Collection.**
   - Graphs equal the accepted ones modulo packet roots.
   - Previously constructed commands are unchanged modulo roots and image paths.
   - The new commands are exactly the build-script-blocked units, with OUT_DIR removed.
   - Maps equal the accepted file counts and bytes.
4. **Executor variants.** Are the diffs confined to excluding build-script edges and the flag?
5. **Series.**
   - Check the 3+7 shape, population, read-set and metadata repetition, and that previously analysed units are still analysed.
   - Is the explanation of the metadata hash difference (embedded packet root) correct?
   - Check the incomplete units and their exact causes (`serde_core` `env!("OUT_DIR")`; `serde_derive_internals` source outside the map).
   - Check the history disclosures, including the r79 overlap with framed-run warmups.
6. **Scope.** No build script or proc macro executed. No SM-4 value, F, T or outcome.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of U-1 with PLAN-r3.'); st['SMU1FrozenSubject'] = sp; write(CTL / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files), archive=pin(out)), indent=2))

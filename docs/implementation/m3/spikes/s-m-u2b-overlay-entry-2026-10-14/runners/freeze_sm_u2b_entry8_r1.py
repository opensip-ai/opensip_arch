from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze the U-2b entry-8 overlay unit: overlay-metadata variant of the accepted command-data producer, its build (vendor
# tree re-acquired after /tmp cleanup), controls, the overlay entry's resolution and DependencySourceSetV1 set, for Codex.
B = Path('/tmp/opensip-implementation'); V = B / 'sm-overlay-metadata-2026-10-14'; S = B / 'sm-u2b-entry8-r1-stage'; Q = B / 'reviews/codex-sm-u2b-entry8-r1'
WORK = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14'); P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-u2b-overlay-entry-2026-10-14'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
F = 'src/cargo/util/context/experimental_command_data.rs'; ACC = B / 'sm-command-data-2026-10-10/producer'
assert pin(V / 'parent-util-context-experimental_command_data.rs') == pin(ACC / F)
new = (V / 'producer' / F).read_text(); old = (ACC / F).read_text(); assert new.startswith(old) and '\nfn collect_explicit_experimental_overlay_metadata()' in new[len(old):]  # append-only variant
cp(V / 'producer' / F, 'variant/' + F); cp(V / 'parent-util-context-experimental_command_data.rs', 'variant/parent-experimental_command_data.rs')
for n in ['build_overlay_metadata_r1.py', 'build.log', 'build-attempt0-eroded-vendor.log', 'build.json', 'run_overlay_metadata_r1.py', 'overlay-metadata-runs-r1.json', 'u2b-metadata-attempts-entry8.json',
          'check_u2b_dependency_sources_entry8.py', 'u2b-source-audits-entry8.json', 'build_u2b_sets_entry8.py', 'u2b-sets-entry8.json']: cp(V / n, n)
cp(WORK / 'cargo-vendor.log', 'vendor/cargo-vendor.log')
vendor = WORK / 'cargo-producer-vendor'; rows = [dict(crate=d.name, checksumFile=pin(d / '.cargo-checksum.json')) for d in sorted(vendor.iterdir()) if d.is_dir()]
lost = sorted(p.name for p in (B / 'native-cargo-profile-source-2026-10-09/vendor').iterdir())
write(S / PREFIX / 'vendor/vendor-index.json', dict(standing='RE-ACQUIRED PRODUCER VENDOR TREE (cargo vendor --locked --versioned-dirs; checksums verified by Cargo against the producer Cargo.lock)', directory=str(vendor), crates=rows, sameCrateDirectoriesAsLostTree=[r['crate'] for r in rows] == lost, producerCargoLock=pin(V / 'producer/Cargo.lock')))
runs = json.loads((V / 'overlay-metadata-runs-r1.json').read_text())['runs']
for r in runs:
    root = Path(r['root'])
    for n in ['packet.json', 'metadata.json', 'stdout.log', 'stderr.log']: cp(root / n, f"runs/{r['label']}/{n}")
members = sorted(p for p in (V / 'u2b-sets' ).rglob('*') if p.is_file()) + sorted((V / 'u2b-source-audits').glob('*.json'))
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(p.relative_to(V).as_posix()); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(raw))
out = S / PREFIX / 'entry8-records.tar.xz'; out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(lzma.compress(buf.getvalue(), preset=9))
write(S / PREFIX / 'entry8-records-index.json', dict(archive='entry8-records.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=p.relative_to(V).as_posix(), **pin(p)) for p in members]))
sid = json.loads((V / 'u2b-sets-entry8.json').read_text())['sets'][0]
cp(Path(__file__), 'runners/freeze_sm_u2b_entry8_r1.py')
ctrl = {r['label']: r for r in runs}
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M U-2b overlay entry: `mr-rs-medium-serde-json` / `rs-medium-serde-json`

This is the follow-on to U-2b (accepted, `codex-sm-u2b-r1`), which left this entry pending. The entry's `serde_json` depends on `serde_core`. The T2 overlay links `serde`, `serde_core` and `serde_derive` to the sibling `rs-medium-serde` mount, and the accepted command-data producer applies those links as projected `patch.crates-io` paths. The accepted metadata harness takes no projected configuration, so it could not resolve this entry.

## Variant

- **What it is.** An append-only change to a copy-on-write clone of the accepted command-data producer (`variant/`; the audit asserts the accepted file is an exact prefix). The appended test `collect_explicit_experimental_overlay_metadata`:
  - applies the accepted overlay projection (`values`) and query context (`graph`);
  - then calls Cargo's `output_metadata` instead of building the unit graph, with dependencies included, filtered to `aarch64-apple-darwin`, and frozen, locked and offline as the accepted harness ran.
- **Execution.** Nothing compiles or executes.
- **Build.** The accepted controls recipe (`build_overlay_metadata_r1.py`): `cargo test --no-run --locked --offline`, vendored source, lane held. The image is `{json.loads((V / 'build.json').read_text())['sha256'][:8]}…`.
- **Vendor tree.** The first build failed because macOS `com.apple.tmp_cleaner` had emptied the accepted vendor tree under `/tmp` (all 507 crate directories; `build-attempt0-eroded-vendor.log`). It was re-acquired with `cargo vendor --locked --versioned-dirs` into the implementation cache: 507 crates, with exactly the lost tree's directory names, each verified by Cargo against the producer's `Cargo.lock` (`vendor/`; lead decision `LD-WORKDIR-TMP-EROSION`).

## Runs

Each observation root has a private home whose registry is a copy-on-write clone of template r117 (U-2a). The corpus copies are checked unchanged.

| Run | Overlay links | Exit | Packages | Registry | Equals the accepted harness |
|---|---|---|---:|---:|---|
| control A: `rs-medium-serde` | none | {ctrl['control-A-rs-medium-serde']['exitCode']} | {ctrl['control-A-rs-medium-serde']['packages']} | {ctrl['control-A-rs-medium-serde']['registryPackages']} | {ctrl['control-A-rs-medium-serde']['controlEqualsAcceptedHarness']} |
| control B: overlay `rs-medium-serde` | accepted | {ctrl['control-B-overlay-rs-medium-serde']['exitCode']} | {ctrl['control-B-overlay-rs-medium-serde']['packages']} | {ctrl['control-B-overlay-rs-medium-serde']['registryPackages']} | {ctrl['control-B-overlay-rs-medium-serde']['controlEqualsAcceptedHarness']} |
| target: overlay `rs-medium-serde-json` | accepted | {ctrl['target-overlay-rs-medium-serde-json']['exitCode']} | {ctrl['target-overlay-rs-medium-serde-json']['packages']} | {ctrl['target-overlay-rs-medium-serde-json']['registryPackages']} | — |

The controls compare package ids and the resolve graph (node ids, dependency edges and features) with U-2b's accepted-harness metadata. With the overlay applied, the target has three fewer registry packages than standalone serde-json (37), because the overlay supplies `serde`, `serde_core` and `serde_derive` as path packages, which stay in the snapshot (NE:1687).

## Set

The U-2b audit and set scripts (`*_entry8.py`; only input and output names changed) give:
- set `{sid['dependencySourceSetId']}`;
- {sid['registryPackages']} registry packages, {sid['regularFiles']} files and {sid['totalBytes']} bytes;
- reference model and product bridge in agreement;
- a generated lock, labelled a sizing stand-in (NE:1264), as in U-2b.

All set records are in `entry8-records.tar.xz` (index pinned). With this set, every Rust entry has a dependency-source set.

## Standing

- **Admission.** No source authentication, import admission or Plan.
- **Values.** No SM-5 or SM-7 value; those are U-2c's.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-U2B-OVERLAY-ENTRY-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], variantAppendOnlyAndConfined=True, vendorReacquisitionLockedAndDisclosed=True, controlsEqualAcceptedHarness=True,
                overlayProjectionAsAccepted=True, setBuiltWithAcceptedScripts=True, referenceAndBridgeAgree=True, generatedLockLabelled=True, sourceAuthentication=False, importAdmission=False,
                SM5ValueRecorded=False, SM7ValueRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-U2B-OVERLAY-ENTRY-r1 (U-2b follow-on)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run Cargo, any image, runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries, including `{V}`, `{WORK}`, the accepted producer at `{ACC}`, and U-2b's records under `{B}/sm-dependency-source-sets-2026-10-14`.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.** U-2b (your `codex-sm-u2b-r1` ACCEPT, which left this entry pending); the accepted command-data producer and its overlay projection; D-2 and D-3 of the S-M report plan r3; and `LD-WORKDIR-TMP-EROSION`.

## What to review

1. **Variant.**
   - Is it append-only to the accepted file, with the accepted overlay projection and query context reused?
   - Does it set frozen, locked and offline as the accepted harness does?
   - Does it use `output_metadata` with dependencies and the platform filter?
   - Does nothing compile or execute?
2. **Build and vendor.**
   - Is the re-acquisition sound, locked and checksum-verified?
   - Do the directory names equal the lost tree's?
   - Is the cause disclosed?
3. **Controls.** Recompute both controls against U-2b's accepted harness metadata. Is the comparison adequate (package ids, nodes, edges and features)?
4. **Target and set.**
   - Is the overlay applied exactly as the accepted plans give it, with manifest pins checked?
   - Is the corpus unchanged?
   - Are the set scripts derived by names only?
   - Spot-check the set identity with the reference model.
5. **Scope.** No admission, SM-5 or SM-7 value.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of U-2b overlay entry.'); st['SMU2bEntry8FrozenSubject'] = sp; write(CTL / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

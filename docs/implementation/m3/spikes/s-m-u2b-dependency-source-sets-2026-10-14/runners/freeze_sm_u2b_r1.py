from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze U-2b (S-M report plan r3, D-2 / U-2): DependencySourceSetV1 sets for the Rust rows from template r117, axum control.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-dependency-source-sets-2026-10-14'; S = B / 'sm-u2b-r1-stage'; Q = B / 'reviews/codex-sm-u2b-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-u2b-dependency-source-sets-2026-10-14'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
sets = json.loads((W / 'u2b-sets.json').read_text())['sets']; ax = [s for s in sets if s['entry'] == 'rs-medium-axum'][0]
assert ax['axumControl'] == dict(descriptorByteEqualAccepted=True, setIdEqualAccepted=True, packageKeysEqualAccepted=True, fileManifestsByteEqualAccepted=187)
for n in ['build_u2b_receipts_r1.py', 'u2b-receipts.json', 'run_u2b_resolved_metadata_r1.py', 'u2b-metadata-attempts-r1.json', 'run_u2b_resolved_metadata_overlay_r2.py', 'u2b-metadata-attempts-overlay-r2.json',
          'check_u2b_dependency_sources_r1.py', 'u2b-source-audits.json', 'build_u2b_sets_r1.py', 'u2b-sets.json']: cp(W / n, n)
for n in ['Cargo.toml', 'Cargo.lock', 'src/main.rs', 'build_hash_bridge_r1.py', 'build.log', 'build.json']: cp(W / 'hash-bridge' / n, 'hash-bridge/' + n)
for s in sets:
    if s['built']:
        for n in ['descriptor.json', 'observations.json', 'unified-features.json']: cp(W / 'u2b-sets' / s['slug'] / n, f"sets/{s['slug']}/{n}")
for n in ['mr-rs-medium-serde-json__rs-medium-serde-json.stdout', 'mr-rs-medium-serde-json__rs-medium-serde-json.stderr']:
    cp(W / 'u2b-metadata' / n, 'pending-entry-8/attempt1-' + n); cp(W / 'u2b-metadata-overlay-r2' / n, 'pending-entry-8/attempt2-' + n)
members = sorted(p for d in ['u2b-receipts', 'u2b-metadata', 'u2b-metadata-overlay-r2', 'u2b-source-audits', 'u2b-sets'] for p in (W / d).rglob('*') if p.is_file())
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(p.relative_to(W).as_posix()); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(raw))
out = S / PREFIX / 'u2b-records.tar.xz'; out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(lzma.compress(buf.getvalue(), preset=9)); assert out.stat().st_size < 100 * 2**20
write(S / PREFIX / 'u2b-records-index.json', dict(archive='u2b-records.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=p.relative_to(W).as_posix(), **pin(p)) for p in members]))
cp(Path(__file__), 'runners/freeze_sm_u2b_r1.py')
rows = '\n'.join(f"| {s['entry']} | {'built' if s['built'] else 'pending'} | {s.get('dependencySourceSetId', '—')[:23] + ('…' if s.get('built') else '')} | {s.get('registryPackages', '—')} | {s.get('regularFiles', '—')} | {s.get('totalBytes', '—')} | {'original' if s.get('lockIsOriginal') else ('generated (experimental)' if s.get('built') else '—')} |" for s in sets)
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M U-2b: Rust dependency-source sets

This is an outside-product data unit, the second part of U-2 in the S-M report plan r3. Under D-2, SM-5 and SM-7 take the Rust dependency-source set as the contracts' `DependencySourceSetV1`: the activated, admitted, non-path packages of the lock, for the target (NE:612, NE:1693-1694; DS4-P1). This unit builds that set for every Rust medium entry from the U-2a template r117, with axum, whose set was accepted earlier, carried through as the control.

## Pipeline

1. **Receipts** (`build_u2b_receipts_r1.py`).
   - **Source.** Built only from template r117. Each package's archive must match its lock checksum.
   - **Index lines.** Decoded byte for byte from r117's stock Cargo `.cache` files (format: `0x03`, index version 2, `Unknown`, then version and JSON-line pairs). Every locked version and checksum must be present.
   - **Lock sources.** Only crates.io sources occur; path packages stay in the snapshot (NE:1687).
2. **Resolved metadata** (`run_u2b_resolved_metadata_r1.py`).
   - **Recipe.** The accepted `run_axum_resolved_metadata.py` recipe, looped over the entries: the accepted harness image `45816163…` (its pin was checked), offline, frozen and locked, with dependencies included and filtered to `aarch64-apple-darwin`.
   - **Controls.** A private Cargo home seeded only from the receipt, and the corpus copy checked unchanged.
   - **Axum control.** It resolves 191 packages, 187 from crates.io, the accepted counts.
3. **Source audit** (`check_u2b_dependency_sources_r1.py`). The accepted audit, looped: every extracted tree equals its archive. Axum gives 187 packages and 7,338 files.
4. **Keys, features, manifests, descriptor** (`build_u2b_sets_r1.py`).
   - **Steps 5 and 7.** The accepted recipes, generalised.
   - **Step 6, reconstructed.** Its accepted script was not retained, so it is rewritten with the accepted format (sorted `[{{path, contentSha256, byteLength}}]`).
   - **Identities.** Every identity is computed by the reference model and by the product bridge, rebuilt from the accepted `hash_bridge.rs` source against the current `opensip-identity` (`hash-bridge/`). The two agree everywhere.
   - **Axum control.**
     - The rebuilt bridge first reproduced the accepted set `879ff234…` and unified features `7dfdb8a1…`.
     - The pipeline reproduces the accepted package keys, all **187 file manifests byte for byte**, and the accepted descriptor byte for byte, with set id `879ff234…`.
   - **jsonschema.** The reference model loads the product's vendored jsonschema 4.25.1. The earlier measurement copy is no longer complete.

## Sets

| Entry | State | Set id | Registry packages | Files | Bytes | Lock |
|---|---|---|---:|---:|---:|---|
{rows}

The overlay's `rs-medium-serde` entry gives the same set as `rs-medium-serde` (same lock).

## Decisions and labels (lead, applied here)

- **Generated locks.** Only axum ships an original lock. For the others, `lockfileIdentity` is the experimental lock generated in the accepted corpus collection. NE:1264 says a missing original lock is `input-closure-incomplete` (`lockfile-missing`) and never an implicit generate-lockfile, so a product run over these trees would refuse. Their sets are therefore **sizing stand-ins** for SM-5 and SM-7, labelled as such, and not what a product run would admit.
- **Resolver.** Each set's resolver is taken as Cargo takes it: `workspace.resolver`, then `package.resolver`, else the package edition's default. The basis is recorded per set.
- **Overlay.** Each overlay entry is its own set, as D-3 runs it (two entry children).

## Pending: overlay entry `rs-medium-serde-json`

- **The failure.** Its metadata resolution fails in both attempts: `no matching package named serde_core`.
- **The cause.** The overlay links `serde`, `serde_core` and `serde_derive` to the sibling mount, as the accepted command-data producer projects them. The accepted harness takes no projected configuration and ignores config files, so attempt 2's private-home `config.toml` was not read.
- **What it needs.** A harness variant that applies the accepted overlay links. The working tree of the accepted harness producer is no longer complete, so the variant has to be built separately. It is owed before U-2c's R8 entry 8.
- **Retained.** Both attempts are under `pending-entry-8/`.

**Records.** Receipts, decoded index lines, metadata, audits, keys, manifests and descriptors are in `u2b-records.tar.xz`, with every member pinned in `u2b-records-index.json`.

## Standing

- **Admission.** No source authentication, import admission or Plan.
- **Values.** No SM-5 or SM-7 value; the series are U-2c.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-U2B-DEPENDENCY-SOURCE-SETS-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], receiptsFromTemplateR117Only=True, acceptedHarnessAndRecipesUsed=True, axumControlByteEqual=True, rebuiltBridgeReproducesAcceptedIds=True,
                step6ReconstructionValidated=True, referenceAndBridgeAgree=True, generatedLocksLabelledSizingStandIns=True, overlayEntry8PendingHonestly=True, setsBuilt=8,
                sourceAuthentication=False, importAdmission=False, SM5ValueRecorded=False, SM7ValueRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-U2B-DEPENDENCY-SOURCE-SETS-r1 (U-2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Cargo, any image, harness, bridge or runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries, including `{W}` and the retained private Cargo homes named in the attempt records;
- recomputing identities with the reference model (`docs/coop/design-corrections/native/native_evidence_model.v2.py`, with the product's vendored jsonschema on `sys.path`) in a read-only way.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - The S-M report plan r3, D-2 and U-2; NE:612, :1264, :1663, :1687, :1693-1694; DS4-P1.
  - The accepted axum metadata, context-identity and dependency-fragment spikes.
  - U-2a (`codex-sm-u2a-r2`).

## What to review

1. **Receipts.**
   - Is the `.cache` decoding exact?
   - Is every archive checksum verified?
   - Is every locked version present?
   - Is r117 the only source?
2. **Harness use.** Does the runner equal the accepted recipe apart from looping? Check the image pin and the immutability check.
3. **Audit and steps 5-7.** Check each step against its accepted script. Is the step-6 reconstruction faithful? Check its format against the accepted manifests.
4. **Axum control.** Recompute it: the descriptor byte for byte, set `879ff234…`, the 187 manifests, the keys, and the rebuilt bridge's reproduction of the accepted identities.
5. **Other sets.** Spot-check at least two entries' identities with the reference model.
6. **Decisions.** Are these sound and adequately labelled?
   - the generated-lock stand-in label (NE:1264);
   - the resolver basis;
   - per-entry overlay sets;
   - the honest pending entry 8.
7. **Scope.** No source authentication, import admission, SM-5 or SM-7 value.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of U-2b (dependency-source sets).'); st['SMU2bFrozenSubject'] = sp; write(CTL / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files), archive=pin(out)), indent=2))

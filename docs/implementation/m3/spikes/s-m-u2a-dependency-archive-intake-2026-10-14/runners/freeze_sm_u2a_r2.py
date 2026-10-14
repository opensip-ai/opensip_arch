from pathlib import Path
import json, hashlib, shutil, subprocess, os, re
# Round-2 freeze of U-2a (Codex SM-U2A-R1-RF-01: index-recipe deltas declared; round 1 retained) (S-M report plan r3, D-2 / U-2): the public intake of the crates.io archives that the eight generated Rust
# locks pin but template r116 lacked, and the supplemental template r117, for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-dependency-source-sets-2026-10-14'; S = B / 'sm-u2a-r1-stage'; Q = B / 'reviews/codex-sm-u2a-r2'; R1 = B / 'reviews/codex-sm-u2a-r1'; S1 = B / 'sm-u2a-r1-stage-round1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-u2a-dependency-archive-intake-2026-10-14'
assert not Q.exists() and json.loads((R1 / 'review.json').read_text())['verdict'] == 'REQUIRED-FINDINGS'
if S.exists() and not S1.exists(): S.rename(S1)
assert not S.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] in (None, str(R1))
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
# Coverage check over all nine Rust locks (axum's included).
t = json.loads((W / 'registry-intake-template-r117.json').read_text()); arch = {os.path.basename(f['path']): f['sha256'] for f in t['files'] if f['path'].startswith('cache/')}
C = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-sm-owned-corpus-xw576l4w')
cov = []
for l in ['poly-medium-napi-rs', 'rs-medium-aws-lambda-rust-runtime', 'rs-medium-axum', 'rs-medium-hyper', 'rs-medium-serde', 'rs-medium-serde-json', 'rs-medium-tokio', 'mr-rs-medium-serde-json/rs-medium-serde', 'mr-rs-medium-serde-json/rs-medium-serde-json']:
    raw = (C / l / 'Cargo.lock').read_bytes(); n = miss = bad = 0
    for b in raw.decode().split('\n[[package]]\n')[1:]:
        f = dict(re.findall(r'^(name|version|source|checksum) = "([^"]*)"$', b, re.M))
        if f.get('source') == 'registry+https://github.com/rust-lang/crates.io-index':
            n += 1; k = f"{f['name']}-{f['version']}.crate"
            if k not in arch: miss += 1
            elif arch[k] != f.get('checksum'): bad += 1
    cov.append(dict(lock=l, path=str(C / l / 'Cargo.lock'), **pin(C / l / 'Cargo.lock'), registryRows=n, missingArchives=miss, checksumMismatches=bad))
assert all(c['missingArchives'] == 0 and c['checksumMismatches'] == 0 for c in cov)
write(W / 'u2a-coverage-r1.json', dict(standing='U-2a COVERAGE: EVERY CRATES.IO ROW OF THE NINE RUST LOCKS HAS ITS ARCHIVE IN TEMPLATE r117 WITH THE LOCK CHECKSUM', template=dict(path=str(W / 'registry-intake-template-r117.json'), **pin(W / 'registry-intake-template-r117.json')), locks=cov))
intake = json.loads((W / 'u2a-public-intake-r1.json').read_text()); assert intake['exitCode'] == 0 and intake['outcome']['success']
for n in ['prepare_u2a_missing_public_indexes_r1.py', 'prepare_u2a_missing_public_archives_r1.py', 'archives-u2a.log', 'prepare_u2a_public_intake_packet_r1.py', 'u2a-public-intake-packet-r1.json',
          'run_u2a_public_cache_intake_r1.py', 'u2a-public-intake-r1.json', 'prepare_u2a_registry_template_r117.py', 'registry-intake-template-r117.json', 'u2a-coverage-r1.json']: cp(W / n, n)
for p in sorted((W / 'missing-public-index-inputs-u2a').iterdir()): cp(p, 'index-inputs/' + p.name)
cp(W / 'missing-public-archive-inputs-u2a/receipt.json', 'archive-inputs/receipt.json')
root = Path(intake['root']); cp(root / 'intake.json', 'intake-outcome/intake.json'); cp(root / 'entry-outcome.json', 'intake-outcome/entry-outcome.json')
cp(Path(__file__), 'runners/freeze_sm_u2a_r2.py'); cp(S1 / PREFIX / 'runners/freeze_sm_u2a_r1.py', 'runners/freeze_sm_u2a_r1.py'); cp(S1 / PREFIX / 'REPORT.md', 'history/round1-REPORT.md'); cp(S1 / 'subject.json', 'history/round1-subject.json')
idx = json.loads((W / 'missing-public-index-inputs-u2a/receipt.json').read_text())
names = ', '.join(f"{i['name']} ({i['publishedVersionRecords']})" for i in idx['inputs'])
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M U-2a: crates.io archive intake for the Rust dependency-source sets

**Round 2.** Codex round 1 (`codex-sm-u2a-r1`) found that the index script's name selection went beyond paths, names and counts. Those deltas are now declared (below). The data, fetch and intake are unchanged from round 1, and round 1's report and subject are under `history/`.

This is an outside-product data unit, the first part of U-2 in the S-M report plan r3. Under D-2, the Rust dependency-source set for SM-5 and SM-7 is the contracts' `DependencySourceSetV1`: the activated, admitted, non-path population of each workload's lock. Building those sets for the Rust rows other than axum needs every locked crates.io archive.

The accepted registry template r116 lacked {idx['missingLockedArchives']} locked archives of the eight generated locks (`index-inputs/receipt.json`, `lockedBy`). Ten of them are windows-target crates, and the rest are mostly dev-dependencies. This unit acquires and admits those archives with the accepted recipes. Except for the declared deltas below, each script changes only paths, names, counts and messages.

**Declared deltas (round 2; Codex SM-U2A-R1-RF-01).**
- **Index script.** The accepted fetch (anonymous HTTPS, no proxy, auth or cookies, redirects refused, row checks) is unchanged. The way names are chosen is new: instead of parsing offline-resolution diagnostics, it parses the eight generated locks, compares their crates.io rows with template r116's archive membership, records each lock's pin and the `lockedBy` rows in the receipt, and asserts that every locked version and checksum appears in the fetched index.
- **Packet script.** It computes the version-record total from the per-name entries, because the U-2a index receipt has no top-level total.

The names are lock-derived, as the lead decision of 2026-10-10 requires.


| Step | Script | Accepted parent |
|---|---|---|
| Index | `prepare_u2a_missing_public_indexes_r1.py`: the accepted anonymous fetch unchanged; lock-derived name selection, lock and template comparison, lock provenance and the locked-version checksum check are **declared deltas** (above). | `prepare_sm_hierarchy_missing_public_indexes_r7.py` (fetch) |
| Archives | `prepare_u2a_missing_public_archives_r1.py`: **every** published version of each name, from static.crates.io, verified whole against the index checksum. No version winner is chosen. | `prepare_sm_deno_smithy_missing_public_archives_r13.py` |
| Packet | `prepare_u2a_public_intake_packet_r1.py` | the r13 intake-packet recipe |
| Intake | `run_u2a_public_cache_intake_r1.py`: the closed lowercase supplied-entry intake image (accepted public intake entry). | `run_sm_smithy_hierarchy_public_cache_intake_r12.py` |
| Template | `prepare_u2a_registry_template_r117.py`: template r116 plus the intake's files. | the r13 supplemental-template recipe |

## Results

- **Index.** {len(idx['inputs'])} names: {names}.
- **Archives.** {intake['outcome']['intake']['archives']} archives fetched, every one matching its index checksum ({json.loads((W / 'missing-public-archive-inputs-u2a/receipt.json').read_text())['bytes']:,} bytes).
- **Intake.** Exit 0 and success: {intake['outcome']['intake']['indexes']} indexes and {intake['outcome']['intake']['versionRecords']} version records, with the stock cache serialization round-tripped (`intake-outcome/`).
- **Template r117.** {len(t['files'])} files: {sum(f['path'].startswith('cache/') for f in t['files'])} archives and {sum(f['path'].startswith('index/') for f in t['files'])} index files. The {len(t['overlaps'])} overlaps are recorded in the template manifest: byte-identical archives kept once, and newer index files replacing their named slots.
- **Coverage** (`u2a-coverage-r1.json`). Every crates.io row of all nine Rust locks, axum's included, now has its archive in r117 with the lock's checksum.

**Retained, not staged.** The archive bytes (about 293 MB) stay in the working directory, pinned by `archive-inputs/receipt.json`; the template root likewise.

## Standing

- **Admission.** No source authentication, no native admission and no corpus resolution. The template is labelled a supplemental raw cache copy for future experiments.
- **Not yet built.** The dependency-source sets themselves are U-2b; the SM-5 and SM-7 series are U-2c.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-U2A-DEPENDENCY-ARCHIVE-INTAKE-r1', round=2, productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], round1FindingResolved=True, fetchIntakeTemplateRecipesUnchangedExceptPathsCounts=True, indexNameSelectionDeltasDeclared=True, dataUnchangedFromRound1=True, namesLockDerived=True, wholeVersionSetsAcquired=True, allArchivesChecksumMatched=True,
                closedLowercaseIntakeUsed=True, intakeSucceeded=True, templateR117BuiltFromR116PlusIntake=True, allNineLocksCovered=True, sourceAuthentication=False, nativeAdmission=False, corpusResolutionRun=False,
                SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-U2A-DEPENDENCY-ARCHIVE-INTAKE-r1 (U-2a), round 2

This is round 2. Round 1 (`{R1}`) returned REQUIRED-FINDINGS on `SM-U2A-R1-RF-01`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Cargo, any image, intake or runner, tests or the lane. **No network.** Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries, including the retained archives and template root under `{W}` and the generated locks under `{C}`.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.** S-M report plan r3, D-2 and U-2; the accepted public-intake entry and the earlier accepted index, archive, packet and template recipes named in REPORT.md.

## What to review

0. **Round-1 finding.** Are the index-recipe deltas now explicitly declared in REPORT.md, and scoped by the expected fields? Is all data unchanged from round 1 (`history/round1-subject.json`)?
1. **Recipes.**
   - Diff each U-2a script against its accepted parent.
   - The fetch, archive, intake and template steps may change only paths, names, counts and messages.
   - The index name-selection logic and the packet total are the declared deltas.
2. **Names.** Recompute the missing locked archives from the eight generated locks against template r116. Is each name lock-derived, and does each locked version and checksum appear in its index?
3. **Archives.** Do all 1,128 records match their index checksums? Rehash a sample of the retained archives.
4. **Intake.** Check the closed image and its pins against the accepted entry intake, the outcome counts, and the stock round trip.
5. **Template r117.** Check:
   - r116 plus the intake files;
   - the overlaps recorded and justified;
   - that every row is pinned.

   Recompute the nine-lock coverage.
6. **Scope.** No source authentication, native admission or corpus resolution. The sets themselves are U-2b's.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex round-2 review of U-2a.'); st['SMU2aFrozenSubjectRound2'] = sp; write(CTL / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

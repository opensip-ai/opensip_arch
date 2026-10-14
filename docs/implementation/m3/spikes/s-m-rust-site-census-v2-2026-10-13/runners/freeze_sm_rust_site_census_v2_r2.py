from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Round-2 freeze of U-3 (Codex SM-SITE-V2-R1-RF-01/-RF-02 applied; round 1 retained) (S-M report plan PLAN-r2): the S-M Rust site census v2 (literal and control-flow sites) and the SM-13 fixed-bytes
# and closed-formula desk record, for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-rust-site-census-v2-2026-10-13'; S = B / 'sm-rust-site-census-v2-r1-stage'; Q = B / 'reviews/codex-sm-rust-site-census-v2-r2'; R1 = B / 'reviews/codex-sm-rust-site-census-v2-r1'; S1 = B / 'sm-rust-site-census-v2-r1-stage-round1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-rust-site-census-v2-2026-10-13'
assert not Q.exists() and json.loads((R1 / 'review.json').read_text())['verdict'] == 'REQUIRED-FINDINGS'
if S.exists() and not S1.exists(): S.rename(S1)
assert not S.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] in (None, str(R1))
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
for script, out in [('audit_sm_rust_site_census_v2.py', 'site-census-checks-v2.json'), ('derive_sm13_fixed_bytes.py', 'sm13-fixed-bytes.json')]:
    before = (W / out).read_bytes(); r = subprocess.run(['/usr/bin/nice', '-n', '10', PY, '-I', '-B', str(W / script)], capture_output=True, text=True); assert r.returncode == 0, r.stderr; assert (W / out).read_bytes() == before, out
checks = json.loads((W / 'site-census-checks-v2.json').read_text()); fixed = json.loads((W / 'sm13-fixed-bytes.json').read_text()); census = json.loads((W / 'site-census-v2.json').read_text())
build = json.loads((W / 'producer/build.json').read_text()); assert pin(build['executable']) == {k: build[k] for k in ['bytes', 'sha256']}
assert checks['v1KindsUnchangedInV2'] and checks['allPopulationsRepeated'] and checks['allSiteCountsDeterministic'] and checks['workloadsWithExactCoverage'] == [] and census['compilerChildren'] == 354
for n in ['driver.rs', 'site_walk.rs', 'site_walk-v1.rs', 'closed-driver-source.rs', 'build_site_driver_v2.py', 'build.json', 'build.log', 'sha-build.log']: cp(W / 'producer' / n, 'producer/' + n)
cp(build['executable'], 'compiled-image/site-driver-v2')
for n in ['run_sm_rust_site_census_v2.py', 'audit_sm_rust_site_census_v2.py', 'derive_sm13_fixed_bytes.py', 'site-census-v2.json', 'site-census-checks-v2.json', 'sm13-fixed-bytes.json', 'census-v2-run.log', 'census-v2-run-attempt0-priority-error.log']: cp(W / n, n)
cp(Path(__file__), 'runners/freeze_sm_rust_site_census_v2_r2.py'); cp(S1 / PREFIX / 'runners/freeze_sm_rust_site_census_v2_r1.py', 'runners/freeze_sm_rust_site_census_v2_r1.py')
for n in ['round1-derive_sm13_fixed_bytes.py', 'round1-sm13-fixed-bytes.json']: cp(W / n, 'history/' + n)
cp(S1 / PREFIX / 'REPORT.md', 'history/round1-REPORT.md'); cp(S1 / 'subject.json', 'history/round1-subject.json')
assert pin(W / 'round1-derive_sm13_fixed_bytes.py')['sha256'] == next(f['sha256'] for f in json.loads((S1 / 'subject.json').read_text())['files'] if f['path'].endswith('/derive_sm13_fixed_bytes.py'))
rows = checks['workloads']
t1 = '\n'.join(f"| {r['ordinal']} | {r['id']} | {r['subjectCountS']} | {r['firstPartySubjectsWithSites']} | {r['firstPartySitesOfferedByRelation']['literal@syntactic']} | {r['firstPartySitesOfferedByRelation']['control-flow@syntactic']} | {r['dependencyCrateSitesOfferedByRelation']['literal@syntactic']} | {r['dependencyCrateSitesOfferedByRelation']['control-flow@syntactic']} |" for r in rows)
t2 = '\n'.join(f"| `{x['relationAtRung']}` | {x['relationSchemaId']} | {x['layer']} | {x['resolution'] or 'unset (A6)'} | {x['candidateFixedBytes']}{' + text(resolution), excluded (A6)' if not x['resolution'] else ''} |" for x in fixed['perCandidate']['rows'])
fb = fixed
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M Rust site census v2 and SM-13 fixed bytes (U-3)

**Round 2.** Codex round 1 (`codex-sm-rust-site-census-v2-r1`) returned two required findings, both applied. **RF-01:** the occupancy companion's fixed bytes now include its `schemaVersion` constant 1 (140, was 139), and the near-clones row names its required unbound resolution value as a variable term. **RF-02:** the frame count is now the G3 batch partition, left unset, with ceil(C/B) labelled only as the uniform full-packing case. The census and every owner parameter are unchanged. Round-1 report, derivation and output are under `history/`.

This is an outside-product experiment and desk record, unit U-3 of the accepted S-M report plan (`docs/implementation/m3/s-m-report-plan/PLAN-r2.md`). It completes SM-13's S-M-round decomposition (PROPOSAL-r6:589) for the medium Rust workloads.

- **Part one (sites).** A site census v2 adds `literal@syntactic` and `control-flow@syntactic` sites. It states `reachability@from-resolved-calls` and `clones` mode `near` as derived, and names the compiler query behind each site kind.
- **Parts two and three (bytes and formulas).** It records the exact fixed bytes per candidate, per frame and per census row from the registered schemas and RPP `candidateSpoolAccounting`, with the closed formulas (a)-(e) and SM-14's formula. Every later-owned parameter is left unset.

It produces no SM-13 or SM-14 value and chooses no owned parameter. Large-workload census inputs are U-7's.

## Part one: census v2

### The variant

- **Source.** `producer/site_walk.rs` (v2) is the accepted census r1 walk (`producer/site_walk-v1.rs`, `fedaa40d…`, unchanged otherwise) plus:
  - literal expressions and pattern literals, each also by rustc `LitKind`;
  - `if`; `match`, also by `MatchSource`; `loop`, also by `LoopSource`; `break`; `continue`; `return`; and short-circuit `&&`/`||`.
- **Mapping left open.** Mapping these sites to NE `literalKind` or control-flow `edgeKind` is G3's. They are counted, not classified.
- **Driver.** `producer/driver.rs` differs from the closed framed driver (`closed-driver-source.rs`, `43315ea6…`) by the r1 variant's lines plus one `extern crate rustc_ast;`.
- **Build.** It uses the r1 recipe (bare rustc, pinned 1.95 rustc-dev sysroot). The image is `{build['sha256'][:8]}…`, {build['bytes']} bytes, at `compiled-image/site-driver-v2`.

### The run

- **Executor.** The unchanged closed graph executor and root observer ran over the nine accepted prepared entries, twice each: {census['compilerChildren']} compiler children.
- **Repetition.** Every population repeated the accepted pilots, and site counts were deterministic.
- **Unchanged v1 kinds.** For every launched unit, each site kind and file that census r1 counted has exactly r1's count in v2 (`v1KindsUnchangedInV2` {checks['v1KindsUnchangedInV2']}).
- **First attempt.** It was refused before any work, because it was launched under an outer `nice` and the runner's own priority call could not lower the value. Its log is `census-v2-run-attempt0-priority-error.log`.
- **Timing.** No timing statistic is claimed.

### New sites

First-party sites are on covered subjects only. Dependency-crate sites are reported apart and are not workload subjects. Subject coverage is exact for no workload, as in r1.

| Ord | Workload | S | Subjects with sites | First-party literal | First-party control-flow | Dependency literal | Dependency control-flow |
|---|---|---|---|---:|---:|---:|---:|
{t1}

### Grouping and derived relations

- **Grouping.** `site-census-checks-v2.json` groups site kinds by the relation@rung they are offered for (NE:590-601). The grouping is a label only.
- **Derived relations.** `reachability@from-resolved-calls` has no own site kind; it is derived from calls@resolved-callee sites. `clones` mode `near` (candidate only) is derived from body sites.
- **Queries.** `siteKindQueries` names the compiler query or HIR source behind every site kind.

## Parts two and three: fixed bytes and closed formulas

### Method

`derive_sm13_fixed_bytes.py` counts deterministic-CBOR heads, fixed map keys and fixed values from these sources:
- RPP (`docs/coop/artifacts/rust-provider-protocol.v2.json`: `limitPolicy.candidateSpoolAccounting`, framing and wire schema);
- `fact-plane.v1.json` (`FactCandidateV1`, `anchor-ref.v1`, relation registry);
- the product relation registry;
- `fact-batch-v3`, `occupancy-v1`;
- FA-2's proposed `symbol-census-v1`.

**Reference encoder.** It is the script's RFC 8949 shortest-head rule (`head`). The lead wrote it, and nothing outside this unit has reviewed it. It encodes no value.

### Fixed bytes

**Per candidate (`FactCandidateV1`, 14 keys).** The common fixed part is {fb['perCandidate']['commonFixedBytes']} bytes. Each relation@rung adds its registry values:

| relation@rung | relationSchemaId | layer | resolution | Fixed candidate bytes |
|---|---|---|---|---:|
{t2}

**Variable parts of a candidate** (owner in brackets):
- `candidateOrdinal` (value);
- `producerVersion` (release);
- `targetUniverseId`, `confidenceMillionths` and the relation payload (G3);
- for `clones` near only, the required resolution value, unbound (A6);
- anchors (count: G3). Each source-span anchor is {fb['perCandidate']['perSourceSpanAnchorFixedBytes']} fixed bytes plus path, offsets, `snapshotId` and `contentSha256`.

**Other parts:**
- **(b) Spool entry:** {fb['b_spool']['perEntryFixedBytes']} fixed bytes, plus `stageId` (C4a), `analysisOrdinal` and the candidate.
- **(c) Payload, per FactBatch frame:** envelope {fb['c_payload']['envelopeFixedBytes']} fixed bytes plus `sequence`; FactBatch V2 {fb['c_payload']['factBatchV2FixedBytes']} or V3 {fb['c_payload']['factBatchV3FixedBytes']}; occupancy companion {fb['c_payload']['occupancyCompanionFixedBytes']}.
- **(d) Frames:** a {fb['d_frames']['prefixBytesPerFrame']}-byte transport prefix each, which is not counted in (c). The number of FactBatch frames per stage is the G3 batch partition, which is left unset. ceil(candidates ÷ B) holds only under uniform full packing with batch size B, and is not the general formula.
- **(e) Census row:** {fb['e_census']['rowFixedBytes']} fixed bytes. The complete census container is {fb['e_census']['completeContainerFixedBytes']}.

### Closed formulas

`sm13-fixed-bytes.json` writes each formula with its parameters unset:
- (a) Σ sites × emission factor (G3), per relation@rung and stage (C4a);
- (b)-(e) as the fixed parts above, plus the named variable parts;
- SM-14 = Σ over stages of S_stage × K_stage, with K_stage unset (C4a).

### Ambiguities

The formulas below carry each reading where the sources leave a choice:
- **A1.** Whether RPP:151 counts the whole envelope or its payload value.
- **A2.** Whether FactBatch is V2 or V3 (`target-attribution-v2`).
- **A3.** What `maxResponseFrames` counts.
- **A4.** Whether the census is per Analyze or per stage, and the scope of its bound.
- **A5.** The anchor `snapshotId` and `contentSha256` formats under snapshot2.
- **A6.** The `clones` near candidate's resolution value.

The owning units decide these. No reading is chosen here.

## Standing

- **Owned parameters.** No stage, key, emission factor, census kind, batching or reading is chosen.
- **Values.** No SM-13 or SM-14 value is given, and no site count is presented as a candidate count. SM-11 has no quotient, because coverage is not exact.
- **Out of scope.** Large workloads are U-7's. There is no native admission and no product change.
- **Gates.** L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-RUST-SITE-CENSUS-V2-r1', round=2, productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], round1FindingsResolved=True, round1HistoryRetained=True, variantOnlyAddsLiteralAndControlFlow=True, closedExecutorObserverUnchanged=True, compilerChildren=354,
                allPopulationsRepeated=True, allSiteCountsDeterministic=True, v1KindsUnchangedInV2=True, workloadsWithExactCoverage=0, derivedRelationsStated=True, siteKindQueryTablePresent=True,
                fixedBytesCorrect=True, ambiguitiesStatedNotChosen=True, sitesLabelledNotCandidates=True, ownedParametersChosen=False, SM13ValueDerived=False, SM14ValueDerived=False,
                SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-RUST-SITE-CENSUS-V2-r1 (U-3), round 2

This is round 2. Round 1 (`{R1}`) returned REQUIRED-FINDINGS on `SM-SITE-V2-R1-RF-01` and `-RF-02`; do not modify it.

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run the compiler, Cargo, the driver, the runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing, source reading and Git queries;
- reading the T2 store under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store`;
- re-running the read-only scripts `nice -n 10 python3 -I -B {W}/audit_sm_rust_site_census_v2.py` and `nice -n 10 python3 -I -B {W}/derive_sm13_fixed_bytes.py`. Each rewrites its output in `{W}` and must reproduce it byte for byte.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - The accepted S-M report plan PLAN-r2, U-3 (your `codex-s-m-report-plan-r2`).
  - M3-L r6 item 9, SM-13's S-M part (PROPOSAL-r6:589).
  - The accepted census r1 (`docs/implementation/m3/spikes/s-m-rust-site-census-2026-10-13`, your `codex-sm-rust-site-census-r2`) and its NBO M3L-R6-NBO-01 (the full NE:590-601 range).

## What to review

0. **Round-1 findings.** Are RF-01 (occupancy constant; near-clones resolution term) and RF-02 (frames as the unset G3 partition; ceil(C/B) conditional only) resolved in the derivation, JSON and REPORT? Are the census outputs and every other byte unchanged from round 1 (compare `history/round1-*`)? Check for any other omitted constant.
1. **The variant.**
   - Diff `producer/site_walk.rs` against `producer/site_walk-v1.rs`. It must equal the accepted r1 `producer/site_walk.rs`.
   - Diff `producer/driver.rs` against `closed-driver-source.rs`.
   - Is the change confined to the new site kinds and one `extern crate rustc_ast`?
   - Do the new kinds mean what REPORT.md says?
   - Is mapping to `literalKind`/`edgeKind` left to G3?
2. **Build and run.**
   - Check the build record and image pin.
   - The runner must equal the r1 runner except for names and the v1 pin.
   - Check the closed executor/observer pins, the 354 children, population repetition and determinism.
   - Check the retained first attempt.
3. **The audit.** Re-run it. Check:
   - the new groups and the derived-relation statements;
   - the site-kind query table against the source;
   - the v1 equality check;
   - that coverage is not exact and no quotient is derived.
4. **The fixed bytes.** Re-run the derivation. Independently recompute at least these against the cited schemas and RPP:
   - the candidate common part and two relation rows;
   - the anchor;
   - the spool entry;
   - the envelope;
   - FactBatch V2 and V3;
   - the census row.

   Are the variable parts and owners right, and is every ambiguity stated without a choice?
5. **Scope.** No owned parameter, SM-13 or SM-14 value, or site-as-candidate claim.

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
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex round-2 review of SM-RUST-SITE-CENSUS-V2-r1 (U-3).'); st['SMRustSiteCensusV2FrozenSubjectRound2'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files)), indent=2))

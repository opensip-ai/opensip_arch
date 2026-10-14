from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io, lzma
# Freeze U-2c (Rust SM-5 two-part sealing and SM-7 transfer under PLAN-r3 D-2/D-3) for Codex: runners, variants, r2 series,
# superseded r1 series as history, read-only audit, evidence archive, report, subject manifest and review request.
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u2c'); S = B / 'sm-u2c-r1-stage'; Q = B / 'reviews/codex-sm-u2c-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; CTL = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06'); SP = A / 'docs/implementation/m3/spikes'
PREFIX = 'docs/implementation/m3/spikes/s-m-u2c-rust-sealing-transfer-2026-10-14'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
st = json.loads((CTL / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
# The two-part probe's repository span is the accepted typed probe's span verbatim; only the closing mark is renamed end -> mid.
acc = (SP / 's-m-sealing-typed-2026-10-09/probe.py').read_text().splitlines(); span = acc[4:23]; assert span[0].startswith('for member in') and span[-1].endswith(';end=time.monotonic_ns()')
new = (W / 'probe_two_part.py').read_text(); assert '\n'.join(span[:-1] + [span[-1][:-len(';end=time.monotonic_ns()')] + ';mid=time.monotonic_ns()']) in new
assert acc[3].startswith("spec=json.loads(Path(sys.argv[1]).read_text());control=json.loads((B/'control-template.json')") and acc[3].endswith('start=time.monotonic_ns();rows=[];excluded=[]')
for n in ['prepare_u2c_inputs_r1.py', 'ds_probe.py', 'run_u2c_sm5_ds_r1.py', 'probe_two_part.py', 'run_u2c_sm5_two_part_r2.py', 'receiver_two_phase.py', 'run_u2c_sm7_r1.py', 'receiver_ne_shape.py', 'run_u2c_sm7_r2.py', 'audit_u2c_r1.py']: cp(W / n, 'runners/' + n)
for n in ['u2c-inputs.json', 'sm5-two-part-results-r2.json', 'sm7-results-r2.json', 'u2c-audit.json', 'sm5-two-part-run.log', 'sm7-r2-run.log']: cp(W / n, n)
for n in ['sm5-ds-results-r1.json', 'sm5-run.log', 'sm7-results-r1.json', 'sm7-run.log']: cp(W / n, 'history/' + n)
for p in sorted((W / 'descriptors').glob('*.json')): cp(p, 'descriptors/' + p.name)
inputs = json.loads((W / 'u2c-inputs.json').read_text())['entries']
write(S / PREFIX / 'package-manifests-index.json', dict(standing='PER-PACKAGE FILE MANIFESTS USED BY U-2c (COPIES OF U-2b ACCEPTED MANIFESTS; NOT REPUBLISHED; PACKAGE TREES ARE COPY-ON-WRITE CLONES, NOT PUBLISHED)',
     rows=[dict(entry=e['entry'], package=p['name'] + '@' + p['version'], manifest=p['manifest'], fileManifestSha256=p['fileManifestSha256'], files=p['files'], bytes=p['bytes'], manifestBytes=pin(p['manifest'])['bytes'], manifestSha256=pin(p['manifest'])['sha256']) for e in inputs for p in e['packages']]))
members = sorted(p for d in ['sm5-evidence', 'sm5-two-part-evidence', 'sm7-evidence', 'sm7-r2-evidence'] for p in (W / d).rglob('*') if p.is_file())
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(p.relative_to(W).as_posix()); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''; t.addfile(info, io.BytesIO(raw))
out = S / PREFIX / 'u2c-evidence.tar.xz'; out.write_bytes(lzma.compress(buf.getvalue(), preset=9))
write(S / PREFIX / 'u2c-evidence-index.json', dict(archive='u2c-evidence.tar.xz', archiveSha256=pin(out)['sha256'], members=[dict(member=p.relative_to(W).as_posix(), **pin(p)) for p in members]))
write(S / PREFIX / 'provenance.json', dict(acceptedTypedSealingProbe=dict(path=str(SP / 's-m-sealing-typed-2026-10-09/probe.py'), **pin(SP / 's-m-sealing-typed-2026-10-09/probe.py')), acceptedTypedSealingRunSet=pin(SP / 's-m-sealing-typed-2026-10-09/run_set.py'), acceptedTypedSealingResults=pin(SP / 's-m-sealing-typed-2026-10-09/results.json'),
     acceptedTransferRunner=pin(SP / 's-m-transfer-2026-10-09/run_transfer.py'), acceptedTransferReceiver=pin(SP / 's-m-transfer-2026-10-09/receiver.py'), acceptedTransferResults=pin(SP / 's-m-transfer-2026-10-09/results.json'),
     twoPartProbeRepositorySpanVerbatim=True, receiverSnapshotPhase='the accepted receiver.py checks (1 MiB cap, sorted unique paths, per-row length and digest, trailing bytes), factored into content(); not verbatim',
     referenceModel=pin(A / 'docs/coop/design-corrections/native/native_evidence_model.v2.py'), nativeSchemas=pin(A / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'), corpusManifestSha256='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578'))
cp(Path(__file__), 'runners/freeze_sm_u2c_r1.py')
au = json.loads((W / 'u2c-audit.json').read_text()); ms = lambda v: f'{v / 1e6:.3f}'
s5 = {r['entry']: r for r in au['sm5']}; s7 = {r['entry']: r for r in au['sm7']}; r1a = {r['entry']: r for r in au['sm5r1']}; r1b = {r['entry']: r for r in au['sm7r1']}
order = [e['entry'] for e in inputs]
t5 = '\n'.join(f"| `{e}` | {s5[e]['repository']['rows']} | {s5[e]['repository']['snapshotEquivalentDescriptorBytes']} | {s5[e]['dependency']['packages']} | {s5[e]['dependency']['entries']} | {s5[e]['dependency']['bytes']} | {s5[e]['dependency']['descriptorCanonicalBytes']} | {ms(s5[e]['repositoryPart']['medianNanos'])} | {ms(s5[e]['dependencyPart']['medianNanos'])} | {ms(s5[e]['elapsed']['medianNanos'])} | {ms(s5[e]['elapsed']['maxNanos'])} |" for e in order)
t7 = '\n'.join(f"| `{e}` | {s7[e]['snapshotRows']} | {s7[e]['dependencyEntries']} | {s7[e]['dependencyChunks']} | {s7[e]['dependencyManifestBytes']} | {s7[e]['frames']} | {ms(s7[e]['transfer']['medianNanos'])} | {ms(s7[e]['transfer']['maxNanos'])} | {ms(s7[e]['acceptedRepositoryOnlyMedianNanos']) if s7[e]['acceptedRepositoryOnlyMedianNanos'] else '—'} |" for e in order)
th = '\n'.join(f"| `{e}` | {ms(r1a[e]['medianNanos'])} | {ms(r1b[e]['medianNanos'])} |" for e in order)
R8 = au['R8TwoEntryChildren']
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M U-2c: Rust SM-5 two-part sealing and SM-7 transfer series

This unit runs U-2 of the S-M report plan r3 for every Rust entry: SM-5 in two labelled parts from one timed span (D-2), and SM-7 streaming the sealed repository set and then the dependency-source set (D-2), with R8 as its two Cargo entries (D-3). The sets are U-2b's accepted `DependencySourceSetV1` sets (seven from U-2b, the overlay entry from its follow-on). Generated-lock sets remain sizing stand-ins (NE:1264): only axum's lock is original.

All runs are lead macOS preliminary measurements: 3 warmups then 7 measured fresh children per entry, priority 10 read back for the parent and every child, the ordinary lane held for the whole set, and a private 0700 Darwin TMPDIR. Times are milliseconds (median and max of the 7).

## Inputs

`prepare_u2c_inputs_r1.py` clones each accepted package tree (copy-on-write) out of U-2b's private Cargo homes into the implementation cache (`LD-WORKDIR-TMP-EROSION`), and checks every file against the package's accepted file manifest. The trees and manifest copies are not republished; `package-manifests-index.json` pins every manifest and its `fileManifestSha256`. The descriptors are copied under `descriptors/`.

## SM-5: two parts, one span (r2)

`probe_two_part.py` is a new pinned variant:
- **Part 1, repository.** The accepted typed sealing probe's span, verbatim (`s-m-sealing-typed-2026-10-09/probe.py`; the freeze asserts it). The probe's closing mark is renamed `mid`.
- **Part 2, dependency source.** In the same span, every member of the entry's set is read no-follow (inode and before/after stat checks) and SHA-256-hashed in manifest order, then checked against its length and digest. Each `fileManifestSha256` and the set identity are then computed with the reference model.
- **After the span.** The registered snapshot/plan shape checks and a `DependencySourceSetV1` schema check.

`run_u2c_sm5_two_part_r2.py` is the accepted `run_set.py` recipe. As a control, every child's repository part must reproduce the accepted typed shape for its workload: rows, inventory digest, snapshot2/plan2-equivalent digests, descriptor bytes and exclusions. Each R8 entry's repository part is the accepted overlay union (439 rows; D-3: each entry's map carries the whole overlay).

| Entry | Repo rows | Snapshot descriptor bytes | Dep packages | Dep entries | Dep bytes | Dep descriptor bytes | Repo part | Dep part | Span median | Span max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{t5}

**Bounds.** Each part is reported against its own bounds, and every row meets them.
- **Repository part** (PROPOSAL-r6:559 via D-9): at most 100,000 rows, a 4 MiB descriptor and 8 GiB.
- **Dependency part** (NE:2931-2932 `ProtocolLimitsV3`; the schema's `packages` maxItems): at most 4,096 packages, 1,000,000 entries and 8 GiB.
- **No contract bound** was found on dependency descriptor bytes, so they are only reported.

Under D-9 the dependency part is reported beside snapshot2's rows, not added to them. The repository part's medians are within a few percent of the accepted typed series (`u2c-audit.json` carries both).

## SM-7: repository then dependency source (r2)

`run_u2c_sm7_r2.py` keeps the accepted `run_transfer.py` snapshot phase: the same sealed copies, canonical manifest and u32-framed chunks of at most 1 MiB. Every single entry's sealed manifest is byte-equal to the accepted transfer's.

The dependency phase follows NE §3.2/§9.2 order, with JSON payloads and no CBOR or protocol conformance claimed:
1. One `DependencySourceManifest` frame `{{dependencySourceSetId, entries[{{packageKey, path, byteLength, contentSha256}}]}}`, in descriptor package order, under `maxFramePayloadBytes` (64 MiB).
2. Raw content chunks, each at most `maxDependencySourceChunkBytes` (1 MiB).
3. A `DependencySourceSeal`, which the receiver (`receiver_ne_shape.py`) recomputes and echoes as `DependencySourceAccepted`.

The receiver's snapshot phase is the accepted receiver's checks factored into `content()` (not verbatim). Package keys come from U-2b's accepted observations.

The span runs from the first frame written to the receiver's verified response. The repository-only figure is the accepted 2026-10-09 transfer, shown for comparison.

| Entry | Repo rows | Dep entries | Dep chunks | Dep manifest bytes | Frames | Median | Max | Accepted repo-only median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{t7}

**Controls.**
- **Positive.** One minimal valid dependency phase is accepted.
- **Negative.** Nine malformed streams are refused with a nonzero exit:
  - oversized frame;
  - snapshot digest mismatch;
  - truncated frame;
  - dependency digest mismatch;
  - seal entry-count mismatch;
  - seal manifest-digest mismatch;
  - oversized dependency chunk;
  - duplicate entry;
  - trailing bytes.

## R8 (`mr-rs-medium-serde-json`): two entry children (D-3)

R8's figures are the sums of the two entries' values (medians summed, and maxima summed):

| Figure | Median sum | Max sum |
|---|---:|---:|
| SM-5 whole span | {ms(R8['sm5']['elapsed']['medianSumNanos'])} | {ms(R8['sm5']['elapsed']['maxSumNanos'])} |
| SM-5 repository part | {ms(R8['sm5']['repositoryPart']['medianSumNanos'])} | {ms(R8['sm5']['repositoryPart']['maxSumNanos'])} |
| SM-5 dependency part | {ms(R8['sm5']['dependencyPart']['medianSumNanos'])} | {ms(R8['sm5']['dependencyPart']['maxSumNanos'])} |
| SM-7 | {ms(R8['sm7']['transfer']['medianSumNanos'])} | {ms(R8['sm7']['transfer']['maxSumNanos'])} |

## History: r1 (superseded, retained)

Both r1 series ran cleanly but did not match the plan and contract shape. They are kept under `history/` and in the evidence archive, and they supply no figure.
- **SM-5 r1** timed the dependency part alone in its own span, but D-2 requires one span.
- **SM-7 r1** sent a descriptor frame and then a manifest frame per package. NE has no descriptor frame in transport, and it has one manifest and a seal.

| Entry | SM-5 r1 dep-only median | SM-7 r1 median |
|---|---:|---:|
{th}

## Audit

`audit_u2c_r1.py` (read-only) recomputes every statistic from the raw child records, and checks:
- exits, empty stderr and the part split;
- the accepted repository controls and each entry's set identity, counts and bytes against U-2b;
- the bounds;
- the R8 sums.

The output is `u2c-audit.json`. All raw child records are in `u2c-evidence.tar.xz` (index pinned).

## Standing

- **What this is.** Measured SM-5 (two parts) and SM-7 inputs for the S-M report (U-6).
- **What it is not.** No S-M value, F or T is computed here. No source authentication, import admission, snapshot or Plan identity admission, or protocol conformance.
- **Gates.** SM-5 and SM-7 placeholders are not filled. L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-U2C-r1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], sm5OneSpanTwoParts=True, repositorySpanVerbatimAccepted=True, repositoryControlsReproduceAccepted=True,
                sm7SnapshotPhaseAsAccepted=True, dependencyPhaseNeOrder=True, receiverControlsAdequate=True, statisticsRecomputedFromRaw=True, boundsReportedPerPart=True, r8TwoEntryChildrenSums=True, r1RetainedAsHistory=True,
                generatedLockLabelled=True, protocolConformanceClaimed=False, sourceAuthentication=False, importAdmission=False, SM5PlaceholderFilled=False, SM7PlaceholderFilled=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-U2C-r1 (U-2c: Rust SM-5 two-part sealing and SM-7 transfer)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, probe, receiver, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading, Git queries, and extracting the evidence archive into a fresh directory under your own temporary space. You may read the working directory `{W}` (including the `ds/` package clones and `manifests/`), U-2b's records under `/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14` and `/tmp/opensip-implementation/sm-overlay-metadata-2026-10-14`, and the accepted spikes under `{SP}`.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - S-M report plan r3: D-2 (`PLAN-r3.md:60-70`), D-3 (`:72-76`), D-9 (`:113-117`) and the U-2 row (`:123`).
  - NE §3.1-3.2 (`native-evidence.md:1650-1712`), the frame table (`:2876-2879`) and limits (`:2929-2933`).
  - The accepted typed sealing (`s-m-sealing-typed-2026-10-09`) and transfer (`s-m-transfer-2026-10-09`) series.
  - U-2b and its overlay-entry follow-on (your `codex-sm-u2b-r1` and `codex-sm-u2b-entry8-r1` ACCEPTs).
  - `LD-WORKDIR-TMP-EROSION`.

## What to review

1. **SM-5 (r2).**
   - Is the repository part the accepted typed probe's span verbatim?
   - Is the dependency part inside the same timed span, with a sound part split?
   - Are the dependency reads no-follow and checked against the accepted manifests, with identities computed by the reference model?
   - Does every child reproduce the accepted typed repository shape?
   - Is R8 handled per D-3 (overlay union per entry)?
2. **SM-7 (r2).**
   - Is the snapshot phase as accepted, with sealed manifests byte-equal to the accepted transfer?
   - Does the dependency phase follow NE's order and fields (manifest, chunks, seal, echo) within NE's limits?
   - Are the package keys taken from U-2b's observations?
   - Are the receiver checks and the positive and negative controls adequate?
   - Are disclosures accurate: JSON payloads, no protocol conformance, and the receiver's refactored snapshot phase?
3. **Statistics.** Recompute medians, maxima and the R8 two-entry sums from the raw child records in the archive (or the result files), and check them against `u2c-audit.json` and `REPORT.md`.
4. **Bounds.** Is each part reported against its own sourced bounds, with no invented bound, and the descriptor-bytes bound stated as absent?
5. **History and scope.**
   - Are both r1 series retained and labelled as superseded with accurate reasons?
   - Are the generated-lock sets labelled as stand-ins?
   - Is it true that no S-M value, F or T, placeholder fill, admission or gate claim is made?

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
write(Q / 'status.json', dict(unit='SM-U2C-r1', reviewer='codex', pane='w5:p1', subject=sp, state='requested'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files), review=str(Q)), indent=1))

from pathlib import Path
import json, hashlib, shutil, subprocess, os, tarfile, io
# Freeze the outside-product sized SM-9 lower-bound replay series r1 (S-M-round input to M3-L r6 item 9, SM-9) for Codex.
B = Path('/tmp/opensip-implementation'); W = B / 'sm-replay-sized-2026-10-13'; S = B / 'sm-replay-sized-r1-stage'; Q = B / 'reviews/codex-sm-replay-sized-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PREFIX = 'docs/implementation/m3/spikes/s-m-replay-sized-2026-10-13'
N = A / 'docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09/native'; V = B / 'sm-replay-native-rows-2026-10-13'
assert not S.exists() and not Q.exists()
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): out = S / PREFIX / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, out); assert pin(out) == pin(src)
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
packets = json.loads((W / 'sized-packets-r1.json').read_text()); variant = json.loads((V / 'build-release.json').read_text()); checks = json.loads((W / 'sized-replay-checks-r1.json').read_text())
# Re-run the read-only audit and require identical output.
out = subprocess.run(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(W / 'audit_sized_replay_r1.py')], capture_output=True, text=True); assert out.returncode == 0, out.stderr
assert json.loads((W / 'sized-replay-checks-r1.json').read_text()) == checks and checks['mediansMonotoneInSize'] is True
for n in ['prepare_packet.py', 'remint_selected_schema.py']: assert (W / n).read_bytes() == (N / n).read_bytes()
for n in ['generate_sized_packets_r1.py', 'run_sized_replay_r1.py', 'audit_sized_replay_r1.py', 'prepare_packet.py', 'remint_selected_schema.py', 'selected-native-v2-at-2fbb75c-parent.schema.json',
          'selected-schema-differences.json', 'sized-packets-r1.json', 'sized-replay-results-r1.json', 'sized-replay-checks-r1.json', 'generate.log', 'replay.log',
          'run_sized_replay_r2.py', 'sized-replay-results-r2.json', 'replay-r2.log']: cp(W / n, n)
for n in ['src/main.rs', 'closed-main.rs', 'Cargo.toml', 'Cargo.lock', 'run_release_build.py', 'build-release.json', 'build-release.log', 'first-build-release-garbled-script.json', 'first-build-release-garbled-script.log', 'to_rows.py', 'convert.log']: cp(V / n, 'rows-variant/' + n)
cp(variant['executable'], 'compiled-image/opensip-sm-replay-bench-rows')
for p in sorted(W.glob('remint-*-report.json')): cp(p, 'remint-reports/' + p.name)
r1outs = sorted(W.glob('replay-[0-9]*-*.std*')); r2outs = sorted(W.glob('replay-r2-*-*.std*'))
assert len(r1outs) == 2 * 10 * len(checks['series1']['completedSizes']) + 2 and len(r2outs) == 2 * 10 * len(packets['packets'])
for p in r1outs: cp(p, 'runs/series1-closed/' + p.name)
for p in r2outs: cp(p, 'runs/series2-rows/' + p.name)
cp(B / 'freeze_sm_replay_sized_r1.py', 'runners/freeze_sm_replay_sized_r1.py')
# Packets (~127 MB) and their rows forms (~70 MB): archive them as one deterministic .tar.xz (LFS-tracked under docs/implementation/**).
members = sorted(W.glob('packet-*.json')) + sorted(V.glob('packet-*-rows.jsonl')); assert len(members) == 3 * len(packets['packets'])
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.PAX_FORMAT) as t:
    for p in members:
        raw = p.read_bytes(); info = tarfile.TarInfo(('rows/' if p.suffix == '.jsonl' else 'packets/') + p.name); info.size = len(raw); info.mtime = 0; info.mode = 0o644; info.uid = info.gid = 0; info.uname = info.gname = ''
        t.addfile(info, io.BytesIO(raw))
import lzma
archive = S / PREFIX / 'packets.tar.xz'; archive.parent.mkdir(parents=True, exist_ok=True); archive.write_bytes(lzma.compress(buf.getvalue(), preset=9))
assert archive.stat().st_size < 100 * 2**20
index = [dict(member=('rows/' if p.suffix == '.jsonl' else 'packets/') + p.name, **pin(p)) for p in members]; write(S / PREFIX / 'packets-index.json', dict(archive='packets.tar.xz', archiveSha256=pin(archive)['sha256'], members=index))
assert not [p for p in S.rglob('*') if p.is_file() and p.stat().st_size > 100 * 2**20]
rows = checks['workloads']; s1 = checks['series1']; sets = {s['count']: s for s in checks['series2']['sets']}; agree = checks['seriesAgreement']
setTable = '\n'.join(f"| {s['count']} | {s['objects']} | {s['blobs']} | {s['packetBytes']} | {s['maxRowBytes']} | {s['medianReplayMs']:.3f} | {s['maxReplayMs']:.3f} | {s['minReplayMs']:.3f} |" for s in checks['series2']['sets'])
agreeTable = '\n'.join(f"| {x['count']} | {x['r1MedianMs']:.3f} | {x['r2MedianMs']:.3f} | {x['ratio']:.4f} |" for x in agree)
wlTable = '\n'.join(f"| {r['workload']} | {r['sizingSources']} | {r['SM9LowerBoundMedianMs']:.3f} | {r['SM9LowerBoundMaxMs']:.3f} | {r['SM9LowerBoundMinMs']:.3f} | {'yes' if r['SM9LowerBoundAloneExceedsEditTarget'] else 'no'} |" for r in rows)
over = [r['workload'] for r in rows if r['SM9LowerBoundAloneExceedsEditTarget']]; under = [r['workload'] for r in rows if not r['SM9LowerBoundAloneExceedsEditTarget']]
productHead = git(P, 'rev-parse', 'HEAD')
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M sized SM-9 replay series (labelled synthetic lower bound)

This is an outside-product experiment. It supplies an S-M-round input to M3-L r6 item 9: a **lower bound** on SM-9, the complete replay of a graph of the size SM-2/SM-4 imply, for each of the 14 S-M workload rows. It does not fill SM-9, compute F or T, or record any outcome (A)-(C).

## Lead decision applied

`LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING` (2026-10-13, recorded in the control state; reviewed with this unit):

- **Boundary.** The native release `replay_run` of the closed accepted measurement driver `opensip-sm-replay-bench` (`spikes/s-m-full-replay-partial-2026-10-09/native`, release image `e82a4e2f…`, product `37581132`). Release is the shipped profile; the debug and Python reference boundaries are oracles, not product replay.
- **Sizing.** One synthetic fact and one finding per analysed source: TS distinct configured files (express: 141 synthesized-program roots), Rust RUST3-LIM subjects S. Real per-source fact volumes are F/G3 emission recipes bound after day 0, so a per-source graph understates the real graph. The result is labelled a LOWER BOUND.
- **Use.** A lower bound decides that (A) fails wherever SM-9_lb alone exceeds 2 s, because F = start + SM-5 + SM-7 + SM-9 (PROPOSAL-r6:606) with every term non-negative. Where SM-9_lb ≤ 2 s, (A) is **not established**; the S-M round needs an explicit rule (possibly an L delta) there.

## Packets

The closed accepted generator `prepare_packet.py` and re-mint `remint_selected_schema.py`, byte-identical to the 2026-10-09 spike copies, produced one raw and one selected packet per distinct size (`generate_sized_packets_r1.py`, `generate.log`). The selected native-v2 schema is the one the closed image embeds: `selected-native-v2-at-2fbb75c-parent.schema.json` is `git show 2fbb75c^:schemas/sources/native-v2.schema.json` (`e5834d37…`), equal to native-v2 at `37581132`. Only the `source` path in `selected-schema-differences.json` differs from the accepted spike's. **Control:** the regenerated 193-source raw and selected packets are byte-identical to the accepted spike's (`f33da670…`). All packets are retained in the deterministic archive `packets.tar.xz`; `packets-index.json` pins every member.

## Series 1: the closed image (retained history)

`run_sized_replay_r1.py` ran the closed image `e82a4e2f…` with the accepted `run_release_set.py` recipe, parametrised only by packet: ten fresh children per size, three warmups then seven measured samples, explicit parent priority 10 with child readback 10, the lane held for the whole series, a private 0700 Darwin TMPDIR, HOME unchanged, the image rehashed before and after each set.

It completed every size whose selected packet fits in {checks['canonicalMaxBytes']} bytes ({', '.join(map(str, s1['completedSizes']))}). At 678 the first child **refused**: `ByteLimit` at `src/main.rs:9`. The closed driver parses the whole packet as one product canonical JSON document, and opensip-identity's `canonical.rs` `MAX_BYTES` is 4 MiB; selected packets {', '.join(map(str, s1['packetSizesOverMaxBytes']))} all exceed it. The refusal is in the driver's input transport, before replay. Its stdout/stderr, `replay.log` and partial `sized-replay-results-r1.json` are retained unchanged. No bound was raised.

## Series 2: the rows-transport variant

`rows-variant/` holds a separate pinned variant (`7635c002…`, `compiled-image/opensip-sm-replay-bench-rows`). It is not a modification of the closed driver:

- `src/main.rs` differs from the closed `closed-main.rs` only in input loading (lines 9-12): the packet is JSON Lines, a header row then one object or blob row per line, and **each row** is parsed by the same product `parse_json` under its unchanged 4 MiB `MAX_BYTES`. The registry, `RetainedInputs`, traversal budget, replay limits and the timed `replay_run` interval are byte-identical. Header counts are checked against the rows.
- It builds with the accepted `run_release_build.py` recipe (only its standing label and product-commit field differ) and the accepted `Cargo.lock`, against `product-37581132`, a `git archive` export of product `37581132d8…`, the closed image's product. The audit checks the export against `git ls-tree` file by file. A first build ran an earlier text of the build script whose product-commit field was garbled; its record and log are retained (`first-build-release-garbled-script.*`); the rebuild produced the identical image.
- `to_rows.py` converts each selected packet: values are copied, duplicate keys and floats refused, every row is at most 4 MiB (largest {checks['largestRowBytes']} bytes), and the rows reassemble to a value equal to the source packet (`convert.log`). Replay validates the reachable retained preimages, as in the accepted spike, so an altered descriptor would refuse.

`run_sized_replay_r2.py` is the series-1 runner with only the image and packet form changed. Every child of all 14 sets replayed fully and reconstructed exactly `count` findings.

## Results (lead macOS, preliminary, not D12)

Series agreement where both ran (same objects and blobs; medians in ms):

| Sources | Series 1 closed | Series 2 rows | Ratio |
|---:|---:|---:|---:|
{agreeTable}

Series 2:

| Sources | Objects | Blobs | Selected packet bytes | Largest row bytes | Median ms | Max ms | Min ms |
|---:|---:|---:|---:|---:|---:|---:|---:|
{setTable}

The accepted 193-source release median was {checks['accepted193ReleaseMedianMs']:.3f} ms. Series-2 medians are monotone in size (`mediansMonotoneInSize` {checks['mediansMonotoneInSize']}); the descriptive log-log slope is {checks['logLogSlopeDescriptive']:.3f}. Nothing is extrapolated from it.

| Workload row | Sizing sources | SM-9_lb median ms | max ms | min ms | Every measured sample > 2 s |
|---|---:|---:|---:|---:|---|
{wlTable}

- **SM-9_lb alone exceeds 2 s in every measured sample** (so F > 2 s on this host for that graph, if the boundary and sizing stand): {', '.join(over) if over else 'none'}.
- **(A) not established by the lower bound:** {', '.join(under) if under else 'none'}.

## Observation

The largest single row (one object descriptor) grows with graph size, to {checks['largestRowBytes']} bytes at 1,381 sources. A much larger workload could reach the product's 4 MiB per-document cap in one object. This is recorded for the large-workload units, not as a measured limit.

## Disclosures

- **Product state measured.** Product `37581132` (before `2fbb75c`). The product head is now `{productHead}`. Since then, evaluator source changed only by `include_bytes!` renames to `.current` registries (plus test fixtures); registry data and selected schema bytes changed (native-v2 is now `81d57d6…`); opensip-host and opensip-identity gained new data/digest modules outside the replay call. Replay cost at the current head is not measured here.
- **Synthetic graphs.** Every fact and finding is synthetic. These are not compiler fact volumes, real findings or admitted sources. Packet generation time is not a product figure.
- **Host and resets.** Lead macOS host, not D12. Each sample is a fresh process; no page-cache state is recorded, so no Q0 §9.2 cold or warm label is claimed.
- **Scope.** No product change, native admission, S-M completion, L-G1, effective L or qualification. SM9LowerBoundOnly=true, SM9FigureComplete=false, SM9PlaceholderFilled=false, FComputed=false, TComputed=false, outcomeRecorded=false.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-REPLAY-SIZED-r1', productBase=productHead, architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], closedImageUnchanged=True, closedGeneratorBytesUnchanged=True, acceptedPacket193Reproduced=True,
                series1RefusalRetainedAt678ByteLimit=True, noBoundRaised=True, variantDiffConfinedToInputLoading=True, exportTreeEqualsProductCommit=True, rowsReassembleEqual=True,
                packetArchiveMatchesIndex=True, series2Sets=len(checks['series2']['sets']), samplesPerSet='3 warmups + 7 measured', allSeries2ChildrenFullReplay=True, seriesAgree=True, mediansMonotoneInSize=True,
                lowerBoundLabelSound=True, workloadsWhereLowerBoundAloneExceeds2s=over, workloadsWhereANotEstablished=under,
                SM9FigureComplete=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-REPLAY-SIZED-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run either replay image, the generator, the converter, the runners, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only hashing, JSON parsing, source reading and Git queries (including `git show`, `git diff` and `git ls-tree` in the product repository);
- extracting `packets.tar.xz` into a fresh directory under your own private temporary directory to compare members;
- re-running the read-only audit: `nice -n 10 python3 -I -B {W}/audit_sized_replay_r1.py`. It rewrites `sized-replay-checks-r1.json` in `{W}`, and must reproduce it exactly. It also hashes the product export in `{V}/product-37581132` against `git ls-tree`.

## Subject

- Stage: `{S}`
- `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- Bases: product `{productHead}` (clean), architecture `{git(A, 'rev-parse', 'HEAD')}`.
- Working directories: `{W}` (packets, runners, series outputs) and `{V}` (rows variant, export, rows).
- Authority: M3-L r6 item 9 and its derived figures (`docs/implementation/m3/provider-protocol-l/PROPOSAL-r6.md`, about :580-:620; outcomes (A)-(C)). Precedent: the accepted 193-source spike `docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09` (its `native/` directory).
- Lead decision under review with this unit: `LD-SM9-BOUNDARY-AND-LOWER-BOUND-SIZING`, quoted in `REPORT.md`.

## What to review

1. **Closed pieces.** `prepare_packet.py` and `remint_selected_schema.py` equal the accepted spike copies. The closed image pin equals `native/build-release.json`. `run_sized_replay_r1.py` follows `native/run_release_set.py`, parametrised only by packet. No bound, budget or source was changed.
2. **Selected schema.** `selected-native-v2-at-2fbb75c-parent.schema.json` equals native-v2 at `2fbb75c^` and at `37581132`. Compare `selected-schema-differences.json` with the accepted spike's.
3. **Series 1 refusal.** The refusal at 678 is `ByteLimit` in `parse_json` of the whole packet (`native/src/main.rs:9`; `crates/identity/src/canonical.rs` `MAX_BYTES` at `37581132`). It is retained unchanged, and the completed sets are exactly the packets that fit.
4. **Rows variant.** `rows-variant/src/main.rs` against `rows-variant/closed-main.rs` (= `native/src/main.rs`): is the change confined to input loading, does each row stay under the unchanged cap, and is the timed replay interval identical? The Cargo.toml path change, the accepted lock, the build recipe diff, the export against `git ls-tree 37581132`, the retained first build, the image pin (equal to `compiled-image/opensip-sm-replay-bench-rows`). `to_rows.py`: values copied, not rebuilt; equality on reassembly.
5. **Packets and series.** The archive members equal `packets-index.json`, `sized-packets-r1.json` and `rows-variant/convert.log`; packet-193 raw and selected equal the accepted spike's. Both results files and `runs/`: 3+7 shape, priority readback, every child a full replay with `findings == count`, medians and maxima recomputed; series agreement on overlapping sizes.
6. **Audit.** Re-run it. Check the per-workload mapping to sizes (napi has distinct TS 193 and Rust 239 rows; the overlay is 279), and that the 2 s comparison uses every measured sample.
7. **Standing.** Is "lower bound" sound for this boundary and sizing? Is the inference "SM-9_lb > 2 s implies F > 2 s" stated correctly and limited to this host and boundary? Is (A) left unestablished where the bound does not exceed 2 s? Is the variant a lawful new pinned variant, not a modification of a closed piece made to let data pass? Are the product-state, synthetic, host and reset disclosures accurate? Is anything filled, computed or recorded that item 9 reserves for the S-M round?

Product, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed, and only L-G1 remains open. Native admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{json.dumps(expected, indent=2)}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(Q), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Codex review of SM-REPLAY-SIZED-r1.'); st['SMReplaySizedFrozenSubject'] = sp; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=sp, members=len(files), archive=pin(archive), over=over, under=under), indent=2))

from pathlib import Path
import os, json, hashlib, shutil, subprocess, tarfile, lzma, io, re
# Freeze S-M-TYPED-SEALING-REMAINING-R1 (SM-5 typed synthetic sealing over the remaining Rust/TS development read sets)
# for independent review. Round 2 corrects r1 RF-1 (REPORT class census); measurements, archives and audit are unchanged. Raw per-child stdout/stderr are packed per workload as deterministic USTAR/xz (LFS, under the
# remote's 100 MiB file limit); every member keeps its produced bytes, pinned in raw-pins.json.
B = Path('/tmp/opensip-implementation'); D = B / 'sm-sealing-typed-remaining-2026-10-11'; S = B / 'sm-sealing-typed-remaining-r2-stage'; R = B / 'reviews/grok-sm-sealing-typed-remaining-r2'; R1 = B / 'reviews/grok-sm-sealing-typed-remaining-r1'; S1 = B / 'sm-sealing-typed-remaining-r1-stage'
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'; C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
prefix = 'docs/implementation/m3/spikes/s-m-sealing-typed-remaining-2026-10-11'; closed_prefix = 'docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E.pop(k, None)
def git(root, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=root, env=E).decode().strip()
def digest(raw): return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def pin(root, path): return dict(path=path, **digest((root / path).read_bytes()))
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
st = json.loads((C / 'CURRENT-STATE.json').read_text()); assert st['currentReview'] is None
assert not S.exists() and not R.exists() and not (A / prefix).exists()
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == '' and git(A, 'rev-parse', 'HEAD') == st['architectureHead']
assert (A / '.gitattributes').read_text().count('docs/implementation/**/*.tar.xz') == 1
for name in ['probe.py', 'control-template.json', 'run_set.py', 'audit.py']: assert (D / name).read_bytes() == (A / closed_prefix / name).read_bytes()
results = json.loads((D / 'results.json').read_text()); checks = json.loads((D / 'checks.json').read_text())
T = S / prefix; T.mkdir(parents=True)
loose = re.compile(r'^(.*)-(\d+)\.(stdout|stderr)$'); raw_pins = []; packed = []
by_workload = {}
for p in sorted(D.iterdir()):
    m = loose.match(p.name)
    if m: by_workload.setdefault(m.group(1), []).append(p)
    else: assert p.is_file(); shutil.copyfile(p, T / p.name)
assert sorted(by_workload) == sorted(w['id'] for w in results['workloads'])
for wid, members in sorted(by_workload.items()):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w', format=tarfile.USTAR_FORMAT) as t:
        for p in sorted(members, key=lambda q: q.name):
            raw = p.read_bytes(); info = tarfile.TarInfo(p.name); info.size = len(raw); info.mtime = 0; info.mode = 0o444; info.uid = info.gid = 0; info.uname = info.gname = ''
            t.addfile(info, io.BytesIO(raw)); raw_pins.append(dict(workload=wid, member=p.name, **digest(raw)))
    data = lzma.compress(buf.getvalue(), format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9); assert len(data) < 100 * 1024 * 1024
    out = T / 'raw' / (wid + '.tar.xz'); out.parent.mkdir(exist_ok=True); out.write_bytes(data); packed.append(dict(workload=wid, path='raw/' + out.name, **digest(data)))
    with tarfile.open(out, mode='r:xz') as t:
        got = {m.name: digest(t.extractfile(m).read()) for m in t.getmembers()}
    assert got == {r['member']: dict(bytes=r['bytes'], sha256=r['sha256']) for r in raw_pins if r['workload'] == wid}
write(T / 'raw-pins.json', dict(schemaVersion=1, packing='deterministic USTAR (mtime 0, mode 0444, uid/gid 0) + xz preset 9 CRC64; one archive per workload', members=raw_pins, archives=packed))
# The staged audit reads raw/<id>.tar.xz and must reproduce checks.json exactly.
assert json.loads(subprocess.check_output(['/usr/bin/nice', '-n', '10', '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', str(T / 'audit_remaining.py'), '--stdout'])) == checks
shutil.copyfile(B / 'run_sm_sealing_typed_remaining_r1.py', T / 'run_sm_sealing_typed_remaining_r1.py'); shutil.copyfile(Path(__file__), T / Path(__file__).name)
rows = checks['workloads']; ms = lambda n: f'{n / 1e6:.6f}'
table = '\n'.join(f"| {r['id']} | {r['regularRows']} | {r['bytes']} | {r['snapshotDescriptorBytes']} | " + (f"{ms(r['medianNanos'])} | {ms(r['maxNanos'])}" if 'medianNanos' in r else 'refused | refused') + ' | ' + ('yes' if all(r['bounds'].values()) else 'NO: ' + ', '.join(k for k, v in r['bounds'].items() if not v)) + ' |' for r in rows)
refused = [r for r in rows if r['outcome'] != 'SEALED-EQUIVALENT']; assert [r['id'] for r in refused] == ['rs-very-large-aws-sdk-rust']
(T / 'REPORT.md').write_text(f"""# Typed synthetic snapshot/plan-equivalent sealing over the remaining 21 Rust/TS development read sets

This new preliminary record extends the accepted typed sealing measurement (`{closed_prefix}`, 13 medium read sets) to the remaining Rust and TypeScript/JavaScript development repositories of the pinned T2 corpus: the union of the Rust and TS/JS `devIds` in the small, large and very-large language buckets (8, 5 and 5 by bucket; by repository `sizeClass`, 8 small, 4 large and 6 very-large, because `poly-very-large-deno` is very-large but selected through its large per-language buckets), and to the three remaining accepted overlay workspaces (aws-lambda/tokio, smithy/powertools, smithy SDK). None is held out. Python overlays and the already-measured serde/json overlay are excluded. The closed probe, control template, set driver and audit are reused at their committed bytes, unchanged (byte-checked against `HEAD` before the run). Read sets are repository-only, as in the closed precedent; dependency-source sets are not invented.

Per workload, three warmups and seven measured fresh children ran under the ordinary lane with a private 0700 Darwin TMPDIR, unchanged HOME, and observed priority 10 on the parent and every child. Every member tree was verified against its corpus digest before reading. {checks['successfulChildren']} children exited zero with empty stderr. One child refused: the first `rs-very-large-aws-sdk-rust` child exited 1 because its registered snapshot shape check (outside the timed span) rejected the inventory under `source-inventory` `maxItems` 100000. The driver retains the refusal and does not run that workload's remaining nine children. The audit derives that workload's exact sorted inventory from the retained refusal evidence (the ValidationError instance) and confirms that `maxItems` is the only schema error. That workload has no timing.

| Workload | Regular rows | Source bytes | Snapshot descriptor bytes | Median ms | Max ms | Within snapshot2 bounds |
|---|---:|---:|---:|---:|---:|---|
{table}

## Findings against snapshot2's bounds (PROPOSAL-r5 SM-5, MC item 5)

- **Rows (100,000):** {', '.join(checks['rowBoundMisses'])} exceeds the row bound on its repository-only read set.
- **Descriptor (4 MiB):** {', '.join(checks['descriptorBoundMisses'])} exceed the 4 MiB snapshot-equivalent descriptor. The registered schema bounds rows, not descriptor bytes, so the three sealed workloads among them pass the registered shape check while exceeding the SM-5 descriptor bound; the refused aws-sdk-rust inventory misses both.
- **Total bytes (8 GiB):** no workload exceeds it.

{checks['workloadsWithinAllSnapshot2Bounds']} of 21 read sets fit all three bounds. Every miss is a repository whose `sizeClass` is very-large or the very-large smithy SDK overlay, and adding dependency sources can only enlarge these sets. Per PROPOSAL-r5, a snapshot2 miss is MC's S-R successor question. It is recorded, not worked around: the probe, template and bounds are unchanged, and no sources were trimmed.

Raw children are retained per workload as deterministic USTAR/xz archives under `raw/`. Each member's produced bytes are pinned in `raw-pins.json`. `audit_remaining.py` is new; it follows the closed audit's identity, shape and statistical checks but records the bounds instead of asserting them. It reproduces `checks.json` from either the loose or the packed children. Public control identities match the synthetic host replay fixture, which is not the private 413 fixture. Run on the lead macOS host, not D12; timings are preliminary. Overlay configuration is not captured, and no root manifest is invented.

SM5FigureComplete=false, SM5PlaceholderFilled=false, SMComplete=false, LG1Met=false, snapshotPlanIdentitiesAdmitted=false, dependencySourceSetsIncluded=false, effectiveL=false, productQualification=false. No F or T. Product, law and lock are unchanged.
""")
paths = ['docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md', 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json', closed_prefix + '/REPORT.md', closed_prefix + '/checks.json', 'docs/implementation/m3/reviews/grok-sm-sealing-typed-r1/review.json']
for p in paths: assert (A / p).is_file(), p
m = dict(schemaVersion=1, unit='S-M-TYPED-SEALING-REMAINING-READSETS-R1', productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'),
         files=[pin(S, p.relative_to(S).as_posix()) for p in sorted(T.rglob('*')) if p.is_file()], authorities=[pin(A, p) for p in paths],
         productAuthorities=[pin(P, p) for p in ['design-lock.json', 'schemas/sources/identity-v3.schema.json', 'crates/host/tests/fixtures/replay-fixtures.json', 'tools/quality/corpus.py', 'tools/quality/store.py']])
write(S / 'subject.json', m); subject = pin(S, 'subject.json'); write(S / 'stage.json', dict(subjectManifest=subject, prefix=prefix)); R.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=subject['sha256'], workloads=21, successfulChildren=checks['successfulChildren'], refusedChildren=checks['refusedChildren'],
                workloadsWithinAllSnapshot2Bounds=checks['workloadsWithinAllSnapshot2Bounds'], rowBoundMisses=checks['rowBoundMisses'], descriptorBoundMisses=checks['descriptorBoundMisses'], totalBytesBoundMisses=checks['totalBytesBoundMisses'],
                closedRecipeUnchanged=True, snapshot2BoundMissIsMCSuccessorQuestion=True, SM5FigureComplete=False, SM5PlaceholderFilled=False, SMComplete=False, LG1Met=False, snapshotPlanIdentitiesAdmitted=False,
                dependencySourceSetsIncluded=False, sourceAdmissionClaimed=False, effectiveL=False, productQualification=False, productCodeUnchanged=True)
(R / 'REQUEST.md').write_text(f"""# Review request: S-M-TYPED-SEALING-REMAINING-READSETS-R1 (round 2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{R}/`).

## Boundaries

Do not edit either repository, the stage, the raw run directory or control files. Do not run the probe, the set driver, the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held-out sources or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, schema validation, in-memory archive reading, statistics and Git queries are permitted; the staged `audit_remaining.py --stdout` is read-only and may be run.

## Subject

- Stage: `{S}` (archive prefix `{prefix}`)
- `subject.json`: {subject['bytes']} bytes, SHA-256 `{subject['sha256']}`, {len(m['files'])} members, plus authority and product-authority pins. Rehash every member and pin.
- Raw run directory (produced form, for cross-checking `raw-pins.json`): `{D}`

## What to review

**Round 2.** Your r1 review (`{R1}`) raised one required finding, RF-1: the report's class census. The census sentence (and the matching very-large sentence) in `REPORT.md` is corrected. Confirm that, apart from `REPORT.md` and the staged preparer (now `prepare_sm_sealing_typed_remaining_r2.py` in place of the r1 preparer), every member is byte-identical to the r1 stage `{S1}`.

New preliminary SM-5 measurement extending the accepted 13-set typed sealing record (`{closed_prefix}`, your review `grok-sm-sealing-typed-r1`) to the 18 remaining small/large/very-large Rust/TS development repositories and three remaining overlays.

1. **Closed recipe unchanged.** `probe.py`, `control-template.json`, `run_set.py` and `audit.py` equal the committed closed copies. The new driver `run_sm_sealing_typed_remaining_r1.py` byte-checks them against `HEAD`, verifies member trees before reading, sets and observes priority 10, holds the lane, and uses a private 0700 TMPDIR.
2. **Raw retention.** Each `raw/<id>.tar.xz` is deterministic, under 100 MiB, and holds exactly the members pinned in `raw-pins.json`, which match the produced loose files in the raw run directory.
3. **Audit.** `audit_remaining.py` performs the closed audit's identity, public-control, registered-shape and statistical checks, and records rather than asserts the bounds. Running it with `--stdout` reproduces `checks.json`. Check especially the refused workload: its inventory is taken from the retained ValidationError instance. Confirm the instance is the probe's sorted unique inventory, that `maxItems` on `sourceInventory` is the only schema error, and that no timing is claimed.
4. **Findings.** The row miss, the three descriptor misses (registered schema accepts them; the 4 MiB bound is PROPOSAL-r5 SM-5/MC item 5), and no total-bytes miss. A snapshot2 miss is MC's S-R successor question; nothing is trimmed and no bound is changed.
5. **Scope.** Repository-only, overlay configuration not captured, preliminary lead macOS host (not D12), no identity admission, no dependency sets, no F/T, no full SM-5, full S-M, effective L or qualification.

Product, law and lock are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{json.dumps(expected, indent=2)}
```

The lead will give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
""")
st.update(currentReview=str(R), currentCandidate=str(S), currentReviewStatus='PREPARED-NOT-SUBMITTED', currentWork='Review remaining-readset typed sealing (SM-5).'); st['SMSealingRemainingFrozenSubjectR2'] = subject; write(C / 'CURRENT-STATE.json', st)
print(json.dumps(dict(stage=str(S), subject=subject, members=len(m['files']), archives=[(a['workload'], a['bytes']) for a in packed]), indent=2))

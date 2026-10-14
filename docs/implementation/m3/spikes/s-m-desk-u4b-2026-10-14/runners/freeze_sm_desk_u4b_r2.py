from pathlib import Path
import json, hashlib, shutil, subprocess, os
# Freeze ROUND 2 of the S-M desk record U-4b (Codex SM-U4B-R1-RF-01: Express SM-2 from the synthesized program only, D-4;
# cohort Express kept as separately labelled information; uniqueness check) for Codex.
B = Path('/tmp/opensip-implementation'); W = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u4b'); S = B / 'sm-desk-u4b-r2-stage'; Q = B / 'reviews/codex-sm-desk-u4b-r2'; S1 = B / 'sm-desk-u4b-r1-stage'; Q1 = B / 'reviews/codex-sm-desk-u4b-r1'
P = Path('/Users/sb/code/opensip-ai/opensip'); A = P.parent / 'opensip_arch'; SP = A / 'docs/implementation/m3/spikes'
PREFIX = 'docs/implementation/m3/spikes/s-m-desk-u4b-2026-10-14'
assert not S.exists() and not Q.exists()
E_ = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE']: E_.pop(k, None)
def git(p, *args): return subprocess.check_output(['/usr/bin/git', *args], cwd=p, env=E_).decode().strip()
def pin(p): raw = Path(p).read_bytes(); return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def write(p, v): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(v, indent=2) + '\n')
def cp(src, rel): o = S / PREFIX / rel; o.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, o); assert pin(o) == pin(src)
assert git(P, 'status', '--porcelain') == '' and git(A, 'diff', '--name-only') == '' and git(A, 'diff', '--cached', '--name-only') == ''
r1v = json.loads((Q1 / 'review.json').read_text()); assert r1v['verdict'] == 'REQUIRED-FINDINGS' and [f['id'] for f in r1v['requiredFindings']] == ['SM-U4B-R1-RF-01']
for n in ['derive_u4b.py', 'u4b-desk-records.json']: cp(W / n, n)
cp(W / 'derive_u4b_r1.py', 'history/round1-derive_u4b.py'); cp(W / 'u4b-desk-records-r1.json', 'history/round1-u4b-desk-records.json'); cp(S1 / PREFIX / 'REPORT.md', 'history/round1-REPORT.md'); cp(S1 / 'subject.json', 'history/round1-subject.json')
cp(Path(__file__), 'runners/freeze_sm_desk_u4b_r2.py'); cp(B / 'freeze_sm_desk_u4b_r1.py', 'runners/freeze_sm_desk_u4b_r1.py')
d = json.loads((W / 'u4b-desk-records.json').read_text()); R = d['SM10']; mib = lambda v: f'{v / 1048576:.1f}'; ms = lambda v: f'{v / 1e6:.1f}'
def cell(lang, row, comp):
    g = {r['reset']: r for r in R if r['language'] == lang and r['row'] == row and r['component'] == comp and (row != 'mr-rs-medium-serde-json' or r['source'].startswith('larger') or comp in ('SM-3', 'SM-9'))}
    return f"{mib(g['warm']['medianBytes'])} / {mib(g['cold']['medianBytes'])}"
TS = ['js-medium-express', 'poly-medium-napi-rs', 'ts-medium-powertools-lambda', 'ts-medium-smithy-typescript', 'ts-medium-umami', 'ts-medium-vite']
RS = ['poly-medium-napi-rs', 'rs-medium-aws-lambda-rust-runtime', 'rs-medium-axum', 'rs-medium-hyper', 'rs-medium-serde', 'rs-medium-serde-json', 'rs-medium-tokio', 'mr-rs-medium-serde-json']
tts = '\n'.join(f"| `{r}` | " + ' | '.join(cell('tsjs', r, c) for c in ['SM-1', 'SM-2', 'SM-5', 'SM-7', 'SM-9']) + ' |' for r in TS)
trs = '\n'.join(f"| `{r}` | " + ' | '.join(cell('rust', r, c) for c in ['SM-3', 'SM-4', 'SM-5', 'SM-7', 'SM-9']) + ' |' for r in RS)
s11 = d['SM11']
t11 = '\n'.join(f"| {x['ordinal']} | `{x['row']}`{' / ' + x['entryChild'] if x['entryChild'] else ''} | {x['S']} | {ms(x['SM4']['warm']['medianNanos'])} / {ms(x['SM4']['warm']['maxNanos'])} | {ms(x['SM4']['cold']['medianNanos'])} / {ms(x['SM4']['cold']['maxNanos'])} | {mib(x['SM10']['warm']['medianBytes'])} / {mib(x['SM10']['cold']['medianBytes'])} | {len(x['coveredUnits']['firstPartyAnalysed'])} ({', '.join(x['coveredUnits']['firstPartyAnalysed']) or '—'}) | {len(x['coveredUnits']['firstPartyNotAnalysed'])} | {x['coveredUnits']['dependencyUnitsAnalysed']} | none: {x['quotientReason']} |" for x in s11)
r8w = sum(x['SM4']['warm']['medianNanos'] for x in s11 if x['ordinal'] in (7, 8)); r8c = sum(x['SM4']['cold']['medianNanos'] for x in s11 if x['ordinal'] in (7, 8))
(S / PREFIX / 'REPORT.md').write_text(f"""# S-M desk record U-4b: SM-10 per F/T component, and SM-11's labelled coverage

**Round 2.** Codex round 1 (`codex-sm-desk-u4b-r1`) found SM-U4B-R1-RF-01: the JSON held two current SM-2 records per reset for Express, one from the cohort and one from the synthesized program. D-4 selects the synthesized program only. Round 2 makes three changes:
- Express is excluded from the cohort loop.
- The cohort's Express figures move to `SM10Informational`, labelled "NOT D-4 SM-2".
- The derivation asserts that every current entry is unique by language, row, component, reset and entry child, and that the count is exactly 152.

No measurement changed. Every other entry equals round 1's, and SM-11 is unchanged. The round-1 derivation, records, report and subject are under `history/`.

This is a desk record under the accepted S-M report plan r3 (`docs/implementation/m3/s-m-report-plan/PLAN-r3.md`, U-4; D-3, D-5, D-7). It completes U-4: U-4a (`s-m-desk-u4a-2026-10-13`) covered SM-8 and S_eff's first term. `derive_u4b.py` reads committed result records, or records pinned by a committed index. Nothing was run. It fills no placeholder, computes no F or T and records no outcome.

## SM-10 per F/T component

**Definition (item 9).** SM-10 is per-process `wait4` `ru_maxrss`, information only. It is given in the native unit as recorded (`bytes` on this macOS host), with the checked conversion to bytes (identity, asserted 0 ≤ v < 2^64). For each row, component and reset, the record gives the median and maximum over the 7 measured runs of that run's process peak. `u4b-desk-records.json` has 152 current entries, each with its source and unique by language, row, component, reset and entry child. It also has two informational entries (the cohort's Express run), which are not SM-2 under D-4.

**Sources.**
- **Warm** (D-7, "warm, priming by warmups, no declared caches"): the accepted component series. These are SM-1 and SM-3 ready, the TS cohort and synthesized program (D-4), typed sealing and transfer (TS rows), replay sized r2, U-1 static-profile for SM-4 (D-5), and U-2c's SM-5 r2 and SM-7 r3 (Rust rows).
- **Cold:** U-5a (TS rows) and U-5b (Rust rows).

**Labels.**
- **SM-4.** A run launches many compiler children, so the per-run value is the **largest single compiler child's peak**, with the child counts recorded. The executor parent is not a recorded process (lead decision LD-U4B-SM4-RSS).
  - **hyper.** Its warm SM-4 is the accepted static-profile series, because U-1 changes no hyper unit (D-5). Its cold SM-4 is the U-1 runner over the same population.
- **SM-7.** The figure is the receiver child's peak; the sender is the measuring parent.
- **SM-1 and SM-3.** Each is one shared start figure for its language.
- **Express SM-2.** The synthesized program (D-4), only.
- **SM-9.** These are synthetic replay scenarios at each row's D-1 size.
- **R8 (D-3).** RSS is reported per entry child, and the table shows the larger of the two (lead decision LD-U4B-R8-RSS). D-3's sums apply to per-child time; peaks of sequential children are not added.

Medians in MiB (1 MiB = 1,048,576 bytes), **warm / cold**. Maxima are in the JSON.

**TS rows**

| Row | SM-1 | SM-2 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
{tts}

**Rust rows**

| Row | SM-3 | SM-4 | SM-5 | SM-7 | SM-9 |
|---|---:|---:|---:|---:|---:|
{trs}

## SM-11: SM-4 and SM-10 by covered units (medium Rust rows)

**Rule (item 9, S-M round part).** For each workload the record carries:
- the exact subject count S by RUST3-LIM's recipe;
- SM-4's time and SM-10's peak RSS, each labelled with the compilation units it covers.

A quotient by S is recorded **only** where those units are exactly the workload's first-party crates holding its S subjects. A figure that includes dependency crates, or misses a first-party unit, is recorded with its coverage and no quotient. The worker's scratch is not measured here.

**Coverage.** The coverage comes from U-1's populations, the SM-4 series under D-5, read from the first measured run's unit standings. A unit is first-party when its Cargo `pkg_id` is a `path+` package; every other unit is a dependency. S is RUST3-LIM's count, as the census records it.

| Ord | Row | S | SM-4 warm ms (median / max) | SM-4 cold ms | SM-10 MiB warm / cold | First-party analysed | First-party not analysed | Dependency units analysed | Quotient |
|---|---|---:|---:|---:|---:|---|---:|---:|---|
{t11}

**Result.** Every row's covered units include dependency crates. Every row except hyper also misses first-party units, which are unavailable for the reasons in the JSON (build scripts, proc macros, non-library targets and their dependants, and `serde_core`'s `OUT_DIR` include). Under item 9's rule, **no SM-11 quotient is recorded**. This agrees with the accepted census.

**R8 two entry children (D-3).** The SM-4 medians sum to {ms(r8w)} ms warm and {ms(r8c)} ms cold.

## Standing

- **Records.** Desk records only, on the lead's macOS host, labelled preliminary, not D12.
- **Not filled.** No `⟨SM-n⟩` placeholder, F, T or outcome; SM-12 to SM-14 are untouched.
- **Gates.** O7, D3 and D13 are closed. L-G1 is open, and L is not in effect.
""")
files = [dict(path=p.relative_to(S).as_posix(), **pin(p)) for p in sorted(S.rglob('*')) if p.is_file()]
write(S / 'subject.json', dict(schemaVersion=1, unit='SM-DESK-U4B-r2', round=2, productBase=git(P, 'rev-parse', 'HEAD'), architectureBase=git(A, 'rev-parse', 'HEAD'), prefix=PREFIX, files=files)); sp = pin(S / 'subject.json'); Q.mkdir(parents=True)
expected = dict(verdict='ACCEPT', requiredFindings=[], subjectManifestSha256=sp['sha256'], rf01ExpressSm2SynthesizedOnly=True, currentEntriesUnique=True, sm10AllRowsComponentsResets=True, nativeUnitAndCheckedConversion=True, sourcesCorrect=True, sm4ChildPeakLabelled=True, r8RssNotSummed=True,
                sm11CoverageExact=True, sm11NoQuotientCorrect=True, statisticsRecomputed=True, desksOnlyNothingRun=True, placeholderFilled=False, FComputed=False, TComputed=False, outcomeRecorded=False, SMComplete=False, LG1Met=False, effectiveL=False, productQualification=False)
(Q / 'REQUEST.md').write_text(f"""# Review request: SM-DESK-U4B-r2 (S-M desk record U-4b round 2: SM-10 and SM-11)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading and Git queries; reading committed archives in memory; reading the index-pinned working copies the derivation names:
- U-1's series at `/tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/bsabsent-static-profile-series-r1.json`, with its graphs via `bsabsent-command-source-maps-r1.json` there;
- U-5b's working directory `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u5b`.

## Subject

- **Stage.** `{S}`
- **Subject file.** `subject.json`: {sp['bytes']} bytes, SHA-256 `{sp['sha256']}`, {len(files)} members. Rehash every member.
- **Bases.** Product `{git(P, 'rev-parse', 'HEAD')}` (clean); architecture `{git(A, 'rev-parse', 'HEAD')}`.
- **Authority.**
  - S-M report plan r3: U-4 (`PLAN-r3.md:125`), D-3, D-5 and D-7.
  - Item 9's SM-10 and SM-11 rows, and the S-M round rule for SM-11 (`provider-protocol-l/PROPOSAL-r6.md`).
  - U-4a (`s-m-desk-u4a-2026-10-13`).
  - The accepted warm series, U-5a, U-5b, U-1 and U-2c, and the census (`s-m-rust-site-census-2026-10-13`).

## Round 2

Round 1 (`{Q1}`, your REQUIRED-FINDINGS) raised SM-U4B-R1-RF-01 on duplicate Express SM-2 records. Confirm:
- Express SM-2 is now the synthesized program only, for both resets.
- The cohort's Express entries are informational and kept apart.
- The uniqueness and count assertions hold (152 current entries).
- Every other entry, and SM-11, equals round 1's.
- The round-1 records are retained as history.

## What to review

1. **SM-10.**
   - Does every row, component and reset come from the correct accepted source, with the native unit and checked conversion?
   - Are the medians and maxima over the 7 measured runs right? Recompute them.
   - Are the SM-4 largest-child label, the hyper source choice under D-5, the SM-7 receiver label, and the R8 per-entry and larger-of-two treatment (not summed) sound and disclosed?
2. **SM-11.**
   - Are S, the SM-4 times and the SM-10 peaks correct?
   - Is the coverage (first-party by `path+` `pkg_id`; analysed, not analysed with reasons, and dependency units) exact against U-1's populations?
   - Is "no quotient" correct under item 9's rule for every row?
   - Is the R8 SM-4 sum right?
3. **Scope.** Is this desk-only, with no placeholder, F, T, outcome or gate claim?

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
write(Q / 'status.json', dict(unit='SM-DESK-U4B-r2', round=2, reviewer='codex', pane='w5:p1', subject=sp, state='prepared'))
print(json.dumps(dict(stage=str(S), subject=sp, files=len(files)), indent=1))

from pathlib import Path
import json, statistics
# Render S-M-REPORT.md from sm-report-data.json (assemble_sm_report.py) and the accepted desk/figure records. Numbers come
# only from JSON; prose states labels, definitions and standing.
W = Path(__file__).resolve().parent; A = Path('/Users/sb/code/opensip-ai/opensip_arch'); SP = A / 'docs/implementation/m3/spikes'
d = json.loads((W / 'sm-report-data.json').read_text()); C = {(c['row'], c['language'], c['figure'], c['reset']): c for c in d['components']}
# Round 2: the renderer reads ONLY sm-report-data.json (every other figure is materialized there with source pins).
OF = d['otherFigures']
ms = lambda v: f'{v / 1e6:,.1f}'; s3 = lambda v: f'{v / 1e9:.3f}'
TS = ['js-medium-express', 'poly-medium-napi-rs', 'ts-medium-powertools-lambda', 'ts-medium-smithy-typescript', 'ts-medium-umami', 'ts-medium-vite']
RS = ['poly-medium-napi-rs', 'rs-medium-aws-lambda-rust-runtime', 'rs-medium-axum', 'rs-medium-hyper', 'rs-medium-serde', 'rs-medium-serde-json', 'rs-medium-tokio', 'mr-rs-medium-serde-json']
def comptable(lang, rows, figs):
    h = '| Row | ' + ' | '.join(figs) + ' |\n|---|' + '---:|' * len(figs) + '\n'
    return h + '\n'.join(f"| `{r}` | " + ' | '.join(f"{ms(C[(r, lang, f, 'warm')]['medianNanos'])} / {ms(C[(r, lang, f, 'cold')]['medianNanos'])}" for f in figs) + ' |' for r in rows)
R = {(x['row'], x['language']): x for x in d['rows']}
def ft(lang, rows):
    out = '| Row | F warm | F cold | T warm | T cold | F warm without SM-9 | Outcomes |\n|---|---:|---:|---:|---:|---:|---|\n'
    for r in rows:
        x = R[(r, lang)]
        out += f"| `{r}` | {s3(x['F_warm_medianNanos'])} | {s3(x['F_cold_medianNanos'])} | {s3(x['T_warm_medianNanos'])} | {s3(x['T_cold_medianNanos'])} | {s3(x['F_warm_withoutSM9_medianNanos'])} | {', '.join('(' + o + ')' for o in x['outcomes'])} |\n"
    return out
def sens(lang, rows):
    out = []
    for r in rows:
        x = R[(r, lang)]; s = x['sensitivity']; notes = []
        if s.get('BHoldsWithoutSM9') is False: notes.append('(B) depends on the synthetic SM-9: without it, warm F is ' + s3(x['F_warm_withoutSM9_medianNanos']) + ' s')
        if s.get('BHoldsWithoutSM9') is True: notes.append('(B) holds without SM-9')
        for k, lab in [('warmCHoldsWithoutSM9', 'warm (C)'), ('coldCHoldsWithoutSM9', 'cold (C)')]:
            if s.get(k) is False: notes.append(f'{lab} depends on the synthetic SM-9')
            if s.get(k) is True: notes.append(f'{lab} holds without SM-9')
        for k, lab in [('warmCHoldsWithoutDoubleCountedStart', 'warm (C)'), ('coldCHoldsWithoutDoubleCountedStart', 'cold (C)')]:
            if s.get(k) is True: notes.append(f'{lab} holds without the double-counted TS start (D-4)')
            if s.get(k) is False: notes.append(f'{lab} depends on the double-counted TS start (D-4)')
        if not s['outcomeSameUnderSumOfMaxima']: notes.append('the outcome differs under sums of maxima (warm F ' + s3(x['F_warm_maxNanos']) + ' s)')
        if notes: out.append(f"- `{r}` ({lang}): " + '; '.join(notes) + '.')
    return '\n'.join(out)
allrows = [(r, 'tsjs') for r in TS] + [(r, 'rust') for r in RS]
hasB = [f'{r} ({l})' for r, l in allrows if 'B' in R[(r, l)]['outcomes']]; hasC = [f'{r} ({l})' for r, l in allrows if 'C' in R[(r, l)]['outcomes']]; hasA = [f'{r} ({l})' for r, l in allrows if R[(r, l)]['outcomes'] == ['A']]
bNoSM9 = [f'{r} ({l})' for r, l in allrows if R[(r, l)]['sensitivity'].get('BHoldsWithoutSM9') is True]
cNoSM9 = [f'{r} ({l})' for r, l in allrows if R[(r, l)]['sensitivity'].get('warmCHoldsWithoutSM9') is True or R[(r, l)]['sensitivity'].get('coldCHoldsWithoutSM9') is True]
cOnlySM9 = [f'{r} ({l})' for r, l in allrows if 'C' in R[(r, l)]['outcomes'] and f'{r} ({l})' not in cNoSM9]
edge = [f'{r} ({l})' for r, l in allrows if not R[(r, l)]['sensitivity']['outcomeSameUnderSumOfMaxima']]
rep = sorted({(c['sources'], c['medianNanos']) for c in d['components'] if c['figure'] == 'SM-9' and c['reset'] == 'warm'})
yn = lambda b: 'yes' if b else 'NO'
sm8row = lambda x: f"| `{x['row']}` | {x['source']} | {ms(x['medianNanos'])} | {ms(x['maxNanos'])} | {'/'.join(x['callNames'])} |"
sm6rows = '\n'.join(f"| `{w['row']}` | {w['entries']} | {w['bytes']} | {w['snapshotDescriptorBytes']} | {yn(w['TS2EntriesWithin200000'] and w['snapshot2RowsWithin100000'] and w['descriptorWithin4MiB'] and w['bytesWithin8GiB'])} |" for w in OF['SM6']['rows'])
def poprow(p):
    r = p['repository']; dd = p['dependency']; name = f"`{p['row']}` ({'TS' if p['language'] == 'tsjs' else 'Rust'})" + (f" / {p['entryChild']}" if p.get('entryChild') else '')
    dep = f"{dd['packages']} | {dd['entries']} | {dd['bytes']} | {dd['descriptorCanonicalBytes']} | {yn(dd['withinPackages'] and dd['withinEntries'] and dd['withinBytes'])}" if dd else '— | — | — | — | —'
    return f"| {name} | {r['rows']} | {r['bytes']} | {r['snapshotDescriptorBytes']} | {yn(r['withinRows'] and r['withinDescriptor'] and r['withinBytes'])} | {dep} |"
def scope_rows(w):
    return '\n'.join(f"| `{w['workload']}` | {w['S']} | {a['actor']} | {ms(a['medianNanos'])} | {ms(a['maxNanos'])} | {a['peakRssBytes']} | {yn(w['arraysAndCommitmentsEqual'])} |" for a in w['actors'])
fb = OF['SM13']['fixedBytes']
def sites_total(m): return sum(m.values())
text = f"""# S-M report: one-shot M3 provider figures (item 9)

**Lead report record, 2026-10-14 (U-6 of the S-M report plan r3). Preliminary: the lead's macOS host, not the D12 runner. Unreviewed until Codex accepts it.** This is the report M3-L r6 item 9 asks S-M for (`provider-protocol-l/PROPOSAL-r6.md`, item 9). It applies the plan's definitions D-1 to D-9 (`s-m-report-plan/PLAN-r3.md`) to accepted records, gives every figure SM-1 to SM-14 at its standing, computes F and T per workload under each reset S-M applied, and records **every** outcome that holds.

It is the S-M round's input, not its decision. The S-M delta round on L (L-G1) records these outcomes in L and raises the owner questions they name. Nothing here fills a `⟨SM-n⟩` placeholder in L, changes L, or takes effect. O7, D3 and D13 are closed, and only L-G1 is open.

**Round 2** (Codex SM-U6-R1-RF-01 and RF-02): every figure in §4 and §5 is now materialized in `sm-report-data.json` → `otherFigures` from pinned accepted records, and the renderer reads only that file. §4 adds the SM-5 populations against their bounds, and SM-12's maxima and peak RSS for every actor, Sui included. The timing components, F, T and outcomes are unchanged from round 1. **Round 3** (Codex SM-U6-R2-RF-01 and NBO-01): SM-14's subject-count map now covers all 12 item-9 and §3a Rust workloads, adding rspack and Sui from the SM-12 records and cross-checking every census count. The large-workload table gives entry counts. `sm-report-data.json` carries every number in this report, with its source records pinned by SHA-256. `assemble_sm_report.py` recomputes each component statistic from the raw run records: the median and maximum of 7 measured runs after 3 warmups.

## 1. Definitions applied

- **Workloads** (item 9, r2).
  - **TS rows (6):** express, napi-rs (TS), powertools-lambda, smithy-typescript, umami and vite.
  - **Rust rows (8):** napi-rs (Rust), aws-lambda-rust-runtime, axum, hyper, serde, serde-json, tokio, and the overlay `mr-rs-medium-serde-json` (R8).
- **Statistic.** 3 warmups and then 7 runs; median, with the maximum also reported.
- **D-1, SM-9.** SM-9 is the native release `replay_run` over a synthetic graph with one fact, one finding and one fingerprint per counted source. The source count is the TS row's distinct configured files (express: the 141 synthesized roots) or the Rust row's RUST3-LIM S. It is a **workload source-count scenario, not a bound on any real workload**, so every F, T and outcome below is **conditional on D-1**.
- **D-2, the Rust dependency set.** The Rust dependency-source set is `DependencySourceSetV1` (DS4-P1). SM-5 for Rust is the two-part one-span series. SM-7 for Rust streams the repository set and then the dependency set with every NE §9.2 field (U-2c).
- **D-3, R8.** R8 runs as its two Cargo entries. SM-4, SM-5 and SM-7 are the sums of the two entry children. SM-3 enters F once per child, so twice.
- **D-4, SM-2.** SM-2 is the cohort's whole-process span; for express it is the synthesized program. T = F + SM-2 counts the TS start twice, once in SM-1 and again inside SM-2. The over-count is stated beside each TS T.
- **D-5, SM-4.** SM-4 is the static-profile whole graph. It uses U-1's series (build-script outputs absent) for the rows U-1 changes, and the accepted static-profile series for hyper.
- **D-6 to D-9.** D-6 defines SM-8, D-7 the reset labels, D-8 SM-12's labels, and D-9 S_eff's first term (§4).
- **Resets (D-7).**
  - **Warm:** the accepted 3+7 series, "warm, priming by warmups, no declared caches".
  - **Cold:** U-5a (TS) and U-5b (Rust): "cold OpenSIP state, page cache recorded (never claimed flushed)".

## 2. Component figures (ms; median, warm / cold)

Maxima are in `sm-report-data.json`. SM-1 and SM-3 are each one start figure shared by every row of their language.

**TS rows**

{comptable('tsjs', TS, ['SM-1', 'SM-2', 'SM-5', 'SM-7', 'SM-9'])}

**Rust rows** (R8 shows the D-3 entry sums; SM-3 is per child)

{comptable('rust', RS, ['SM-3', 'SM-4', 'SM-5', 'SM-7', 'SM-9'])}

**Labels.**
- **TS SM-5 and SM-7.** These are the repository-only read set, because T2 pins no `node_modules` tree (SM-6).
- **Rust SM-5.** It is the repository part and the dependency part in one span.
- **Rust SM-7.** The dependency phase carries NE's fields with JSON headers; no protocol conformance is claimed.
- **SM-4.** It covers part of each workload (§4, SM-11).
- **SM-9.** It is synthetic under D-1.

## 3. F, T and outcomes

**Definitions.**
- **F and T** (item 9): F = start (SM-1 or SM-3) + SM-5 + SM-7 + SM-9, and T = F + analysis (SM-2 or SM-4). Each is computed here as the **sum of component medians**; the sums of maxima are in the JSON.
- **Targets.** These are the owner-approved targets (`analysis-quality/PLAN.md` §5.2 and §5.3), held on the D12 runner, so this comparison is preliminary:
  - edit target: ≤ 2 s median, **warm**;
  - medium budgets: cold ≤ 30 s and warm ≤ 8 s.
- **Outcome rules** (item 9):
  - **(B)** holds when warm F > 2 s;
  - **(C)** holds when cold T > 30 s or warm T > 8 s;
  - **(A)** holds only when neither does.

Cold F is shown for information; the edit target is warm.

Seconds:

**TS rows**

{ft('tsjs', TS)}
**Rust rows**

{ft('rust', RS)}
**Outcomes that hold** (every one, preliminary, conditional on D-1):
- **(A)** only: {', '.join(hasA)}.
- **(B)**, F > 2 s: {', '.join(hasB)}.
- **(C)**, T over a medium budget: {', '.join(hasC)}.

**Sensitivities.** These are reported beside the outcomes; nothing is substituted for them.
{sens('tsjs', TS)}
{sens('rust', RS)}

**Reading.**
- **(B) comes from the synthetic SM-9.** (B) holds without SM-9 only for {', '.join(bNoSM9) or 'no row'}. Every other (B) depends on D-1's one-fact-and-one-finding-per-source replay scenario.
- **SM-9 grows faster than linearly.** Across the D-1 scenarios, the replay span grows faster than the source count: {rep[0][0]} sources take {s3(rep[0][1])} s and {rep[-1][0]} sources take {s3(rep[-1][1])} s, which is ×{rep[-1][0] / rep[0][0]:.1f} sources against ×{rep[-1][1] / rep[0][1]:.1f} time. This is descriptive; no complexity claim is made.
- **(C) without SM-9.** (C) holds without SM-9, under at least one reset, for {', '.join(cNoSM9)}. For {', '.join(cOnlySM9)}, (C) depends on SM-9. Rust SM-4's whole-graph span includes dependency crates, and TS SM-2 includes the TS start (D-4).
- **Edge case.** {', '.join(edge)}: (A) on sums of medians, but warm F exceeds 2 s on sums of maxima. The outcome stands as computed, with this stated.
- **For the delta round.** Under item 9, (B) raises owner question O3 and (C) raises O4. Both are recorded together, and neither masks the other. These are the S-M delta round's to record and raise, with the D-1 dependence stated.

## 4. Other figures

Every value in this section is materialized in `sm-report-data.json` → `otherFigures`, with the source records pinned in `pins`.

**SM-5 populations** (item 9 SM-5; D-9; D-2). The rows are the snapshot2-equivalent inventory population. The repository part's bounds are 100,000 rows, a 4 MiB descriptor and 8 GiB. The dependency part's bounds are 4,096 packages, 1,000,000 entries and 8 GiB (NE:2931-2932; the schema's packages maxItems). No contract bound was found on dependency descriptor bytes, so they are reported only. R8 is given per entry; each entry's repository part is the overlay union (D-3). The dependency part is reported beside snapshot2's rows, never added to them.

| Row | Repo rows | Repo bytes | Snapshot descriptor bytes | Within repo bounds | Dep packages | Dep entries | Dep bytes | Dep descriptor bytes | Within dep bounds |
|---|---:|---:|---:|---|---:|---:|---:|---:|---|
{chr(10).join(poprow(p) for p in OF['SM5Populations']['rows'])}

**SM-6** (accepted, `s-m-sm6-readset-2026-10-09`): the TS read-set size. It is repository-only, labelled, because T2 pins no dependency tree.

| Row | Entries | Content bytes | Descriptor bytes | Within TS2 and snapshot2 bounds |
|---|---:|---:|---:|---|
{sm6rows}

**SM-8** (D-6; U-4a): the longest single public compiler call, in ms.

| Row | Source | Median | Max | Call |
|---|---|---:|---:|---|
{chr(10).join(sm8row(x) for x in OF['SM8']['rows'])}

Label: {OF['SM8']['label']}.

**SM-10** (U-4b): the `wait4` peak RSS per process, for every row, component and reset. There are {len(OF['SM10']['entries'])} current entries, unique by {OF['SM10']['uniqueKey']}, plus {len(OF['SM10']['informational'])} informational entries. All are in `otherFigures.SM10`. The values are information only, in native bytes with checked conversion. For SM-4 the value is the largest compiler child per run, and R8 is given per entry and as the larger of the two.

**SM-11** (U-4b; U-7): SM-4's time and SM-10's peak, labelled by covered units. **No quotient is recorded for any workload** ({OF['SM11']['quotientsRecorded']}). Every medium row's covered units include dependency crates, and all but hyper also miss first-party units (`otherFigures.SM11.medium`). Large-workload coverage: {'; '.join(f"{w['id']} {w['firstPartySubjectsWithSites']} of {w['S']} subjects with sites" for w in OF['SM11']['large'])}. {' and '.join(OF['SM11']['largeNotAnalysed'])} have no analysed entry.

**SM-12** (accepted, `s-m-rust-scope-2026-10-09`, plus `s-m-sui-scope-series-2026-10-10`): rebuilding the Rust subject scope.
- **Measurement.** Time is the {OF['SM12']['labels']['time']}. Memory is {OF['SM12']['labels']['memory']}.
- **Worker prototype.** The {OF['SM12']['labels']['workerPrototype']}.
- **Still owed.** {OF['SM12']['labels']['pending']}.

Times in ms, median and max of 7; peak RSS in bytes.

| Workload | S | Actor | Median | Max | Peak RSS bytes | Arrays and commitments equal |
|---|---:|---|---:|---:|---:|---|
{chr(10).join(scope_rows(w) for w in OF['SM12']['rows'])}

D-8: "the accepted manifest" is the T2 corpus manifest (`c8cc48e1…`).

**SM-13** ({OF['SM13']['label']}): census v2 (`s-m-rust-site-census-v2-2026-10-13`) and U-7 (`s-m-large-site-census-2026-10-13`).

Fixed bytes per candidate, by relation@rung:

| Relation@rung | Candidate fixed bytes |
|---|---:|
{chr(10).join(f"| {r['relationAtRung']} | {r['candidateFixedBytes']} |" for r in fb['perCandidate']['rows'])}

The other fixed parts:
- (b) spool entry: {fb['b_spool']['perEntryFixedBytes']} bytes;
- (c) envelope {fb['c_payload']['envelopeFixedBytes']}, FactBatch V2 {fb['c_payload']['factBatchV2FixedBytes']} or V3 {fb['c_payload']['factBatchV3FixedBytes']}, occupancy companion {fb['c_payload']['occupancyCompanionFixedBytes']};
- (d) {fb['d_frames']['prefixBytesPerFrame']} bytes of transport prefix per frame;
- (e) census row {fb['e_census']['rowFixedBytes']}, complete container {fb['e_census']['completeContainerFixedBytes']}.

The formulas (a) to (e) are in `otherFigures.SM13.fixedBytes`, with these parameters unset: {'; '.join(f"{owner}: {', '.join(v)}" for owner, v in OF['SM13']['unsetParameters'].items())}. Site totals (first-party / dependency crates) are labelled sites, not candidates:
{chr(10).join(f"- `{w['id']}`{' (ord ' + str(w['ordinal']) + ')' if 'ordinal' in w else ''}: {sites_total(w['firstPartySitesOfferedByRelation'])} / {sites_total(w['dependencyCrateSitesOfferedByRelation'])}" for w in OF['SM13']['sitesMedium'] + OF['SM13']['sitesLarge'])}

**SM-14:** the formula `{OF['SM14']['formula']['formula'] if isinstance(OF['SM14']['formula'], dict) and 'formula' in OF['SM14']['formula'] else OF['SM14']['formula']}`. S is exact for every item-9 and §3a Rust workload: {', '.join(f'{k} {v}' for k, v in OF['SM14']['S'].items())}. Sui is included "if S-P permits". These come from `otherFigures.SM14.S`, taken from the SM-12 subject-count records and equal to every census count. K_stage is unset (C4a).

**S_eff** (D-9; U-4a): the first term is snapshot2's admitted rows, from SM-5, for all 12 Rust workloads. It is not filled.

| Workload | Rows | Total bytes | Descriptor bytes | Within all bounds |
|---|---:|---:|---:|---|
{chr(10).join(f"| `{k}` | {v['rows']} | {v['totalBytes']} | {v['snapshotDescriptorBytes']} | {yn(v['withinAllBounds'])} |" for k, v in OF['SEffFirstTerm']['rows'].items())}

Under D-2, the dependency-source part (the SM-5 table above) is reported beside this term, not added to it. The other terms of S_eff remain formulas.

## 5. Large workloads (§3a; no outcome depends on them)

Per-entry outcomes with exact reasons are in `{OF['LargeWorkloads']['entryCoverage']}`.

| Workload | S | Analysed entries | Subjects with sites | S_eff first term (rows; descriptor bytes) |
|---|---:|---:|---:|---|
{chr(10).join(f"| `{w['id']}` | {w['S']} | {len(w['entries']) if isinstance(w['entries'], list) else w['entries']} | {w['firstPartySubjectsWithSites']} | {OF['LargeWorkloads']['SEffFirstTerm'][w['id']]['rows']}; {OF['LargeWorkloads']['SEffFirstTerm'][w['id']]['snapshotDescriptorBytes']} |" for w in OF['LargeWorkloads']['census'])}
| `poly-large-rspack` | 1384 | 0 | — | {OF['LargeWorkloads']['SEffFirstTerm']['poly-large-rspack']['rows']}; {OF['LargeWorkloads']['SEffFirstTerm']['poly-large-rspack']['snapshotDescriptorBytes']} |
| `rs-very-large-sui` (if S-P permits) | 3318 | 0 | — | {OF['LargeWorkloads']['SEffFirstTerm']['rs-very-large-sui']['rows']}; {OF['LargeWorkloads']['SEffFirstTerm']['rs-very-large-sui']['snapshotDescriptorBytes']} |

The causes are in the coverage record:
- rspack: both entries are refused by the pinned stable compiler (nightly-only `-Z` flags).
- sui: two Git dependencies cannot be checked out offline, and its bin source is an excluded symlink.
- deno: the root descriptor (22,825,382 bytes) is over the closed driver's bound.
- smithy-rs: 15 of its 25 entries are unavailable.

## 6. Standing and what this report does not do

- **Preliminary.** These are the lead's macOS host figures, not D12's. The targets are held on the D12 runner.
- **Conditional.** F, T and every outcome depend on D-1's synthetic SM-9.
- **Not filled.** No `⟨SM-n⟩` placeholder is filled in L. SM-11's quotients, SM-13's values, SM-14's values, S_eff, the worker's scratch and `domainCommitment` wait for the completion round (item 9, r6).
- **Not changed.** L, the closed drivers, executors, observers and generators, and every accepted record are unchanged. No G3 or C4a parameter is chosen.
- **Still open.** Full S-M closes at the S-M delta round. L-G1, effective L, native admission and worker, K1 and qualification remain open.
"""
(W / 'S-M-REPORT.md').write_text(text); print('rendered', len(text))

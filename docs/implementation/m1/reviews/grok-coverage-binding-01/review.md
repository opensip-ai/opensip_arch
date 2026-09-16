# Independent Grok review: coverage source binding

**Reviewer:** Grok (explicitly authorized independent reviewer). Codex remains implementation lead.
**Subject:** `/tmp/opensip-implementation/m1-grok-coverage-review-01/subject`
**Manifest SHA-256:** `dc6dcccfd4f12e97dd87e3a38135d9f4834dd153dee972387adadeafa7a7d1d7` (verified before review and at completion)
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

This is not a Claude review, not whole-product acceptance, not Report1 succession, not a browser/storage/host-custody verdict, and not final source selection.

## Scope judged

Bounded executable reference correction for R-COVERAGE-SOURCE-1:

- standalone experimental panel schema
- source identity / admission boundaries
- selection / prefix rules
- refusals
- conditional byte/depth estimates

Pending duties named by the subject (Report1 carrier/version, producer/checker/fixture joins, whole-report prefix and shared-budget recomputation, generated source and browser adapter, actual snapshot lease) are **not defects merely because they are pending**. A scope limitation is recorded only where it would make a claim in this subject false. None did.

## Frozen bytes

| Item | Expected | Observed |
| --- | --- | --- |
| `subject-manifest.json` | `dc6dcccfd4f12e97dd87e3a38135d9f4834dd153dee972387adadeafa7a7d1d7` | match, 5410 bytes |
| source checkpoint | `3b0d8d7a4ca68940406ebab2a16908cfbff98bbae55d85d577725a20b4f521a3` | match |
| 33 manifest members | per-file sha256+bytes | all match before and after |
| extra/missing files | none | none |
| private copy vs subject after reruns | identical | identical |

Pinned owners used to judge the change still match `input-pins.json`:

| Pin | SHA-256 | Bytes |
| --- | --- | --- |
| joint09 checkpoint06 | `e084dd8693b07e1fc2c0bfb6f809bcc4d4ce3c1f1431664dfbf78f254c4607f0` | 208819 (1199 members) |
| `native-evidence.md` | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` | 329013 |
| `identity-and-evidence.md` | `c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f` | 135448 |
| joint09 `source-check-result.json` | `f0ef35e60baabf183c62e1abe29b9b721efccddf0d80d4a013911e2313e22db7` | 20040 |

Architecture working-tree `git status` shows those two owner prose files dirty versus HEAD; the **pinned bytes** still match. This review judged the pins, not an unpinned HEAD snapshot. Product repository `/Users/sb/code/opensip-ai/opensip` has no `coverage_source.py` / experimental schema (supports `productChanged: false`). Original `review-queue-01/queue.json` still lists 11 frozen units and does not add this experiment as a frozen target (supports `originalFrozenQueueChanged: false`; the queue README records it as supplemental).

Neither working tree was written by this review. `save_checkpoint.py` was not run. Check/measure/prepare/historical scripts were executed only from `review/private-copy/`.

## Owner inspection (the claimed gap is real)

Native §4.1a (`native-evidence.md` ~1924–1940): for every `CoverageResultV3`, `coverage2` is minted from `{schemaVersion: 2, scopeId, payloadSchemaDigest, payloadDigest}` after producer admission. That is one descriptor and one registered payload, not a stream identity.

Identity `open_run_closure` / `close_run` (`identity_model.proposed.v3.py` 1800–1801, 1906–1926): evidence `coverageIds` equal the union of selected view coverage roots **as a set**; each retained `coverage2` is re-admitted through `admit_coverage_result_v3`. `semantic-evidence.coverageIds` is `x-opensip-order: canonical-set`.

Report08 `EvidencePanelV1` (`parent-report08/build_owner.py` 1188–1190) still carries a single `coverageId` plus `entries: CoverageResultV3[]` with hostAsserted `entries-are-retained-stream-prefix-of-coverage-id`. Checker join `J-EVIDENCE-COVERAGE` (`parent-report08/check.py` 719) requires `run.coverageId == data.coverageId`. Fixture construction (`build_fixtures.py` 64) takes `evidence.coverageIds[0]` as that diagnostic/stream id. Byte-law material even builds 2000 `CoverageResultV3` rows under one `coverageId` (`check.py` 2273–2286).

The actual admitted retained Run names **two** distinct `coverage2` records:

- `coverage2:6c1803534378981891c21dc080c2425247cad60a19d7371a348ec91bb60c09ce` (package@manifest-declared)
- `coverage2:c96e33f4ab90977b4b741e2c4e47a7b312adf739e5bf8ddf04bf1d6062222ff0` (file@enumerated)

So the diagnosis in `correction.json` is correct: one `coverage2` cannot identify that collection, and the envelope diagnostic `coverageId` must stay independent.

The experiment’s replacement shape is the right reference correction:

- panel source = `{runId, evidenceId}` of the exact admitted Run
- each row = `{coverageId, descriptor, result}`
- selection = canonical prefix of `semantic-evidence.coverageIds`
- embedded checks = identities / counts / selected native schema document
- host checks = `close_run` + canonical equality to that projection

## Reproduction of author checks (private copy)

Python: `/tmp/opensip-implementation/metadata-reference-env/bin/python` 3.14.6, always `-I -B`. Sources executed via `compile(path.read_bytes(), ...)`.

| Script | Exit | Output vs frozen subject |
| --- | --- | --- |
| `check.py` | 0 | stdout byte-identical to `check01.stdout`; rewrote `panels.json` / `negative-panels.json` / `result.json` to the same hashes |
| `measure_integration.py` | 0 | stdout byte-identical to `integration-measurements.json` |
| `historical-fixture-audit/check.py` | 0 | stdout byte-identical to `historical-fixture-audit/result.json` |
| `prepare.py` | 0 | regenerated `coverage-panel.experimental.schema.json` and `input-pins.json` byte-identical; identity URI `urn:opensip:product-v1:identity:v3` |

Author `result.json` `checkCount: 32` is therefore an observed rerun, not a trusted comment. `prepare01.stderr` still records the failed identity2+identity3 discovery assertion; current `prepare.py` selects identity3 by URI. That failure evidence is preserved, not silently repaired.

## Independent counterexamples

Runnable copy: `review/tests/independent_counterexamples.py`
Results: `review/results/independent-counterexamples.json` — **72/72 passed**.

Constructed and observed:

### Wrong source joins

- Wrong expected `runId` → `ProjectionRefusal: SOURCE_RUN_MISMATCH`.
- Panel `source.evidenceId` swapped to the other retained `semantic-evidence` object `evidence3:27425ba0d9c8a55773a5d9f9263bfe44101a0e4a49f39bf7bc1c2bd695d66255`: **embedded checks pass**, host join → `SOURCE_PROJECTION_MISMATCH`.
- Panel `source.runId` substituted: same split.
- Honest cap-1 prefix verified at cap 2 → `SOURCE_PROJECTION_MISMATCH` (host cap is part of the join).

### Self-consistent wrong identities

- Rehashed payload + matching `payloadDigest` + new `coverageId` `coverage2:611e8be44ec20cefc88fe616d8c36e64195d6ef443564d8bca0fe612b5743439`: embedded passes, not in source, host join fails.
- Stuffing that hash-valid object into the map does **not** expand `project()` output.
- Identity-consistent scope/commitment mismatch (descriptor identity and payload digest recomputed; `subjectScopeCommitment` names the other scope): embedded passes; host join fails; actual native producer refuses `native.subject-scope-commitment-mismatch` and `native.examined-universe-commitment-mismatch`.

### Lost / corrupt records (not empty success)

Missing coverage, missing evidence, missing payload → owner `EvidenceUnavailable` with the missing reference. Corrupt `{}` blob and truncated blob → `AdmissionError: BLOB_DIGEST`. Wrong record kind → `REFERENCE_IDENTITY`. Unadmitted run (`evidenceId` all-zero) → `EvidenceUnavailable`, not an empty panel.

### Non-prefix selections

Source order is canonical-set `[6c18…, c96e…]`. A one-row document carrying only `c96e…` is sorted and identity-consistent (embedded passes) and is **not** a prefix; host join fails. Reversed two-row document fails embedded `ENTRY_ORDER_OR_DUPLICATE`. Duplicate id fails the same.

`project()` itself uses `coverage_ids[:entry_limit]`, so a successful projection cannot emit a non-prefix. Caps 2 and 3956 are canonical-equal on this two-id Run.

### Source mutation / non-aliasing

Caller `(run, objects, blobs)` are unchanged after `project()`. Mutating the **actual returned panel** (not a deepcopy) does not alias caller source (`aliased: false`). Unsorted source `coverageIds` do not project: identity schema `x-opensip-order: canonical-set` refuses first, so `SOURCE_COVERAGE_ORDER` in `coverage_source.py` is not reachable after a successful `close_run`.

### Shape vs native authority

Self-rehashed RC-6 contradiction (`examinedExhaustive=false` with `coverage=complete` on a non-resolved rung `manifest-declared`):

- panel schema + embedded identity/count checks **pass**
- `verify_against_source` **fails** (`SOURCE_PROJECTION_MISMATCH`)
- `admit_coverage_result_v3` **REFUSE** with `RC-6: coverage=complete claims the examined partition is total, so examinedExhaustive must be true`

Historical `parent-bases.fixture.json` `/audit-full/panels/evidence/data/entries/0` (sha256 `ab8fdf865a6747586625cc7e077f12cd9e9f0d42972f9a8618bb936b5f6a1a65`) still validates as `CoverageResultV3` shape and still carries RC-1, RC-6, and `native.coverage-cause-not-for-deficiency:language-tier-unsupported:body-language-owner-ambiguous`. It remains a declared shape/join witness, not the admitted retained Run, and was not reclassified.

### Misleading empty results

A document with `entries=[]`, `total=0`, `omitted=0`, `omissionCause=none` against this two-id Run: embedded passes, host join fails. Honest cap-0 projection is `entries=[]`, `total=2`, `omitted=2`, `omissionCause=item-cap` and **does** join at cap 0. Missing/unadmitted source never becomes that honest empty prefix.

`ExactValidator` rejects `total: true` (`type(value) is int`), so bool-as-integer cannot sneak through document validation.

### Conditional byte / depth estimates

Recomputed with the pinned joint estimators (`derive_budget.py` `structural_max_bytes`, `derive_depth.py` `depth`) and the foundation canonical codec (`B.V.C`), which agrees with identity `C.canonical` on these panels:

| Quantity | Claimed | Independent |
| --- | --- | --- |
| structural row bound old/new/delta | 100328 / 100718 / 390 | same |
| actual row overhead | 390, 390 | 1046→1436 and 1026→1416 |
| present prefix panel bytes (state wrapper) | 671 / 2107 / 3520 / 3520 | same |
| document depth current / with proposed carrier | 39 / 39 | same |
| `explorationMaxCanonicalBytes` | 4194304 | same |
| `documentMaxBytes` | 27829365 | same |
| `maxEvidenceEntries` | 3956 | same as schema `maxItems` and `ENTRY_LIMIT` |

`measure01` vs current differs only by renaming `minimumEmptyPrefixPanelBytes` → `actualZeroRowPrefixPanelBytes`; numeric values are unchanged. The 27,829,365-byte whole-report figure remains a **conditional** bound: it holds only if a successor still applies the same shared 4MiB exploration cap to the newly wrapped complete panels, including metadata and later-state reserves. The standalone schema has no `byte-budget` / `rejectedByteDelta`. That is a stated limitation, not a false claim.

Admitted payload decode: `json.loads(blob)` equals owner `C.parse(blob)` (`equal_typed`) and `C.canonical` round-trips both blobs (1046 and 1026 bytes). So the stdlib decode does not currently diverge on this Run.

## Findings

### Must-fix defects

None. No constructed counterexample made a claim inside this stated reference scope false.

### Justified should-fix

**S1. Author non-aliasing check mutates a deepcopy, so it cannot detect returned aliases.**

- File/line: `check.py` 38–39
- Trigger: `returned-values-do-not-alias-source`
- Reproducer: after `panels['2'] = S.project(...)`, the author does `p=copy.deepcopy(panels['2']); p['entries'][0]['result']['entry']['confidenceMillionths']=0` then asserts caller source equality. Independently mutating `panels[2]` in place (see `independent_counterexamples.py` case `mutating-actual-returned-panel-does-not-alias-caller-source`) is the test that actually probes aliasing.
- Observed: the named check would still pass if `project()` returned caller-owned dictionaries, because the deepcopy is the object mutated.
- Expected: mutate the returned panel (or compare object identities of `panel['entries'][i]['descriptor']` / `['result']` against `objects` / parsed blobs) without copying first.
- Reason: the implementation **does** `copy.deepcopy` inputs (`coverage_source.py` 42) and independent in-place mutation did not alias caller source. This is a test-gap should-fix, not an implementation defect. It should not block this reference-scope accept.

### Advisories

**A1. Payload decode uses stdlib `json.loads` rather than owner `C.parse`.**
`coverage_source.py` 55–57. After actual `close_run`, both admitted blobs round-trip through `C.parse` / `C.canonical`, so this is not currently exploitable with the pinned owner. A weaker `close_run` could let stdlib JSON accept duplicate keys or values the owner would refuse, and a decode failure would be `json.JSONDecodeError` rather than an owner admission class. Successor code should decode with the owner codec. Not a must-fix for this owner-bound experiment.

**A2. `SOURCE_COVERAGE_ORDER` is unreachable after successful `close_run`.**
`coverage_source.py` 50–51. Unsorted `evidence.coverageIds` fail identity `x-opensip-order: canonical-set` (`AdmissionError`) before that guard. Harmless defense in depth; do not treat it as a tested owner-bypass.

**A3. Item cap `3956` is a literal**, duplicated in `coverage_source.py`, `prepare.py`, and the schema, rather than read from the pinned `BudgetProfileV1.maxEvidenceEntries`. It matches today. Drift would be a successor problem.

**A4. Standalone `entriesProjection.total`/`omitted` use uint64 maxima**, not report `Uint53`, and omit `byte-budget` / `rejectedByteDelta`. Documented. Successor carrier must restore those fields and shared exploration reservation; this experiment must not be copied forward as a whole-report budget profile.

**A5. Selection is lexicographic canonical prefix of `evidence.coverageIds`.** That is the stated law and matches identity canonical-set order. It is not severity/sufficiency order. Decide that policy at Report1 integration; it is not a defect of this reference.

**A6. Fixture width is two coverage ids.** Prefix, non-prefix, and extra-object tests are meaningful at that width. They do not by themselves prove a 3956-row producer. Structural bounds cover the schema maximum; actual retained rows do not.

## Scope limitations (not defects)

- Document-local `verify_embedded` cannot prove Run membership, prefix completeness, or native semantic admission. The subject states this; the six (plus independent extra) identity-consistent forgeries confirm it. Host join is `close_run` of the source plus canonical equality, which is sufficient: a panel equal to that projection is the admitted set.
- Optional envelope diagnostic `coverageId` is correctly kept out of this panel. Integrating it back as a stream identity would reintroduce R-COVERAGE-SOURCE-1.
- `project()` deep-copies the whole Run as test/reference custody. That is not a proposed production snapshot lease.
- Historical RC-1/RC-6/cause faults are shape/join-witness properties, not a product analyzer bug, and were not silently repaired.
- README standing still says actual Claude review is pending. This authorized Grok review does not satisfy that historical sentence and does not need to; it also does not freeze a combined successor.
- Whole-report 27,829,365-byte and depth-39 figures are conditional estimator results, not a reachable maximum or producer qualification.

## Commands executed

All with `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B`. No commits, pushes, agents, or `save_checkpoint.py`.

1. SHA-256 of `subject-manifest.json` and every listed file (before).
2. SHA-256 of pinned checkpoint, owner prose, and schema registry.
3. Copy subject → `review/private-copy/` and hash-compare.
4. `review/private-copy/check.py`
5. `review/private-copy/measure_integration.py`
6. `review/private-copy/historical-fixture-audit/check.py`
7. `review/private-copy/prepare.py`
8. `review/tests/independent_counterexamples.py` (loads frozen subject bytes + pinned joint owner; writes only `review/results/`)
9. Independent structural bound / depth / canonical-size recomputation inside that test (exec of `derive_budget.py` / `derive_depth.py` as modules, which do not write unless `__main__`)
10. SHA-256 of manifest, subject files, private copy, and pins (after)

## Limitations of this review

- One synthetic admitted Run (two `coverage2` rows), not a live analyzer or store.
- Native historical-fixture checks used the audit’s local bijection/cause guards, matching the subject’s declared limit (full producer admission of that shape fixture is not claimed).
- Did not re-hash every byte of the eleven original frozen queue subjects; confirmed this experiment is not among those eleven units.
- Did not execute browser adapters, generated eight-output pipeline, or host snapshot custody (out of scope).
- Did not change the implementation.

## Verdict restated

**ACCEPT WITHIN STATED REFERENCE SCOPE.**

The executable correction binds one `coverage2` to one descriptor and one registered `CoverageResultV3`, anchors the panel to the exact admitted Run’s `evidence3`, selects a canonical prefix, refuses lost/corrupt/unadmitted source through owner exception types rather than an empty list, splits document-local identity/count checks from host membership/native admission, and the claimed 390-byte / depth-39 / 27,829,365-byte figures recompute from the pinned estimators under the stated conditions. Author checks reproduce byte-for-byte. Independent counterexamples, including forgeries that pass embedded checks, fail in the ways the subject claims.

Fix S1 when convenient. Do not treat this accept as Report1 integration, product storage, browser delivery, or milestone completion.

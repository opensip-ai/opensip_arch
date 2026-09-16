# Native wire carriers, TS2 and Rust3: author candidate 05

**Standing.** This is an AUTHOR correction candidate for root and fresh independent review. It is not approval, source promotion, product integration, a production codec, admission, sender or generator, and it claims no platform or M2/M3 qualification.

It answers independent review 04 (`/tmp/opensip-implementation/m1-native-wire-owner-review-04`, verdict changes-required): four required findings RF-1..RF-4 and advisories A-1..A-5.
- **Subject reviewed:** frozen `m1-native-wire-owner-subject-04`, sibling manifest sha256 `fdd640ff2888f260d9095fb21dcc9cb055ba39e2ca97039a490398cfc8fbb266`.
- **Root reproduction:** root reproduced 478 checks and 108 mutants from the 39 inputs; its evidence is `m1-native-wire-owner-root-validation-04`.

Custody:
- **Read-only inputs.** Architecture, product, frozen subjects and historical reviews were read-only.
- **Writes.** I wrote only under this directory.
- **Nothing else.** No subagents, network, background tasks or private sessions were used, and nothing was committed or pushed.
- **No frozen imports.** Nothing was imported from a frozen subject.
- **Bytecode.** Every Python run used the reference interpreter with `-I -B`, `env -i` and a private bytecode prefix under `tmp/`. No `__pycache__` or `.pyc` exists outside `tmp/`.
- **Prior evidence preserved as byte copies (verified with `cmp`):**
  - `prior/subject-04/` and `prior/subject-04-manifest.json`: candidate 04 results (478/0, 108/108) and its successor documents;
  - `prior/review-04/`: `review.json`, `review.md`, `probe_dialect_scope.py` with its output, `probe_sender_prepared.py` with its output, `probe_ts2_boundary.out.json`, `mutants.py` with its output, `custody-after.json`;
  - `prior/root-validation-04/`: `stdout.txt` (478/0), `stderr.txt`;
  - all earlier `prior/` directories, unchanged.

## Candidate paths

Everything is under `/tmp/opensip-implementation/m1-native-wire-owner-author-05/`. `tools/filelist.py` is the complete execution closure with 40 `INPUTS`.

**Declarative outputs (built):**
- `wire-carriers.v1.json`
- `owner-pattern-successor.v1.json`
- `public-route-successor.v1.json`
- `successor.json`
- `admission-vectors.json`
- `p3-guard-successor.v1.json`
- `field-coverage.json`

**Reference and check code:**
- `check.py`, `selftest.py`
- `tools/owner_successor.py`, `tools/representability.py`, `tools/sender_ref.py`
- `tools/check_static.py`, `tools/check_reference.py`, `tools/check_routes.py`
- `tools/rules.py`, `tools/public_routes.py`, `tools/succ.py`, `tools/vectors.py`, `tools/build.py`, `tools/common.py`, `tools/filelist.py`
- `tools/outcome.py`, `tools/isolation.py`, `tools/manifest.py`
- unchanged support: `tools/wirecodec.py`, `tools/patterns.py`, `tools/admission_ref.py`, `tools/records_*.py`, `tools/ecma_probe.js`

**Results:** `check-result.json`, `selftest-result.json`, `isolation-result.json`, `outcome.json`, `subject-files.json`.

**Changes from candidate 04:**
- 8 new architecture pins (44 in total): the foundation documents of the identity-model.v3 local registry closure. They are import-source-context, enumeration-plan v1, subject-inventory v1, evaluator-emission-plan v1, target-attribution v1 and v2, incoming-search v1, and execution-inputs v1.
- 1 new input, `prior/review-04/probe_dialect_scope.out.json`, which the checker replays.
- A new admission rule, `RELATION-PAYLOAD-PATH-LAW` (54 rules in total).
- The planner entry-bound param `entryBounds`.

```
cd <subject>; PY=/tmp/opensip-implementation/metadata-reference-env/bin/python
R() { env -i PATH=/usr/bin:/bin HOME=/tmp OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch TMPDIR=$PWD/tmp PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=$PWD/tmp/pycache $PY -I -B "$@"; }
R tools/build.py; R tools/vectors.py; R tools/manifest.py --inputs-only; R check.py; R selftest.py; R tools/isolation.py; R tools/outcome.py; R tools/manifest.py
```

## Per-finding dispositions

### RF-1: defaulted partially stale prepared sets: bounds judged on the rows actually carried

**Selector.** `tools/representability.py` `prepared_output_set_admit_successor`, which wraps the owner `prepared_output_set_admit` (function and callee-closure source digests are in `public-route-successor.v1.json`). The rule is `PREPARED-V3-WIRE-LIMIT`.

**Published change: which rows are judged.** Review-04 asked for the check on "the rows that would actually be selected". A retained prepared set carries **every** row in its `PreparedOutputManifest`:
- `PREPARED-V3-ENTRY`: `entries[i]` answers `rows[i]`;
- `PREPARED-V3-SET-JOIN`: the host recomputes `preparedOutputSetId` over `[entries[*].planRow]`.

So stale and failed rows travel with the usable rows. The candidate therefore judges the bound (rows and blob bytes) over the carried rows, for **every non-rejected owner outcome**: `admitted`, and the defaulted partial-stale `fallback-non-prepared`. The owner's usable rows are a subset of the carried rows, so the carried bound implies the usable-row bound.

`wireLimitBasis` publishes `carriedRows`, `carriedBlobBytes` and the owner partition `ownerUsableRows + ownerStaleRows + ownerFailedRows = carriedRows`. The partition check `PREPARED_ROW_PARTITION` is a stated defensive branch: the pinned owner always partitions.

**Outcomes:**
- **Explicit mode, over the bound:** refuses with `native.prepared-output-exceeds-wire-limit`.
- **Defaulted mode, over the bound:** the set is not selected. The outcome is `fallback-non-prepared` with zero usable rows, the owner `staleRows` kept, `wireLimitDisclosure` listing the faults, and `ownerOutcome` and `ownerDisclosure` retained. The same holds for a partially stale set.
- **Defaulted, within the bound:** the owner partial-stale fallback is unchanged (for example 255 usable rows of 256).

**Precedence (owner refusal precedence preserved; now stated in the rule, the route selector and the route row, A-3):**
1. prepared path representability, before the owner, over every row;
2. owner non-inert;
3. owner stale, explicit mode only;
4. wire limit.

**Planner defence in depth.** `REQUEST-WIRE-ACCOUNTING` `params.entryBounds` makes the planner refuse any manifest whose entry count exceeds `maxSnapshotEntries`, `maxDependencySourceEntries` or `maxPreparedOutputEntries`. The fault is `entries:<Manifest>`, reported before frame faults.

**Vectors** (all run through the pinned owner with the successor installed):
- `PREPARED-V3-WIRE-LIMIT` (24):
  - defaulted, one stale row in 300: fallback, disclosure `entries`, 0 usable, basis 300/299/1;
  - defaulted, one stale row in 257 (256 usable): fallback, because carried rows are counted;
  - defaulted, one stale row in 256 and in 10: owner fallback kept, with 255 and 9 usable rows;
  - stale plus blob-byte over, including an over-limit blob on the stale row itself;
  - all 300 rows stale;
  - a failed row with 300 rows (defaulted, fallback) and a failed row with 10 (explicit, admitted) or 257 (explicit, refused);
  - explicit stale plus over-limit: owner stale refusal;
  - non-inert, and non-inert plus stale, in both modes: owner not-inert refusal.
- `PREPARED-V3-PATH-REPRESENTABILITY` (13): a bad site path combined with stale rows, a non-inert row or over-limit rows, in both modes, refuses on the path key. The review's dylib row plus bad generated path also refuses on the path key.
- `REQUEST-WIRE-ACCOUNTING` (27):
  - 256 prepared entries accepted; 257 and the review's 299 refused as `entries:PreparedOutputManifest`;
  - Rust3 snapshot entries at the bound accepted, one over refused;
  - dependency entries one over refused;
  - TS2 snapshot entries at the bound accepted, one over refused.
- `route-prepared-modes` also executes defaulted-257 with one stale row (fallback, 0 usable) and defaulted-10 with one stale row (owner fallback, 9 usable).

### RF-2: ECMA interpretation restricted to declared owners

**Closed scope** (`owner-pattern-successor.v1.json#/scope`):

| Scope id | Document | Consumer (module instance) |
|---|---|---|
| native-evidence-model | native-evidence.schemas.v2 | `native_evidence_model.v2` `SCHEMAS` via its `C` (`validate_native`, `native_identity`, `file_manifest_identity`, dependency and prepared set admission) |
| provider-startup-model | the same evidence schema copy `BUNDLE` | `provider_startup_model.v1` `validate_startup` via `REGISTRY` |
| provider-wire-model | occupancy-companion.schema.v1 `COMPANION` | `provider_wire_model.v1` `validate_wire` / `admit_fact_batch` via `REGISTRY` |
| identity-model-v3-registered-records | relation-payload-schemas.v2 (its `_LOCAL_REGISTRY` copy) | `identity-model.v3` `validate_registered_record` |

**Mechanism: no global monkeypatch.**
- **No canonical changes.** No `canonical.py` module object and no `ExactValidator` class is modified.
- **Scoped view.** In each scoped module instance only the module-level name `C` is rebound to `ScopedCanonical`. Its `validate` replicates `canonical.validate` (typed, then `ExactValidator.validate`). Its validator extends that module's own `ExactValidator` with a `pattern` keyword that is ECMA-262 /u **only** for schema nodes carrying `x-opensip-successor-ecma-pattern`. Every other node goes to the pinned evaluation.
- **Marks.** Marks are added only to pattern nodes of the scoped document object that the module holds; registries are rebuilt.
- **Untouched.** `NE.IM` (identity-model.py v2), `NE.STARTUP`, `NE.WIRE` and `WI.FP` are left exactly as pinned.

**Parents.** `evidence`, `occupancy`, `relationRegistry2`, `canonical`, `nativeModel`, `startupModel`, `wireModel` and `identityModel3`. `selectorSources` adds the callee closure of `identity-model.v3` `validate_registered_record`.

**Executed checks:**
- **`owner-successor-scope-installed`.** Each scoped consumer refuses `x<LF>/../y.rs` and admits `a/..<LF>` under the successor, while the pinned model differs. Only the four scoped instances carry the view; `NE.IM.C`, `NE.STARTUP.C`, `NE.WIRE.C` and `WI.FP` do not. The marked documents are exactly {evidence, occupancy, relation-payload}, the pinned instances have no marks, and the canonical `pattern` validators are the untouched Draft 2020-12 ones.
- **`owner-successor-no-change-set-closed`.** The set of non-parent documents review-04 found affected (from its replayed `probe_dialect_scope.out.json`), minus the now-scoped relation registry, equals `noChangeDocuments`: identitySchemas2, identitySchemas3, workflowCommon, c2v3 and rust2.
- **`owner-successor-no-change:<document>`**, one per document. It runs every review-04 changed example (plus a path corpus for `LogicalPath`) through the real consumers, pinned and successor, and requires equal results. Each example is also shown to be a real ECMA/Python difference, and a marked node through the scoped view would take the ECMA result, so the checks are not vacuous. Consumers:
  - identity v2: `NE.IM.validate_registered_record` and identity-model.v3 `validate_registered_record`;
  - identity v3: identity-model.v3 `validate_registered_record`;
  - workflows common: native `validate_workflow`;
  - c2v3 and rust2: the pattern evaluated through all four scoped canonical views.
- **Fact-plane owner: `fact-plane-path-law-no-change`.** `check-fact-plane.py` `_is_path` (pin `checkFactPlane`) has no lookahead. It splits on `/` and refuses control scalars, so it never admits a real dot segment, refuses every terminator-hidden segment, and is identical under the successor. **No fact-plane change is required.** It is stricter than the corrected schema on legitimate control-bearing names (`a/..<LF>`, `a<LF>b`), and also refuses `a//b` and `a/`; that is existing fact-plane law, recorded and unchanged.

**The "unchanged" list is corrected.** It now states:
- every canonical module object and class;
- every document outside the scope, for every consumer, including the scoped instances;
- identity-model.py v2 and every nested model copy;
- the pinned module-level `RELATION_DOCUMENT` of identity-model.v3 (only its registry copy is scoped);
- the model-local regexes;
- all non-pattern keywords.

**Controls in both directions:**
- narrowed: `r4_patch_native_only_not_other_scopes`, `rf2_scope_narrowed_startup`, `rf2_scope_narrowed_wire`;
- widened: `rf2_scope_widened_global_ecma`, `rf2_scope_widened_identity_documents_marked`, `rf2_no_change_document_dropped`.

### RF-3: relation-payload CanonicalPath in the corrected closure

**Row and closure.**
- `schemaPatternRows` now has 35 rows: 34 in the evidence schema and 1 in the relation-payload schema, each equal to the raw defect-token count of its document.
- `relationPayloadPathSites` is recomputed from the pinned document, and `RELATION-PAYLOAD-PATH-LAW` `params.sites` is built from it. The four sites are `FilePayloadV1.path`, `PackagePayloadV1.manifestPath`, `VcsChangePayloadV1.path` and `VcsChangePayloadV1.previousPath`.
- Nothing in identity documents or in other schema dialects is changed.

**Driven through retained fact admission.**
- `vectors:RELATION-PAYLOAD-PATH-LAW` has 24 vectors, 6 per site, run through identity-model.v3 `validate_registered_record`.
- That is the call `registered_payload` (retained fact admission) makes for every relation payload, and the check verifies the call in the pinned source.
- Refused with `REGISTERED_RECORD`: `x<LF>/../y.rs`, `x<U+2028>/./y.rs` and `../y.rs`. Admitted: `src/a.rs`, `a/..<LF>` and `a<LF>b.rs`.
- `relation-payload-sites-covered-and-pinned-divergence` shows that at all four sites the pinned model admits a hidden dot segment and refuses `a/..<LF>`.

**Not driven.** A full `admit_frame` over a retained Run bundle; none is available here. This is stated in the rule and the check detail.

### RF-4: reference sender enforces the Cancel law

**Plan.** The plan carries `cancelEcho`: the planned `executionId`, `analysisOrdinal` and reason, plus the Hello, OpenUniverse and Analyze slots.

**What `sender_ref.consume` refuses:**
- `cancel-before-hello`: a Cancel before the Hello slot has been sent (P3 `*PRE_COMPLETE` excludes START).
- `cancel-echo`: any Cancel that is not exactly `expected_cancel(plan, slotsConsumed)`. That means `executionId` null until OpenUniverse has been sent and then the planned value, `analysisOrdinal` null until Analyze has been sent and then the planned value, and reason `user-interrupt`.
- Also: a second Cancel or any frame after it, sequence, frame type, chunk schedule, seal count and exact payload bytes.

**Defensive branches, stated honestly** (module docstring, rule text and `params.defensiveBranches`):
- `cancel-over-reserve` cannot fire once the echo is exact, because the reserve is the maximal echo.
- `frame-limit` and `request-limit` cannot fire for a transcript that conforms to a plan accepted under the same limits.

**Vectors: `HOST-SEND-SCHEDULE` (34):**
- Cancel before Hello (Rust3 and TS2);
- null echo after Hello; execution echo after OpenUniverse; full echo after Analyze (Rust3 and TS2);
- wrong same-length `executionId` (Rust3 and TS2); `executionId` before OpenUniverse; null `executionId` after it;
- wrong, null and early `analysisOrdinal`; wrong reason; a longer `executionId` (now `cancel-echo`);
- payload-byte divergence on the same frame type (OpenUniverse) and with the same chunk coordinates (`SnapshotFileChunk` `snapshotId`);
- consumption under lowered limits (frame limit, request frames, request bytes), plus TS2 having no totals.

**Executed.** `sender-cancel-echo-matches-cancel-nullability` compares the sender echo law with `admission_ref.cancel_nullability` at all 17 positions of a Rust3 and a TS2 plan. The planned echo is accepted by both, and each single-field alternative is refused by both.

**Remaining meaningful mutants are controls:** payload-bytes check removed, request-limit and frame-limit re-checks removed, Cancel before Hello allowed, echo unchecked, ordinal echoed before Analyze, rule text weakened.

### Advisories

| Advisory | Disposition |
|---|---|
| **A-1** | `route-remedy-keying` binds each (key, fault kind) to its condition phrase: `generated-logical-path-owner-schema` to "generated-file logical path"; `site-path-owner-schema` to "prepared output site path"; other path faults to "dependency source file path"; each also needs "'..'" and "cannot be carried". `entries:<Manifest>` needs "entry" and "limits". 20 pairs are executed. The `native.provider-input-not-representable` remedy is unchanged: "…or a dependency source file path, prepared output site path or generated-file logical path with a '.' or '..' segment, a leading '/', or an empty or drive-prefix segment where its path law forbids them; rename or exclude it - nothing is normalized". The `native.provider-input-exceeds-wire-limit` remedy is unchanged: "…does not fit the provider protocol frame, entry or request limits under the host's canonical send schedule; reduce or split that input - nothing is truncated or re-chunked". Control `r4_remedy_drop_generated_phrase`. |
| **A-2** | Stated defensive, and exercised by consuming plans under lowered limits. Controls `r4_sender_no_request_limit_recheck` and `a2_sender_no_frame_limit_recheck`. |
| **A-3** | Precedence stated in the rule text, the route selector `applies` and the route row; vectors in both modes. Control `a3_precedence_text_dropped`. |
| **A-4** | `successor.json` `futureQualification` lists the duties, checked by `integration-duties-declared`: source-bridge promotion of the in-memory rows and scope; production Rust/TS matchers with ECMA semantics for `[\s\S]*` inside a lookahead; an M3 sender with the Cancel echo law; generator support; renderer rebase; the D9 exit-contract successor; fact-plane/relation-registry promotion and a retained-closure run; prepared read authority for a partially stale fallback set. |
| **A-5** | Exact pins retained: 44 (the 36 of candidate 04 plus the 8 registry-closure documents), plus the Node 24.16.0 pin, verified before and after the run. The Node system libraries (CoreFoundation, Security, libc++, libSystem) are a trusted, unselected boundary. The `open`/`subprocess.Popen` audit is closure evidence, not confinement. |

## Substantive findings

1. **Carried rows versus usable rows.** Carried rows, not usable rows, are what the wire must bound. A defaulted set with one stale row among 257 has 256 usable rows but a 257-entry manifest, and it is now not selected. Counting usable rows alone would reproduce the review-04 carrier `ARRAY_BOUND` failure.
2. **Occupancy's pinned defect differs.** Pinned occupancy `LogicalPath` refuses both `x<LF>/../y.rs` and `a/..<LF>`. Its defect is the Python `$` before a final newline, not the lookahead. The scoped successor admits the legitimate name.
3. **Fact-plane path law.** The fact-plane `_is_path` needs no correction for the terminator defect, but it refuses every control-bearing path. Legitimate newline names admitted by the corrected relation schema would still be refused at fact-plane admission. This is recorded, not changed: it belongs to the fact-plane unit.
4. **Identity LogicalPath stays pinned.** Identity v2/v3 `LogicalPath` keeps its pinned Python evaluation (for example `a/..<LF>` is refused). Any change there belongs to the identity unit and is not made.
5. **Worker duty for partial-stale fallback.** A partially stale fallback set within the bound still carries its stale and failed rows. The worker must never read them; this is listed as an integration duty.

## Evidence

- **Check:** 567 checks, 0 failed (`check-result.json`).
- **Selftest:** 132/132 mutation controls caught with a clean baseline (reviewer-01 14, reviewer-02 13, reviewer-03 8 and reviewer-04 4 mutants adapted, plus controls for every review-02, review-03 and review-04 finding and material advisory).
- **Admission vectors:** 333 vectors in 30 groups; 25 rules exempt with reasons.
- **Isolation:** copies only the 40 inputs, reruns check and selftest, and requires identical check IDs and outcomes (`isolation-result.json`).
- **Outcome:** `outcome.json` resolves every review-04 RF/A row against named checks, and retains the review-03 (R3-) and review-02 (R2-) rows.

Corrections during this round, disclosed:
- **Build failure:** `tools/succ.py` lost a closing bracket during editing; found by the parse step and fixed.
- **Failed check, first full run (567 checks, 1 failed):** `relation-payload-sites-covered-and-pinned-divergence` failed because its source probe searched too short a window after `def registered_payload(`. It now matches the exact `validate_registered_record(row['document'],row['selector'],value)` call; rerun: 567/0.
- **Wording mismatch before the first run:** the scope-declared check first looked for a word the law text does not contain; it now requires the law's "Outside scope every pattern keeps its pinned evaluation".

## Not claimed

- approval or acceptance
- product integration
- production decoder, admission, sender or generator
- platform or M2/M3 qualification
- that the pinned owner source files are changed (the successor is applied in memory; root promotes nothing here)
- a full retained-closure `admit_frame` run
- commit or push, or a clean git state
- general filesystem confinement
- the Node system libraries

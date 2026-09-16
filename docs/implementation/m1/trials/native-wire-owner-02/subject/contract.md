# Native wire carriers, TS2 and Rust3: author candidate 02

**Standing.** This is an AUTHOR correction candidate for root and fresh independent review. It is not approval, a production wire decoder, production admission, an analyzer, a generator or product code. It addresses independent review 01 (`/tmp/opensip-implementation/m1-native-wire-owner-review-01`, verdict changes-required: six required findings and ten advisories), plus the root decisions given for this round.

Every architecture, product, frozen and evidence byte was read-only. Candidate 01 (`m1-native-wire-owner-author-01`), frozen subject 01 and review 01 are preserved unchanged, with local byte copies of their results under `prior/`. Nothing was committed or pushed. My earlier author choices are not treated as authority over owners.

## Files

`subject-files.json` is the explicit, complete subject file list. It does not list itself.

| Group | Contents |
|---|---|
| inputs (27) | `wire-carriers.v1.json`, `wire-carriers.meta.schema.json`, `successor.json`, `field-coverage.json`, `admission-vectors.json`, `p3-guard-successor.v1.json`, `reference-environment.json`, `contract.md`, `check.py`, `selftest.py`, the builder, checker, manifest, isolation and outcome scripts under `tools/`, and the frozen method inputs `inputs/ts2-fields.json`, `inputs/rust3-fields.json` and `inputs/generator-candidate03-options.json` |
| outputs | `check-result.json`, `selftest-result.json`, `isolation-result.json`, `outcome.json` |
| evidence | `prior/` (subject-01 results, manifest and review-01 probe outputs); nothing reads it |

```
export OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch PYTHONDONTWRITEBYTECODE=1 TMPDIR=$PWD/tmp PYTHONPYCACHEPREFIX=$PWD/tmp/pycache
python3 -B tools/build.py && (cd tools && python3 -B vectors.py) && python3 -B tools/manifest.py --inputs-only
PY=/tmp/opensip-implementation/metadata-reference-env/bin/python
$PY -I -B check.py && $PY -I -B selftest.py && $PY -I -B tools/isolation.py && python3 -B tools/outcome.py && python3 -B tools/manifest.py
```

`tools/build.py` reads only the pinned architecture snapshot and `inputs/`. No script reads any other `/tmp` author or review directory. The copied `inputs/` bytes equal their origins (hashes recorded in `successor.json` `subjectInputs`). `tmp/` is scratch and is excluded from the subject.

## 1. Required findings

### RF-1: no hidden `/tmp` inputs

- The two field inventories and the generator candidate03 `options.json` are frozen byte copies under `inputs/`, pinned in `tools/common.py` `SUBJECT_INPUTS`.
- The gap-resolution proposal and the review files are listed in `successor.json` `provenanceOnly`. Nothing opens them.
- `check.py` also cross-checks `field-coverage.json` against the frozen inventories (`field-coverage-matches-inputs`).
- `isolation-result.json` copies exactly the 27 input files into a fresh directory and runs `check.py` and `selftest.py` there. Its environment has only `PATH`, `HOME`, `OPENSIP_ARCH`, `TMPDIR`, bytecode flags and a worker count. The isolated result IDs and outcomes must equal the primary run.

### RF-2: complete pinned closure, checked before use

- `ARCH_PINS` holds 35 architecture files. They are the observed transitive closure, including the files the review found unpinned: `discovery-defaults.py`, `native-capability-matrix.v2.json`, `identity-schemas.v2.json`, `capability-manifest-domains.v2.json`, `check-fact-plane.py`, the three workflow schemas, `identity-model.py`, `relation-payload-schemas.v2.json`, and `resolved-inputs.v2.json` for CVE1.
- `check.py` does the following, in order:
  1. Verifies every pin (sha256 and byte length) before importing any architecture code. If a pin fails, it writes a refusal result and stops.
  2. Sets `sys.dont_write_bytecode`, a private `sys.pycache_prefix` and `tempfile.tempdir`, all under the subject `tmp/`.
  3. Installs an `open` audit hook.
  4. Re-verifies the pins after the run.
- It then fails on any of:
  - an architecture read outside the pins (`closure-architecture-reads-pinned`, 35 reads, 0 unpinned);
  - any architecture `.pyc` read (`closure-no-architecture-bytecode`);
  - any `/tmp` read outside the subject copy and the reference environment (`closure-no-hidden-tmp-reads`);
  - an unused pin (`closure-every-pin-used`).
- **This run found an extra gap the review did not name.** Without the private prefix, Python read pre-existing git-ignored `__pycache__` bytecode inside the architecture tree. It is now excluded and checked; the bytecode files themselves were not modified.
- `reference-environment.json` declares Python 3.14.6, jsonschema 4.25.1, referencing 0.37.0, jsonschema-specifications 2025.9.1, rpds-py 2026.6.3 and attrs 26.1.0. `reference-environment-matches` asserts these versions and that both libraries load from the reference venv.
- Extern type names are checked against the frozen generator options (`extern-namespaces-match-generator-options`), and the CVE1 tags against `resolved-inputs.v2` (`cve1-tags-match-owner`).
- **Architecture acceptance uses exact snapshot pins.** Of the 35 pinned files, 22 are modified or untracked relative to HEAD `c3856824` (11 modified, 11 untracked). No commit is required, and no historical approval is modified.

### RF-3: PreparedOutput total bound and fate (root decision)

- `maxPreparedOutputEntries` = 256 is retained as the **total** entry bound: `Rust3PreparedOutputManifestV3.entries` is 0..256, and `outputOrdinal` (entry and chunk) is 0..255.
- `maxExpansionRows` and `maxGeneratedFileRows` stay preparation-set limits and never widen the wire.
- `PREPARED-V3-WIRE-LIMIT` refuses **before spawn** any selected set with:
  - more than 256 inert rows of any kinds;
  - blob bytes over `maxPreparedOutputTotalBlobBytes`;
  - an encoded manifest over `maxFramePayloadBytes`.
- The refusal is `request-rejected` (2) `REQUEST.PRECONDITION_FAILED` with detail `native.prepared-output-exceeds-wire-limit`. It joins the D9 route row family of the non-inert/stale prepared refusals (`native-evidence.md` line 3525, extended by `SUCC-PREPARED-V3`).
- Vectors cover each case with exact encoded length:
  - 256 rows are admitted; 1 directive + 256 expansion rows are refused;
  - blob bytes exactly at the limit are admitted, one over is refused;
  - a 256-row manifest with 1,000 × 256-byte configuration entries (just under 64 MiB) is admitted, and 1,024 entries (over) is refused.

### RF-4: ProviderFault uses worker-observed semantics (root decision)

`RUST3-PROVIDER-FAULT`, parameterized:
- **Worker-observed triple.** The worker reads Hello before writing any frame. `phase` is the P3 phase reached by replaying exactly the frames the worker has read and written. `executionId` is the OpenUniverse value iff the worker has read OpenUniverse, else null. `analysisOrdinal` is the Analyze value iff it has read Analyze, else null.
- **Host possible-phase set.** Let W be the last admitted worker→host frame (Hello if there is none). The host admits the payload iff the triple equals the worker-observed triple after W, or after any prefix of the host→worker frames sent since W.
- **Consequences.** An in-flight OpenUniverse or Analyze admits null or the sent value, jointly consistent with `phase`. A frame the worker provably read (shown by a later admitted worker frame) requires the value.

Deterministic vectors:
- the two reviewer races, `…SnapshotManifest, ProviderFault` and `…Analyze, ProviderFault`, with both lawful triples admitted and inconsistent triples refused;
- an in-flight OpenUniverse, a fault in WAIT_HELLO_ACK, and a fault before Hello (refused).

`p3-race-traces-admitted-by-owner-table` confirms the owner `protocol3_run` admits both races as P3-28. Cancelled keeps the accepted host-send-phase rule (`RUST3-CANCEL-TYPES`).

### RF-5: normative segment-based paths (root decision)

- Paths use two normative lexical rules (`privateRepresentation.lexicalRules`), not patterns:
  - `canonical-path-segments` (rust2 CanonicalPath): split on `/`; every segment non-empty and not `.` or `..`; no U+0000 or backslash; the first segment does not start with `[A-Za-z]:`. The bound is ≤ 4096 UTF-8 bytes for snapshot paths (C-2 `canonicalRelativePath`) and ≤ 4096 scalars for dependency-source paths (the registered bound).
  - `logical-path-segments` (identity LogicalPath): segments of 1..255 scalars, not `.` or `..`, with no NUL or backslash.
- They apply to every path member, **including DependencySource manifest entries and chunks**. There, the registered Native2 CanonicalPath pattern is only supplementary: it admits `a\n/../b`, `a\n//b`, `a//b`, `a/` and `C:x`, all refused here (`native2-canonical-path-pattern-weaker`).
- Newline itself is not forbidden by either owner. `a\nb` is admitted; `a\n/../b`, `a\n//b`, `x\n/..` and `a\n/.` are refused.
- Path scalars carry no pattern.
- `privateRepresentation.patternDialect` declares ECMA-262 `u` semantics without `s`, with `(?![\s\S])` as end of text. A generator must lower every lookaround pattern to a handwritten check, because the Rust `regex` crate has no lookaround; `pattern-lowering-required-declared` lists the scalars that need this.
- `Ts2SnapshotEntryV1.linkTarget` lost its unowned 4096 bound (ADV-6). It is now non-empty, bounded only by the frame limit, and has no lexical rule.

### RF-6: packageKey join, bounds and order (root decision)

- **Order.** `DEPSRC-CUSTODY` entries follow the UTF-8 byte tuple (name, version, sourceId, path) of the exactly joined package row. This equals `DependencySourceSetV1.packages` `x-opensip-order` followed by DependencyFileManifestV1 path order (`depsrc-order-derived-from-owner`).
- **Join.** `PACKAGE-KEY-JOIN`: `packageKey` must byte-equal `name SP version SP sourceId` of exactly one package row.
- **Set constraint.** `DEPSRC-SET-KEY-CONSTRAINTS` (`SUCC-DEPSRC-SET-KEY`) refuses, before Plan binding, a name or version containing a scalar ≤ U+0020, or a constructed key over 4096 scalars. The refusal is `request-rejected` (2) `REQUEST.PRECONDITION_FAILED` with detail `native.dependency-source-package-key-invalid`. With that constraint the key is injective and parses at its first two spaces.
- **Preserved.** A valid empty `sourceId` is kept, so the key minimum is 4 scalars (`a 1 `). Spaces inside `sourceId`, which the owner allows, are kept too (`my-proj 0.1.0 path+file:///my proj`).
- **Bounds derived from the owner.** Row bounds 256 + 256 + 4096 + 2 = 4610 exceed the registered key maxLength of 4096 (`package-key-bounds-derived-from-owner`). A 4096-scalar key is admitted; 4097 is refused.

## 2. Advisories

| Id | Resolution |
|---|---|
| ADV-1 | The architecture is accepted by exact snapshot pins, with git status recorded in this contract; no commit. |
| ADV-2 | `admission-vectors.json` holds 136 id-bound vectors in 23 groups: 22 admission rules plus the P3 overlay state machine. Each group has at least one accept and one refuse vector, executed through `tools/admission_ref.py` using the rule `params`, so a changed parameter changes behaviour. The other 25 of the 47 admission rules are exempt, each naming the executed owner check or its M2 status. `vectors-cover-every-rule` enforces this. All 14 reviewer mutants, adapted to the new structures, are selftest controls with expected check ids. |
| ADV-3 | TS2-G2, TS2-G9, R3-G18 and R3-G19 are attached in `field-coverage.json` `recordLevelGaps`. Two author-added rows cover `Rust3C2StageBudgetV1.unit` and `.limit`. The two array-index rows now use status `carried-positional`. |
| ADV-4 | `transitions.typescript-semantic.unavailableSelection` states that host-phase selection is outcome-equivalent to the owner's payload-observation guard, but the trace ids differ (precheck vs T2-23). |
| ADV-5 | The overlay is published as `p3-guard-successor.v1.json`, with application order and the equivalence to T019's stageIndex==0. `p3-overlay-updates-match-rust2` derives its updates from rust2 T015–T018. The outputSeen reset at Analyze has no behavioural effect in lawful traces (one Analyze, initial false), so it is checked structurally against T015 rather than by behaviour. |
| ADV-6 | Unowned `linkTarget` bound removed. |
| ADV-7 | The orders differ through map-key order: CVE1 sorts keys bytewise, so `contentSha256` compares first, while CBOR sorts length-first, so `kind` and `path` compare first. Anchors differing only in `path` sort identically (`anchor-order-path-only-same`). The delivery.v2 "field-for-field" versus CBOR-order tension is resolved in favour of the more specific TS transport ordering. |
| ADV-8 | The 4096 anchor limit now cites `fact-batch.schema.v3` anchors `maxItems` as the JSON-vector bound; the 100000 wire refusal is stated as outcome-equivalent to the later fact2 mint refusal (`native-evidence.md` 3838–3843). |
| ADV-9 | Commitment rows carry a `valueClass` derived from owner recipe text (`commit-map-value-classes-match-owner`, 12 fields). COMMIT-MAP vectors execute the Rust3 and TS2 frame, StageResult, Complete, Unavailable and BudgetExhausted domains against commitments computed from the owner recipe text, never from the map. |
| ADV-10 | Rust3 interrupt in START cites rust2 `d9Join.rule` (interruption timing) and `native-evidence.md` 3838–3843, both checked. |

## 3. Unchanged and still accepted from candidate 01

These are unchanged and still checked:
- per-key scope2 in both languages;
- fact-ref refusal, the non-empty wire anchor rule and the unnarrowed fact2 ANCHOR_RANGE;
- the raw TS2 manifest digest and the citation correction;
- the non-self-referential dependency-source digest;
- the PreparedOutput V3 value substitution onto PreparedOutputSetV3 rows;
- the `outputSeen` guard;
- the separate TS2/Rust3 CBOR profiles, the byte-string representation, selectors, namespaces, the exec1 grammar and the 100000 anchor count.

No wire member, CBOR type, frame name, protocol major or identity recipe changes. The new typed details (`native.prepared-output-exceeds-wire-limit`, `native.dependency-source-package-key-invalid`) are scoped refusal routes for inputs that cannot be represented on the wire.

## 4. Verification (reference check, not qualification)

- **`check.py`: 299 checks, 0 failed.** They cover:
  - pin-before-import, the closure and environment assertions;
  - grammar, 48 owner member lists, frames, literals (the retained 256 limit included);
  - owner-derived parameters, lexical rules and pattern lowering, the extern closure, map order and citations;
  - coverage against the frozen inventories;
  - all 136 vectors, grouped per rule;
  - reference-owner runs of `native_evidence_model.v2` (scope2, coverage admission, `protocol3_run` differential and races, dependency-source admission and file manifest identity, prepared set admission and identity), `provider_startup_model.v1` and `provider_wire_model.v1`;
  - wire examples under both CBOR profiles.
- **`selftest.py`: 37 controls**, each run as a subprocess on its own subject copy and required to fail a named expected check:
  - 14 adapted reviewer mutants;
  - RF-3..RF-6 and advisory controls;
  - RF-1/RF-2 closure controls: a dropped architecture pin, a tampered pin, a changed frozen input and a wrong package version.
- **`isolation-result.json`** runs both scripts from a fresh copy of only the input files.
- **Not claimed:** `tools/wirecodec.py` and `tools/admission_ref.py` are test scaffolding, not a production decoder or admission. No generator was run; root's renderer trial is separate. There is no M2/M3 qualification.

## 5. Remaining

**Truly remaining contradictions: none.** Items for the reviewer's attention, all owner-derived or root-decided rather than arbitrary:
1. The two new typed refusal details and their D9 route-row extension.
2. The worker obligation to read Hello before writing any frame, which ProviderFault admission relies on. It follows from Hello carrying the major, token and limits negotiation.
3. The outputSeen reset is checked structurally (ADV-5).

**Future qualification, separate from contract completeness:**
- generator support for bytes, variant-record, alias, frame-payload and optional kinds, the lexical rules and pattern lowering;
- M2 production implementation of every handwritten rule, with these vectors as reference;
- M3 codecs and analyzers;
- root binding after independent review.

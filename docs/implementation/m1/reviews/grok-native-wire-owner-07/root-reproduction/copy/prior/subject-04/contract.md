# Native wire carriers, TS2 and Rust3: author candidate 04

**Standing.** This is an AUTHOR correction candidate for root and fresh independent review. It is not approval, source promotion, a production codec, admission, sender or generator, and it claims no platform or M2/M3 qualification.

It resolves independent review 03 (`/tmp/opensip-implementation/m1-native-wire-owner-review-03`, verdict changes-required): four required findings RF-1..RF-4 and advisories A-1..A-9. The subject reviewed was `m1-native-wire-owner-subject-03`, outer manifest `2d68beaa…0cbf4`, which I re-verified as 64/64 before starting.

Custody:
- **Read-only inputs.** Architecture, product, prior subjects, reviews and author-01..03 were read-only.
- **Writes.** I wrote only under this directory.
- **Nothing else.** No subagents, network, background tasks or private sessions were used. Nothing was committed or pushed.
- **Prior evidence retained.** Subject-03 results (373 checks, 78/78 controls), its manifest and the review-03 probe outputs are byte copies under `prior/`.
- **Bytecode.** Every Python run used the reference interpreter with `-I -B` and a private bytecode prefix under `tmp/`. After each run, `__pycache__` outside `tmp/` was confirmed absent.

## Files and how to run

`tools/filelist.py` is the complete execution closure: 39 `INPUTS`. New in candidate 04:
- `owner-pattern-successor.v1.json`
- `tools/owner_successor.py`
- `tools/sender_ref.py`
- `prior/review-03/probe_canon_newline.out.json`, the review-03 engine output that the checker replays

`subject-files.json` is an output and is read by nothing in check or selftest. Isolation copies only the inputs.

```
cd <subject>; PY=/tmp/opensip-implementation/metadata-reference-env/bin/python
env -i PATH=/usr/bin:/bin HOME=$HOME OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch TMPDIR=$PWD/tmp $PY -I -B tools/build.py
  (then, with the same prefix: tools/vectors.py; tools/manifest.py --inputs-only; check.py; selftest.py; tools/isolation.py; tools/outcome.py; tools/manifest.py)
```

## Per-finding dispositions

### RF-1: every relevant wire and extern path site is covered: resolved

**Closed site set.** `wire-carriers.v1.json` `pathSites` is closed and recomputed by `tools/patterns.py` `path_sites`. Its definition:
- every wire scalar carrying a segment lexical rule;
- every string schema node reachable from the carriers through `$ref` whose effective ECMA-262 constraint (its `pattern` and a sibling `not` pattern) admits `a/b` and refuses `a/../b`.

The fixed-form prepared `logicalPath` template is correctly not a site. Result: 10 sites.

| Site kind | Sites | Bound rule(s) |
|---|---|---|
| Wire scalars | `Ts2ProjectPath`; `Rust3CanonicalPath`, `Rust3DependencySourcePath` | `logical-path-segments`; `canonical-path-segments` (normative) |
| Occupancy `LogicalPath` | 1 | `logical-path-segments`, equivalent |
| Evidence path fields | `ExpansionSiteV1.path`, `GeneratedFileV1.logicalPath`, `crateRootPaths/items`, `jsRootFiles/items`, `programRootFiles/items`, `DependencySourceManifestV3` entry `path` | `relative-path-dot-segments`, equivalent (the dependency manifest also has `canonical-path-segments`, narrowed, routed) |

**Complete-string law.** `relative-path-dot-segments` is a new structured lexical rule:
- split only on `/`;
- no segment exactly `.` or `..`;
- no leading `/`;
- no NUL or backslash;
- at least one scalar.

Segments are compared exactly, so `..` followed by a line feed is a legitimate segment and a bare `..` is not. No spelling is coerced or truncated.

**Owner pattern corrected.** The defect was the owner lookahead `(?!.*(^|/)\.\.?(/|$))`, whose `.` stops at a line terminator. The owner pattern successor rewrites it to `(?![\s\S]*(^|/)\.\.?(/|$))` at every occurrence in the owner evidence schema: 34 rows (31 of the `+` form, 3 of the `*` form), recomputed and equal to the raw occurrence count. Carrier extern validation evaluates these effective patterns.

**Executed.**
- **`path-sites-closed`:** published sites equal the recomputed set.
- **`path-site-bindings-executed`:** all 7 schema sites and 8 bindings are run on a 36-string terminator corpus against the pinned engine. An equivalent binding must decide exactly what the effective schema decides; a narrowed binding must be a subset.
- **`vectors:PATH-SITE-SEGMENT-LAW`:** 35 vectors, 5 per site across generated `logicalPath`, expansion-site `path`, `crateRootPaths`, `jsRootFiles`, `programRootFiles`, the dependency manifest `path` and occupancy `LogicalPath`:
  - `x<LF>/../y` and `x<U+2028>/../y` refused;
  - `../y` refused;
  - `a/..<LF>` and `a<LF>b` admitted.
- **`ecma-review03-probe-replayed`:** replays the review-03 Node outputs for the pinned patterns, and shows that the corrected pattern changes exactly the strings with a real `..` or `.` segment after a terminator.

### RF-2: consistent final owner for ECMA vs Python: resolved

**Selected owner.** The declared JSON Schema 2020-12 dialect, recorded in `owner-pattern-successor.v1.json`:
- **Evaluator.** Every owner schema `pattern` is ECMA-262 RegExp with flags `u`. This applies in every loaded `foundation/canonical.py` `ExactValidator` instance: the native model `C` and `IM.C`, the startup model `C` and the wire model `C`.
- **Pattern correction.** The corrected lookahead above, at every occurrence.
- **Model regexes.** Those that compile or mirror owner schema patterns evaluate the same ECMA pattern: `_LOGICAL_RE` (mirror), `_UNIT_ROOT_RE` and `_MEMBER_ROOT_RE` (schema-derived).
- **Completeness.** The complete model regex inventory (10 calls) classifies the rest as model-local, outside the schema-dialect law.

Root preferred fixing the declared-schema semantics; no restriction on POSIX file names was invented.

**Pinned sources.** `selectorSources` holds callee-closure source digests for:
- the canonical validator;
- every native, startup and wire model function that calls canonical validation;
- the wrapped selectors: `dependency_source_set_admit`, `prepared_output_set_admit`, `generated_include_lookup`, `file_manifest_identity`, `_source_kind`, `parse_cargo_lock`.

**Installation.** `tools/owner_successor.py` `install` applies the successor in memory to freshly loaded pinned models, never to source files. It verifies every row's `from` value and rebuilds module registries. The successor selectors refuse to run on an owner instance without it.

**Routes, not exceptions.**
- **Dependency sets, phase A.** Before the owner, a file the owner would hash that fails the owner path schema is refused on `native.dependency-source-not-wire-representable:path-owner-schema`.
- **Prepared sets, phase A.** Before the owner, a site or generated path failing its owner path schema is refused on the new representability key `native.prepared-output-not-wire-representable`, in both prepared modes.
- **Legitimate names.** Legal names reach the owner and are admitted with identities.

**Executed.**
- **`owner-successor-evaluates-ecma`:** the successor `validate_native` equals the Node engine on the corpus. The pinned owner disagrees on `x<LF>/../y`, `x<LF>/..`, `a/..<LF>`, `..<LF>`, `a/.<LF>` and `<LF>/..`.
- **`owner-successor-no-untyped-exception`:** 14 dependency and prepared cases each end as admitted or routed, as expected.
- **`owner-pinned-model-python-re-divergence`:** the pinned defects are reproduced as evidence.
- **`ecma-owner-differential`:** all 28 owner patterns, 87 strings, 0 disagreements.
- **`vectors:OWNER-PATTERN-EVALUATION` (13):** covers `validate_native`, `_LOGICAL_RE`, startup `OpenUniverseV3` validation, owner dependency-set admission with identity, and owner prepared-set admission.
- **Selector vectors:** `vectors:DEPSRC-WIRE-REPRESENTABILITY` (26) and `vectors:PREPARED-V3-PATH-REPRESENTABILITY` (6).

### RF-3: prepared route text and code agree on mode; route semantics strengthened: resolved

**Mode law.** An over-limit prepared set follows the owner PO-1 mode law (nativeMd 1853-1856), derived from the owner text by `prepared-modes-follow-owner-po1`:
- **Explicit mode:** refuse with `native.prepared-output-exceeds-wire-limit`.
- **Defaulted mode:** `fallback-non-prepared`, with a `wireLimitDisclosure` listing the faults, zero usable rows (no partial selection) and no refusal.

The rule params, the selector `modes`, and the route row condition ("…when prepared mode was selected explicitly; when prepared mode was defaulted the set is ignored with a disclosure and owners are analyzed non-prepared (no refusal)") agree. `route-prepared-modes` executes explicit-257 (refused), defaulted-257 (fallback with disclosure) and defaulted-256 (admitted). Vectors cover both modes, each with positive and negative cases.

**Public codes (A-1).** Every key has a `conditionClass`:
- **representability** (the dependency key and the prepared path key): `REQUEST.PRECONDITION_FAILED`, envelope detail `native.provider-input-not-representable`, joined to the non-inert / release-declaration family (row 3525, `D9_MAP` `native.prepared-output-not-inert`, executed owner refusal);
- **bound** (the prepared limit key and the request key): `REQUEST.UNSATISFIABLE`, envelope detail `native.provider-input-exceeds-wire-limit`, joined to the bound-exceeded family (row 3534 "bounded selection array exceeds its published bound, without truncation", `D9_MAP` `PROJECT.SCOPE_LIMIT`).

Both remedies were rewritten so that each is a true next step for every key using it.

**Origin.** `admitted-plan-input` carries actor `external-input`. `route-origin-closed` derives the expected class through the owner `originatingBoundaryLaw` ("Invalid external input is an admission rejection") and requires it to equal the derived termination class.

**Surviving route mutants (A-2) are now caught.**

| Mutant | Caught by |
|---|---|
| Swapped envelope details; wrong remedy text | `route-remedy-keying`, which checks every (key, fault kind) pair the vectors produce (17 pairs) for its condition phrase |
| Dependency timing moved to plan time | `route-timing-anchored`, which binds each owner function to its timing and owner text |
| Origin meaning set to host invariant | `route-origin-closed` |
| Prepared refusal applied only when explicit | `vectors:PREPARED-V3-WIRE-LIMIT` and `route-prepared-modes` |
| Bound key given the wrong code | `route-join` |
| Representability class switched | `route-join` |

### RF-4: planner output bound to the sender schedule: resolved

- **Canonical schedule.** `REQUEST-WIRE-ACCOUNTING` computes an immutable canonical host send schedule. Every chunk of an entry carries exactly the maximum chunk bytes except its last, and a zero-length entry has no chunk.
- **No minimality claim.** The false claim is removed; the rule states "frame-minimal but not byte-minimal".
- **Qualified refusal.** A refusal means the input "does not fit under the canonical host send schedule", never "no lawful encoding exists".
- **Send plan.** The planner returns:
  - `schedule` slots with sequence, frameType, exact envelope payloadBytes, chunk coordinates and seal `totalChunkCount`;
  - `cancelReserve`;
  - totals and seals.
- **Consumption contract.** `HOST-SEND-SCHEDULE` is the private plan-consumption contract the M3 sender must honour. `tools/sender_ref.py` `consume` is the reference, and it refuses:
  - wrong sequence or frame type;
  - chunk-schedule divergence, including a lawful but different chunking;
  - payload-byte or seal-count mismatch;
  - frames not in the plan;
  - a second Cancel, or any frame after a Cancel;
  - a Cancel over the reserve;
  - frame, request-byte or request-frame limit overruns, re-checked after every frame.
- **Independent realization.** `realize` builds the canonical transcript independently of the planner.
- **Kept laws.** The 40-byte prefix exclusion and the single-Cancel law are unchanged.

**Executed.**
- **`schedule-not-byte-minimal`:** a 30-byte dependency file with 24-byte chunks costs 574 envelope bytes greedy, against 572 for `[7,23]` under the owner `wire_cbor`. The reference sender still refuses the `[7,23]` transcript.
- **`schedule-realization-agrees`:** 12 accepted accounting plans are realized independently and consumed exactly.
- **`vectors:HOST-SEND-SCHEDULE`:** 14 vectors, including the 9663676416-byte request consumed with its Cancel at the end, and a lawful alternate chunking at that limit refused.
- **`request-schedule-claims`:** text claims (no positive byte-minimal claim, qualified refusal, Cancel law, `plan2` fate, sender binding).

### Advisories

| Advisory | Resolution |
|---|---|
| **A-1** | See RF-3. Bound keys now use `REQUEST.UNSATISFIABLE`; representability keys keep `REQUEST.PRECONDITION_FAILED`. |
| **A-2** | See RF-3. Remedy keying, timing and origin semantics are executed, not self-consistent copies. |
| **A-3** | The request selector states `planIdFate`: `plan2` is computed but not published; no `run3`, Coverage or worker exists; the termination carries no runId, coverageId or executionId (checked on the derived termination). `anchorScope` limits the line-2848 anchor to timing only. |
| **A-4** | Exact TS2 `SnapshotManifest` frame vectors at 67108864 bytes (180399 entries: 180206 with 250-scalar paths, 193 with 251) and one byte over. The review's doubled TS2 frame limit mutant is caught. |
| **A-5** | Seal `entryCount`, total and `totalChunkCount` are pinned by planner vectors (zero-length and multi-chunk) and by the sender's seal-count divergence. The review's zero-length-counts-a-chunk mutant is caught. |
| **A-6** | Set-admission vectors for `a<LF>/../b` and `a<U+2028>/../b` (routed before owner identity) and for `a/..<LF>`, `..<LF>`, `a/.<LF>` (admitted). `owner-admits-unrepresentable-dependency-inputs` shows the pinned owner admits `a<LF>/../b`. The review's newline-lexical-skip mutant is caught. |
| **A-7** | The rule text states that P3-29 is the only Cancel row, so at most one Cancel is sent. The reserve is counted in the request totals and keeps an interrupt at 130. `request-schedule-claims` checks the P3-29 row count against the pinned table. |
| **A-8** | The 36 exact pins are retained, 23 differing from HEAD `c3856824`. The architecture tree is changing under concurrent work, and no clean-git claim is made. The Node binary is pinned (sha256 and bytes, verified before and after exec). Its system libraries (CoreFoundation, Security, libc++, libSystem) are a trusted, unselected reference boundary. The audit covers `open` and `subprocess.Popen` only and is not a confinement proof. |
| **A-9** | `calleeClosureSha256` for every wrapped owner function in the route successor, and `selectorSources` callee closures in the owner pattern successor, are recomputed by `route-selectors-owner-source` and `owner-successor-selector-sources`. |

## Evidence

- **Check.** `check-result.json` reports every check. At the last full run, 478 checks passed with 0 failures; the final counts are in `outcome.json`.
- **Selftest.** 108 mutation controls: 14 reviewer-01, 13 reviewer-02 and 8 reviewer-03 mutants adapted, plus controls for every review-02 and review-03 finding and material advisory. A clean baseline is required.
- **Admission vectors.** 259 vectors in 29 groups; 25 rules are exempt with reasons.
- **Isolation.** Copies only the 39 inputs, reruns check and selftest, and requires identical check IDs and outcomes.

Corrections during this round, disclosed:
- **Vacuous control fixed.** `rf1_binding_rule_wrong` originally changed an occupancy binding to its own value; it now mutates an evidence-schema binding.
- **Control expectation corrected.** `rf3_translator_dot` now names the owner differential, because the corrected wire closure no longer contains `.`.
- **Rejected outcome cleaned.** A rejected prepared outcome now reports no usable rows.
- **Stale route-join choice revised.** Candidate 03 bound the two limit keys to `PRECONDITION_FAILED`; that choice was revised as described under A-1.

## Not claimed

- approval or acceptance
- production decoder, admission, sender or generator
- platform or M2/M3 qualification
- that the pinned owner source files are changed (the successor is applied in memory, and root promotes nothing here)
- commit or push
- a clean git state
- general filesystem confinement
- the Node system libraries

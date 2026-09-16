# Native wire carriers, TS2 and Rust3: author candidate 03

**Standing.** This is an AUTHOR correction candidate for root and fresh independent review. It is not approval, a production wire decoder, production admission, an analyzer, a generator, product code, or M2/M3 qualification.

It resolves independent review 02 (`/tmp/opensip-implementation/m1-native-wire-owner-review-02`, verdict changes-required): three required findings RF-1..RF-3 and advisories A-1..A-7. My resumed author context is used as context, not as acceptance.

Architecture, product, frozen, evidence, author-01/02, subject-01/02 and review bytes were all read-only. Their results are preserved as byte copies under `prior/`. I wrote only under this directory, and nothing was committed or pushed.

## Files and how to run

`tools/filelist.py` is the static subject file list and the execution closure (A-2). There are 35 `INPUTS`:
- the carrier documents;
- `public-route-successor.v1.json`;
- the vectors;
- `check.py` and `selftest.py`;
- every tool, including `tools/ecma_probe.js`;
- the three frozen `inputs/`;
- `prior/review-02/probe_ecma_compare.json`, the reviewer's independent engine output, which the checker replays.

`subject-files.json` is an OUTPUT written by `tools/manifest.py`. `check.py` and `selftest.py` never read it. `isolation.py` does not copy it.

```
cd <subject>; export PY=/tmp/opensip-implementation/metadata-reference-env/bin/python
E="env -i PATH=/usr/bin:/bin HOME=$HOME OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch TMPDIR=$PWD/tmp"
$E $PY -I -B tools/build.py && $E $PY -I -B tools/vectors.py && $E $PY -I -B tools/manifest.py --inputs-only
$E $PY -I -B check.py && $E $PY -I -B selftest.py && $E $PY -I -B tools/isolation.py
$E $PY -I -B tools/outcome.py && $E $PY -I -B tools/manifest.py
```

(In zsh, spell the `env -i ...` prefix out rather than using `$E`.)

`check.py` sets up a clean run before importing any architecture code:
- It verifies all 36 architecture pins.
- It forces `sys.dont_write_bytecode` and a private `sys.pycache_prefix` under the subject `tmp/`, so stale git-ignored architecture `.pyc` files are never read.
- It sets `tempfile.tempdir`.
- It audits `open` and `subprocess.Popen` events.

## RF-1: every new refusal is joined to the closed public route owner

**Public form chosen (following existing route law, minimal vocabulary).** Each new refusal is an internal decision key with `termination.domainDetail` absent. The `errorCode` names the condition and the key is retained in the operational record. This is exactly the release-declaration route shape (`native.release-capability-unregistered`). `public-route-successor.v1.json` is the scoped successor. It targets:
- `native-evidence.schemas.v2.json#/x-opensip-public-route-registry`;
- `public-detail-registry.v1.json` records (now pinned);
- workflows `common.schema.json` `$defs/DomainDetailCode`;
- `native_evidence_model.v2.py` `PUBLIC_ROUTE_REMEDIES`;
- the `native-evidence.md` section 10 request-precondition route row (line 3525).

**What it adds.**

| internal key | selector (owner function wrapped) | timing anchor | envelope detail |
|---|---|---|---|
| `native.dependency-source-not-wire-representable` | `dependency_source_set_admit` successor; owner refusals keep precedence; a refused set mints no `dependencySourceSetId` | nativeMd 2500 "dependency-source admission, before PlanId" | `native.provider-input-not-representable` |
| `native.prepared-output-exceeds-wire-limit` | `prepared_output_set_admit` successor, only on owner outcome `admitted` (A-6) | nativeMd 1855 "refused before Plan construction" | `native.provider-input-exceeds-wire-limit` |
| `native.provider-request-exceeds-wire-limit` | Plan-time pre-spawn planner (`tools/representability.py`) | nativeMd 2848 "Plan time (no spawn)" | `native.provider-input-exceeds-wire-limit` |

- **Two new public members.** Exactly two `DomainDetailCode` members are added, used only as `envelopeDetail`. `failure_envelope_errors` requires one registered remedy, and no existing remedy is a true next step for these conditions (`remedyKeyingConstraint`).
- **One new origin.** One `possibleOrigins` value, `admitted-plan-input`, is an explicit vocabulary extension. Existing keys, classes, codes, the D9 exit table and the 315 existing members are unchanged.
- **Rules reference routes, not literals.** Admission rules carry `params.route.routeKey`; there are no class, code, exit or timing literals. The meta-schema forbids the old `refusal` literal.

**Executable join (`tools/check_routes.py`).**
- **`route-join:<key>`.** The published rows are applied in memory to the pinned owner model. The owner `public_termination_for`, `failure_envelope_errors` and `CLASS_TO_EXIT` then derive the termination, envelope errors and exit. Results are validated against the real `StepTermination` and `DomainDetail` schemas, extended only by the two published members. The derived termination must have the same members, class and code as the owner release-declaration row: request-rejected, `REQUEST.PRECONDITION_FAILED`, exit 2, no `domainDetail`.
- **`route-join-owner-family`.** Each route-table row's class, code and exit equals the derivation, the owner `D9_MAP[native.prepared-output-not-inert]` row, and an executed owner `prepared_output_set_admit` refusal. The pinned line 3525 row text is also checked.
- **`route-origin-closed`.** Every existing origin is refused for the new keys, and without the successor the keys are unregistered.
- **`route-remedy-not-reused`.** The registry and the common enum stay equal at 315 members. New codes are not registered, not aliased, and their remedies are distinct.
- **`route-timing-anchored:<key>`.** The needle must appear at the pinned line, and the timing token must name that owner phrase. It is also executed: the dependency refusal mints no identity, and the prepared refusal outcome is `rejected`.
- **`route-selectors-owner-source`.** The owner function source SHA-256 (AST segment of the pinned model) is checked, and each wrapper must call the owner.
- **`route-rule-references`.** The same `route-rule-references` check verifies that every rule references a published key, that every key is referenced, and that the selector rule lists agree.
- **Mutation controls.** Every mutation the reviewer reported as uncaught is now caught: class/code changed (`r2_depsrc_class`), `when` changed (`r2_prep_when`), detail renamed (`r2_prep_detail`, `r2_depsrc_detail`). Further controls cover `domainDetail` present, envelope detail unregistered, errorCode changed, route-row exit 4, origin widened, owner digest, timing anchor moved, literal refusal restored, and remedy reuse.

## RF-2: pre-spawn representability and aggregate accounting

**Dependency-source set admission successor.** Rules `DEPSRC-SET-KEY-CONSTRAINTS` and `DEPSRC-WIRE-REPRESENTABILITY` run on an owner-admitted set only. Nothing is normalized, truncated or renamed. They refuse:
- a name or version with a scalar ≤ U+0020;
- a constructed key over 4096 scalars;
- a non-NFC name, version or sourceId;
- a file path that is non-NFC, over 4096 scalars, or fails `canonical-path-segments`.

Executed reachability (`owner-admits-unrepresentable-dependency-inputs`): the owner admits and mints identities for `C:x`, `a//b`, `a/`, a non-NFC path, a non-NFC name and a space in a name; the successor refuses all of them. There are 19 owner-run vectors, covering:
- the review's six paths (`C:x`, `c:/lib.rs`, `a:b/c`, `Z:`, `a//b`, `a/`);
- non-NFC name, version, sourceId and path;
- space in name and in version;
- keys of 4096 and 4097 scalars;
- a 4096-scalar path;
- a newline path;
- DEL (deliberately admitted);
- owner-refusal precedence.

**Prepared set admission successor.** More than 256 inert rows, or blob bytes over 1073741824, refuse. The owner admits 257 rows and over-limit bytes (`owner-admits-over-limit-prepared-sets`). There are five owner-run vectors, including owner non-inert precedence.

**Plan-time planner (`REQUEST-WIRE-ACCOUNTING`, both majors).** The host plans the exact host-to-worker sequence:
- Hello, OpenUniverse, SnapshotManifest, chunks and Seal;
- for major 3, DependencySource Manifest, chunks and Seal, then Prepared Manifest, chunks and Seal iff `preparedOutputSetId` is non-null;
- Analyze;
- one reserved Cancel echoing the execution and analysis.

Accounting rules:
- **Frame size.** Each frame is measured as its exact deterministic-CBOR envelope payload.
- **Byte limits exclude framing.** The 40-byte prefix is excluded from every limit, following rust2 `framing.lengthScope` "payload bytes only" and `limitPolicy.aggregateAccounting` (checked: `request-accounting-law-matches-owner`).
- **What refuses.** Any planned frame over `maxFramePayloadBytes` refuses. For major 3 only (the only limits schema that declares totals), `maxRequestPayloadBytesTotal` and `maxRequestFrames` also refuse.
- **Author choices.** Chunking is greedy (full chunks, remainder last, no chunk for zero-length entries), and one maximal Cancel is reserved.
- **No materialization.** Chunk bytes are represented by length only (`ByteLen`) and never materialized.

Boundaries and verification:
- **Byte-accounting proof.** `request-accounting-closed-form-matches-owner-encoder` proves the byte accounting three ways:
  - 396 chunk-frame cases compared with the owner `provider_wire_model.wire_cbor` encoder across CBOR head thresholds (sequence up to 2^32);
  - the published dependency-manifest boundary recomputed in closed form with the owner encoder;
  - a small request materialized frame by frame (6834 bytes, 10 frames) and also accepted by the carriers.
- **Exact boundary vectors** are solved by `tools/vectors.py` and re-verified by the check:
  - a `DependencySourceManifest` frame of exactly 67108864 bytes (328963 realistic crates.io-key entries) accepted, and one byte over refused;
  - a request of exactly 9663676416 payload bytes (snapshot 8588886016 + 890000 bytes, dependency 1071644672 bytes) accepted, and one over refused;
  - frame counts at and one over a lowered frame limit;
  - a prepared manifest of 256 rows with 1024 configuration items refused and 1000 accepted;
  - TS2 accepted with 10 GiB (no totals) and refused on a 200000 × 4096-scalar manifest;
  - hand-derived frame counts for 0-byte, 3-byte, 2 MiB and 2 MiB + 1 files.
- **`maxRequestFrames` is unreachable.** It cannot be reached by inputs that the other limits accept: the bound is 796198 < 1000000 (`request-frames-bound-unreachable`). It is still enforced.

Scope: set admission and the pre-spawn planner only. A codec refusing malicious worker frames remains a separate M2 obligation.

## RF-3: closed pattern sites and executed dialect

**`patternDialect` is structured.**
- Engine `ECMA-262 RegExp`, flags `u`, evaluation `new RegExp(p, flags).test(value)`.
- Four line terminators, plus dot, dollar and `\s` semantics.
- The pinned reference engine: Node 24.16.0, sha256 `1ee75375…c4b8`, 120573328 bytes, V8 13.6.233.17, ICU 78.3, Unicode 17.0.

**Closed lists.**
- `patternSites` lists every reachable pattern site: 13 wire sites (11 scalars, `Rust3PreparedOutputEntryV3.logicalPath`, `Rust3SubjectV2.subjectId`) and 41 extern sites reached through 66 extern roots and `$ref`. That is 13 distinct patterns, each with document, pointer, negation and construct inventory.
- `loweringRequired` is the closed 53-site subset that needs hand lowering for the Rust `regex` crate (lookahead, `.`, bare `\s`/`\S`). The one site outside it is the negated occupancy `LogicalPath/not` pattern `(^|/)\.\.?(/|$)`.
- `pattern-sites-closed` and `pattern-lowering-closed` require exact equality with the closure recomputed from the pinned schemas.

**Execution.**
- Carrier patterns, and extern JSON Schema `pattern` via an extended validator, are evaluated through `wirecodec.ecma_to_python`. This finite translation covers dot, `$`, `\s`/`\S` and `\uXXXX`, and refuses any other construct or flag.
- `ecma-differential` runs the pinned engine and the translation over all 13 patterns and a 47-string terminator corpus with 0 disagreements. Python `re` disagrees 9 times on the same corpus, shown for contrast.
- `ecma-review-probe-replayed` replays the review-02 engine output exactly.
- `ecma-newline-counterexamples`: for `a/..\n`, `a/.\n` and `..\n`, the engine and the translation admit, Python `re` refuses, `canonical-path-segments` admits, and a DependencySourceManifest carrying them is admitted.

**Mutation controls.**
- `r2_dialect_s` (flags `us`)
- `r2_lowering_scalars_only`
- a removed pattern site
- flipped negation
- translator `$` and `.` defects
- a tampered Node pin

**Execution closure, recorded honestly.** Node's bytes are verified before exec. The only executed program is that binary (`closure-subprocess-exec-pinned`). Its OS dynamic libraries (CoreFoundation, Security, libc++, libSystem) are recorded but not pinned.

**Recorded owner-model divergence.** `owner-model-uses-python-re` shows that `native_evidence_model.v2 validate_native` evaluates the ECMA pattern with Python `re`, so it refuses `a/..\n`, which the declared dialect admits. This is recorded, not corrected here.

## Advisories

- **A-1.** Pins are kept as exact snapshot pins: 36 files, now including `public-detail-registry.v1.json`. Twenty-three differ from HEAD `c3856824`: 12 modified and 11 untracked. The architecture tree is also changing concurrently under other work (for example `docs/implementation/m1/trials/native-wire-renderer-05`). Each check verifies all 36 pins before use and again after the run. No clean-git claim is made.
- **A-2.** The 35-file execution closure is `tools/filelist.py`. `closure-execution-inputs-listed` fails on any subject read outside it; it read 23 of the files. The audit covers only `open` and `subprocess.Popen`. It is not a general confinement proof: listdir, stat and dynamic library loads are not observed.
- **A-3.** `lexicalRules` are structured data executed by `wirecodec.lexical`. Their `text` is rendered from the structure and compared (`lexical-rule-text-rendered`), and the structure is checked against owner text (`lexical-rules-derived-from-owner`). `CANONICAL-PATH-ADMISSION` and `TS2-LOGICAL-PATH-ADMISSION` carry `members` and `externMembers` recomputed from the carrier graph (`path-members-match-carrier-graph`). Rust has 6 wire members plus `Native2DependencySourceManifestV3 /entries/*/path`; TS2 has 5. The extern hook applies `externMembers` from the rule. Both review mutants (drop the chunk path, drop the drive clause) are caught.
- **A-4.** DEL and C1 controls in name and version are stated as deliberately admitted, with vectors. Separate observation: a C1 U+0085 in a Cargo.lock package name makes the owner lock parser refuse (`LOCK_PACKAGE_INCOMPLETE`) before this rule applies.
- **A-5.** `RUST3-PROVIDER-FAULT` states the P3-28 to FAULT conversion. `provider-fault-refusal-same-d9` executes `stage_authority` for both terminal kinds: identical operational-failed 4 `PROVIDER.PROTOCOL_VIOLATION`, no facts, no Coverage, no Run.
- **A-6.** The prepared refusal sits in the selector that wraps the owner `prepared_output_set_admit`; the owner source digest is pinned.
- **A-7.** Confirmed. R3-G19 is the proposal's checker-citation defect, resolved by the SUCC-TS2-MANIFEST-DIGEST citation correction. R3-G18 (common-control owner) stays in `falseGaps[R3-G18]`. Checks: `gap-r3-g19-is-citation-defect` and `gap-r3-g18-is-control-owner`.

## Retained from candidate 02

The following decisions stand unchanged, with their checks retained:
- per-key scope2;
- fact-ref refusal and anchor rules;
- raw manifest digests;
- package-key tuple order and exact join;
- the PreparedOutput V3 entry join;
- the P3 guard successor;
- the commitment map;
- echoes;
- ProviderFault worker-observed semantics;
- CBOR profiles;
- field coverage (TS2 200 rows, Rust3 374).

`successor.json` holds 19 scoped rows (new: SUCC-DEPSRC-REPRESENTABILITY, SUCC-REQUEST-ACCOUNTING, SUCC-PUBLIC-ROUTES, SUCC-PATTERN-DIALECT), the false gaps, and 10 review-02 resolutions, each naming the checks that test it.

## Evidence

- **Check (`check-result.json`).** All named checks, including closure and environment checks. Results are in `check-result.json` and summarized in `outcome.json`.
- **Selftest (`selftest-result.json`).** 78 mutation controls: 14 reviewer-01 mutants, 13 reviewer-02 mutants, and controls for every review-02 finding and advisory. Each control must fail a named expected check, and the baseline must be clean.
- **Isolation (`isolation-result.json`).** Copies only the 35 inputs, verified against `subject-files.json` digests, without `subject-files.json`. It runs check and selftest with a minimal environment and requires identical check IDs and outcomes.
- **Admission vectors.** 176 vectors in 25 groups; 25 rules are exempt with stated reasons.

Corrections made during this round, disclosed:
- `encoded_length` memoized by object id without holding references; a transient envelope's id reuse returned a stale length. Fixed by retaining references.
- Three hand-derived frame-count literals were wrong and are corrected.

## Not claimed

- approval or acceptance
- a production decoder or admission
- a generator run
- M2/M3 qualification
- commit or push
- a clean git state
- general filesystem confinement
- that the owner model's Python `re` pattern evaluation matches the declared ECMA dialect

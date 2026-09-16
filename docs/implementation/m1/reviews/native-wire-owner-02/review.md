# Independent review: native TS2/Rust3 wire owner candidate 02

**Verdict: changes-required.** Three required findings and seven advisories follow.

- **Subject:** `/tmp/opensip-implementation/m1-native-wire-owner-subject-02`, 42 files (the inner list holds 27 inputs, 4 outputs and 10 evidence files; the external manifest covers all 42).
- **subjectManifestSha256:** `5d11f55577dbf5de58cacefb5c43ffd1268263952e639f769fc489c15def0e4d`.
- **Exact set before the review:** PASS (42/42 hashes and byte lengths match; no extra or missing files; no dotfiles, `__pycache__` or `.pyc` in the subject). The result after the review is recorded at the end.
- **Architecture:** `opensip_arch` HEAD `c3856824`. All 35 pins verified. 22 of them differ from HEAD (11 modified, 11 untracked); they are accepted as immutable snapshot pins, and no commit is required for this unit.
- **Standing:** independent review only. This is not approval and makes no generator, production codec/admission/compiler or M2/M3 claim. Nothing was committed or pushed. No private sessions were read. Of the author-02 directory, only its file listing was viewed.

## Reproduction

- **Setup:** fresh copy under `scratch/copy`; `PATH=/usr/bin:/bin`; own `TMPDIR`; reference interpreter with `-I -B`.
- **check.py:** 299 checks, 0 failed. `check-result.json` is byte-identical to the frozen output.
  - Rerun with `PYTHONDONTWRITEBYTECODE`/`PYTHONPYCACHEPREFIX` unset: still 299/0 with the same ids and outcomes. `check.py` forces its own bytecode prefix.
  - Closure: 35 architecture reads, 0 unpinned, 0 bytecode, 0 hidden `/tmp` reads.
  - The tree does contain stale `foundation/__pycache__/*.cpython-314.pyc` files. None was read, and none was newer than my marker afterwards.
- **selftest.py:** 37/37 caught; `selftest-result.json` is byte-identical.
  - It fails from the 27 inputs alone, because it reads `subject-files.json` at import. The real execution closure is 28 files, not the 27 `contract.md` states (A-2).
- **`prior/`:** every file is byte-equal to its review-01 scratch or subject-01 original.

## Review-01 findings

| Id | Status | Independent basis |
|---|---|---|
| RF-1 hidden /tmp inputs | resolved | Inputs frozen and pinned; the fresh copy runs; the audit shows no outside reads |
| RF-2 closure/pins | resolved | Pins checked before import; 35/0 closure; private prefix forced; versions asserted. The closure only covers owners the checker reads, so the unconsulted detail registry falls outside it (new RF-1) |
| RF-3 PreparedOutput | bounds and route resolved; detail join open | 256/255, blob 1 GiB and frame 64 MiB all equal `ProtocolLimitsV3`. See new RF-1 |
| RF-4 ProviderFault | resolved | Reviewer race model, below |
| RF-5 paths | semantics resolved; lowering and dependency reachability open | New RF-2, RF-3 |
| RF-6 packageKey | resolved; detail and NFC open | Probes below; new RF-1, RF-2 |
| ADV-1…10 | resolved (ADV-2 with residue A-3; ADV-9 per author checks) | ADV-7 confirmed by probe: CBOR and CVE1 differ for anchors differing in both digest and path, and agree when only the path differs |

## Owner choices

### PreparedOutput: accepted; its detail is not joined (RF-1)

- **Bound:** 256 is the retained total (`ProtocolLimitsV3.maxPreparedOutputEntries` const 256, nativeMd 2934).
- **Reachability:** an over-limit set is reachable (rows up to 10^6; 1024×256-byte configurations).
- **Refusal point:** the owner already refuses non-inert and stale selections before spawn as `request-rejected`/`REQUEST.PRECONDITION_FAILED` (`native_evidence_model.v2.py:2039-2076`). That is the natural home for the count/bytes refusal (A-6).

### ProviderFault worker-observed semantics: accepted

- **Why the prefix set is complete:** in lawful P3, only host→worker frames can be in flight between admitted worker frames. After Cancel there is no ProviderFault row (`WAIT_CANCELLED` is outside `*PRE_COMPLETE`).
- **Race model** (`scratch/probe_fault_race.py`):
  - Covers 145 worker cuts over 4 transcripts (prepared on/off; 0 or 2 chunks per custody), replayed independently from the P3 rows.
  - Result: 0 lawful triples refused, 0 perturbed triples admitted.
  - Owner `protocol3_run` gives P3-28 for every host-order trace.
  - A mid-stream `ANALYZING` fault after `CoverageV3` is admitted.

### Worker reads Hello before any output: accepted; no new fault suppression

- **Follows from inherited protocol:** START is host-controlled (P3-01). The worker cannot know the major, tokens or limits (byte equality before HelloAck) without reading Hello.
- **Only the trace differs:** the owner table admits `[Hello, ProviderFault]` as P3-28, while the candidate refuses a START-phase payload, which becomes FAULT. `stage_authority` (`:3702-3713`) maps provider-fault and fault identically: operational-failed 4 `PROVIDER.PROTOCOL_VIOLATION`, with no facts, Coverage or Run. State this (A-5).

### Paths: segment rules accepted; lowering rejected (RF-3); dependency application needs a refusal route (RF-2)

`canonical-path-segments` behaves as follows:

| Input | Result |
|---|---|
| `a\n/../b`, `a\n//b`, `x\n/..`, `a//b`, `a/`, `C:x` | refused |
| `a\nb` | admitted |

This matches the rust2 rule text (`rust-provider-protocol.v2.json:466`).

### PackageKey: accepted

- **Join and order:** the owner key is `f'{name} {version} {source}'`, and packages sort by (name, version, sourceId) in bytes. The candidate matches both exactly.
- **Order equivalence:** 20,000 random pairs gave 0 disagreements between tuple order and key-byte order.
- **Boundaries:** an empty sourceId and a sourceId containing spaces are admitted; a 4096-scalar key is admitted and 4097 is refused.

### `native.dependency-source-package-key-invalid`: not joined (RF-1)

## Required findings

### RF-1: the new typed details join no closed vocabulary, D9 map or (dependency source) route row

**Evidence.**
- **Registry:** `public-detail-registry.v1.json` is the single closed public registry (315 records). It lists `native.prepared-output-not-inert` and `native.stale-prepared-output` under "native model D9 mapping". Neither new detail appears in its records, aliases or `newInThisCorrection`.
- **Enum:** `common.schema.json` `DomainDetailCode` is generated from that registry ("unknown names refuse"). The registry file is not pinned and never read.
- **Model:** `D9_MAP` (`native_evidence_model.v2.py:3591-3614`) has neither detail, and nativeMd 3543-3544 makes an unmapped detail a model error.
- **Public form not stated:** nativeMd 3546-3558 and `x-opensip-public-route-registry` say that where no member exists, `domainDetail` is absent and the key goes to the operational record. The candidate never says which form applies.
- **Successor targets:** `SUCC-PREPARED-V3` targets only the prose row at 3525. `SUCC-DEPSRC-SET-KEY` targets no route row at all, and no owner route row exists for dependency-source set refusals.
- **Mutants:**
  - dependency-source refusal changed to operational-failed/`SYSTEM.OUTCOME.ILLEGAL_STATE`: 0 checks fail;
  - prepared `when` changed to "after spawn": 0 checks fail;
  - renaming either detail is caught only by the author's own vector literals.

**Fix.**
- For each detail, publish one public form. Either:
  - (a) add it as a registry/`DomainDetailCode`/`D9_MAP` member through scoped successor rows; or
  - (b) keep it as an internal key with `domainDetail` absent under `REQUEST.PRECONDITION_FAILED`, with a D9 row.
- Add a pre-Plan dependency-source route row and extend the prepared row.
- Pin the registry, and bind class, code, exit and when to owner rows by check.

### RF-2: dependency sources that the owner admits but the wire cannot represent have no pre-spawn refusal

The candidate did not apply the review-01 RF-3 principle here.

**Evidence** (`scratch/probe_depsrc.out.json`).

- **Paths.** The owner `DependencyFileManifestV1` path pattern and `file_manifest_identity` admit `C:x`, `c:/lib.rs`, `a:b/c`, `Z:`, `a//b` and `a/`. `canonical-path-segments` refuses all of them.
  - Snapshot paths are protected upstream: c2 v3 `canonicalRelativePath` forbids a drive prefix.
  - Dependency files are not. `a:b` is a legal POSIX name in git, vendored or imported trees.
  - The candidate introduced this narrowing itself.
- **Frame capacity.** `DependencySourceManifest` is one frame.

  | Entry shape | Encoded bytes per entry | Manifest exceeds 64 MiB above |
  |---|---|---|
  | minimal | 116 | 578,523 entries |
  | realistic crates.io key | ~204 | ~328,964 entries |

  The owner `maxItems` and `maxDependencySourceEntries` are 1,000,000. No DEPSRC rule mentions `maxFramePayloadBytes`.
- **Aggregates.** `maxRequestPayloadBytesTotal` (9 GiB) is below snapshot 8 GiB + dependency 8 GiB + prepared 1 GiB. `maxRequestFrames` (10^6) is at or below the possible dependency entries plus snapshot frames. No rule states the fate of either.
- **NFC.** The set constraint admits a non-NFC sourceId (`e\u0301`), but the wire key refuses it with `NON_NFC`. The owner does not require NFC.
- **Consequence.** Each case turns a reachable input into operational-failed `PROVIDER.PROTOCOL_VIOLATION` or a host invariant fault.

**Fix.**
- Add a dependency-source wire-representability refusal, applied at set admission or at the latest before spawn, for:
  - paths failing `canonical-path-segments`;
  - non-NFC name, version, sourceId or path;
  - an encoded manifest over `maxFramePayloadBytes`.
- Give aggregate request bytes/frames an explicit fate: a refusal or a recorded root decision.
- Classify it as `request-rejected` (2) `REQUEST.PRECONDITION_FAILED` with the RF-1-joined detail.
- Add vectors with exact encoded lengths.

### RF-3: hand-lowering list incomplete; declared dialect not executed

**Evidence.**
- **No list in the input:** `patternDialect.loweringRequired` is prose that says the list is "computed and asserted by check.py".
- **The computed list is scalar-only:** `check_static.py:310-316` scans only `scalars` (11 names) and asserts `len >= 10`. It omits:
  - the inline lookahead patterns `Rust3PreparedOutputEntryV3.logicalPath` and `Rust3SubjectV2.subjectId`, which the declared "scalar/extern" predicate itself excludes;
  - all 7 distinct extern lookaround patterns across the 22 referenced extern roots, including Native2 CanonicalPath and identity LogicalPath.
- **The checker runs Python, not the declared ECMA-262 `u` dialect:** under node ECMA the Native2 pattern admits `a/..\n`, `a/.\n` and `..\n`, while Python refuses them (its `$` matches before a final newline). The lexical rule admits all three.
- **Mutants:** a dialect "WITH `s`" and a narrowed `loweringRequired` text each fail 0 checks.

**Fix.**
- Publish an explicit closed list of `{location, pattern}` covering scalars, inline members and reachable externs.
- Check it for set equality against a computed closure.
- Execute patterns under the declared dialect, or bind the newline vectors.

## Advisories

- **A-1.** Root binding must retain the 22 pinned files that are modified or untracked relative to HEAD.
- **A-2.** The closure audit sees only `open` events and exempts the whole venv. The execution closure is 28 files, including `subject-files.json`.
- **A-3.** Text and implementation are not bound. Dropping the drive clause from `lexicalRules`, or dropping the chunk path from the `CANONICAL-PATH-ADMISSION` text, fails 0 checks, because `wirecodec.LEXICAL` and the extern hook are hardcoded copies. The link between manifest `entries[].path` and the lexical rule exists only in rule text.
- **A-4.** DEL and C1 characters stay admissible in name/version and the key. That is harmless (0 order disagreements); state it as deliberate.
- **A-5.** State that refusing a ProviderFault payload is D9-identical to P3-28.
- **A-6.** Give "before spawn" an owner location: `prepared_output_set_admit`.
- **A-7.** R3-G19 is attached to the SUCC-TS2-MANIFEST-DIGEST citation correction; confirm that is the intended owner.

## Scope items accepted

- **Per-key scope2:** checked against the owner descriptor.
- **TS2 raw manifest digest:** the field is DigestHex; the delivery.v2 domain exists but cannot fit the field.
- **Dependency-source digest:** the owner digest is self-referential ("exact transport manifest frame bytes as sent"), so the non-self-referential successor is needed.
- **Anchors:** the non-empty wire span rule (fact-plane) is separate from fact2's `0<=a<=b<=len` (`identity-model.v3.py:1892`), and it is not narrowed.
- **Fact-ref refusal:** fact2 anchors are closed with no fact reference.
- **Prepared kinds:** inert kinds only (`INERT_ROW_KINDS`).
- **Guard/transition successor:** confirmed by the race model and the P3 differential.
- **Commitment domains and field coverage:** accepted per author checks.
- **Id-bound vectors:** real for parameters; weak for text (A-3).

## Untested limits

- **Not run or re-derived:**
  - No generator was run.
  - The scaffolding is not treated as production code.
  - Commitment classes, scope2 equality and the TS2 digest were not re-derived with new fixtures.
  - The 299 checks and 37 controls were not individually re-derived.
- **Race model scope:** it covers single-Analyze transcripts; Cancel was argued from the P3 table, not enumerated.
- **Reachability not measured:** drive-prefix dependency file names and dependency sets above 329k entries were not observed in real crates.
- **Frame capacity:** computed from synthetic exact-CBOR entries.
- **Audit:** not extended to events other than `open`.
- **Evidence:** full detail is in `review.json`; probes are under `scratch/`.

## Exact set after the review

PASS: after writing review.json/review.md, external manifest sha256 still 5d11f55577dbf5de58cacefb5c43ffd1268263952e639f769fc489c15def0e4d; walk finds 42 files, no extra, no missing, no hash/length mismatch; 35/35 architecture pins unchanged; HEAD c3856824 with the same 11 M / 11 ?? pin status.

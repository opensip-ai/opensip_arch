# Independent review: native TS2/Rust3 wire owner candidate (subject 01)

**Verdict: changes-required.** The candidate is close, but it is not yet sufficient as the single reviewable input for a shared bytes-aware Rust/TS generator plus handwritten admission. Six required findings follow; each has a scoped, concrete fix and none needs a wire change.

- **Subject:** `/tmp/opensip-implementation/m1-native-wire-owner-subject-01`, 18 files.
- **Subject manifest sha256:** `01f4ba5d426f0cf7b80d2232fbdc7c334e994a4a6c13079549d217756c7a0cab`.
- **Exact set before the review:** PASS (18/18; no extra or missing files; every hash and byte length matches). The result after the review is recorded at the end.
- **Architecture:** `opensip_arch` at HEAD `c3856824`, with a dirty working tree. All 29 pins match.
- **Standing:** independent review only. This is not approval and makes no product decoder, admission, compiler, generator-run or M2/M3 claim. Nothing was committed or pushed. The author-01 and root-validation-01 directories were not read.

## Reproduction

- `check.py` rerun from a scratch copy (with `TMPDIR` in scratch): 133 checks, 0 failed. The results are byte-identical to `check-result.json`.
- `selftest.py` rerun: 16/16 controls caught; `selftest-result.json` is byte-identical.
- It does **not** run from the 18 frozen files plus the architecture alone (RF-1).
- Changing unpinned executed dependencies still gives 133/0 (RF-2).

## Five author choices

| # | Choice | Result |
|---|---|---|
| 1 | PreparedOutput per-kind row bounds; oversize manifest is a host invariant | **Rejected** (RF-3) |
| 2 | P3-25 `outputSeen=false`; host never sends Cancel before Hello | **Accepted**. Equivalent to rust2 T019 (`rust-provider-protocol.v2.json:710`), because Coverage always sets `outputSeen` (T017/T018). The published P3 table alone admits FactBatch→Unavailable (reviewer trace P3-23, P3-25), so the overlay is needed. START is host-controlled (Hello is host→worker; `protocol3-transitions.v1.json:342` excludes START). |
| 3 | ProviderFault `phase` = host phase at receipt; Cancelled `observedPhase` = host phase at send | **Split.** Cancelled is **accepted**: after P3-29 any in-flight worker frame is P3-34 (reviewer trace), so in every admitted trace the send phase equals the worker's receipt phase (`rust-provider-protocol.v2.json:457`, `native-evidence.md:3302`). ProviderFault is **rejected** (RF-4). |
| 4 | `exec1_`+32 hex; TS path 4096 scalars; Rust path 4096 bytes | **Accepted.** Owners: `identity-and-evidence.md:63-70`; identity-schemas.v3 LogicalPath and fact.anchors path at 4096 scalars; `c2-plan-stage-schema.v3.json:161` at 4096 UTF-8 bytes. The Rust pattern itself is defective (RF-5). |
| 5 | 100000 anchors at the wire | **Accepted.** `identity-schemas.v3.json:1829` fact.anchors has maxItems 100000, and fact-plane and delivery.v2 give no count bound. The refusal is outcome-equivalent (`native-evidence.md:3838-3843`). |

## Required findings

### RF-1: the checker needs hidden /tmp author inputs

**Evidence.**
- `tools/common.py:8-10,41-43` pins `m1-typescript-wire-translation-01/fields.json`, `m1-rust-wire-translation-01/fields.json` and `m1-protocol-gap-resolution-01/resolutions.md`.
- `tools/check_static.py:22-24` reads all of them.
- A scratch copy with those three paths removed fails with `FileNotFoundError`.

**Fix.** Keep these inputs build-only (`tools/build.py:41-42` is their only content consumer), or freeze copies inside the subject.

### RF-2: the transitive executable/data pins are incomplete

**Evidence.** Pinned models load unpinned architecture files at import:
- `native_evidence_model.v2.py:36` loads `discovery-defaults.py` (modified in the tree);
- `:55` loads `native-capability-matrix.v2.json`;
- `:246` loads `identity-schemas.v2.json`;
- `:2540` loads `capability-manifest-domains.v2.json`;
- `provider_wire_model.v1.py:46` loads `check-fact-plane.py`.

On an architecture copy with three of these files byte-changed, the checker still reports 133/0.

Data owners the IDL depends on are also unpinned:
- CVE1 (`wire-carriers.v1.json:344` → `resolved-inputs.v2.json:688`);
- the generator candidate03 `options.json` that fixes extern type names.

Reference-env package versions are not recorded.

**Fix.**
- Pin all of these files.
- Add a checker assertion that every file loaded from the architecture root is in the pin set. This also covers the lazy loads in `identity-model.v3.py`.
- Record the reference-env package versions.

### RF-3: PreparedOutput row bounds and fate

**Evidence.**
- rust2 `PreparedOutputManifestV2.entries` is `0..maxPreparedOutputEntries` (`rust-provider-protocol.v2.json:385`).
- `ProtocolLimitsV3.maxPreparedOutputEntries` is 256 (`provider-handshake.schemas.v1.json:340`), retained unchanged (`native-evidence.md:2934`).
- The IDL instead sets `entries maxItems 2000256` and `outputOrdinal max 2000255` (`wire-carriers.v1.json:2391,2286`).
- The carrier admits 257 directive entries.
- A change back to 256 fails only `limit-literals`, which pins the author's own sum.
- `maxExpansionRows` and `maxGeneratedFileRows` are set limits. At 10^6 rows the manifest cannot fit the 64 MiB frame, so the widened bound is unreachable anyway.
- delivery.v2 `overflowFate` (`delivery.v2.json:998`) is justified only because a count ≤128 makes overflow a host defect. An oversized Plan-bound set (rows up to 10^6, `native-evidence.schemas.v2.json:2956`) is a reachable input, so `operational-failed/ILLEGAL_STATE` misclassifies it.

**Fix.**
- Keep the retained total: `maxItems 256`, `outputOrdinal max 255`.
- Before spawn, refuse any set with more than 256 inert rows, blob bytes over the limit, or an encoded manifest over `maxFramePayloadBytes`.
- Classify that refusal as `request-rejected (2) REQUEST.PRECONDITION_FAILED` with a typed detail (for example `native.prepared-output-exceeds-wire-limit`), in the same row family as the non-inert/stale refusals (`native-evidence.md:3525`).
- Anything above 256 rows needs an explicit, jointly satisfiable successor for `maxPreparedOutputEntries`.

### RF-4: ProviderFault phase and nullability race

**Evidence.**
- `RUST3-FAULT-CANCEL-TYPES` (`wire-carriers.v1.json:4362`) requires the host phase at receipt.
- P3-28 admits ProviderFault in every `*PRE_COMPLETE` phase, and host→worker frames change the phase.
- `protocol3_run` admits `[… SnapshotManifest, ProviderFault]` and `[… Analyze, ProviderFault]` as P3-28.
- A worker that faulted before reading the in-flight frame can only report the earlier phase. Under this rule that lawful provider fault becomes a protocol violation.
- Null rules: the IDL says "worker has not received", which the host cannot observe; `contract.md:221` says "sent or received".
- D9 is unchanged, but terminalKind, trace and vectors become nondeterministic.

**Fix.**
- `phase` is the worker's phase after the last frame it read or wrote.
- The host admits `phase` iff it is one of the phases entered since the last admitted worker frame (host→worker transitions only).
- For `executionId`/`analysisOrdinal`: if OpenUniverse/Analyze was sent after that worker frame, admit null or the sent value; otherwise require the sent value.
- Add vectors for the two traces above.

### RF-5: Rust3CanonicalPath does not implement the rust2 rule

**Evidence.**
- The pattern at `wire-carriers.v1.json:492` claims the rust2 rule (`rust-provider-protocol.v2.json:466`).
- It uses `.` inside lookaheads, so it admits `a\n/../b`, `a\n//b`, `x\n/..` and `a\n/.` under Python re and under ECMA without the `s` flag.
- Replacing it with the weaker owner pattern is not caught by the checker.
- The owner Native2 CanonicalPath (`native-evidence.schemas.v2.json:669`, used for dependency-source paths) has the same bypass and also admits `a//b`, `a/` and `C:x`.
- Joins currently mask the impact, but a generated validator would encode the wrong language.
- 13 scalar patterns use lookahead and one uses lookbehind. Neither exists in the Rust `regex` crate, and no dialect is declared.

**Fix.**
- Make the segment rule normative in handwritten admission: split on `/`; every segment non-empty and not `.` or `..`; no NUL or backslash; no `[A-Za-z]:` prefix; ≤4096 UTF-8 bytes.
- Apply the same rule inside DEPSRC-CUSTODY.
- Declare the pattern dialect and require generators to lower lookaround patterns to handwritten checks.
- Add newline vectors.

### RF-6: packageKey grammar, bounds and order

**Evidence.**
- Owner row bounds are name ≤256, version ≤256, sourceId ≤4096 with no character restriction or minimum (`native-evidence.schemas.v2.json:1573`). The constructed key can reach 4610 scalars against the registered `packageKey maxLength 4096`.
- The pattern admits an empty sourceId, but `minScalars 5` refuses `a 1 `.
- A space in sourceId breaks the key.
- The order equivalence in `contract.md:143-144` fails when name or version contains a byte ≤0x20. The owner does not forbid such bytes (counterexample `a\x01`).

**Fix.**
- Order entries by the tuple (name, version, sourceId, path) in bytes, which equals `packages` order then path order.
- Make `packageKey` an exact echo join to its package row.
- Add a scoped successor: dependency-source set admission refuses a name or version containing a byte ≤0x20, or a constructed key over 4096.
- Align `minScalars` with the sourceId domain.

## Advisories

- **ADV-1.** 20 of 26 architecture pins are modified or untracked against HEAD. Snapshot or commit them before root binding.
- **ADV-2.** The checks pin literals, not handwritten semantics: 10 of 14 reviewer mutants are uncaught (`scratch/mutants-result.json`). Every admission rule needs id-bound vectors, in particular:
  - PER-KEY-SCOPE2, DEPSRC-CUSTODY, PREPARED-V3-SET-JOIN and RUST3-FAULT-CANCEL-TYPES;
  - the `outputSeen` reset;
  - the COMMIT-MAP terminal domains.
- **ADV-3.** Coverage equals both inventories exactly (TS2 200/200, Rust3 372/372). However:
  - TS2-G2, TS2-G9, R3-G18 and R3-G19 are attached to no row;
  - `Rust3C2StageBudgetV1.limit`/`unit` have no row;
  - two rows use the carrier "array index i".
- **ADV-4.** TS2 Unavailable is selected by host phase, while the owner guards on a payload-derived observation. The outcome is equivalent, but trace ids differ; state this.
- **ADV-5.** `protocol3_run` does not apply the overlay. Publish the overlay as a scoped P3 guard successor for conformance harnesses.
- **ADV-6.** `Ts2SnapshotEntryV1.linkTarget` has a 4096 bound with no owner (`delivery.v2.json:698` has none).
- **ADV-7.** CVE1 strings are length-prefixed, so path-only anchor pairs sort the same under both profiles. The demonstrated difference comes from map-key order. Also record the delivery.v2 AnchorRefV1 "field-for-field" versus CBOR-order tension (`delivery.v2.json:768` vs `fact-plane.v1.json:272`) as resolved in favour of the TS owner.
- **ADV-8.** `contract.md:109` gives the "4096 JSON-vector bound" without an owner.
- **ADV-9.** The COMMIT-MAP terminal and frame domains are consistent with `native-evidence.md:126,129`, but no Rust3 owner vector executes them.
- **ADV-10.** For Rust3 interrupt in START, cite `native-evidence.md:3838-3843` and rust2 d9Join rather than the TS-scoped `delivery.v2.json:1146`.

## Independent positive evidence (summary)

- **scope2 descriptor:** matches `native_evidence_model.v2.py:1500`, `native-evidence.md:1889ff` and `identity-and-evidence.md:287-294`.
- **TS2 raw manifest digest:** matches `delivery.v2.json:850` and `rust-provider-protocol.v2.json:212`.
- **Dependency-source self-reference:** real (`native-evidence.schemas.v2.json:4150,4229`).
- **Anchor rules:**
  - the non-empty wire rule is owner-backed (`fact-plane.v1.json:252`);
  - fact2 stays `0<=a<=b<=len` (`identity-model.v3.py:1892`);
  - the fact-ref refusal is owner-backed (`identity-schemas.v3.json:1829`).
- **Inert kinds only:** owner-backed (`native_evidence_model.v2.py:2011-2012,2047`; `native-evidence.md:2880,3525`).
- **CBOR probes (hand-built bytes):**
  - TS2 decodes negatives down to −2^63; Rust3 refuses major type 1.
  - Both refuse undefined/simple values, floats, tags, indefinite items, non-shortest lengths and byte-string map keys.
  - Empty bytes and hex-as-bytes are refused at the carrier.
  - The two map-order profiles coincide for text keys.
- **CVE1:** the scaffolding matches `resolved-inputs.v2.json:688`.

## Limits

- `wirecodec.py` is author scaffolding, and no generator was run.
- Fixture-heavy joins were accepted from the author's reference-owner checks plus a reading of the owner code, not re-derived with new fixtures.
- Lazy imports in `identity-model.v3.py` were not traced at runtime.
- The scratch architecture copy was deleted after recording its result.
- Full detail and citations are in `review.json`; scratch evidence is in `scratch/`.

## Exact set after the review

PASS. After both review files were written, the manifest sha256 is unchanged (`01f4ba5d…0cab`), and the walk finds 18 files with no extra, no missing and no hash or length mismatch.

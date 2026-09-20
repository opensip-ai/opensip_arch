# Independent review — native record shapes 270

**Standing:** bounded native-Rust review of frozen `native-record-shapes-checkpoint-270`. Closed 125-definition private trust schema compiled to 551 static nodes. Shape admission returns an owned inert value. **Not** typed edge extraction, collection locators, complete shared-budget graph, current/historical population, non-key subjects, other-root contexts, private-policy adoption/merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 269 (`14062a48…5bee`), 268, 267, 266, and 264/265 were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5673276 B, 506 members, SHA256 `7198e69b7a3f87ffb1f8bb28dfb677aa19c9e174ec5e9a320885a1401839337e`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **506/506**. Product-inputs **392/392** live-equal.

Nested parent 269 pin `9e66cc48…f197` (4825912 B / 518 / 386 files) equals the reviewed 269 freeze; live trial tar still matches; `trust-before.rs` equals that 269 `trust.rs` (`25fd3948…7cad`). Nested 265 `73c3b3f5…86df` (2290904 B / 1630) and reader 232 r4 `26bf1187…e2e9` (59724 B / 58) match reviewed archives. Schema source `private-trust-state.schemas.v1.json` SHA256 `1328ba16…4208` (172108 B) equals the 265 extract. `canonical.py` `d47f25db…b442`. `trust_record_reference.py` `00ad3a34…e6df`. `Cargo.lock` unchanged vs 269.

Product vs 269: **392** files, **385** unchanged, **1** changed (`trust.rs` `5fb3ceae…88bb` — only `#[path = "trust_record_shapes.rs"] mod trust_record_shapes;`), **6** added (`trust_record_shapes.rs` `48e02d8d…a8fd` 6390 B; `trust_record_shape_nodes.rs` `fbcee4a5…e131` 201761 B; `trust_record_shape_tests.rs` `9b157eb5…1e7a` 4012 B; `record270-{fragments,patterns,records}.ndjson`). Inherited 269 fixtures unchanged.

---

## What 270 adds

Private generated 551 nodes (`node_0`…`node_550`) from the exact current 265 schema. Generation report: `allKeywordsChecked`, `referenceGraphAcyclic`, 25 patterns, annotation-only `title`/`description`/`x-integration`/`x-installation-outcome-successor`. Closed internal `Definition` enum (125 variants; `named()` 125 arms). No runtime schema compiler/resolver, no new crate dependency, no public API (`mod` inside private `trust`; `lib.rs` does not name it). `admit` is `pub(super)`: product `parse_json` → exact `canonical_bytes` equality → `nodes::shape` → owned inert `V`.

Product JSON profile is **not** signed metadata: 4MiB / 32 containers / integers in `[-2^63, 2^64-1]` / **non-NFC allowed**. Metadata remains 64-container / signed i64 / NFC. `I64Positive` schema maximum is signed i64 max; `u64::MAX` parses and is Shape-refused.

Type-specific JSON Schema keywords stay vacuous on other types; typed `const`; `oneOf`/`allOf`/`not`/`contains`/`if-then-else`; closed properties. `x-opensip-order`: `utf8` / `path` / `(slot,path)` via `ordered()` (strict unique increasing keys); `sequence` preserves given order. `unique()` is exact product canonical bytes in a `BTreeSet`, including object refs, with no hash-collision assumption.

Lexical patterns deliberately differ from later semantic owners:

| Pattern | Shape behavior | Later owner |
|---|---|---|
| loose SemVer | admits `1.0.0-01` and `1.0.0-.` | 267 `Version::parse` refuses both |
| `$` anchors | `dollar()` strips one trailing LF | `(?![\\s\\S])` Hex64 does not |
| `SignedMemberPath` | first char ≠ `/`; remaining no NUL (**first NUL allowed**) | 268 `path_ok` also refuses drive/device/trailing-dot/space/non-NFC |
| `LogicalPath` | negative lookahead `.` does not cross LF (`foo\n.` admits) | normalized paths later |
| `CoreLogicalPath` | 1..=255 **Unicode chars** per segment | byte-width would refuse 255 `é` |

No normalization, namespace, or custody is implied. `node_2` is the sole literal-false fragment (closed `additionalProperties`).

r1 differential: 201 passed / 1 failed — overcap fixture hex exceeded its own 4MiB JSON (`ByteLimit`). r2 compact `rawRepeat` `{byte:32, length:4194305}` reconstructs the actual 4MiB+1 input; admission still refuses. Production unchanged. Clippy 18 `true &&` tautologies from `minItems:0` corrected in the generator only (`a.len() >= 0` stripped). Exact rustfmt regeneration matches frozen node/helper SHAs.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **202/202** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 10 compiled controls + baseline | **11/11**; core fields/patches/source SHA-equal frozen `mutation-check-r1` (stdout SHA differs by thread ids) |
| Exact live | independent Rust admit/pattern probes | **pass** (review-local extra test; frozen product unmodified) |
| Exact live | Python regex vs 25 schema patterns | **57/57** |
| Inspected | 38048 fragments / 551 nodes | only node 2 (literal false) has no positive |
| Inspected | 32300 pattern rows / 25 patterns | newline/NUL/Unicode insertions |
| Inspected | 251 records / 207 positive / 125 defs | includes 71 original coverage + redirected 265 reader checks; expected outcomes are SHAPE+canonical only |
| Inspected | r1 ByteLimit / r2 `rawRepeat` / PrunedTreeRowV2 positive | production unchanged |
| Inspected | 268 workspace 493+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): skip definition shape (`u64::MAX` as `I64Positive`; `reference-extract:record-shape`); skip canonical equality (`"e\\u0301"`; `reference-extract:noncanonical`); skip strict array order (node 41 reversed `TR-*`); skip object uniqueness (node 357 duplicate parent objects); skip conditional then (node 78 invalid `phaseAfter`); skip negative path fragment (node 143 `"."`).

First fail **other** assertions (not exploit proofs):

- `skip-contains` (`node_89` always-true): **wrongShapeAdmissionCaught false**. First fail is overrefusal of valid `clock-write-s4-kept-T` / fragment node 76. Forcing contains-true fires the `writes` if-branch, which then requires `timeEvidence.kind == "new"`; the kept-T record has `writes:["evalHighWater"]` and `kind:"kept"`.
- `signed-first-nul-overrefusal`: pattern 10 / node 413 `"\0"` (valid first-NUL) refused.
- `reject-final-newline-dollar`: pattern 5 `P-MACOS-ARM64-A1-APFS\n` refused.
- `unicode-width-as-bytes`: node 27 long `é` string refused when width is UTF-8 bytes.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`Error`/`admit`/`Definition` not exported from `lib.rs` |
| First-NUL `SignedMemberPath` | pattern and `admit` accept `"\0"`; `"a\0"` is Shape |
| `$` one trailing LF | platform pattern admits; two LFs refuse; Hex64 `END` still refuses LF |
| Loose SemVer vs 267 | `1.0.0-01` and `1.0.0-.` pattern-admit; `Version::parse` is `None` |
| LogicalPath LF | `foo\n.` admits; `foo/.` refuses |
| Core 255 chars | 255 `é` (510 UTF-8 bytes) admits; 256 refuses |
| 268 `path_ok` vs signed | `C:src` / `CON` / `file.` / `file ` signed-admit, package-refuse |
| Product vs metadata encoding | composed `e\u{301}` NullableString admits; `u64::MAX` parses / I64Positive Shape; `"e\\u0301"` NonCanonical; 33 nested arrays Json |
| Overcap | reconstructed 4194305-byte input remains refused |

---

## Remaining (do not count closed)

Source-bound typed references and complete shared-budget graph; current/historical population and non-key subjects; other-root contexts; private-policy adoption/merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. Shape admission mints none of those proofs. 270 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 392 product files: 385 unchanged vs 269. Nested 269/265/232 pins match reviewed archives.
- [x] **202** security tests, Clippy, and fmt reproduced. Ten controls behave as documented (six wrong admissions; four other-first, including skip-contains overrefusal of valid ClockWriteEventV1).
- [x] Generated 125-definition / 551-node closed schema; product canonical profile separated from metadata 64/i64/NFC; lexical patterns independently distinct from 267/268; admit is owned/inert/private.
- [ ] **Not** typed edges, current authority, native custody, or product installation.

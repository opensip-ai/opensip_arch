# Continued independent code review: m1-canonical-subject-03

This is a nonblind continuation of review 01 (session 0b25126b-49da-4a62-ab1c-d5f18b15cebf).
Review 01 withheld its verdict because Bash was denied. In this session Bash was available,
and I executed the checks marked "Claude" below myself.

- **Subject:** `/tmp/opensip-implementation/m1-canonical-subject-03.json`, SHA-256
  `f28bcd791a8c1c6d4d313b2cb87f82363ba7819c2a31877f897581a60642abbc` (recomputed).
- **Unit verdict: ACCEPT-UNIT.** This covers only the lexical, canonical and hash code, the
  developer design binding and verifier, and the root workspace, all at these exact bytes. It is
  not M1, carrier, provider, CLI, performance or release acceptance. All 32 release gates and 54
  recovery cases remain unperformed.
- **Inventory candidate** `docs/implementation/m1/repository-file-inventory.v2.json`
  (`f4352ab3f6249a65bfd95ebf1b2d6086fe9954a20de6597d722222ed71176008`): **CHANGES-REQUIRED**.
  Two small corrections are needed (§5). This does not block the unit verdict: unit acceptance
  does not include inventory conformance, which the successor route owns.

Provenance of evidence:
- **Claude-executed:** commands I ran in this session, with outputs under `results/`.
- **Static:** reading only.
- **Codex receipt:** retained output I inspected but did not produce.

## 1. Subject binding and delta (Claude-executed)

- **Manifest:** the hash matches; all 13 rows match SHA-256 and byte length; there are no extra
  files, no symlinks, and the design-lock hash matches. My adapted `probes/verify_manifest.py`
  gives the same result.
- **Subject02 → 03:** the only change is `canonical_tests.rs:5`, which adds `vec::Vec`.
- **Subject02 failure preserved:** validation-02 still shows test and clippy exit 101 with
  `E0425 cannot find type Vec`.
- **Subject01 → 03:**
  - `canonical.rs` is byte-identical (e5246528…).
  - `digest.rs` → `digests.rs` adds Display/Error (`digests.rs:13-29`) and swaps the hash
    backend (`digests.rs:5,31-33`).
  - `lib.rs:11-21` makes the modules private and adds explicit re-exports.
  - `canonical_tests.rs` changes only module paths and adds the 18-vector test (`:274-359`).
  - `Cargo.toml`/`Cargo.lock` change the dependency; `verify_design.py` and its tests change.

## 2. Root fixes: disposition of review-01 items

| Review-01 item | Successor03 | Disposition |
|---|---|---|
| ADV-01 sha2 → cpufeatures → libc effects | Replaced by `sha2-const-stable =0.1.0` | **Resolved**, per §3. `cargo tree -e all --target all` and `cargo metadata` show only `opensip-identity → sha2-const-stable`, with no normal, build or target dependencies. |
| ADV-03 `digest.rs` name and public modules | `digests.rs`; private `mod`s with explicit `pub use` | **Resolved.** Matches inventory 14:351-352. |
| ADV-10 DigestError traits | Display + `core::error::Error` with `source()` | **Resolved.** Probe `digest_error_is_a_core_error_with_source` passes. |
| ADV-08 verifier looseness | Exact pin keys and types, top-level objects, remaining findings | **Resolved at the stated scope**; small remainder in ADV-R2-03. |
| ADV-07 hash oracle gaps | 18 hashlib padding and size vectors | **Resolved** for raw SHA-256 (§3). The Python cross-link gaps are closed by the new groups plus my 39 probes. |
| ADV-02 H over unadmitted values | Renamed `hash_canonical_value` | **Improved, still forward scope** (ADV-R2-04). |
| ADV-04/05/06 precedence, memory, recursion | Unchanged code | Unchanged. Memory is now measured (ADV-R2-06). |
| ADV-09 evidence binding | validation-03 records subject hash, cwd, argv, output hashes, tool and lock pins | **Resolved.** I rechecked all 12 output hashes, the lock pin and the three executable hashes. |

## 3. Dependency challenge: sha2-const-stable 0.1.0

Challenged points:
- **Provenance metadata is not evidence.**
  - `repository` and `homepage` name `saleemrashid/sha2-const`, but the listed authors are
    different people. So the fork's source is not demonstrably that repository.
  - `.cargo_vcs_info.json` names commit `ca853c81…`, which I did not (and offline cannot)
    confirm exists upstream.
  - It is edition 2018 with no maintenance signal.
  - I infer no endorsement or maintenance. The selection has to stand on the exact bytes alone.
- **Exact bytes** (Claude-executed):
  - The cached `.crate` SHA-256 `5f179d4e…` equals the Cargo.lock checksum.
  - All 35 archive members are byte-equal to the extracted registry source; the only extra
    extracted file is Cargo's `.cargo-ok`.
  - The archive has no `build.rs`.
  - `Cargo.toml` and the four `src` files hash exactly as root's `source-review.json` states.
  - The dev-dependencies (hex, proptest, sha2 0.8) are never built for dependents. Metadata
    confirms this: kinds are `dev`, and the resolve graph has none.
- **Source reading** (static, all four files):
  - No `unsafe`, `extern`, `std`, `cfg`, statics, macros from other crates, or intrinsics.
  - Only integer arithmetic on fixed arrays, inside `#![no_std]`.
  - SHA-256 `update`: block buffering keeps offset below 64, and full blocks compress in place
    (`sha.rs:48-75`).
  - `finalize`: 0x80, then zero padding, then a two-block path when offset exceeds 56, then the
    64-bit big-endian bit length at 56..64 (`:77-100`).
  - Compression follows FIPS 180-4 (`:106-187`). The SHA-256 rotation constants are Σ0 (2,13,22),
    Σ1 (6,11,25), σ0 (7,18,SHR 3), σ1 (17,19,SHR 10) (`:192-204`).
  - Bounds hold by invariant, so nothing reachable panics. The length overflow would need more
    than 2^61 bytes.
- **Independent oracles** (Claude-executed):
  - H256, K256, H512 and K512 recomputed from integer square and cube roots of primes equal
    `constants.rs`.
  - My hashlib recomputation of all 18 subject vectors equals both the Rust literals and
    `hashlib-vectors.json`.
  - A public-API differential over 1535 inputs had 0 mismatches:
    - pattern lengths 0..1100, covering every padding boundary up to 17 blocks
    - 300 seeded random blobs up to 64 KiB
    - all 129 NIST CAVP SHA256ShortMsg and LongMsg vectors, each checked against hashlib first
    - 4194303, 4194304, 4194305, 4194306 and 8388609 bytes
- **Tradeoff:** there is no hardware acceleration. One observation on this host: 34 MiB/s in a
  debug build, 269 MiB/s in release (ADV-R2-01).

On these bytes, a small, dependency-free, auditable software implementation is an acceptable
pure-layer selection under root's literal no-OS-dependency reading. It is not a cryptographic
audit, and any version or byte change needs a new review.

## 4. Behaviour through the new public API (Claude-executed)

- **Adapted probes:** I copied review-01's probes after verifying they byte-equal Codex's
  `probe-subject.json`. The full diff is in `results/probe-adaptation.diff`. Changes:
  - **API only:** in `probes.rs`, `canonical::parse/encode` → `parse_json/canonical_bytes` and
    `digest::{frame,identity,raw_sha256,Error}` → `hash_preimage/hash_canonical_value/raw_sha256/DigestError`.
  - **Targets:** `Cargo.toml` path and `Cargo.lock` point at subject03 and sha2-const-stable;
    `verify_manifest.py` points at subject03 and its hash.
  - **Verifier probes:** the new verifier hash; the four review-01 permissive observations
    inverted to refusals, per the claimed fix; a new `SuccessorPinProbes` class.
  - **New files:** `sha_probes.rs` and `sha_differential.py`.
- **Rust probes:** all 18 pass (15 original groups plus 3 new).
- **Reference differential:** same seeded corpus as Codex (corpus.hex `1b700716…` is identical).
  Over 14000 inputs: 4490 accepts and 9510 refusals, with 0 accept/refuse or canonical-byte
  disagreements against the pinned `canonical.py`, 0 panics, and no output longer than its input.
- **H differential:** all 4490 accepted canonical values: `hash_canonical_value("probe", v)`
  equals hashlib over the literal §3 frame, and equals `raw_sha256(hash_preimage(...))`.
- **Verifier probes:** all 39 pass:
  - the approval chain
  - superseded source rows
  - path escapes
  - rejection of pins with wrong value types, and of non-object pins, locks and approval blocks
  - rejection of non-list `remainingRequiredDesignFindings`
  - the real architecture with 46 inputs, plus altered pins
  - the observation in ADV-R2-03
- **Snapshot validation:**
  - `cargo test --workspace --locked --offline`: 10 passed
  - clippy `--all-targets -D warnings`: exit 0
  - `fmt --check`: exit 0
  - `python3 -B unittest`: 9 passed
  - design verifier: 46 inputs
  - metadata and tree: exit 0
  - No `__pycache__` was written into the snapshot.

**Codex receipts** (not my execution):
- `m1-canonical-root-probes-01` ran my unedited probes against **subject01**: 15 groups,
  34 verifier probes, 14000 cases with 0 disagreements, and the same four H goldens.
- `validation-03` records all six commands exiting 0 on subject03. I rehashed those receipts
  but otherwise relied on my own reruns.

## 5. Inventory candidate assessment

What is right, from my own row-by-row comparison with v1 (`47909b56…`):
- All 198 original rows are unchanged by value.
- The 20 packages and `pendingDecisions` are identical.
- The only other change is the `standing` text.
- No paths are duplicated, and exactly four rows are added.
- `design-lock.json` (repository/manifest) is acceptable.
- `tools/verify_design.py` (tooling/validator) is acceptable.
- `crates/identity/src/canonical_tests.rs` (opensip-identity/test; `<subject>_tests.rs` per
  14:172) is acceptable.
- The `digests.rs` owner is unchanged.

Required corrections before acceptance:
- **INV-01: undeclared cross-package source edge.**
  - The row `tests/conformance/test_design_binding.py` is assigned to package `verification`,
    which declares `dependencies: []`.
  - The file loads `tools/verify_design.py` by path (`test_design_binding.py:10-13`), and that
    file belongs to package `tooling`, also `dependencies: []`.
  - Build-plan 851-854 requires detecting undeclared sibling source imports, and
    `inventory-successor.json:12` says no package edge changed.
  - The test is the tooling validator's own behavioral test, not cross-package contract
    conformance (14:49, 14:296; build-plan 866 treats root `tests/` as fixture and link
    owners).
  - Fix, either:
    - put this test under the `tooling` owner, or
    - add a separately reviewed `verification → tooling` edge. That would change the package
      table, which the candidate says is unchanged.
- **INV-02: the preservation claim is inaccurate.**
  - `inventory-successor.json:19` claims `"originalBytesPreserved": true`.
  - v2 re-sorts all rows by path, so 40+ original rows (docs/*, package.json, providers/*,
    rust-toolchain.toml, schemas/README.md, …) change position, and the original file byte
    sequence is not preserved. Row values are preserved.
  - Fix, either:
    - keep v1 order and insert the four rows, or
    - reword the claim as value-level row preservation with order normalization.

If only these two points change, and the other three rows and all original rows stay the same,
I expect to accept the corrected candidate by its new digest. Nothing here accepts the other
startup refinements, the generation recipe or the metadata proposal.

**Effect on the unit:** subject03 already contains files that the accepted v1 inventory does not
list. Layout conformance is owned by the inventory successor, not by this unit's acceptance. If
INV-01 moves the test, that is a path-only change needing a binding and verifier rerun, not a new
behavioral review.

## 6. Required findings (unit)

None.

## 7. Advisories

- **ADV-R2-01: performance is unqualified.**
  - The software SHA-256 measured 34.1 MiB/s (debug) and 269.2 MiB/s (release), single run,
    16 MiB, this macOS host.
  - The hardware path is gone. Large raw-blob inventories will cost time.
  - The future performance gate should measure this before release; any replacement must keep
    identical bytes and be re-reviewed.
- **ADV-R2-02: dependency provenance rests only on the locked bytes and source review.**
  - Repository metadata points to a different upstream than the authors.
  - The VCS commit is unverified, and there is no maintenance signal.
  - Record `source-review.json` (`593102e6…`) together with the lock checksum in the future
    permitted-graph record.
- **ADV-R2-03: verifier remainder** (`verify_design.py`).
  - "Refuses cleanly" holds for pins and top-level documents (`:44-50,60-67`). A nested
    non-object reference, such as `activation.applicationManifest` as a string, still raises
    `AttributeError` at `:73`, which main's catch set (`:118`) does not cover.
  - My probe observed a non-zero exit with a traceback. It fails closed but is not a clean
    refusal.
  - An absent `remainingRequiredDesignFindings` key passes (`:85`). The pinned real completion
    has `[]`.
  - `:54` `"bytes" in row` is now dead.
- **ADV-R2-04:** `hash_canonical_value(&str, &JsonValue)` (`lib.rs:18-21`, `digests.rs:62-64`)
  still hashes any lexical value under any syntactically valid domain. Future
  `descriptors.rs`/`digests.rs` domain dispatch must consume admitted typed descriptors, and
  `JsonValue` must not become a carrier.
- **ADV-R2-05: no in-repository test uses the public re-export surface.** `canonical_tests.rs`
  uses crate-internal paths, so renaming or dropping a re-export would not be caught. Only my
  external probes cover it. Consider one public-API test.
- **ADV-R2-06: carry-forward, unchanged code.**
  - Measured peak parse memory for 4 MiB inputs: 10–16× input (≤71.3 MiB total).
  - Refusal precedence differs from the reference; both refuse.
  - Recursion on caller-built `JsonValue`s deeper than 32 is unbounded.
  - All belong to future memory, D9 and carrier scope.

## 8. Limitations

- Performance numbers are single observations, not a qualification.
- The dependency review is a close reading plus differential testing, not a formal
  cryptographic or constant-time audit. Inputs are public, so timing was not a concern.
- The upstream repository, commit and maintainer relationship were not verified (offline).
- No Linux or other-target build was executed. The no-target-dependency result rests on
  `cargo tree --target all` and `cargo metadata`, plus source with no `cfg`.
- Codex receipts for subject01 were inspected, not re-executed. Behavioural equivalence on
  subject03 is established by my own reruns.
- My probe expectations are reviewer-authored. The new strictness probes encode the claimed
  successor behaviour.
- Architecture documents beyond the cited passages were not reread.

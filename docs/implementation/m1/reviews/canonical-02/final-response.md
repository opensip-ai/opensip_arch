**Unit verdict: ACCEPT-UNIT for subject03, with no required findings. The inventory candidate is CHANGES-REQUIRED for two small corrections.** The unit acceptance covers only the lexical, canonical and hash code, the design verifier and the root workspace; M1, performance and release are not included. Bash worked this time, so everything below marked as run is my own execution unless I say Codex.

**Subject check (run by me)**
- The manifest hash matches `f28bcd79…`, all 13 files match their hashes and sizes, and there are no extra files.
- `canonical.rs` is unchanged since subject01.
- The only change from subject02 to 03 is the `Vec` import. Subject02's test and clippy failures are still preserved.
- On subject03, `cargo test` passed 10, clippy `-D warnings` and `fmt --check` exited 0, Python unittest passed 9, and the design verifier passed 46 inputs.
- `cargo tree --target all` shows only `opensip-identity → sha2-const-stable`, with no normal, build or target-specific dependencies.

**Challenging the sha2-const-stable choice**
- **Provenance:** I give the package metadata no weight. Its repository field names a different upstream than its authors, and I couldn't verify its VCS commit offline. So acceptance rests only on the exact bytes.
- **Bytes and source:**
  - The cached `.crate` matches the Cargo.lock checksum, and all 35 files in it equal the extracted source. There is no `build.rs`.
  - The source hashes match root's source review.
  - The source has no `unsafe`, FFI, `std` or `cfg`.
  - The SHA-256 padding and compression match FIPS 180-4 on reading.
  - I recomputed the round constants and initial values from primes; they match.
- **Differential against hashlib (0 mismatches):**
  - 1,535 inputs, including all 129 NIST CAVP SHA-256 message vectors and blobs up to 8 MiB + 1.
  - All 18 subject boundary vectors, recomputed independently.
  - H for all 4,490 accepted corpus values.
- **Tradeoff:** one run on this host measured 34 MiB/s in debug and 269 MiB/s in release. Performance qualification is still future.

**Behaviour through the new public API**
- **Rust probes:** I adapted my review-01 probes, changing only API names and targets, and added SHA/H tests. All 18 Rust probe groups passed.
- **Reference differential:** the corpus is byte-identical to the one Codex used. 14,000 inputs gave 0 disagreements and 0 panics against the pinned `canonical.py`.
- **Verifier probes:** 39 passed. The four review-01 "permissive" observations are now refusals, as the successor claims.
- **Codex receipts:** the subject01 probe runs and validation-03 were inspected and rehashed, but they are not my execution.

**Advisories (non-blocking)**
- **Verifier:** a nested non-object reference still raises `AttributeError` outside `main`'s catch set. It exits non-zero with a traceback, so it fails closed but not cleanly.
- **Tests:** no in-repository test uses the public re-exports.
- **Forward scope:** `hash_canonical_value` still hashes any lexical value under any valid-looking domain. Future descriptor code needs to take admitted typed values.
- **Carried forward:** memory is now measured at 10–16× input (≤71 MiB peak for 4 MiB).

**Inventory candidate `repository-file-inventory.v2.json` (`f4352ab3…`): CHANGES-REQUIRED**

The 198 original rows and 20 packages are unchanged in value, and exactly 4 rows are added. Three of the new rows are fine. Two things need fixing:
- **INV-01:** `tests/conformance/test_design_binding.py` is assigned to `verification`, which declares no dependencies. The test loads `tools/verify_design.py`, which belongs to `tooling`. That's an undeclared cross-package import, although the successor record says no package edge changed. It is really the tool's own test. Fix: move it under `tooling`, or add a separately reviewed edge.
- **INV-02:** `originalBytesPreserved: true` isn't accurate. v2 re-sorts all rows, so 40+ original rows change position; only the row values are preserved. Fix: keep v1's order and insert the new rows, or reword the claim.

If only those two points change, I expect to accept the corrected candidate by its new digest. This assessment does not accept the startup refinements, generation recipe or metadata proposal.

Everything is in `/private/tmp/opensip-implementation/m1-canonical-review-02`; I wrote nowhere else.
- review.md
- review.json
- probes/
- results/, including the full probe adaptation diff

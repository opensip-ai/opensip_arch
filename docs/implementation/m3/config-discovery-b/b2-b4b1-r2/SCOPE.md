# B2-b4b1 r2: what the candidate delivers (M3-B unit B2-b4, sub-unit B2-b4b1: the byte census)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements section 2.1 of the accepted B2-b4 plan r4 (`config-discovery-b/b2-b4/PLAN-r4.md`; Codex `codex-b2b4-plan-r4`, after round-3 findings B2B4PLAN-R3-RF-1 and RF-2). Its base is product `ec2d655`: B2-b4a is bound, inventory is v196, and there are 164 contract successors.

## r2 changes (Codex `codex-b2b4b1-r1`, REQUIRED-FINDINGS)

**B2B4B1-R1-RF-1: the platform test accepted a numeric prefix.**
- **The fix.** `recorded` now accepts only an unsigned integer that is the whole JSON value. That means no sign, fraction, exponent or leading zero, and it must be followed only by whitespace and `,` or `}`. Duplicate keys still refuse.
- **New control.** `only_a_whole_unsigned_integer_is_a_recorded_size`: `144` passes, as a spaced or compact value. These each refuse: `144.5`, `144e9`, `144E9`, `144abc`, `-144`, `+144`, `0144`, `"144"`, an empty value and `1440x`.
- **Unchanged.** Nothing else changed, and the census figures are unchanged.
- **Evidence.** Lane r2.

## The outcome: bytes fail too, and they grow with the root spelling

The census now carries bytes for every lead-readable entry and composed workspace, as `base + perRootByte × R` for a discovery root spelled in R bytes. It reports them at R = 134 (the lead probe's root), 1,024 (macOS `PATH_MAX`) and 4,096 (the code's bound on a project root spelling, `path_binding.rs` `components`). No byte margin is claimed. The byte limit is 2^30 (1,073,741,824).

| Entry | base | perRootByte | R = 134 | R = 1,024 | R = 4,096 |
| --- | --- | --- | --- | --- | --- |
| `rs-very-large-aws-sdk-rust` | 552,730,860 | 647,387 | 639,480,718 | 1,215,655,148 | 3,204,428,012 |
| `mr-ts-very-large-smithy-sdk` (workspace) | 143,738,512 | 142,516 | 162,835,656 | 289,674,896 | 727,484,048 |
| `ts-very-large-aws-sdk-js-v3` | 127,858,128 | 134,653 | 145,901,630 | 265,742,800 | 679,396,816 |
| `ts-very-large-aws-cdk` | 94,787,134 | 95,678 | 107,607,986 | 192,761,406 | 486,684,222 |
| `poly-large-rspack` | 90,809,559 | 94,169 | 103,428,205 | 187,238,615 | 476,525,783 |
| `py-very-large-home-assistant` | 65,267,944 | 82,093 | 76,268,406 | 149,331,176 | 401,520,872 |

These entries fail to fit twice in the byte limit:
- **R = 134:** `aws-sdk-rust`.
- **R = 1,024:** `aws-sdk-rust`, which exceeds the limit itself.
- **R = 4,096:** `aws-sdk-rust`, `aws-sdk-js-v3` and the `smithy-sdk` workspace.

This is the evidence B2-b4b2, the item-12 amendment (plan r4 section 2.2), weighs its options against.

**The byte model is exact where it can be checked.**
- **The real stores.** For the four stores the lead probe walked natively (B2-b4a's `evidence/lead-probe-real-stores.log`, pinned by the tool), objects and edges are equal. The modeled bytes at the probe's 134-byte root equal the measured bytes exactly: `aws-sdk-rust` measured 639,480,718 and the model gives 639,480,718. The census refuses if the probe ever exceeds the model.
- **The vectors.** On the walk vectors and composed workspaces, the native bytes equal the prediction at the scratch root's length wherever objects and edges do. They over-count, as an upper bound, where custody or a short read takes a cheaper branch (`evidence/test-census-soundness.log`).

## Paths

| Path | Change |
| --- | --- |
| `tools/security/discovery_census.py` | Bytes in the model (every charge's byte formula, affine in R), byte anchors, the closed size inventory, the read-growth bytes, the probe cross-check, and bytes in both records. |
| `crates/security/src/custody/discovery_census.json` | Regenerated: bytes per entry at three root lengths with `fitsTwiceAt`, the size inventory, the probe cross-check, and the byte limit. The objects-and-edges figures are unchanged. |
| `crates/security/src/custody/discovery_census_vectors.json` | Regenerated: `bytes` and `bytesPerRootByte` per vector, and the size inventory. |
| `crates/security/src/custody/discovery_census_tests.rs` | The soundness tests compare bytes at the scratch root's length. The margin test classifies bytes at each root length against a fresh ledger, and checks the byte limit. New: `the_census_size_inventory_matches_the_build`. |
| `crates/platform/tests/discovery_census_sizes_tests.rs` | **New.** It asserts the `libc` sizes in both records against this build. |
| `tools/tests/test_discovery_census.py` | The constants and read-envelope tests carry bytes. New: the anchors name exactly the size inventory, and an inventory missing `usize` refuses. |

## The model (plan r4 section 2.1)

**Costs.** Every cost is (objects, edges, bytes, perRootByte). An absolute spelling of `rel` is R + 1 + |rel| (R for the root). The model mirrors each charge's byte argument at its site:
- `owned(b)`, at b + `RECORD`;
- the listing;
- each raw name, with `.` and `..`;
- each listed name, at |n| + 2(|rel| + 1 + |n|) + 3·`RECORD`;
- `classify_cost` (segments·2·`size_of::<usize>()`, plus |rel|(1 + t), plus (2 + t)·`RECORD`);
- `obs`, `openDir`, `openReg`, `STATUS`;
- `CAP` (`DescriptorAclCapture` + `BUFFER_BYTES` + 2·`stat` + `attrlist`);
- `FS` (`statfs` + the status read + `DescriptorFilesystem`);
- the scope entry (abs + `ObservedEntry`);
- the slot (|n| + `(String, ChildObservation)`);
- every spelling and record site of `walk`, `named_root`, `subtree` and `enter`;
- `gitdir_target`'s read growth: each buffer's full size, 4096 doubling to the ceiling, as `next_buffer` sizes it.

**The dearer branch in bytes.** A capture's dearer branch is still `FS` (2,368 bytes) over the largest ACL record (128 × 16 + 128 = 2,176), so it is taken in every dimension. A `gitdir` target is charged at the file's length.

**Anchors.** 33 anchors read every constant and byte formula from the 15-file whole-pinned closure, which is unchanged since B2-b4a.

**The size inventory (RF-1 of plan round 3).**
- Every `size_of` operand an anchored formula names must be in the inventory, or the tool refuses. The inventory is `usize`, `libc::stat`, `std::fs::Metadata`, `ObservedEntry`, `(String, ChildObservation)`, `opensip_platform::CapturedAclEntry`, `DescriptorAclCapture`, `libc::attrlist`, `libc::statfs` and `DescriptorFilesystem` (aarch64-apple-darwin).
- The security test asserts the seven it can name. The platform integration test asserts the three `libc` types, by an exact whole-number match in each record.

## The controls

**Native.**
- The two soundness tests now refuse if the walker uses more bytes than the affine prediction at the scratch root's own spelling length. Objects and edges are checked as before, and an incomplete walk still never passes.
- `the_census_size_inventory_matches_the_build` (security) and `the_census_libc_sizes_match_the_build` (platform).
- The margin test checks:
  - `fitsTwiceAt` at each root length against a fresh discovery ledger;
  - the record's byte limit is exactly the profile's.

**Python (18 tests).**
- The constants with bytes.
- `the_anchors_name_exactly_the_size_inventory`.
- `a_formula_naming_an_unpinned_size_refuses`.
- The read envelope with growth bytes at L = 0, 1, 4,095, 4,096, ceiling − 1, ceiling and beyond.
- B2-b4a's integrity, workspace and held-out controls, unchanged.

**The model mutations (the lane).** These are B2-b4a's four, re-anchored to the byte-aware model: `observation-charge-dropped`, `capture-edges-dropped`, `dot-entries-forgotten` and `workspace-member-sum`. There is one new one: `scope-entry-bytes-dropped`. Each must make the native soundness tests fail.

## Check lanes

The evidence is lane r2, over the r2 candidate. Lane r1 (the r1 candidate) is kept in the work directory. See `evidence/checks.json`. The rows are:
- the security suite at base and candidate, with equal failure sets and at least one new passing test;
- warning-denied all-targets Clippy on host, security and platform;
- rustfmt on base-clean and new edited files;
- the platform size test;
- the census controls and the census `--check` over the T2 cache, with the probe cross-check;
- the environment and FW-01 pins, the vector checks, the configuration tables, the operability census and verify_design;
- the five model mutations.

## Not claimed

- No byte margin, no cap change and no law change: those are B2-b4b2 and B2-b4b3.
- No held-out margin, no caller and no qualification.

B2-b is not complete.

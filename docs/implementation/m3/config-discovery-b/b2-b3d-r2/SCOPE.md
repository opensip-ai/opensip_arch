# B2-b3d r2: what the candidate delivers (M3-B unit B2-b, sub-unit B2-b3d: the walker storage redesign)

**Lead scope record, 2026-10-16. Unreviewed candidate.** It implements the accepted B2-b3d plan r2 (`config-discovery-b/b2-b3d/PLAN-r2.md`; Codex `codex-b2b3d-plan-r2`, after round-1 findings RF-1 and RF-2, with NBO-1). That plan implements law M3-B r6 item 12's walker-storage requirement. Its base is product `84caf3f`: B2-b4a and B2-b4b1 are bound, inventory is v197, and there are 164 contract successors.

## r2 changes (Codex `codex-b2b3d-r1`, REQUIRED-FINDINGS)

**B2B3D-R1-RF-1: the parallel observation array is charged before it is reserved.**
- **The fix.** `enter` now charges the whole array (`owned(paths.len().saturating_mul(size_of::<ChildObservation>()))`, one record) after the listing and before `Vec::with_capacity`. The per-slot charge is gone, so nothing is charged twice. The census model mirrors this (one record per listed directory), and its figures fall slightly (below).
- **New controls:**
  - `the_observation_array_is_charged_before_it_is_reserved` (native). Under the largest byte limit that still refuses, a 512-child walk has listed the root and observed no child, and that limit is at least the whole array's size.
  - The structural check holds the order in `enter`: the charge comes before the reservation. A planted reversal fails it.

**NBO-1: the wording.** Bytes keep one per-walk root term (the root spelling, kept once); what the redesign removes is the per-entry root term. The census module's documentation now says the B2-b4a probe cross-check is retired and the new probe is archived separately.

The evidence is lane r3 (lane r2 failed one Clippy lint, `int_plus_one`, in the new test; fixed), and the lead probe is re-run on the r2 walker.

## The outcome

The redesigned walker's census (the same tool and integrity-verified stores, with the model mirroring the new walker), against the r5 provisional caps (2^20 objects, 2^21 edges, 2^30 bytes):

| Entry | Objects (before → after) | Edges | Bytes at R = 4,096 (before → after) |
| --- | --- | --- | --- |
| `rs-very-large-aws-sdk-rust` | 2,611,910 → 1,476,438 | 1,007,224 | 3,204,428,012 → 358,480,897 |
| `mr-ts-very-large-smithy-sdk` (workspace) | 572,330 → 326,252 | 439,389 | 727,484,048 → 100,302,829 |
| `ts-very-large-aws-sdk-js-v3` | 540,986 → 307,004 | 403,655 | 679,396,816 → 88,522,059 |

- **The per-entry root term is gone.** Bytes keep one per-walk root term (`perRootByte` = 1, the root spelling kept once), down from 647,387 for `aws-sdk-rust`.
- **Edges are unchanged.**
- **One entry still fails the r5 caps:** `aws-sdk-rust`, on objects.
- **The caps r6's rule gives** (the smallest power of two at least twice the largest entry; bytes at R = 4,096), as arithmetic only:
  - objects 2^22 (2 × 1,476,438 = 2,952,876 ≤ 4,194,304; 2^21 = 2,097,152 is short);
  - edges 2^21 (2 × 1,007,224 = 2,014,448 ≤ 2,097,152);
  - bytes 2^30 (2 × 358,480,897 = 716,961,794 ≤ 1,073,741,824).
- **This unit claims no margin and changes no cap.** The recording revision of item 12 and B2-b4b3 do that next.

## Paths

| Path | Change |
| --- | --- |
| `crates/security/src/custody/discovery_scan.rs` | The core reads a scope keyed by root-relative path. `custody`, `markers` and `unit_custody` take relative keys. Nested repositories and projects, unit and exclusion paths, refusal paths and `UnobservedAcl.path` are spelled under the root exactly as before. Raw rejected specifications (`JOIN_PATH_GRAMMAR`) keep their raw spelling. Every record is byte-identical. |
| `crates/security/src/custody/discovery_walk.rs` | The walker keeps no per-entry absolute spelling:<br>• `Frame`, `listed` and `verdicts` are relative, and `spell` is gone;<br>• `ListingConversion` converts each name once in the listing visitor and keeps a listing failure's priority (plan r2, RF-2);<br>• each child has one owned relative path, with a parallel observation vector;<br>• the root spelling is kept once;<br>• `trace` and `before_open` take closures, with production stubs that never call them; `trace_child` spells a relative `at` under the walk's root, in tests only;<br>• a test-only `listed_name` shim keeps the closed name controls unchanged. |
| `crates/security/src/custody/discovery_walk_tests.rs` | **Storage reads only:**<br>• the population compares relative keys spelled under `/h/w`;<br>• scope-key reads use relative keys;<br>• the two exact charge-count tests carry the new counts, with each copy named in their comments (file child 4→3, explicit spec 5→4, directory child 10→6, pruned child 5→4).<br>**New:** three `ListingConversion` controls. |
| `crates/security/src/custody/discovery_scan_tests.rs` | The vector runner converts each vector's absolute keys to relative ones, dropping keys outside the root (which the core never reads). The vectors stay pinned and unchanged. Hand-built scopes use relative keys. Expected records are unchanged. |
| `crates/security/src/custody/discovery_census_tests.rs` | The size inventory names `ChildObservation` in place of `(String, ChildObservation)`. |
| `tools/security/discovery_census.py` | The model mirrors the redesigned walker. Anchors (`VISIT`, `CONVERTED_NAME`, `SCOPE_ENTRY`, `ROOT_ENTRY`, `SLOT`), the size inventory and the closure pins are updated. The old probe cross-check is retired, and the record says so. |
| `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json` | Regenerated. |
| `tools/tests/test_discovery_census.py` | The planted-charge control is re-anchored. |
| `tools/tests/test_discovery_walk_storage.py` | **New:** the structural check (plan r2, NBO-1). |

## The controls

**Unchanged behavior.**
- All 52 walk vectors match the B2-b0 reference in population, evidence, custody inputs and records.
- All scan vectors match, and the upward vectors are unchanged.
- The host flag rows and the scenario seam are unchanged.
- Every trace, hook, `Changed` path and `NAME_UNREPRESENTABLE` detail stays absolute.

**`ListingConversion` (plan r2, RF-2).**
- An invalid name followed by an entry limit, a name-byte limit or a native read or close error refuses with the listing failure.
- A complete listing with an invalid name refuses `NAME_UNREPRESENTABLE` with today's detail (`NAME_UNREPRESENTABLE:/w/a:f%FF%3A`), and a clean listing gives sorted relative paths without `.` and `..`.
- Nothing after the first invalid name is converted.

**The structural check (`test_discovery_walk_storage.py`).** On the code with comments and literals blanked, it checks that:
- every `trace` and `before_open` call passes a closure;
- the production stubs never call it;
- `spelled(..)` appears only inside those closures, `ListingConversion::finish`'s refusal closure, the terminal `changed` refusal, or the `spelled` method;
- the absolute `join(..)` is called only by `spelled`.

Planted controls (a direct spelling, a direct-string trace, a stub that calls its closure) each fail it.

**The census soundness.** The native walker uses no more objects, edges or bytes than the redesigned model predicts on every walk vector and composed workspace. The model is exact on 46 of 56 and over-counts only where custody refuses or a read is short.

## Mutations (the lane)

**The census model** (re-anchored): `observation-charge-dropped`, `capture-edges-dropped`, `dot-entries-forgotten`, `workspace-member-sum` and `scope-entry-bytes-dropped`.

**The walker:**
- `absolute-scope-key`: the population map must fail;
- `parallel-observation-dropped`: native walks must fail;
- `name-refusal-wins`: the `ListingConversion` controls must fail.

## Check lanes

See `evidence/checks.json`. The rows are:
- the security and host suites at base and candidate, with equal failure sets and at least three new passing security tests;
- warning-denied all-targets Clippy (host, security, platform);
- rustfmt;
- the environment and FW-01 pins;
- the scan, upward and walk vector checks;
- the walker storage check;
- the platform size test, the census controls and the census `--check`;
- the configuration tables, the operability census and verify_design;
- the eight mutations.

**The lead probe (supporting evidence).** `evidence/lead-probe-real-stores.log` records a throwaway worktree that carried the candidate's walker with raised limits (`lead-probe-tree.diff`, relative to the candidate) and walked the same four stores natively, at a 134-byte root.
- Objects and edges equal the census exactly.
- Bytes equal the census's base plus 134 (see the log). The probe re-ran on the r2 walker.

## Not claimed

- No cap change, law change or margin.
- No held-out or workspace full-ledger margin.
- No production caller and no qualification.

B2-b is not complete.

Codex review: M3-B r10, configuration and discovery. A **law review**, round 1 of r10. r10 amends item 14a's bounds for the open item O-1 that unit B2-c2 routed to the lead for C2, and adds one control and one Not claimed line. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-m3b-r10-r1.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test or generator run (reading, hashing and `git show` / `git diff` are fine). Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store. No network is needed.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/m3-b-r10-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `e6a271b406bdec09f5d5c71ba4f4070b9e148c898e370cd0d690455b00e7c7fc`. It pins `PROPOSAL-r10.md`.
- **Bases:** product `9501ec9d167200e82580fbeab73afd2d1cbd7159`, architecture `10cb57bce72c6613d77bf0734fe5a0526bdbd0cb`.
- **Diff base:** `PROPOSAL-r9.md` (`24fe5a9c…`), the r9 bytes you accepted in `reviews/codex-m3b-r9-r1`; the live `PROPOSAL.md` differs from them only in its acceptance banner. Every change must appear in r10's "r10 changes" section.
- **Context:** O-1 in `config-discovery-b/b2-c2-r2/SCOPE.md` ("Open items") and your `reviews/codex-b2c2-r2/REVIEW.md`, which kept it routed to the lead before C2 emits graphs. The record is `$defs/TypeScriptConfigGraphV1` (and `CanonicalPath`, `TypeScriptConfigProjectionV2`) in the product's `schemas/sources/native-v2.schema.json`. The B2-c2 implementation is `crates/host/src/typescript_config.rs` (walk order LD-B2C2-4) and the unit-root bound is `admit_root` in `crates/host/src/discovery.rs`.

## What r10 changes

1. Item 14a, "Bounds": at most 64 entries in one file's `extends` array, repetitions included, and at most 4,096 characters in a node's canonical path, with where each is checked.
2. Item 14a's `native.typescript-config-bound` row gains both cases.
3. Item 14a's controls gain the record bounds at and one past each bound, the refusal coming before any entry is resolved, and schema admission of every admitted control graph.
4. Banner, the "r10 changes" section (the constraint-by-constraint check of `TypeScriptConfigGraphV1` against item 14a, the decision table and the check order), and one Not claimed line.

## Decide

1. **Completeness.** Is r10's check of `TypeScriptConfigGraphV1`'s constraints against item 14a right: are `extendsResolved`'s `maxItems: 64` and `CanonicalPath`'s `maxLength: 4096` the only constraints item 14a's graphs can violate? Is any other one missed?
2. **Soundness.** Is refusing as `native.typescript-config-bound` the right law decision against the rejected alternatives (raising the schema bound, dropping repetitions, keeping 64, refusing only at C2's emission, truncating paths)? Is the check order deterministic and consistent with LD-B2C2-4, and the subject rule kept?
3. **The public termination.** Is it unchanged and still true (S10's alias rows, D9 row, remedy), so no S10 successor is needed?
4. **Scope and fidelity.** Does r10 change anything beyond what its section lists?
5. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `M3BR10-R1-RF-n` / `M3BR10-R1-NBO-n`.

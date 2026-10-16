Codex review: S10b, the TypeScript configuration remedy successor. A **design-unit review**, round 1 (proposed contract successor 172). Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-s10b-remedy-r1.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test or generator run. You may run the unit's own checker, which reads only architecture files and writes only its `checks.json`; if you run it, run it on a copy (for example copy the architecture's `docs/implementation/m3/config-discovery-b/` tree to a private temporary directory and run it there from a matching root), so the reviewed `checks.json` is not rewritten. Reading, hashing, AST parsing and `git show` / `git diff` are fine. Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store. No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/s10b-remedy-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `ebd8c39811bf01c9a4f1cd39f1c53ae947cfc8e520c4e45befcc40aa116449e9`. It pins the README, `evidence/check.py`, `evidence/checks.json`, the two successor model copies and `successor.json`. Rehash every member.
- **Bases:** product `9501ec9d167200e82580fbeab73afd2d1cbd7159`, architecture `f3e0537a8155ec0982f9165738c3d690be1c3d3f` (M3-B r10 published).
- **Authority:** M3-B r10 (`config-discovery-b/PROPOSAL-r10.md`; your `reviews/codex-m3b-r10-r2`, ACCEPT, after `codex-m3b-r10-r1`'s M3BR10-R1-RF-1): item 14a's termination step 3 (r10 sentence), the r10 remedy control, and item 25 row S10b.
- **Parents:** S10-TSC's two native-model copies, `config-discovery-b/s10-tsc/reference/native_evidence_model.py` and `.v2.py` (contract successor 167 in product `design-lock.json`).
- **Product carrier today:** `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` in product `crates/host/src/outcomes.rs` (S10's string).

## Decide

1. **Exactness.** Is each successor copy its parent with exactly the remedy string's bounds clause rewritten and one comment line added, every other byte, every other `PUBLIC_ROUTE_REMEDIES` entry and `D9_MAP` unchanged?
2. **Truth.** Does the new string name all four item 14a bounds (64 KiB, 64 `extends` entries, 4,096 characters per configuration file path, 32 files) and stay true for all four internal keys, as r10 requires? Is its wording accurate to r10 (entries counted with repetitions; the path limit in characters)?
3. **Scope.** Is S10b the narrow successor row S10b names: no registry, alias, D9, schema or vocabulary change; the selection statement right?
4. **LD-S10B-1.** Is leaving the product carrier to B2-c2b (row S10b's named consumer), with the vectors pinning these copies and the row-59 test tying the carrier to them, a sound reading of row S10b? Is the claim that the product's current string stays true until B2-c2b lands correct?
5. **The checks.** Do `check.py`'s checks and nine mutants establish the above (each mutant failing at its named check)? Is `successor.json` sound for binding (parents accepted and sorted, candidates equal to the subject minus the record, authorities)?
6. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `S10B-R1-RF-n` / `S10B-R1-NBO-n`.

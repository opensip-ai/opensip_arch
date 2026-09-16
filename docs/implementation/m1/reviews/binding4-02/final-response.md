My verdict is **ACCEPT-UNIT** with no required findings and seven non-blocking advisories. I wrote `review.json` and `review.md` to `m1-binding4-review-02`. The manifest hash (`e8043832…`) and all four file hashes matched before and after the review, and the copy I worked from is identical to the frozen subject.

**What I ran:**
- **Tests:** all 56 pass. The changes over the accepted candidate01 only add code: the lock is byte-identical and no test lines were removed.
- **Real run with `--implementation`:** against adapter subject-03 and `opensip_arch` it exits 0 and verifies 28 sources, reporting no generator code executed and no product qualification. The output matches the root `source-preflight.json` exactly.
- **Root real-mirror probes:** the 14 two-hop probes all pass on my copy. The line/pointer alias on the real inventory3 is now refused.
- **Prior review01 probes:** 43 of 46 pass. The three that changed are the intended fixes: two now refuse via the new JSON-pointer guard, and one now fails with a controlled error.
- **My own v4 probes (42 of 42):** old v1–v3 behaviour, three-hop reindexing, inheritance conflicts and suppression, JSON detection by content rather than file name, aliases, path reuse and cycles, and malformed data.
- **My own source preflight probes (35 of 35):** refused attempts to use unaccepted, superseded or locally changed architecture files, including a full local repin. Changed copies, symlinks, map/registry mismatches and open schema fields were also refused. The real architecture and adapter files did not change.
- **Mutation testing (43 mutants):** the tests alone kill 22 of the 24 prior mutants, confirming the claim; the other two cannot change behaviour. Tests plus my probes kill every mutant that can.

**Advisories:**
1. **Any accepted file can be a source:** the preflight accepts any of about 12.9k accepted overlay rows, not just the 46 lock inputs. 20 of the 28 real sources are in that category. If the map and registry both omit a schema ID, even a non-schema file whose accepted meaning was changed by a passage override passes. No real source is affected.
2. **Local-only checks:** major version, profile and owner are only checked for agreement between the map and the registry, not against the architecture. The rows accept unknown keys, and source paths are not confined to `schemas/`.
3. **Test gaps:** six new guards are not isolated by the tests: N05, N09, N14, N15, N16 and N19. The most important is N05, where an accepted path is repinned to a different digest, because the architecture working tree has uncommitted changes. My probes kill all six.
4. **Duplicate-key JSON:** such a file counts as text, so line selectors are allowed on it. This creates no alias, because no JSON pointer can address that file either.
5. **Error types:** a non-JSON source raises a JSON decode error rather than `DesignError`. A list-valued override path still raises `TypeError` in code carried over unchanged. The CLI still exits 1 in both cases.
6. **Checkout lock not checked:** the preflight ignores the lock and verifier inside the implementation checkout; adapter-03 carries the older v3 ones and still passes. This matches the stated trust model of starting from a reviewed checkout.
7. **Review01 advisories:** B4-A01, B4-A02 and B4-A03 are resolved, as is half of B4-A04. B4-A05 and the carried contract-binding advisories still apply.

**Limits:** this is a code-binding review of a developer preflight. It does not accept the adapter's source map or registry content, and it implies no product qualification or new contract approval. I did not reaudit the base approvals, inventory3, metadata-v2 or the schemas themselves. Non-empty multi-hop inheritance was only tested on synthetic fixtures and mirrors, and I did not re-mutate the older v1–v3 guards.

One of my own probe fixtures (V29) was faulty on the first run and refused for the wrong reason; after correcting it, it passes.

Everything is in `/tmp/opensip-implementation/m1-binding4-review-02`; the probe scripts (`probe_v4.py`, `probe_sources.py`) and `mutate.py` sit next to their result files.

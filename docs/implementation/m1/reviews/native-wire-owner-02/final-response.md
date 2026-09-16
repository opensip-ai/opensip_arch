**Verdict: changes-required.** There are 3 required findings and 7 advisories. The review is in `m1-native-wire-owner-review-02/review.json` and `review.md` (`subjectManifestSha256` `5d11f555…0e4d`), with probe scripts and outputs under `scratch/`.

**Reproduction**
- **File set:** the 42 files matched the manifest exactly, before and after the review.
- **Checks:** from a fresh copy, `check.py` gave 299 checks with 0 failures, byte-identical to the frozen result. It also passed with the bytecode env vars unset.
- **Closure:** 35 architecture reads, all pinned, and no `.pyc` read. No hidden `/tmp` reads.
- **Architecture tree:** it does contain old `.pyc` files. None was read or written, and all 35 pins were unchanged afterwards.
- **Selftest:** 37/37 caught, byte-identical. It can't run from the 27 inputs alone because it reads `subject-files.json`, so the real set is 28 files.

**Accepted after my own probes**
- **All six review-01 findings and ten advisories** are fixed as stated. Three new findings grew out of RF-3, RF-5 and RF-6.
- **ProviderFault worker-observed phase:** I wrote my own race model from the P3 table. Across 145 worker cuts, no lawful fault was refused and no altered fault was admitted. The owner table gave P3-28 every time.
- **Reading Hello first:** this follows from the inherited handshake. Refusing a START-phase fault gives the same D9 outcome as P3-28 (operational-failed 4 `PROVIDER.PROTOCOL_VIOLATION`), so no fault is suppressed.
- **PreparedOutput 256/255** refused before spawn: accepted.
- **Path segment rules:** the newline cases behave as stated.
- **PackageKey:** the exact join and tuple order match the owner, with 0 order disagreements in 20,000 random pairs. Empty and space-containing sourceIds are admitted; a 4096-scalar key is admitted and 4097 is refused.
- **Carried-over items** (scope2, raw TS manifest, dependency-source self-reference, anchors, fact-ref, inert kinds, anchor order) check out against the owners.

**Required findings**
1. **The two new details join nothing.** Neither `native.prepared-output-exceeds-wire-limit` nor `native.dependency-source-package-key-invalid` is in:
   - the closed `public-detail-registry.v1.json`, which is unpinned and never read;
   - `DomainDetailCode`;
   - the model's `D9_MAP`.

   No D9 route row covers dependency-source set refusals. Changing that refusal to operational-failed/ILLEGAL_STATE, or the prepared refusal to "after spawn", fails 0 checks.
2. **Dependency sources the owner admits can't all go on the wire, and nothing refuses them before spawn.** This is the same problem review-01 RF-3 raised for prepared outputs.
   - **Paths:** owner-admitted names like `C:x`, `a:b/c` and `a//b` are refused by the candidate's new path rule.
   - **Frame size:** the single dependency manifest overflows 64 MiB at about 329k realistic entries (579k minimal), against a 1,000,000 limit.
   - **Request totals:** the request byte and frame totals have no stated fate.
   - **NFC:** a non-NFC sourceId passes set admission but the wire refuses it.
3. **The hand-lowering list is incomplete.**
   - The checker only scans scalars (11 names, and it asserts just "at least 10"). It misses 2 inline patterns and 7 distinct extern lookaround patterns.
   - It runs Python `re` instead of the declared ECMA dialect. Node shows they disagree on `a/..\n`, `a/.\n` and `..\n`.
   - Changing the dialect or lowering text fails 0 checks.

**Limits**
- No generator was run, and nothing here counts as production code or M2/M3 qualification.
- I took commitment domains and the scope2/digest fixtures from the author's checks rather than re-deriving them.
- The race model did not enumerate Cancel interleavings; I argued those from the P3 table.
- I did not measure how often the dependency-source cases occur in real crates.

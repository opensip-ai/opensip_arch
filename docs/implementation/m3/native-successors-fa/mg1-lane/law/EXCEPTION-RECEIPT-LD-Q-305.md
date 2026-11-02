# Erratum E1 to the adoption receipt ADOPTION-LOADER-POLICY-F1A.md: a digest re-pin of gen-ts-enums.mjs, same scope (2026-11-02 UTC)

**Decision LD-Q-319 (coordinator, session 9ce22ffd, under OD-AUTO-1 and LD-Q-305).** The adoption receipt's bytes stay intact. This erratum is read with it.

**What moves:** the digest of `providers/typescript/scripts/gen-ts-enums.mjs`, the file holding adopted exception D-2 (gen-ts-enums.mjs createRequire).
- Old: `d3a21d1a5c4d5da9dd46e9b08e8712411c4608c561657f5fdc8998512cae605e` (3702 bytes; verified by me at product 4be0f890).
- New: `412e3ca866777ecfdc42f05c68d9a8f8d02a044752e5320c20108615701deafe` (3701 bytes; verified by me at product 1e916f18ce64454365b908a3d3af742610c38ced).

**The whole change, read by me from `git diff 4be0f890 1e916f18`:** line 16 only, `const OUT = "src/generated/ts-enums.ts";` to `const OUT = "src/embedded/ts-enums.ts";`. The exception's site at line 23 is untouched. Diff record: `f1/main-generate-1/evidence/receipt-input-r2/gen-ts-enums.diff`, sha256 `81df2e95165a996b4148e4e84d17b13040bd691051faa2945664ac92c1496ef9`.

**Basis:** R2 different-vendor code review `f1/review/REVIEW-MG1-CODE-r1.md`, sha256 `fdd4086d74fa5a8fbd87defde088277c746399f40c8dd3ccd5e57d7375fe3cd9` (read-only at signing): `MG1-EXCEPTION-SCOPE: UNCHANGED`, `MG1-CODE: ACCEPT` for that product head, `ESCALATION: NONE`.

**This is not a new adoption.** The R3 review `b7562b84...` is not re-run, and no scope is added: same kind, site, expression, target, precheck order and limitation. Exception D-1 (`compiler.ts`) is byte-equal and CP-F1C-COMPILER-VERIFY stays open, all five parts. The stale path in the file's line 1 comment is left as the reviewer accepted.

**If the file changes again before binding, for any reason, this erratum does not cover it.** It covers exactly the new digest above. It establishes no binding, integration or qualification.

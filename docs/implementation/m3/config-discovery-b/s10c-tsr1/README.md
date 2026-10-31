# S10c: TSR-1's successor of S10's registry and S10b's native-model copies

**Bound with unit C2b-1b (LD-Q-160).** It carries the two changes TSR-1 Part R makes to S10's public termination of
TypeScript configuration refusals: R-10.1's eight profile alias rows, and R-10.3's remedy as amended by erratum E3 r3.
TSR-1 (`../../snapshot-plan-c/tsr1/TSR-1-r4.md`, adopted LD-COORD-TSR1) and E3 r3 (`ERRATUM-E3-r3.md` beside it,
adopted LD-COORD-E3) are bound in the same commit, with their receipts.

## Why

TSR-1 resolves a configuration's options under TypeScript 6.0.3 and refuses what it cannot resolve. Part R adds no
public code: each of its eight internal refusals aliases to the existing `native.typescript-config-unresolved`
(CONFIG.INVALID, request-rejected, exit 2), through S10's alias rule (R-10.1). The remedy registered for that code
must then be true for those refusals too, and must stay within `DomainDetail.remedy`'s `BoundedText` maximum of
1,024 characters. R-10.3's original clause was 2,191 characters, so erratum E3 replaced it with a 290-byte clause
(S10b's 646 characters plus the clause make 936).

## What it is

| Successor | Parent | Change |
| --- | --- | --- |
| `registry/public-detail-registry.v1.json` | `../s10-tsc/registry/public-detail-registry.v1.json` (67,246 bytes, `1cf12692…`) | the eight R-10.1 alias rows, each `{internalCode, publicCode: native.typescript-config-unresolved, selector: …/TSR-1-r4.md R-10.1}`, inserted in sorted position; nothing else |
| `reference/native_evidence_model.py` | `../s10b-remedy/reference/native_evidence_model.py` (322,096 bytes, `bdfd8373…`) | E3 r3's clause appended to the `native.typescript-config-unresolved` remedy; one line, nothing else |
| `reference/native_evidence_model.v2.py` | `../s10b-remedy/reference/native_evidence_model.v2.py` (321,976 bytes, `d6455407…`) | the same one line |

**Unchanged:** every other registry member and alias row, every other `PUBLIC_ROUTE_REMEDIES` entry, `D9_MAP`, the
D9 row, the public record and the detail vocabulary. MB14a's four item 14a alias rows stay as S10 has them.

**Selection.** These become the selected copies: the registry for the alias rows, and the two model copies for
`PUBLIC_ROUTE_REMEDIES`. Later edits of either succeed these, not S10's or S10b's.

## The product carriers

They were written with unit C2b-1b, which the product already carries:
- `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` (`crates/host/src/outcomes.rs`) equals this unit's 936-character remedy
  byte for byte;
- `TYPESCRIPT_PROFILE_ALIASES` (`crates/host/src/typescript_config.rs`) is a separate closed map of the eight rows;
  a control compares it with the vectors' `profileAliases`, which the generator below reads from this registry;
- `tools/host/typescript_config_vectors.py` pins this unit's registry and model copy by size and SHA-256 and
  regenerates the configuration vectors from them, including `profileAliases`.

## Checks

`evidence/check.py`, run from the architecture root, writes `evidence/checks.json`. It parses both models' syntax
trees and executes neither.
- **The pins:** the parents, E3 r3 and the three successors are at their pinned bytes (the successors' pins are the
  product generator's).
- **The models:** each successor differs from its parent in exactly one line. Its `PUBLIC_ROUTE_REMEDIES` has the
  same keys, every other value is equal, and the one value is S10b's followed, with no other change, by E3 r3's
  quoted clause (290 ASCII bytes, read from the erratum). The remedy is 936 characters, within 1,024, and both
  copies register the same string.
- **The registry:** every other member is equal; S10's alias rows are all kept in order; exactly the eight R-10.1
  codes are added, each aliased to `native.typescript-config-unresolved` with the TSR-1 R-10.1 selector; the rows stay
  sorted; the bytes are the parent's with one inserted block; and the selector names a present file.

**Ten negative controls (mutants)**, each failing at its named check: the clause altered by one character; the v2
copy left at its parent; another remedy altered; a second line changed; the two copies disagreeing; one profile row
dropped; a row aliased to another public code; a selector naming another path; one of S10's rows altered; the profile
rows appended out of sorted order.

## Not claimed

- No new public code, D9 row, schema or detail vocabulary change.
- **Not TSR-1 Part S.** The native-schema successor NSS-TSR1-S1 that TSR-1 R-11 describes is deferred with erratum S2
  (OD-PROC-1, LD-Q-16 to LD-Q-21; R-11.6 is not to be implemented as written). The product's native schema is still
  the frozen parent `7179d52e…`, and nothing of Part S is bound here.
- No TypeScript limit beyond TSR-1's, and no qualification.

# S10b: the TypeScript configuration remedy successor (contract successor 172)

**Proposed design unit, 2026-10-16, round 1.** It writes successor row S10b of M3-B r10's item 25 (`../PROPOSAL-r10.md`; Codex `codex-m3b-r10-r2`, ACCEPT, after `codex-m3b-r10-r1`'s M3BR10-R1-RF-1).

## Why

M3-B r10 adds two bounds to item 14a: at most 64 entries in one file's `extends` array, and at most 4,096 characters in a node's canonical path, both refused as `native.typescript-config-bound`. Their public termination is S10's: the alias to `native.typescript-config-unresolved`, its D9 row (request-rejected, exit 2, `CONFIG.INVALID`) and its remedy.

S10's remedy says "keep each file within 64 KiB and the graph within 32 files". A well-typed file with 65 repeated entries naming one present base is within both, so that text is false for r10's refusals. r10's termination step 3 requires the remedy to name every bound, and item 25's row S10b is the successor that rewrites it.

## What it is

Complete successor copies of S10's two native-model files (contract successor 167):

| Successor | Parent |
| --- | --- |
| `reference/native_evidence_model.py` | `../s10-tsc/reference/native_evidence_model.py` (321,895 bytes, `0e05bbf0…`) |
| `reference/native_evidence_model.v2.py` | `../s10-tsc/reference/native_evidence_model.v2.py` (321,775 bytes, `4b88aebb…`) |

Each is its parent with exactly two edits:
1. **The remedy keyed by `native.typescript-config-unresolved`.** Its bounds clause changes from "keep each file within 64 KiB and the graph within 32 files;" to "keep each file within 64 KiB and 64 extends entries, each configuration file path within 4,096 characters, and the graph within 32 files;". The rest of the string is S10's.
2. **One comment line** after S10's comment on that entry, citing M3-B r10 and S10b.

**Unchanged:** every other `PUBLIC_ROUTE_REMEDIES` entry, `D9_MAP`, and every other byte of both files. S10's public detail registry, its four alias rows, its design mirror and the product's detail vocabulary are not touched, so they stay S10's selected copies.

**Selection.** These two copies become the selected native-model copies for `PUBLIC_ROUTE_REMEDIES`. Every later edit of that table succeeds them, not S10's.

**The new string is true for all four internal keys.** It is one list of alternatives:
- `extends-unresolved`: make every base present as a regular file inside the project (S10's clause);
- `extends-cycle`: break any extends cycle (S10's);
- `bound`: the rewritten clause, which now names all four bounds;
- `malformed`: correct the file's syntax (S10's).

## Lead decision

**LD-S10B-1. The product carrier is written by B2-c2b.** Row S10b says the new string goes into the product carrier `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED` (`crates/host/src/outcomes.rs`) as well as into these copies. S10-TSC changed its model copies and the product together, because the public record was new. Here the product change is one constant, and it belongs with the code that makes the new refusals. B2-c2b, row S10b's named consumer, does three things:
- it changes the constant to this unit's string;
- its vector builder pins these copies instead of S10's;
- its existing row-59 test compares the carrier with the vectors' remedy, which comes from this unit's model.

So the product cannot carry a different string. Until B2-c2b lands, product main carries S10's string and refuses nothing r10 adds. Its text is therefore still true of every refusal the product makes.

**Rejected:** a product commit in this design unit. It would land the new remedy before the refusals it describes, and B2-c2b would then change the same file again.

## Checks

`evidence/check.py`, run from the architecture root, writes `evidence/checks.json`. It parses both models' syntax trees and executes neither.
- **The parents** are S10's accepted bytes (pinned).
- **The edits:** each successor equals its parent with exactly the two edits above.
- **The table:** `PUBLIC_ROUTE_REMEDIES` has the same keys, every other value is equal, and the one value is S10's with only the bounds clause rewritten.
- **The bounds:** the remedy names `64 KiB`, `64 extends entries`, `4,096 characters` and `32 files`, and has a clause answering each of the four internal keys.
- **One string:** both copies register the same remedy.

**Nine negative controls (mutants)**, each failing at its named check:
- **built consistently, so that only a semantic check can catch them:**
  - the entries bound dropped;
  - the path bound dropped;
  - the cycle clause dropped;
  - the v2 copy spelling `4096`;
  - the two copies disagreeing;
- **inconsistent edits, caught by the whole-file check:**
  - the v2 copy left at its parent;
  - another remedy altered;
  - a `D9_MAP` code altered;
  - the comment alone with no remedy change.

## Not claimed

- No product change (LD-S10B-1), no schema, registry, alias, D9 or vocabulary change.
- No TypeScript limit is claimed for either bound (M3-B r10, Not claimed).
- No qualification.

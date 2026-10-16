# B2-b4 description successor (contract successor 165)

**Lead record, 2026-10-16. Proposed; it needs Codex review and root assent.**

This successor refreshes three inventory row descriptions that no longer describe their files. At B2-b4b3 the lead recorded that the descriptions of `discovery_census.json` and `discovery_census.py` were stale. B2-b4c1 also outgrows the census test's description.

The successor uses passage overrides on the rows of `docs/implementation/m2/repository-file-inventory.v199.json` (the v199 candidate). An additive inventory successor must keep every inherited row equal by value, so v199 cannot change these rows itself.

**Description only.** No inventory row other than the three descriptions changes, and nothing changes in the schema, product, law or any package. It binds in the same lock commit as v199.

| Row | Why the old text is stale |
| --- | --- |
| `crates/security/src/custody/discovery_census.json` | It still says "the caps returned to the law" and "objects and edges". Since B2-b4b1 the record carries bytes too; since B2-b4b3 it carries `recorded-margin-holds` and walker-only workspace rows; since B2-b4c1 its held-out rows can be stale or composed. |
| `tools/security/discovery_census.py` | It predates the byte model (B2-b4b1), the redesigned walker it mirrors (B2-b3d) and the blind mode (B2-b4c1). |
| `crates/security/src/custody/discovery_census_tests.rs` | It says only "objects and edges", and "no margin is claimed for a failing entry". Since B2-b4b3 the test makes the full claim with bytes; since B2-b4c1 it classifies composed held-out rows and checks the gate. |

`successor.json` gives each override's exact before and after text.

# B-S10 follow-on: operability mint-audit census for the regenerated contracts

**Product record follow-on; PROPOSED.** B-S10 (Codex `codex-b-s10-r2`, ACCEPT-DESIGN-UNIT; architecture `d8950a8d`) is published, but its product commit stopped at integration.
- **What stopped it.** `tools/check_operability.py source` refused with a mint-audit census difference. The regenerated `crates/contracts/src/generated/invocation.rs`, which now carries the `ProductConfiguration2Root` carrier, has 150 lexical `into(` calls, where the audited record `tools/operability/exceptions.json` has 135. Only that row differs, and the base product passes.
- **Why it was missed.** The B-S10 checks did not run the operability source check. The 14 reviewed product copies therefore do not include this record.
- **State now.** The product checkout was restored to clean, and nothing is committed to the product.

**The change.** The single `mintAudit` row (`crates/contracts/src/generated/invocation.rs`, `into`, `call`) goes from 135 to 150 (`exceptions.diff`). That is the count this tree has; the record's own standing is "Conservative lexical call census … not receiver type inference or mint authority". The 15 new calls are the generated carrier's type conversions. The candidate passes `check_operability source` with the update (`operability-results.json`).

**The product commit after acceptance:** the 14 B-S10 product copies, byte for byte from the published package, plus this record. The design-lock commit binding B-S10 follows, with fresh `verify_design`, the report lane and the standard `generate_contracts.py` check. Nothing is pushed.

**Not changed:** B-S10's design content, every exception class row, and any law.

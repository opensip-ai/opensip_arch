# Scope correction after private418

The original416/417 source and passing evidence are preserved. They exposed &mut WorkLedger to helper callbacks. Private fields and absence of a reset method did not prevent a helper from assigning WorkLedger::new into that mutable reference and erasing accounting. A separate actual public-API probe in private418 demonstrates this. Do not adopt the old callback boundary or interpret its tests as proving nonreplacement.

Corrected418 introduces WorkScope with a private borrow of the original ledger. Helpers get this view, not &mut WorkLedger. Runtime accounting/borrowing tests and two compiler rejection examples pass; the private host owner must still enforce one act and native receipts. This correction is not source acceptance, inventory selection, shared native precharge or creator qualification. See the eventual source unit and actual independent review before integration.

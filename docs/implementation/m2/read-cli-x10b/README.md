# Read-only CLI wording — contract successor X10b

2026-09-30. Claude Opus 5.5, implementation lead. This is the text-only contract successor that law X10 r3 item 8 allows "only if needed". It is needed. The unit is PROPOSED and needs independent review and root assent before selection. It changes no schema, registry, generated code, inventory or product file.

## Why

Law X10 item 3 says each doctor remedy is the selected golden's remedy where a golden fixes one. X10a uses the `doctor-defects-found` golden remedy unchanged ("CI must inspect doctor.defectsFound; exit 0 means the report was produced").

The `doctor-report-not-producible` golden cannot be used as written. Its situation, "the private store cannot be opened to produce the report", and its remedy, "check permissions on the private store root", name a cause doctor's report-production failure does not have. In X10, doctor opens no store. Its report cannot be produced only when it would need more entries than its bound (255 plus the note, or 256), or when an entry cannot be bounded. An unopenable installation is not a report failure at all: it ends on its own law 468 item 6 row with no report (458c item 12).

## Overrides

Six JSON Pointer overrides, on golden 26 (`doctor-report-not-producible`) in each of the three accepted command inventories (coop v3, metadata-v2 v4, the composed-owners proposal):
- `situation` becomes "the bounded doctor report cannot be produced: more entries than its bound, or an entry that cannot be bounded; nothing is truncated";
- `remedy` becomes "Resolve the report-production failure and run doctor again.", the product's existing text from 458c-c.

The class, exit code, error code and domain detail are unchanged.

## Not included

The inventory description of `crates/host/src/doctor_report.rs` ends "Library only: nothing emits it yet.", which X10a makes untrue. A description override must target the latest accepted inventory. While X1a's inventory81 and X10a's own inventory are both under review, there is no stable target. The fix is left to a later description-only successor, as 461b did for 458c.

`evidence/build_x10b.py` rebuilds `successor.json` and the subject manifest deterministically. `evidence/verify_scratch.py` runs the real verify_design with a synthetic in-memory review and assent.

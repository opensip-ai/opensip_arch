# Coverage shared-budget integration01 — unaccepted

This reference integration connects the proposed Run/evidence source binding to
the existing parent report's shared-prefix algorithm. The complete source,
per-row descriptor/payload and provenance wrapper count toward the shared byte
allowance from the first row. Later-panel reservations remain included, and an
earlier whole-panel omission prevents later builders from running.

It also addresses a necessary integration detail: source hydration can stop at
the item cap while the source collection is larger. The projector must use the
full admitted source total, rather than len(hydratedEntries), for item/byte
omission accounting. The internal input requires exactly min(total,itemCap)
hydrated rows. A shorter prefix refuses instead of claiming that the source ends
there. The host must supply the original source owner's admitted projection;
this internal input is not an untrusted public provider API.

coverage_budget.py changes only the coverage branch passed to the unchanged
pinned parent-reservation adapter: source anchor, full count and hydration
guards. The parent binary search, whole-row delta fixed point, panel reservation
and stop rules remain unchanged. The experimental schema adds the parent's
existing ItemProjectionV1 byte-budget carrier and explicit byte-measurement
provenance to coverage-binding01. It does not select a new report major/profile.

16 groups pass. They include prefixes0/1/2/3956 of the actual complete-replay
admitted synthetic two-result Run, source nonmutation, invalid caps, incomplete
hydration, impossible reservation and stopping later builders. Every one of3540
shared-byte boundaries for that actual source is checked for deterministic
output, complete-row prefixes, preserved reservations, exact source/counts,
embedded descriptor/payload identity, the complete wrapped byte bound and the
inherited rejected-whole-row delta calculation. One separate synthetic count-only
control uses total5000 with one hydrated row to prove that a cap does not lose
the source total; it makes no claim of5000 results belonging to this Run.

prepare.py and check.py verify1232 files against the joint06 and coverage-binding
checkpoint02 manifests. Their owners are executed from pinned source bytes.
Run both scripts with metadata-reference-env Python and -I -B. check01 is the
current passing execution. Source snapshots, base reports and product files are
unchanged. Grok review is pending for this separate integration; review of the
earlier coverage source alone does not accept these new bytes.

Remaining: complete report source/carrier/provenance succession; the embedded
owner walker must validate each row.result at its native codec boundary and each
descriptor at its identity boundary; replace the old envelope diagnostic-ID join
with exact source Run/evidence and row identity joins; rebuild source-positive
fixtures and classify synthetic layout cases; validate all existing graph/feature
interactions against the new shared prefix; rederive bounds on the actual final
schema; regenerate consumers and the browser adapter; integrate immutable host
snapshot custody, static parity and delivery. This checkpoint is not a full
report integration, product implementation, independent verdict or M4 completion.

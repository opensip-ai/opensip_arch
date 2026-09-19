# Owned ledger recovery evidence — candidate 157

Private, uninstalled, unselected successor156. Storage now returns an owned CapturedLedger from its actual receipt, association and attempt reads, preserving their exact snapshot relationship for later host composition. This is an integration boundary, not confirmed commitment or authority.

The new child module recovery_snapshot.rs has private fields and no raw constructor, Clone, Default or mutable getter. Its capture function can only read the storage owner's ReadSnapshot. Existing schema checks, physical mirrors, parsers and join_ledger law are unchanged. CapturedLedger retains the supplied binding, exact stored receipt and association bytes, admitted attempt and conditional standing. Attempt data is reconstructed from SQL columns; there is no fictitious stored attempt body. Supplying the binding does not establish its custody or trust.

A borrowed LedgerAnchor exists only for ContinueCarrier. Its generation, journal sequence, digest, operation, Run and full uint64 commit sequence come from the joined association and its lifetime remains tied to the complete evidence. The pending-settlement and legacy-custody-unknown flags remain available through that evidence. Bad joins and negative/open/unobserved results have no anchor. No generic status can be inserted into the sealed object by a parent caller.

ReadSnapshot.recovery_ledger keeps its transaction for callers still composing reads. The read_recovery convenience operation opens the existing WAL snapshot and releases it before returning the owned evidence. Read errors remain errors, never fabricated absence. Retaining the result does not retain a WAL reader or claim current evidence after the files change.

## Validation

36 storage tests and strict workspace/all-target Clippy pass. Three new actual SQLite tests cover all16 pair/attempt combinations, receipt/association/attempt/borrowed-anchor getters, uint64 max and maximum lawful journal sequence, bad joins and supplied carrier mismatch, incomplete schema, settlement changing across fixed snapshots, exact bytes surviving subsequent corruption, and WAL checkpoint after the read. Existing snapshot, schema and index-error tests now consume the sealed result's readonly standing.

Eight compiled mutants plus baseline test anchor gating, lost attempt, skipped join, swapped receipt/association evidence, wrong sequence domain, wrong binding, and a leaked SQL reader. Seven privacy clients fail for the relevant field/type rule; the readonly getter client compiles. Final isolated host99 verifies222 source pins,36 fixtures and51 supplied dependency archives;333 workspace tests and2 doctests pass.

## Remaining integration

The host still has to compose this actual ledger evidence with the security owner's sealed AnchorAssessment and admitted retained filesystem custody, current authority and complete retained closure. No security-to-storage dependency or public authority facade is added here. All full118I2/124F1 custody/exclusion/lease/fence/writer, clock/revocation, migration-prefix/INIT, pin/output/deletion and formal selection obligations remain. A successful ledger anchor may carry legacy unknown custody or pending settlement and is never sufficient on its own to declare commitment.

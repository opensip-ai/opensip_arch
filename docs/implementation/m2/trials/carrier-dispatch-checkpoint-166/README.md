# Physical read-only carrier dispatch 166

Unaccepted cumulative candidate over164.345 product files:342 unchanged,2changed,1new. No product installation, reference selection, custody grant or cumulative approval.

## Behavior

New private carrier_dispatch.rs owns CapturedDispatch with an actual retained SQLite connection or an admitted CurrentCarrierSnapshot and the owned definitions of at most seven known current-format objects. Names are read first, fixing the snapshot. No current-format names means observed inherited1/2 (table/trigger names only) or bound-carrier missing. Partial names refuse. All seven names must have exact selected definitions before any format/current-row query. A valid complete object set without a published format row and without current rows is incomplete publication; rows before publication refuse. A published current carrier is admitted using the same connection and existing checks, without reopening or refreshing the snapshot. Case variants of known current names cannot evade inspection.

The existing CurrentCarrierSnapshot opener now shares read_only_carrier_connection and admit_carrier_definitions with dispatch; WAL, no-create flags, limits, defensive config, busy0, BEGIN, project/boundary/schema checks are unchanged. No external DDL or writes occur. Current snapshot construction receives the already-admitted definition result; actual publication metadata still comes from its own retained SQL transaction. Bare Kind is a classification, not authority. Borrowed current evidence cannot outlive CapturedDispatch. Non-current dispatch retains its read transaction until drop (explicit rollback), as current snapshots already do.

Legacy classifications intentionally follow frozen names-only F46 dispatch. They do not validate historical body content or claim admitted historical schemas. An inherited table with an added column is still observed legacy for that purpose. IncompletePublication describes a physical object/row prefix, not proof that act A/C was lawfully performed. Whole migration legality, marker conditions and writer authorization remain separate. BoundCarrierMissing means the named database snapshot has no known journal objects; it never means the attempt did not commit and never creates a carrier. A missing database path stays an I/O refusal without creation.

## Regression follow-up

Actual162T1 record propagation is pinned by a total-records-minus-one inner Historical(Bound) refusal. Logical propagation uses a valid marker on generation1: its bytes consume logical budget but not stored historical octets, so total logical-minus-one is above the stored total and independently tests the second inherited reader's logical limit. A plain UTF8 body-only fixture would have equal stored/logical budgets and could mask the logical mutant. The marker's tail digest is queried from its actual generation1 tail. Exact maximum succeeds; both propagation mutants are killed.

## Validation

133 security tests and strict whole-workspace/all-target Clippy pass. Six actual-SQL dispatch tests cover empty/legacy schemas, malformed partial/all-name objects, case variants, valid complete unpublished prefixes, rows before publication under restored exact triggers, concurrent publication after names, current metadata replacement after names, read-only/no-create behavior and release of retained WAL readers. One new logical-bound test plus the existing aggregate record assertion address162T1. Ten compiled mutants+baseline pass: names/definition/row order, pre-publication rows, legacy classification, case evasion, refreshed snapshot, reopened current admission, and both per-reader limits. Positive boundary client compiles; five negative clients refuse forgery, mutable objects, escaped/outlived current reference and private hook access. All36 fixtures unchanged.

Final isolated host102 passed:225 exact source files,36 fixtures,51 verified cached dependency archives,362 workspace tests and2 doctests. No source/lock drift; version/help/metadata pass.

r1 tests/Clippy preceded the additional published-metadata snapshot test. Finalr2, mutationr1,privacyr1 andhost102 use final source bytes. No failed product test. Author script/beforeimages and test additions are preserved.

## Integration still required

The physical bracket adapter still calls its prior current-only opener; it does not yet consume this dispatch object. No public host error mapper exists. 150F2/165 routes, final writer mirror-policy disposition, ledger/anchor composition, journal/witness/floor location relation and SQLite path/sidecar custody, continuous exclusion/ABA, clock/current revocation, writes/migration/pins/output/deletion and generated-consumer/selection work remain. Retained SQL state is temporal evidence, never filesystem custody or ongoing writer authority. Actual164 review found no substantive defect; its Linux-only ELOOP and internal-reader/alias/performance limitations remain acknowledged.

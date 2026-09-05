# Lifecycle SQLite carrier, proposed version 2

This package turns the generation/journal outline into reviewable design DDL.
It does not implement the product or qualify G18. Run the retained checker with:

```sh
python3 docs/coop/completion/lifecycle-carrier.check.v2.py --report /tmp/lifecycle-carrier-replay.json
```

The SQL contains six STRICT tables: generation, project_registry,
project_selection, operation_lease, transition and quarantine. The registry is
an explicit addition to the earlier illustrative five-table list. Foreign keys,
state-transition guards, immutable generation identity/path/digest fields and
connection callbacks enforce the declared write protocol. The exact callback
contracts and filesystem ordering are in `lifecycle-carrier.contract.v2.json`.

Publication updates project_selection and marks the matching transition
COMMITTED in the same SQLite transaction. COMMITTED is a transition state;
generations remain READY. A READY row alone grants no execution authority.
New leases require current verification, a verified root binding, the matching
project scope in the lock, and an acquired OS lease capability. Existing leases
keep their original generation as later project selections change.

The verification epoch has four fields: rootVersion, indexSnapshotVersion,
revocationVersion and permissionPolicyDigest. Every field participates in exact
current-state comparison. Counters preserve the security metadata i64 domain.
Changing only revocations or only applied policy invalidates old verification
tickets. The paired security successor must adopt this complete tuple; its old
root/index pair does not suffice.

Project keys are opaque, nonempty strings bounded to 1024 UTF-8 bytes. They are
never used as path segments. The host-owned registry maps a key to a separate
namespace UUID, and journal lookup is exactly:

```text
<host-owned-project-state-root>/projects/<namespaceId>/grant-journal.sqlite
```

The registry binds each ACTIVE project to canonical absolute native path bytes
and an opened directory's device, inode and birth-time identity. macOS uses
fstat birth time; Linux requires statx STATX_BTIME. Missing reliable incarnation
identity refuses namespace binding. The host allocates the key; customer files
cannot nominate another project's namespace. Renaming the same verified object
may update its locator. Replacing the object requires a new key and namespace
without transferring grants. Fresh namespace creation and directory fsync occur
before the registry commit. Retired binding tombstones cannot be reassigned.

A project-scoped lock can only be selected or leased under its own root-bound
project key. A global-only lock may be shared if it contains no project-scoped
tuples. Two known registry keys alone do not authorize cross-project lock reuse.

GC probes OS lease locks nonblockingly while holding the install fence. A busy
lease means retain, release the fence and retry later. GC cannot wait for an
operation while holding the fence that operation may need to finish. SQL foreign
keys independently protect remaining local references; callbacks account for
external lease, rollback, retained-record and policy roots.

The checker executes real SQL success/refusal cases, local file fsync/rename,
subprocess death before and after publication commit, and a real nonblocking
flock contention/release check. It preserves older operations across publication
and validates database integrity afterward. Root-identity and trust callbacks
use explicit synthetic observations; no native statx/fstat identity qualification,
release signatures, power-loss durability, or four-platform qualification is
claimed. The earlier thirteen-event lifecycle model remains frozen as narrower
evidence.

This successor repairs independent review LCR-1, LCR-2 and LCR-S1. The frozen
version 1 and its review remain unchanged; the contract pins that review,
including its exact reproducer source and observed failures.

Every admitted connection requires and checks recursive_triggers=1. Explicit
BEFORE INSERT collision guards reject replacements of primary keys and every
UNIQUE/partial identity across all six tables; registry updates also reject
unique collisions. Existing immutable-update guards remain in force. These
checks close INSERT OR REPLACE, REPLACE, and relevant UPDATE OR REPLACE paths.
Regression cases replay the four original replacement failures and additional
table/index variants with recursive triggers both enabled and fault-injected
OFF. OFF is outside the connection contract; the additional collision defenses
still refuse those writes. Existing successful publication, explicit lease
release, cleanup, retirement, and same-object rename cases remain retained.

Every TEXT column rejects embedded NUL. UUID and digest domains use exact UTF-8
byte lengths plus ASCII grammar; root hex and decimal identity lengths also
count bytes. The real-SQL corpus covers NUL prefix, middle, suffix and same-byte-
length substitutions, ASCII length boundaries, and non-ASCII substitutions in
all repeated UUID/digest carriers and relevant hex/decimal fields. Those cases
require a SQLite CHECK refusal, so a callback refusal cannot hide a weak scalar
constraint. The scope fixture callback now inspects resolved tuple scopes and
refuses project tuples inside a global-only context.

The retained report contains 200 checks: 193 SQL fixture cases, four source-pin
checks, two subprocess-death witnesses and one local OS lease-contention check.
It is reproducible with the command above and makes no product qualification
claim.

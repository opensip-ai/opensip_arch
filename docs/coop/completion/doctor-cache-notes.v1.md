# Doctor and cache integration design evidence

This unit joins distribution §8.1/8.2 to the independent S-DOCTOR surface and
real language-native corpus. It does not execute OpenSIP or qualify any platform.

Run with the pinned TypeScript 6.0.3 package already used by the native corpus:

```sh
/tmp/opensip-architecture-review-env/bin/python -B docs/coop/completion/doctor-cache-check.v1.py --typescript-root /tmp/opensip-architecture-typescript/node_modules/typescript --report /tmp/doctor-cache-replay.v1.json
```

The contract pins the exact relevant parent sections, accepted doctor/G04
contracts, completed compatibility matrix, the security report reader and its
schema, accepted reference lock, and all small corpus source files. Section
pins deliberately exclude unrelated ongoing parent edits. Gate identifiers
match file 08 exactly; G20 is component-operability and G32 is
actor-join-fixture-execution.preview.

The reader parses schemaVersion before interpreting or rendering report members.
Only integer major 1 enters the composed report reader; malformed and future
majors return no rendered members and preserve the original-byte digest. The
90-day and one-subsequent-host-minor window is a minimum support obligation,
with revocation override. It does not expire current-major support automatically.
Core/control/component versions cannot change the report's independent major.

The mode model performs actual reads of temporary metadata fixtures and retains
its invocation read/process/network/write trace. Core and requested-core never
read project or component fixtures. Project mode reads strict-config bytes and
a structurally valid completed lock, skips the local override in CI, and retains
explicit UNDETERMINED checks for corrupt or resource-limited metadata. These
are narrow metadata-read reference checks; the full configuration resolver,
trust custody and product doctor remain qualification work. Setup writes occur
before the invocation and are not represented as doctor writes. Injected
resource-limit observations do not introduce a numeric configuration limit.
Negative trace cases reject source reads, component loads, execution, network,
lock writes and analysis admission.

The 16 positive RSS series contain 336 synthetic launches: 21 for each of four
mode fixtures on each of four platform axes. Each series retains raw timestamps
and bytes. The scorer uses 10 ms samples of process T, maximum peak, median at
or after 20 ms, and the inherited all-samples median for an earlier exit.
Every launch is checked against 60,000,000 steady and 100,000,000 peak bytes;
a lone failing 21st launch fails the series. Missing records, wrong cadence,
warm pairs and VM-level observations cannot pass. Consented probes are explicitly
outside the read-only budget. These are scoring fixtures, not measured RSS;
D-102 runner/preflight identity, actual OS sampling, help/version and release
regression qualification remain required.

Cache cases execute 40 fresh TypeScript compiler programs: all eight real
quality projects under fresh, absent, stale, corrupt and attacker-populated
cache conditions. The provider extracts observed project import edges and
compiler diagnostics; a separate pure SCC evaluator applies the accepted host
cycle rule. Expectations come from the pinned corpus, never from the evaluator.
The checker compares all semantic fields to both that independent expectation
and fresh recomputation. It also verifies source reads, unchanged source bytes,
no cache read or durable result restore, and unchanged cache bytes. Unknown
Coverage stays indeterminate, including malformed, unresolved and dynamic
imports. File hash observations are design evidence, not a Snapshot/Plan/Run
identity or a substitute durable regeneration key.

Artifact-cache and newly downloaded byte cases use the same SHA-256 and
catalog/manifest/current-trust admission function. Corrupt content, changed
binding and revocation refuse both origins. Trust and signature custody here
are explicit injected observations; cryptographic admission remains covered
by the separate security unit. No cache content is analysis evidence.

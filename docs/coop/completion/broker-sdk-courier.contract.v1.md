# Typed broker SDK and result courier join

FROZEN-PROPOSED for independent review. Author: Codex protocol fixture author.
The lead accepted the typed SDK surface. Publication, ordering, caps and request
admission use exact frozen security v5, pinned by `broker-security-inputs.v1.json`.
Independent security acceptance remains a separate adoption gate. Frozen
bootstrap v2 and its launch/request-admission evidence remain unchanged. The new
bootstrap model contains only the successor parser; the typed SDK uses the final
security request boundary rather than another legacy admission helper.

The new ProviderSession broker surface is `BrokerEffects` in
`broker-sdk-api.v1.ts`. It contains only typed opaque write/read handles and
`writeHostState(handle, bytes)` / `readProject(handle)`. The SDK's requestEffect
primitive is private. Neither scratch paths nor raw resultRef, journal locator,
control sequence, operation target, grant scope or framing setter is public.
The input byte array for a write is copied before the first await; subsequent
caller mutations cannot change the staged request. The host enforces its exact
prebound target and narrower byteCap independently of the SDK's global bound.
The resultScratchRoot location is exactly `<installRoot>/projects/<namespaceId>/spawns/<spawnId>/`, with host-minted namespace and spawn UUIDs, root and stage child mode 0700. It is ephemeral SC-OPS transport, created under the project operation lease; nonempty handles require an admitted project operation. It is not a cache or generation. Cleanup follows child exit and completion of every courier reader/writer while retaining the lease. Orphan GC requires the lifecycle fence's nonblocking census to prove that lease released; live or uncertain leases preserve the directory. SDK close only releases its fds and never deletes files.

These APIs are design surfaces with synthetic examples. Shipped TypeScript
receives no handles and continues to read only the existing sealed VFS protocol.

Bootstrap v3 schema retains bootstrapVersion 1 as a scoped design successor,
not a provider/control major change. Each handle has exactly effectClass,
authorizationRef, operationRef and commitClass. HE-2 requires REVERSIBLE;
HE-1 may name REVERSIBLE or IRREVERSIBLE as selected by the host's grant contract.
A nonempty descriptor requires resultScratchRoot. The empty shipped descriptor
has no resultScratchRoot. The path is absolute, exact UTF-8, free of NUL, empty,
dot and dot-dot path components, and bounded at 4,096 UTF-8 bytes. This resource
ceiling fits inside the retained 12,288 decoded-byte bootstrap bound, admits
ordinary host-owned paths without introducing a wire path, and refuses overflow
without truncation. The D-006 decision join below records the cap rationale and executing gates.
The SDK opens and retains that directory only during bootstrap admission, before
provider callbacks. The path is not returned by any SDK method.

Opaque handles are minted by this SDK instance after bootstrap admission, with
separate runtime identity registries for HE-1 and HE-2. Constructors, copied
objects, wrong-class handles and foreign SDK handles fail before filesystem
access or dispatch. HE-1 is single use: publication/dispatch reserves that handle;
no automatic retry follows refusal, failure or uncertain completion. HE-2 repeat
use, if any, remains within the current grant and scratch aggregate limit.

For each operation the SDK allocates the next lawful component-to-host control
sequence internally and records pending `{requestSeq, handleObject, effectClass,
commitClass}` before sending its closed three-field effectRequest body. The
transport validates the ordinary schema, state and direction first. A response
can consume exactly one pending record. No response, repeated response, wrong
requestSeq, wrong commitClass, outcome sequence inconsistency or resultRef from
another response can deliver bytes. Result association uses requestSeq and the
private pending entry; result filename/hex is never sufficient authority.

The exact public result unions are:

- REFUSED carries only the existing PR-1 through PR-9 decisionClass from a lawful
  RF-6 peer refusal. The ordinary refusal remains terminal. No scratch bytes are
  resolved, and no host effect outcome is fabricated.
- FAILED or INDETERMINATE carries the corresponding host effectOutcome and the
  validated commitClass. It carries no bytes. The SDK never retries the effect.
- A completed write returns COMPLETED and the validated commitClass only after
  the receipt's length/digest matches the immutable staged input. The receipt names no file: the SDK compares its digest and length with its immutable staged bytes and never opens a receipt file.
- A completed read returns COMPLETED plus a fresh byte array only after the
  associated COMPLETED effectResult and its rr reference pass the closed grammar,
  host-root custody, per-file and aggregate limits, exact length and digest checks.
  Those bytes must come from the grant's exact member in the already sealed
  snapshot. Scratch is transport, not an additional semantic source.

Startup failure, local object misuse, malformed/unmatched wire response, scratch
custody failure, missing/tampered bytes or allocation failure rejects the Promise
through the existing SDK/provider-operability path. These are not new RF/PR
families, host outcomes, D9 classes or exit codes. API union discriminants are
local typed projections of existing host outcomes, never authority to change
findings, Coverage, policy or termination.

The executable join retains actual temporary directory/file operations:
held directory fd; stage create-new/no-follow/private mode; finite writes and
one bounded immutable copy; publication before request; host stage open/read and
cap enforcement; single-use handle; host result publication before effectResult;
SDK openat regular-file/link-count/owner/length checks before allocation; bounded
reads; digest equality; aggregate accounting; no bytes after failure; cleanup at
spawn end. Independent hostile fixtures cover symlink/hard-link/size/digest/
request-sequence/handle/result swapping and cancellation. Final security owns
the precise durability, atomic publication, cap accounting and lifetime rules.
No draft callback-only example is presented as proof of those physical joins.

The native checker retains its exact assertion count in `broker-sdk-courier.report.v1.json` and executes physical temporary files, including both reversible and irreversible write ordering, read publication ordering, held-fd reads after rename, and controlled FIFO refusal using O_NONBLOCK before fstat. Journal labels are reference ordering observations, not SQLite/witness durability proof. The checker calls the pinned security request-admission boundary with complete host context. Durable journal execution and lifecycle lease/GC enforcement remain separately pinned owners.

## D-006 numeric decision join

Owner of every row below: **Product + Security + Protocol**, with lifecycle
participation for G18. These are explicit design limits, not measured performance
claims. All limits are inclusive; one over refuses without truncation. A
legitimate admitted operation needing more is the falsification signal for a
reviewed successor. An implementation may not silently raise, tune or reinterpret
them. Ordinary OS path/component limits may refuse earlier than the carrier cap.

| Value and exact unit | Source and rationale / tradeoff | At-bound and over-bound evidence / gate |
|---|---|---|
| 16 MiB = 16,777,216 bytes per returned result; same global maximum for a staged write before the host's narrower byteCap | Security courier §7.5 inherited. Bounds individual materialization and integrity work; larger transfers require a reviewed design rather than hidden chunking or partial delivery. | Native exact-size files and 16,777,217-byte no-publication refusal; staged input global bound plus host-specific cap. G09/G21. |
| 64 MiB = 67,108,864 bytes of aggregate result publication per spawn | Security courier §7.5 inherited; four maximum-sized results bound cumulative retained transfer data until cleanup. This ceiling applies only to retained host-published HE-2 result payloads. HE-1 staging is separate, bounded by four single-use handles times 16 MiB and each host byteCap; there is no distributed reservation protocol. | Four actual 16 MiB files; a fifth one-byte publication refuses while the directory listing stays unchanged. G21/G18. |
| 128 MiB = 134,217,728 bytes conservative combined scratch payload ceiling | Derived bound: 64 MiB retained HE-2 results plus at most 64 MiB single-use HE-1 staged bytes; the actual four-handle mix cannot exceed it. This is a payload-byte bound, excluding filesystem metadata and in-memory buffers; no combined 64 MiB claim is made. | Algebraic join to four-handle and per-stage limits plus native 64 MiB result-publication boundary; a supported operation needing more requires a reviewed successor. G09/G21/G18. |
| 4,096 UTF-8 bytes for resultScratchRoot | Scoped bootstrap successor explicitly permitted by frozen security §7.4. A bounded absolute host path fits inside the existing descriptor byte ceiling; the SDK never exposes it as a provider path API. | Exact 4,096-byte non-ASCII path carrier and 4,097-byte refusal, plus structural/native custody checks. G21/G18. |
| Four handles per spawn | Inherited bootstrap v1/v2 choice. Keeps the initial synthetic broker surface finite; fifth registration refuses rather than dropping an operation. Initial shipped TypeScript has zero. | Empty, one, four, fifth, repeated-operation/different-grant and duplicate-grant cases. G09/G21. |
| 16,384 ASCII bytes encoded; 12,288 UTF-8 JSON bytes decoded | Inherited bootstrap representation ceilings, base64 4:3 ratio. Encoded bound is checked before decoding; decoded bound after. Canonical base64 and strict JSON remain separate rules. | Retained exact decoded boundary/encoded equality, encoded 16,385-byte failure, decoded one-over necessarily exceeding the encoded cap, bad alphabet and noncanonical unused bits. G21. |
| Eight JSON container levels | Inherited bootstrap parser work bound; valid closed carriers are shallower. | Retained depth-eight shape check, depth-nine and depth-1,500 controlled refusals. G21. |

The file/cap probes are physical reference execution on one host. Journal labels
are explicit ordering observations and never evidence of SQLite/witness
persistence, syscall crash atomicity, operation-lease correctness or four-platform
qualification. G18's independently retained lifecycle gate owns those joins.

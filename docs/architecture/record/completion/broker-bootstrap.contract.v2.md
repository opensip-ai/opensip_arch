# Broker bootstrap and runtime entry contract

PROPOSED v2, successor repairing BROKER-M1 and BROKER-S1. Author: Codex protocol fixture author, implementing the lead's scoped
WA1/WA8 decisions. This unit supplies request admission, SDK handle acquisition,
and exact runtime launch design evidence. It does not claim a completed HE-2
returned-byte courier, production execution, or architecture approval.

## Authority and scoped successors

The control major, five descriptors, sixteen message bodies and 1,024-byte
opaque reference envelope remain `control-completion.schema.v3.json` and the
reviewed control v5 package. `broker-bootstrap-impact.v1.json` explored an older
2,048-byte enlargement; that alternative is not adopted. No control v6 is needed.

This proposal supersedes only these sentences:

- `security-completion.v2.md` §5.4 **Sequence and identity**, the description
  exposing `gj:<base64url(projectKey)>:<grantGeneration>:<seq>` as authorizationRef;
  and §7.1/7.2's `authorizationRef gj:…` spelling. The locator remains unchanged
  inside the host journal. It no longer crosses the component interface.
- `delivery.v2.json` `/typescriptSemanticSubstrate/packaging/launch`, the prior
  three-element argv; `/typescriptSemanticSubstrate/authority/environment/setExactly`
  and `/extraVariables`, specifically the blanket later-protocol-major prerequisite
  for additional variables. The fixed bindings below are the sole extension.
- `/typescriptSemanticSubstrate/authority/scratch` is concretized: the private
  per-child scratch path is passed as cwd, not another environment key or descriptor.

These structural launch bindings convey no semantic input, config setting,
Plan identity recipe, dynamic operation registration, or permission grant.
Existing host Plan and sealed VFS authority remains unchanged. Actual source
bytes and selectors are pinned in the retained report/freeze.

## Host map and SDK acquisition

Before launch, the host registers the exact operation target and parameters and
completes the existing durable GRANT protocol. For each distinct grant in this
spawn it generates a fresh CSPRNG 128-bit value, spelling the courier handle
`ah:<32 lowercase hexadecimal digits>`. Regenerate on collision, with at most eight candidate draws per allocation. Exhaustion aborts bootstrap, clears the private map, and revokes already registered grants through the existing journal path. No partial bootstrap or spawn is exposed. A handle maps
host-side to the internal journal locator, exact operation, component identity,
install generation, admitted manifest, platform, policy, project key, grant
generation, spawn identity, PID and boot UUID. Neither the locator nor any of
these private values are reconstructed from handle text. Handle possession alone
never authorizes an effect. Process context comes from the host's established
child transport, not fields supplied by the component.

The bootstrap contains one entry per grant, at most four. authorizationRef is
unique. operationRef retains `op-<32 lowercase hex>` and may repeat when one
operation needs several distinct grants. A fifth grant refuses before launch;
never silently truncate. Registrations close before launch. Spawn termination
invalidates the entire map. Each HE-1 grant binds PT-FS-WRITE-HOST-STATE and each HE-2 grant binds PT-FS-READ-PROJECT, in addition to PT-HOST-EFFECT-BROKERED. Both tokens require current manifest declaration, absence of denial, and an exact host-approved scope containing operationRef, target and parameters. Scope is not supplied by the requester. Each request looks up the map and rechecks the
current journal, revocation, current manifest declaration and policy, all exact
bindings, and the registered target/parameters. Unknown, foreign-spawn, wrong
binding or dead handle is RF-6/PR-4; current policy denial is PR-2, undeclared
token PR-1, revocation PR-5, following existing permission predicate precedence across all required tokens: unknown token, missing declaration, explicit deny, revoked, confinement, scope mismatch, consent, exclusive ownership. The first failing predicate wins regardless of token iteration order. This model exercises the declaration, denial, revocation and scope predicates; other security predicates retain their separate carrier requirements. No new RF
family, PR class, D9 code, or host effect outcome is added.

The host supplies OPENSIP_BROKER_CONTEXT as canonical unpadded base64url of a
strict UTF-8 JSON object:

```json
{"bootstrapVersion":1,"handles":[{"effectClass":"HE-1","authorizationRef":"ah:11111111111111111111111111111111","operationRef":"op-22222222222222222222222222222222"}]}
```

These are deterministic TEST handles, not credentials for any running host.
The carrier schema is closed. effectClass is HE-1 or HE-2, both refs use the
exact ASCII grammars above, and handle count is at most four. Unknown fields,
duplicate JSON names or authorizationRefs, invalid UTF-8, surrogates, NaN,
noninteger version, bad base64 spelling, or excessive depth/size fail startup.
JSON member ordering and whitespace may vary; only base64 spelling is canonical.
The host emits sorted compact JSON. The initial shipped TypeScript profile has
**empty handles**. Nonempty fixtures are synthetic registered host operations.

SDK first entry strips all environment keys outside the fixed set below, then
consumes and unsets the bootstrap key exactly once before giving control to
provider callbacks. Failure also removes the key. A missing key is a startup
configuration failure; an empty handles array succeeds. Returned handles are
opaque SDK-created objects. `requestEffect(handle)` accepts only an object in
that SDK instance's private identity registry, assembles the immutable three
body fields itself, and uses its host-bound dispatcher. It has no parameter,
target, frame, findings, policy, Coverage, D9, or exit setters. Unknown, copied,
forged-constructor, or another SDK's object fails locally before dispatch.

The Python constructor's dispatcher injection is the harness's host binding,
not a provider API. Python private attributes are not a sandbox boundary: these
checks demonstrate API discipline; a hostile component can always construct
wire bytes, which the host must validate independently. The reference host
model derives scope matching from map/current/transport values, exercises the
existing permission and journal models, and stops at request admission. Actual
RA/RCI/ICI, witness durability and effects remain under the security journal
contract. It does not assert successful effect execution or HE-2 data delivery.

Bootstrap failure or local unknown handle is an SDK/provider failure; it stops
the worker without producing a valid terminal response. Existing
`delivery.v2.json` `/typescriptSemanticSubstrate/supervision/protocolOrCrash`
and `/terminationIntegration/providerProtocolFault` map that nonzero exit or
EOF-before-terminal to `provider-protocol` / `PROVIDER.PROTOCOL_VIOLATION`.
No coherent Run is fabricated. A host-side missing/mismatched runtime asset or
unspawnable process retains `/supervision/deliveryFailure` instead.

## Exact runtime launch and environment

The host verifies the exact signed closure, then invokes without a shell:

```text
[absBundledNode, --no-addons, --no-global-search-paths,
 --openssl-config=absVerifiedEmptyConfig, absBundledProviderEntry]
```

`share/openssl-empty.cnf` is a zero-byte signed release closure member, SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Verify its exact length/hash like the runtime and provider. No external ICU data
directory is used: full ICU compiled into the release runtime is an inventory
requirement. CLI option behavior is documented by the primary Node sources:
[OpenSSL config](https://r2.nodejs.org/docs/latest-v24.x/api/cli.html#--openssl-configfile),
[no addons](https://r2.nodejs.org/docs/latest-v24.x/api/cli.html#--no-addons),
[no global search paths](https://r2.nodejs.org/docs/latest-v24.x/api/cli.html#--no-global-search-paths).
Runtime/compiler version selection remains the signed release's job.

The host-created per-child scratch directory is mode 0700 and cwd. Destroy it
when the child exits. Host exec environment is built FROM EMPTY with exactly:

```text
LC_ALL=C
LANG=C
TZ=UTC
UV_THREADPOOL_SIZE=4
OPENSIP_BROKER_CONTEXT=<host-encoded bootstrap>
```

HOME, PATH, NODE_*, OPENSSL_CONF, SSL_CERT_*, proxies and every other ambient key
are absent. No ENV grant can widen this initial profile. A future provider
profile requires its own reviewed explicit rule. Runtime initialization is
trusted TCB and precedes SDK entry. The native macOS probe demonstrates that
Node/runtime initialization may synthesize `__CF_USER_TEXT_ENCODING` even with
this exact exec input. The SDK therefore removes runtime-added keys too before
provider callbacks. The report records raw and sanitized observations separately;
it does not claim raw Node process.env always equals the exec environment.
Subprocess exec is constructed from the four fixed post-consumption values;
each descendant entry repeats sanitization. The bootstrap key never propagates.
This remains process isolation and authority reduction, not OS confinement.

## D-006 numbers and substitution properties

| Choice | Purpose and boundary | Substitute-invariant checks and gates |
|---|---|---|
| 128 random bits / 35-character ah spelling | Unpredictable nonsemantic per-grant/spawn courier; collision retry and host map remain authority | Foreign spawn, unknown handle, collision and binding refusals; G20/G21 |
| Eight candidate draws per allocation | Bound entropy failure; exhaust to bootstrap refusal, invalidate partial map and revoke prior grants without spawning | constant entropy, exact draw count, no partial bootstrap or effects; G20/G21 |
| Four grants | Explicit finite initial broker resource envelope; fifth refuses without truncation; empty shipped profile | zero/one/four/fifth and two-grants-one-operation fixtures; G20/G21 |
| 16,384 encoded ASCII bytes / 12,288 decoded bytes | Base64 4:3 representation ceiling; check encoded size before decode, decoded size after; byte limits are admission limits, not performance estimates | exact decoded bound, encoded one-over, canonical unused bits, bad UTF-8; G20/G21 |
| JSON container depth eight | Bound parser stack before JSON admission; closed valid carrier needs only three levels | depth eight malformed shape, depth nine rejection and depth 1,500 resource probe; G20/G21 |
| UV_THREADPOOL_SIZE four | Freeze Node's default pool width as an operability setting; avoid ambient tuning becoming implicit state; no throughput claim | exact host input and native child observations; G14/G24–G28 |
| scratch mode 0700 / empty config zero bytes | Owner-only scratch and no ambient OpenSSL config content | actual cwd/mode, zero-byte digest, post-exit removal; G14/G24–G28 |

A replacement SDK or runtime must preserve these closed wire/API properties,
no authority in courier text, durable/current host validation, exact launch
closure, startup failure mapping, no semantic output mutation, deterministic
environment construction, and retained negative classes. Increasing the broker
count or changing launch inputs requires a scoped reviewed design successor,
not implementation discretion. G14 verifies the signed runtime/config closure;
G20/G21 execute SDK and control integration; G24–G28 execute the shipped provider
startup/teardown and failure behavior. Native probes here are reference evidence,
not release gate passage. The 150 checks include a byte-identical replay of all
484 previously reviewed control checks and an actual Node 24.16.0 probe on one
host. Supported OS release qualification and HE-2 returned bytes remain separate.

### 9.5a The native-context inputs carrier (`typescript-semantic`; contract successor NSS-F1)

**Why it exists.** §2.4 and §9.5 require the TypeScript worker to recompute `TypeScriptNativeContextV2` from its
own sealed inputs, but the major-2 `OpenUniverse` carries only the context's identity and the configuration
graph's digest. Three inputs of that recomputation are not in the sealed snapshot: the selected entry
configuration (inside `TypeScriptConfigGraphV1`, §2.2), the unit root from which TSR-1's `package.json` and
lockfile ancestor walks start (§1.4 `WorkspaceUnitV2.rootPath`), and the retained `ResolvedNodeModulesLayoutV1`,
a resolution observation that is not snapshot inventory (§2.2). A worker must never infer them, for example by
searching configuration candidates until a digest matches. This section carries them.

**Token and negotiation.** `native-context-inputs-v1` is an optional, non-identity `typescript-semantic`
capability token. It does not enlarge the identity token set. It is a token the Plan needs (§9.1, step 1) for
**every** `typescript-semantic` worker, because every such worker owes the recomputation: a signed row without it
is never spawned, and the affected Coverage keys are `unknown / provider-unavailable` (cause
`capability-missing`). When it is in both the Hello and the HelloAck token arrays:
- the `OpenUniverse` payload is `TypeScriptOpenUniverseV3`, which is `TypeScriptOpenUniverseV2` with every member
  unchanged plus `nativeContextInputs`;
- the pre-Analyze `Unavailable` payload is `PreAnalyzeUnavailableV1` (unchanged) or
  `TypeScriptPreAnalyzeInputMismatchV1`.

When it is absent, `TypeScriptOpenUniverseV2` and `PreAnalyzeUnavailableV1` remain, unchanged. A V3 or
input-mismatch payload without the token, or a V2 payload with it, is `PROVIDER.PROTOCOL_VIOLATION`. Protocol major
stays 2. No frame name, phase, transition row, terminal kind, limit member, commitment, identity version or
`rust-semantic` record changes. The field-level records are
`docs/implementation/m3/native-successors-fa/nss-f1/design/native/native-context-inputs.schemas.v1.json` (closed,
with its `x-opensip-native-context-inputs-law`).

**The carrier.** `NativeContextInputsV1` = `{context, configGraph, nodeModulesLayout, unitRoot}`:
- `context`: the exact retained `C` bytes of the `TypeScriptNativeContextV2` that
  `universe.resolvedInputs.nativeContextId` names (the bytes `bind_typescript_universe` admitted);
- `configGraph`: the exact retained `C` bytes of the `TypeScriptConfigGraphV1` that
  `universe.resolvedInputs.tsconfigGraphHash` names;
- `nodeModulesLayout`: the exact retained `C` bytes of the `ResolvedNodeModulesLayoutV1` that the context's
  `nodeModulesLayoutDigest` names, or null exactly when that digest is null;
- `unitRoot`: the `rootPath` (`InternalUnitRootV1`, `""` for the project root) of the `WorkspaceUnitV2` the
  universe was minted for.

No closure, compiler, standard-library or toolchain record is carried. Those members of the context come from
the worker's own installed signed closures, so a worker running other bytes than the Plan's computes another
context and refuses, as §2.4's platform-specific identity requires.

**Digest joins, before `UniverseAccepted`.** The worker checks:
1. `"sha256:" + hex(H("native.context.typescript.v2", context))` equals `universe.resolvedInputs.nativeContextId`;
2. `hex(SHA-256(configGraph))` equals `universe.resolvedInputs.tsconfigGraphHash`;
3. `nodeModulesLayout` is null exactly when the context's `nodeModulesLayoutDigest` is null, and otherwise its raw
   SHA-256 equals that digest;
4. `universe.resolvedInputs.nodeModulesInReadSet` equals "`nodeModulesLayout` is not null".

Each carried byte string must parse as the closed record it names and re-encode under `C` to the identical
bytes, and the decoded context and the universe must agree where §2.4 makes them overlap. Any failure is a
malformed or uncorrelated `OpenUniverse`: the worker sends no `UniverseAccepted` and exits nonzero, and the host
observes a process fault before any source byte is sent. The host checks the same joins before spawn and refuses
a failure there as a host invariant, so the worker-side failure is unreachable from a conforming host.

**The selection, and nothing else.** The worker takes exactly these values from the carrier as host and Plan
authority:
- `configGraph.entryConfigPath`;
- for every layout row, its `installPath`, `realPath`, `packageName` and `packageVersion`, and the layout's
  presence;
- the `contentSha256` of a layout row whose manifest (`realPath`, at most one trailing `/` removed, then
  `/package.json`) is not a sealed VFS file;
- `unitRoot`.

`unitRoot` is the start directory of TSR-1 R-6.1 and R-6.2's ancestor walks and nothing else. It is never a
compiler-host, Program, subject or membership input. Every value derived from it is a context member that the
recomputation compares byte for byte. So a wrong `unitRoot` produces one of three things: a closed-key refusal
(for example a malformed `package.json` met on its walk), a completed context that differs, or the identical
context, in which case nothing the worker computes has changed. It is bound by no digest; this restricted use is
what makes it admissible. The worker never copies any other member of the carried context, graph or layout
into its recomputation, never infers a selection from a digest, and never enumerates configuration or unit
candidates to match one.

**Recomputation and outcomes, after `SnapshotAccepted`.** The worker derives, in this order:
1. **The graph `G'`** by M3-B item 14a's function, from `configGraph.entryConfigPath` over the sealed VFS. `G'` is
   `{schemaVersion 1, entryConfigPath null, nodes []}` when the entry is null.
2. **The context `X'`** from `G'`, the sealed VFS, the selection and its own closures, under §2.4 and TSR-1. Under
   `js-synthesized`, `jsx` is decided from `universe.resolvedInputs.programRootFiles`. `X'.nodeModulesLayoutDigest`
   is null when `nodeModulesLayout` is null, and otherwise the raw SHA-256 of `C(L')`, where `L'` is the carried
   layout with each row's `contentSha256` replaced by the sealed VFS digest of its manifest wherever that manifest
   is a sealed VFS file.

It then decides, first match wins:

| Case | Terminal |
|---|---|
| step 1 refuses | `TypeScriptPreAnalyzeInputMismatchV1` `{input: config-graph, outcome: refused, refusalKey}` |
| step 2 refuses | `TypeScriptPreAnalyzeInputMismatchV1` `{input: native-context, outcome: refused, refusalKey}` |
| `H(X')` differs from `nativeContextId` | `PreAnalyzeUnavailableV1` (`native-context-mismatch`), unchanged |
| `C(G')` differs from `configGraph` | `TypeScriptPreAnalyzeInputMismatchV1` `{input: config-graph, outcome: differs, planBoundDigest, recomputedDigest}` |
| otherwise | `NativeContextVerified` |

- **Refusals.** A refusal is only a decision under the closed key set of the schema's law: M3-B item 14a's four
  keys for step 1, and TSR-1 §7's phase 2, 3, 4-`references` and 5 keys for step 2, without subject. TSR-1 phase 1
  and the §2.4 closure keys concern the worker's own installation. They, resource exhaustion and every other
  inability are process faults, never this payload. The worker does not evaluate TSR-1 phase 4's literal-root and
  root-count checks.
- **Equal ids.** `PreAnalyzeUnavailableV1` keeps its rule: equal ids are `PROVIDER.PROTOCOL_VIOLATION`. A graph
  disagreement under an equal context therefore takes the input-mismatch payload, never a manufactured context
  mismatch.
- **`NativeContextVerified`.** Under the token, `equal: true` also asserts that `G'` equals the carried graph and
  that neither step refused.
- **Pre-Analyze work** is pure data: parsing, hashing and the item 14a, TSR-1 and §2.4 derivations over the sealed
  VFS. No compiler Program is constructed before Analyze.

**`TypeScriptPreAnalyzeInputMismatchV1`** = `{executionId, snapshotId, planId, reason: "native-input-mismatch",
input, recomputation}`.
- **Phase.** It is lawful only under the token and only while the host waits for `NativeContextVerified` (row
  T2-10, `unavailablePayload` pre-analyze).
- **Correlation.** `executionId`, `snapshotId` and `planId` equal `OpenUniverse`. For `outcome: differs`, `input` is
  `config-graph`, `planBoundDigest` equals `universe.resolvedInputs.tsconfigGraphHash`, and `recomputedDigest`
  differs from it. `outcome: differs` with `input: native-context` is `PROVIDER.PROTOCOL_VIOLATION`.
- **After it.** It is followed by zero-exit, EOF and DONE, exactly as `PreAnalyzeUnavailableV1` is, with the same
  post-terminal and process-fault rules. A malformed or uncorrelated payload, equal digests, the forbidden
  combination, an unlisted key, the payload without the token, or the wrong phase is
  `PROVIDER.PROTOCOL_VIOLATION`.
- **Host conversion.** It is identical to `PreAnalyzeUnavailableV1`'s (§9.7). `input`, `outcome`, the digests and
  `refusalKey` are operational evidence only, never a public `DomainDetailCode`.

**What stays Plan authority.** `programRootFiles` and `jsRootFiles` are universe members. The worker builds its
Program from them, and does not re-derive them: TSR-1 R-4.2's candidates exclude `outside-project-boundary` rows,
and the boundary inventory is a security-owned input the Plan does not retain (§1.4, U-4b step 5; U-8), so a
snapshot-only derivation would not be independent but wrong. A root list that changes while the context stays
equal yields `NativeContextVerified`.

**Host duties.** The host builds `nativeContextInputs` from the records the Plan already bound:
- the context bytes given to `bind_typescript_universe`;
- the retained graph and layout, both required binding inputs (§2.2);
- the `rootPath` of the unit in the retained `UnitMembershipV1` that `PlanId` binds through `membershipDigest`.

It sends the retained bytes exactly, never a re-encoding of a decoded copy. It checks the four joins and the
`unitRoot` grammar before spawn.

**Bounds.** Each carried byte string is a `C` encoding under the foundation 4 MiB descriptor bound
(identity-and-evidence §3), so the carrier adds at most 12,599,382 bytes of deterministic CBOR to `OpenUniverse`:
the carrier map, with a maximal `unitRoot` and its member keys, is at most 12,599,362 bytes, and its own key 20. `maxFramePayloadBytes` (67,108,864) and the host's exact send-schedule
measurement are unchanged and remain the only frame bound. No limit member is added.

Cases: `typescript-open-universe-v3-carries-the-retained-context-graph-and-layout-bytes`,
`typescript-carrier-whose-bytes-do-not-hash-to-the-plan-bound-ids-is-refused-before-universe-accepted`,
`typescript-carrier-with-non-canonical-context-bytes-is-refused`,
`typescript-worker-recomputation-from-production-host-frames-verifies`,
`typescript-self-consistent-wrong-host-context-is-native-context-mismatch`,
`typescript-config-graph-disagreement-under-an-equal-context-is-input-mismatch`,
`typescript-recomputation-refusal-is-input-mismatch-never-a-sentinel-digest`,
`typescript-root-list-change-under-an-equal-context-verifies`,
`typescript-open-universe-v3-without-the-token-is-a-protocol-violation`,
`typescript-row-without-native-context-inputs-v1-is-never-spawned`.

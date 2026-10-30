# NSS-F1: the native-context inputs carrier for TS2 (native contract successor), r2

2026-10-30. Author: Claude Opus 5.5 (high), R3-FRONTIER, Herdr w1R:p1, under coordinator decision LD-Q-37 (session
9ce22ffd, w1:p1). Status: **PROPOSED, r2**, after Codex REVIEW-r1 (`REVIEW-r1.md`, REQUIRED-FINDINGS: RF-1, RF-2; NB-1 to NB-6). It needs Codex `NSS-F1: ACCEPT` (R3-FRONTIER, gpt-6-astra/high) and
coordinator adoption under OD-AUTO-1. It changes no product file and no architecture file. It is a documents-only
successor in FA-2's form; its binding is a later step (§12).

**Pins.** Product main `d643410` (r1 was written at `c1e9df9`; the two commits between them change only the design lock, by C1c-1's successor 191, and census receipts, none of them a parent or protocol file). Architecture `45d11ae73`; C1c-1's architecture accept commit `fb396900f` (worktree `opensip_arch-c1c1`) holds the same bytes of every parent. Every parent below is checked at its exact bytes by
`evidence/build_overrides.py`.

**What it answers.** Escalation X-F1-1 Q1 (`../f1/ESCALATION-X-F1-1.md`), from F1 plan review RF-1. TS2 gives the
worker only digests of the configuration graph and the native context. The worker therefore cannot recompute
`TypeScriptNativeContextV2`, as NE §9.5 requires (NE:1618-1620, NE:2950-2952), and cannot build a Program with the
project's options. LD-Q-37 chose option A, an additive, token-negotiated carrier of the retained preimages. This
document specifies it, and keeps option A.

## r2 changes

| # | Finding | Change | Where |
|---|---|---|---|
| 1 | **NSS-F1-R1-RF-1** | The NE:2953 insertion no longer puts refusals "under an equal context". It names two cases: (a) a graph disagreement after a completed recomputation whose context id equals the Plan-bound one; (b) a closed-key refusal of the graph or context recomputation, for which no context is completed and no equality or recomputed id is asserted. A completed differing id stays `native-context-mismatch`, first in §9.5a's order. NC-8 and NC-9 now state that no context digest exists in them. | `evidence/build_overrides.py`, `overrides.json` (NE:2953); §10 |
| 2 | **NSS-F1-R1-RF-2** | The NE:1620 insertion now says the entry and the layout are digest-bound, and that `unitRoot` is bound by no digest and admissible only as the start of TSR-1 R-6's walks, with every other use prohibited. LD-N4 and §9.5a's explanation now allow the third outcome of a wrong root: a closed-key refusal (for example a malformed `package.json` on its walk). | `evidence/build_overrides.py`, `overrides.json` (NE:1620); `section-9-5a.md`; LD-N4 |
| 3 | NB-1 | The schema's description no longer claims every inherited member is restated: the universe is named by selector, and admission of `TypeScriptOpenUniverseV3` is composed (the record and the inherited `TypeScriptSemanticUniverseV2`). The schema now encodes the input-specific key sets: `config-graph` admits only item 14a's four keys, `native-context` only TSR-1's seven. The evidence uses a complete inherited-valid universe and adds five composed-admission cases (complete; empty; a missing member; an extra member; a wrong major) and two wrong-pairing cases. The fixture preimages are also checked against NES's closed records. | `design/native/native-context-inputs.schemas.v1.json`; `evidence/build_nss_f1.py`, `evidence/vectors.json`; §12 |
| 4 | NB-2 | X-NSS-PRICE now enumerates every host operation LD-N5 and LD-N8 impose, and offers a typed prior-admission result as the alternative. | LD-N10; §9 |
| 5 | NB-5 | The architecture-grep sentence no longer limits the historical copies to three directories. | LD-N11 |
| 6 | NB-6 | M-1 names its exact mutation; the other member classes rely on NC-5, the field inventory and source review. | §10 |
| 7 | — | Re-pinned to product `d643410`; `build_overrides.py` now reads a newly locked successor record from another architecture worktree (`--record-root`), checked against the lock's bytes and sha256, and checks the lock's 191 successors. | header; §12 |

No carrier, selection, outcome, payload member, bound or identity changes. NB-3 and NB-4 asked for no change.

## Short names

Paths are relative to `/Users/sb/code/opensip-ai/opensip_arch` (architecture) or `/Users/sb/code/opensip-ai/opensip`
(product), or to `lead-2026-10-25/` for the unit files.

| Name | Document | Bytes | sha256 |
|---|---|---|---|
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` | 329,013 | `83b99783…` |
| **NES** | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered; not edited) | 277,967 | `2d37b810…` |
| **HS / PHS** | the current handshake parents: `docs/implementation/m3/native-successors-fa/rust-commit-alignment-r2/design/native/provider-handshake.schemas.v1.json` and its `product/schemas/sources/handshake-v1.schema.json` (identical; the product source map selects them) | 38,182 | `1fc57cbc…` |
| **ST / PST** | the current startup parents, the same directory's `provider-startup.schemas.v1.json` and `product/schemas/sources/startup-v1.schema.json` (identical) | 34,838 | `e8b2aae5…` |
| **T2O** | `docs/coop/design-corrections/native/typescript-protocol2-order.v1.json` | 11,341 | `007ef7af…` |
| **DLV** | `docs/coop/artifacts/delivery.v2.json` | 143,995 | `47b6cfd1…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135,448 | `c82404f3…` |
| **MB** | `docs/implementation/m3/config-discovery-b/PROPOSAL.md`; item 14a is MB:605-700 | 144,164 | `c1d7be04…` |
| **FA2** | `docs/implementation/m3/native-successors-fa/fa-2/README.md`, the form precedent | 37,836 | `59381765…` |
| **TSR1** | `tsr1/TSR-1-r4.md` (Parts P and R adopted; Part S deferred, LD-Q-17) | 93,986 | `be654c41…` |
| **ESC** | `f1/ESCALATION-X-F1-1.md` | 5,495 | `e58d68ea…` |
| **F1R** | `f1/plan/REVIEW-r1.md` (F1 plan review r1) | 15,153 | `c7c338f2…` |
| **F1P** | `f1/plan/PLAN-r1.md` | 29,867 | `e8a4fdbe…` |
| **CM** | `coordinator/msg-f1.txt` (LD-Q-37, LD-Q-38) | 879 | `53af5a8d…` |
| **SEND** | product `crates/components/src/provider_protocol/ts2/send.rs` | | `864547e9…` |

The unit's own files, under `nss-f1/`:

| File | What it is |
|---|---|
| `NSS-F1-r1.md` | this document |
| `section-9-5a.md` | the text appended to NE as §9.5a (the prose owner) |
| `design/native/native-context-inputs.schemas.v1.json` | the new closed schema document, with `x-opensip-native-context-inputs-law` |
| `design/native/provider-handshake.schemas.v1.json` and `product/schemas/sources/handshake-v1.schema.json` | the handshake successor copies (identical, 39,848 B, `260fb535…`) |
| `overrides.json` | the 18 insert-only passage overrides, generated |
| `evidence/build_overrides.py` | builds and checks `overrides.json` and the handshake copies |
| `evidence/build_nss_f1.py`, `evidence/vectors.json` | worked vectors, schema cases, reference joins, the decision order and the size bound |
| `evidence/bound_selectors.py`, `evidence/bound-selectors.txt` | the selectors the product lock already binds |

## 1. The problem, exactly

1. **The law requires a real recomputation.** The worker "recomputes the context from its own sealed inputs; a
   differing byte is `Unavailable(native-context-mismatch)` before Analyze" (NE:1618-1620; NE:2950-2952). An honest
   `NativeContextVerified{equal:true}` needs a real recomputation, and equal ids in a pre-Analyze `Unavailable` are a
   protocol violation (NE:3205-3226).
2. **What the worker receives today.** Hello, then `TypeScriptOpenUniverseV2` (ST `$defs/TypeScriptOpenUniverseV2`),
   then the snapshot. The universe's `resolvedInputs` hold `tsconfigGraphHash` and `nativeContextId`, both digests.
   "There is no separate context member" (NE:3190-3192). The host's input record agrees: `Ts2Plan` has no context
   member (SEND:78-105).
3. **Three inputs of the recomputation are not in the sealed snapshot.**
   - **The selected entry configuration.** It is `entryConfigPath` inside the `TypeScriptConfigGraphV1` preimage
     (NE:1330-1340). It is either the unit's marker or an explicit program entry (product
     `crates/evaluator/src/enumeration_join.rs`:698-710), so it is a host selection, not a function of the
     snapshot.
   - **The unit root.** TSR-1's `package.json` and lockfile walks start from it (TSR1:894-919). It is
     `WorkspaceUnitV2.rootPath` (NE:632-660). For an explicit entry it is not the entry's directory, and under
     `js-synthesized` there is no entry at all.
   - **The retained layout.** `ResolvedNodeModulesLayoutV1` rows are not snapshot inventory (NE:1399-1418). The
     files the analysis reads in a listed package are snapshot rows (NE:732-741), but the row set is the host's walk
     outcome (product `crates/host/src/node_modules_layout.rs`:767-814).
4. **What the worker must not do.** It must not infer the host's selection from a digest, for example by searching
   configuration candidates until `tsconfigGraphHash` matches, and it must not silently extend a closed payload (F1R
   item 1; ESC Q1).
5. **A second consequence.** Without the effective options the worker cannot build a TypeScript Program with the
   project's compiler options at all. F1-c, TSR1-C31 (CP-WORKER-1) and every F2 fact depend on that.

## 2. The design in one paragraph

A new optional, non-identity `typescript-semantic` capability token, **`native-context-inputs-v1`**, negotiates
**one added member, `nativeContextInputs`, on the existing `OpenUniverse` payload**, and **one added pre-Analyze
`Unavailable` payload**. This is the `target-attribution-v2` / FA-2 pattern, within TypeScript major 2. The carrier
holds the **exact retained `C` bytes** of the Plan-bound context, configuration graph and (when non-null) layout,
plus the unit root. Before `UniverseAccepted` the worker checks each preimage's digest against the Plan-bound id it
already holds. It takes **only the selection** from them: `entryConfigPath`, the layout rows' paths, names and
versions, and the unit root. It re-derives every other value from the sealed VFS and its own signed closures, and
compares byte for byte. A context that differs keeps the unchanged `PreAnalyzeUnavailableV1`. A configuration-graph
disagreement under an equal context, or a recomputation refusal, takes the new
`TypeScriptPreAnalyzeInputMismatchV1`, with the same host conversion. The token is a token the Plan needs for every
TypeScript worker. Without it, every frame, payload, vector and identity is byte-identical to today.

## 3. Lead decisions

Each is made under LD-Q-37's authorization to choose with reasons. Each names the alternatives it rejects.

### LD-N1. The carrier rides on `OpenUniverse`, as one negotiated member

- **Decision.** Under the token, `OpenUniverse` carries `TypeScriptOpenUniverseV3` = `TypeScriptOpenUniverseV2`
  with every member unchanged, plus `nativeContextInputs: NativeContextInputsV1`. `UniverseAccepted` is unchanged.
- **Why `OpenUniverse`.**
  1. **It is the universe-preimage frame.** It already carries the universe whose `resolvedInputs` name the context
     and the graph (NE:3166-3175). The preimages join to those ids in the same frame, with no cross-frame state.
  2. **Reject before disclosure.** The digest joins need no snapshot. A worker that sees an incoherent carrier
     refuses before `UniverseAccepted`, so the host sends no source byte (NE §9.1's ordering principle,
     NE:2846-2866).
  3. **No new phase.** T2O's rows, `UniverseAccepted` and the snapshot frames are untouched.
- **Rejected:**
  - **A new host→worker frame before the snapshot.** It adds a frame name, a phase and two T2O rows, and changes the
    abstract table the product carriers pin (T2O `007ef7af…` is pinned by product `design-lock.json` and
    `schemas/wire/native-carriers-v1.json`). It buys nothing over a member.
  - **Carrying the preimages on `Analyze`.** The recomputation must finish before `NativeContextVerified`, which
    precedes `Analyze` (NE:2992-2997).
  - **A member of the universe or of `resolvedInputs`.** That changes the universe identity, every `fact2`,
    `scope2` and `coverage2` that names it, and `PlanId`. This is the escalation condition of `PLAN.md`.

### LD-N2. The token is needed for every TypeScript worker

- **Decision.** `native-context-inputs-v1` is appended last to `TypeScriptCapabilityToken` (HS copy;
  `TypeScriptCapabilitiesV2.maxItems` 12 → 13). It is not an identity token. It is "a token the Plan needs"
  (NE:2848-2853) for **every** `typescript-semantic` worker. A signed row without it is never spawned: the keys are
  `unknown / provider-unavailable`, cause `capability-missing`.
- **Why every worker.** Every TS2 exchange has a Plan-bound `nativeContextId` and owes §9.5's recomputation. A
  worker without the carrier cannot honestly emit `NativeContextVerified{equal:true}`. Spawning it would invite
  exactly the dishonest verification RF-1 forbids.
- **Cost.** No signed TypeScript provider release exists yet (F4 signs; MAP row F1). M3's own F1/F4 release carries
  the token. So no existing row loses.
- **Rejected:**
  - **An optional token whose absence spawns a worker that verifies by digest only.** That is option C (amend
    §9.5/§2.4 to trust the host), which LD-Q-37 rejected.
  - **A protocol major 3.** Not needed: the change is additive within major 2, as `target-attribution-v2` and FA-2
    were (NE:2811; FA2 "Within the current majors").

### LD-N3. What the carrier holds: three retained byte strings and the unit root

- **Decision.** `NativeContextInputsV1` = `{context, configGraph, nodeModulesLayout, unitRoot}`.
  - `context`, `configGraph` and `nodeModulesLayout` are CBOR byte strings holding the **exact retained `C`
    bytes** of `TypeScriptNativeContextV2`, `TypeScriptConfigGraphV1` and `ResolvedNodeModulesLayoutV1`.
    `nodeModulesLayout` is null exactly when the context's `nodeModulesLayoutDigest` is null.
  - `unitRoot` is a text string, `InternalUnitRootV1` (NES `$defs/InternalUnitRootV1`; `""` for the project root).
- **Why byte strings, not decoded maps.**
  1. **The digests are over these bytes.** `nativeContextId` is `H` over `C(X)`, and `tsconfigGraphHash` and the
     layout digest are raw SHA-256 over `C(X)` (NE:1330, NE:1490, NE:1576-1578). Carrying `C(X)` makes each check
     one hash, with no re-canonicalization ambiguity. The worker still parses each string and requires that it
     re-encodes to the identical bytes (LD-N5).
  2. **TS2's CBOR depth bound is 7** (product `provider_protocol/ts2.rs`:67, `TS2_FRAME_MAX_DEPTH`). A decoded
     context nests `payload → carrier → context → configProjection → honoredOptions → paths → row → substitutions`,
     depth 8. As byte strings the carrier is depth 2.
  3. **It is what the host retains.** `bind_typescript_universe` takes "the retained context bytes" as a required
     argument (NE:1583-1592), and the admitted layout is held as "its canonical bytes and their raw SHA-256" (product
     `node_modules_layout.rs`:125).
- **Why the context is carried, although its non-selection members are re-derived.**
  1. **It binds the layout.** The layout bytes join to the Plan through the context's `nodeModulesLayoutDigest`.
     Without the context preimage, the worker could bind the layout only through its own recomputation, and an
     incoherent carrier would then look like a derivation disagreement instead of a host fault.
  2. **It attributes a mismatch.** The worker can name the differing member in its bounded stderr diagnostic, which
     F1's controls assert (§10, NC-5). That attribution is operational evidence, never a wire member.
  3. **It is small.** 1,879 B in the product fixture (`evidence/vectors.json` `sizes`), at most 4 MiB.
- **Why the unit root is carried as a value, not inside a digest-bound record.** No record the worker holds a
  digest of names it. The unit's `WorkspaceUnitV2` is Plan-bound only through `UnitMembershipV1.membershipDigest`,
  whose preimage has one row per snapshot path (NE:745-786). Carrying it would add up to 200,000 rows to bind a single
  string. LD-N4 shows why an unbound unit root is safe.
- **What is not carried, and why.**
  - **No closure, compiler, standard-library or toolchain record.** The context's `toolchain` and `toolClosure`
    members must come from the worker's own installed signed closures (NE:1481-1487, TSR1:861-880). A carried copy
    would let a worker running other bytes than the Plan's compute the Plan's context, defeating
    `typescript-context-identity-is-platform-specific-through-its-signed-tool-closure` (NE:1567-1574).
  - **No `UnitMembershipV1`, scope descriptor or boundary inventory.** See LD-N4 and LD-N7.

### LD-N4. The selection, and the rule that makes an unbound selection safe

- **Decision.** The worker takes exactly these values from the carrier:
  1. `configGraph.entryConfigPath`;
  2. for every layout row, `installPath`, `realPath`, `packageName` and `packageVersion`, and the layout's
     presence;
  3. the `contentSha256` of a layout row whose manifest is not a sealed VFS file;
  4. `unitRoot`.

  It copies no other member of the context, graph or layout into its recomputation. It never infers a selection
  from a digest, and never enumerates configuration or unit candidates to match one.
- **The rule.** A selection value is admissible only if it is digest-bound to a Plan-bound id the worker holds, or
  if every value the worker derives from it is a member it compares byte for byte with a Plan-bound value before
  Analyze, and it has no other use.
  - Values 1 to 3 are digest-bound: value 1 through `tsconfigGraphHash`, values 2 and 3 through the context's
    `nodeModulesLayoutDigest` and `nativeContextId`.
  - Value 4 meets the second branch. `unitRoot` is used only as the start directory of TSR-1 R-6.1 and R-6.2
    (TSR1:894-919), whose outputs `packageModuleType` and `lockfileIdentity` are context members. Under
    `js-synthesized` R-6.1's first directory is the unit's own marker, so the same holds. A wrong `unitRoot`
    produces one of three things: a closed-key refusal met on its walk (for example a malformed `package.json`,
    `native.typescript-profile-package-json-malformed`), which is the input-mismatch payload with no context id; a
    completed context that differs, which is `native-context-mismatch`; or the identical context, in which case
    nothing the worker computes has changed. `unitRoot` is bound by no digest; this restricted use is what makes it
    admissible.
  - `languageMode` does not use `unitRoot`. It is a function of the entry (null gives `js-synthesized`) and its
    effective `allowJs` (NE:173-175; MB:658-664).
- **Prohibited uses of `unitRoot`.** It is never a compiler-host input (current directory, type roots, `rootNames`),
  a Program input, a subject filter or a membership test. The Program's current directory is the project root. This
  closes the only route by which an unbound value could change analysis without changing the context.
- **Why layout names and versions are selection.** They are C2b-0's parse of each manifest
  (`node_modules_layout.rs`:1178-1318), and the worker's resolver reads each manifest's own bytes from the VFS, never
  these two fields. Re-deriving them would make the worker carry a second implementation of C2b-0's manifest grammar
  with no analysis consequence. Their bytes are still committed: they are inside `C(L')`, whose digest enters the
  recomputed context.
- **Rejected:**
  - **Option B, discovery in the worker.** It duplicates B2's instruments in TypeScript. A snapshot with several
    units names no unit, and it is still an inference (ESC Q1 B).
  - **Deriving the unit root from the entry's directory.** It is wrong for an explicit entry and undefined under
    `js-synthesized` (§1, item 3).

### LD-N5. The digest joins, before `UniverseAccepted`

- **Decision.** The worker checks:
  1. `"sha256:" + hex(H("native.context.typescript.v2", context))` equals `universe.resolvedInputs.nativeContextId`;
  2. `hex(SHA-256(configGraph))` equals `universe.resolvedInputs.tsconfigGraphHash`;
  3. the layout's presence equals the context's `nodeModulesLayoutDigest` being non-null, and its raw SHA-256 equals
     that digest;
  4. `universe.resolvedInputs.nodeModulesInReadSet` equals the layout's presence.

  Each byte string must parse as its closed record and re-encode under `C` to the identical bytes. The context and
  the universe must agree where NE §2.4 makes them overlap (NE:1593-1598). `unitRoot` must match its grammar.
- **Failure.** It is a malformed or uncorrelated `OpenUniverse`. The worker sends no `UniverseAccepted` and exits
  nonzero (F1P LD-F1-5; F1R item 10). The host sees a process fault before any source byte. The host runs the same
  checks before spawn and refuses there as a host invariant (SEND's builder rows, `PlanRefusal::HostInvariant`), so
  a conforming host never reaches the worker-side failure.
- **Why canonical re-encoding.** `H` is defined over `C(X)` (IE:117-120, IE:170). Bytes that hash correctly but are not `C`
  of what they decode to are a forgery of the recipe. Vector `context-not-canonical-though-hashed` is refused.
- **Why a fault, not `Unavailable`.** An incoherent carrier is the host's own payload contradicting its own Plan.
  No recomputation has run, so `native-context-mismatch` would be a false statement (NE:3216-3219).

### LD-N6. Recomputation, its order and its outcomes

- **Decision.** After `SnapshotAccepted` the worker derives two things, in this order:
  1. **`G'`**, by MB item 14a's one function, from `entryConfigPath` over the sealed VFS (MB:605-700). With a null
     entry, `G'` is `{schemaVersion 1, entryConfigPath null, nodes []}`.
  2. **`X'`**, by NE §2.4 and TSR-1, from `G'`, the VFS, the selection and its own closures. The layout member is
     `null` when `nodeModulesLayout` is null, and otherwise `SHA-256(C(L'))`, where `L'` is the carried layout with
     each row's `contentSha256` re-derived from the VFS wherever its manifest is a sealed VFS file.

  It then decides, first match wins:

  | Case | Terminal |
  |---|---|
  | step 1 refuses | `TypeScriptPreAnalyzeInputMismatchV1` (config-graph, refused) |
  | step 2 refuses | `TypeScriptPreAnalyzeInputMismatchV1` (native-context, refused) |
  | `H(X') ≠ nativeContextId` | `PreAnalyzeUnavailableV1` (`native-context-mismatch`), unchanged |
  | `C(G') ≠ configGraph` | `TypeScriptPreAnalyzeInputMismatchV1` (config-graph, differs) |
  | otherwise | `NativeContextVerified` |

  `evidence/vectors.json` `decisionOrder` gives all eight reachable combinations.
- **Why the graph is re-derived, not taken.** MB14a is a host derivation, and only its entry is a selection
  (LD-Q-37). Taking the carried edges would let a host `extends`-resolution defect pass into the worker's options.
- **Why the context comparison comes first.** It is the published §9.5 law, with its existing lawful terminal.
  A graph difference usually changes the context, and then the context mismatch is the honest, more specific
  statement.
- **Why a new payload for a graph-only difference.** Equal ids in `PreAnalyzeUnavailableV1` are a protocol
  violation (NE:3225-3226), so a graph difference under an equal context has no lawful terminal today. RF-2 forbids
  manufacturing a context mismatch for it. Proceeding silently would admit a universe whose `tsconfigGraphHash`
  misdescribes the snapshot it travels with.
- **Why a refusal is a terminal, not a sentinel digest.** F1R item 1: "inability to construct a context is not
  automatically a differing *recomputed* context". A refusal carries its key, never an invented digest.
- **The closed refusal-key set.** MB14a's four keys (MB:666-673) for step 1, and TSR-1 §7's phase 2, 3,
  4-`references` and 5 keys for step 2 (TSR1:925-960). TSR-1 phase 1 keys and NE §2.4's closure keys concern the
  worker's own installation, so they are process faults, as are resource exhaustion and crashes. The worker skips
  TSR-1 phase 4's literal-root and root-count checks, because it does not re-derive roots (LD-N7).
- **`NativeContextVerified`.** Under the token, `equal: true` also asserts that `G'` equals the carried graph and that
  neither step refused. The payload is unchanged.
- **Rejected:**
  - **A process fault for a refusal.** It reports a disagreement between two implementations of one law as a
    provider crash (operational-failed 4), while the context case is the clean indeterminate (3). Same class of
    disagreement, same outcome class.
  - **Widening `PreAnalyzeUnavailableV1`'s `reason` enum.** It would change a closed published payload's
    admission in place, and its correlation (recomputed id differs) does not fit a refusal.

### LD-N7. Program roots stay Plan authority

- **Decision.** `programRootFiles` and `jsRootFiles` are universe members, and the worker takes them as given. It
  builds its Program from them. The roots also feed the `js-synthesized` `jsx` rule (NE:1422-1428). A root list that
  changes while the context stays equal yields `NativeContextVerified`.
- **Why the roots are not re-derived.**
  - TSR-1 R-4.2's candidates exclude `outside-project-boundary` rows (TSR1:729-735).
  - The boundary inventory is "a security-owned input the Plan does not retain" (NE:813-815; U-8, NE:816-878).
  - So a worker deriving roots from the snapshot alone would put files of a nested repository or project into its
    roots. That would be a different derivation, not an independent one.
  - Carrying the boundary prefixes would add another unbound selection whose derived values (the roots) are
    universe members with no worker-side comparison of their own. They would fail LD-N4's rule.
- **What answers RF-2.** F1's C-10 tests a root-list change under an equal context and expects
  `NativeContextVerified`. It tests a configuration-graph change under an equal context and expects the
  input-mismatch payload. Context-mismatch cases change real context members (§10).
- **Disclosed limit.** A host TSR-1 §4 defect that yields wrong roots under a correct context is not caught by
  this exchange. It is caught by C2b-1b's TSR1-C16 to C20 and C27, the host's own controls. This is the same
  boundary as subjects, which are Plan authority on `Analyze`.

### LD-N8. Host duties

- **What and from where.** The host builds `nativeContextInputs` from records the Plan already bound:
  - `context`: the retained context bytes given to `bind_typescript_universe` (NE:1583-1592);
  - `configGraph`: the retained graph, a required binding input (NE:1338-1343);
  - `nodeModulesLayout`: the retained layout, required whenever non-null (NE:1413-1416);
  - `unitRoot`: the `rootPath` of the universe's unit in the retained `UnitMembershipV1`, which `PlanId` binds
    through `membershipDigest` (NE:745-746).
- **How.** It sends the retained bytes exactly, never a re-encoding of a decoded copy. `Ts2Plan` (SEND:78-105) gains
  one member holding the four values.
- **When.** At Plan time, inside the send-schedule constructor. C4 calls the constructor (SEND:10-14), and it
  measures the exact `OpenUniverse` payload (REQUEST-WIRE-ACCOUNTING). Before spawn, the builder checks LD-N5's
  joins and grammar and refuses a failure as `PlanRefusal::HostInvariant`.
- **The host's admission of the worker's frames.**
  - It decodes the new pre-Analyze payload only under the token, and only in `WAIT_NATIVE_CONTEXT_VERIFIED`.
  - It checks the payload's correlation (§2 of the schema law).
  - It converts the payload exactly as `PreAnalyzeUnavailableV1`: `stage_authority("unavailable")`, one host-minted
    `CoverageResultV3` per requested key, `provider-unavailable` with a null cause (NE:3227-3266).
- **Plan time.** C4 treats the token as needed for every TypeScript worker (LD-N2).

### LD-N9. Bounds

- **Each preimage is at most 4 MiB.** Every carried string is a `C` encoding the host minted under the foundation
  4 MiB descriptor bound: IE:117-120, product `crates/identity/src/canonical.rs`:5 (`MAX_BYTES` 4,194,304) and
  :117. The layout refuses above it explicitly (`node_modules_layout.rs`:86).
- **The carrier adds at most 12,599,382 bytes** of deterministic CBOR to `OpenUniverse`. That is three maximal
  strings with their 5-byte heads, a maximal 4,096-character `unitRoot` of 16,384 UTF-8 bytes, and the member keys:
  a 12,599,362-byte map plus a 20-byte key. It is computed in `evidence/build_nss_f1.py` (`sizes`). The product
  fixture's carrier is 2,946 bytes.
- **The frame bound is unchanged.** `maxFramePayloadBytes` stays 67,108,864 (NE:2962). The host's exact
  send-schedule measurement stays the only frame-size authority. If a universe and the carrier together exceed it,
  the existing typed `ExceedsWireLimit` refusal before spawn applies. NSS-F1 adds no limit member and no new refusal
  route.
- **Headroom.** The carrier leaves 54,509,482 bytes of the frame for the rest of `OpenUniverse`. The universe's
  `resolvedInputs` is itself a `C` descriptor of at most 4 MiB. Its CBOR is at most nine times its `C` length, since
  each CBOR item head is at most 9 bytes and each `C` item at least 1. That gives 36 MiB, which fits.

### LD-N10. Pricing (LD-Q-38) and the worker's pre-Analyze bounds

- **The worker.** Under LD-Q-38 (CM), worker-side code is outside OD-PROC-1 §3.3(a). Its pre-Analyze verification
  is bounded by the sealed inputs' caps and by D3 supervision. NSS-F1 makes those bounds explicit, so F1 can cite
  them:

  | Work | Bound |
  |---|---|
  | carrier parse, re-encode, three hashes | three strings of ≤ 4 MiB, nesting ≤ 32 (IE:117) |
  | `G'` (MB14a) | ≤ 32 nodes of ≤ 64 KiB, ≤ 64 `extends` entries per node, paths ≤ 4,096 characters; package candidates ≤ 3 per ancestor directory (MB:611-656) |
  | `X'` (TSR-1 §1–3, §5, §6) | over `G'`'s ≤ 32 nodes; TSR-1's per-write and per-collection bounds (TSR1 R-1.9); R-6 walks ≤ (segments of `unitRoot` + 1) directories × 6 lookups; `package.json` ≤ 1 MiB |
  | `L'` | ≤ 100,000 rows (NES `ResolvedNodeModulesLayoutV1.entries.maxItems`) × one VFS lookup, digests already in the manifest |
  | own closures | the worker's installed trees; ≤ 256 stdlib rows (NES `standardLibraryComponentDigests.maxItems`) |
  | `H(X')`, `C(G')` | ≤ 4 MiB each |

  No compiler Program is built before Analyze. From Analyze on, DLV's `ProviderWorkBudgetV1` governs, unchanged.
- **The host.** The additions are a copy of at most about 12 MiB of retained bytes, three hashes, and a grammar
  check, inside D2b's send builder.
  - That builder is not M1a-metered today. NSS-F1 does not change that standing.
  - The records' own admission and hashing are already C2b's charged work.
  - **The operations LD-N5 and LD-N8 impose on the host**, each to be priced by whichever unit prices them (r2,
    NB-2): for each of the three byte strings, parsing it (≤ 4 MiB, nesting ≤ 32), validating it against its
    closed NES record, re-encoding it under `C` and comparing the bytes, with the allocations of each; one `H` and two
    raw SHA-256 over ≤ 4 MiB each; the presence and digest checks of the layout; the §2.4 overlap comparisons
    between the decoded context and the universe; the `unitRoot` grammar; and the copy of ≤ 12,599,382 bytes into
    the payload. LD-Q-38 exempts worker code only; these are host operations.
  - **Recommendation (X-NSS-PRICE).** Either price them inline at their sites, or have C4's metered Plan admission
    perform them once and hand the builder a typed prior-admission result (the four values with a proof type that
    only that admission constructs), so the send-time work is a copy. The present D2b builder's unmetered standing
    is not a basis for leaving these operations unpriced.

### LD-N11. The form of the successor, and the retained-identity check (LD-Q-10)

- **Decision.** The form is FA-2's (FA2 LD-F8):
  - **NE:** nine insert-only line overrides. Line 3007 appends §9.5a (`section-9-5a.md`).
  - **ST and PST:** four JSON Pointer string overrides each, with the same text in both.
  - **T2O:** one JSON Pointer string override.
  - **HS and PHS:** complete successor copies, because a token enum append cannot be a pointer override.
  - **A new schema document**, with a byte-identical product copy.
  - The token is appended **last**, so no enum member moves.
- **No selector collides.** `evidence/build_overrides.py` reads the product lock's 191 contract successors and
  refuses any selector they already bind. The NE lines FA-2, RUST3-LIM and RCA-r2 bind (93, 138, 1913, 1927, 2790,
  2791, 2814, 2826, 2883, 2884, 2942, 2990, 3028, 3070, 3182, 3235, 3279, 3292, 3313, 4195) are all avoided.
- **The retained-identity check (LD-Q-10's lesson).** For each document whose digest this change could move, every
  pin was enumerated by tool (`git grep` of the digest over both trees at the pins) and classified:

  | Document | Moves? | Pins (product) | Class | Retained identity? |
  |---|---|---|---|---|
  | NES `2d37b810…` | **no**: not edited; the new records live in a new document | — | — | Its digest is a registered `payloadSchemaDigest`. That is why it is untouched, as NE:124 and FA2 LD-F8 do. |
  | NE `83b99783…` | **no**: overrides live in the successor record; the parent bytes are frozen | many source pins | — | no change |
  | ST/PST `e8b2aae5…`, T2O `007ef7af…` | **no**: pointer overrides, parent bytes frozen | `schemas/registry.json`, `admission-registry.json`, `admission-source-map.json`, `source-map.json`, `tools/contracts/generator-closure.json`; T2O: `design-lock.json`, `schemas/wire/native-carriers-v1.json` | live pins | none |
  | HS/PHS `1fc57cbc…` → `260fb535…` | **yes** (the token) | `schemas/registry.json`, `admission-registry.json`, `admission-source-map.json`, `source-map.json`, `tools/contracts/generator-closure.json` (live pins, which move at binding); `crates/components/tests/data/native-rust3-profile-cases.v1.json` (a test fixture, which moves with them) | live pins and a fixture | **none** |

  - **The handshake digest.** No `importId`, `payloadSchemaDigest`, closure `schemaDigests` or other retained record
    carries it: the product grep finds only the six files above, at `c1e9df9` and again at `d643410`. Architecture hits
    are historical review and evidence copies (for example under `config-discovery-b/b-s10`, `s10-tsc` and
    `native-publication`, and many more review records), which stay and are not live pins. So the move re-identifies no
    retained record, unlike TSR-1 Part S's native schema (LD-Q-10).
  - **Identities.** No `H` domain, record, field, vector, universe identity or `PlanId` changes (§5).

## 4. Candidates evaluated

| # | Candidate | Verdict | Why |
|---|---|---|---|
| A1 | **A negotiated member on `OpenUniverse`** | **Chosen** | LD-N1 |
| A2 | A new host→worker frame before the snapshot | Rejected | a frame name, phase and T2O rows; a pinned table changes; no gain (LD-N1) |
| A3 | Decoded preimage maps instead of `C` bytes | Rejected | depth 8 > TS2's 7; re-canonicalization ambiguity (LD-N3) |
| A4 | Also carry the closures | Rejected | it defeats the platform-specific identity check (LD-N3) |
| A5 | Carry `UnitMembershipV1` to bind the unit root | Rejected | up to 200,000 rows for one string; the unit root is safe under LD-N4's rule |
| A6 | Re-derive the roots, with carried boundary prefixes | Rejected | another unbound selection, which fails LD-N4's rule (LD-N7) |
| A7 | A process fault for a recomputation refusal | Rejected | a false crash classification (LD-N6) |
| A8 | Proceed on a graph-only disagreement | Rejected | it admits a universe whose graph misdescribes its snapshot (LD-N6) |
| B | Worker-side discovery | Rejected | inference; duplicated instruments (ESC; LD-N4) |
| C | Trust the host's context by digest | Rejected | it gives up §9.5's independent check (LD-Q-37) |

## 5. Absent token and old peers: everything behaves as today

| Host | Worker | What happens |
|---|---|---|
| NSS-F1 host | release without the token | Plan time: a needed token is missing, so the worker is never spawned (`capability-missing`; NE:2848-2853). No byte is written. |
| pre-NSS-F1 host | release with the token | The old host's closed `TypeScriptCapabilityToken` cannot name the token, so the Hello it would build fails its own closed check before spawn (SEND's builder: `law.check("Hello", …)`). No byte is written. |
| NSS-F1 host | release with the token | V3 and the §9.5a exchange |
| any | `rust-semantic` | unchanged: the token is TypeScript-only |

Without the token:
- every existing TS2 frame, payload, JSON vector and D2b test vector (`TypeScriptOpenUniverseV2`,
  `NativeContextVerifiedV1`, `PreAnalyzeUnavailableV1`) admits and refuses exactly as today;
- no identity changes: no `H` domain, record, member or recipe is added or changed. `nativeContextId`,
  `tsconfigGraphHash`, the layout digest and the universe identity keep their recipes and inputs, so no
  `fact2`/`scope2`/`coverage2`/`view2`/`seal3`/RunId moves;
- **`PlanId` is unchanged.** The token list is release data on the signed capability row, not a Plan member. The Plan
  binds the context digest set, the universe, the membership digest and the closures, none of which change. A new
  release with the token has its own release identity, as any release does.

The only behavioral change without the token is LD-N2's spawn rule. It is NE §9.1 step 1's existing rule, applied to
one more needed token.

## 6. What changes (exact texts in `overrides.json`, `section-9-5a.md` and the two new files)

### NE overrides (insert-only; the `before` is the parent line)

| NE line | Where | Inserted |
|---|---|---|
| 125 | §0, DLV `OpenUniverseV1` row | under the token, the payload is `TypeScriptOpenUniverseV3` (§9.5a) |
| 127 | §0, DLV `unavailableTerminal` row | under the token, `Unavailable` is also lawful in that interval with `TypeScriptPreAnalyzeInputMismatchV1`, converted identically |
| 1620 | §2.4 independent derivation | the selection reaches the worker on §9.5a's carrier: entry and layout digest-bound; `unitRoot` bound by no digest and admissible only for R-6's walks (r2, RF-2); only the selection is taken |
| 2853 | §9.1 step 1 | the token is a token the Plan needs for every TS worker |
| 2862 | §9.1 step 3 | the TS OpenUniverse also carries the carrier; the joins are checked before `UniverseAccepted` |
| 2953 | §9.4 | the recomputation's inputs arrive on `OpenUniverse`; the input-mismatch payload's two cases, (a) a graph disagreement under a completed, equal context and (b) a closed-key refusal with no context and no equality asserted (r2, RF-1) |
| 3007 | end of §9.5 | appends **§9.5a** |
| 3192 | §9.7 "Native context" | the preimage bytes travel in `nativeContextInputs.context`, never a second identity |
| 3215 | §9.7 pre-Analyze `Reason` | the token-gated second payload is admitted in that phase; it is not another reason of V1 |

### ST and PST overrides (the same four strings in both)

- `/x-opensip-startup-law/typescriptOpenUniverse/payload`: names `TypeScriptOpenUniverseV3` under the token.
- `/x-opensip-startup-law/typescriptOpenUniverse/nativeContext`: the preimage bytes are digest-bound, never a
  second identity.
- `/x-opensip-startup-law/nativeContextVerified`: `equal: true` also asserts the graph equality and no refusal.
- `/x-opensip-startup-law/preAnalyzeUnavailable/reason`: the second payload; host conversion identical.

### The T2O override

`/eventObservations/unavailablePayload`: `TypeScriptPreAnalyzeInputMismatchV1` is also pre-analyze under the token.
No T2O row, phase or guard changes, and T2O's bytes stay as pinned.

### The handshake successor copies

These are the parent's bytes with exactly these edits, checked structurally by `build_overrides.py`:
- `native-context-inputs-v1` appended last to `TypeScriptCapabilityToken.enum`; `RustCapabilityToken` unchanged;
- `TypeScriptCapabilitiesV2.maxItems` 12 → 13;
- the token's description gains one sentence: a member, although the registered `CapabilityToken` omits it;
- `x-opensip-wire-law.supersedes[3]` names the added TypeScript token;
- `x-opensip-wire-law.nativeContextInputs`, added before `commitments`, with `negotiated`, `notNegotiated`,
  `violation`, `planNeed` and `majors`;
- the document `description` names §9.5a.

### The new schema document

`native-context-inputs.schemas.v1.json` (`$id` `opensip.product.native-context-inputs.1`) publishes closed
JSON-vector records, with the handshake schema's `<m>Hex` byte-string convention: `NativeContextInputsV1`,
`TypeScriptOpenUniverseV3`, `TypeScriptPreAnalyzeInputMismatchV1` and its two `recomputation` variants. Its
`x-opensip-native-context-inputs-law` restates §9.5a's negotiation, Plan need, carrier, joins, selection,
recomputation, layout rule, correlation, host conversion, the closed refusal-key set, and the bounds. None of the
keys is a `DomainDetailCode`.

## 7. Worker duties, field by field

| Context member | Worker source | Selection? |
|---|---|---|
| `schemaVersion` | constant 2 | — |
| `languageMode` | `G'`'s entry (null gives `js-synthesized`) and effective `allowJs` (NE:173-175; MB:658-664) | no |
| `toolchain.compilerName` | constant `typescript` | — |
| `toolchain.compilerVersion` | own admitted compiler closure manifest `semanticVersion` (NE:1481) | no |
| `toolchain.compilerPackageDigest` | own toolchain tree `package.json` (TSR1 R-5.1) | no |
| `toolchain.typescriptStdlibMerkleRoot` | 64-hex suffix of own stdlib closure's recomputed `closure2` id (NE:1483) | no |
| `toolchain.standardLibraryComponentDigests` | own stdlib tree's complete `.d.ts` inventory (NE:1484) | no |
| `toolchain.libSelection` | `X'.honoredOptions.lib` under NE §2.4's fold and TSR-1 §2 | no |
| `toolClosure.compiler`, `.runtime`, `.closureId` | own toolchain tree `lib/typescript.js`, `bin/node`, own closure id (TSR1 R-5.1) | no |
| `configProjection.honoredOptions`, `.strippedOptions` | TSR-1 §1–3 over `G'`'s node bytes; `SynthesizedCompilerOptionsV1` under `js-synthesized`, with `jsx` from the universe's roots | no |
| `configProjection.configGraphPaths` | `G'`'s node paths | no |
| `typeAcquisitionEnabled`, `executableSelected` | constants `false` | — |
| `moduleResolutionMode` | `X'.honoredOptions.moduleResolution` | no |
| `packageModuleType` | TSR-1 R-6.1 from `unitRoot` over the VFS | `unitRoot` only |
| `nodeModulesLayoutDigest` | null, or `SHA-256(C(L'))` (LD-N6) | row paths, names, versions, presence; unjoinable digests |
| `lockfileIdentity` | TSR-1 R-6.2 from `unitRoot` over the VFS | `unitRoot` only |

`G'` is MB14a from the carried `entryConfigPath` only. The worker's TSR-1 tables are the same source-pinned host data
(TSR1 P-0.3), which F1R item 11 accepts.

## 8. Relation to the governing laws

- **NE §9.5 and §2.4 (NE:1618-1620, NE:3003-3007).** The law is unchanged and now executable. "Its own sealed
  inputs" means the sealed VFS, the worker's own signed closures, and the Plan-bound selection, which is
  digest-bound or self-certifying under LD-N4. The host still computes the context before PlanId from admitted bytes
  and never from a worker claim (NE:1476-1478): the carrier flows host to worker only.
- **NE:3205-3226 (pre-Analyze `Unavailable`).** `PreAnalyzeUnavailableV1` is unchanged in members, reason,
  correlation, phase, equal-id violation and host conversion. NSS-F1 adds a separate token-gated payload for the two
  cases V1 cannot lawfully express, a graph-only difference and a refusal. It reuses V1's phase (T2-10), after-rules
  and conversion.
- **TSR-1 §6 (TSR1:892-924).** R-6.1 and R-6.2 start from the unit's root. NSS-F1 supplies that root to the worker.
  TSR-1's P-0.5 ("the worker's independent recomputation … applies TSR-1 too, so a host that departs from it is
  caught", TSR1:141-145) becomes realizable.
- **TSR-1 §8 (TSR1:961-977).** NSS-F1 adds no custody input to C2b-1a's typed inputs. The host-side outputs are
  unchanged. NSS-F1 transports already-retained host records to the worker. Part S's deferral (LD-Q-17) is
  untouched: no `""` path is admitted here beyond `unitRoot`'s existing `InternalUnitRootV1` grammar.
- **CP-WORKER-1 (TSR1-C31).** C31 needs a Program built with the project's honored and stripped options. Under
  NSS-F1 the worker builds it from its own verified context `X'`, so C31 can be accepted against production host
  frames. Two notes for F1:
  - F1R item 8's self-export case needs a layout-present configuration. With the layout absent, NE:1416-1419 makes
    every bare specifier unresolved, a self-reference included, and NSS-F1 does not change that.
  - With the layout present, the rows bound the installed-dependency directories the resolver may read. They do
    not confine first-party package-scope or self-export lookup inside the VFS.
- **F1R mapping.**
  - RF-1: the carrier, the input inventory (§7), the no-inference rule, and the sentinel prohibition (LD-N6).
  - RF-2: LD-N6 and LD-N7, and NC-7 to NC-10.
  - RF-6: LD-Q-38 and LD-N10.
  - RF-7 and RF-8: F1's adapter and resolver, constrained by LD-N4's prohibited uses and the C31 notes above.

## 9. Cascade and cross-law items

| ID | For | Item |
|---|---|---|
| **X-NSS-B** | binding (the coordinator assigns, recommended in F1's first host sub-unit) | Materialize `successor.json` in FA-2's form from `overrides.json`, the two copies, the new schema and its product copy, under `docs/implementation/m3/native-successors-fa/nss-f1/`. Add the new schema's source-map, registry and admission rows. Re-pin the five handshake live pins and the rust3 profile fixture. Run `verify_design` on a scratch lock, then bind. Byte fidelity to this document is the only review question. |
| **X-NSS-D** | the host codec (D2b's successor work; the coordinator assigns, recommended F1) | `Ts2Plan` gains the carrier. The builder adds `TypeScriptOpenUniverseV3` under the token with LD-N5's checks. The carriers file (`schemas/wire/native-carriers-v1.json`) gains the records. The admission adds the new pre-Analyze payload, its correlation and its conversion. The old no-token refusals keep their controls. |
| **X-NSS-C4** | C4 (Plan composition) | The token is needed for every TypeScript worker. C4 supplies the four values from the retained records (LD-N8). |
| **X-NSS-C2B** | C2b-1a/1b | They expose the retained context bytes, the graph, the layout bytes and the unit root to C4 unchanged. No new derivation. |
| **X-NSS-F1** | F1 (implements at R2) | The worker duties (§7, LD-N4 to LD-N7), and the controls and mutations (§10). F1-b and F1-c's context half are frozen only after adoption (premise rule). |
| **X-NSS-F4** | F4 (release and closures) | Signed TypeScript capability rows carry the token. The installed worker holds its own compiler and stdlib closure descriptors and trees, from which LD-N6 recomputes. |
| **X-NSS-PRICE** | the coordinator | LD-N10's enumerated host operations (r2), and the choice between inline pricing at their sites and one metered C4 admission handing the builder a typed prior-admission result. |
| **X-NSS-M** | the design-evidence models (`provider_startup_model.v1.py`, `native_evidence_model.v2.py`) | Not updated, as FA2-N1-01 decided for FA-2: they are historical design evidence, and this unit's evidence is its own scripts and vectors. The implementing owners carry successor-aware loading. |

## 10. Controls and mutations F1 must carry

The positive cases use **production host frames**: `OpenUniverseV3` bytes built by the product builder (X-NSS-D)
from retained records, retained as a vector file, and consumed by the worker with its own test closure. No
in-process fixture supplies extra context. They cover `ts-tsconfig`, `js-allowjs` (a jsconfig entry) and
`js-synthesized`, and a null and a non-null layout. MAP's fixtures `ts-small-constructs` and
`js-small-body-parser` are the recommended real pair.

| ID | Case | Expected |
|---|---|---|
| NC-1 | positive, each mode and both layout branches | `NativeContextVerified`, recomputed id equal |
| NC-2 | carrier bytes whose digests miss: context; graph; layout; layout present under a null digest and absent under a non-null one; `nodeModulesInReadSet` disagreeing | no `UniverseAccepted`, nonzero exit; host builder `HostInvariant` before spawn |
| NC-3 | context bytes that hash correctly but are not `C` (whitespace, key order, duplicate key) | as NC-2 |
| NC-4 | a self-consistent wrong host context (one honored option changed, re-hashed, universe id updated) | `PreAnalyzeUnavailableV1`, recomputed ≠ carried |
| NC-5 | one change per context member class, each a real member: `allowJs` through `languageMode`; an honored option; a stripped option; `lib` through `libSelection`; `package.json` `type` through `packageModuleType`; lockfile kind or presence through `lockfileIdentity`; a joinable layout row's manifest bytes through the layout digest (non-null layout only); a swapped worker closure through `toolchain` | `PreAnalyzeUnavailableV1`; the diagnostic names the member |
| NC-6 | `unitRoot` wrong: (a) its derived values differ; (b) an explicit entry in a subdirectory whose own `package.json` `type` differs from the unit root's | (a) `PreAnalyzeUnavailableV1`; (b) `NativeContextVerified`, because the walk starts at `unitRoot`, not the entry's directory |
| NC-7 | `extends` order or target changed in the carried graph so that the context stays equal | `TypeScriptPreAnalyzeInputMismatchV1` (config-graph, differs) |
| NC-8 | a VFS node that TSR-1 phase 2/3/5 refuses (hand-built host frames); and a wrong `unitRoot` whose walk meets a malformed `package.json` | input mismatch (native-context, refused, the key); no context is completed and no context digest exists |
| NC-9 | an `extends` target absent from the VFS | input mismatch (config-graph, refused, `native.typescript-config-extends-unresolved`); `X'` is never derived and no context digest exists |
| NC-10 | `programRootFiles` changed, the universe re-hashed, the context equal | `NativeContextVerified` |
| NC-11 | the carried entry is an explicit `other` config, while `tsconfig.json` exists at `unitRoot` | the worker uses the carried entry; NC-7's companion case must still give its exact payload |
| NC-12 | token negotiation: V3 without the token; V2 with it; the input-mismatch payload without it | `PROVIDER.PROTOCOL_VIOLATION` (host), and the worker-side refusal |
| NC-13 | old vectors without the token | byte-identical admission as before |
| NC-14 | precedence: graph and context both differ | `PreAnalyzeUnavailableV1`, not the input mismatch |
| NC-15 | host admission of the new payload: wrong phase; equal digests; native-context with `differs`; an unlisted key; a key of the other input's set; an uncorrelated id | `PROVIDER.PROTOCOL_VIOLATION`; a valid payload converts identically to V1 |
| NC-16 | a layout row whose manifest is a VFS file with other bytes; a row whose manifest is absent (an excluded package) | the first gives `PreAnalyzeUnavailableV1`; the second keeps the carried digest and verifies |
| NC-17 | maximal carrier (three 4 MiB strings) | fits; the host schedule measures it exactly |

| Mutation | Killed by |
|---|---|
| M-1 copy the carried context's `configProjection.honoredOptions` into `X'` instead of deriving it | NC-4. Other member classes are covered by NC-5 against §7's field inventory, and constants and forbidden flows by source review; NC-4 is not proof that every member class is derived |
| M-2 take the carried graph's edges instead of re-deriving `G'` | NC-7 |
| M-3 report a context mismatch for a graph-only difference | NC-7; host equal-id rule (NC-15) |
| M-4 keep a layout row's carried digest when its manifest is in the VFS | NC-16 |
| M-5 put the input mismatch before the context comparison | NC-14 |
| M-6 skip a carrier digest join | NC-2 |
| M-7 accept non-canonical bytes | NC-3 |
| M-8 start the R-6 walks from the entry's directory | NC-6(b) |
| M-9 search configuration candidates for one matching `tsconfigGraphHash` | NC-11 with NC-7, and a source census: no VFS enumeration of configuration candidates |
| M-10 emit a sentinel digest instead of a refusal | NC-8, NC-9 |
| M-11 drop the token gate (always V3) | NC-12, NC-13 |
| M-12 use `unitRoot` as the compiler-host current directory or type-root base | a source census: `unitRoot` reaches only the R-6 functions |

## 11. Not claimed

- No product, architecture, inventory, registry, generated-code or review file is touched.
- No protocol major, frame name, phase, T2O row, terminal kind, limit member, identity version, `H` domain, record
  member of a registered schema, relation or public code is added or changed.
- No measurement of a compiler, a resolver or a real repository. The fixture is the product's synthetic
  native-context fixture (TypeScript 5.6.3 data). The bounds are cited caps and arithmetic.
- No decision on TSR-2, Part S, F1's adapter (RF-7), F1's resolver confinement (RF-8), or F2's budgets.
- The design-evidence models are not updated (X-NSS-M).

## 12. Evidence and checks

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3` with `-I -B`. Nothing ran cargo, npm, a product
tool, a provider, a compiler or a frame codec.

- **`evidence/build_nss_f1.py --product … --arch … [--check]`** reads the product fixture
  `crates/host/tests/fixtures/native-context-fixtures.current.json` (`ae72825a…`), whose TypeScript universe
  retains the context frame, the graph and the layout.
  - **The fixture joins.** It checks the three joins on the real retained bytes: the context's `H` equals the
    universe's `nativeContextId`; the graph digest equals `tsconfigGraphHash`; the layout digest equals the
    context's. It checks canonical re-encoding of all three, and recomputes the universe key.
  - **Seven reference carrier-join cases**, one positive and six refusals.
  - **The fixture preimages are valid NES records** (`TypeScriptNativeContextV2`, `TypeScriptConfigGraphV1`,
    `ResolvedNodeModulesLayoutV1`).
  - **Twenty-two standalone schema cases** against the new document, with the product's vendored jsonschema
    4.25.1 (`tools/contracts/python-packages`) and NES registered by `$id`: eleven valid, eleven refused, including
    both wrong input/key pairings.
  - **Five composed `TypeScriptOpenUniverseV3` admission cases** (r2, NB-1): the record and its universe under ST's
    `TypeScriptSemanticUniverseV2`. A complete universe admits; an empty universe, a missing member, an extra member
    and protocol major 1 refuse. The universe's members other than `resolvedInputs` are illustrative values. The
    standalone cases alone are not exchange-admission evidence.
  - **The decision order**, eight rows.
  - **The size bound.**
  - Output: `evidence/vectors.json`, and `--check` reproduces it byte for byte.
- **`evidence/build_overrides.py --arch … --product … [--record-root …] [--check]`** checks every parent at its pinned bytes. Each
  `before` is the parent line or pointer value; each override is insert-only; no selector is already bound by the
  product lock's 191 successors (a record not yet in `--arch` is read from a `--record-root`, at its locked bytes). Each handshake copy is the parent plus exactly the listed edits, both
  structurally and textually, with the Rust enum unchanged. Output: `overrides.json` and the two copies;
  `--check` reproduces them.
- **Not run:** `verify_design` with a scratch lock. That is the binding step (X-NSS-B).

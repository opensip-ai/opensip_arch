"""Apply the exact ADJ-2..5 and planning text corrections to the work copy. Every `old` must occur exactly once;
all edits are checked against the original text before any file is written.

usage: apply_startup_edits.py <work-candidate-root>
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
NE = "docs/v2/contracts/product-v1/native-evidence.md"
P3 = "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
RD = "docs/coop/design-corrections/native/README.md"
CK = "docs/coop/design-corrections/native/check_native_evidence.v2.py"
INV = "docs/v2/architecture/repository-file-inventory.v1.json"
IBP = "docs/v2/architecture/implementation-boundaries-and-build-plan.md"

LAST_S0_ROW = "| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | `#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3` | **Superseded** by the same-named definitions of `native/provider-handshake.schemas.v1.json`. The registered document is not edited: its raw SHA-256 is a registered `payloadSchemaDigest` (§10), so a byte change there would be a schema-document successor with its own re-registration. |"
TS = "$.typescriptSemanticSubstrate.providerProtocol"

S0_ROWS = [
    f"| `docs/coop/artifacts/delivery.v2.json` | `{TS}.wireSchema.payloadSchemas.OpenUniverseV1`, `{TS}.wireSchema.payloadSchemas.UniverseAcceptedV1`, `{TS}.wireSchema.definitions.SnapshotId`, `{TS}.wireSchema.definitions.PlanId`, `{TS}.wireSchema.definitions.TypeScriptSemanticUniverseV1`, `{TS}.wireSchema.definitions.TypeScriptSemanticUniverseKey` | **Superseded** for typescript-semantic major 2 by `TypeScriptOpenUniverseV2` / `TypeScriptUniverseAcceptedV2` / `TypeScriptSemanticUniverseV2` (`native/provider-startup.schemas.v1.json`, §9.7): member names unchanged; `snapshotId` carries `snapshot2`, `planId` carries `plan2`, `universe` is the `typescript-v1` map with `typescript-v2` `resolvedInputs`, and every universe coordinate typed `TypeScriptSemanticUniverseKey` (`universeKey`, `CoverageKeyV1` and `FactCandidateV1` `sourceUniverseId`/`targetUniverseId`) is the native semantic-universe identity. `ExecutionId` and `PlanIntentCommitment` are **retained**. |",
    f"| `docs/coop/artifacts/delivery.v2.json` | `{TS}.wireSchema.payloadSchemas.CoverageV1`, `{TS}.wireSchema.definitions.CoverageResultV1`, `{TS}.wireSchema.payloadSchemas.UnavailableV1`, `{TS}.wireSchema.payloadSchemas.BudgetExhaustedV1`, `{TS}.wireSchema.definitions.StageResultV1.fields.coverageCommitment`, `{TS}.wireSchema.payloadSchemas.CompleteV1.fields.coverageStreamCommitment`, `$.typescriptSemanticSubstrate.supervision.deterministicBudget.coveragePayload`, `$.typescriptSemanticSubstrate.supervision.cleanUnavailable.coveragePayload` | **Superseded** for major 2 (§9.7). The frame name `Coverage` and its `frameSchemas` row are **retained**; the payload is `TypeScriptCoverageV2`, the `CoverageV1` wrapper whose `CoverageResultV3` entries answer the requested keys by position. `TypeScriptUnavailableV2` / `TypeScriptBudgetExhaustedV2` keep their members with `CoverageResultV3` coverage in stage-major/key order. Commitment recipes and domains are unchanged over the `CoverageResultV3` values. |",
    f"| `docs/coop/artifacts/delivery.v2.json` | `{TS}.ordering.unavailableTerminal`, `$.typescriptSemanticSubstrate.supervision.cleanUnavailable.allowedImmediatelyAfter`, `{TS}.wireSchema.payloadSchemas.CancelledV1.fields.observedPhase` | **Extended** by §9.7 and `native/typescript-protocol2-order.v1.json`. `Unavailable` stays lawful immediately after `Analyze` with the post-Analyze payload, and is additionally lawful with `PreAnalyzeUnavailableV1` (`native-context-mismatch` only) after `SnapshotAccepted` and before `NativeContextVerified`, with host-derived coverage. `observedPhase` is `snapshot` for a Cancel received in that inserted interval. No enum member or terminal route is added. |",
    "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.payloadSchemas.OpenUniverseV2`, `$.wireSchema.payloadSchemas.UniverseAcceptedV2`, `$.wireSchema.definitions.SnapshotId`, `$.wireSchema.definitions.PlanId`, `$.wireSchema.definitions.RustUniverseV1`, `$.planAndDomainProjection.sourceUniverseIdAlgorithm`, `$.planAndDomainProjection.allSemanticUniverseIdAlgorithm` | **Superseded** for rust-semantic major 3 by `OpenUniverseV3` / `UniverseAcceptedV3` / `RustSemanticUniverseV2` (§9.7): member names unchanged; `snapshotId`/`planId` carry `snapshot2`/`plan2`; `universe` is the `rust-v1` map with `rust-v2` `resolvedInputs`; `repositoryResolution` is `RepositoryResolutionV3` joined to the universe and the selected preparation; universe ids are the native semantic-universe identity. |",
    "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `$.wireSchema.frameSchemas.Coverage`, `$.wireSchema.payloadSchemas.CoverageV2`, `$.wireSchema.payloadSchemas.UnavailableV2`, `$.wireSchema.payloadSchemas.BudgetExhaustedV2`, `$.commitments.stageCoverage`, `$.commitments.coverageStream`, `$.wireSchema.definitions.StageResultV2` | **Superseded** for major 3 (§9.2, §9.7). The frame is `CoverageV3` (P3-24) with payload `CoverageV3`, the `CoverageV2` wrapper with `CoverageResultV3` entries. `UnavailableV3` (P3-25; reason never `native-context-mismatch`) and `BudgetExhaustedV3` keep their members with `CoverageResultV3` coverage. P3-21 carries `PreAnalyzeUnavailableV1`. Commitment recipes and domains are unchanged over `CoverageResultV3` values. |",
]

SECTION_97 = """### 9.7 Startup frames, pre-Analyze `Unavailable`, Coverage wrappers and cancellation

Field-level records are in `docs/coop/design-corrections/native/provider-startup.schemas.v1.json`
(closed, with its `x-opensip-startup-law`). The `typescript-semantic` major-2 order is the
published abstract table `docs/coop/design-corrections/native/typescript-protocol2-order.v1.json`.
Registered and historical artifacts are unchanged, and §0 names every superseded selector.

**OpenUniverse and UniverseAccepted.** Member names are inherited unchanged.
`executionId` and `planIntentCommitment` keep their owners. `snapshotId` carries the
verified Plan's `snapshot2` text and `planId` its `plan2` text; every later member that is
an exact echo of them carries the same text. A universe coordinate on the wire is the
native semantic-universe identity `sha256:hex(H(native.semantic-universe.<language>.v2,
universe.resolvedInputs))` (§11); `CoverageKeyV2`, subject scopes and `fact2` carry its
64-hex suffix.

- **`typescript-semantic` OpenUniverse.** `TypeScriptOpenUniverseV2` = `{executionId, snapshotId, planId,
  planIntentCommitment, providerId, universe, universeKey}`.
  - `universe` is `TypeScriptSemanticUniverseV2`: the `typescript-v1` map with `protocolMajor` 2 and
    `resolvedInputs` = `TypeScriptUniverseV2ResolvedInputs`.
  - `universeKey` is the universe identity, recomputed by host and worker.
  - The universe's `providerBuildId`, `providerDescriptorSha256`, `runtimeDescriptorSha256`,
    `protocolMajor`, `nodeVersion`, `v8Version`, `modulesAbi`, `typescriptVersion`,
    `typescriptCompilerSha256`, `typescriptStdlibMerkleRoot` and `platformId` equal the admitted
    `TypeScriptHelloAckV2`.
  - There is no `repositoryResolution`, and no dependency-source or prepared frame.
- **`typescript-semantic` UniverseAccepted.** `TypeScriptUniverseAcceptedV2` = `{executionId, snapshotId,
  planId, universeKey}` echoes OpenUniverse; `universeKey` is the worker's own recomputation.
- **`rust-semantic` OpenUniverse.** `OpenUniverseV3` = `{executionId, snapshotId, planId, planIntentCommitment,
  providerId, universe, repositoryResolution}`.
  - `universe` is `RustSemanticUniverseV2`: the `rust-v1` map with `protocolMajor` 3 and
    `resolvedInputs` = `RustUniverseV2ResolvedInputs`. Its `protocolMajor`, `providerBuildId`,
    `rustCommitHash`, `hostTriple`, `targetTriple` and `sysrootDigest` equal `HelloV3.expectedIdentity`.
  - `repositoryResolution` is `RepositoryResolutionV3`. Its `dependencySourceSetId` and
    `preparedOutputSetId` equal `universe.resolvedInputs`.
  - `authorizationId` and `effects` are null when `preparedOutputSetId` is null. Otherwise they are
    the selected preparation's `authorizationId` (null for `imported-descriptor`) and the effects of
    the `AuthorizedExecutionV2` it names.
- **`rust-semantic` UniverseAccepted.** `UniverseAcceptedV3` = `{executionId, snapshotId, planId, providerId,
  universe, repositoryResolution}`, with exact recursive equality to OpenUniverse.
- **Native context.** The native context is the universe's `resolvedInputs.nativeContextId`. Its 64-hex
  suffix must be a member of the verified `plan.nativeContextDigests`; there is no separate
  context member.
- **Derived modes (`rust-semantic`).** `dependencyMode` and `preparedMode` are host-derived
  observations of the admitted `OpenUniverseV3`, never wire members.
  - `dependencyMode` is true for every admitted payload. `dependencySourceSetId` is required and
    non-null, and an empty `DependencySourceSetV1` still takes `DependencySourceManifest`
    (`entries []`), `DependencySourceSeal` (all counts 0) and `DependencySourceAccepted`, with no
    chunk.
  - `preparedMode` is `preparedOutputSetId` non-null.
  - Rows P3-09 and P3-10 are therefore unreachable from an admitted major-3 OpenUniverse and remain
    only as the abstract table's guard partition.
  - The executable binding is `protocol3_open_universe_event`. Event-only traces that assert the
    booleans directly remain abstract table tests.

**Pre-Analyze `Unavailable`.** A native-context mismatch detected after custody is the
worker terminal `Unavailable` with `PreAnalyzeUnavailableV1` = `{executionId, snapshotId,
planId, reason: "native-context-mismatch", nativeContextId, recomputedNativeContextId}`.

- **Phase.** It is lawful only while the host waits for `NativeContextVerified`:
  `typescript-semantic` `WAIT_NATIVE_CONTEXT_VERIFIED` (row T2-10) and `rust-semantic` row P3-21.
  Outside that phase the payload is a protocol violation, and inside it the post-Analyze
  payloads are.
- **Reason.** It must be exactly `native-context-mismatch`. No other reason is admitted before
  Analyze, and that reason is never admitted after Analyze (`TypeScriptUnavailableV2`,
  `UnavailableV3`).
- **Correlation.**
  - `executionId`, `snapshotId` and `planId` equal OpenUniverse.
  - `nativeContextId` equals `universe.resolvedInputs.nativeContextId`.
  - `recomputedNativeContextId` is the worker's recomputation (§9.5) and differs from it.
  - The payload carries no `analysisOrdinal`, `affectedStageIds`, `coverage` or
    `coverageCommitment`, because the worker has received no Analyze.
- **After it.** The exchange continues with zero-exit, then EOF, then DONE.
  - Any other frame is a post-terminal fault.
  - A nonzero exit, signal, deadline or stdout byte is a process fault.
  - A malformed or uncorrelated payload, equal contexts, another reason or the wrong phase is
    `PROVIDER.PROTOCOL_VIOLATION`: no facts, no Coverage and no Run.
- **Host conversion.** Only after DONE is the clean terminal converted, as
  `stage_authority("unavailable")` (indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`). It is never
  treated as an operational fault.
  - **Affected domains.** Every stage the host would have placed in this Analyze
    (`typescript-semantic` `multiStageAnalyze.selection`; `rust-semantic`
    `planAndDomainProjection.selectedStageRule`), with the requested coverage domains the host
    derived before spawn.
  - **Minted entries.** For each requested key the host mints one `CoverageResultV3` with:
    - key: the host subject scope;
    - `coverage`: `unknown`;
    - `examinedUniverse`: the host commitment and count;
    - `resolutionCompleteness`: `completeness_from_stage` with `attempted=false`,
      `stageTerminal=unavailable` and `examinedExhaustive=false`, which gives `not-attempted` on a
      resolved rung and `not-applicable` otherwise;
    - `closedWorld`: `closed_world_v2` over no manifest, no recognized entry points and no edges,
      with external consumers `unknown`;
    - `derivationKinds`: `[]`;
    - `confidenceMillionths`: 0;
    - deficiency `provider-unavailable` with a null cause.
  - **Admission.** Each entry is admitted through `admit_coverage_result_v3`, and then
    `run_termination` applies.
  - **Worker input.** No stage id and no coverage comes from the worker
    (`pre_analyze_unavailable_conversion`).

**Coverage frames.** `CoverageResultV3` is an entry type, never a frame.

- **Frame names.** `typescript-semantic` keeps the frame name `Coverage`. Its payload
  `TypeScriptCoverageV2` is the `CoverageV1` wrapper `{analysisOrdinal: 0, stageId, entries,
  coverageCommitment}`, with `entries` a list of 1 to `maxCoverageEntriesPerFrame`
  `CoverageResultV3` values. `rust-semantic` renames the frame `CoverageV3` (§9.2, P3-24); its
  payload `CoverageV3` is the `CoverageV2` wrapper with `CoverageResultV3` entries.
- **Entry attribution.** `CoverageResultV3` has no `stageId` or `entryOrdinal`. The wrapper
  `stageId` attributes every entry, and `entries[i]` answers `requestedCoverageDomain.keys[i]`.
  - `relation`, `resolution` and `subjectScopeCommitment` equal the requested key.
  - `sourceUniverse` and `targetUniverse` are the 64-hex suffixes of its universe ids.
  - The request key's `producer`, `producerVersion` and `schemaVersion` stay request coordinates.
  - The entry count equals the requested key count.
- **Commitments.** Recipes and domains are unchanged; they now commit the ordered
  `CoverageResultV3` values. This covers `CoverageV1`/`CoverageV2` `coverageCommitment`,
  `typescript-semantic` `StageResultV1.coverageCommitment` and `CompleteV1.coverageStreamCommitment`,
  and `rust-semantic` `commitments.stageCoverage`, `commitments.coverageStream` and
  `StageResultV2.coverageCommitment`.
- **Terminal coverage.** `TypeScriptBudgetExhaustedV2`/`BudgetExhaustedV3` and post-Analyze
  `TypeScriptUnavailableV2`/`UnavailableV3` keep their members. Their `coverage` holds
  `CoverageResultV3` values in stage-major/key order, carrying `budget-exhausted` or
  `provider-unavailable`; entry `k` belongs to the stage whose cumulative requested-key range
  contains `k`.
- **Stage output order.** Zero or more FactBatch frames, then exactly one Coverage frame per stage,
  is unchanged.

**Cancellation (`typescript-semantic`).** `CancelledV1.observedPhase` is `snapshot` for a
Cancel that the worker receives after emitting `SnapshotAccepted` and before receiving
Analyze, that is, with host phase `WAIT_NATIVE_CONTEXT_VERIFIED` or `READY_ANALYZE` at Cancel.
- No enum member or terminal route is added.
- These rules are unchanged: Cancel may be sent once from any nonterminal state, only `Cancelled`
  may follow, then EOF, and user-interruption D9 precedence still applies.
- `rust-semantic` `CancelledV2` still reports the exact concrete phase.

**Reference scope.** `provider_startup_exchange` admits Hello, HelloAck, OpenUniverse,
UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and Cancelled, each in
the phase the published machine is in. Snapshot, dependency-source, prepared, Analyze and
FactBatch frames are abstract events there. No framing, process or compiler is exercised.

"""

CHECK_STARTUP_BLOCK = r'''
    # ---- provider startup publication (section 9.7): the successor records are held to the INHERITED member lists,
    # the registered bundle, the section 9.2/9.4 reason prose and both published event machines, not to themselves.
    startup_doc = json.loads((HERE / "provider-startup.schemas.v1.json").read_text(encoding="utf-8"))
    ts_order = json.loads((HERE / "typescript-protocol2-order.v1.json").read_text(encoding="utf-8"))
    p3_doc = json.loads((HERE / "protocol3-transitions.v1.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(startup_doc)
    startup_faults: list[str] = []
    startup_open: list[str] = []
    def walk_startup(x, p):
        if isinstance(x, dict):
            if x.get("type") == "object" and "additionalProperties" not in x:
                startup_open.append(p)
            for k, v in x.items():
                walk_startup(v, p + "/" + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk_startup(v, p + "/" + str(i))
    walk_startup(startup_doc, "")
    sdefs = startup_doc["$defs"]
    universe_rows = json.loads((REPO / "docs/coop/artifacts/resolved-inputs.v2.json").read_text(encoding="utf-8"))[
        "planIdContract"]["semanticUniverseSchemas"]
    for name, inherited_required in [
            ("TypeScriptOpenUniverseV2", ps_ts["OpenUniverseV1"]["required"]),
            ("TypeScriptUniverseAcceptedV2", ps_ts["UniverseAcceptedV1"]["required"]),
            ("TypeScriptCoverageV2", ps_ts["CoverageV1"]["required"]),
            ("TypeScriptUnavailableV2", ps_ts["UnavailableV1"]["required"]),
            ("TypeScriptBudgetExhaustedV2", ps_ts["BudgetExhaustedV1"]["required"]),
            ("OpenUniverseV3", ps_rust["OpenUniverseV2"]["required"]),
            ("UniverseAcceptedV3", ps_rust["UniverseAcceptedV2"]["required"]),
            ("CoverageV3", ps_rust["CoverageV2"]["required"]),
            ("UnavailableV3", ps_rust["UnavailableV2"]["required"]),
            ("BudgetExhaustedV3", ps_rust["BudgetExhaustedV2"]["required"]),
            ("TypeScriptSemanticUniverseV2", universe_rows["typescript-v1"]["required"]),
            ("RustSemanticUniverseV2", universe_rows["rust-v1"]["required"])]:
        d = sdefs[name]
        if list(d["required"]) != list(inherited_required) or d.get("additionalProperties") is not False:
            startup_faults.append(f"{name} members {d['required']} != inherited {inherited_required}")
    entry_ref = {"$ref": model.SCHEMAS["$id"] + "#/$defs/CoverageResultV3"}
    for name, member in (("TypeScriptCoverageV2", "entries"), ("CoverageV3", "entries"), ("TypeScriptUnavailableV2", "coverage"),
                         ("UnavailableV3", "coverage"), ("TypeScriptBudgetExhaustedV2", "coverage"), ("BudgetExhaustedV3", "coverage")):
        if sdefs[name]["properties"][member]["items"] != entry_ref:
            startup_faults.append(f"{name}.{member} items are not the registered CoverageResultV3")
    if (sdefs["PreAnalyzeUnavailableV1"]["properties"]["reason"] != {"const": "native-context-mismatch"}
            or "native-context-mismatch" not in model.SCHEMAS["$defs"]["UnavailableReasonV3"]["enum"]):
        startup_faults.append("PreAnalyzeUnavailableV1 reason is not exactly the registered native-context-mismatch")
    startup_law = startup_doc["x-opensip-startup-law"]
    added92 = re.search(r"`UnavailableReasonV3` adds (.*?)\.\n", contract_text, re.S)
    added94 = re.search(r"`Unavailable\.reason` adds (.*?)\.\n", contract_text, re.S)
    rust_added = re.findall(r"`([a-z-]+)`", added92.group(1)) if added92 else []
    ts_added = re.findall(r"`([a-z-]+)`", added94.group(1)) if added94 else []
    want_ts = sorted(set(ps_ts["UnavailableV1"]["fields"]["reason"].removeprefix("enum ").split("|")) | set(ts_added))
    want_rust = sorted((set(ps_rust["UnavailableV2"]["fields"]["reason"].split("|")) | set(rust_added)) - {"native-context-mismatch"})
    if (not ts_added or sorted(sdefs["TypeScriptUnavailableV2"]["properties"]["reason"]["enum"]) != want_ts
            or startup_law["postAnalyzeReasons"]["typescript-semantic"] != want_ts):
        startup_faults.append(f"typescript post-Analyze reasons != delivery.v2 reasons + section 9.4 additions {want_ts}")
    if (not rust_added or sorted(sdefs["UnavailableV3"]["properties"]["reason"]["enum"]) != want_rust
            or startup_law["postAnalyzeReasons"]["rust-semantic"] != want_rust):
        startup_faults.append(f"rust post-Analyze reasons != rust-provider-protocol.v2 reasons + section 9.2 additions {want_rust}")
    p3_rows = {r["id"]: r for r in p3_doc["rules"]}
    if (p3_rows["P3-24"]["frame"] != "CoverageV3" or p3_rows["P3-21"]["frame"] != "Unavailable"
            or p3_rows["P3-21"]["phase"] != "WAIT_NATIVE_CONTEXT_VERIFIED"):
        startup_faults.append("protocol3 rows no longer carry the CoverageV3 frame or the pre-Analyze Unavailable phase")
    if set(p3_doc.get("rowPayloads", {})) - set(p3_rows) - {"standing"}:
        startup_faults.append("protocol3 rowPayloads names a row that does not exist")
    if set(p3_doc.get("derivedObservations", {})) != {"standing", "dependencyMode", "preparedMode"}:
        startup_faults.append("protocol3 derivedObservations must name exactly dependencyMode and preparedMode")
    ts_rows = {r["id"]: r for r in ts_order["rules"]}
    if (ts_order["ruleCount"] != len(ts_order["rules"]) or len(ts_rows) != len(ts_order["rules"])
            or ts_rows["T2-08"]["next"] != "WAIT_NATIVE_CONTEXT_VERIFIED"
            or ts_rows["T2-10"].get("guard") != {"unavailablePayload": "pre-analyze"} or ts_rows["T2-13"]["frame"] != "Coverage"):
        startup_faults.append("typescript order table does not carry the section 9.7 insertions exactly")
    allowed_ts_frames = set(ts_protocol["wireSchema"]["frameSchemas"]) | {"NativeContextVerified", "zero-exit", "eof", "*PROCESS_FAULT", "*"}
    added_ts_frames = sorted({r["frame"] for r in ts_order["rules"]} - allowed_ts_frames)
    if added_ts_frames:
        startup_faults.append(f"typescript order table adds frames {added_ts_frames}")
    pre_terminal = set(ts_order["wildcards"]["*PRE_TERMINAL"]["phases"])
    def ts_phases(row):
        return set() if row["phase"] == "*ANY" else (pre_terminal if row["phase"] == "*PRE_TERMINAL" else {row["phase"]})
    def ts_overlap(a, b):
        if a["frame"] != b["frame"] or not (ts_phases(a) & ts_phases(b)):
            return False
        ga, gb = a.get("guard", {}), b.get("guard", {})
        return not any(k in gb and gb[k] != v for k, v in ga.items())
    overlapping = [(a["id"], b["id"]) for i, a in enumerate(ts_order["rules"]) for b in ts_order["rules"][i + 1:] if ts_overlap(a, b)]
    if overlapping:
        startup_faults.append(f"typescript order rows overlap {overlapping}")
    report["providerStartup"] = {"document": "native/provider-startup.schemas.v1.json", "defs": len(sdefs),
                                 "openObjects": startup_open, "typescriptOrderRules": len(ts_order["rules"]),
                                 "faults": startup_faults}
'''

EDITS = [
    (NE, "s0-startup-rows", LAST_S0_ROW, LAST_S0_ROW + "\n" + "\n".join(S0_ROWS)),
    (NE, "s9.1-steps-3-4",
     "3. **OpenUniverse** carries `snapshot2`, `plan2`, the universe descriptor\n   including `nativeContext`, and `RepositoryResolutionV3`. The host state\n   machine admits it only when `identityNegotiated=true`; otherwise the run faults\n   with `sourceBytesSent=false` (`protocol3-open-universe-without-identity-faults`).\n4. Snapshot custody, dependency-source custody, prepared custody,\n   `NativeContextVerified`, then Analyze.",
     "3. **OpenUniverse** carries `snapshot2` (as `snapshotId`), `plan2` (as `planId`) and the\n   universe descriptor, whose `resolvedInputs.nativeContextId` is the Plan-bound\n   native context; `rust-semantic` also carries `RepositoryResolutionV3` and\n   `typescript-semantic` carries none (§9.7 gives both payloads field by field). The host state\n   machine admits it only when `identityNegotiated=true`; otherwise the run faults\n   with `sourceBytesSent=false` (`protocol3-open-universe-without-identity-faults`).\n4. Snapshot custody; for `rust-semantic`, dependency-source custody (always, an empty set\n   included) and prepared custody (only when `preparedOutputSetId` is non-null); then\n   `NativeContextVerified` or the pre-Analyze `Unavailable(native-context-mismatch)` of\n   §9.7; then Analyze."),
    (NE, "s9.2-native-context-row",
     "| `NativeContextVerified` | worker→host | `{nativeContextId, recomputedNativeContextId, equal:true}` — a mismatch is sent as `Unavailable(native-context-mismatch)` | no |",
     "| `NativeContextVerified` | worker→host | `NativeContextVerifiedV1` `{nativeContextId, recomputedNativeContextId, equal:true}` — a mismatch is sent instead as `Unavailable` with `PreAnalyzeUnavailableV1` (§9.7) | no |\n| `Unavailable` | worker→host | before Analyze (P3-21): `PreAnalyzeUnavailableV1`, reason `native-context-mismatch` only; after Analyze (P3-25): `UnavailableV3`, reason never `native-context-mismatch` (§9.7) | yes |"),
    (NE, "s9.2-coverage-row",
     "| `CoverageV3` | worker→host | `CoverageResultV3` entries, exact bijection with the requested domain | no |",
     "| `CoverageV3` | worker→host | `CoverageV3`: the inherited `CoverageV2` wrapper `{analysisOrdinal, stageId, entries, coverageCommitment}` whose `entries` are `CoverageResultV3`, `entries[i]` answering requested key `i`, exact bijection with the requested domain (§9.7); this frame name supersedes the inherited `Coverage` | no |"),
    (NE, "s9.2-derived-modes",
     "`dependencyMode`/`preparedMode` are set at OpenUniverse, `identityNegotiated` at\nHelloAck.",
     "`dependencyMode`/`preparedMode` are set at OpenUniverse as host-derived\nobservations of the admitted `OpenUniverseV3` (§9.7: `dependencyMode` is always\ntrue, `preparedMode` is `preparedOutputSetId` non-null; neither is a wire member),\n`identityNegotiated` at HelloAck."),
    (NE, "s9.4-coverage-mention",
     "`TypeScriptNativeContextV2` of §2.4), `CoverageV3`, `resolution-completeness-v2`,",
     "`TypeScriptNativeContextV2` of §2.4), `CoverageResultV3` coverage in the `Coverage` frame (§9.7), `resolution-completeness-v2`,"),
    (NE, "s9.4-normal-order",
     "worker→host frame with the §9.2 payload (§0). This sentence changes no Coverage frame\nselector: §9.2 names only the `rust-semantic` frame `CoverageV3`.",
     "worker→host frame with the §9.2 payload (§0). The complete major-2 order, including the\npre-Analyze `Unavailable`, the post-Analyze `Unavailable`, `BudgetExhausted` and cancellation,\nis the published abstract table\n`docs/coop/design-corrections/native/typescript-protocol2-order.v1.json` (§9.7). The\n`typescript-semantic` Coverage frame keeps the inherited name `Coverage`; only\n`rust-semantic` renames it `CoverageV3`."),
    (NE, "s9.7-section",
     "only. No new DomainDetailCode, no new D9 code. LIVE D9 is not discharged.\n\n---\n\n## 10. Deficiencies, precedence and D9 mapping",
     "only. No new DomainDetailCode, no new D9 code. LIVE D9 is not discharged.\n\n" + SECTION_97 + "---\n\n## 10. Deficiencies, precedence and D9 mapping"),
    (NE, "s12-count-free-cases",
     "`native/native-cases.v2.json` (428 cases) carries hand-authored expected outcomes; every",
     "`native/native-cases.v2.json` carries hand-authored expected outcomes (its case count and positive/negative split are reported by the generated report, not restated here); every"),
    (NE, "s12-count-free-defs",
     "against the closed bundle, 115 definitions; workflow payloads",
     "against the closed bundle; workflow payloads"),
    (NE, "s12-startup-evidence",
     "`hashlib`/`cbor2`-authored vectors). It frames no bytes and runs no worker.",
     "`hashlib`/`cbor2`-authored vectors). It frames no bytes and runs no worker. Startup frames\nvalidate against `native/provider-startup.schemas.v1.json` and run through\n`provider_startup_exchange` over the published Rust (`protocol3-transitions.v1.json`) and\nTypeScript (`typescript-protocol2-order.v1.json`) event machines; the host conversion of a\npre-Analyze `Unavailable` executes through the existing coverage admission."),
    # ------------------------------------------------------------------ protocol3 transitions
    (P3, "open-universe-state-update",
     "   \"sets\": \"dependencyMode and preparedMode from the frame's booleans; these are the guards P3-08..P3-10 and P3-14..P3-15 select on\"",
     "   \"sets\": \"dependencyMode and preparedMode as HOST-DERIVED OBSERVATIONS of the admitted OpenUniverseV3 payload (derivedObservations), never frame booleans; these are the guards P3-08..P3-10 and P3-14..P3-15 select on\""),
    (P3, "derived-observations-and-row-payloads",
     " \"ruleCount\": 34,",
     " \"derivedObservations\": {\n"
     "  \"standing\": \"Event fields that are not wire members. native_evidence_model.v2.protocol3_open_universe_event derives them from an OpenUniverseV3 admitted under native-evidence section 9.7; an event-only trace that supplies them directly is an abstract table test and makes no whole-wire claim.\",\n"
     "  \"dependencyMode\": \"true for every admitted OpenUniverseV3: RepositoryResolutionV3.dependencySourceSetId is required and non-null, and an empty dependency set still takes DependencySourceManifest, DependencySourceSeal and DependencySourceAccepted. Rows P3-09 and P3-10 are therefore unreachable from an admitted major-3 OpenUniverse.\",\n"
     "  \"preparedMode\": \"repositoryResolution.preparedOutputSetId is not null (equal to universe.resolvedInputs.preparedOutputSetId)\"\n"
     " },\n"
     " \"rowPayloads\": {\n"
     "  \"standing\": \"The payload record each frame row admits; validation stays owned by the named schema documents and section 9 prose.\",\n"
     "  \"P3-01\": \"HelloV3 (native/provider-handshake.schemas.v1.json)\",\n"
     "  \"P3-02\": \"HelloAckV3 (native/provider-handshake.schemas.v1.json)\",\n"
     "  \"P3-03\": \"OpenUniverseV3 (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-04\": \"UniverseAcceptedV3 (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-20\": \"NativeContextVerifiedV1 (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-21\": \"PreAnalyzeUnavailableV1, reason native-context-mismatch only (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-24\": \"CoverageV3 wrapper with CoverageResultV3 entries (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-25\": \"UnavailableV3, reason never native-context-mismatch (native/provider-startup.schemas.v1.json)\",\n"
     "  \"P3-26\": \"BudgetExhaustedV3 (native/provider-startup.schemas.v1.json)\"\n"
     " },\n"
     " \"ruleCount\": 34,"),
    # ------------------------------------------------------------------ native README
    (RD, "readme-schema-count-free",
     "| `native-evidence.schemas.v2.json` | 100 closed Draft 2020-12 records (",
     "| `native-evidence.schemas.v2.json` | the registered closed Draft 2020-12 bundle, definition count in the generated report `schemas.defs` ("),
    (RD, "readme-cases-count-free",
     "| `native-cases.v2.json` | 132 hand-authored cases (46 positive, 86 negative/adversarial) with the",
     "| `native-cases.v2.json` | hand-authored positive and negative/adversarial cases, counts in the generated report `cases`, with the"),
    (RD, "readme-matrix-count-free",
     "| `native-capability-matrix.v2.json` | 60 cells: 10 capabilities × 6 language modes over",
     "| `native-capability-matrix.v2.json` | one cell per capability × language mode, counts in the generated report `matrix`, over"),
    (RD, "readme-startup-files",
     "frames nothing and qualifies no worker |\n| `native-cases.v2.json` |",
     "frames nothing and qualifies no worker |\n"
     "| `provider-startup.schemas.v1.json` | closed startup and coverage successor records: `TypeScriptOpenUniverseV2`/`TypeScriptUniverseAcceptedV2`/`TypeScriptSemanticUniverseV2`, `OpenUniverseV3`/`UniverseAcceptedV3`/`RustSemanticUniverseV2`, `NativeContextVerifiedV1`, `PreAnalyzeUnavailableV1`, `TypeScriptCoverageV2`/`CoverageV3`, `TypeScriptUnavailableV2`/`UnavailableV3`, `TypeScriptBudgetExhaustedV2`/`BudgetExhaustedV3`, and the `x-opensip-startup-law` |\n"
     "| `typescript-protocol2-order.v1.json` | published typescript-semantic major-2 abstract event machine: the inherited delivery.v2 order plus the section 9.4/9.7 insertions |\n"
     "| `provider_startup_model.v1.py` | startup admissions and the TypeScript order interpreter loaded by the model; `provider_startup_exchange` and `pre_analyze_unavailable_conversion` live in the model because they compose the native coverage owners |\n"
     "| `native-cases.v2.json` |"),
    (RD, "readme-startup-selectors",
     "| superseded by `provider-handshake.schemas.v1.json` | §0, §9 |",
     "| superseded by `provider-handshake.schemas.v1.json` | §0, §9 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `...payloadSchemas.OpenUniverseV1`, `...UniverseAcceptedV1`, `...definitions.SnapshotId`, `...PlanId`, `...TypeScriptSemanticUniverseV1`, `...TypeScriptSemanticUniverseKey` | superseded (major 2: `TypeScriptOpenUniverseV2`/`TypeScriptUniverseAcceptedV2`, snapshot2/plan2, native universe identity) | §9.7 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `...payloadSchemas.CoverageV1`, `...definitions.CoverageResultV1`, `...UnavailableV1`, `...BudgetExhaustedV1`, `...StageResultV1.fields.coverageCommitment`, `...CompleteV1.fields.coverageStreamCommitment`, supervision `coveragePayload` rows | superseded (frame `Coverage` kept; `CoverageResultV3` entries in the inherited wrappers) | §9.7 |\n"
     "| `docs/coop/artifacts/delivery.v2.json` | `...ordering.unavailableTerminal`, `...supervision.cleanUnavailable.allowedImmediatelyAfter`, `...CancelledV1.fields.observedPhase` | extended (pre-Analyze `Unavailable`; `snapshot` over the inserted interval) | §9.7 |\n"
     "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `...OpenUniverseV2`, `...UniverseAcceptedV2`, `...definitions.SnapshotId`, `...PlanId`, `...RustUniverseV1`, `$.planAndDomainProjection` universe id algorithms | superseded (major 3: `OpenUniverseV3`/`UniverseAcceptedV3`, derived modes) | §9.7 |\n"
     "| `docs/coop/artifacts/rust-provider-protocol.v2.json` | `...frameSchemas.Coverage`, `...CoverageV2`, `...UnavailableV2`, `...BudgetExhaustedV2`, `$.commitments.stageCoverage`, `$.commitments.coverageStream`, `...StageResultV2` | superseded (frame `CoverageV3`; `CoverageResultV3` entries; pre-Analyze payload at P3-21) | §9.2, §9.7 |"),
    # ------------------------------------------------------------------ checker
    (CK, "consumed-startup",
     "    (\"docs/coop/design-corrections/native/occupancy-companion.schema.v1.json\", \"FactBatchV3 companion items resolved by the wire model registry\"),\n]",
     "    (\"docs/coop/design-corrections/native/occupancy-companion.schema.v1.json\", \"FactBatchV3 companion items resolved by the wire model registry\"),\n"
     "    (\"docs/coop/design-corrections/native/provider-startup.schemas.v1.json\", \"owned: startup, pre-Analyze Unavailable and Coverage wrapper records (section 9.7)\"),\n"
     "    (\"docs/coop/design-corrections/native/typescript-protocol2-order.v1.json\", \"owned: typescript-semantic major-2 abstract event machine (section 9.7)\"),\n"
     "    (\"docs/coop/design-corrections/native/provider_startup_model.v1.py\", \"owned: startup admissions and TypeScript order interpreter loaded by the model (section 9.7)\"),\n]"),
    (CK, "startup-drift-controls",
     "                              \"section94Members\": len(ts_prose), \"faults\": wire_faults}\n",
     "                              \"section94Members\": len(ts_prose), \"faults\": wire_faults}\n" + CHECK_STARTUP_BLOCK),
    (CK, "ok-includes-startup",
     "          and not wire_faults and not wire_open)",
     "          and not wire_faults and not wire_open\n          and not startup_faults and not startup_open)"),
    (CK, "print-startup-faults",
     "    for fault in wire_faults + [\"open object \" + p for p in wire_open]:\n        print(\"FAIL provider-wire:\", fault)\n",
     "    for fault in wire_faults + [\"open object \" + p for p in wire_open]:\n        print(\"FAIL provider-wire:\", fault)\n"
     "    for fault in startup_faults + [\"open object \" + p for p in startup_open]:\n        print(\"FAIL provider-startup:\", fault)\n"),
    (CK, "limitations-startup",
     "descriptor digests hash canonical.py bytes, which equal RFC 8785 only for the fixture value domain.\",\n    ]",
     "descriptor digests hash canonical.py bytes, which equal RFC 8785 only for the fixture value domain.\",\n"
     "        \"Provider startup exchanges admit Hello, HelloAck, OpenUniverse, UniverseAccepted, NativeContextVerified, Unavailable, the Coverage frame and Cancelled; snapshot, dependency-source, prepared, Analyze and FactBatch frames are abstract events, and the event machines are abstract host tables, not a framed process.\",\n    ]"),
    # ------------------------------------------------------------------ planning inputs
    (INV, "pending-decision-handshake-names",
     "    \"Use existing shared identity tokens/HelloV3 contracts and generated bindings; no extra shared provider SDK is selected for the distinct TS2/Rust3 protocols. Reconsider only with demonstrated reuse.\",",
     "    \"Use the existing shared identity tokens, frame envelopes and generated bindings with the per-language handshakes (typescript-semantic TypeScriptHelloV2/TypeScriptHelloAckV2, rust-semantic HelloV3/HelloAckV3); no extra shared provider SDK is selected for the distinct TS2/Rust3 protocols. Reconsider only with demonstrated reuse.\","),
    (IBP, "build-plan-handshake-names",
     "fallback. Current worker protocols are TS2/Rust3. Reuse shared identity tokens,\nHelloV3 framing and generated contract carriers. No additional provider SDK is\nselected merely to hide their distinct protocol obligations.",
     "fallback. Current worker protocols are TS2/Rust3. Reuse shared identity tokens,\nframe envelopes and generated contract carriers; the handshakes stay per language\n(`TypeScriptHelloV2`/`TypeScriptHelloAckV2` for TS2, `HelloV3`/`HelloAckV3` for Rust3).\nNo additional provider SDK is selected merely to hide their distinct protocol obligations."),
]

texts = {}
for rel, label, old, new in EDITS:
    if rel not in texts:
        texts[rel] = (ROOT / rel).read_text(encoding="utf-8")
for rel, label, old, new in EDITS:
    if texts[rel].count(old) != 1:
        raise SystemExit(f"{rel} [{label}]: expected exactly one occurrence, found {texts[rel].count(old)}")
log = []
current = dict(texts)
for rel, label, old, new in EDITS:
    before = hashlib.sha256(current[rel].encode("utf-8")).hexdigest()
    current[rel] = current[rel].replace(old, new, 1)
    log.append({"file": rel, "edit": label, "beforeSha256": before,
                "afterSha256": hashlib.sha256(current[rel].encode("utf-8")).hexdigest()})
for rel, text in current.items():
    if rel.endswith(".json"):
        json.loads(text)
    (ROOT / rel).write_text(text, encoding="utf-8")
print(json.dumps({"applied": len(log), "edits": log}, indent=1))

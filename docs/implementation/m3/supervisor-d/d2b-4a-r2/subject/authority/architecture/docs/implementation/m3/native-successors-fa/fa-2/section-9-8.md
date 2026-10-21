### 9.8 Symbol census on negotiated Analyze and Complete (worker product)

A TypeScript or Rust provider's symbol census is its explicit population assertion (the
header above; identity §4): the first-party symbols its program declares over the binding's
symbol extent (enumeration contract §5), with the paths it examined. The worker delivers it
on negotiated payloads of two existing frames. The host projects it into `SubjectInventoryV1`
records exactly as it projects `TargetAttributionV2` from `OccupancyCompanionV1` (§9.6): the
inventories are host-derived typed inputs under their published admission owners, never stage
outputs and never a new frame name (execution-inputs contract §§6-7). Field-level records are
in `docs/implementation/m3/native-successors-fa/fa-2/design/native/symbol-census.schemas.v1.json`
("the census schema"; closed, with its `x-opensip-symbol-census-law`).

**Negotiated payloads, not new frames.** Capability token `symbol-census-v1` (§9.1). When it
is on both Hello and HelloAck, the `Analyze` payload is `TypeScriptAnalyzeV2`
(`typescript-semantic`) or `AnalyzeV3` (`rust-semantic`), and the `Complete` payload is
`TypeScriptCompleteV2` or `CompleteV3`. Each is the inherited payload (`delivery.v2`
`AnalyzeV1` / `CompleteV1`; `rust-provider-protocol.v2` `AnalyzeV2` / `CompleteV2`) with every
inherited member unchanged in name, type and law, plus one member, `symbolCensus`. When the
token is absent the inherited payloads remain. A census-bearing payload without the token, or
an inherited payload with it, is `PROVIDER.PROTOCOL_VIOLATION`. Frame names, phases,
terminals, limits, commitments, identity versions, `protocol3-transitions.v1.json` and
`typescript-protocol2-order.v1.json` are unchanged. Protocol major stays 3 / TypeScript major 2.

**When a census is owed (Plan time).** The host owes a worker a census exactly when the
Plan's `EnumerationPlanV1` expects at least one `(cellOrdinal, programOrdinal, symbol)`
inventory (enumeration contract §4) whose available binding's universe is that worker's
universe. Every such binding names one `enumerator.closureId`: the worker's provider closure,
which is also the `producerClosure` of every stage the worker serves. The host requests a
census from every worker it asks for a `symbol`-kind key, and from no other. A Plan that binds
such a universe to another enumerator, or that disagrees with this rule, is a host invariant
refused before spawn. Where a census is owed, `symbol-census-v1` is a token the Plan needs
(§9.1, step 1): a signed row without it is never spawned, with that step's consequence.

**Phase 1: the request commits to the census rule.** On Analyze, `symbolCensus` is
`SymbolCensusRequestV1` `{enumeratorClosure}`, that enumerator's `closure2` text, when a
census is owed, and `null` otherwise. Every requested key whose relation's registry
`subjectKind` is `symbol` (the registry's `subjectKindLaw`) carries, as `subjectScopeCommitment`,
the §4.1a commitment of the census-free descriptor

    D∅ = {schemaVersion: 2, snapshotId, sourceUniverse, targetUniverse,
          relation, resolution, enumeratorClosure, subjects: []}

built from the key and the Plan before spawn. D∅ fixes everything the Plan fixes (the
snapshot, the relation and rung, both universes and the enumerator) and leaves only the
subjects open. Every other key carries §4.1a's commitment over the host's `D`, as before; no
key carries the inherited per-stage file-scope commitment (§0). Before analysis the worker
recomputes each `symbol`-kind key's D∅ commitment and rejects a mismatch as provider-protocol,
which is the inherited worker rule's disposition.

**Phase 2: the return commits to the values.** On `Complete`, `symbolCensus` is
`SymbolCensusV1`, and it is `null` exactly when the request's was:
- `{state: "complete", examinedPaths, rows}`. `examinedPaths` is the canonical set of the
  logical paths the worker examined. `rows` are `SymbolCensusRowV1`
  `{nativeSubjectId, path, qualifiedName, exported, signatureTokens}`, strictly ascending
  and unique by the UTF-8 bytes of `nativeSubjectId` (a `SubjectIdV1`), each `path` a member
  of `examinedPaths`. Rows name first-party symbols only: an external symbol is not a row,
  and a symbol with no fact is still one. The worker supplies no `planId`,
  `parameterDigest`, `cellOrdinal`, `programOrdinal`, `kind`, state carrier,
  `subjectLanguage` or `projections`.
- `{state: "over-bound", rowCount, examinedPathCount}`, with no rows. It is sent instead
  exactly when the complete census would exceed 100,000 rows, 100,000 examined paths or
  4,194,304 bytes of deterministic CBOR. A census is never truncated or split.

There is no `partial` and no `unavailable` census: a worker that cannot attest its complete
symbol extent does not send `Complete`.

Every `symbol`-kind entry in that Analyze's `Coverage` or `CoverageV3` frames carries, as
`key.subjectScopeCommitment` and `examinedUniverse.subjectScopeCommitment`, the §4.1a
commitment of D∅ with `subjects` set to the rows' `nativeSubjectId`s in canonical-set order
(identity §3; this is not row order), and `examinedUniverse.subjectCount` equal to the row
count. The worker computes it with the foundation canonical encoder and `H` frame, the one
recipe of §4.1a. Under an `over-bound` census these entries keep their requested commitment with
`subjectCount` 0. This is the only departure from §9.7's requested-key equality.

**Other terminals carry no census.** A clean `BudgetExhausted` or post-Analyze `Unavailable`
carries none. Its `symbol`-kind entries keep the requested D∅ commitment with `subjectCount`
0, and the owed inventories are host-derived outcomes of the terminal: `partial`,
`budget-exhausted`, a null cause, no rows and no examined paths; or `unavailable` with
`provider-unavailable`. The pre-Analyze conversion mints D∅ entries (§9.7). A fault, a
cancellation or a missing `Complete` admits no census (§10).

**Host projection and admission, at clean settlement only.** After the clean settlement of a
`Complete` (terminal, zero exit, EOF, every commitment recomputed), and atomically with that
Analyze's candidates and Coverage, the host:
1. projects the census once for every owed locator into `SubjectInventoryV1`
   `{schemaVersion: 1, planId, parameterDigest, cellOrdinal, programOrdinal, kind: "symbol",
   state: "complete", deficiency: null, nativeCause: null, examinedPaths, rows}`. It fills
   `planId` from the retained Plan and `parameterDigest` as the raw SHA-256 of
   `C(EnumerationPlanV1)`. On every row it adds `kind: "symbol"`, `subjectLanguage` from the
   subject-inventory suffix table on `path`, and `projections: []` (projection unavailable).
   Rows are byte-equal across locators;
2. owner-admits each record against its schema, its locator and the state law (`complete`:
   `examinedPaths` equals the binding's symbol extent), before the full enumeration join;
3. builds `D` for every `symbol`-kind key from the admitted census (§4.1a) and admits each
   entry through `admit_coverage_result_v3`, unchanged.

A refusal anywhere discards the whole return. Each record's identity is the raw SHA-256 of
`C(record)`, and the host captures it into `hostCapture.hostDerivedRefs` with origin
provider-return. A projected record or a `D` above its 4 MiB `C` ceiling takes the same route
as an `over-bound` census: the subject-scope bound's scope-limit route, which this section does
not own. Nothing here truncates, shards or rewrites a census.

**Refusals.** A malformed, misordered, out-of-bound, wrongly null or token-mismatched census
payload, and a request commitment the worker cannot recompute, are `PROVIDER.PROTOCOL_VIOLATION`
under the §10 fault law. A locator, state, extent or row refusal is the enumeration owner's,
with origin provider-return. A census-commitment or count mismatch on an entry is §4.1a's
existing refusal. Internal keys stay internal; no public code, D9 code, deficiency or cause
is added.

**Not this section.** Census rows mint no `fact2` and are not candidates. The host never
builds a census from facts, anchors or files. No new `H` domain, relation, frame, phase or
terminal exists. The in-host syntax census (E1) needs no carrier and is unaffected.

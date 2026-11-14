### 9.8 Symbol census on negotiated Analyze and Complete (worker product)

A TypeScript or Rust provider's symbol census is its explicit population assertion (the header above; identity §4) under one named population rule: the first-party symbols its program declares over the binding's symbol extent (enumeration contract §5) that the rule selects, with the paths it examined. The default rule, `native.symbol-census-population.default.v1`, selects the first-party symbols its program declares over the binding's symbol extent, all of them. A census's rule is the population-rule binding of its enumerator closure (below); a closure whose binding names the default rule, or that has no binding while the carrier of bindings does not yet exist, is under the default rule. Only a rule stated in this section can be bound. A census's `complete` state and its row count describe its rule's population and no wider one. Rule ids are immutable (erratum FA2-CENSUS-E1). The worker delivers it
on negotiated payloads of two existing frames. The host projects it into `SubjectInventoryV1`
records exactly as it projects `TargetAttributionV2` from `OccupancyCompanionV1` (§9.6): the
inventories are host-derived typed inputs under their published admission owners, never stage
outputs and never a new frame name (execution-inputs contract §§6-7). Field-level records are
in `docs/implementation/m3/native-successors-fa/fa-2/design/native/symbol-census.schemas.v1.json`
("the census schema"; closed, with its `x-opensip-symbol-census-law`).

**Population rules and their carrier (errata FA2-CENSUS-E1, FA2-CENSUS-E2 and FA2-CENSUS-E3).** The passages I1-I11 below are text of this section, inserted here in that order. Each is incorporated from the exact bytes of the file named, at the lines given, without its block-quote markers (`>`), and reads as if it were written here. Its line references keep reading the files they name; `9.8:N` is `docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md`, FA-2's rendering of this section. Nothing else in those files is text of this section: not their commentary, evidence, probes, code columns or status lines. The two sentences above and below that FA2-CENSUS-E1 amends (`9.8:3-5`, `9.8:56-57`) stand here in its words (`E1:54`, `E1:58`).

- **E1** = `docs/implementation/m3/errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md`, 32,962 bytes, sha256 `1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1`. Adopted by `docs/implementation/m3/errata-2026-11-13b/ADOPTION-FA2-CENSUS-E1.md` (3,472 bytes, sha256 `35cc11057dea4267a97d32fa43024a0be0e833849d5c71ea4ad32c7a53f76b46`).
- **E2** = `docs/implementation/m3/errata-2026-11-13c/ERRATUM-FA2-CENSUS-E2.md`, 35,800 bytes, sha256 `56723546361dd29bed388b22837f57f2fbb4ae131e61a7a957544ab0ad6f031e`. Adopted by `docs/implementation/m3/errata-2026-11-13c/ADOPTION-FA2-CENSUS-E2.md` (3,574 bytes, sha256 `a4434259e1ce294e066bc787d42935abcb3ee946c7d7b7c63b0c1ed7c48192d8`).
- **E3** = `docs/implementation/m3/errata-2026-11-14b/ERRATUM-FA2-CENSUS-E3.md`, 28,608 bytes, sha256 `83a1919be8a4a4a10f5d160ff403823433cf2df75d3bfdacb939d9194d382c5d`. Adopted by `docs/implementation/m3/errata-2026-11-14b/ADOPTION-FA2-CENSUS-E3.md` (8,068 bytes, sha256 `1d5a2c8d1b325e50ff2193ef4a62d27425a205b97151b8c3b87a480635f53261`).

| Passage | Lines | What it states |
|---|---|---|
| I1 | E1:74-78 | rule `…typescript.v1`: its sentences, members and seeds, and the two-copies rule (FCE1.3) |
| I2 | E1:82-111, the columns "#", "Declaration class" and "Rule" only (`E1:80`) | rule `…typescript.v1`: declaration classes C1-C28 (FCE1.3) |
| I3 | E1:122 | relations under `…typescript.v1` (FCE1.4) |
| I4 | E1:132 | widening: a wider population is a new rule (FCE1.5) |
| I5 | E1:160 | one population-rule binding per enumerator closure (FCE1.7) |
| I6 | E3:19-95 | the carrier, statements A1-A10: the closure (A1), form (A2), bindable rules (A3), writer and conflicting bindings (A4), when the carrier exists (A5), the Plan-time checks (A6), retention, binding classes and the replay table (A7), review (A8), "stated in this section" (A9), the end of the complete-census prohibition (A10) |
| I7 | E2:53-71 | rule `…typescript.v2`: v1 with statements 0-3 (FCE2.2) |
| I8 | E2:103-104, from its first word to "moves to v2." | `…typescript.v1` withdrawn before any use (FCE2.3) |
| I9 | E3:159 | rule `…typescript.v3`: v2 with statement 4 (FCE3.3) |
| I10 | E3:130-147, line 141 included | statement 4 of `…typescript.v3` and the two sentences on F3 (FCE3.2) |
| I11 | E3:167-168, from its first word to "moves to v3." | `…typescript.v2` withdrawn before any use (FCE3.3) |

Where these passages differ in wording, the later erratum governs, as it states itself: E3 A5 (`E3:34`) ends the interim readings of `E1:54` and `E1:160`, and E3 A3 (`E3:23-30`) is the only source of rules that packaging may write and a Plan may admit. So `…typescript.v1` and `…typescript.v2`, stated here, bind no closure (I8, I11; E3 A7, row RT-5).

**The rules stated in this section.** The block below lists every population rule this section states. It adds no rule, binding or check. Its syntax: the block is the lines strictly between the one line of this section that is exactly three backquotes (U+0060) followed by `opensip-stated-population-rules-v1`, and the next line that is exactly three backquotes. Each line is one row, the RFC 8785 form of a JSON object with exactly the members `a2Sha256`, `bindsRoleSubprotocol`, `rule` and `standing`, and the rows are strictly ascending by the UTF-8 bytes of `rule`. `rule` is a rule id. `a2Sha256` is the lowercase hex sha256 of that rule's A2 bytes (E3 A2). `standing` is `prospective` for a rule of E3 A3, and then `bindsRoleSubprotocol` is the one role subprotocol whose closures that A3 row binds; the prospective rows are exactly A3's rows. `standing` is `historical` for a rule stated only for reading retained evidence (E3 A7), and then `bindsRoleSubprotocol` is `null`; such a rule is no A3 row and passes no check of E3 A6. A reader that finds anything else refuses the block and reads no rule as stated.

```opensip-stated-population-rules-v1
{"a2Sha256":"6f2726992d65dfcf33700abcad964a9b1aad82178976ee2a2b508e66b7a84671","bindsRoleSubprotocol":"rust-semantic","rule":"native.symbol-census-population.default.v1","standing":"prospective"}
{"a2Sha256":"18c187c85b012882dd9ce022d8f4a907210456c2dd4f24d7cc614633cde12307","bindsRoleSubprotocol":null,"rule":"native.symbol-census-population.typescript.v1","standing":"historical"}
{"a2Sha256":"9610e54655c714ab30cbd54bd09d76fff993543b65f3c2d16eaa3a753f081600","bindsRoleSubprotocol":null,"rule":"native.symbol-census-population.typescript.v2","standing":"historical"}
{"a2Sha256":"c10552a44dc8086d300fc647f8607eda22f7327f00560302d42469ca8b8f85c7","bindsRoleSubprotocol":"typescript-semantic","rule":"native.symbol-census-population.typescript.v3","standing":"prospective"}
```

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
  of `examinedPaths`. Rows name first-party symbols of the census's population rule only: an external symbol is not a row, a declaration the rule excludes is not a row, and a symbol the rule includes that has no fact is still one. The worker supplies no `planId`,
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

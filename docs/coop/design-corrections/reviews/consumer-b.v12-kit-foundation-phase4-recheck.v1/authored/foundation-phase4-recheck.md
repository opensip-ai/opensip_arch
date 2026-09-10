# Phase 4 successor recheck

**Verdict: `PHASE4_DATA_ADMITS`**

Same-origin follow-through after `foundation-phase4-selfaudit.v1` `PHASE4_DATA_INCOMPLETE`. Not a new fresh origin. Independently rechecked the two corrected `standaloneCanonicalVector` files that correspond to the withdrawn grades `R-COUNT-CLASS-ATTEMPT` and `R-CODE-VS-DATA-MATRIX`.

Scope is the standalone vector plus raw retained Run properties. This is not a newly required whole-Run acceptance test, not whole-foundation ACCEPT, and not product qualification. Other Phase 4 grades retain prior scoped standing only; they are not automatically accepted by this recheck.

## Original clauses (full text, not labels)

Charter Phase 4 paragraph:

> Derive the complete registered relation/rung applicability table. Derive state-dependent count/class/attempt rules and apply them to retained scopes and Coverage even when no fact is present. Verify code-versus-data capability distinction against the published matrix and body/normalizer laws. Enumeration completeness is distinct from resolution completeness; do not invent a resolved rung for file facts. Every advertised mode must have a representable analysis path; document the chosen grammar.

Requirements for the two IDs under recheck:

| ID | Kind | Requirement | Observable |
|---|---|---|---|
| `R-COUNT-CLASS-ATTEMPT` | standaloneCanonicalVector | Apply state-dependent count/class/attempt rules to retained scopes and Coverage including fact-absent cases. | vectors applying the rules to scopes/Coverage with and without facts |
| `R-CODE-VS-DATA-MATRIX` | standaloneCanonicalVector | Verify code-versus-data capability distinction against the published matrix and body/normalizer laws. | matrix application cited on syntax Runs and a table vector |

The other three Phase 4 clauses were not re-executed. Their prior self-audit standing is unchanged and is not a blanket ACCEPT of the rest of the foundation.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-phase4-recheck.v1/output/phase4_recheck.py
```

Comparisons: `phase4-recheck-results.json`. Operands/owners: `phase4-owner-mapping.json`.

Claimed `ok`, claimed counts, and scalar flags were comparison targets only. Every admitted observable was re-derived from current kit law and the actual retained records.

## Exact input hashes

Successor `data-manifest.json` SHA-256 `0db360733a100cc56161de13389aa801f74d111b7b94b2c45a8925ce79c5017f` (945 bytes) matches the grant. Kit `consumer-input-manifest.json` SHA-256 `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8`. Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec`. Requirements SHA-256 `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495`.

| Path | SHA-256 | Bytes | Match |
|---|---|---|---|
| `foundation/code-vs-data-matrix.json` | `c7fc60d191e5b2a6043864374199827536144fb24ecef0be2ba0ac93a684c4cb` | 7293 | yes |
| `foundation/count-class-attempt.json` | `75fc228b6799a61a9e927682786c9b970f565d936d20dfb056e1f22f03e0e846` | 54020 | yes |
| `foundation/count-class-attempt.store.json` | `7b68f4a26b862cafa7ef9410cccf17551633516653db5d2ac2d3cde809387d58` | 428923 | yes |
| `runs/syntax-code.store.json` | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` | 889618 | yes (unchanged vs original foundation store) |
| `runs/syntax-data.store.json` | `2c4f195099c5a3edf303349c1fcc182d325d73d3a65913fdcc3fe9a585b3cc7e` | 490800 | yes (changed vs this origin's original store `00fce98f9683084563b1bf54e1119813fc97d670250e49fd7d56ad5fe57e5099`) |

No first-failure at hash verification.

## Prior finding dispositions

| ID | Self-audit | Now | Classification |
|---|---|---|---|
| `R-COUNT-CLASS-ATTEMPT` | withdrawn | **executed-pass, closed** | existing-law reconstruction of retained scopes and Coverage |
| `R-CODE-VS-DATA-MATRIX` | withdrawn | **executed-pass, closed** | existing-law reconstruction of published matrix cells and measured syntax-Run fields |

Neither withdrawal was a missing or contradictory kit recipe. The incompleteness was unexecuted original observables in the earlier standalone vectors. The successor records now retain those observables. This origin did not remint consumer records.

## `R-COUNT-CLASS-ATTEMPT` — executed-pass

Independent snapshot identity: `snapshot2:3547d9e93bf52f7900e712df6b96ec6658c57aba848bab68a8ebd2ec1e87a97e`. Schema stock of the snapshot record is empty.

Each of the six vectors retains a `subject-scope` record, a coverage envelope, and a `CoverageResultV3` payload. That is the object the original clause named. The earlier scalar `{relation, resolution, factsPresent, unresolvedEdgeCount, …}` shape is no longer the tested object.

Joins independently recomputed for every vector (claimed C/H not trusted):

- `scope.snapshotId` equals snapshot typedId
- `coverage.scopeId` equals independently hashed scope typedId
- `coverage.payloadDigest` equals `SHA256(C(payload))`
- `coverage.payloadSchemaDigest` equals SHA-256 of `native-evidence.schemas.v2.json` (`a87331bc…`)
- `payload.key.subjectScopeCommitment` equals `sha256:` plus independently hashed scope H
- `examinedUniverse.subjectCount` equals `len(subjects)`
- envelope/scope identities match claimed C/H/typedId
- snapshot, scope, coverage envelope, and payload blob are members of the retained count-class store
- fact C/H/typedId, `payloadDigest`, `payloadSchemaDigest` (relation-payload schema document `53380a24…`), and `snapshotId` join when a fact is retained
- file payload `path` / `contentSha256` / `byteLength` join snapshot `sourceInventory` and scope subjects when a file fact is retained
- RC-2 unresolved-edge count and `edgeKind` classes join `resolutionCompleteness` when unresolved-edge facts are retained

`CoverageResultV3`, `subject-scope`, coverage envelope, and fact schema stock are empty on all six.

| Vector | Facts | Independent RC | Notes |
|---|---|---|---|
| `file-enumerated-with-fact` | 1 file@enumerated | RC-1 `not-applicable`, attempted false | `src/a.ts` present in snapshot inventory |
| `file-enumerated-fact-absent-examined-missing-path` | 0 | RC-1 `not-applicable`, attempted false | subjects=`["absent.ts"]` **not** in snapshot; Coverage still complete / not-applicable |
| `file-enumerated-fact-free-empty-scope` | 0 | RC-1 `not-applicable`, attempted false | subjects=`[]`, `subjectCount=0` |
| `imports-resolved-zero-unresolved-complete` | 1 imports@resolved-target | RC-2 `complete` | measured unresolved-edge count 0 |
| `imports-resolved-unresolved-edge-incomplete` | 1 unresolved-edge@observed | RC-2 `incomplete` | measured class `unresolved-module-specifier`, count 1 |
| `imports-resolved-skipped-not-attempted` | 0 | RC-2 `not-attempted` | `attempted=false`, `stageTerminal=null` (schema allows null) |

RC-6 holds on every retained Coverage: `coverage=complete` is paired with `examinedExhaustive=true`. RC-6 does not require `resolutionCompleteness.state=complete`; the skipped and incomplete resolved-rung entries remain lawful.

Original clause execution, not claimed `ok`:

- fact-absent Coverage: yes (`fact-absent-examined-missing-path` and `fact-free-empty-scope`)
- RC-1 not-applicable on non-resolved rungs: yes
- RC-2 complete / incomplete / not-attempted on `imports@resolved-target`: yes

### notReached (preserved, not treated as executed refusals)

The vector lists two negative controls with **no** retained scope or Coverage records:

- `rc6-complete-coverage-without-exhaustive-examination` (claimed RC-6)
- `rc0-unregistered-pair-unresolved-edge-enumerated` (claimed RC-0)

Status: `notReached-as-retained-record-refusal`. Those refusals were not executed on retained bytes. They do not fail the ID, and they were not invented as replacement graphs. The six retained vectors already execute the original clause, including fact-absent Coverage.

## `R-CODE-VS-DATA-MATRIX` — executed-pass

Kit owners actually used (the prior withdrawal was that these were absent from the exhibit):

- `native-capability-matrix.v2.json` cells
- `native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry` `classLaw`
- `identity-schemas.v3.json#/$defs/body-language-version.properties.languageId.enum` `{typescript, javascript, rust}`
- framed body identity `opensip.fact-identity.v1` languageId (not a clones-payload JSON field)
- `SyntaxGrammarBundleV1.normalizer.specificationDigest`

Published matrix cells independently read from the kit, not from the vector flag:

| Cell | Kit state | Claimed state | Match |
|---|---|---|---|
| `clones-fact` × `syntax-only` | `SUPPORTED-DESIGN` (note: grammar-bearing languages only) | `SUPPORTED-DESIGN` | yes |
| `clones-fact` × `ts-tsconfig` | `SUPPORTED-DESIGN` | `SUPPORTED-DESIGN` | yes |
| `inventory` × `syntax-only` | `SUPPORTED-DESIGN` | `SUPPORTED-DESIGN` | yes |

Grammar registry `classLaw` and code/data language lists match the kit. `json` is not in the BLV enum. `clones@normalized-body-hash` is a typescript capability and is not a json capability.

### Measured syntax-code store (raw properties, not Run admission)

- context domain `native.context.syntax.v2`
- `selectedGrammarIds` = `["rust"]`
- grammar row `grammarId=rust`, `languageId=rust`, `syntaxClass=code`
- `languageId` is a BLV member
- normalizer `specificationDigest` `8fe22043ebe7e18a9c27b7a288f71b1010b024f040284d0eafab8659f8dd9d91`
- two clones facts at `normalized-body-hash`: `fact2:7dcdff1d…f344b8` (L0-verbatim) and `fact2:664472f8…1cb270` (L1-lexical)
- independently parsed body-identity frames: `languageId=rust` on both, in the BLV enum
- clones Coverage `coverage2:1504457d…ba77`: `coverage=complete`, `deficiency=null`, `nativeCause=null`
- file fact `fact2:852404c1…a717` remains `enumerated`

### Measured syntax-data store (successor bytes; raw properties, not Run admission)

- `selectedGrammarIds` = `["json"]`
- grammar row `grammarId=json`, `languageId=json`, `syntaxClass=data-document`
- `json` is **not** in the BLV enum
- zero clones facts
- clones Coverage `coverage2:b87610f3…573c37`: `coverage=unknown`, `deficiency=language-tier-unsupported`, `nativeCause=capability-missing`
- that is an unavailable disclosure, not a complete empty clone result
- file fact `fact2:97e82756…ce95ac` remains `enumerated`

Original clause on **measured** fields, not on `ok` and not on application prose: code grammar bears clones and a BLV languageId; data-document grammar does not enter the clone preimage and discloses clones as unavailable.

### Should-issue (does not refuse the ID)

`application.syntax-code` says “selected typescript code grammar”. Independently measured `selectedGrammarIds` is `["rust"]`. Classification: claimed-prose mismatch, not an oracle, not missing law. Rust is a lawful code/BLV language. The original clause was evaluated on the measured store fields. Finding `FD-SHOULD-CVD-APPLICATION-PROSE-TYPESCRIPT-VS-MEASURED-RUST`. Does not reopen the withdrawal.

## Other Phase 4 standing (not re-run)

| ID | Prior self-audit | This recheck |
|---|---|---|
| `R-RELATION-RUNG-TABLE` | stands | prior scoped standing only |
| `R-ENUM-VS-RESOLUTION` | stands | prior scoped standing only |
| `R-ADVERTISED-MODE-PATHS` | stands | prior scoped standing only |

Trace successor recheck remains historical (`TRACE_DATA_ADMITS`). Phases 0–3 were not reopened.

## Missing vs contradictory vs reconstruction

No missing or contradictory kit recipe for these two clauses. No existing-law reconstruction error on the retained records. The two prior withdrawals close as existing-law reconstructions now that the successor vectors retain scopes/Coverage and measured matrix/body/normalizer fields.

First failure: none. notReached: the two negative controls without retained records, preserved.

## Limitations

- Cited syntax stores and the count-class store are unverified for whole-Run admission/replay.
- Negative RC-0/RC-6 controls have no retained Coverage/scope records.
- Other foundation IDs were not re-run.
- S-\* author-process custody remains external from the prior review.
- Consumer input records were not repaired or reminted.

No whole-foundation ACCEPT. No product qualification.

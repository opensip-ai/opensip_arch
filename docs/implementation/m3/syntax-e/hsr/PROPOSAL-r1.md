# Historical schema readers: proposal HSR r1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted. Not code.** Law for the identity owner's **historical schema readers**, the lead's decision B on E2s's stop (overnight log, "E2s stopped before review, correctly"). It names one contract successor, **HSR-1**, one code unit, **HSR-a**, and re-scopes unit **E2s** of law M3-E1 (E1 item 20). This law touches no product file.

**Lead decisions.** LD-H1 to LD-H12 are lead decisions dated 2026-10-04. They are made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects, and the owner may reverse any of them. None needs an owner decision to proceed. Owner notes 1 to 3 flag what bears on the owner's data.

**Product.** Main `43ea32a` (X3c-3), read only. E2s stopped on `b7b87b7`. The two commits between them (I1-b1, X3c-3) change no file this law cites except `crates/evaluator/src/policy.rs`, whose cited lines are unchanged, and the design lock and `tools/verify_design.py` are byte-identical at both.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **STOP** | E2s's stop report, `scratchpad/e2s/stop-report.md` in the lead's session scratchpad (3,613 bytes) | `8ebe1307…` |
| **E2S-D** | E2s's unfinished diff, `git diff b7b87b7` in worktree `/Users/sb/code/opensip-ai/opensip-e2s` (26 files, +480 −86) | `6b8fe118…` |
| **E1** | `docs/implementation/m3/syntax-e/PROPOSAL-r5.md`, M3-E1 r5, accepted by GROK2 | `3b9eae37…` |
| **M3P10** | `docs/implementation/m3/M3-PLAN-r10.md`, accepted by Codex | `ec8c38f8…` |
| **I1** | `docs/implementation/m3/preview-pack-i1/PROPOSAL-r3.md`, M3-I1 r3, accepted by CODEX2 | `204f8ee8…` |
| **I1L** | `docs/implementation/m3/preview-pack-i1/i1-l/successor.json`, bound (35,443 bytes) | `9c490137…` |
| **SYN1 / SYN1F** | the READMEs `syntax-e/syn-1/README.md` and `syntax-e/syn-1f/README.md`; both units bound, at `682991f` and `218465f` | `b97ba9b5…`, `c17a08d9…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes) | `c82404f3…` |
| **IDS** | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`, the selected identity schema bundle (200,510 bytes) | `73645b76…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes) | `83b99783…` |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (133,335 bytes) | `1ee203e3…` |
| **SS2** | `docs/implementation/m1/source-selection-v2/README.md`, in force through source-selection-v3 | `2c90c4da…` |
| **ARS1** | `docs/implementation/m2/admission-runtime-selection-v1/README.md`, bound | `d0d543dd…` |
| **MH** | `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, M3-H r3, accepted by Grok | `7a562720…` |
| **VD2** | `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, accepted by Codex | `2e4f70b4…` |
| **ON** | the overnight log, `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry | live file |

Product paths are at `43ea32a` unless marked. The precedents for HSR-1's form are SD-7 and SD-8, REG v3, CRC-2 and ENUM-1.

## Acceptance gate

This law and HSR-1 may be reviewed and accepted now, together.
- **Neither needs a build.** The evidence is Python only: HSR-1's build, check and binding scripts.
- **HSR-1 binds** in a binding-only product commit after this law is accepted (HSR-1 README, LD-5).
- **HSR-a launches** once HSR-1 is bound. **E2s integrates** after HSR-a (item 15).
- **No owner decision is needed.** The contracts permit historical readers and already plan for them (item 2).

## Decisions at a glance

| # | Decision | Rejected |
|---|---|---|
| 3 | **Historical schema readers (decision B).** A retained record is admitted against the exactly selected earlier bytes of its schema document, by exact digest, from a closed table. Nothing is re-minted. | re-deriving the 12 corpora (A); rewriting their digests (C); leaving stores broken; a new major; a version-fallback reader; reading old records with the current bytes |
| 4 | **The table is declared in IE,** at the end of the payload registry section, by exact digest and bytes. Two rows: H1, the native evidence schemas at `e5834d37…`; H2, the enumeration plan schema at `10627cb6…`. | a new IDS member; a standalone registry with a `verify_design` extension; admission-registry rows; a table in code only |
| 5 | **Minting names the current bytes. Retained reads use the table.** The host chooses a new record's digest. Retained closure, replay and every check of a retained record admit the current digest or a table row of the same document, against exactly those bytes. The retained schema blob is still required. | an input-set or per-Run mode; owner joins that refuse historical digests; validating against the current bytes; a compiled reader standing in for a missing blob |
| 6 | **One reader per digest.** A row whose digest is still an implementation's current digest is read by the current reader there. | refusing such a row, which forces E2s and HSR-a into one commit |
| 7 | **Identity, mixed stores, verification.** Stored identities stand. One store and one Run may mix readers. No defect, field or code is added. | a disclosure field; a doctor defect for old records |
| 8 | **Extension:** one row per retired digest, by the successor that retires it, through a VD2 supersession of IE:808. Rows are never removed. | a blanket rule with no rows; batching rows later; pruning old rows |
| 9 | **HSR-1:** a VD2 supersession of I1-L's IE:214 (the second reviewed exception, for SYN-1 and SYN-1F); plain overrides of IE:662, IE:678 and IE:808; plain overrides of two IDS strings. | leaving IE:214 contradicted; a complete IE or IDS copy |
| 10 | **S2:** E2s mirrors SYN-1's corrected rule sentence, byte for byte, in the three evaluator registries. | keeping "twelve"; a later unit; other wording |
| 11 | **No X9 or crash-matrix consequence.** | none needed |
| 13–15 | **Units:** HSR-a (identity readers, the evaluator's digest joins, constructors, two historical files; inventory) lands first, with dormant rows; then E2s, rebased, with S2 and new controls. | one commit for both; E2s first; rows added by E2s |

---

## A. The problem

**1. What E2s found (STOP; E2S-D).**
- **The change.** E2s materializes SYN-1 and SYN-1F (E1:825). It changes five product schema sources:

  | Source | Before (bytes, sha256) | After |
  |---|---|---|
  | `schemas/sources/native-v2.schema.json` | 280,357, `e5834d37…` | 280,738, `93a39da8…` |
  | `schemas/sources/enumeration-plan-v1.schema.json` | 19,975, `10627cb6…` | 20,005, `cc29483f…` |
  | `schemas/sources/execution-inputs-v1.schema.json` | 39,910, `604bd941…` | 39,940, `0c196cba…` |
  | `schemas/sources/subject-inventory-v1.schema.json` | 16,861, `6ab46925…` | 16,891, `34e49cd1…` |
  | `schemas/sources/identity-v3.schema.json` | 198,423, `eb6ec957…` | 198,461, `080a8522…` |

- **The product admits a retained record only on the compiled digest.** `RetainedInputs::registered_record_shape` refuses `PayloadSchemaDocument` unless the carried digest equals the compiled schema's (`crates/identity/src/closure.rs:575-592`). The payload-registry walk (`:1150-1230`), the schema-blob membership check (`:1497-1525`) and relation payloads (`:351-385`) compare the same way. The evaluator matches parameters and import payloads by raw sha256 against its registries (`enumeration_join.rs:105-120`, `policy.rs:497-512`, `import_joins.rs:105-115` and `:215-245`, `import_payloads.rs:77-95`), and the Coverage producer against `coverage-registry.json`'s one digest (`coverage.rs:318-330`, `:401-404`).
- **The Coverage id hashes the digest** (`coverage.rs:405-416`; IE:185). So would the `import2` id and, through `analysisSpecDigest`, the PlanId.
- **The failures.** On `b7b87b7` plus E2S-D, 66 tests fail: host lib 23, host `admission_tests` 10 (B0 to B8), security lib 8, storage lib 25. The errors are `PayloadSchemaDocument`, `EVALUATOR_PARAMETER_UNREGISTERED` and `MissingBlob(93a39da8…)`. All read 12 independently derived corpora: 11 host fixtures under `crates/host/tests/fixtures/` and `crates/security/tests/fixtures/journal-seal-cases.json`, which is X9's run-candidate corpus (`crates/storage/src/crash_matrix_support/run_candidate.rs:30`). X3c-3 has since added storage commit tests over the same candidate.
- **Only two digests are carried.** HSR-1's check script shows that the 12 corpora carry `e5834d37…` (all twelve) and `10627cb6…` (ten of them), and that none carries a digest of the other three changed sources. Item 4 gives the reason on the text.
- **Real stores (record).** STOP and ON say that Runs already retained in the owner's real stores would be refused. As far as the product source shows, no build can write a Run today: the CLI admits only `doctor`, `help`, `version` and `completion`, and refuses default analysis ("Default analysis is not implemented in this development build", `apps/cli/src/arguments.rs:103-105`). So the break is real now for the 12 corpora, and it would be real for every owner store from the first analysis on, at this change and at every later one. The decision is the same either way (owner note 1).

**2. What the contracts already say.**

| Source | Text | Bearing |
|---|---|---|
| IE:10 | "Historical identifiers are never relabelled." | Re-minting old records is out. |
| IE:185 | `coverage2` hashes "scope, CoverageResultV3 payload and exact schema digest" | A schema change moves every new Coverage id, so old ids can only stand if old records are read as they are. |
| IE:213-214, with I1L's bound override | "Schema/domain changes require a new identifier major and reviewed migration, not a permissive parser." I1's one exception ends: "So every existing record keeps its bytes, identity, validity and replay result … Every other schema or domain change keeps this rule." | SYN-1 and SYN-1F add `source-parse-error` under the existing majors (E1:806). No reviewed exception covers it, and it is the first such change that moves a digest retained records carry. That is the gap. |
| IE:661-662 | `payloadSchemaDigest` is the SHA-256 "of the exact full bytes of the document the row names" | Read today as the selected bytes only. |
| IE:678 | `view.schemaDigests` names documents on the closed registry; anything else refuses `SCHEMA_DOCUMENT_UNREGISTERED` | Same. |
| IE:1089; IE:1324-1325 | "Historical Runs keep their earlier custody-only reading"; "Historical closures, Plans and Runs keep their bytes and are not re-read under this law." | Old records are read by their own rules. |
| SS2:20-28 | "Historical documents with the same URI remain distinguishable by their raw schema digest and retained descriptor. An old URI or major alone never authorizes a new interpretation. Do not remint historical Run, evidence, coverage or Plan identities. Current producer dispatch uses the selected schema bytes. Historical readers use the retained exact descriptor and compatible owner" | The accepted source selection plans historical readers, keyed by exact digest, and forbids re-minting. |
| ARS1:9 | "Historical native and policy documents with the same schema ID are refused as current sources. This helper does not implement the separate retained historical reader." | The reader is owed, and it is not an admission source. |
| `schema_registry.rs:1-2`, `:564`, `:617-618`; its inventory description | "never interprets historical bytes by alias"; "Same-URI historical bytes never acquire current interpretation by version fallback"; "historical readers and semantic joins remain separate" | The registry was built to keep the reader separate. |
| IDS `/x-opensip-evaluator-profile/majorLaw` | "Unchanged ancestors referenced by digest retain their existing identifier majors; their values change if committed input/schema bytes change." | New records under new bytes get new values; old records keep theirs. |
| NE:1939-1943 (§4 step 6) | "A caller may restate it but never choose it: a value that is not the registered document's digest refuses `native.coverage-payload-schema-not-registered`" | The minting rule. It stays. |

**Conclusion.** No passage forbids a historical reader that admits a record against the exact bytes its digest names. IE:214 forbids a permissive parser, and a version-fallback reader would be one; an exact-digest reader is not. SS2 and ARS1 plan the reader. What is missing is the reader itself, and a reviewed exception at IE:214 for SYN-1 and SYN-1F. This law supplies both. It needs no owner decision.

## B. The law

**3. Decision: historical schema readers (LD-H1).**
- **The rule.** The product keeps the earlier selected bytes of a schema document compiled in, by exact digest, as a **historical schema reader**. A retained record that carries a historical digest is admitted and replayed against exactly those bytes. Its stored identities are never recomputed under the new bytes. New records always carry the current digests. Nothing is admitted on any digest other than a selected current digest or an enumerated historical one.
- **The corpora stay byte for byte** and become the historical readers' proof. New tests cover current-digest records (items 13 and 14).
- **Rejected:**

  | Option | What it would do | Why not |
  |---|---|---|
  | **(A)** Re-derive the 12 corpora | regenerate the fixtures under the new digests | It helps no retained store. It changes X9's run-candidate input. The corpora have no generator, so re-deriving them through product code ends their independence. It recurs at every change. |
  | **(C)** Rewrite the corpus digests mechanically | replace the digest strings | Coverage, import and Plan identities hash the digest, so the rewrite must recompute them through product code: the same loss as (A), and the same X9 change. Stores stay broken. |
  | Leave stores broken | land E2s as it is | Every owner store would refuse its own Runs from the first change after analysis ships. It contradicts SS2:23 and IE:10. |
  | A new major | native evidence schemas v3, enumeration plan v2 | Old records still name the old bytes, so a reader of them is needed anyway. It also cascades majors and needs a migration, as I1:283-290 found for I1's member. |
  | A version-fallback reader | admit any digest whose `$id` matches | It is the "permissive parser" of IE:214, and SS2:22 forbids it. |
  | Read old records with the current bytes | accept listed digests, validate against today's bytes | A record must be read under the bytes it was admitted under. A later change need not keep every earlier annotation and reference. |
  | Keep the old digests in the evaluator registries | E2s's own probe | It fails at identity's comparison (STOP), and it would let new records name old bytes. |

**4. The carried documents and the closed table (LD-H2).**
- **Which documents are carried.** A retained record names a schema document by digest only through `payloadSchemaDigest`, an analysis-spec or stage-spec parameter's `schemaDigest`, a `view.schemaDigests` member or a `schema` proof-input-ref. Each names a document on IDS's payload registry (IE:655-678). A stage-spec's `outputSchemaDigest` names a member of a producer closure's tree instead, and a new output schema is a new closure (IE:1303-1325).
- **E2s's five documents.** Two are payload-registry documents: `native/native-evidence.schemas.v2.json` (the `coverage` row and the `dependency` and `prepared` import rows) and `foundation/enumeration-plan.schema.v1.json` (a `parameter` row). The execution inputs, subject inventory and identity schemas are not, so no record carries their digests and they get no row. They are read against the current bytes, which only add a member.
- **Where the table is declared.** In IE, as a new subsection, "Historical schema readers (contract successor HSR-1)", appended to IE:808, the payload registry section's last line. It is closed and names each row by exact digest and length:

  | Row | Document | `$id` | sha256 | Bytes | Accepted architecture copy | Retired by |
  |---|---|---|---|---|---|---|
  | H1 | `native/native-evidence.schemas.v2.json` | `urn:opensip:product-v1:native:evidence-schemas:v2` | `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773` | 280,357 | `docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json` | SYN-1 |
  | H2 | `foundation/enumeration-plan.schema.v1.json` | `opensip.product.enumeration-plan.1` | `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c` | 19,975 | `docs/implementation/m2/admission-runtime-selection-v1/schemas/sources/enumeration-plan-v1.schema.json` | SYN-1F |

  Each copy is in the lock's accepted set with exactly that digest, and is the copy the product's base source maps name. Neither document references another, so each reader's closure is its own bytes.
- **Rejected:**
  - **A new IDS member.** A JSON Pointer override changes one string and cannot add a member, so it needs a complete IDS copy, which forks the text CRC-2 and SYN-1F carry.
  - **A standalone registry document with a `verify_design` extension.** It is a second authority, and the VD change needs its own law and an F8c-style re-pin. The digests already bind the bytes (LD-H11).
  - **Admission-registry rows.** VD admits one source per `$id`, by design (ARS1:9).
  - **A table in code only.** It could grow without review.

**5. Minting and retained records (LD-H4, LD-H5).**
- **Minting.** A boundary that creates a record names the selected current bytes of each document, and only those. The host chooses the digest. A caller may restate it but never choose it (NE:1941-1943). This covers `admit_coverage_result_v3` (NE §4 step 6, which M3-H item 10 implements), import admission, pre-Plan analysis-spec admission, view production and every other boundary that creates a record. A historical digest there refuses with the boundary's existing refusal for an unregistered document.
- **Retained records.** Retained closure, replay, Run closure and every later check of a retained record admit the carried digest when it is either the selected current digest of the document its payload-registry row names, or a table row's digest for that document.
  - **Exact bytes.** The record is validated against exactly the bytes its digest names, through the registry row's selector. Every digest annotation and reference of that document is read from the same bytes. A reader never mixes versions.
  - **Retention is unchanged.** The store still retains the schema bytes under that digest. A compiled-in reader never stands in for missing retained bytes: absence stays retention loss.
  - **Re-applied producer laws.** The evaluator's view join re-runs the Coverage producer law over retained Coverage (`view_joins.rs:480-497`), and M3-H uses the same join at minting (MH item 10). A re-run over a retained record is a retained check: "the registered document" there is the version the record's own digest names. At minting, H names the current digest itself (MH item 10, step 1), so the join sees only current digests on H's path.
  - **Resolution comes first.** A digest resolves to its document before any registry row, key or cardinality rule applies. So a current and a historical digest of one document cite one row, and two parameters of one spec citing them refuse under the one-per-row rule (IE:730-752).
  - **Nothing else.** A schema `$id`, URI, major or version alone never selects a reader, and no caller, store, environment or configuration adds one.
- **Why enforcement sits at the minting boundary (LD-H4).** The owner joins are shared by minting and replay (MH item 10: "the same composition Run closure re-runs"). One Run may hold both readers' records (item 7). So the join cannot tell a new record from an old one by the input set, and only the boundary that chooses the digest knows. It already chooses it (NE step 6; MH item 10, step 1).
  - **Rejected: a minting or retained mode on the input set.** H's staging overlay holds new records beside retained ones, such as an import the new Plan selects. A minting-mode set would refuse those.
  - **Rejected: owner joins that refuse historical digests.** Replay would break.
- **Rejected for LD-H5:** validating historical records against the current bytes (item 3), and letting the compiled bytes cover a missing blob, which would turn retention loss into success.

**6. One reader per digest (LD-H7).**
- Every digest in the selected registry and in the table names exactly one document. No digest is read by two readers.
- **Dormant rows.** A row whose digest is still an implementation's selected current digest, because that implementation has not yet selected the retiring successor's bytes, is read there by the current reader. It is never a second reader. At `43ea32a` both H1 and H2 are dormant: the product still compiles `e5834d37…` and `10627cb6…` as current. E2s makes both active.
- **Rejected: refusing a row that equals a current pin.** HSR-a could then not carry H1 and H2 before E2s, and the two units would have to land in one commit (LD-H8).

**7. Identity, mixed stores and Runs, verification (LD-H12).**
- **Identity.** Nothing is re-minted. A historical record keeps its stored identifiers: `coverage2`, `import2` and `fact2`, its Plan's `analysisSpecDigest` and PlanId, and everything above them. Their descriptors carry the historical digest, so recomputing them from retained bytes gives the stored values.
  - **A historical Coverage's id** is its stored `coverage2:H("coverage", {schemaVersion: 2, scopeId, payloadSchemaDigest: e5834d37…, payloadDigest})`. The same payload admitted today gets `payloadSchemaDigest: 93a39da8…` and so a different id. The two are different records and are never equated.
  - **Findings still correspond.** `finding-key2` names no schema digest (IE:188), so comparison across the change matches findings as before.
- **Mixed stores and Runs.** Each record is read by the digest it carries. One store may hold both readers' records. So may one Run: a Plan created after E2s may select an import retained before it. Replay, Run closure and comparison need no mode, flag or per-store setting.
- **Verification and doctor.** A record admitted by a historical reader is admitted. No defect, field, code or class is added. A record whose digest is neither current nor in the table refuses with its existing refusal: in Run closure `PayloadSchemaDocument`, which replay already routes, and at the evaluator `EVALUATOR_PARAMETER_UNREGISTERED`, `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT`, `native.coverage-payload-schema-not-registered` or `SCHEMA_DOCUMENT_UNREGISTERED`. `opensip doctor` reads no Run today (law X10), so it says nothing new. Any later verify surface reports replay's result.
- **Rejected:** a `schemaReader` disclosure field, which needs a public-field successor against the owner's no-new-codes direction; a doctor defect for a historical record, since old data read correctly is not a defect.

**8. Extension (LD-H3).**
- **Who.** Only a reviewed contract successor of the identity owner changes the table, by superseding HSR-1's IE:808 override in VD2's form. VD2 keeps the chain linear, so there is one current table.
- **When.** A successor that changes the selected bytes of a payload-registry document adds exactly one row for that document: the digest it retires, its bytes, its accepted architecture copy and the successor's name. A successor that changes two such documents adds two rows, one each.
- **Never removed.** No row is removed or edited, and nothing else adds one.
- **Additive only.** The table keeps readable the records that carry a digest. A record that carries none is read against the current bytes, so an exception that is not purely additive still needs a new major and a reviewed migration (IE:214).
- **The code side.** The code unit that materializes the retiring change makes the row active by moving the current pin. The code unit that adds a row compiles its bytes and a test that the compiled table equals the contract's.
- **Rejected:** a blanket rule that keeps "all earlier versions" with no rows, which is unreviewable; batching rows later, which leaves a window of refused records; pruning rows after some releases, which would refuse records still retained.

**9. Contract successor HSR-1 (LD-H6).** HSR-1 (`hsr/hsr-1/`, reviewed in this request) carries items 3 to 8 as identity text. Every target line was checked against the product lock at `43ea32a`:

| # | Kind | Parent | Selector | Current meaning | Change |
|---|---|---|---|---|---|
| 1 | **supersession** (VD2) | IE | line 214 | I1L's override (lock index 77) | I1's exception text, verbatim. Before its last sentence, a **second reviewed exception**: SYN-1 and SYN-1F's single additive `source-parse-error`, under the existing majors and without migration, whose earlier bytes stay readable as historical readers. The last sentence stays, and one sentence states the extension rule. |
| 2 | override | IE | line 662 | raw | `payloadSchemaDigest`: the selected current bytes or, for a retained record only, a historical reader's bytes |
| 3 | override | IE | line 678 | raw | `view.schemaDigests`: the same, for a retained view |
| 4 | override | IE | line 808 | raw | the new subsection: the table and items 5 to 8 |
| 5 | override | IDS | `/x-opensip-payload-registry/law/payloadSchemaDigest` | raw | the same rule, the minting rule and the resolution order |
| 6 | override | IDS | `/x-opensip-evaluator-profile/majorLaw` | raw | a sentence beside I1's: the second exception keeps every major |

- **Why the second exception belongs here (LD-H6).** SYN-1 and SYN-1F were accepted as native and foundation successors, and neither addressed IE:214 (SYN1, SYN1F "Consequences for E2s"). Under I1L's text, "Every other schema or domain change keeps this rule" now contradicts a bound change. The identity owner closes that here, in I1's own form, and states what makes this exception different: it moves a carried digest, so it needs the reader.
  - **Rejected: leaving IE:214 as it is.** The selected identity contract would forbid what SYN-1F's bound copies already do.
  - **Rejected: a new major for SYN-1's member.** Item 3.
- **Untouched, with reasons** (HSR-1 README): NE §4 step 6 and NE §7.2 (the minting rule and the digest preimage, both still true); WS:490; IE:641-643; IDS's `registered-schema-document` strings; every product copy (CRC-1 LD-7, CRC-2 LD-4); the admission registry and `verify_design`.
- **Evidence.** HSR-1's scripts build the record deterministically, check it independently, and bind it on VD in a throwaway worktree with every refusal probe. The review request pins the results.

**10. S2: the rule sentence in three registries (LD-H9).**
- **What.** `coverage-registry.json#/deficiencyCause/deficiencies/input-closure-incomplete/rule`, `enumeration-registry.json#/causes/input-closure-incomplete/rule` and `execution-registry.json#/causeRegistry/input-closure-incomplete/rule` (all under `crates/evaluator/src/`) each carry native-v2's old `allowedCauses` rule string verbatim, "…which is why section 10 lists twelve of them…". SYN-1 changed native-v2's string to "thirteen" and named `source-parse-error` (SYN-1's product copy, line 49). E1 item 20's E2s row lists only cause-list selectors, so E2s left the three strings alone (STOP, S2).
- **Decision.** E2s mirrors SYN-1's corrected string byte for byte at those three selectors, and E2s-T1 checks each equals native-v2's selected string.
- **Why.** After E2s, "twelve" is false in shipped registries that state the same rule as the schema, and each copy was verbatim. Mirroring keeps one text for one rule.
- **Rejected:** keeping "twelve"; a later unit, which reopens the same three files in the same lane; any wording other than SYN-1's.
- **Scope.** The strings are annotation that no code dispatches on, and they are carried by no record. The change moves no digest any record carries.

**11. X9 and the crash matrix: no consequence.**
- **The corpus.** `journal-seal-cases.json` stays byte for byte. The synthetic run candidate is built from it exactly as before (`run_candidate.rs:1-20`). After E2s it is admitted through H1 and H2 on replay, which is a retained check (item 5), so `replay_run` and `prepare_commit` see the same records and identities.
- **The candidate builder is not a minting boundary.** It is labelled synthetic test support in storage's `crash_matrix_support` (X9 r1 item 6). It rewrites only the ProjectId, the evaluator closure and the identities that depend on them, and keeps the corpus's records and digests, which replay then reads as retained.
- **Unchanged:** every kill point, driver, label, census, required-runs file, timing guard and evidence record of X9; the M2 completion record. HSR-a and E2s add no kill point and change no commit, custody or recovery logic. HSR-a changes storage's registry constructor only to pass the historical sources.
- **No lead-set rerun.** The ordinary lanes run every test over the X9 corpus (host B0 to B8, storage commit tests, security seal tests), and they are the proof. HSR-a records the registry construction time before and after (item 13), because every crash-matrix child builds the registry.
- **No X9 revision is needed.**

## C. Units

**12. Units at a glance.**

| Unit | What | Review | Size |
|---|---|---|---|
| **HSR-1** | contract successor (item 9) | ACCEPT-DESIGN-UNIT, with `supersededPassages` (Grok, this request) | design only |
| **HSR-a** | the identity reader set, the evaluator's digest joins, the registry constructors, two historical files and the tests (item 13) | ACCEPT-UNIT with `inventoryCandidateAssessment` | M, 2 days |
| **E2s** | as E1 item 20, rebased onto HSR-a, with S2 and E2s-T3 to E2s-T5 (item 14) | ACCEPT-UNIT, its own contract record (E1 item 20) | M, 2 days (mostly built) |

**13. HSR-a: the identity-side reader set.**
- **Identity** (`crates/identity/src/schema_registry.rs`):
  - a closed `HISTORICAL_READERS` table equal to HSR-1's rows: document, `$id`, product path, bytes and sha256;
  - construction from the current sources and the historical sources, both positional and closed. A historical source is length- and sha256-checked like a current one. Its `$id` must equal the current source's for the same document, and it must hold no external reference. Each active row compiles as its own program, whose closure is its own bytes. A dormant row (item 6) compiles nothing;
  - a resolver from (document, digest) to a reader, for retained joins, and a current-digest accessor, which is the only digest a minting boundary may name;
  - every digest maps to exactly one document, checked at construction.
- **Identity's retained joins** (`closure.rs`): `registered_record_shape` (`:575-592`); the payload-registry walk, including the `parameter` row match by resolution (`:1150-1230`); `registered_schema_blob` (`:1497-1525`); relation payloads (`:351-385`), through the same resolver though no row exists for that document today; `foreign_record` (`:1107`) and `foundation_digest_law` (`:1235`), which read the carried digest's own reader.
- **The evaluator's digest joins** resolve digests through identity instead of comparing raw sha256: `enumeration_join.rs:105-135`, `policy.rs:497-522`, `import_joins.rs:105-115` and `:215-245`, `import_payloads.rs:77-105`, and the declared digest in `coverage.rs:309-416`, where `None` still names the current digest. The registries keep naming the current digest only, and a drift check holds each registry's `sha256` and `nativeSchemaSha256` equal to identity's current pin.
- **Constructors.** `crates/host/src/schema_sources.rs` and `crates/storage/src/schema_sources.rs` embed and pass the historical sources. No production constructor builds a selected registry without them.
- **Files.** Two new files, `schemas/historical/native-v2.e5834d37.schema.json` and `schemas/historical/enumeration-plan-v1.10627cb6.schema.json`, byte-equal to H1's and H2's copies. They are outside `schemas/sources/` and outside every source map. They are not rows of `tools/contracts/generator-closure.json`, so HSR-a takes no generation slot. Its request shows the drift gate reporting `changed: []`, and HSR-a stops if it reports anything else.
- **Binding by digest (LD-H11).** `verify_design` is unchanged. A file whose sha256 equals the table's digest is those bytes, and construction refuses any other. A test asserts the compiled table equals HSR-1's rows, literally.
  - **Rejected:** a `verify_design` extension now (item 4); copying the files into `schemas/sources/`, which the source maps and the admission registry would then have to list, and VD refuses duplicate `$id`s there.
- **Inventory.** An inventory successor, with its number assigned at launch after checking `git ls-files`, adds the two files and gives `schema_registry.rs` a true description. Its current one ends "historical readers and semantic joins remain separate", which HSR-a makes false. `tools/identity/dependency-policy.json` re-pins identity's local sources, as E2s does.
- **The one minting-shaped corpus test (LD-H10).** `native_owner_tests.rs:818`, `coverage_producer_recomputes_scope_and_preserves_rc3_rc4_rc6`, feeds the corpus's 15 producer cases to the Coverage producer. Fourteen declare no digest, which means "the current one". After E2s that would name `93a39da8…`, whose bytes the corpus does not retain (STOP's `MissingBlob`), and the expected Coverage ids, which hash `e5834d37…`, would no longer follow. HSR-a re-points the test to the retained re-check: each case declares H1's digest, as Run closure does over retained Coverage (`view_joins.rs:485`), and every expected value stays. Before E2s, H1 is dormant and the run is identical. After E2s, H1 is active and the same expectations hold.
  - **Rejected:** editing the corpus; deleting the test; a test seam that mints under a historical digest.
- **Measured.** `embedded_schema_registry()` and storage's `registry()` construction time, before and after, on this host, with E2s's materialization applied in scratch (HSR-T10).
- **Controls:** HSR-T1 to HSR-T10 (section D).
- **Gate.** HSR-1 bound. Built on main after the binding commit.

**14. E2s, re-scoped.**
- **Integration edge:** HSR-a. E2s rebases onto HSR-a's commit and re-freezes. Its schema-registry pins, identity dependency-policy pins and contract record are rebuilt on HSR-a's bytes.
- **Scope, unchanged:** E1 item 20's selectors, generated carriers and design-lock record.
- **Scope, added:** S2's three `rule` selectors (item 10).
- **Not E2s's:** reader code, the historical files and the producer-test re-point. They are HSR-a's.
- **Controls:** E2s-T1 (extended) and E2s-T2, as E1 item 20 states them; E2s-T3 to E2s-T5 (section D).
- **Gate.** HSR-a integrated. E2s still finishes by day 12 at the latest (E1:848; M3P10:534).

**15. Order (LD-H8).** HSR r1 and HSR-1 accepted → HSR-1 binding-only commit → HSR-a integrated → E2s rebased, reviewed and integrated → E3, as before.
- **Why HSR-a first.** Every main commit stays green. HSR-a lands with H1 and H2 dormant. It changes no existing test's outcome, and the one test it re-points passes before and after. E2s then moves the current pins, and the 66 tests and every later corpus test pass with the corpora unchanged.
- **Rejected:**
  - **One commit for both.** It mixes two review subjects, one of them in the generation lane, which E1 item 20 keeps as its own candidate.
  - **E2s first.** That is the blocker: 66 failures, and stores refused.
  - **HSR-a with an empty table and the rows added by E2s.** It moves reader code and new files into E2s's generation-lane candidate, and E2s would then need an inventory.
- **Schedule.** HSR-a (2 days) fits before E2s's day 12. E3 stays on day 14 with its slack (M3P10:535), and the 33-day critical path does not move (M3P10:564).

## D. Controls

| # | Unit | Case | Expected |
|---|---|---|---|
| HSR-T1 | HSR-a | The compiled table equals HSR-1's rows (document, `$id`, sha256, bytes). An absent, extra, reordered, replaced or truncated historical source. | equal; each malformed set refuses construction, as for current sources |
| HSR-T2 | HSR-a | Partition: every digest names one document. A row with another `$id`; a historical document with an external `$ref`. A row equal to its current pin. | both malformed rows refuse construction; the equal row is dormant, read by the current reader |
| HSR-T3 | HSR-a | Retained admission over a test-only registry (synthetic documents: version B0 and a widened B1; `cfg(test)` constructor, unreachable from production): a record carrying B0's digest; a value valid only under B1 carrying B0's digest; an unlisted digest | admitted against B0; `Mismatch`; refused as today |
| HSR-T4 | HSR-a | Minting: the current-digest accessor; `inspect_coverage_producer` with `None`; a minting caller naming an active row's digest (synthetic) | current pin only; names the current digest; refused with the existing refusal |
| HSR-T5 | HSR-a | Identity (synthetic): a historical Coverage's recomputed `coverage2`; the same payload under the current bytes | equals the stored id; a different id |
| HSR-T6 | HSR-a | Resolution before cardinality (synthetic): two parameters citing a current and a historical digest of one document | refused (`ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS` in the import join, `EVALUATOR_PARAMETER_DUPLICATE` in the parameter joins) |
| HSR-T7 | HSR-a | Retention (synthetic): a historical record whose store lacks the schema blob | evidence missing naming that blob; never admitted by the compiled reader |
| HSR-T8 | HSR-a | Every production constructor of the selected registry (host, storage) | supplies the historical sources (source pin) |
| HSR-T9 | HSR-a | Its own commit: the full lanes, with every corpus byte-unchanged; the re-pointed producer test | pass; the test reproduces every expected value |
| HSR-T10 | HSR-a | Scratch proof against E2s: HSR-a's candidate with E2s's materialization (E2S-D, rebased) applied on top, uncommitted, in a throwaway worktree; host, security and storage lanes | every test over the 12 corpora passes; the corpora are byte-unchanged; H1 and H2 are active; construction time recorded |
| E2s-T1 | E2s | E1 item 20's selector mirror check, plus the three `rule` strings | each `rule` string equals native-v2's selected string |
| E2s-T2 | E2s | as E1 item 20 | as E1 item 20 |
| E2s-T3 | E2s | Historical proof: H1 and H2 active; every test over the 12 corpora; each corpus's sha256 | active; pass; equal to its `43ea32a` bytes |
| E2s-T4 | E2s | Current digests, with new test values not derived from the corpora by product code: a Coverage minted with `None`; a `source-parse-error` Coverage under `input-closure-incomplete` at `93a39da8…`, and the same claiming `e5834d37…`; an enumeration-plan parameter citing `cc29483f…` | names `93a39da8…`; admitted, and `Mismatch` (H1's enum lacks the member); admitted |
| E2s-T5 | E2s | Mixed: one retained view naming an H1 Coverage and a current Coverage | the view join passes; each Coverage keeps its id |

## E. Forbidden substitutes

- Selecting a reader by schema `$id`, URI, major or version alone.
- Validating a historical record against the current bytes, or a current record against a historical reader.
- Re-minting, recomputing or rewriting a retained record's identifiers or digests, in a store or in a corpus.
- Regenerating, re-deriving or mechanically rewriting any of the 12 corpora, X9's included.
- A reader row that is not in IE's table, or one added by code, configuration, environment, store contents or a caller.
- A compiled-in reader standing in for schema bytes missing from the store.
- A minting boundary that names a historical digest, through a default, a provider claim or a test seam reachable in production.
- A per-store or per-Run legacy mode or flag.
- Removing or editing a row once bound.
- Counting a current and a historical digest of one document as two registry rows.
- A production constructor of the selected registry without the historical sources.
- Listing historical documents as admission or generation sources.

## F. Cross-law items

| # | For | Item |
|---|---|---|
| X-HSR-1 | **E1's next revision** | Item 19 gains HSR-1 (identity owner; needed before HSR-a; it records the second IE:214 exception for SYN-1 and SYN-1F). Item 20's E2s row gains the HSR-a edge, S2's three `rule` selectors, E2s-T1's extension and E2s-T3 to E2s-T5, and notes that the producer-test re-point is HSR-a's. E1 r5 has no item 21. |
| X-HSR-2 | **M3-PLAN's next revision** | Law HSR and successor HSR-1; unit HSR-a (M, 2 days; identity; inventory number at launch; no generation slot, item 13); edges HSR-1 → HSR-a → E2s; E2s still by day 12 at the latest; E3 on day 14; the 33-day path unchanged. It records owner note 1's fact. |
| X-HSR-3 | **M3-H, M3-C and the import owner** (record notes; no accepted text changes) | Each already has the host choose the digest it mints: MH item 10 step 1 ("the registered NES document's digest and never a caller's"); C's pre-Plan analysis-spec admission and Plan construction; import admission. Read "registered" as the selected current digest, from identity's current-digest accessor. Each unit's controls gain one case: a historical digest refused at its minting boundary. |
| X-HSR-4 | **Every later successor** that changes the selected bytes of a payload-registry document | It supersedes HSR-1's IE:808 override and adds one row per retired digest, and its code unit compiles the row. For example, E1's PY-REG changes the native `languageId` enum (E1 item 19), and any native evidence schema successor of M3-L or M3-H would do the same. |
| X-HSR-5 | **ENUM-1** (record) | ENUM-1's description overrides live on SYN-1F's design copy only, and the product copy stays SYN-1F's bytes. Materializing them would move `cc29483f…` and need a row. No unit plans it. |
| X-HSR-6 | **Later IDS copies** | Any later complete identity-schema copy carries HSR-1's two strings in place (HSR-1 README, cross-law item 1). |

## Owner notes (FYI; none blocking)

1. **No real store holds a Run yet, as far as the product source shows.** The CLI refuses default analysis (`apps/cli/src/arguments.rs:103-105`). So today's break is in the 12 test corpora. Without this law, the same break would hit every owner store at the first schema change after analysis ships. With it, retained Runs stay readable across every such change. This corrects the overnight log's "runs already retained in your real stores would be refused on replay".
2. **The product keeps retired schema bytes.** About 300 KB now (H1 and H2), and one more document version per later change to a payload-registry document.
3. **This is a reversible lead decision** on the owner's data path (ON, "Lead decision: historical schema readers").

## Questions for the reviewer

- **Q1 (contract fit).** Do IE, SS2, ARS1 and the bound successors permit an exact-digest historical reader, and is a second reviewed exception at IE:214 the right way to close SYN-1 and SYN-1F's gap (items 2 and 9)?
- **Q2 (the table).** Is it closed, exact and correctly limited to the two carried documents, and is the extension rule enforceable through VD2 (items 4 and 8)?
- **Q3 (minting and retained).** Is "the host names the current digest at minting; retained checks read the table" sound, including the re-applied Coverage producer law, mixed Runs and resolution before cardinality (items 5 to 7)?
- **Q4 (units and order).** Are HSR-a's sites and controls complete? Is HSR-a first with dormant rows right? Is the producer-test re-point honest (items 6 and 13 to 15)?
- **Q5 (S2 and X9).** Is mirroring the rule sentence right, and is there truly no X9 consequence (items 10 and 11)?

## Not claimed

- No product build, test or lane was run for this law. HSR-1's Python evidence is the only run.
- No owner store was inspected. Owner note 1 rests on the product source.
- No cross-release evaluator semantics: HSR covers schema bytes, not changes to evaluator code between releases.
- No migration of any store, and no disclosure of which reader read a record.
- No `verify_design` change, and no change to the generation lane.
- No change to X9 or the M2 record. E1's E2s row changes only through E1's next revision (X-HSR-1), and I1's exception text survives verbatim.
- No count of today's corpus tests. The 66 are STOP's, on `b7b87b7`. HSR-T10 and E2s-T3 count them at the base they run on.

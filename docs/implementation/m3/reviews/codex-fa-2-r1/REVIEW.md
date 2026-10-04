**FA-2 r1 — REQUIRED-FINDINGS**

Codex reviewed the exact pinned FA-2 subject. Two required findings correct scope that is broader than LD-F6 and the TS2/Rust3 carrier. The carrier, two-phase commitment recipe, host projection, bounds/state choices, inherited-key correction and successor structure otherwise have no required finding. Exact replacements below change no wire design.

Subject manifest: `docs/implementation/m3/native-successors-fa/fa-2-subject.json`, SHA-256 `c339f4fbc24d233183adbd955ff76144fe0d916a9e7992b4417e8b3e840cb7b8`.

Successor: `docs/implementation/m3/native-successors-fa/fa-2/successor.json`, **38623 bytes**, SHA-256 `cac9b7d6326dfc1764b599758e9e82a4378f9485a89f4d21ccf555d7b2406ca7`.

The 40 supplied pins matched. Product HEAD was `cd5958b3608f44a0035566c9d4500e5005c62e91` (I1-P, lock only). H r1 and L r3 were treated as context/obligation, not accepted authority; the draft unit record was not part of the subject.

**Required findings**

**FA2-R1-01 (P2)** — `docs/implementation/m3/native-successors-fa/fa-2/successor.json:78 (NE:1927 after); docs/implementation/m3/native-successors-fa/fa-2/evidence/build_fa2.py:157; docs/implementation/m3/native-successors-fa/fa-2/README.md:211`

The insertion into the generic §4.1a admission recipe sends every symbol-kind key to a census admitted under §9.8. That includes syntax-universe symbol keys, although §9.8 only supplies the TS2/Rust3 worker carrier and expressly leaves the in-host syntax census unaffected. The adjacent NE:1913 insertion has the correct TypeScript/Rust qualification; step 1 loses it. An implementation following step 1 literally would require a worker-carried census for in-host syntax admission.

Evidence:

- successor.json's NE:1927 after says '(for a `symbol`-kind key, the census admitted under §9.8)' without a universe restriction.
- The NE:1913 after explicitly says 'of a TypeScript or Rust universe'.
- section-9-8.md:3-11 scopes the carrier to TypeScript or Rust providers; line 112 says the in-host syntax census needs no carrier and is unaffected.
- Accepted NE §1.2:253-258 retains syntax-only CoverageResultV3 claims; §4.1a defines their scope commitment with the Plan-bound enumerator and complete population, rather than making a TS2/Rust3 carrier a syntax prerequisite.

Restrict the NE:1927 insertion to TypeScript/Rust universes, update its generator and README summary, then regenerate the successor, subject manifest and pins. Keep the parent line and all other admission steps unchanged.

Exact replacement for `docs/implementation/m3/native-successors-fa/fa-2/successor.json; passageOverrides selector {line:1927}; after`:

```text
1. The host builds `D` from **its own** enumeration (for a `symbol`-kind key in a TypeScript or Rust universe, the census admitted under §9.8) and mints `scope2`. A provider-supplied
```

Exact replacement for `docs/implementation/m3/native-successors-fa/fa-2/evidence/build_fa2.py:157; inserted string for line 1927`:

```text
 (for a `symbol`-kind key in a TypeScript or Rust universe, the census admitted under §9.8)
```

Exact replacement for `docs/implementation/m3/native-successors-fa/fa-2/README.md:211; complete table row`:

```text
| 1927 | §4.1a step 1 | "its own enumeration" is, for a symbol key in a TypeScript or Rust universe, the census admitted under §9.8 |
```

**FA2-R1-02 (P2)** — `docs/implementation/m3/native-successors-fa/fa-2/README.md:266 (X-FA2-C)`

The cascade does not preserve LD-F6's scope. Clause (i) assigns the native worker closure to every available TS/Rust binding, including host-produced inventory bindings. Clause (ii) requires a worker for every universe with a symbol inventory, including syntax universes. LD-F6 and §9.8 instead constrain TS/Rust bindings that owe the worker's symbol census. The broader cascade conflicts both with host inventory ownership and with the same table's X-FA2-E1 statement that syntax universes have no child.

Evidence:

- README.md:121-125 restricts the shared enumerator to 'such bindings', meaning the expected symbol inventories bound to a worker's universe; section-9-8.md:24-31 states the same bounded rule.
- README.md:266 instead says 'every available TS or Rust binding' and 'Every universe'; README.md:265 says syntax universes have no child.
- Accepted M3-C r6:447 rejects a consuming language provider as producer when it did not produce the record; its full-admission rule at 881-882 separately recognizes host-derived file/package inventories and their host-internal origin.
- native-capability-matrix.v2.json:949 describes inventory as host discovery/enumeration output in every language mode. H1:521-545 and 685 route that ownership problem separately as X-H3; H1 is the pinned obligation/context, not acceptance authority.
- Accepted NE:3054-3059 states that producer and enumerator are not blanket-identical; FA-2's narrower symbol-worker case is compatible with that rule.

Replace the complete X-FA2-C row with the following bounded cascade. It narrows clauses (i) and (ii), and leaves the separately routed host-inventory ownership decision with X-H3. Re-pin README and the subject manifest.

Exact replacement for `docs/implementation/m3/native-successors-fa/fa-2/README.md:266; complete table row`:

```text
| **X-FA2-C** | M3-C's next revision (after r7) | (i) The enumerator of every available TS or Rust binding that owes a symbol inventory is that universe's worker provider closure, which also produces that worker's stages (LD-F6). This rule does not select enumerators for host-derived file/package inventories or for the inventory relations (X-H3). (ii) Every TS or Rust universe that an expected symbol inventory binds through an available binding has a worker; otherwise that inventory has no producer, and J2b's full join refuses it as `ENUMERATION_INVENTORY_MISSING_RECORD` (ENC:111). (iii) At Plan time the token is a "token the Plan needs" wherever a census is owed. | C4a |
```

**Decisions requested by REQUEST.md**

**1. Carrier and current majors are lawful; Complete is an appropriate chosen carrier.**

The owning successor explicitly negotiates new payload versions on existing Analyze/Complete frames, following target-attribution-v2 and EXC:270-272. F02:271-273's owning-surface successor requirement is met by this form after independent acceptance and root assent. No frame, transition, terminal, identity version or limits-map member changes. Complete yields one census per Analyze/universe and atomic admission with the settled candidate/Coverage stream. Rejected candidates are assessed separately below.

**2. D∅ followed by D_census preserves the one §4.1a / IE §3 recipe; the request equality exception is minimal.**

Both descriptors use the same closed subject-scope shape and H domain. Closure, snapshot, universes, relation and rung are fixed before execution; only the independently admitted census subjects arrive later. The returned Coverage payload commits the same digest as coverage2.scopeId, so no circular identity is introduced. Request relation/rung/universes, array position and ordinary key equality remain checked. Pre-Analyze, non-Complete clean terminals, over-bound returns and zero-row complete censuses use D∅ and subjectCount 0. The vectors reproduce NE's scope2 oracle and correctly separate UTF-8 row order from canonical-item ordering. Apply FA2-R1-01 to the generic recipe's scope.

**3. The wire/host split produces the SIS symbol record, with lawful EXC ownership.**

The provider supplies nativeSubjectId, path, qualifiedName, exported and signatureTokens. The host supplies the exact Plan locator, raw SHA-256 C(EnumerationPlanV1) parameterDigest, symbol kind, complete/null/null carrier, suffix-derived subjectLanguage and projections:[]. SIS explicitly represents unavailable detector projection by the empty array. Owner admission still checks schema, extent equality, row/locator validity and cross-locator equal rows before D and Coverage admission. The generated projection is schema-valid, but its labelled synthetic locator does not exercise a real Plan join.

**4. LD-F4 through LD-F6 are coherent within their declared scope; the cascade needs FA2-R1-02.**

No wire partial census is required by ENC:120: empty-known-row partial inventories are lawful, while clean BudgetExhausted/Unavailable already discard unsafely unsettled candidates and receive host-derived outcomes. Complete requires a complete population. The bounded over-bound variant avoids turning truthful population overflow into malformed-wire failure; projected SIS and D canonical-byte overflow separately take the same deferred X-H6 route. Its small counts-only payload adds no limit member. The symbol-worker enumerator constraint is a bounded case of the actual-producing-closure law, not a universal producer/enumerator equality. A missing needed token prevents spawn under existing §9.1. X-H6 and the Rust 256-subject-cap follow-ups remain separate owner gates.

**5. F-1 is real; LD-F7's every-key, commitment-only supersession is correct.**

DLV's keyConstruction and RequestedCoverageDomainV1.workerRule require the per-stage SubjectScopeV1 file commitment; RPP coverageDomainAlgorithm[3] has the corresponding fileScopeCommitment rule. §4.1a instead uses D with the key's own relation and resolution. One inherited stage commitment cannot satisfy two distinct key descriptors. Row C must therefore supersede those key-commitment clauses for non-symbol keys as well, irrespective of negotiation, while preserving SubjectScopeV1, subjects, analysisDomain, domainCommitment and commitments.subjectScope as the inherited transport/file-set proofs. It also expressly supersedes DLV normalSuccess's full-key echo only to the stated return rule.

**6. Structural exactness and schema/copy consistency pass; two scope statements are not true at their current breadth.**

The permitted script reproduces all nine generated files and verifies every before value against the exact parents. Thirteen NE insertions and six startup string overrides preserve inherited text; the paired handshake copies contain exactly the listed token/description/maxItems/supersedes/wire-law edits, and both census copies are identical. No additional schema defect was found. All 14 supplied schema cases passed. The two required findings concern semantic scope, not a pin or generation failure.

**7. No further normative carrier/key/token contradiction was found; the executable references remain limited evidence.**

The NE §0 rows explicitly supersede the DLV/RPP payload names and key clauses and extend the registered CapabilityToken only for handshake arrays. The registered native schema bytes and payloadSchemaDigest remain unchanged; new Analyze stage arrays name inherited selectors rather than invent a second contract. FactBatch's target-attribution laws remain independent of this terminal carrier. Existing no-token native cases and abstract event/transition models remain historical controls. The references' old handshake source and unconditional wrapper key comparison are recorded as FA2-N1-01; they do not verify new negotiated behavior.

**8. The successor is structurally compatible with the three inspected locks; acceptance/assent are still pending.**

At e093e90, 15c0779 and cd5958b all five parents are accepted at pinned bytes; copied parents have no bound override, FA-2's selectors are unbound, candidate paths are fresh and the 10 candidate members equal the 11-member subject minus successor.json. B-S1's eleven NE selectors are disjoint. Static inspection of the real contract_successor/successor_chain routines found no additional structural issue. The current DRAFT unit is not acceptance or root assent. This REQUIRED-FINDINGS review does not permit selection; a corrected re-pinned subject needs its own accepted review and matching assent.

**Carrier and other rejected candidates**

| Candidate | Review ruling | Reason |
|---|---|---|
| 1 | Chosen carrier is lawful and appropriate. | Negotiated Analyze requests the closure and Complete carries one complete population at atomic settlement. |
| 1a | Agree with rejection as a design choice, not as an inherently illegal extension. | Per-stage Coverage adds repetition/designation and terminal payload variants without improving population admission. |
| 1b | Agree with rejection. | FactBatch's candidate batching and independently negotiated attribution versions are a poor census lifetime/cardinality fit. |
| 1c | Agree with rejection under current lifecycle. | NativeContextVerified is pre-Analyze; census extraction there precedes the stage work budgets and cannot solve the before-spawn request/pre-Analyze-refusal coordinate. |
| 2 | Agree with rejection. | declares facts are not an exhaustive population assertion, need not be requested, and cannot supply their own scope subjects. |
| 2a | Agree with rejection. | The existing inventory relations are source-path/package-name relations; symbol facts would require registry change and still not assert census completeness. |
| 3 | Agree: reject committing unavailable values; adopt the rule coordinate. | The host cannot extract native symbols before execution; D∅ names the fixed descriptor using the existing recipe. |
| 3a | Agree with preferring D∅; an extent coordinate would require a different contract. | Putting paths in a symbol scope is wrong, while a separately typed extent commitment needs new producing/join rules. The admitted census's extent is independently checked. |
| 3b | Agree with rejection. | Echoing D∅ in returned Coverage while scopeId names nonempty subjects breaks the identical-digest join and loses the in-band examined partition commitment. |
| 4 | Agree with rejection. | Facts/anchors/file paths cannot independently establish the provider's explicit symbol population. |
| 5 | Agree with rejection under the retained invocation model. | A first census stage cannot revise keys already fixed in the one Analyze request; a second child departs from one child per universe. |
| 6 | Agree that a new frame/major is unnecessary. | A new frame conflicts with EXC's current constraint; negotiated payload succession is available within the existing majors. |
| Additional: OccupancyCompanionV1 or nested StageResult | No preferable missed carrier found. | The companion couples the census to target-attribution-v2/FactBatch fragmentation; nested StageResult reintroduces per-stage repetition. Both need new payload laws without improving the chosen Complete carrier. |
| LD-F3 full SIS wire record / worker projections | Agree with rejection. | The Plan locator and detector projection coordinates belong to the host; sending them to the worker only to echo them adds no trustworthy population information. |
| LD-F4 partial wire population | Agree with rejection as a bounded design decision. | ENC permits partial outcomes but does not require trusted rows from an unsettled terminal. Adding safely committed partial rows would require a separate terminal/lifetime design. |
| LD-F5 large census as schema fault | Agree with rejection. | A truthful size overflow should take the owned scope-limit route rather than assert provider protocol corruption. |
| LD-F7 symbol-only inherited key supersession | Agree with rejection. | The inherited per-stage file recipe conflicts with §4.1a for all relation/rung descriptors. |
| LD-F8 registered-schema edits / duplicate StageRequest transcription | Agree with rejection. | Changing registered schema bytes changes payloadSchemaDigest; duplicate inherited records create drift instead of naming the accepted selector. |

These rejections are choices among lawful forms where stated, rather than claims that an explicit future owner successor could never adopt the alternative. No missing carrier is preferable under the current request construction, per-stage budget and clean-settlement rules.

**Non-blocking observations**

**FA2-N1-01** — `docs/coop/design-corrections/native/provider_wire_model.v1.py:48; docs/coop/design-corrections/native/provider_startup_model.v1.py:41,186-205`

The existing design-evidence references still load the original handshake/startup schemas; the startup model also unconditionally compares subjectScopeCommitment with the requested key. They therefore do not demonstrate a negotiated FA-2 handshake or admission of a nonempty census return. Their stated scope is historical design evidence, and FA-2 explicitly defers product implementation, so this is not an additional carrier-law blocker.

In the implementing owners' review, track successor-aware schema loading and the conditional symbol-key check through clean settlement. Retain the old no-token refusal controls. No FA-2 byte change is requested for this observation.

**FA2-N1-02** — `docs/implementation/m3/native-successors-fa/fa-2/README.md:292`

The evidence count is misstated. The script has seven valid payload cases and five refused payload cases, plus the two projected-SIS cases. All 14 passed; this changes no validation result.

Exact replacement for the evidence-count paragraph:

```text
With `--deps` it validates 14 cases against the new schema using the design encoder's `ExactValidator` (`foundation/canonical.py`, jsonschema 4.25.1 installed offline into a scratch directory). Seven are valid payloads, five are payload refusals, and two check the projected record against SIS (one valid, one refused). All pass.
```

**Validation and limits**

The permitted evidence script ran with the pinned Python at nice 19 and exited 0. It regenerated nine files in memory, reproduced the scope2 oracle, passed all 14 supplied schema cases, and checked the exact before values, candidates, copies and three locks. See [evidence-check.txt](evidence-check.txt), [pin-check.txt](pin-check.txt) and [pin-check-final.txt](pin-check-final.txt).

| Lock | Contract successors | Parents/copy carry/selectors/fresh paths |
|---|---:|---|
| `e093e908dd7fe735356a896f3cf4b97e1d93198e` | 77 | Pass |
| `15c077935a9fdd9d2550726922669d576e7f6c4b` | 81 | Pass; B-S1 NE selectors disjoint |
| `cd5958b3608f44a0035566c9d4500e5005c62e91` | 82 | Pass; I1-P does not collide |

The real `contract_successor` / `successor_chain` code was inspected statically; `verify_design.py` was not run. The generated schema checks are neither a CBOR codec exercise nor a provider/compiler/frame or real Plan-extent join. They do not resolve X-H6 or the existing Rust request cap.

No cargo, product builds/tests, crash-matrix commands, repository edits, commits or delegation occurred. The offline dependency install and all scratch/output stayed in this review directory. Commands used a private review-local HOME and TMPDIR (0700), and did not read/create the real OpenSIP home or read the private 413 UUID fixture.

The corrected subject must be regenerated, re-pinned and reviewed before selection. Independent acceptance and matching root assent remain required by the existing binding rules; this review supplies neither.


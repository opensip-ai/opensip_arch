# Author handoff — blind-consumer corrections, native + security (actual Claude, coauthor)

**Standing:** PROPOSED successor edits, NOT SELF-ACCEPTED. The acceptance of
`candidate-subject.v5` does **not** cover these bytes. A fresh independent reviewer and a fresh
blind consumer must see a newly frozen subject. Nothing here awards readiness, qualifies a
platform, or authorizes implementation. Passing a reference checker is design evidence only.

Source of the items: `/tmp/opensip-design-corrections/consumer-b.v1/output/blind-review.md`
(fresh blind session, 5 MUST + 6 SHOULD). Its own code and vectors were treated as evidence, not
as authority; every claim below was re-derived from current repository bytes.

**Scope actually edited (13 files, digests in `evidence/edited-files.json`):**

| File | What changed |
|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | §0 row, §2.2, §2.3, **new §2.4**, **new §4.1a**, §9.4, §10, §11, §12, §13 H-8, §14, Standing |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | S3, S8, S9.1, S9.2, S10, S10.2, **new S12.1**, S13, Standing |
| `native/native-evidence.schemas.v2.json` | +14 closed defs (86 → 100) |
| `native/native_evidence_model.v2.py` | subject-scope/coverage boundary, TypeScript native context, canonical-set fix |
| `native/native-cases.v2.json` | +31 cases (101 → 132), +24 fixtures |
| `native/check_native_evidence.v2.py` | new `foundationIdentityVector` and `concat` steps |
| `native/README.md` | counts, CB-* map rows, handoff paragraph |
| `security/security_lifecycle_model_v1.py` | S12.1 public-detail projection |
| `security/security-lifecycle.schemas.v1.json` | +`PublicDetailProjectionV1` (42 → 43) |
| `security/root-schema-cases.v1.json` | +2 strict end-anchor regressions, +2 root fixtures |
| `security/public-detail-cases.v1.json` | **new**, 10 cases |
| `security/check-security-lifecycle.v1.py` | new case file, new model, new sweep |
| `security/README.md` | provenance, counts, sweep description |

**Not touched, deliberately:** `native/source-pins.v2.json`, `security/source-pins.v1.json`,
`native/native-evidence-report.v2.json`, `security/security-lifecycle-report.v1.json` (Codex
refreshes after integration); every historical file; `identity-and-evidence.md`,
`admission-and-qualification.md`, `workflows-and-surfaces.md`; `JOINT-INTERFACES.md`;
`discovery-defaults.py`; `public-detail-registry.v1.json`; every workflow schema and model;
`integration-host-model.py`; `check-integration.py`; inventories, registers, coordinator and
readiness documents.

---

## M-1 — `subjectScopeCommitment` producing recipe (closed)

**Recipe.** `subjectScopeCommitment` = `"sha256:"` + the 64 hex of
`H("subject-scope", D)`, i.e. the *same digest* as the foundation `scope2` identity, in the native
`Sha256Text` textual form. `D` is the closed foundation record
`identity-schemas.v2.json#/$defs/subject-scope`
`{schemaVersion:2, snapshotId, sourceUniverse, targetUniverse, relation, resolution,
enumeratorClosure, subjects}`. No native `H` domain; no second preimage; no new digest.

**Inputs and domain** are stated field by field in native §4.1a (snapshot, the key's own relation
and rung, the two bare-hex universe digests, the Plan-bound enumerator `closure2`, and the
complete examined subject inventory as a canonical set with duplicates refusing).

**Join with `scope2`.** Identical suffix, deliberately. The commitment is the provider's *in-band*
commitment inside the payload whose `payloadDigest` mints `coverage2`; `coverage.scopeId` is the
host's *out-of-band* binding of the same scope. Equality of the two is the check.

**Producing/checking boundary — implemented.** `admit_coverage_result_v3(payload,
scope_descriptor, unresolved_facts)` in the native model. The host builds `D` from **its own**
enumeration and mints `scope2` before reading the payload's commitment, so no claimant-supplied
digest is ever authority. Refusals (all `PROVIDER.PROTOCOL_VIOLATION`, operational-failed 4, §10
fault law → no facts, no Coverage, no Run):
`native.coverage-key-scope-mismatch:<field>`, `native.subject-scope-commitment-mismatch`,
`native.coverage-entry-key-mismatch`, `native.examined-universe-commitment-mismatch`,
`native.examined-universe-subject-count-mismatch`, plus the RC-2 bijection faults.

**Coverage use — implemented.** `coverage_view_use(view, admissions)`: a `view2` may name a
`coverage2` only if it was admitted at that boundary and its `scope2` is one of the view's own
`scopeIds` (`native.coverage-not-admitted-at-producer-boundary`,
`native.coverage-subject-scope-outside-view`).

**No circularity.** Derivation order is total and acyclic: closures → native context → universe →
`scope2` → commitment → Coverage payload → `coverage2` → `view2`. No universe, context or scope
descriptor names a scope, Coverage, view, evidence or Run. The workspace-roots `scope-descriptor`
whose raw digest is `scopeDigest` is a different record and is explicitly distinguished.

**Old artifact preserved.** `c2-plan-stage-schema.v4.json $.coverageKey.key[subjectScopeCommitment]`
is untouched. Its §0 disposition moved from *Retained* to **Retained (shape) and extended**; its
`"SHAPE ONLY; computation and verification stay deferred (R1-C2-03)"` deferral and its
`EXAMPLE ENCODING for the fixtures only` note remain historical bytes and remain a non-recipe.

**Identity-contract coordination — already converged.** While this session worked, identity §3
gained the same recipe in its own words ("another textual form of the **same** digest, not a
separate hash of the subjects or of the scope identifier string"), the same descriptor fields and
the same `subjectCount` rule. Native §4.1a now records the agreement rather than requesting the
sentence. **Codex action: none outstanding for M-1** beyond confirming the two statements stay in
step when either document next moves.

**Cases (14):** `subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form`
(hand-spelled canonical bytes + `hashlib` oracle via the new `foundationIdentityVector` step),
`subject-scope-commitment-binds-the-snapshot-not-only-the-subject-list`,
`coverage-admission-mints-coverage2-from-the-host-subject-scope`,
`coverage-commitment-chosen-by-the-claimant-is-refused`,
`coverage-producer-chosen-narrower-examined-partition-is-refused`,
`coverage-examined-subject-count-that-disagrees-with-the-enumeration-is-refused`,
`coverage-key-naming-a-universe-outside-the-host-scope-is-refused`,
`coverage-complete-claimed-over-an-admitted-unresolved-edge-is-refused-at-the-boundary`,
`coverage-incomplete-over-an-exhaustive-partition-admits-with-the-same-commitment`,
`coverage-use-requires-the-subject-scope-to-be-in-the-evaluated-view`,
`coverage2-whose-subject-scope-is-outside-the-view-is-refused`,
`coverage2-never-admitted-at-the-producer-boundary-is-refused-in-a-view`,
`subject-scope-duplicate-subject-refuses-rather-than-silently-deduping`,
`coverage-payload-schema-digest-a-caller-chose-is-refused`.

---

## M-2 — closed TypeScript native context

**New records** (native schema bundle): `TypeScriptNativeContextV2` (H domain
`native.context.typescript.v2`), `TypeScriptToolchainIdentityV1`, `TypeScriptToolClosureV1`,
`TypeScriptConfigProjectionV2`, `TypeScriptHonoredOptionsV1`, `TypeScriptStrippedOptionV1`,
`TypeScriptLockfileIdentityV1`, `TypeScriptLibComponentV1`, `TypeScriptModuleResolutionMode`,
`NativeContextLanguageV1`, `NativeContextAdmissionV1`.

`typescriptStdlibMerkleRoot` lives at `TypeScriptNativeContextV2.toolchain.typescriptStdlibMerkleRoot`,
exactly mirroring `NativeContextV2.toolchain.rustcDevLlvmDigest`. Both are bare `DigestHex`, both
are the 64-hex suffix of a `closure2`, and admission recovers the closure id by re-prefixing and
requires a **retained** closure of the right kind that recomputes to it.

**Field locations and producing recipe** are tabulated in native §2.4: compiler version from the
*admitted signed closure manifest* (never `tsc --version`), compiler/runtime digests as members of
the signed `kind=toolchain` closure, every stdlib declaration file digest from the retained
`kind=stdlib` tree, `libSelection` covered by retained components, the effective compilerOptions
projection with typed stripping reasons, the resolved `extends` graph paths, the node_modules
layout digest and the lockfile identity.

**Retained trees:** both closures are retained whole (descriptor + file tree) and joined to the
selected compiler.

**No fake Rust context:** `NativeContextV2` is named as the Rust record; a Rust descriptor offered
as a TypeScript context refuses `native.native-context-language-mismatch`.

**No platform family** in the TypeScript context, and the reason is stated: TypeScript
capabilities are platform-invariant by design (§1.1), so one source tree must not mint two
`nativeContextId`s on two platform families.

**Universe / Plan binding:** `bind_typescript_universe` refuses a universe naming a context this
host did not mint; `plan_native_context_digests` emits the bare 64 hex the foundation `plan`
record requires. **A-2** is stated as a table in §11: one digest, three admitted textual forms
(foundation typed prefix / native `Sha256Text` / bare `DigestHex` suffix), with the rule for which
is required where. **A-1** is fixed in §2.3, §2.4 and §14 with the exact nesting.

**Independent tests (17 cases):** a stdlib change alone and a compiler change alone each move the
context and the universe id, and they move it to *different* values; malformed merkle root naming
no retained closure; a tool digest outside the named closure tree; a stdlib component digest
disagreeing with the retained tree; a Rust descriptor offered as the TypeScript context; a
universe bound to a foreign context; worker recomputation mismatch →
`Unavailable(native-context-mismatch)` before Analyze; and the bare-hex/`sha256:` spelling split.

---

## M-5 — public detail codes the closed registry cannot express

**Determination.** The de-facto rule in current bytes, now stated normatively in security §S12.1
and implemented as `public_detail` / `public_details`:

1. Base code = everything before the **first** colon; the remainder is `DomainDetail.subject`.
2. A `detail` whose base code is a registry member wins over the enclosing `refusal`. This is why
   the 38 `ROOT.*` document defects are public codes rather than collapsing into one
   `PAYLOAD-NOT-ADMISSIBLE` — and it is exactly why `ENVELOPE.*` / `PROFILE_SET.*` must be
   registered: they occupy the same position in `admit_profile_set_envelope` that `ROOT.*` occupies
   in `admit_root_document`, and S9.1 names them normatively as `detail`.
3. Otherwise the `refusal` supplies the code and the whole detail is subject text. That is the
   existing, correct reading for `RECOVERY.REFUSED` (`CHALLENGE_EXPIRED`, `COUNTER_MISMATCH:<k>`),
   `CONFIG.CUSTODY_REFUSED` (`SYMLINK`, `WRITABLE_BY_OTHERS`) and `PROJECT.EXPLICIT_PATH_INVALID`
   (`JOIN_PATH_GRAMMAR`). **Those sub-details must NOT be registered** — doing so would create a
   second public vocabulary for the same events.
4. **Closed, not a prefix rule.** The unit declares `SECURITY_PUBLIC_DETAIL_CODES` (191 members). A
   detail whose base lies inside one of the eight families this unit publishes (`AUTHZ.`,
   `ENVELOPE.`, `GRANT.`, `NT-TCB-`, `PLAN.`, `PROFILE_SET.`, `ROOT.`, `TRANSITION.`) but outside
   that set **refuses**. There is no open `PROFILE_SET.*` wildcard.
5. The D9 branch comes from the **refusal**, never from the detail.
6. `PROFILE_SET_KEY_NOT_MACHINE_ID` is **not** a code: it is a subject sub-detail of the registered
   `NT-TCB-PROFILE-UNQUALIFIED` (`NT-TCB-PROFILE-UNQUALIFIED:PROFILE_SET_KEY_NOT_MACHINE_ID:<id>`),
   in the same position as `platform-display-alias-not-machine-id`. S8 prose corrected.

### Codex action 1 — add 11 records to `public-detail-registry.v1.json` and the typed enum

`owner: "security"`, `selector: "security/security_lifecycle_model_v1.py (D9 and typed refusal declarations)"`.
Two more than the blind reviewer listed: the sweep found the per-role spellings of S9.1's schema-2
threshold rule, which the registry does not carry (it has `ROOT.ROLE_THRESHOLD_POLICY` and
`ROOT.ROOT_THRESHOLD_POLICY` but neither of these).

| Code | Emitted by | D9 branch |
|---|---|---|
| `ENVELOPE.SHAPE` | `admit_profile_set_envelope` | request-rejected 2 `EXTENSION.ADMISSION_REJECTED` |
| `ENVELOPE.KIND` | " | " |
| `ENVELOPE.BODY_DIGEST` | " | " |
| `PROFILE_SET.SCHEMA_SHAPE` | " | " |
| `PROFILE_SET.SCHEMA` | " | " |
| `PROFILE_SET.CANON` | " (subject = the canonicalization error) | " |
| `PROFILE_SET.CORE_PIN_MISMATCH` | " | " |
| `PROFILE_SET.NO_TR_PROFILE_ROLE` | " (subject `core-release-embedded-copy-only`) | request-rejected 2 **`REQUEST.SCHEMA_MAJOR_UNSUPPORTED`** (refusal is `ROOT.SCHEMA_UNSUPPORTED`) |
| `PROFILE_SET.SIGNATURE_THRESHOLD` | " | request-rejected 2 `EXTENSION.ADMISSION_REJECTED` |
| `ROOT.TR_REPAIR_THRESHOLD_POLICY` | `admit_root_document` schema-2 role rule (subject `TR-REPAIR`) | " |
| `ROOT.TR_PROFILE_THRESHOLD_POLICY` | " (subject `TR-PROFILE`) | " |

`common.schema.json#/$defs/DomainDetailCode` takes the same 11 members (271 → 282, registry and
enum stay exactly equal, preserving the §12 drift check the blind consumer verified as E19).

### Codex action 2 — add one internal alias

```json
{"internalCode": "RF-6:AUTHORIZATION.GRANT_NOT_CURRENT",
 "publicCode": "TRUST.COMPONENT_REVOKED_DURING_OPERATION"}
```
The S6 linearization trace's spelling for a request refused after revocation. It is an internal
decision key, not a public code.

### Representative emitted shapes (validated)

Produced by `evidence/pending-detail-shapes.json` (script `emitted-shapes.py`), which ran
`integration-host-model.public_termination` twice: once against current repository bytes and once
against a **/tmp copy** patched with the 11 records. Result: `currentBytesRefuseEveryPendingCode:
true` (all 11 raise `Refusal('unregistered public domain detail')`), `afterRegistrationAllAdmit:
true` (all 11 validate against `common.schema.json#/$defs/StepTermination`). The repository
registry and enum were **not** modified.

```json
{"class": "request-rejected",
 "errorCode": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
 "domainDetail": {"code": "PROFILE_SET.NO_TR_PROFILE_ROLE",
                  "subject": "core-release-embedded-copy-only",
                  "remedy": "Under a schema-1 root only the copy embedded in the signed core release is used; adopt a schema-2 root with an active TR-PROFILE first."}}

{"class": "request-rejected",
 "errorCode": "EXTENSION.ADMISSION_REJECTED",
 "domainDetail": {"code": "ENVELOPE.BODY_DIGEST",
                  "remedy": "Recompute bodyDigest as the metadata-profile digest of the canonical body under its domain."}}
```
All 11 shapes are in `evidence/pending-detail-shapes.json` under `representativeTerminations`.

**Until they are registered a host cannot emit the refusals S8/S9.1 mandate.** The new sweep
`public-domain-details-are-a-closed-set-with-a-bounded-pending-registration-gap` asserts the
not-yet-registered set is a **subset** of the declared pending list, so it shrinks to empty when
Codex lands the records and can never grow from the security side.

---

## S-2 — the product root admission boundary

Named explicitly in S9.1: **`security/security-lifecycle.schemas.v1.json $.schemas.RootV1` and
`$.schemas.RootV2`, reached only through `admit_root_document`.** The historical
`docs/coop/completion/security-schemas.v8/root.schema.json` is the preserved **rule source** for
schema 1, not a second gate, and is unchanged. The successor is deliberately not byte-equivalent:
every successor pattern ends with `(?![\s\S])` where v8 ends with a bare `$`, so a trailing
newline that v8 admits the product **refuses**.

Regressed **through the actual host gate**, not the schema alone:
`schema-1-root-with-a-trailing-newline-index-origin-url-refuses-at-the-product-boundary` and
`...-role-namespace-...` → `REFUSE` / `PAYLOAD-NOT-ADMISSIBLE` / detail `ROOT.SCHEMA_SHAPE` /
request-rejected 2 `EXTENSION.ADMISSION_REJECTED`, with `inputValid: false` against `RootV1`.
Mutation-checked: restoring the bare `$` makes both cases fail.

---

## S-6 — stale `(obligation, Codex)` sweep

Every one was verified against current bytes; **all five were already discharged**, and the prose
now names the implementing function and the asserting checks instead of claiming an obligation.
Zero occurrences of `(obligation, Codex)` or `Integration obligation` remain in either contract.

| Was | Actual state | Now cited |
|---|---|---|
| security S3 boundary-inventory integration join | discharged | `integration-host-model.admit_repository_discovery`; `host-nested-boundaries-*`, `host-native-inventory-substitution-refused`, `security-native-shared-unit-roots/-pruned-trees` |
| security S9.2 workflow `CoreTransitionIntentV1` enum + store fields | discharged (11 required fields, 5 operations) | the schema itself; the host model validates one intent against both records |
| security S10 Plan projection derived from grants | discharged | `semantic_projection_for_grants` at host-model line 167; checker drops `ctx.semanticGrantPrincipals` |
| security S10.2 recovery-table equality | discharged | `security-workflow-recovery-action-table-identical` |
| security S10.2 recovery projection composed like repair | discharged | `recovery_authorization_projection`; `recovery-caller-projection-refused` |
| native §13 H-8 integration join | discharged | same as S3 row |

No obligation was invented to replace them, and no native/OS/crypto product qualification is
claimed anywhere: a correct reference design does not implement the actual product.

---

## Codex coauthor-note findings on the draft — all seven addressed

`CODEX-REVIEW-NOTE.txt` (written into this directory while the pass was active) probed the draft
bytes and found six real defects, then a seventh on the first correction. Every one is fixed with a
regression that a mutation test proves bites. None is left for integration.

| # | Finding | Fix | Regression |
|---|---|---|---|
| 1 | changing universe `allowJs`/`checkJs` against an unchanged admitted context was ADMIT | `universe_context_field_faults`: `languageMode`, `packageModuleType`, `allowJs`, `checkJs`, `lockfileKind`, `nodeModulesInReadSet`, `jsDiagnosticsEnabled`, `jsAdmittedToProgram`, `configOrigin`, `extends`-graph emptiness, synthesized-options presence; `native.universe-context-field-mismatch:<field>` | `typescript-universe-field-contradicting-the-admitted-context-refuses` (5 contradictions), `typescript-universe-agreeing-with-the-admitted-context-admits`, `typescript-context-bytes-that-are-not-the-admitted-ones-refuse` |
| 2 | dropping an unselected retained declaration library was ADMIT although the contract said "every declaration file" | `standardLibraryComponentDigests` must equal the **complete** `.d.ts` inventory of the retained tree; basename ambiguity in the tree refuses | `typescript-stdlib-inventory-missing-an-unselected-declaration-library-refuses`, `typescript-stdlib-tree-with-two-paths-sharing-a-basename-refuses` |
| 3 | `plan_native_context_digests([a, a])` refused; units may legitimately share one context | the Plan field is a canonical set; identical admitted contexts deduplicate. `NATIVE_CONTEXT_DUPLICATE` removed | the base positive case now passes `["$a", "$a"]` and expects one member |
| 4 | the "platform-invariant context id" claim is impossible: `closure2` includes `platform` | corrected in the schema description, the model docstring and §2.4: resolution *semantics* are platform-invariant; the *identity* is platform-specific through the signed tool closure, as it must be | `typescript-context-identity-is-platform-specific-through-its-signed-tool-closure` |
| 5 | `admit_coverage_result_v3`'s optional schema digest was an arbitrary override | a caller may restate but never choose it; a value that is not the registered document digest refuses `native.coverage-payload-schema-not-registered`. The two positive coverage cases now recompute `coverage2` with `hashlib` from scope + registered document digest + canonical payload instead of pinning a literal | `coverage-payload-schema-digest-a-caller-chose-is-refused` |
| 6 | `pendingRegistration` was a drafting flag that would go stale after integration | computed against `public-detail-registry.v1.json` at call time (read-only), so it clears by itself when the records land; `PENDING_PUBLIC_DETAIL_REGISTRATIONS` remains only as the bound the sweep asserts. Three brittle case assertions removed; the invariant is carried by the sweep | `sweep_public_detail_closure`; `root-document-defect-...` still asserts an empty pending list for a registered code |
| 7 | follow-up: `context` defaulted to `None` and skipped every overlap check — the same bypass on the same entry point | `context` is a **required** argument with no weaker admit path; omission is the typed refusal `native.universe-context-not-supplied`; all callers and cases updated | `typescript-universe-bound-without-the-retained-context-refuses` |

Two checker primitives were added to keep the cases honest rather than to make them pass:
`foundationIdentityVector` (independent `hashlib` oracle for a foundation-domain identity) and
`concat` (assert an exact typed refusal whose subject an earlier step computed, instead of a frozen
literal).

## Tests and results (run with `/tmp/opensip-architecture-review-env/bin/python -I -B`)

Against a **disposable mirror** at `verify/repo` with pins regenerated there only
(`repin-disposable.py` refuses to run outside `/tmp`). Repository pins and reports untouched.

| Checker | Result |
|---|---|
| `native/check_native_evidence.v2.py` | **PASS 132/132** cases; 60 matrix cells; 0 open objects; 0 uncovered feedback |
| `security/check-security-lifecycle.v1.py` | **passed true**, 456/456 cases, **10/10 sweeps** |
| `check-integration.py` | **327 passed, 0 failed** |

Mutation tests (each mutant reverted afterwards):

| Mutation | Cases that failed |
|---|---|
| trust the claimant's `subjectScopeCommitment` | `coverage-commitment-chosen-by-the-claimant-is-refused`, `coverage-producer-chosen-narrower-examined-partition-is-refused` |
| skip the native-context closure retention join | `typescript-stdlib-merkle-root-that-names-no-retained-closure-refuses` |
| let any dotted family member through as a code | `an-unregistered-member-of-a-published-family-refuses-rather-than-opening-a-wildcard` |
| drop the internal alias table | `an-internal-linearization-key-is-aliased-to-its-registered-public-code` |
| restore the bare `$` in `RootV1.indexOrigin.url` | `schema-1-root-with-a-trailing-newline-index-origin-url-...`, `root-document-defect-emits-the-specific-ROOT-code-...` |
| skip the universe/context overlap check, the stdlib inventory check, the required-context refusal and the registered-schema-digest check (four at once) | `typescript-universe-field-contradicting-the-admitted-context-refuses`, `typescript-stdlib-inventory-missing-an-unselected-declaration-library-refuses`, `typescript-universe-bound-without-the-retained-context-refuses`, `coverage-payload-schema-digest-a-caller-chose-is-refused` |

**One pre-existing cross-unit regression fixed in passing.** Codex's tightened foundation
canonical-set admission made `default_capability_selection` emit `analysis-spec.
requestedCapabilities` in discovery order, which the foundation validator now refuses
(`array order canonical-set: strict unique order required`). The native model now sorts by
canonical bytes and refuses a duplicate row; the case expectation was reordered to match. This was
failing before any of my edits.

**Pin state.** The foundation launcher (`foundation/run-reference-checks.py`) is pin-blocked in
the working tree because its pin list covers foundation, workflow, native and security bytes that
several sessions have moved concurrently. That is parallel-integration pin drift, not a design
blocker; Codex re-pins after integration. I did not repin any repository manifest.

---

## Remaining cross-unit changes (Codex)

1. **Registry + typed enum:** the 11 records and 1 alias above (M-5). Blocking for a host that
   must emit the S8/S9.1 refusals; nothing else depends on it.
2. **Re-pin and re-run:** `native/source-pins.v2.json`, `security/source-pins.v1.json`,
   `foundation/source-pins.v1.json`, and regenerate `native/native-evidence-report.v2.json`,
   `security/security-lifecycle-report.v1.json`, the foundation reports and the integration report.
3. **Optional host-side join for M-1/M-2** (`integration-host-model.py`, Codex-owned): compose
   `N.admit_coverage_result_v3` and `N.admit_native_context` / `N.bind_typescript_universe` /
   `N.plan_native_context_digests` in the host model, so the commitment and the TypeScript context
   are exercised end to end beside the boundary-inventory join. Not required by the corrections;
   it would strengthen the cross-unit evidence.
4. **Codex-owned blind items untouched here, as instructed:** M-3 canonical array law and
   machine-readable markers, M-4 resolved-config shape, S-1 `$.hostTerminationUnion` disposition,
   S-3 inventory tie-break, S-4 `regeneration-mismatch` registration, S-5 blind-kit dependency
   closure. Note that M-3 already bites in practice — see the `default_capability_selection`
   regression above — so the machine-readable ordering markers matter beyond the policy example.

## Standing, again

Coauthor only. NOT SELF-ACCEPTED, no independent acceptance, no readiness grade, no product
qualification. These are successor edits to an accepted subject and require a newly frozen subject
for the next independent review and the next blind consumer.

---

## Reproducing these runs

The disposable mirror is not retained (it was a full copy of `docs/`). Two commands rebuild it:

```
mkdir -p /tmp/opensip-verify && tar cf - -C /Users/sb/code/opensip-ai/opensip_arch docs | tar xf - -C /tmp/opensip-verify
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/blind-corrections-author.v1/repin-disposable.py /tmp/opensip-verify
cd /tmp/opensip-verify
/tmp/opensip-architecture-review-env/bin/python -I -B docs/coop/design-corrections/native/check_native_evidence.v2.py --regenerate-pins
/tmp/opensip-architecture-review-env/bin/python -I -B docs/coop/design-corrections/native/check_native_evidence.v2.py
/tmp/opensip-architecture-review-env/bin/python -I -B docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report /tmp/sec.json
/tmp/opensip-architecture-review-env/bin/python -I -B docs/coop/design-corrections/check-integration.py --report /tmp/int.json
```

`repin-disposable.py` refuses to run outside `/tmp`. Retained reports of the final runs are in
`evidence/native-run.json`, `evidence/security-run.json` and `evidence/integration-after.json`;
`evidence/integration-baseline.json` and `evidence/security-baseline.json` are the pre-correction
runs, and `evidence/security-mutant.json` is one mutation run.

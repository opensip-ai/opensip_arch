import pathlib
table = pathlib.Path('/tmp/delta-table.md').read_text()
body = '''# bv6-corrections-author.v2 — correction coauthor handoff

**Role.** Correction **coauthor** working with Codex. Not an independent reviewer,
not an accepting reviewer. No product implementation, agents, commit, push or
publication. All v2 writes are under
`/tmp/opensip-design-corrections/bv6-corrections-author.v2`.

**Technical assent: TRUE** to the exact bytes in §4 as a correct, minimal and
mutually consistent disposition of all eight root points, the four original blind
v6 required findings, the three advisories, my own findings, and every coherence
point in `CODEX-PUBLIC-NOTE.md`. It asserts **no agreement by Codex**, no
independence, no acceptance and no readiness.

---

## 1. Custody

`work/` verified byte-exact against `root-input/final-v1-source-inventory.json`
before any edit — 6839 declared, 0 missing, 0 mismatched, 0 undeclared. Frozen
manifest SHA-256 recomputed as `ca5f36d4…44042ee9`, matching. After all edits: 0
missing, 0 undeclared, **15 changed this turn**, **17 aggregate vs frozen v16**.

`CODEX-PUBLIC-NOTE.md` was **absent** at initial assessment and **present** before
this handoff. I read it in full; it **materially changed CX-BV6-03 and CX-BV6-04
and corrected my own initial assessment**, which is retained verbatim in
`assessment/`.

---

## 2. Root points — all eight agreed and corrected

### CX-BV6-01 (MUST) — overlapping scopes admitted at Run closure

**My CB6-NEW-3 deferral is withdrawn.** Deferring a demonstrated violation of
existing published law was not defensible. `coveragePartitionLaw` is now published
in the relation registry beside `coverageTotalityLaw`, `identity-model` **reads**
its `partitionKey`, and per-view subject disjointness is **decided at retained Run
closure**. Root's own v3 probe now refuses the overlap case with
`SUBJECT_SCOPE_PARTITION_OVERLAP:references@resolved-binding:foo` while both
lawful cases still admit.

I assessed each proposal boundary rather than accepting it. **Accepted:** the
grouping key (it equals the registry `matchOn` *and* the tuple already stated in
§3, so the enforced and stated keys become one object); per-view isolation;
coverage of scopes without Coverage; and the single-producer limit. **Not adopted
as proposed:** the overlap test runs *after* every scope passes its own
well-formedness checks, so a foreign-snapshot scope refuses as **itself**; and the
key is **published in the registry and read**, not hardcoded in the model.

All three Codex precision points applied: scopes without Coverage bypass the
per-Coverage **producer** guard but still reach the ladder guard; the reported
subject is `min` by **UTF-8 byte order**, named exactly and not equated with
canonical-JSON order; and `whyItIsNeeded` now says an invalid partition was
*accepted* and claims over such a view *can* be ambiguous or double-counted,
without asserting every consumer does.

**Disclosed consequence:** adding the law to the relation registry changes that
registered schema document's digest, which is committed in `view.schemaDigests`,
so retained-Run identities over fixtures move. Ordinary for a committed schema
document, not a defect — recorded because the probe baseline RunId visibly changed.

### CX-BV6-02 (SHOULD) — helper admitted what its own schema refused

Reproduced exactly; the cause was mine (`req.get(...)` conflating explicit null
with absence, and a truthiness test). Now: `satisfied` must be an actual `bool`;
key **presence** is distinguished from value so an explicit `null` refuses in both
branches; and every violation routes to **`CONFIG.INVALID`**, matching
`validate_import_record` and `admit_atom`. Root's five-case probe now agrees on all
five. The "works even when a host skips schema validation" comment is gone,
replaced by the accurate requirement that two boundaries deciding one law agree.

### CX-BV6-03 (MUST) — imported-evidence requirement ownership

My v1 answer addressed imported-*prepared* **native** Runs — a different plane. A
separate owning law now lives in `imported-evidence.schema.json` with **seven**
outcomes, each bound to the payload field that grounds it, mirrored as
`ImportedRequirementDeficiency`, with `EvidenceRequirement.deficiency` a
plane-tagged union whose plane is decided **at admission** from registry membership.

All five Codex coherence points applied:

1. **Satisfied ≠ positive.** `observable-unhit` is *bounded negative* evidence that
   can satisfy, and the disclosure carries the polarity. Optional absence is
   `satisfiedBy: declared-optional-absence` — satisfied *by absence*.
2. **Not "never affects applicability."** Imported evidence can never *by itself*
   establish the native closed world or authorize an unsafe delete/replace, but it
   *may* be an additional required condition. Both directions are controlled by real
   `repair_preview` cases.
3. **Optional is explicit and bound.** `required` is **never** defaulted to
   optional, so an unsupplied declaration is read as required and an unresolved
   condition is never silently satisfied.
4. **Every input is bound to an owning field.** Targets come from
   `RepairPlanDescriptor.targets` — **no field is added** to `EvidenceRequirement`;
   all-versus-any is its **existing** `completeness`; required-versus-optional is
   `evidenceUse`. The projection is documented as pure over already-admitted inputs
   and claims no Run validation.
5. **History has its own projection.** `HistoryPayloadV1` carries `revisionRange`
   and `collectionScope` and none of the runtime fields, so history has its own two
   outcomes and neither kind may report the other's.

**Root's counterexample is resolved.** `complete` over `[seen, missing]` with only
`seen` observed returned `satisfied=true` under the draft `any()`; against final
bytes it returns `import-absent-for-requirement`, while `partial-acceptable` over
the same inputs still satisfies.

### CX-BV6-04 (SHOULD) — command names vs operation tokens, and the receipt join

Two corrections. First the conflation: `genericMutationClasses` held 20 **command
names** while the annotations called it the operation domain; three names refuse
and six admitted tokens were absent.

Second — and this **corrects my own initial assessment** — Codex is right that a
missing Python emitter does not establish absence of a normative obligation. I
verified the citations: `ImportResult` and `NativePreparationResult` **both
require** `receiptId`; `ReceiptId` is `receipt2:`; §10 declares exactly one receipt
domain; and `MutationReceiptV1` **requires** `operation`. Both steps already owed a
receipt carrying an operation — only the **binding** was missing. That is (b) a
missing design law, not (a) a reference-model limit, and it is corrected now.

Published: `byStepKindReceiptOperation` (four kinds, each with its owning
result/params citations), `byCommandGenericMutationStep` (20 rows), and
`admissibleGenericFieldDomain` (the actual **23** tokens, verified by admitting each
at the real field). `analyze` needs **no exception** — the binding is by step kind,
so its import step carries `import` exactly as the import command's does; the v1
checker subtraction is removed. **Injectivity is dropped as a law**: `import` is
emitted by *two* commands, a worked non-invertible case. Nothing is narrowed —
`config-write` stays admissible although no step kind binds it. No auto-retry, no
native execution, no new authorization; a fresh preparation is a new authorized
execution, never a delivery replay.

### CX-BV6-05 · CX-BV6-06 · CX-BV6-07 (SHOULD)

**05:** the unit prerequisite is scoped to the five **compilation** modes;
`syntax-only` explicitly needs no unit and is the path when U-1 yields none.
**06:** restated as a **projection** law — the full result carries `causes` on both
branches and may carry `disclosures` on the failing one; the record carries only the
satisfaction/deficiency projection and nothing licenses dropping the rest.
**07:** all four items — the unverified external TypeScript claim removed; the
ordering corrected (the digest *is* computed and compared; what never happens is
**admission**); the no-drift claim scoped to model-versus-table; and the
imported/non-native `ViewEntryV3` example removed, with the global native provider
scope retained as root accepts it is defensible.

### CX-BV6-08 (SHOULD) — v1 evidence corrections

The v1 handoff and every original report stay **verbatim**. Corrected here: v1
claimed all writes were inside its output directory (false — `/tmp/cb6_*.py`,
`/tmp/bl-*`, `/tmp/w*`, `/tmp/i*`, `/tmp/id2-3.json`, `/tmp/probe-cw.json`,
`/tmp/cb6-delta*.json`); claimed `D9Deficiency` byte-unchanged (only its **enum**
is — I added a description); overstated the `config-write` search scope; called
`byCommand` keyed both ways when it is not an inverse map; said "no filesystem was
executed" when Python read, wrote and hashed throughout (what was *not* done is
product execution or host durability qualification); and treated `DomainDetailCode`
as a five-member set when it is a 287-member registry. `run-six.sh` lacked
`pipefail` and is not the canonical six. The disposable copy excludes most of
`reviews/` and reuses report filenames.

**Method corrected:** the two v1 prose-substring/wrapping controls are **removed**,
not repaired — replaced by full-Run enforcement of the same wording. No new
substring or wrapping control was added, and no suite was re-run after every edit.

---

## 3. Original findings

All severities and ownership preserved. **CB6-MUST-1** extended (plane-tagged,
typed presence, consistent routing). **CB6-MUST-2** substance unchanged; three
rationale statements corrected. **CB6-SHOULD-1** materially revised.
**CB6-SHOULD-2** now *enforced* rather than asserted. **CB6-ADV-1** scoped.
**CB6-ADV-2** retained with the disagreement recorded. **CB6-ADV-3** unchanged;
inherited D9 bytes still untouched. **CB6-NEW-1** retained. **CB6-NEW-2 corrected
and narrowed** — my interim widening to three orphans was wrong; only
`config-write` is unbound. **CB6-NEW-3 withdrawn.** **CB6-NEW-4** new: editing a
registered schema document moves retained-Run identities over fixtures.

---

## 4. Changed source — 17 vs frozen v16, 15 this turn

Abbreviated to the first eight hex characters; the untruncated values and per-file
edit lists are in `handoff.json#/changedSource/files`.

''' + table + '''

**Not touched:** v1 and its handoff; all `root-input` files; every generated report
and all four source-pins manifests in `work/`; the crosswalk, historical
preservation reports, post-reset dispositions, qualification gates and validation
summary; `d9-exit-contract.v1.14.json` and every inherited artifact; the blind v6
report; and the live repository, read-only throughout.

---

## 5. Commands and results

Run in the **separate disposable repinned copy**
`disposable/checker-run.v1`. `work/` was never repinned — its pins are stale, which
is expected and is neither a product failure nor a PASS. `run-suites.sh` sets
`pipefail` and is **explicitly not the canonical six**; root runs those after final
source, records and pins. Every verdict is read from the suite's own report JSON.

| Suite | Result | v1 → v2 |
|---|---|---|
| `check-foundation.py` | PASS 231/231 | 231 → 231 |
| `check-identity.py` | 1345 passed, 0 failed | 1338 → 1345 |
| `check-security-lifecycle.v1.py` | 456/456, 10 sweeps true | 456 → 456 |
| `check_native_evidence.v2.py` | PASS 355/355 cases | 355 → 355 |
| `run-reference-checks.py` | pins valid, 1761/1761 | 1672 → 1761 |
| `check-integration.py` | 388 passed, `failed: []` | 378 → 388 |

**Root probes re-run against final bytes.** Overlap v3: the overlap case now
refuses with the exact cause. No-coverage v1: the overlapping no-Coverage case now
refuses; disjoint still admits. Requirement draft: helper and schema agree on all
five. Imported draft: both relations now report plane `imported`. Mutation map v2:
**cannot run unmodified** — it reads the key this correction removed *because that
key was the conflation*; its unmodified failure is retained and
`probes/probe_cx04_map.py` asks the same question against the corrected structure,
reporting `fieldDomainMatchesSchemaExactly: true` over 23 operations.

**Preserved failed attempts:** my first partition probe (a harness defect —
identical subjects collided on identity); my over-strong boundary/schema agreement
control (rows 10–11 asserted agreement the schema cannot provide); and my initial
CX-BV6-04 assessment, retained verbatim with its wrong reasoning.

---

## 6. Limitations

* Design reference evidence over synthetic trusted inputs. No compiler, provider,
  renderer, ledger or product emitter executed. Passing controls is not
  qualification.
* **Reference model vs design law:** the model emits a receipt only for
  `repair-apply` and does not exercise a production import or native-preparation
  emitter. Stated as a qualification limit, deliberately distinct from the design
  law, which is normative and complete.
* `imported_requirement_outcome` is a **pure projection** over already-admitted
  inputs; it validates no opaque Run and admits no payload, observation scope or
  polarity.
* The shared fixture builds one view per Run; the per-view isolation control
  constructs a second view directly — synthetic, not producer-generated.
* Editing a registered schema document moved fixture Run identities. Disclosed.
* Pins in the proposed copy are stale by design.
* A fresh independent Claude review and a **new blind consumer** on the accepted
  successor bytes remain required. This is coauthor assent to exact bytes — **not
  agreement, acceptance or readiness**, and Codex has not assented.
'''
pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/handoff.md').write_text(body, encoding='utf-8')
print('written', len(body))

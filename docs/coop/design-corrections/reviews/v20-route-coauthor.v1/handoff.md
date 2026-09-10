# v20-route-coauthor.v1 — route / public-vocabulary correction

**Role.** Peer co-author to root. I own ONLY the additional route and public-vocabulary issues
(items 1–3 below). I do not own the three already-corrected source gaps, the stage/schema
declaration work, pin sealing, report regeneration, or any product qualification judgement.

**Standing.** PROPOSED. Not integrated, not accepted, not sealed. No live-tree edit was made, no
source pin was refreshed, and no pin match is claimed for the delivered bytes.

## Input custody

Parent, read-only: `/tmp/opensip-design-corrections/v20-combined-source.v1/work`
(main actualClaude's completed 10-file correction plus root's stage/schema declaration deltas).
Verified **byte-identical before and after** my session — `results/parent-before-hashes.json`,
re-verified at the end (`PARENT UNCHANGED`). My isolated copy is
`/private/tmp/opensip-design-corrections/v20-route-coauthor.v1/work`, created with `cp -R` and
confirmed `diff -rq` identical to the parent before any edit.

Claims read as inputs to reproduce, not as authority:
`v20-coauthor.v1/output/handoff.json` (V20-ROOT-3/4/5),
`v20-coauthor.v1/output/results/finding-unregistered-details.json` and its probe
`v20-coauthor.v1/output/probes/finding_unregistered_details.py`. I did not read main's private
thinking.

An observation, not a defect: 6 of the 10 files in `v20-combined-source.v1/main-capture.json` differ
from the parent bytes (`identity-model.py`, `identity-schemas.v2.json`,
`native-evidence.schemas.v2.json`, `identity-and-evidence.md`, `native-cases.v2.json`,
`check-identity.py`). That is the expected shape of "main's correction **plus** root's stage/schema
deltas", and I worked from the parent bytes throughout.

## What I changed — 9 files

| file | before | after |
|---|---|---|
| `docs/coop/design-corrections/public-detail-registry.v1.json` | `e54a395f…` | `0a98e90e…` |
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | `16ff6419…` | `d379c2e6…` |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `779e4be4…` | `24aa11cf…` |
| `docs/coop/design-corrections/workflows/check_workflows.v1.py` | `fa16227c…` | `5c64b593…` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `4f502929…` | `29809f35…` |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `77e885a6…` | `027dce36…` |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `b1fff36d…` | `82745fa9…` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `efdcf8ef…` | `bb41cde2…` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `92d396d8…` | `d3c6e698…` |

Full digests: `results/changed-files.json`. No file added or removed (8654 before, 8654 after).
Source overlay carrying **only** these 9 files: `overlay/` — verified byte-equal to the corrected
work tree and to carry nothing else.

## Item 1 — V20-ROOT-3: REGISTERED, as root directed

**Reproduced first, independently** (`probes/p1_reproduce_unregistered.py`,
`results/p1-before.json`): of the 36 DomainDetail codes `workflows_model.v1.py` emits, exactly two —
`BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER` and `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`, both from
`verify_scope_parameter_binding` on `REQUEST.PRECONDITION_FAILED` — were in neither
`public-detail-registry.v1.json` records, nor the mirrored `DomainDetailCode` enum, nor
`internalAliases`, and the real carrier `common.schema.json#/$defs/StepTermination` **REFUSED** both.
The probe's live-validator control is non-vacuous in the same run: two registered codes ADMIT and an
invented one REFUSES.

**Disposition: minimal explicit registration**, which is what the owning contract supports.

- These are not internal decision keys. They are passed as `Refusal.detail` and land directly in the
  public `DomainDetail.code` position via `Refusal.termination()`, under the same `BASELINE.` public
  namespace as seven already-registered codes emitted by the same module the same way. The registry's
  own `aliasRule` reserves `internalAliases` for keys that *may not* appear as a public
  `DomainDetailCode`; these are the opposite case. So an alias was not available and a remap was not
  indicated.
- The two conditions are genuinely distinct next steps for a caller — *state a scope parameter* vs
  *supply the one already selected* — so collapsing them onto one existing code would delete real
  information and silently rename two published outputs.
- `CONFIG.INVALID` for the new ambiguity is untouched, and no third `BASELINE.SCOPE_*` spelling was
  created.

**What was edited.** Both codes added to `records` (owner `workflows`, selector
`workflows/schemas/common.schema.json#/$defs/DomainDetailCode`) and mirrored exactly into the
`DomainDetailCode` enum — both lists were byte-identical sorted code lists before and remain so,
which is what `check-integration.py`'s `public-detail-registry-schema-parity` enforces (287 → 289).
A `scopeBindingDetailsRegistered` statement records what was registered and why, placed **beside**
`newInThisCorrection` rather than inside it, so the earlier four-member account keeps its exact
words. Consumers updated: the two `len(PUBLIC_CODES)==287` drift guards in `check-identity.py` and
the `287-member registry` comment in `check_workflows.v1.py`. The emission site in
`workflows_model.v1.py` gained a comment stating the law; **no executable line of
`verify_scope_parameter_binding` was touched**, so every class, error code, detail spelling, remedy
string, order and reachability is preserved.

**Normative prose** (`identity-and-evidence.md`, *Where the binding is actually decided*): the old
sentence said the conditions "each refuse with their own typed reason" without naming them and
without saying they were carriable — and two of them were not. It now names both codes, both
carriers, and both meanings, and corrects a third point: *a row cited under another schema is not a
separate reason*, because the verifier filters candidates by schema digest, so such a row leaves none
and meets the missing-selection refusal.

**Controls added** (in `check-identity.py`, beside main's existing block — 20 new checks). Not
register-string assertions: they take the **actual `Refusal` objects** the direct verifier raises,
project them through the model's own `termination()`, and validate against the real carrier and
against a full `kind=failure` `CommandEnvelope`. They also run `adopt_baseline` — the caller the
contract names — for real, and prove the refusal propagates out of it with detail intact and reaches
the same two surfaces from there; a positive case (the selected document) shows those controls
measure the binding and not some unrelated precondition. Negatives on both surfaces use
`BASELINE.SCOPE_PARAMETER_AMBIGUOUS`, a name this correction deliberately did **not** register.

**Counterfactual, to prove the controls are real** (`probes/p3_counterfactual_unregister.py`,
`results/p3-counterfactual.json`): in a disposable clone with **only** the registration reverted and
nothing else, `check-identity.py` exits 1 with 8 named failures, including
`both-direct-verifier-terminations-are-admitted-by-the-real-public-carrier-schema`,
`both-scope-binding-refusals-compose-a-schema-admitted-failure-envelope` and
`both-adopt_baseline-refusals-reach-the-real-carrier-and-the-failure-envelope`.

## Item 2 — V20-ROOT-4: REAL, and corrected

Main classified it advisory. **It is a real public route gap**, measured
(`probes/p2_duplicate_capability_route.py`, `results/p2-before.json`):
`public_termination_for("DUPLICATE_REQUESTED_CAPABILITY")` and `failure_envelope_errors(...)` both
refuse `native.public-route-key-unregistered:…`, so this refusal had no derivable public termination
at all.

**Origin and reachability, traced rather than guessed.** `default_capability_selection` builds one
row per (unit, default capability) and refuses when two rows share their ownership tuple — i.e. when
two units share `(rootPath, languageMode)`. Running the **actual** discovery instrument
`discover_units` over a marker set built specifically to collide (a directory with both `Cargo.toml`
and `package.json`; a directory with `tsconfig.json` + `jsconfig.json` + `package.json`; an
`allowJs` tsconfig against a jsconfig elsewhere) yields **no** duplicate `(rootPath, languageMode)`
pair — `by_dir` is keyed by directory, at most one rust and one tsjs unit per directory, and their
modes are disjoint — and the resulting default selection succeeds. **So it is a host invariant over
the default path, not something an admitted repository can provoke**; it is reachable in practice
only from a host bug or a hand-built units list.

That does not make it advisory, and here is the decisive evidence: the route registry **already
registers this exact condition** as `native.requested-capability-duplicate-ownership-tuple`, and its
`host-generated-internal-layer` branch was written verbatim for this call site — *"a host BUG minting
its own invalid internal layer — **default construction that emitted two rows for one cell**"*. The
guard at that very call site was raising a private name instead, so the registry's own
host-generated route was reachable from nothing. The registry also asserted *"exact whole-item
duplicates never reach here — uniqueItems and the canonical-set order law refuse them first"*, which
is true on the explicitly-supplied-spec path and **false** on the default path, because this guard
runs before `admit_analysis_spec`.

**Correction: name the registered key.** The guard keeps its position, keeps refusing, and still
never dedupes; it now detects on the ownership tuple and raises
`native.requested-capability-duplicate-ownership-tuple:<capabilityId>:<languageMode>:<workspaceRoot>`.
For these rows the two detections coincide exactly — `default_capability_selection` writes
`required: True` literally on every row, so a byte-identical duplicate and a tuple duplicate are the
same set — and the emitted subject now matches `admit_requested_capabilities` format, so the two
guards cannot drift in what they publish. **No origin is guessed here**: the helper emits the key
alone and the host calls `public_termination_for(key, origin)`, exactly as `helperDoesNotGuessOrigin`
requires of every other guard.

The position is kept deliberately: `requestedCapabilities` is `uniqueItems`, and measured
(`results/p2-before.json` → `sameRowsAtWholeSpecBoundary`) the schema's answer for these rows is a
generic `ValidationError` restating the whole instance — the same reason the cardinality guard
precedes generic validation.

**Not done:** registering `DUPLICATE_REQUESTED_CAPABILITY` as a second route row. That is a parallel
vocabulary for one condition, and `aliasRule` / `aliasMapIsContextFree` forbid a context-free alias
for an origin-dependent key, so a duplicate full route row was the only alternative shape.

The registry's reachability sentence and both prose paragraphs in `native-evidence.md` are corrected
to state what actually happens on each path. Controls: the two existing `rejects_because` consumers
now assert the registered key with its tuple subject; new controls take the **actual**
`AdmissionError` the real call raises through `normalize_internal_key`, `public_termination_for` and
`failure_envelope_errors` for all three origins and validate the composed terminations and failure
envelopes against the real workflows schemas; laundering into an impossible origin still refuses; and
the bespoke key is proven still underivable as a public route.

## Item 3 — V20-ROOT-5: assessed, currently correct, constraint kept

`PUBLIC_ROUTE_REMEDIES` keyed by public code is a **maintenance constraint, not a wrong current
output**. Item 2 routes a third path to the same key and therefore the same three codes, and each
remedy is true of it: `CONFIG.INVALID` and `native.capability-spec-invalid` both already state the
`(capabilityId, languageMode, workspaceRoot)` condition after the earlier widening, and
`HOST.INVARIANT_VIOLATED` — *"the host produced an invalid internal record"* — is exactly what a
default construction emitting two rows for one cell is.

**The table is not re-keyed.** Instead the constraint is promoted from a Python comment to a
normative `remedyKeyingConstraint` statement in the route registry, and given a **total** control:
every registered key × every declared origin composes envelope errors, every emitted code is a
closed-registry member, and every emitted remedy is exactly the table's entry for that code — which
is what "keyed by code" means. The sharing is measured rather than assumed, so the constraint has
teeth where codes really are shared.

## Executed results — real commands, real exits

All checkers run with `/tmp/opensip-architecture-review-env/bin/python -I -B` (3.12.13).

| checker | before | after | gate |
|---|---|---|---|
| `foundation/check-identity.py` | exit 0 — 1548 passed / 0 failed | exit 0 — **1591** passed / 0 failed | run directly, **no pin gate** |
| `workflows/check_workflows.v1.py` | exit 0 — 1803 / 1803 | exit 0 — 1803 / 1803 | run directly, **no pin gate** |
| `check-integration.py` | exit 0 — 412 / 0 failed | exit 0 — 412 / 0 failed | run directly, **no pin gate** |
| `native/check_native_evidence.v2.py` | exit 0 — 375/375 | exit 0 — 375/375 | **disposable repinned clone only** |
| `security/check-security-lifecycle.v1.py` | exit 0 — 456/456, 10 sweeps | exit 0 — 456/456, 10 sweeps | **disposable repinned clone only** |
| `workflows/run-reference-checks.py` | exit 0 — passed | exit 0 — passed | **disposable repinned clone only** |

**Failures I hit and fixed, recorded rather than smoothed over.** The first run of the item-2
controls failed 2 of them (`results/mid2-identity.stdout`, exit 1):
`the-bespoke-unregistered-key-is-gone-from-the-model-source` — my control grepped the whole source
and the replaced key is still *named once*, in the comment recording why it was replaced; retargeted
at the `raise`, plus a control that it is still underivable as a route.
`the-default-path-and-the-vocabulary-helper-publish-one-vocabulary-not-two` — I had asserted the two
raw strings equal; they differ by `capabilityId` because the default selects the whole matrix. That
assertion was asserting the fixture, not the vocabulary; it now asserts the same key and the same
3-part subject shape.

**One file I clobbered and restored.** Running `check_native_evidence.v2.py` directly in `work`
made it write its pin-failure result over the canonical `native/native-evidence-report.v2.json`
(97459 → 3925 bytes). Restored to the exact parent bytes `5f31c119…` and re-verified; it is **not**
in the changed set. That is why the pin-gated checkers are run only in disposable clones.

## Pin standing — unchanged and still root's

**No pin in `work` was edited and no pin match is claimed for the delivered bytes.** The four
ledgers already disagreed with the parent bytes before I touched anything — the before-baseline
repin rewrote 9 / 10 / 10 / 10 digests in foundation / native / security / workflows. My correction
adds two more per ledger (11 / 12 / 12 / 12). Every pin-gated result above was obtained in a
throwaway `cp -Rc` clone that was repinned there and nowhere else.

## Findings dispositions

| id | disposition |
|---|---|
| **V20-ROOT-3** | **CORRECTED.** Reproduced independently, then registered both details with mirrored enum/registry, consumer updates, normative prose, and 20 controls proven non-vacuous by counterfactual. |
| **V20-ROOT-4** | **REAL, CORRECTED.** Main classified it advisory; the route gap is measured and the registered key's own host-generated route was written for this call site. Reachability honestly bounded to a host invariant, evidenced by the actual discovery instrument. |
| **V20-ROOT-5** | **ASSESSED, currently correct; constraint kept and made enforceable.** No table redesign. |
| V20-ROOT-1 (pins) | **NOT MINE, untouched.** Confirmed still open and now slightly larger; measured above. |
| V20-ROOT-2 (stale generated reports) | **NOT MINE, untouched.** Still open; see follow-ups. |

## Required follow-ups (root)

1. **Pin seal.** Five ledgers now disagree by construction, including the 9 files this correction
   changes. Root reseals after integration; I refreshed nothing.
2. **Regenerate the stale canonical reports.** V20-ROOT-2 stands and widens: `validation-summary.v1.json`
   still says foundation identity 1431, native 355, workflows 1795 against current 1591 / 375 / 1803,
   and `native/native-evidence-report.v2.json` + `workflows/workflows-report.v1.json` are delivered at
   their accepted-19 bytes. I deliberately did not regenerate any of them.
3. **`d9-exit-contract` successor** — the pre-existing `successorArtifactObligation` for the
   `host-invariant` faultCause is untouched and still live; item 2 makes that route reachable from one
   more call site, which strengthens rather than changes the obligation.
4. **Merge and assess all bytes** of `overlay/` — the 9 changed files only.

## Bounded limitations, stated plainly

- Every probe is a **helper, schema, closure or invocation** probe over the design source in my
  disposable copy. **None is a product qualification**, none runs a product host, a compiler, a
  provider, Cargo or repository code, and nothing here authorizes implementation or readiness.
- The item-2 reachability finding is bounded to what I measured: `discover_units` over marker
  inventories including deliberately colliding ones. It is a structural argument (`by_dir` keyed by
  directory; one rust + one tsjs unit per directory; disjoint modes) supported by an executed case,
  **not** an exhaustive proof over all marker inventories.
- No full-design review, no six-checks re-run, no independent-20 / blind-9 / full-application work is
  claimed or attempted here; those follow the final merged source and pin seal.
- The three earlier source gaps and the stage/schema declaration work are outside my scope and I did
  not assess them.

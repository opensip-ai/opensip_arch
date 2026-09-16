# Review: envelope6 pre-Run interruption form (m1-interruption-envelope-subject-01)

**Reviewer:** actual Claude (claude-opus-5), fresh and independent. This is a scoped design/reference review.
**Verdict:** **accept-conditional.** This is not a promotion.

The single delta at `/allOf/19/then` correctly and minimally expresses the owned D9 `interrupted` class (130) for an invocation interrupted before any committed Run. It is strictly additive, and the gap RP-OBL-C01 is real. The acceptance holds only under these conditions:

- The parent envelope5 is still an **unaccepted report04 candidate**.
- **F1:** owner prose must be amended with the selection.
- **F2:** host admission must refuse Run erasure.
- **F3:** the after-commit carrier claim for query-class commands is unverified.

## Pins
- Manifest SHA256 `76897423…71bf` verified. The file set is 40/40 exact on the original and on the reviewer copy, both before and after execution.
- All 34 input pins match their named source paths (sha256 and bytes).
- Environment: the reference env with `python -I -B` (jsonschema 4.25.1, CPython 3.14.6), using its own TMPDIR. No bytecode was written.
- The root `check.py` ran in the copy, exited 0, and its output equals `root-result.json`: 42 probes, 43 fixtures, 15 positive controls.
- Read-only material from outside the manifest was used only for owner-valid probe payloads: report04 `fixtures.json#/deliveryGoldens/24/envelope` and `#/bases/candidates-run/envelope`.

## Independent delta
I diffed v5 against v6 myself. Only `$id`, `title`, `description`, `schemaMajor.const` and `/allOf/19/then` differ.
- The old `then` is byte-equal as `oneOf[0]`.
- The two alternatives are mutually exclusive by termination class, so `oneOf` is the same as `anyOf` (confirmed by mutation).
- `allOf` entries 0–18 and 20–22 are unchanged.

## Is the gap real?
Yes. In envelope5:
- `kind=failure` requires `errors` (allOf/3).
- `errors=[]` forces `REQUEST.UNKNOWN_OPTION`, exit 2 and diagnostics (allOf/19).
- None of the 315 `DomainDetailCode`s names an interruption or cancellation. 314 of them *are* shape-admitted beside an interrupted termination. So the only v5 route is an unrelated detail, which the owner forbids ("explanatory detail beside an existing code, never a termination code", workflows-and-surfaces.md:1367).
- An UNKNOWN_OPTION envelope with an "interrupted" diagnostic is admitted, but it misstates class, code and exit.

The other kinds can't carry it either:
- `run` and `doctor` need their payloads, and a fabricated run envelope before a Plan/Run is forbidden (:1344).
- `query` and `mutation` need their records.
- `meta` forces success/0.
- `invocation` needs a full invocation:3 record and is not bound as a general aggregate carrier. That is owner reading, not a schema proof (O2).

## Owner law
- **D9 (:1355–1364):** interrupted ⇒ 130 and a signal, with runId only after a commit. The new form fixes class, D9Signal and 130, and has no runId. StepTermination still applies on top.
- **Cancellation (:224–228):** before-settle ⇒ interrupted; after-settle is never reclassified. Phase isn't visible in the envelope, so the host owns the selection, and the contract says so.
- **report04 aggregate `{interrupted, signal, runId?}`:** with no committed analysis this is exactly `{class, signal}`. Closing `executionId`, `authority`, `coverageId` and `domainDetail` is correct, and that narrowing applies only to the new form.
- **Ledger:** `stepResults` and `Cancellation` are untouched. No new code, detail, kind, identity, class or signal is added.

## Independent probes (`work/probes.py`, 80 cases, all pass)
**Admitted:**
- All 3 signals in v6 (all refused in v5).
- The form with `clientCorrelationId` (128 chars), `projectId` and `projectRoot`.

**Refused in both majors:**
- `null` for errors, clientCorrelationId, projectId, requestId, termination, exitCode, kind and signal.
- clientCorrelationId empty or 129 chars.
- `errors:{}`, termination as an array, an unknown top-level key, kind absent.

**Refused on the new form:**
- Termination extras: runId, executionId, authority, coverageId, domainDetail, errorCode, phase.
- Exits 0, 2 and 4.
- Every other class at exit 130.
- `errors=[]` under each other kind.
- Hybrids between UNKNOWN_OPTION and interruption.

**UNKNOWN_OPTION branch:** admitted in both majors. Its mutants (missing or empty diagnostics, exit 4, another code, added signal, added run) are refused in both.

**Bytes:** a duplicate `errors` key and `130.0` both raise AdmissionError.

**After commit:** the interrupted `kind=run` golden, with runId, is admitted in both majors. Adding `errors=[]` is refused. `kind=failure` keeping runId is refused, even with every payload stripped.

**Superset:** over 46 values (43 fixtures, base, UNKNOWN_OPTION, golden), no v5-admitted value is refused in v6. The only v6-only value is the new form.

## Mutations
**Killed:**
- Drop the `not` clause.
- Drop the termination `additionalProperties:false`.
- Drop exit const 130.
- Set alt1 diagnostics minItems to 0.
- Drop alt2.
- Remove availability, findings, query or diagnostics from `not` (tested with owner-valid payloads).

**Surviving, each redundant with an existing constraint (defence in depth):**
- signal → any string: StepTermination still binds D9Signal.
- class → any D9Class: other classes need fields the closed object forbids.
- kind const, errors maxItems, termination required.
- run, advisoryReport, querySurface, queryRecord, meta in `not`: existing allOf entries also refuse them.

## Findings
- **F1 (medium, blocks selection).** workflows-and-surfaces.md:1340–1341 still says `kind=failure` requires a **nonempty** `errors`. The pinned owner text doesn't mention the existing UNKNOWN_OPTION exception either. The integration duties include no owner-prose amendment. Add one naming both empty-errors forms, the before-settle/no-committed-Run condition, and the ban on dummy Runs and invented details.
- **F2 (medium, integration).** Shape can't detect Run erasure. The interrupted Run golden, rewritten as the new form with run and runId dropped, **is admitted by v6**. Name an envelope host-admission join, for example by extending `J-ENV-TERMINATION-RUN`, that refuses the new form when the ledger records a committed Run or a phase other than before-settle. Add refusal goldens. `J-LEDGER-AGGREGATE` covers only report-bearing documents.
- **F3 (low-medium).** The "existing Run-bearing interruption carrier" is shown only for `kind=run` (fit). Query-class commands that commit a Run and then run a query step (candidates-run, inspect-run, review-brief-run) have no demonstrated interruption carrier. Show that `kind=run` is lawful for them, or record a separate obligation. Do not widen the new form to runId.
- **F4 (low).** The root's `new-form-no-{run,meta,query,availability}` probes use placeholder `{}` payloads that fail their own schemas, so they don't show the `not` clause is load-bearing. Use owner-valid payloads when rebasing. retentionDisclosure and agentHints remain untested with valid payloads.
- **F5 (low).** Provenance: the parent is the report04 candidate path `m1-report-projection-subject-04/owner`, which is not a product owner path. Keep "conditional on unaccepted envelope5" in every downstream record. If report04 changes envelope5, rebind the parent sha256 and redo the restoration check.

**Observations:**
- O1: `projectRoot` is permitted, as on the existing failure forms.
- O2: `kind=invocation` was excluded by owner reading, not by a schema proof.
- O3: pinning exit 130 in schema is stricter than the host-checked pairing used elsewhere, and harmless.

## Not claimed
- Acceptance or promotion of envelope5, report04 or envelope6.
- Signal handling, cancellation/delivery races or host delivery.
- Codec, runtime, browser, CLI, inventory or source integration.
- Metadata semantic admission.
- Checker confinement.

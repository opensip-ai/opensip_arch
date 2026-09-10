# v19 subject coauthor — handoff

**Role.** Actual Claude, source coauthor with Codex. Not independent acceptance. The v19 native
handoff is completed and immutable and nothing in it was altered; the only writes are under
`/tmp/opensip-design-corrections/v19-subject-coauthor.v1`. No pins, commits, governance or product
implementation. `technicalAssent.value` is `true` and is an author's assent to his own bytes.

## Is root's identified loss real? Yes — and on four independent grounds

I reproduced it from the actual producers rather than from root's result file, across all three Plan
fields **and** the two inherited bounded fields. `terminate()`'s local `dd` helper **rebuilds** a
DomainDetail from the observation field by field —
`{'code': detail, 'remedy': obs.get('remedy', remedy)}` — and never copies `obs['subject']`.
Everything else about the envelope was already right, which is precisely why neither unit's own
suite could see it.

1. **Native §14 promises the subject.** Its owning sentence is "public detail `PROJECT.SCOPE_LIMIT`
   and subject `field:count>limit` … and **the subject always names which one overflowed**." At the
   envelope a caller actually reads, it named nothing: all five bounded fields arrived as one
   indistinguishable `PROJECT.SCOPE_LIMIT`.
2. **The workflows contract names `subject` as the carrier.** "Dynamic paths or refusal explanations
   travel in bounded `subject`/`remedy` fields, **never as newly invented codes**." Dropping half
   that carrier leaves a consumer who must distinguish two overflows holding only the newly invented
   code the same sentence forbids. The loss defeats the mechanism the contract designates.
3. **The module already disagreed with itself.** `Refusal.termination()` builds the *identical*
   StepTermination shape and **does** carry `subject` when present. Two producers of one record
   disagreeing about one of its fields is the defect; the fix removes a disagreement rather than
   adding a rule.
4. **The schema was already built for it.** `subject` is an existing optional `BoundedText` on the
   common-schema `DomainDetail`, and the `evidence.pinned` branch makes it *required* there — so it
   is load-bearing published surface, not decoration.

**Scope of the defect: exactly one site.** The module's other DomainDetail carriers
(`Refusal.termination()`, and the two paths that pass a whole detail dict through) preserve it.
`dd` is the only place a DomainDetail is reconstructed field by field, and therefore the only place a
field can be dropped.

## The fix

Inside the existing `if detail:` branch, after the DomainDetail is created:

```python
if obs.get('subject'):
    t['domainDetail']['subject'] = obs['subject']
```

Two lines plus a comment block. `workflow.before.py` → `workflow.proposed.py`:

| | sha256 |
|---|---|
| before (exact frozen18, and byte-identical to the copy in the v19 native work tree I never edited) | `a268aa4b9e9089a51104365a6c82faf5b01602b84b1dd5adbf0384810e25f7bd` |
| proposed | `53ec304c692226659cea730403dd382cc2e54c7e9aea65be445672feaf129eb5` |

**No schema, code or contract change** — confirmed; `subject` is already published as optional.
It **copies, it does not admit**: a malformed trusted observation carrying a non-string or
over-length subject still yields a record the published schema refuses, exactly as it already does
for a malformed `remedy` or `detail`. A control asserts that the refusal is the schema's and not this
edit's, so no universal schema-admission claim is made.

**One deliberate divergence from root's sketch.** Root suggested `if 'subject' in obs`. I used
`if obs.get('subject'):` — the *same* truthiness test `Refusal.termination()` already uses. They are
identical for every well-formed observation and differ only on an explicit `subject: None` (which
presence-testing would copy, manufacturing a schema-invalid record out of a merely sloppy one) and
on `subject: ''` (which carries no disclosure and which the sibling also drops). Matching the sibling
is what makes the "two producers of one record agree" control true on **all three** of present,
absent and empty rather than two of them. If root prefers the literal presence test, the only
behavioural difference is those two edge shapes and I do not object; the empty-string row would then
need inverting. Recorded as `V19S-ROOT-3`.

## Probe — 59/59

`out/probes/probe-subject-preservation.v1.py` → `out/evidence/probe-result.json`. Before and
proposed models are loaded side by side from two shadow trees whose only differing file is
`workflows_model.v1.py`, so every comparison isolates the one edit. `N` is read-only from the
completed v19 native work.

**Real:** `N.admit_plan_selection_cardinality`, `N.admit_requested_capability_cardinality` and
`N.unit_scope_descriptor` are invoked and raise real `ScopeRefusal`s; `N.scope_refusal_termination`
projects them and its actual typed fields are the observation handed to `W.run_invocation`. The
returned `StepTermination`, aggregate termination, `DomainDetail` and whole `InvocationRecord` are
validated against the **published pinned schemas** via the model's own `validate_import_record`.

**Synthetic:** every invocation record, requestId/projectId, `orderedSteps` and step script is a
trusted fixture observation from `workflow-cases.v1.json`; the earlier *completed* step result is
supplied by that script, so "earlier committed result preserved" is a statement about the returned
invocation record, **not** about any Run closure. `W.synthetic_execution_id` is the module's own
declared fixture adapter. No product host, provider, compiler, OS or filesystem is executed.

Per field — `semanticClosures:129>128`, `nativeContextDigests:129>128`, `importIds:257>256`,
`requestedCapabilities:1025>1024`, `workspaceRoots:1025>1024` — the probe asserts: the exact subject
is retained **per step and in the aggregate termination**; the before model demonstrably dropped it;
exit code is 2 and unchanged; class, errorCode, detail and remedy are unchanged; the remedy is that
field's own; the refused step has **no result and no derivation**; the earlier completed step keeps
its result; the after-record **with the subject removed equals the before-record byte for byte**; and
both records validate against the published schemas.

Backward equality: **all 32** existing invocation cases run through both models are byte-identical,
plus seven `dd`-carrying observation events with no subject, plus a detailless observation that still
produces no `domainDetail`. A meta-control shows the schema validator is **live** — it admits a
well-formed detail and refuses an unregistered code, a wrong-typed subject, an over-length subject,
an undeclared property and a non-record at the invocation root selector — because a validation
control that never refuses would prove nothing.

## Durable checks — delivered, not inserted

Two small blocks for root to place; neither suite was run.

- `checks/check_workflows.subject.block.py` (8 rows) — workflow-side only, no cross-unit import.
- `checks/check_integration.subject.block.py` (8 rows) — the cross-unit seam over the **actual**
  native producer. It belongs there because native owns the refusal and its subject while workflows
  owns the envelope: each unit is correct on its own side, so only the composition can see the seam,
  which is exactly why neither unit's suite caught this.

`out/probes/verify-durable-blocks.py` establishes three things without running either suite:
**static** — every free name each block references is bound at module level by its target checker
(what catches a block that would `NameError` on integration): both resolve; **execution** — each
block is exec'd against a namespace faithfully rebuilt from the real modules (the workflows namespace
rebuilds the same schema registry that checker builds): 8/8 and 8/8; **discrimination** — both are
re-run against the **before** model and required to fail there: 3/8 and 5/8 fail. The rows that pass
on *both* models are exactly the backward-compatibility rows, which is the correct pattern.

## Limitations, including two of my own errors

- One site changed; no other observation field was audited for a similar loss beyond confirming that
  `dd` is the only place a DomainDetail is reconstructed field by field.
- The six suites and the pin gate were **not** run, per instruction. Backward equality rests on the
  32 invocation cases, not on a suite result.
- The durable blocks were verified by static resolution plus faithful-namespace execution — weaker
  than a real suite run, and stated as such.
- **My first shadow tree symlinked `integration-host-model.py`**, whose `Path(__file__).resolve()`
  followed the link back to the unpatched module, so the integration block was briefly graded against
  the wrong bytes and correctly failed. Both trees now hold a real copy, and I turned the accident
  into the deliberate discrimination control above.
- **My first name-resolution analyzer** reported six of a block's own locals as unresolved because it
  reused the module-level collector for the block's own side. Fixed to walk the whole tree; both the
  failure and the fix are preserved in the probe.

**Root owns:** integrating `workflow.proposed.py` and resealing the ledgers that carry it, placing
the two blocks, and the truthiness-versus-presence decision (`V19S-ROOT-1/2/3`).

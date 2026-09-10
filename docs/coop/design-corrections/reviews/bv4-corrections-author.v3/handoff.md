# bv4-corrections-author.v3 — handoff

Focused third pass closing the two remaining publication joins. Root recorded
**ASSENT-TO-SUBMITTED-SOURCE** (`technicalAssent: true`, `finalSourceAssent: true`)
on the exact bytes of `review-ready.v5.json`. That is **coauthor technical assent
only** — not independent, blind or application acceptance, not user approval, not
readiness, not product qualification. **Source is unchanged after that assent.**

`sourceRoot = /tmp/opensip-design-corrections/bv4-corrections-author.v3/work`
v1, v2, the frozen v13 subject and `d9-exit-contract.v1.14.json`
(`8dd3303855f49bfd…`) are all untouched.

---

## The two items

### CX-BV4-DEFAULT-PUBLIC-CARRIER

`selection-account-only` named a Python helper **return**, not a published
carrier, and `AnalysisResult` is a closed union that refuses an added property.
Correcting it exposed four more defects across the checkpoints, each reproduced
by root on my exact bytes: the projection **discarded `workspaceRoot`** (four
distinct ownership tuples collapsed to two details); there was no carrier for
**multiple** absences in the original invocation; the flat 1024 bound is **per
analysis-spec, not per invocation** (two admitted 1023-request selections compose
2046 and refused); the typed notice admitted **any** `DomainDetailCode`; and
envelope membership is **not** declared parity, so the collection reached only
JSON and agent.

Selected law: `CapabilityAvailabilityNoticeV1` carries the complete ownership
tuple in **typed fields** — never concatenated, because `workspaceRoot` is a
`UserInputPath` bounded at 4096 while `BoundedText` is 1024 — with `code` a
**const** `native.capability-unavailable`, an existing registry member.
Composition is **per step** (`{stepId, noticeCount, notices[≤1024]}` inside
`{stepCount, totalNoticeCount, steps[≤64]}`) on `CommandEnvelope.availability` in
the original invocation, so nothing is discarded and no invocation-wide request
cap is invented. A step that made no selection contributes no entry; one that
found nothing absent contributes an **empty** entry; a retried step contributes
one; the same tuple may recur across steps.
`capability-availability` is a **declared** parity field of **every**
`requestClass: analysis` command — all five, including `repair-verify` — and
declared means required. Advisory throughout: no Coverage, no Control verdict, no
repair authority, never a fabricated clone `Candidate`.

**A regression I introduced, and fixed.** I had added `if k in envelope['parity']`
to `render` so an old fixture would keep passing. That silently weakened the
inherited required-field behaviour for *every* parity field — a missing
`required-coverage` simply vanished from all five formats. Strict access is
restored with the reason recorded in the code; §8's existing conversion stands
(`operational-failed` / `DELIVERY.REQUIRED_FAILED` / `delivery-required`, RunId
retained; the helper exception alone is not a public termination).

### CX-BV4-PUBLIC-ROUTE-COMPLETE

**14 of 16** branch targets were prose that the real `DomainDetail` schema
refuses, none of the keys was in `internalAliases`, my `recordsEditOwnedByRoot`
claimed otherwise, and **my own control whitelisted `request detail` /
`operational record` prefixes so it could not fail**. Then: a `kind=failure`
envelope requires a **nonempty** `errors` array, so routes leaving `domainDetail`
absent refused; guard output is colon-suffixed with no normalizer; the `preview-*`
guard emitted prose; and a 4096-character mode produced a 4149-character subject
that made the envelope schema-invalid.

Selected law: `public_termination_for(key, origin)` derives a real
`StepTermination` for every branch and `failure_envelope_errors` composes the
required array — exactly the termination's detail where it has one, the route's
`envelopeDetail` where it does not. Origins follow admission §1 and the inherited
D9 law: external configuration → `CONFIG.INVALID`; externally supplied or
retained spec of *known* external origin → `REQUEST.PRECONDITION_FAILED`; a host
**bug** minting its own invalid internal layer → `operational-failed` /
`SYSTEM.OUTCOME.ILLEGAL_STATE` with `faultCause: host-invariant` (rule 5,
`domainCondition: host-fault`); authenticated release declaration →
`REQUEST.PRECONDITION_FAILED`; producer boundary → `PROVIDER.PROTOCOL_VIOLATION`.
A `NOT-SELECTED` cell is **origin-independent** (`REQUEST.UNSATISFIABLE` with the
existing `PROVIDER.NOT_SELECTED`). Each key declares the boundaries it can arise
at and refuses any other. `normalize_internal_key` matches the longest registered
key before a colon; every guard now emits a **registered** key, `preview-*`
included. `bounded_subject` elides over-long subjects with the **units stated**:
`raw` is a Unicode scalar string, length and slicing count **code points** (what
`BoundedText`'s `maxLength` counts), the SHA-256 input is `raw.encode("utf-8")`
with no normalization, 64 lowercase hex after the ASCII marker `...#sha256:`,
result exactly 1024 code points — under the **ordinary collision-resistance
assumption**, with the guarantee confined to what is published and **no retained
store promised or named**.

Four public `DomainDetailCode` members **are** added — `native.capability-spec-invalid`,
`native.release-declaration-invalid`, `native.coverage-cause-unsupported`,
`HOST.INVARIANT_VIOLATED` — because those routes had no code naming their remedy;
reuse was taken where honest. Registry and generated enum are in lockstep at 287.
Only the two genuinely **context-free** keys are aliased, and the `aliasRule` now
says a missing alias is a positive statement.

**The selected D9 composition** is published in product source: inherit v1.14
**unchanged** plus exactly `faultCause: host-invariant` → the **existing**
`SYSTEM.OUTCOME.ILLEGAL_STATE`. Root corrected two claims of mine and both are
retracted in the source: `total and injective` is a property of the **declared
cause domain**, so an orphaned error code was never a totality violation; and
only the host-**invariant** subtype was unrepresentable — other host-fault causes
always existed. Existing classes, exit codes, reason codes and error codes are
unchanged, but `faultCause` **does** grow by one, and saying otherwise would be
false.

---

## Root's editorial proposal — my position

I read `root-publication-shorthand-proposal.py` in full and **agree with all
three**; I did not run it and did not edit source after assent. All three anchors
occur **exactly once** in the released bytes, so it applies cleanly.

1. **`release_absence_notices` leaf before `stepId`** — agree. The helper returns
   `{noticeCount, notices}` and does *not* carry `stepId`; `invocation_availability`
   adds it. The current sentence attributes the `stepId`-bearing type to the
   helper that does not produce it.
2. **List all five analysis commands** — agree, and I flag this as a residual
   **inconsistency rather than shorthand**: native §1.4 still names four while the
   command inventory, workflows §8 and the retained controls all carry five. Two
   current statements of one law disagree, which is the same class of defect this
   pass corrected elsewhere. The fix adds no behaviour.
3. **Name the typed notice in `CommandEnvelope.availability`** — agree. The
   carrier is `CapabilityAvailabilityNoticeV1`, not a generic `DomainDetail`.

Root owns these before final pins. My assent covers the bytes root assented to
and does not extend to later bytes.

---

## Delta

**Aggregate vs frozen v13 — 19 files, 0 additions, 0 deletions** (v1+v2+v3, the
complete set for eventual direct integration; per-file
`beforeSha256`/`afterSha256` in `handoff.json`).
**This turn vs released v2 — 12 files**, `v2Sha256`/`finalSha256` in
`handoff.json`; before-images for all twelve are in `before-images/` and each
equals the v2 released byte.

Released work contains no source-pin change, no generated report, no validation
summary, no readiness or crosswalk record, no historical artifact change, and no
added or deleted file.

## Final checks — once, on the final bytes

Fresh disposable copy `disposable/suite-final-v6`, explicit measured temporary
repin (34 entries over 19 files); **no earlier suite directory was overwritten**.
These pins are a **development instrument, not accepted pin evidence**.

| script | exit | result |
|---|---|---|
| `check-foundation.py` | 0 | 231/231 |
| `check-identity.py` | 0 | **1282 passing calls, 0 failed** (1203 at v2) |
| `check-product-quality.py` | 0 | 24/24 |
| `check-product-configuration.py` | 0 | 28/28 |
| `check-array-orders.py` | 0 | 65/65 |
| `check_workflows.v1.py` | 0 | 1598/1598 |
| `check_native_evidence.v2.py` | 0 | 347/347 cases; 66 cells; 0 open objects |

The released and suite copies differ in exactly three files: the two temporarily
repinned manifests and `native-evidence-report.v2.json`, regenerated *inside* the
disposable copy. **20 disposable roots** are declared in `handoff.json`.

## Checkpoint account

Five checkpoints. Root raised **1 + 3 + 6 + 3 + 1** findings; every one was read
in full, agreed and corrected, and **none was contested**. Two were defects I
introduced in this same pass — the `render` required-field filter, and a control
written so it could not fail. Root also corrected its own prior feedback twice
(the `repair-verify` format list; a hardcoded 950-character prefix that should
have been 949), and both are recorded as root stated them; neither changed my
source, because my controls iterate each command's own declared formats and
compute the prefix from the formula.

## Probe honesty

`p1_route.py` and `p2_envelope.py` are **composition** tests over representative
strings and now say so in the files; `p3_actual_guards.py` **invokes** the guards.
The distinction is carried into the control names
(`every-representative-guard-string-…` versus `every-ACTUAL-guard-refusal-…`),
because only the latter catches a guard that emits prose — which is exactly how
the `preview-*` defect was found.

## Limits

No product exists to measure and none was assumed; every compiler, grammar,
provider, release declaration, permission value, renderer and host behaviour is a
**synthetic** trusted input. Schema admission is not host execution: no real CLI,
renderer, agent surface or D9 interpreter was run and no Run was closed from
content-derived evidence. Passing-call totals are development evidence under
temporary pins — not the six pinned commands, not distinct-case counts, not
qualification. The successor D9 **artifact** is not written here; the historical
bytes stand and that divergence is deliberate and named. Six failed attempts and
their logs are retained in `handoff.json`.

Root owns: complete custody, final integration assessment, the three editorial
reconciliations, records **before** pins, pin seal and freeze, the six pinned
commands, fresh independent review, a **new** blind reconstruction, and full
independent application review.

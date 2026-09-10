# bv4-corrections-author.v4 — handoff

Narrowly bounded publication follow-up against frozen **v14**
(`45b1e128ca51d114…`, 6047 files). Root recorded
**ASSENT-TO-EXACT-COAUTHOR-SOURCE** (`technicalAssent: true`) on the exact bytes
of `review-ready-3.json` (`73dc744b57ba1945…`). That is **root technical source
assent only** — not independent review, not blind reconstruction, not application
acceptance, not readiness, not product qualification, not user approval.
**Source is unchanged after that assent.**

`sourceRoot = /tmp/opensip-design-corrections/bv4-corrections-author.v4/work`
Frozen v14, the live repository, v1–v3, history, pins, generated reports and
readiness records are all untouched, and `identity-model.py` was never edited.
These corrections **do not mutate v14** — they need a successor freeze and
review. The concurrent independent session on immutable v14 was never accessed,
influenced or impersonated.

**Delta: 5 files changed, 0 additions, 0 deletions.** Per-file
`beforeSha256`/`afterSha256` in `handoff.json`; a before-image for every one, and
each equals the frozen v14 byte.

---

## The two items

### CX-V14-ADMISSION-AVAILABILITY-MIRROR — confirmed

Admission §1.1 still named the checkpoint-1 carrier — a singular `DomainDetail`
via `DoctorResult.defects[]` or `StepTermination.domainDetail` — after v3
superseded it in native §1.4 and workflows §8; and the same section *opened* by
saying the release registry supplies the **exact applicable** capabilities,
contradicting its own later sentence that the registry states availability, never
scope. Both now mirror the selected law: the absence is delivered **in the
invocation that selected it**, on `CommandEnvelope.availability`, as a
`CapabilityAvailabilityV1` whose per-step notices carry the complete ownership
tuple in **typed fields** including the unit's own `workspaceRoot`; a declared
parity field of **every** `requestClass: analysis` command; advisory throughout.
The registry declares **availability** and does not fix request scope — the
matrix does.

Correcting the prose was not enough. Root found two authoritative-looking
definitions a consumer would actually look up still describing the superseded
route: the `x-opensip-public-route-registry` `operationalCarrier` annotation, and
the `release_absence_details` docstring — which additionally claimed a
composition that does not happen, since `invocation_availability` calls
`release_absence_notices`, never that helper. Both are corrected. The legacy
helper is **retained** as an explicitly non-authoritative compatibility
projection; no API was removed, and the generic environment note is *limited*
rather than denied.

### Default-cardinality boundary — a real, narrow, reachable gap

`workspaceRoots` admits 1024 unit roots while the matrix-fixed default requests
11 capabilities per TypeScript unit, so **93 units fit at 1023 rows — one under
the bound, not exactly at it — and 94 do not, at 1034**. Units 94…1024 were an
ordinary band the scope law *admits* and the default analysis could not express,
and the only outcome was a generic `ValidationError` of 265 492 characters naming
no field, count or limit. Not default-only: an explicitly supplied over-long spec
hit the same thing. No existing law owned it and no earlier refusal fired.

New narrow owning pre-Plan helper `admit_analysis_spec` is **the** boundary for a
complete spec, defaulted or explicit, in a published order: **bounded selection
cardinality first — conditional on the field actually being a JSON array in an
object — then generic schema validation, then the closed native vocabulary.** An
oversized valid array refuses **typed**: `request-rejected`, exit 2,
`REQUEST.UNSATISFIABLE`, public detail `PROJECT.SCOPE_LIMIT`, subject
`field:count>limit`, composing a schema-admitted `StepTermination` and complete
failure envelope.

Deliberately **not** done: nothing truncated, no capability dropped, the
matrix-fixed default unchanged, no sharding or raised bound, no extra steps
executed, **not** classified as a host defect (the host computes the default
correctly; the *request* cannot be served within a published bound), no new
public detail code — the registry stays at 287 — and no retained-corruption
classification broadened.

**The judgement call.** Reusing `PROJECT.SCOPE_LIMIT` was contestable and I put
both sides at the first checkpoint rather than defending it. Root agreed the
reuse is appropriate *because* the widened meaning and the pre-Plan owning
boundary are explicit in the same change: the published law now names **four
bounded fields across two record families**. **New behaviour, stated plainly:** a
condition that previously escaped as an untyped exception now refuses typed, and
the boundary runs vocabulary admission at *request* time for an explicit spec.
No previously admitted input is now refused.

---

## Defects I introduced, which root found

**The serious one.** `admit_analysis_spec` indexed `requestedCapabilities` and
took its length **unconditionally**, breaking the very promise its new paragraph
made. Root ran 17 independently selected cases on my halted bytes: 12 held and
**five failed** — one missing field (`KeyError`), three non-length scalar types
null/boolean/integer (`TypeError`), and one **oversized string**, which was
published as 1025 capabilities with a full typed refusal and a schema-admitted
failure envelope. That last one is a public misclassification of a malformed
record as a scope limit — introduced by me while removing a different
misclassification. My controls missed it because they exercised only well-formed
specs; a boundary tested only with valid input is not tested.

Fixed: the precheck is conditional on an actual list inside an object, every
other shape reaches the schema untouched, and nothing is coerced. Eight
malformed/missing-field controls now assert `ValidationError` rather than merely
*not* a `ScopeRefusal`; a no-coercion control compares against a snapshot taken
**before** the calls so it can actually fail; and two controls cover a case root
did not test — an actual 1025-item array of malformed items still refuses typed,
because the count is genuine, while the same items within the bound refuse on the
schema. **All 17 of root's cases now hold**, verified by root's own unmodified
probe bound to the final checkpoint.

**A claim retracted.** I said the earlier guard placement *would* have been
reached on an oversized retained payload and *would* have reclassified corruption
as a request refusal. That goes beyond the evidence: `admit_run` obtains the
retained spec through `payload(digest, "analysis-spec")`, which schema-validates
it before the vocabulary helper is invoked, so an oversized retained array
refuses there and never arrives. The subclass relationship I cited is real; a
real subclass relationship on an unreachable path is not a defect. Retracted in
both docstrings, the published paragraph, the control comment and the probe
comment — replaced by two controls that **measure** the ordering.

**Evidence inaccuracies in my own checkpoint 1**, all found by root: "two arrays"
where there are four fields across two record families; 93 units described as
fitting *exactly*; a report path recorded for the native checker, which ignores
`--report` and writes in-tree; four argparse failures recorded for
`suite-final-v4a` when it was **three** argparse failures plus one **pin
mismatch**; and an accidental write described as outside `work/` when it was
inside it. All corrected additively; the original checkpoint is preserved.

**One custody slip.** Invoking the native checker with `--help` inside `work/`
rewrote its in-tree PIN-MISMATCH report — the same trap as v1. Caught by a full
6047-file manifest drift audit, not by noticing; restored byte-exact and
confirmed by re-audit. Root noted the identical failure bytes were preserved in
the retained failed attempt and that this is not a custody blocker; I am not
dressing it up as one.

## Root's additive clarifications

1. My checkpoint-3 limits said *six* malformed shapes were broken; root measured
   **five** failing cases. This handoff uses the exact five. Checkpoint 3 is
   preserved unchanged; no source edit and no rerun were needed.
2. Root reconstructed and retained the pre-amendment `p4` bytes (`e21b4c9c…`),
   independently SHA-matching checkpoint 2, in
   `bv4-v4-checkpoint3-final.v1/probe-history`. The amendment changed a
   **comment** that asserted the retracted claim; no recorded measurement
   changed and both `p4` logs are untouched.
3. Checkpoint 3 metadata was rewritten twice after first publication — once to
   add the verbatim replay account, once to remove a **circular hash** I should
   not have written (I had recorded the hash of a report that itself hashes the
   checkpoint). **Source bytes were identical across all three revisions**; root
   recovered and SHA-verified all of them, and its first feedback assembly
   rejected the changed hash before delivering assent. The assent binds **only**
   `73dc744b…`, which is why this handoff is a separate document rather than a
   fourth rewrite of it.

## Checkpoint account

Three checkpoints. Root raised **3 + 2** findings; every one was read in full,
agreed and corrected, and **none was contested**. Two were defects I introduced
in this same pass. Root also supplied an additive immutable mirror note, both of
whose observations were accepted.

## Final checks — once, on the final bytes

Fresh disposable copy `disposable/suite-final-v4d`, explicit measured temporary
repin (12 entries over 5 files, three pin manifests). The runner **refuses a
destination that already exists**, so no earlier run directory was ever
overwritten. These pins are a **development instrument, not accepted pin
evidence** and not the repository seal.

| script | exit | result |
|---|---|---|
| `check-foundation.py` | 0 | 231/231 |
| `check-identity.py` | 0 | **1331 passing calls, 0 failed** (1282 at v3) |
| `check-product-quality.py` | 0 | 24/24 |
| `check-product-configuration.py` | 0 | 28/28 |
| `check-array-orders.py` | 0 | 65/65 |
| `check_workflows.v1.py` | 0 | 1598/1598 |
| `check_native_evidence.v2.py` | 0 | 347/347 cases; 66 cells; 0 open objects |

Root's 17 selected cases: **17/17 hold**. Eight disposable roots are declared in
`handoff.json`, with every failed attempt retained.

## Probe honesty

`p1_mirror.py` and `p4_preplan_order.py` were run against the **frozen v14 bytes**
as well as the corrected ones, so their controls are demonstrably discriminating
— on frozen v14 all six mirror assertions are false and the complete explicit
over-bound spec produces an untyped 263 663-character `ValidationError`.
`p2_cardinality.py` is **retained unchanged** even though its explicit-path case
called the vocabulary helper directly, which is not the boundary an explicit spec
traverses; `p4` supersedes that case and says so, rather than the file being
rewritten to look correct in hindsight. `p5_root_cases_replay.py` replays
**root's** case list, attributes it at the top, and is my account rather than a
substitute for root's own evidence.

## Limits

No product exists to measure and none was assumed. No real CLI, renderer, agent
surface, D9 interpreter, native host or invocation was executed and no Run was
closed; every compiler, provider and release declaration is a synthetic trusted
input, and schema admission is not host execution. The retained-path evidence is
read-only ordering evidence over source. Passing-call totals are development
evidence under temporary pins — not the six pinned commands, not distinct-case
counts, not the final seal, not qualification. The five failing cases were found
by **root**, on my halted bytes, not by me. No product implementation, commit,
push, publication or subagent, in this pass or any prior one.

Root owns: complete custody and integration of these exact assessed bytes; the
separate ongoing independent v14 review, whose findings are not supplied or
assumed here; the successor freeze and pin seal, and records **before** pins; the
six pinned commands; fresh independent review and a **new** blind reconstruction;
and full independent application review.

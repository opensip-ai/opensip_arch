# Combined consistency pass — source coauthor

**Boundary.** Source coauthorship only: not independent acceptance, not a blind, not a
readiness or candidate-acceptance claim. The main active copy was never written; `before/`
is read-only and every input still matches `before.json`. These are rebase **candidates**,
to be applied only against verified matching before-bytes and control flow.
`identity-model.py` and `integration-fixtures.py` were read as control-flow evidence only;
no proposed version is emitted for them. No implementation, pins, reports, readiness or
suite reruns.

**Substantive assent.** I assent to the combined change set on the merits, having
re-verified each premise against the captured bytes. One retraction and two qualifications
below; none blocks integration.

## Pre-integration validation

All three prior agreed anchors occur **exactly once** and were unapplied. `close_run` order
is unchanged: producer admission with the owning dialect (`:1547`) → `COVERAGE_PRODUCER_ADMISSION`
(`:1549`) → ownership (`:1551`) → grammar (`:1552`) → suffix backstop (`:1560`); closure names
`COVERAGE_SOURCE_VARIANT_*` at `:1070-1075`. `protocol3_run` init/step order unchanged.
Proposed model parses; `PLAN_SELECTION_FIELDS` unchanged; `SCOPE_LIMIT_REMEDY` key set
unchanged with exactly one changed value.

## Dispositions

**Agreed snippets applied verbatim:** precedence-final paragraph; `SCOPE_LIMIT_REMEDY`
remedy; the `initialState` splice.

**Protocol table:** added `initialState` + `initializationAndUpdateOrder`. **Main's
corrected `matchLaw` is preserved verbatim — my earlier proposed matchLaw is superseded and
must not be applied.** Main's version is better than mine: it publishes global pairwise
disjointness *and* names the control that asserts it, which answers my earlier reason for
withholding that claim. All 34 rows byte/value identical, `ruleCount` 34, no key removed.

**1 — `scopeCapabilityLaw`.** `guardOrder` rewritten to the actual two-boundary order:
producer admission first (`source-path` + `bodyIdentityJoin`, caller-supplied dialect)
refusing a *false* `complete` before any closure prerequisite; then ownership, grammar,
suffix backstop; an honestly disclosed unsupported scope is **admitted** at both and closes
its Run carrying `onUnsupportedScope`. `refusals` qualified: both name sets stay retained
and distinct, but are not both reachable for every scope — where the producer boundary
applies this law it refuses first. Root correct.

**2 — `protocol3_run` docstring.** `rules` restated as a reference control input; the rows
are pairwise disjoint so permuting today's rows preserves every outcome, which is what the
control asserts; declared first-match order remains normative and governs any future
overlapping row. Root correct, and matching my own static enumeration.

**3a — context collapse.** Both docstrings now state that units collapse *exactly when* the
entire admitted context descriptor is identical, naming `configProjection` (incl.
`configGraphPaths`), `moduleResolutionMode`, `packageModuleType`, `nodeModulesLayoutDigest`
and `lockfileIdentity`.

**3b — the generic-exception claim.** Replaced in the model docstring and in **both** prose
paragraphs. Verified empirically under the pinned interpreter: a `maxItems` error exposes
`json_path` `$.nativeContextDigests`, `validator_value` 3 and a derivable `len(instance)`.
What it lacks is the **typed projection** — no `PROJECT.SCOPE_LIMIT`, no
`REQUEST.UNSATISFIABLE` class/exit, no `field:count>limit` subject, no per-field remedy.
Schema routing semantics untouched.

**4 — Plan-array order.** Restated as phases: declaration order decides the subject at the
prospective-Plan boundary among fields **present** there; `plan_native_context_digests`
calls the same function with `nativeContextDigests` alone, before any prospective Plan
exists, so an overflow refuses at that earlier producer boundary. No global ordering claim.
Publication clarity only — `PLAN_SELECTION_FIELDS` and all executable order are unchanged.

**5 — §9.2.** Now names the published initial state and the ordered updates as part of the
complete artifact. No new security enforcement claimed.

## Retraction

My earlier claim that defaulting `identityNegotiated` true would admit OpenUniverse
pre-negotiation was **wrong; I withdraw it.** Re-derived from the published rows:
READY_OPEN_UNIVERSE is entered *only* by P3-02 on HelloAck — the very frame that writes that
flag; WAIT_SNAPSHOT_ACCEPTED only via P3-07 downstream of OpenUniverse; WAIT_DEPENDENCY_ACCEPTED
only via P3-13. No guard can read an initial value. The sound rationale is different and
holds: `protocol3_run` **returns** `finalPhase`, `terminalKind`, `sourceBytesSent`,
`stagesCompleted` and `identityNegotiated`, so for an empty or early-faulting stream those
outputs *are* the initial values, and the empty trace is likewise unpublished. The bypass
claim appears nowhere in these proposals.

## Qualifications

- **Q-1.** The two docstrings said units collapse "only when" those three components are
  identical. That direction is actually **true** — incomplete and misleading, not false. The
  strictly false statement was the remedy value corrected in the prior pass, which asserted
  the converse. Both are fixed; the record should not call the docstrings false.
- **Q-2, flagged not changed.** The same "no field, no count, no limit" claim survives at
  proposed-model lines **3897** and **3931**, in functions root did not name. Left to keep
  the diff within brief and limit rebase risk — same defect, root's call.

**Disagreements: none on the five items;** the only correction to root's framing is Q-1.

## Hashes

| file | before | proposed |
|---|---|---|
| `native-evidence.md` | `655fdc92…dd00c` | `b4bc55632ae852912c971c3ef0620a39a05d4ae49bbf67f0ca4de1c964995369` |
| `identity-schemas.v2.json` | `c0831e2b…97d1` | `e58745a606bfef43d3ccc6ed7ba3086e1280516afd16fc128d140822c4d86c0c` |
| `native_evidence_model.v2.py` | `2fa50d97…4edc` | `59b80c3726b83afb1ea0668ec2ce640586cdbcf62b4be7eb01847428dcaa88ac` |
| `protocol3-transitions.v1.json` | `336e56fc…9bec` | `62d18f0e62ada864f9ebfa67e1036a7570162143d4ed765c847d241967eb1bd3` |

Read-only, not proposed: `identity-model.py` `09e35a8c…d0b1`, `integration-fixtures.py`
`6b83940c…1316`.

Diff shape: md 4 hunks (3317→3335); identity-schemas 1 hunk (3688→3688, no reformatting);
model 8 hunks (4074→4093); table 1 hunk (345→362, pure addition).

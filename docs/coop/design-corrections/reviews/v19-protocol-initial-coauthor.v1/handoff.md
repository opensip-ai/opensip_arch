# Protocol-3 initial-state publication correction — source coauthor

Source coauthorship only; no independent, blind or readiness claim. Inputs are read-only
captures of proposed source. The main author's copy and all prior outputs are untouched.
No environment built, no suite run.

## Does publication need this? Yes

The artifact promises code-free reconstruction and cannot deliver it without
`initialState`. `guardLaw` advertises that OpenUniverse is unreachable before negotiation —
but P3-03 guards `identityNegotiated: true` and **nothing published says that field starts
false**. A consumer defaulting it true reconstructs a host that admits OpenUniverse
pre-negotiation, defeating the exact property the artifact advertises. Same for
P3-08..P3-10 and P3-14/P3-15, which select on `dependencyMode`/`preparedMode` with no
published origin, and for `stagesCompleted`/`stageIndex`, which the artifact increments
without ever stating where they start.

## Does the proposed order match source? Exactly

`protocol3_run`: state + trace initialised (`:429-432`); `preMatchLaw` in its published
order (`:435` FAULT-absorb, `:437` post-terminal, `:439` process-fault); match loop
(`:441-455`); noMatch (`:456-457`); frame `stateUpdates` (`:458-466`); `next` resolution
including the stage-dependent increment (`:467-470`); `terminalKind` (`:471-472`); phase
then trace (`:473`). Root's recital is the source order step for step.

## The `matchLaw` sentence is false — confirmed, not assumed

I verified it with a bounded static enumeration (`check_order.py`). P3-08
`{dependencyMode:true}`, P3-09 `{dependencyMode:false, preparedMode:true}`, P3-10
`{dependencyMode:false, preparedMode:false}` are pairwise **disjoint and exhaustive** over
the boolean square; P3-14/P3-15 likewise on `preparedMode`. Exactly one row of each set
matches any admitted state, so re-ordering a set among itself is unobservable. The old
sentence claimed the opposite.

**Stronger finding, deliberately not published.** Across the whole 34-row table, *no* pair
of rows can both match one (phase, frame, guard-state) — first-match-wins never
disambiguates anything as published. I kept this out of the artifact because it is a
property of today's rows, not a law: one overlapping row would falsify it, and publishing
it would invite consumers to rely on order-independence. The replacement keeps declaration
order **normative** and states only the local disjointness.

**Where order genuinely is load-bearing** is not among the rows but between `preMatchLaw`
entries: entry 1 (phase already FAULT) and entry 3 (any `*PROCESS_FAULT` "from ANY phase")
both cover a process-fault frame arriving in FAULT, and the source resolves it to
`FAULT-absorb` at `:435` before `:439`. As published those two entries conflict with no
stated precedence — the new `initializationAndUpdateOrder` resolves that existing gap.

## Changes

Artifact: **added** `initialState` (nine fields, AST-extracted from the model literal and
round-trip verified) and `initializationAndUpdateOrder` (four ordered entries); **replaced
the final sentence of `matchLaw` only**. All 34 rows byte-identical; every other
pre-existing key byte-identical; key set grows by exactly those two; `ruleCount` still 34.
No new guard, frame, phase, terminal or stage-count semantics.

Model: one splice — the three-line literal becomes
`state = dict(PROTOCOL3_TRANSITIONS["initialState"])`. All nine values are scalars
(asserted), so the shallow copy is complete and per-call isolation holds; the spliced
module re-parses under `ast`. Behaviour unchanged by construction: the published dict
equals the literal it replaces.

## Hashes

| artifact | sha256 |
|---|---|
| `protocol3-transitions.v1.json` (in) | `2fce5656601904551eae810ff664da5924094c67bcf66c905a337fc126d6b98b` |
| `protocol3-transitions.proposed.json` | `6311b06d5616520309f214f2e6d4125fac6bdafa5b8628270fc810f86ac80ac9` |
| `initial-state-before.py` (occurs once) | `ec20cb161987781ce123a883f5bbfaa61425e72089ea4ab92b89b8a493b27351` |
| `initial-state-after.py` | `aa2d7f4031156fbed2cd5519426aa84434abb49d88d485e9910708646676ed9a` |
| `native_evidence_model.v2.py` (in) | `2fa50d9748d9f9bba1849b84f03fd61806cbd1f61353860e9bf50e7158024edc` |
| spliced model — **rebase arithmetic only, not written** | `4837f6604ba43dfdbbb6e20bdb63153403fc985ab9aa5e5ac740f5cf5d2c7813` |

**Rebase.** The model consumes only `phases`, `rules`, `wildcards`, `stateUpdates`, so the
two additions are inert for it. If a control outside my capture asserts an exact key set or
a digest of the artifact, it must be updated — I could not see it and do not claim it
passes. The splice anchor occurs exactly once at `:429-431`; if it no longer matches,
`protocol3_run` changed and it must not be blind-applied. Your before18/after19 differential
is the right check for the splice; I ran no dynamic protocol run and claim none.

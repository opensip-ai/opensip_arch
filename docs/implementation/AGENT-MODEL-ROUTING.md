# Cross-vendor model routing for implementation plans

Status: execution-process guidance. This document does not change product law,
unit scope, dependency order, acceptance standing, review independence, or
qualification. Accepted and hash-pinned plan snapshots remain byte-identical.

## Default capability route

Use **`R1-BALANCED`** for ordinary planning, implementation, testing, and
revision. Its Codex route is **GPT-6.1 Sol with medium reasoning**. Its Claude
route is **Claude Sonnet 5.5 with high effort**. Use **Claude Opus 5.5 with
medium effort** without changing the route only when the plan marks
`longHorizonLead: true`: the same lead owns a parent unit and at least one
dependent successor through more than one review/integration cycle. The current
OpenSIP workflow is making good progress at this capability level.

These are operational counterparts, not claims of benchmark equivalence. Effort
labels are vendor-specific. The plan records the base model ID below. The
execution record also captures the exact selector exposed by the tool and the
resolved version when the tool provides one; do not rely only on a moving
`sonnet`, `opus`, or similar alias.

Every new plan, or the next revision of an active plan, includes this block near
its scope or execution section:

```text
Capability route: R1-BALANCED
Codex: gpt-6.1-sol / medium
Claude: claude-sonnet-5-5 / high
Claude long-horizon lead: claude-opus-5-5 / medium
longHorizonLead: <true | false; reason>
Escalate when: <unit-specific observable trigger(s)>
Escalation route: <R2-DEEP | R3-FRONTIER | R4-EXCEPTIONAL>
Independent review: <different vendor family; required capability route>
De-escalate when: <closed uncertainty or mechanically bounded remainder>
Exceptional authorization: <owner decision reference; required only for max>
```

The route is operational metadata, not evidence that the work is correct. A
model change cannot replace the normal source pins, checks, independent review,
root assent, binding, integration, or qualification gates.

## Bootstrap and enforcement

The repository-root `AGENTS.md` and `CLAUDE.md` require Codex and Claude to read
this document and run the route preflight before substantive OpenSIP planning or
execution. `tools/agent_model_route.py` parses the exact plan block, validates
that it is consistent with the named capability route, and compares the route,
provider, model, and effort with launcher-provided session metadata. Missing
metadata fails closed; a model name alone is not enough to establish the route.

Install the committed bootstrap as the global discovery file for both tools so
that agents started from product worktrees also receive it:

```bash
python3 -I -B tools/install_agent_bootstrap.py install
python3 -I -B tools/install_agent_bootstrap.py check
```

The installer creates links only when the target is absent, accepts an existing
link to these committed files, and refuses to replace any other file or link.

From the architecture checkout, check an existing session with:

```bash
python3 -I -B tools/agent_model_route.py check \
  --provider codex --plan /absolute/path/to/plan.md
python3 -I -B tools/agent_model_route.py check \
  --provider claude --plan /absolute/path/to/plan.md
```

For an accepted frozen plan that predates route metadata, do not change the
accepted bytes merely to satisfy the parser. Use the route selected by its
current authorized handoff, or the default when no selection exists:

```bash
python3 -I -B tools/agent_model_route.py check \
  --provider codex --route R1-BALANCED
```

On a mismatch, the current agent records a concise handoff and stops before
substantive work. The printed replacement command is for the owning interactive
shell or coordinator; invoking `launch` through an already-running agent's tool
does not terminate that agent. After the old agent ends, a shell may replace
itself with the required agent:

```bash
python3 -I -B tools/agent_model_route.py launch \
  --provider codex --plan /absolute/path/to/plan.md --cwd /absolute/worktree
```

In Herdr, use an existing available shell pane; the router sets the route
metadata in that pane and starts the exact provider arguments:

```bash
python3 -I -B tools/agent_model_route.py spawn \
  --provider claude --plan /absolute/path/to/plan.md \
  --pane w1:p2 --name unit_lead --cwd /absolute/worktree
```

The router does not kill or silently retarget a running agent. A route change is
a visible handoff boundary: the old session stops, and a correctly routed
replacement starts or is spawned. Use `--dry-run` on `launch` or `spawn` to
inspect the exact command without creating a session.

Before `spawn`, confirm this process is inside Herdr, list the current workspace
and live agents, and choose a pane whose foreground process is an interactive
shell at its prompt. The new name must not appear in `herdr agent list`:

```bash
test "${HERDR_ENV:-}" = 1
herdr pane list --workspace "$HERDR_WORKSPACE_ID"
herdr agent list
```

The tool refuses a real `spawn` outside Herdr. Herdr itself rejects a pane that
is not an available shell and a live-name collision.

## Cross-vendor routes

| Capability route | Codex | Claude | Use |
|---|---|---|---|
| `R0-MECHANICAL` | GPT-6 Luna, low by default; the unit may select medium for multi-file tool use | Claude Haiku 5.5, medium | Extraction, formatting, inventories, log summaries, or mechanical edits whose complete result is checked deterministically. The unit must select one Codex effort explicitly. Never the sole author or approver of semantic law, security/custody policy, acceptance, or qualification. |
| `R1-BALANCED` | GPT-6.1 Sol, medium | Claude Sonnet 5.5, high; Opus 5.5, medium only when `longHorizonLead: true` | Default for scoped design work, implementation, tests, plan revisions, and coordinated deliverables. |
| `R2-DEEP` | GPT-6.1 Sol, high | Claude Opus 5.5, medium; raise to high if the invariant remains disputed | Cross-contract reasoning, concurrency or cancellation, custody/provenance/security, source-graph reachability, resource-accounting proofs, difficult debugging, or dependency-dense composition. |
| `R3-FRONTIER` | GPT-6 Astra, high | Claude Opus 5.5, high; use Claude Fable 5.1, high after an inadequate Opus pass | Ambiguous architecture choices, conflicting evidence, consequential acceptance disputes, or a semantic failure unresolved by `R2-DEEP`. |
| `R4-EXCEPTIONAL` | GPT-6 Astra, extra-high (`xhigh` in the CLI) | Claude Fable 5.1, high; evaluate max only if needed | Final whole-product qualification, adversarial security review, or an exceptional bounded issue for which representative evidence shows a material benefit. Not a routine route. |

`max` is not a normal route in either tool. Use it only after an explicit owner
decision for a bounded problem whose prior high or extra-high attempt was
insufficient. A plan selecting `max` records that decision on its `Exceptional
authorization` line; the preflight refuses `max` without it.

## Observable escalation triggers

Escalate from `R1-BALANCED` to `R2-DEEP` when any of these is true:

- the unit changes or reconciles two or more accepted contract families;
- the unit must establish or reopen concurrency, cancellation, failure-ordering,
  custody, provenance, security-boundary, reachability, or resource-accounting
  proof not already closed by an accepted plan;
- the unit composes previously accepted libraries into a production path;
- the first independent review returns a high-severity required finding;
- two correction rounds fail for the same underlying reason;
- the author and independent reviewer disagree about a counterexample, standing,
  or gate closure.

Escalate from `R2-DEEP` to `R3-FRONTIER` only for an unresolved architecture
choice, conflicting authoritative evidence, a consequential acceptance dispute,
or a repeated semantic failure after the deep pass. Use `R4-EXCEPTIONAL` for the
final M6/Q0 qualification or a separately authorized adversarial audit.

De-escalate to `R1-BALANCED` once the disputed invariant is closed and the
remaining work is local implementation against an accepted plan with
deterministic tests. Use `R0-MECHANICAL` only when the remaining work is
mechanical and a stronger-model or deterministic gate checks the complete
output.

## Independence

The implementation model and independent acceptance reviewer **must** be from
different vendor families. Merely switching between Sonnet, Opus, Fable, or
Haiku does **not** establish independence. A Codex-authored subject uses a
Claude-family or other non-OpenAI reviewer; a Claude-authored subject uses a
Codex or other non-Anthropic reviewer. If no different-vendor reviewer is
available, the unit remains awaiting independent review; a same-vendor review
may be advisory but cannot issue the independent acceptance verdict. Increasing
the author's reasoning effort does not remove this requirement. Review must use
at least `R2-DEEP` for contract law, cancellation/concurrency, custody or
security, production composition, and qualification. The minimum reviewer route
for a routine scoped unit is `R1-BALANCED`.

## Unit-level M3 routing examples

These rows illustrate application of the route rules; they do not select the
current live unit. Revalidate the active unit against the newest live control
state. If that state does not pin one exact plan and route, report
`ROUTING-BLOCKED` rather than borrowing a route from this table.

| Work | Capability route | Change point |
|---|---|---|
| C2a3 retention/funding, when active | `R1-BALANCED` for local implementation against the already accepted addendum; this is a specific application of the rule above because merely consuming a closed proof does not reopen it. Use `R2-DEEP` if implementation needs a plan deviation, a test or counterexample challenges funding sufficiency/failure propagation, or independent review returns a required finding on resource, funding, callback, or trusted-meter semantics | Return to `R1-BALANCED` when the accepted addendum remains valid or a corrected revision is accepted, the disputed invariant is closed, and implementation again consists only of local code plus deterministic controls. Use `R3-FRONTIER` if the same semantic contradiction remains after an `R2-DEEP` correction and independent review. |
| D5 structural source graph and production reachability | `R2-DEEP` | Use `R3-FRONTIER` for disputed root/exemption semantics or an acceptance disagreement. |
| C2b0/C3 source, custody, and provenance joins | `R2-DEEP` | Return to `R1-BALANCED` for isolated implementation after all owning laws and pins are closed. |
| C4/J2 and G provider-chain production composition | `R2-DEEP` | Return to `R1-BALANCED` after interfaces and failure-order invariants are frozen. |
| Inventory, description, and status publication | `R1-BALANCED` | `R0-MECHANICAL` may draft non-authoritative deltas only when complete deterministic checks and independent review remain. |
| M6/Q0 whole-product qualification | `R3-FRONTIER`, evaluate `R4-EXCEPTIONAL` | Keep a different-vendor independent reviewer; no automatic qualification follows from the route. |

Plan authors should replace broad triggers with unit-specific observables wherever
possible: a named review verdict, failed control, disputed invariant, affected
contract count, or exact gate. Do not escalate merely because a unit is long.

## Current model references

- OpenAI model-selection guidance: <https://developers.openai.com/api/docs/guides/model-selection>
- Anthropic model-selection guidance: <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>

Re-check these references before changing the model IDs in this document. Model
availability and aliases can change; the capability-route meanings should remain
stable.

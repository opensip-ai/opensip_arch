# Agent-use evaluation requirements

The consumer delivery proposal must carry a reviewed agent-use evaluation plan.
Any claim of agent-use benefit requires retained results addressing actual tool
use and completed-task benefit. These requirements govern study planning and
benefit claims. Command delivery and release qualification continue to use their
existing owning gates; no M5 completion criterion, DR-G gate or G13 report schema
is changed here. Correctness, oracle, parity, security and performance
qualification retain their existing owners and bounds.

## Compare completed tasks

Before running a study, pin the task set, allowed inputs, expected evidence,
scoring rubric, trial count, sampling/order policy, time/tool/token budgets and
criteria for drawing a benefit claim. Use fresh isolated sessions for each trial, prevent cross-arm conversation or
answer carryover, and counterbalance trial order or disclose why it cannot be
counterbalanced. Use paired tasks against the same source and retained evidence: a plain agent with ordinary search/read tools, and the
same model/effort with the planned OpenSIP interface in addition. Give both arms
equal access to relevant permitted source information; record the additional
structured evidence supplied by OpenSIP as the treatment. Do not seed one arm
with hidden answers or exclude tasks because the tools were not called.

Include explaining a finding, tracing a relevant caller chain, investigating a
changed result and retrieving supporting evidence for a narrow review. Include
exact-name/search-sufficient tasks, misleading lexical matches, incomplete or
truncated evidence and unavailable retained inputs. Score an honest limitation
or refusal as required by the task oracle; an unsupported complete answer must
not beat a correct bounded answer. Pin any language/capability coverage claimed;
results from one task family or language do not establish general benefit.

Use a separately reviewed public/synthetic fixture set with independently
prepared answers. A campaign needing private or held-out inputs requires its
own access authority and admission procedure. This documentation unit authorizes
no experiment, corpus access, runtime benchmark or product execution.

## Record adoption, benefit and cost separately

| Measurement | Required interpretation |
|---|---|
| Tool adoption | Tasks offered tools, tasks with any OpenSIP call, calls by operation, first useful selection and unnecessary/redundant calls; retain zero-use trials |
| Task outcome | Correct completed tasks and partial/failed/abandoned/timed-out tasks against the predeclared rubric; inspect evidence support as well as the final answer |
| Missed or misused evidence | Required evidence omitted, unsupported claims, wrong Run/source selection, and ignored availability/Coverage/truncation; distinguish unavailable evidence from a retrieval failure |
| Token cost | Total per task including instructions, tool descriptions/schemas, calls, returned context, retries and final answer; report input/output and cached/reused tokens separately where observable |
| Elapsed time | End-to-end task duration including tool latency, retries and failures; disclose setup/index preparation separately and report cold versus retained-evidence conditions |

Predeclare what a useful selection means for each task; a raw call count is not
an outcome. Report per-task paired results and aggregate uncertainty or
dispersion, with denominators and all failures. Retain the chosen repetition
policy and random seeds where available. Missing token telemetry is unknown,
never zero. Record premature termination and budget exhaustion under the same
scoring rules in both arms. An agent that never calls a tool may still incur
its prompt cost; availability and adoption do not establish benefit.

Freeze the exact product and model/provider versions or exposed selectors,
reasoning effort, system/task instructions, tool descriptions and schemas,
interface configuration, harness/oracle/scoring versions, source/Run/capability
pins and environment. Retain permitted prompts, responses, tool-call arguments
and results, timings, usage observations, exits and scoring rationale in the
campaign's evidence record. Identify any unavailable telemetry or incomplete
trace. Keep the rubric fixed during scoring; where feasible, blind scorers to the
treatment arm and disclose masking limitations. Use independent assessment for
ambiguous outcomes. A description/schema/prompt change is an interface treatment,
not an engine optimization; compare it separately or identify the confounding.

The study's reviewed plan must set task-specific success/quality criteria and
acceptable cost tradeoffs before measuring, rather than choosing thresholds to
fit observed results. This guide selects no numeric product release threshold.
Report negative results and no demonstrated improvement explicitly. A favorable
adoption or token result cannot compensate for an unsupported answer or missing
qualification evidence.

## Optional context-pack experiment

A separately scoped proposal may compare the existing query/inspection workflow
with token-budgeted packaging of admitted excerpts and references. Do not assume
that `InspectionBundle` or `ReviewBrief` already defines token budgeting. Pin the
experimental tokenizer/version, counting convention, budget, selection/order and
truncation rules, reusable prefix and any already-shown-span policy. Record what
was included, omitted and why, its source/Run provenance and how the investigator
can retrieve the remaining admitted evidence. Measure round trips, repeated
context, task quality, total tokens and latency against the same baseline tasks.

Treat this as an experimental consumer proposal, with no new public fields,
endpoint, cache admission shortcut or obligation to ship it. Before public
selection, require a reviewed owning contract for tokenizer/budget semantics,
source custody, omission/continuation, failure and resource accounting. Benefit
must justify that proposal. Persistent conversational memory, session ingestion
and code-linked recall remain deferred; neither this experiment nor citations
turn a recollection into accepted semantic authority.

## Keep the qualification account separate

Agent-use results assess a consumer workflow. They do not replace authenticated
measurement custody, independent semantic oracles, native capability/platform
cells, renderer parity, or the qualification contract's benchmark protocol and
limits. Its 3 warmups and 7 measured runs still govern its benchmarks; agent
trial repetition is chosen in the separate reviewed study plan. Keep engine
output-equivalent performance measurements distinct from stochastic agent task
results. Documentation review is not evidence that a study ran or that the
product/agent server is implemented, integrated, bound or qualified.

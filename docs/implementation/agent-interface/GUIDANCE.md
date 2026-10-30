# Guidance for the planned agent interface

These are delivery requirements for tool descriptions, help and examples using
the selected product contracts. They are not a new tool protocol.

## Start with the question

Give each exposed tool or operation a short purpose, a concrete question it
answers, when to use it, when ordinary exact-name search is sufficient, its
read/effect boundary, required selection/identifiers and relevant limitations.
Use question-oriented entry guidance and progressive examples so an agent can
choose a useful first step without reading every internal concept. Keep all
twenty selected operations discoverable; a smaller introductory menu must not
remove operations or invent aliases, groups or parameters on the public wire.

| Question / purpose | Existing graph-query:3 operations |
|---|---|
| Which retained analysis am I looking at? | `run.list`, `run.show` |
| What finding needs explanation? | `finding.list`, `finding.show` |
| What admitted evidence and limitations support it? | `fact.list`, `coverage.show`, `artifact.get` |
| What is adjacent, connected, or reachable in this selected graph? | `graph.neighbors`, `graph.path`, `graph.reach` |
| What baseline/result changed? | `baseline.show`, `comparison.show`, `comparison.diff` |
| What should I inspect for an advisory review? | `candidate.list`, `inspection.show`, `review.brief` |
| What policy, import, receipt or availability applies? | `policy.effective`, `import.show`, `receipt.show`, `availability.show` |

Examples must use the owning request schemas, with schema-checked concrete
requests supplied by the future implementation unit. This table gives selection
intent only. CLI `review brief` uses its host-owned production request; public
query `review.brief` has its own owner. Do not infer interchangeable requests from
similar names. The same applies to other command/query names.

Exact-name text search is appropriate for locating a literal spelling or opening
a known source file. Use OpenSIP when the question needs retained Run identity,
admitted finding/fact provenance, Coverage, graph selection, comparison or typed
availability. Text matches remain navigation evidence and cannot establish a
semantic relationship or replace a native/evaluator finding. Do not encourage
a tool call when search already answers the user's actual question.

## Keep the evidence visible

The agent renderer preserves the JSON envelope and all required parity fields;
`agentHints` may help navigation but cannot change their meaning. Descriptions
and examples must teach the agent to retain the concrete resolved Run/view,
provenance, availability, evidence limitations, truncation and termination that
the selected owner requires. Do not relabel all operations as advisory: exactly
`comparison.diff`, `candidate.list`, `inspection.show` and `review.brief` have
that graph-query status. Graph traversal itself does not seal a new Run.

Explain these situations with the existing typed states and remedies:

- `latest` resolves to a concrete retained selection before traversal. A later
  Run does not silently change an in-progress selection or continuation.
- No returned edges, no findings, traversal completion and sufficient evidence
  are different observations. An empty page cannot prove that no callers exist;
  preserve Coverage, scope, deficiency and resolution limitations.
- A page boundary is different from an operation bound. Follow only an issued
  continuation; never reset work budgets, invent a cursor or claim completion
  because the final page has no cursor.
- Unavailable retained evidence, incompatible selection and an index that can be
  rebuilt from the same available closure have different remedies. Explain the
  actual state without substituting current source or a newer Run.
- An inspection bundle or review brief is advisory. Candidate ordering, agent
  prose and recalled rationale cannot acquire policy, verdict or repair authority.

Carry citations back to the selected admitted evidence. A current working-tree
excerpt is navigation context unless its source correspondence is actually
admitted; equal symbol bytes alone do not prove cache reuse or semantic freshness.
Never collapse syntax-only candidates, compiler-backed facts and model-produced
suggestions into one undifferentiated semantic claim.

## Useful examples for delivery

Help and tool descriptions should demonstrate a bounded investigation: select a
retained Run, explain a finding through its fact/artifact references, disclose
Coverage and follow an appropriate graph query if needed. Provide a changed-result
example through the comparison owner, and a narrow advisory review example
through candidates/inspection/brief. Include unavailable and truncated outcomes
alongside positive examples. The future implementation must validate each actual
request and response against its selected schema and required parity behavior.

Keep fitness functions and `fit` visible in command guidance. `fit` can perform
authoritative analysis and return an advisory whole-repository report; its sealed
Run keeps its own verdict. Agent narration does not edit policy or turn that
report into a Control verdict. Read-only querying does not grant execution,
mutation, repository hooks, evidence import or repair permission.

No token-budget, tokenizer, inline-excerpt or already-shown-span member is added
to an existing request by this guide. No persistent conversational-memory feature
is selected. Evaluate optional packaging as described in
[EVALUATION.md](EVALUATION.md#optional-context-pack-experiment) before proposing a
public contract.

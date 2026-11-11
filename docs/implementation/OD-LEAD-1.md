# OD-LEAD-1: Claude lead on Fable 5.2, cheaper workers, Codex review

Status: accepted owner decision; effective 2026-11-10.
Scope: OpenSIP's agent staffing and routing. This is not a product-law change or
a technical acceptance verdict for any pending subject.

## Owner instruction

Given directly to the Claude session that became lead, on 2026-11-10:

> i want you to utilize cheaper ai agents to do the work and utilize you running fable 5.2 when thet need help. you can and should have those workers utilize codex to review their work. they can communicate with codex through herdr.

The owner had already appointed Claude as lead coordinator and Codex as
reviewer, superseding the earlier Codex-only staffing selection. The lead asked
whether recording this decision and the matching router change in this
repository was authorized; the owner answered "go".

The operational details below implement that decision. They are not additional
quotations from the owner.

## What changes

1. **Lead and escalation model.** Claude Fable 5.2 at high effort
   (`claude-fable-5-2 / high`) is a permitted Claude counterpart on
   `R3-FRONTIER` and `R4-EXCEPTIONAL`. The lead coordinator runs on it. It is
   not a default for `R0-MECHANICAL`, `R1-BALANCED` or `R2-DEEP`.
2. **Workers do the work.** Authoring, implementation, testing and mechanical
   work go to the cheapest route whose description fits: `R1-BALANCED` (Claude
   Sonnet 5.5, high) by default, `R0-MECHANICAL` (Claude Haiku 5.5, medium) for
   mechanical work whose whole result is checked deterministically.
3. **Escalation goes to the lead.** When a worker hits an escalation trigger in
   [the routing document](AGENT-MODEL-ROUTING.md#observable-escalation-triggers),
   or is otherwise stuck, it stops and hands the question to the lead. The lead
   resolves it, or assigns a deeper route when the remaining work needs one.
   `R2-DEEP` stays available; it is no longer the automatic next step.
4. **Codex reviews.** Claude-authored subjects use `CROSS-VENDOR` review by
   Codex. Workers may send their own review requests to Codex through Herdr.
   The request names the exact subject, what the reviewer may run, and the
   verdict wanted. A reviewer records its first verdict before it sees the
   author's explanations.

## What does not change

- No one accepts their own work. Codex does not accept Codex-authored work.
- Existing eligible acceptances stand. Frozen plans and acceptance records keep
  their bytes.
- The route preflight still fails closed on missing or mismatched session
  values. A handoff that selects this model declares it in its route block.
- The capability-route meanings, the review-capability floors for consequential
  scopes, and [OD-REVIEW-1](OD-REVIEW-1.md) remain as written.

## Router

`tools/agent_model_route.py` accepts `claude-fable-5-2 / high` when a plan
declares it under `R3-FRONTIER` or `R4-EXCEPTIONAL`, and refuses it elsewhere.
`tools/test_agent_model_route.py` covers both.

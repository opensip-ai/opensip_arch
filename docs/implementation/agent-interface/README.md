# Agent interface and agent-use evaluation

This delivery guide records requirements for the planned agent consumer and its
evaluation. It supplements implementation planning; it selects no semantic
contract, public schema, fitness policy or release gate. Review and local
integration evidence live in [review/](review/). Documentation acceptance is
separate from implementing the interface or demonstrating an agent benefit.

- [Interface guidance](GUIDANCE.md) explains question-oriented tool selection,
  evidence disclosures and bounded follow-up using existing owners.
- [Evaluation requirements](EVALUATION.md) define what future agent-use studies
  must retain and compare before claiming benefit. No study has run for this unit.

The [workflow contract §8](../../v2/contracts/product-v1/workflows-and-surfaces.md#8-command-inventory-outputs-and-parity-ar-13-surfaces-ar-16)
owns command inventory, agent/JSON parity and query semantics. The closed
[graph-query:3 schema](../../coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json)
and [graph projection contract](../../coop/design-corrections/workflows/query-projection-contract.v3.md)
own operation names, parameters, bounds and continuation. The
[qualification contract §§2–4](../../v2/contracts/product-v1/admission-and-qualification.md#2-separate-report-custody-semantic-correctness-and-qualification)
and [applied gate map](../../coop/design-corrections/qualification-gates.applied.v1.json)
retain report custody, correctness, performance, parity and release obligations.

Follow the existing [delivery sequence](../../v2/architecture/implementation-boundaries-and-build-plan.md#implementation-milestones-after-design-acceptance):
complete the admitted core evidence path first; prepare query and shared renderer
guidance with M4, then the agent server with M5; actual release qualification
remains M6. A later unit must check the current accepted coverage schedule before
execution. This guide neither accelerates agent serving into M3 nor delays core
delivery for an optional context-pack experiment. Fitness functions and `fit`
remain part of the product.

The input was the completed Graphicle/OpenSIP comparison (2026-10-29), retained at
`/Users/sb/code/reports/Graphicle and OpenSIP comparison.md`, report SHA-256
`0231fb026ed2d4052fe2475e734982331b6d7257e98973c18b60b04603a68b8d`, with Graphicle source
research pinned to `4bbe6cd85d7c9ebce9de5ae7a7c19a105668f1aa`. Its transferable
observations concern discoverability and measured tool use, not a replacement
architecture or evidence of OpenSIP performance. Token-budgeted packaging is
only a candidate to evaluate under a separate proposal; persistent conversational
memory and session-ingestion/recall features remain deferred.

If implementation needs new request members, tool operations, evidence authority,
fitness policy or qualification criteria, stop this guide's application at that
boundary and obtain the owning reviewed successor and binding. In particular, an
unbound guide cannot override a selected passage. Frozen owners and historical
reviews remain unchanged.

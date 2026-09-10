# Status and Authority

> **Preview application:** D-369 applies the independently reviewed [reference architecture](../../coop/completion/reference-architecture.v2.md) and [exact successor manifest](../../coop/completion/architecture-application.v1.json). Older reservations and broader authoritative-product directions below retain their historical scope; the manifest names the sentences replaced for the preview. V1 claim/freeze status is unchanged. [File 08](08-decision-and-readiness-register.md) remains the only readiness checklist.

> **Status:** DRAFT — non-binding V2 architecture guide
> **Authority:** Exact V1 bytes, selectors, claim status, freeze disposition, and
> product disposition remain authoritative.
> **Active checklist:** [OpenSIP V2 Decision and Readiness Register](08-decision-and-readiness-register.md)

## Exact resolution, not “latest wins”

V2 is a readable working surface, not a replacement status authority. A reader
must begin with the reviewed snapshot in
[`v1-authority-baseline.json`](v1-authority-baseline.json), verify the separate
[`v1-status-evidence.json`](v1-status-evidence.json), and resolve the
[V1-to-V2 claim matrix](09-v1-to-v2-claim-matrix.md).

For each claim:

1. verify the exact path and full SHA-256;
2. resolve the named selector and every derivation/merge input;
3. verify the status-evidence digest and read its exact review/adjudication/
   closure/checker selector; a baseline hash alone proves no standing;
4. read `claim-register.v1.json` status;
5. read the freeze §3 disposition, including any `UNSET` or withheld seal;
6. read `product-dispositions.v1.json` where product authority is involved; and
7. carry every named blocker, closure ID, residual, and application record.

There is no “newest file,” “advanced head,” or narrative tie-break rule. A newer
filename may be rejected, unapplied, a merge input, or unrelated to the binding
surface.

## Stop-on-conflict rule

If a path, digest, selector, derivation, checker subject, claim status, freeze
disposition, or product decision differs from the baseline/matrix—or if those
sources disagree—stop. Record the conflict at
[DR-001](08-decision-and-readiness-register.md#inherited-v1-prerequisites) and
request an explicit V1 status resolution or a reviewed V2 design delta. Do not:

- silently pick the newer-looking artifact;
- promote `PASSED` or `CANDIDATE` to applied/binding;
- treat application as a freeze disposition;
- use a checker that binds different bytes;
- infer a missing recipe from fixtures or narrative; or
- allow V2 prose to close a V1 blocker.

## Labels used in V2

| Label | Meaning |
|---|---|
| **Preserved V1 structural law** | The applied/status-resolved V1 source owns the meaning; V2 restates only the architecture boundary. |
| **Accepted but unapplied V1 material** | Reviewed shape may guide a successor, but it is not a settled recipe, schema, or implementation authority. |
| **V1 unset/blocking** | Freeze disposition or required closure is missing; the blueprint gate is hard-blocked. |
| **Binding product decision** | Product posture is settled by the named product authority, even if integration artifacts are absent. |
| **Proposed V2 direction** | Non-binding delta requiring product/architecture successors and review. |
| **Open V2 decision** | Tracked only in the central register with owner, evidence, and readiness impact. |

Paragraphs must not mix a preserved V1 law with a proposed V2 mechanism under
one label. Identity/proof/replay recipes are described as settled only when the
matrix maps them to an exact applied owner artifact.

## Current authority layers

| Source | Role |
|---|---|
| [`IMPLEMENTER-BLUEPRINT.md` §1.1](../../coop/IMPLEMENTER-BLUEPRINT.md) | Exact build-head pins, derivation/merge instructions, checker standing |
| [`IMPLEMENTATION-FREEZE.md` §3](../../coop/IMPLEMENTATION-FREEZE.md) | Surface disposition; `UNSET — BLOCKS FREEZE` overrides narrative optimism |
| [`IMPLEMENTATION-FREEZE.md` §6 and §7.1](../../coop/IMPLEMENTATION-FREEZE.md) | Sealed laws and parked identity-recipe property |
| [`claim-register.v1.json`](../../coop/artifacts/claim-register.v1.json) | Per-claim status and binding reference |
| [`product-dispositions.v1.json`](../../coop/artifacts/product-dispositions.v1.json) | Product-authority choices such as P-1, P-2, G3, and CD-RT-5 |
| [`v1-status-evidence.json`](v1-status-evidence.json) | Non-binding reproducibility manifest for independent review/adjudication/closure/checker standing |

The non-binding [transition brief](../../OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md)
is design guidance, never status evidence.

## Scope boundary

V2 may propose a new distribution, component lifecycle, independent releases,
and operational qualification. It may not change V1 semantics, bypass inherited
conditions, claim qualification, or authorize implementation. The exact hard
blueprint prerequisites are DR-001 through DR-011 plus applicable V2 decisions
in the central register. DR-012 remains a release/authoritative-launch gate, not
a circular precondition to authoring a blueprint.

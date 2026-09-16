# OpenSIP design: start here

This repository contains the design record, not an implementation. You do not need to read the evidence files to understand the architecture.

## The five-minute path

1. Read [the product scope and delivery stages](v2/architecture/10-mvp-and-future-scope.md): one complete product design, implemented in stages.
2. Read [the consolidated product contracts](v2/contracts/product-v1/README.md) for the current identity/evidence, security/lifecycle, native language, workflow/output and admission contracts.
3. Read [the decision and readiness register](v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) for design acceptance, release obligations and separate implementation authorization.
4. Use [the current-source map](coop/design-corrections/current-source-map.proposed.md) when tracing older architecture chapters. D-372 applies its owning successors while preserving compatible inherited laws and historical reviews.

For the topic walkthrough, read [host authority](v2/architecture/01-semantic-model-and-host-authority.md), [components](v2/architecture/02-distribution-and-components.md), [security](v2/architecture/03-configuration-and-security.md), [operations](v2/architecture/04-lifecycle-delivery-and-operations.md), and [evidence workflows](v2/architecture/13-evidence-workflows-and-product-contracts.md), using each chapter’s current-applicability note.

The result is the architecture in ordinary prose. Stop there unless you need to audit evidence.

## If you need one specific answer

- **What did the Codex–Claude depth review find?** Read [the correction record](coop/design-corrections/README.md) for the addressed findings and retained independent reviews; the [original audit](coop/architecture-depth-review/REVIEW.md) remains historical evidence.
- **What is decided?** Read [the decision and readiness register](v2/architecture/08-decision-and-readiness-register.md).
- **What is the product, and how will it be staged?** Read [product scope and delivery stages](v2/architecture/10-mvp-and-future-scope.md).
- **Are the Fallow ideas TypeScript-only?** No. Read [common contracts and native implementations](v2/architecture/10-mvp-and-future-scope.md#language-independent-contracts-native-implementations).
- **Who is allowed to do what?** Read [host authority](v2/architecture/01-semantic-model-and-host-authority.md).
- **How are components packaged and selected?** Read [distribution](v2/architecture/02-distribution-and-components.md).
- **How are trust, signing, and grants handled?** Read [security](v2/architecture/03-configuration-and-security.md).
- **What is still blocked or requires an owner?** Read [`BLOCKED-FOR-OWNER.md`](../BLOCKED-FOR-OWNER.md) and [`DECISIONS-NEEDED.md`](../DECISIONS-NEEDED.md).
- **What was accepted so far?** Read [the architecture completion goal](v2/architecture/12-architecture-completion-goal.md) for the current target and historical preview acceptance, and the completion review in the catalog.

## What the directories mean

- `docs/v2/architecture/` — the main architecture chapters.
- `docs/coop/` — the collaboration record and completion evidence.
- `docs/coop/artifacts/` — supporting contracts and historical evidence.
- `docs/coop/completion/` — frozen reviews, fixtures, checkers, and reports.
- `DECISION-PACKETS/` — working decision packets and review history.
- `tools/` — scripts used to generate or verify the record.
- `docs/catalog/` — searchable indexes; use these when auditing, not for first reading.

Files with `.draft`, `.proposed`, `review`, `freeze`, `report`, `cases`, or `fixtures` in the name are process or evidence files. They are not required for a first understanding of the design.

## Current completion state

The complete intended-product design is accepted under D-372, following the independent design and fresh blind consumer reviews pinned in the application record. [The application record](coop/design-corrections/application.v1.json) pins the exact subjects and evidence. The [central register](v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) records conditions 1–4 at design level. Condition 5 remains NOT MET: implementation is not authorized, and release qualification is still required. D-369 remains the historical preview milestone.

# OpenSIP design: start here

This repository contains the design record, not an implementation. You do not need to read the evidence files to understand the architecture.

## The five-minute path

1. Read [the current status](v2/architecture/00-status-and-authority.md).
2. Read [the semantic model and host authority](v2/architecture/01-semantic-model-and-host-authority.md).
3. Read [distribution and components](v2/architecture/02-distribution-and-components.md).
4. Read [configuration and security](v2/architecture/03-configuration-and-security.md).
5. Read [lifecycle and operations](v2/architecture/04-lifecycle-delivery-and-operations.md).
6. Read [MVP and future scope](v2/architecture/10-mvp-and-future-scope.md).
7. Before implementation, read [evidence workflows and product contracts](v2/architecture/13-evidence-workflows-and-product-contracts.md) for the Fallow-informed design constraints and their preview/future scope split.

The result is the architecture in ordinary prose. Stop there unless you need to audit evidence.

## If you need one specific answer

- **What is decided?** Read [the decision and readiness register](v2/architecture/08-decision-and-readiness-register.md).
- **What is in the preview?** Read [MVP and future scope](v2/architecture/10-mvp-and-future-scope.md).
- **Who is allowed to do what?** Read [host authority](v2/architecture/01-semantic-model-and-host-authority.md).
- **How are components packaged and selected?** Read [distribution](v2/architecture/02-distribution-and-components.md).
- **How are trust, signing, and grants handled?** Read [security](v2/architecture/03-configuration-and-security.md).
- **What is still blocked or requires an owner?** Read [`BLOCKED-FOR-OWNER.md`](../BLOCKED-FOR-OWNER.md) and [`DECISIONS-NEEDED.md`](../DECISIONS-NEEDED.md).
- **What was finally accepted?** Read [the architecture completion goal](v2/architecture/12-architecture-completion-goal.md) and the completion review in the catalog.

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

The adopted preview architecture is complete. Implementation authorization remains a separate decision. The final evidence and decision history are retained for auditability; they do not change the reading path above.

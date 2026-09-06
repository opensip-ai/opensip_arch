# OpenSIP documentation

Start with the [current design map](catalog/current-design.md). Topic catalogs cover [security](catalog/security.md), [protocol and SDK](catalog/protocol.md), [qualification](catalog/qualification.md), [reviews and freezes](catalog/reviews-and-freezes.md), and [historical material](catalog/historical-material.md).

The architecture record retains its original custody paths under `docs/v2/architecture`, `docs/coop`, `DECISION-PACKETS`, and `tools`. Do not move or delete a file named by a frozen path or digest without a reviewed successor migration. See [operations](operations/README.md) and the [full inventory](operations/document-inventory.v1.json).

## Root-level custody files

These files remain at the project root because frozen snapshots, decision records, and tooling reference those exact paths:

- `BLOCKED-FOR-OWNER.md` — owner-blocked obligations
- `DECISIONS-NEEDED.md` — unresolved decision routing
- `DECISIONS-RECOMMENDED.md` — reviewed recommendations
- `HANDOFF.D-000-orchestrator-live.txt` — orchestrator handoff
- `PROPOSAL.cross-citation-convention.md` — citation convention proposal
- `STATUS.2026-08-26.md` — historical status snapshot

They are indexed here for navigation; relocating them requires a separate path-and-digest migration.

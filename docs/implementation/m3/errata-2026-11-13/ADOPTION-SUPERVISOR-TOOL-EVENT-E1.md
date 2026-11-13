# Adoption receipt: ERRATUM SUPERVISOR-TOOL-EVENT-E1 (a tool's unavailable confinement has its own event)

**Prepared by the records clerk on the lead coordinator's binding instruction (OD-LEAD-1); the lead's merge of this branch is its adoption.** This is an erratum to M3-D r5 F-4 (`docs/implementation/m3/supervisor-d/PROPOSAL.md`, live `:1053`; r5 `:1051`). The accepted bytes are NOT edited.

**Adopted:** the exact bytes `docs/implementation/m3/errata-2026-11-13/ERRATUM-SUPERVISOR-TOOL-EVENT-E1.md` (6,334 bytes), sha256 `7858744b8684949c5e64adca04812bccc78aaad0c796ffb4bdbb761b6c12c326`, the bytes both reviewers read at head `42c6d51388101a998d3f14eafa42c16d4fb87c6b`.

**Substance (the erratum controls):** each provider launch is recorded as `supervision.confinement.unavailable {reason}` and each tool launch as `tool.confinement.unavailable {reason}`, which requires Project only (item 21, live `:694`, r5 `:692`); each is an ordinary registration; the provider event is unchanged. The rest of `:1053` is unchanged.

**Left undecided, with their triggers (recorded by the erratum, not decided here):** the equivalent event for a tool's `applied` launch (before any tool profile ships, `supervision.confinement.applied` for tools needs its own registration and erratum), and a public carrier for tool disclosures.

**Basis, bound by value:** Codex gpt-6.1-sol/high (`reviews/codex-errata-2026-11-13-r1/review.json`): ACCEPT. Claude claude-opus-5-5/medium (`reviews/claude-errata-2026-11-13-r1/review.json`): ACCEPT at `42c6d5138` after its r3 required finding RF-7 and advisories A-1, A-2 were closed.

**Product side:** the tool-event commits on product branch `sup-disclose-1a-r1` (`d7be820b`, `18f7033e`, `bad0bea4`) rest on this erratum; this receipt resolves their "at risk" mark but accepts no code. No design-lock entry.

# Errata of 2026-11-14 (e): E1A-E2 (r2; text accepted by both reviewers and adopted by the lead's receipt)

`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`. This index was written by the records clerk when the
erratum was bound; it is not part of the text the two reviewers accepted. The erratum is additive: the accepted bytes of
M3-B r10 and of the bound erratum DISCOVERY-FLAGS-E1a r4 stay frozen and are not edited.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-E1A-E2.md` | Erratum to the bound erratum DISCOVERY-FLAGS-E1a r4 (control 8.4's 4,097-character leg) and to accepted M3-B r10 item 14a (the place of the node-path check, at discovery and at the post-seal validation): a path candidate longer than item 14a's 4,096-character node-path bound is `native.typescript-config-bound`, decided on its spelling before it is opened and not passed over for the next candidate; at the post-seal validation it is a rederivation result under E1a 2.4; E1a 8.4's 4,097 leg is that refusal with an absent base; a file the walk encounters in its admitted, non-pruned scope over `LogicalPath`'s limit remains the walk's refusal. A byte-identical copy of `LC/j3d-ts/discovery-flags/ERRATUM-E1A-E2-r2.md` (sha256 `2896a7effe705e8d4c71f456d8920a3fb45ff0573abbc41d48bd204433617ac3`, 12,770 bytes). | the lead's adoption receipt | erratum, adoption receipt | two (Codex, Claude), at these bytes, in the lead cache (not as commits in this repository) |
| `ADOPTION-E1A-E2.md` | The lead's adoption receipt (byte-identical copy of `LC/j3d-ts/discovery-flags/ADOPTION-E1A-E2.md`; its cache paths are mapped in the unit record). | lead | adoption receipt | n/a |

Owed: the implementing code (DISCOVERY-FLAGS-1 stack fix round 3) accepted by two reviewers; erratum E1c (over-long package candidates); the provider-side statement, with the next provider change.

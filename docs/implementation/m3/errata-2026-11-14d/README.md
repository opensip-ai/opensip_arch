# Errata of 2026-11-14 (d): M3B-14A-E1 (r2; text accepted by both reviewers and adopted by the lead's receipt)

`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`. This index was written by the records clerk when the
erratum was bound; it is not part of the text the two reviewers accepted. The erratum is additive: the accepted bytes of
M3-B r10 and of the bound erratum DISCOVERY-FLAGS-E1a r4 stay frozen and are not edited.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-M3B-14A-E1.md` | Erratum to M3-B r10 item 14a (the path-specifier candidates sentence) and, as its stated consequence, to the bound erratum DISCOVERY-FLAGS-E1a r4 item 7.2: the candidates of a path `extends` specifier are formed from the normalized path N as TypeScript 6.0.3's `getExtendsConfigPath` does (N alone when N ends in `.json`, otherwise N then N followed by `.json`); N equal to the project root is unresolved; the scope gate decided on N decides both candidates. A byte-identical copy of `LC/j3d-ts/discovery-flags/ERRATUM-M3B-14A-E1-r2.md` (sha256 `d09f80e58c4548d34090df24f99e6025a6181f297164cb10015679cfa7391d31`, 12,658 bytes). | `LC/j3d-ts/discovery-flags/REVIEW-REQUEST-M3B-14A-E1.md`; the lead's adoption receipt | erratum, adoption receipt | two (Codex, Claude), at these bytes, in the lead cache (not as commits in this repository) |
| `ADOPTION-M3B-14A-E1.md` | The lead's adoption receipt (byte-identical copy of `LC/j3d-ts/discovery-flags/ADOPTION-M3B-14A-E1.md`; its cache paths are mapped in the unit record). | lead | adoption receipt | n/a |

Owed: the implementing code (DISCOVERY-FLAGS-1 stack fix round 1) accepted by two reviewers. Known over-refusals listed by the receipt are not changed by this erratum.

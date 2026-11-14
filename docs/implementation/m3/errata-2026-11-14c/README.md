# Errata of 2026-11-14 (c): DISCOVERY-FLAGS-E1a (r4; text accepted by both reviewers and adopted by the lead's receipt)

`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`. This index was written by the records clerk when the
erratum was bound; it is not part of the text the two reviewers accepted. The erratum is additive: the accepted bytes of
M3-B r10 and MC8 stay frozen and are not edited.

| File | Subject | Source | Form | Review |
|---|---|---|---|---|
| `ERRATUM-DISCOVERY-FLAGS-E1a.md` | Erratum to M3-B r10 (items 14 and 14a) and MC8 (C-N1): the effective `allowJs` of tsconfig/jsconfig markers is derived at discovery, over the session's captures, on the discovery ledger, before the final U-1..U-9 construction chooses a mode; every derived graph and mode is validated against the sealed inventory after sealing; one scope gate, host-invariant key `j3d-ts.discovery-flags-unimplemented`, reasons `cargo` and `pruned-base`. A byte-identical copy of `LC/j3d-ts/discovery-flags/ERRATUM-E1a-r4.md` (sha256 `95a91ad979138c66101192f722ccc7f7bac6bb84f24a30d9c3771d965bebf19c`, 65,537 bytes). | `LC/j3d-ts/discovery-flags/REVIEW-REQUEST-E1.md`; the lead's adoption receipt | erratum, adoption receipt | two (Codex, Claude), at these bytes, in the lead cache (not as commits in this repository) |
| `ADOPTION-DISCOVERY-FLAGS-E1a.md` | The lead's adoption receipt (byte-identical copy of `LC/j3d-ts/discovery-flags/ADOPTION-E1a.md`; its cache paths are mapped in the unit record). | lead | adoption receipt | n/a |

Owed: the implementing code (DISCOVERY-FLAGS-1) accepted by two reviewers; errata E1b (Cargo) and E1c (pruned bases).

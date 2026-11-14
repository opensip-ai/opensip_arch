# M3B-14A-E1: adopted at r2 (lead, 2026-11-14 UTC)

`LC/j3d-ts/discovery-flags/ERRATUM-M3B-14A-E1-r2.md`, sha256
`d09f80e58c4548d34090df24f99e6025a6181f297164cb10015679cfa7391d31`, is adopted as an erratum to accepted M3-B r10
(`opensip_arch/docs/implementation/m3/config-discovery-b/PROPOSAL.md`, item 14a, "Resolution of one specifier S", the
path-specifier candidates sentence) and, as its stated consequence, to DISCOVERY-FLAGS-E1a r4 item 7.2's
first-candidate argument. Neither document is edited. Accepted by both reviewers at these bytes: Codex
`review-codex/VERDICT-M3B-14A-E1-r2.md` (sha256 e4a282de52acf5b12bcfe37f7cb9acad00581f13aaa78dd65d7addc8638e8b46),
Claude `review-opus/VERDICT-M3B-14A-E1-r2.md` (sha256 cf1a908ba05821b60121aa7c6a53bc0bbb878fb33ce89c49033e79f94e999fa8).
History: r1 (Claude ACCEPT; Codex one required factual correction, M3B-14A-E1-RF-1: a project root directory whose own
name ends in `.json`), r2 (both ACCEPT; the outcome of every statement is as in r1).

What it binds (the text governs; this is a summary): the candidates of a path `extends` specifier are formed from the
NORMALIZED path N, as TypeScript 6.0.3's `getExtendsConfigPath` does: N alone when N ends in `.json`, otherwise N then
N followed by `.json`; when N is the project root the specifier is unresolved; the scope gate decided on N decides both
candidates. Origin: the Claude reviewer's STK-R1 and STK-R2 on the DISCOVERY-FLAGS-1 host stack (the adopted sentence,
read literally, appended `.json` before normalizing, so `./sub/.` read `sub/..json` where the compiler reads
`sub.json`).

Recorded with the adoption:
- Known over-refusals, unchanged by this erratum, for the owner's post-M3 review list (the compiler resolves, the
  product refuses): a trailing separator (`./sub/`); a backslash specifier; a bare `.` or `..` (the compiler treats
  them as a directory and consults `package.json`'s `tsconfig` field); a `..` that rises above the project root and
  returns; `"allowJs": null`.
- For the code delta (reviewers' notes): the test names the configuration file holding the specifier; a test with a
  root file literally named `..json`; normalization stays the containment-aware one (not an absolute normalization
  followed by a prefix test).
- Binding into the design repository is owed before the implementing unit (DISCOVERY-FLAGS-1) integrates into main.

It accepts requirements only: no implementation, price, census, integration or Run gate.

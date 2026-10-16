# M3-B-r8 round-2 review

Verdict: **REQUIRED-FINDINGS**

Round-1 RF-2 is resolved. RF-1 is substantially addressed but one contradictory grammar disposition remains. No non-blocking observations.

## Exact subject and scope

Rehashed subject.json: 440 bytes, SHA-256 `2c1ff3cf7e37c57d07e604746f263c17446b3f0d99a365d00adeceead2a3b420`. Its sole member PROPOSAL-r8.md is 132594 bytes, SHA-256 `3cae5053b7fbdde39ce41090b40a3e21b00714a2445fcdb0edd1d3f1c2c8b0cb`; the pin matches.

Confirmed clean product main `01c73e2d54e037e3e41adc2f5d97df854552921e` and architecture HEAD `c7108e3f066a0a5d306e7e080a9790fc40f3e32d`. Diffed the candidate against both live r7 PROPOSAL.md and the prior r8 candidate. Substantive changes remain within item 14a, S10 and the Not claimed line, with the declared r8 banner/change notes.

## M3BR8-R2-RF-1 — Align the name pattern and malformed example

At lines 587–588, the pinned expression

`^(@[a-z0-9~-][a-z0-9._~-]*/)?[a-z0-9~-][a-z0-9._~-]*`

matches all of `pkg..x`: a valid initial p followed by admitted name characters, with no remaining subpath, and within the name-length bound. The following sentence nevertheless says “such as pkg..x … is malformed.” The name contains dots, but neither the entire name nor any subpath segment is exactly dot or dot-dot.

This yields two different normative outcomes: search node_modules/pkg..x and its stated fallback candidates, or refuse malformed without searching. The explicit closed-grammar goal requires one answer. Remove or replace the malformed example if that name is intended to be allowed, or state the intended extra name restriction in the grammar and matching controls. Align the scoped counterpart as well.

## Earlier findings and other conclusions

**Round-1 RF-1 partially resolved.** Ordered malformed/path/absolute/package classification, explicit subpath segment restrictions, no percent decoding, lexical dot/dot-dot normalization before containment, canonical project-relative node identity, retained repeated edges and identity-based cycle/node-bound checks now address the earlier substantive gaps. The new disposition controls cover the earlier examples. The isolated contradiction above is why r1Rf1Resolved and candidateOrderAndGrammarExplicit remain false.

**Round-1 RF-2 resolved.** The candidate now separates the alias target/public detail from D9 CONFIG.INVALID and explicitly excludes using that D9 code to select B-S9's CONFIG.INVALID public-detail remedy. S10 must register a remedy under native.typescript-config-unresolved in the successor public-route table and product carrier. Its remedy covers missing files, cycles, bounds and malformed syntax; each alias reaches the declared public detail, D9 row, subject and remedy. The S10 row now carries the complete obligation.

The other conclusions from round 1 remain sound: a law step is needed for pre-Plan lookup; JSONC reading and the stated file/node bounds are reasonable; effective allowJs matches NE's jsconfig supply, own/base precedence, later-base precedence and checkJs fallback. Refusing every unresolved edge is conservative and avoids an unsupported partial-graph field. Shared resolution for C2 prevents two separately derived graphs.

Reading an actually selected file in node_modules is a snapshot read-set operation, not discovery enumeration. C1 custody, the pre-C1 no-link rule, root containment and the bans on fetch/install/execution preserve that distinction. One graph-configuration public detail with four context-free aliases is justified as a single repair family; its new remedy route is now explicitly keyed correctly. Contract-successor publication and the B-S10 materialization pattern are appropriate future mechanisms.

This review does not publish the law, write S10's registry/vocabulary/remedy artifacts, implement B2-c2, make a binding or grant qualification.

## Boundaries

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. Used only read-only inspection/parsing, hashing and Git queries. No Cargo, tests, builds, lane, network, other panes or delegation; no private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.

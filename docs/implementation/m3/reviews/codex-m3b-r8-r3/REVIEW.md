# M3-B-r8 round-3 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none. All earlier findings are resolved.

## Exact subject and scope

Rehashed subject.json: 440 bytes, SHA-256 `aabce4a48770ab9238a9db1681859c4c1529aec8a36a97249a5ef9687e37fd2f`. Its sole member PROPOSAL-r8.md is 133196 bytes, SHA-256 `58adf8f0879f56b4a6ed9b4b6955e087fdad4423cd8134581d023911f8fe0d3f`; the pin matches.

Confirmed clean product main `01c73e2d54e037e3e41adc2f5d97df854552921e` and architecture HEAD `c7108e3f066a0a5d306e7e080a9790fc40f3e32d`. Independently diffed the candidate against live r7 PROPOSAL.md and the prior round. Substantive changes remain confined to item 14a, S10 and the Not claimed line, with the declared r8 title/banner/change notes. The round-3 delta only corrects the name examples and corresponding controls and records that correction.

## Earlier findings

**M3BR8-R2-RF-1 resolved.** The pattern, prose and controls now agree: dots within a name are ordinary characters, so pkg..x and @scope/a.b are well-formed package names and proceed to package lookup. They are not guaranteed to resolve. Dot-led, underscore-led and uppercase names (.pkg, _pkg, Pkg, @Scope/x) are malformed. Dot/dot-dot subpath segments remain malformed. The contradictory pkg..x malformed example is removed.

**M3BR8-R1-RF-1 resolved.** The retained ordered malformed/path/absolute/package classes, pinned name expression, subpath restrictions, no percent decoding, lexical normalization before containment and canonical project-relative node identity close the earlier naming ambiguities. Repeated edges retain their order while naming one node; cycle and 32-node checks use those identities. Candidate order and first-regular-file selection are explicit.

**M3BR8-R1-RF-2 resolved.** S10 explicitly registers the new public detail, its four aliases, D9 row and remedy under native.typescript-config-unresolved itself in the successor public-route remedies and product carrier. D9 CONFIG.INVALID is correctly distinguished from public detail CONFIG.INVALID; the latter's B-S9 remedy is not accidentally selected. The shared remedy addresses the four declared configuration-failure classes.

## Law assessment

The new law step is needed because the selected native reference consumes effective allowJs as an observation, while NE specifies its meaning and graph retention without this pre-Plan file-resolution algorithm. One first-party bounded JSONC reader shared with C2 is appropriate. The accepted proposal specifies comments/trailing commas, last-key behavior, option/extends types, 64 KiB per file, 32 graph nodes, and typed malformed/cycle/bound/unresolved outcomes. It does not claim complete TypeScript resolver compatibility.

The effective-allowJs derivation matches NE:527–545: each jsconfig node supplies true unless it writes a value; own options beat bases; later bases beat earlier ones; inherited/written allowJs, including false, wins; otherwise effective checkJs supplies the value with false default. Refusing every unresolved edge avoids guessing or inventing a partial-graph carrier.

The read-set/descent distinction matches NE:735–741: actually read pruned bytes are snapshot-inventoried under custody, without enabling discovery enumeration. Root containment, C1 custody and pre-C1 link refusal preserve the intended read boundary. No fetch, install or execution is authorized.

The four internal keys form one external configuration-repair family, so one public record and context-free aliases are justified. The request-rejected/exit-2/CONFIG.INVALID D9 classification, class-plus-config-path subject and correctly keyed remedy produce the specified complete public termination. A contract successor for registry/aliases/routes/remedy and B-S10-style product vocabulary materialization is the appropriate future S10 mechanism.

## Limits and boundaries

This acceptance covers the exact law proposal. No S10 artifacts, reader code, binding or product qualification are created by it; those remain separately reviewed work.

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. Used only read-only inspection, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane, network, other panes or delegation; no private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed.

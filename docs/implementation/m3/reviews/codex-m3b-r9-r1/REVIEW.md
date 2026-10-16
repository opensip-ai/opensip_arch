# M3-B r9 law review

Verdict: **ACCEPT**.

Subject manifest: `docs/implementation/m3/config-discovery-b/m3-b-r9-subject.json`, 440 bytes, SHA-256 `940fefbea8c9e6533c0511015971bde37f20e6dc067750866aa88865945ad528`.

Its sole member, `PROPOSAL-r9.md`, matches its pin: 136,065 bytes, SHA-256 `24fe5a9cc473870dc0b3ea43bb23abb0ddcda4de099a25a41d0cd65cb6069b8e`. The r8 diff base matches the accepted snapshot: 133,196 bytes, SHA-256 `58adf8f0879f56b4a6ed9b4b6955e087fdad4423cd8134581d023911f8fe0d3f`. Architecture HEAD matches the manifest's `a35987d7092ba921a0459ae7e8f9660c3f676186`; product main is clean at the pinned `1f70dba4d18d9db7b11253b9202846d2ca2bc50e`.

## Decisions

1. **Empty documents are a sound explicit law amendment.** The new rule supplies the missing normative authority identified by B2C2-R1-RF-1. An empty or comment-only configuration supplies no extends edges or written options. NE:527-545 then gives an empty tsconfig effective allowJs=false/checkJs=false, while an empty jsconfig supplies its node-local allowJs=true. Applying the same rule to entry and base files keeps the shared graph reader coherent. It requires no evaluation, process or external acquisition. The amendment does not admit unterminated comments, arbitrary malformed syntax or non-object values, nor bypass the file-size check. Existing bounds, containment, candidate resolution, custody, cycle handling and inheritance remain intact.

2. **The object requirement is a faithful explicit completion.** A configuration is an object whose compilerOptions member, when present, is an object. Stating that requirement closes r8's implicit structural typing rather than adding a fifth refusal class or a new route. Null is a present JSON value and therefore fails the object requirement; it is distinct from the newly admitted absence of any value after valid whitespace/comments. Arrays, strings and other non-object roots also remain malformed. This matches LD-B2C2-2(h), and makes the Python null conflation identified in B2C2-R1-RF-2 unambiguously incorrect.

3. **No S10 successor is necessary.** The four internal aliases, public detail, request-rejected/2 D9 row, CONFIG.INVALID code, absent fault cause and subject remain unchanged. The pinned S10 registry and model match the reviewed snapshots, and the product lock still binds S10 as contract successor 167. Its detail-keyed remedy remains true: correcting a file's syntax/structure to an admitted configuration addresses malformed object shapes, while files now admitted as empty need no refusal remedy. Neither registry vocabulary nor remedy bytes need to change.

4. **Scope is exact.** The complete r8-to-r9 diff consists of the title/banner and preserved acceptance history, the r9 changes section, the appended grammar rule, the control bullet covering empty and null cases, and the Not claimed line. All are declared. The text from item 14a's bounds through its refusal/public-termination/basis sections is byte-for-byte unchanged, as is the r8 changes section. The new controls cover empty and comment-only files as entry/base configurations, null roots with and without comments, and null compilerOptions. The TypeScript citation motivates the authored law decision and is used only as supporting evidence; it does not import TypeScript's remaining parser or resolver behavior.

## Findings and limits

No required findings or non-blocking observations.

This acceptance resolves the law-authority issue in B2C2-R1-RF-1 once the implementation pins and follows this accepted revision. It does not accept B2-c2 r1, discharge the Python null bug or exponential-inheritance finding, or establish that r2 has corrected them. Those remain implementation-review work. The 64-entry graph-record issue is unchanged.

Review used read-only file inspection, hashing, JSON parsing and Git queries. No build, test, generator or network operation was run. No repository, candidate worktree or control file was edited. No installation, private fixture, signing key or held-out store was accessed, and no delegation was used. Only the two requested review outputs were written.

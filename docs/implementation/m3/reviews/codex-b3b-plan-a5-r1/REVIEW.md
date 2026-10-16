# B3-b plan r2 amendment A5 review

Verdict: **ACCEPT**.

Required findings: none. Non-blocking observations: none.

Reviewed subject: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A5.md`, independently verified as 5005 bytes, SHA-256 `ad64083ba36ae654d7dfe0a15f28fda1d6b97f761a6c6f8282ef6a16de8aa25b`. Architecture HEAD is `18d385688acd95025480fb31e78e657c16c0bbd8`; product main is clean at `e367d7f465d8d0a74819cad5010a58b8641e4c7a`.

## Split and gate

The split is sound. B3-b3a1 owns the closure, anchored model, repository costs and margins, walker equality projection, measured validation and under-count mutations. B3-b3a2 owns the blind-mode extension, extended closure binding and synthetic confidentiality/lifecycle controls. Acceptance of a1 does not authorize a held-out read. Acceptance of a2 must cover the exact final tool and closure incorporating the accepted a1 model; the existing section 4.3 requirement to accept those exact bytes remains explicit.

A1's single gated receipt refresh is preserved. During a1 and a2 development the receipt remains stale and no held-out store opens. B3-b3b performs the one mechanical blind run after a2 acceptance, followed by the original post-run review. Splitting the pre-run work does not add a blind run or relax the output allowlist.

The model work retains the three root lengths (134, 1024 and 4096), worst read-growth and retry envelopes, all six named synthetic populations, the existing actual-versus-predicted checks and one under-count mutation per new term. The original projection's field-level equality and explicit pin-change allowlist remain obligations; adding terms must not disguise changes in walker population, charges or walker margins.

## Terms

A5-2 preserves A2-3 step 4's disjoint assignment: carrier reads, custody and declaration rows in the reader term; placement, visible-repository listing, item 6b and provider-manifest reads in the member term; member descent in walker rows. Placement and listing are explicitly paid at zero admitted members over the declaring entries and listed population. The model therefore cannot simply multiply every member-term cost by admitted-member count. Existing native binding records, post-read checks, retained copies and gitlinks must be included wherever their actual charges occur, once each.

Repository rows gain the applicable terms and re-evaluated margins. Workspace full-ledger margins remain outstanding until B3-b3c. This does not conflate the unchanged walker equality projection with the new full-ledger totals.

## Parse accounting decision

A5-3 correctly identifies the bound as a bound on ledger charges. Law M3-B r9 item 12 specifies the walker's charges and everything item 6b charges, including every other charged step. Plan r2 section 4.1 likewise says everything item 6b and the readers charge. It does not define a measurement of total process allocation or parser execution cost.

The source supports the stated distinction. `workspace_declarations.rs` calls `parse_toml` and `parse_json` directly for carriers and provider manifests; its observation interface carries no parse-accounting operation or ledger. The native observation charges bounded reads, custody, post-read checks and kept-read storage/copies, but those charges do not constitute a separate charge for the pure parses. The 4 MiB read cap bounds the input, rather than proving an aggregate parser-memory ledger bound. By contrast, `git_tracking.rs::config_decided` charges one object, one edge and the config length before parsing/checking; the member index decode charges one object, one edge and twice the index length. Those charged parses/decodes remain in the member term.

Consequently, the uncharged reader parses contribute no separate ledger component. A5 expressly amends the earlier section 4.2/A2 wording that listed a parse component; it does not silently omit an existing charge. Acceptance of the earlier code alone would not prove this conclusion, but the current calls and the stated law do support it.

**The decision core need not acquire parse charges as a prerequisite to this census bound.** Adding them would be a product accounting change beyond this plan's tooling split. If that change is desired, it belongs in a separately scoped, reviewed B3-b product correction to the core/native observation accounting interface and its controls, before freezing the a1 cost derivation and final a2 closure. The model, validation and pins must then reflect the changed charges. It should not be implemented as an unreviewed change inside the census calculation. This acceptance makes no claim that the discovery ledger measures all parser allocations or total memory use.

## Remaining steps and review boundaries

B3-b3b and B3-b3c remain unchanged through A5's explicit incorporation: exact-byte pre-run acceptance, the one authorized blind run, its post-run review, workspace full-ledger sums, 2x margins and return of failing caps to the law. A1's closure/receipt reasoning, A2's charge assignment and carried observation, A3's completed controls and A4's accepted branch-A order and gitlink boundaries are not removed. The final status round remains.

This is acceptance of the plan amendment, not acceptance of a bound implementation, permission to open held-out data now, qualification or completion of B3-b. Only the requested review files are written. Neither repository nor control files were edited. No compiler, Cargo, tests, builds, lane, census tool, network, private fixture, installation directory, signing keys, held trees, T2 held-out entry, other panes or delegation were used.

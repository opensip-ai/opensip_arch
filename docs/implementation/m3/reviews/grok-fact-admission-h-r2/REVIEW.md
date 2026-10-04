# Law M3-H r2 — fact admission

Verdict: **REQUIRED-FINDINGS**. One finding. The r1 anchor-owner defect is closed in item 14.4, and item 10's move onto the view-join call matches the product owner. Item 10, item 11's heading and item 22 do not carry that routing through.

Subject: `docs/implementation/m3/fact-admission-h/PROPOSAL.md`, 106667 bytes, sha256 `4ae48f09d890174796b31e94f09ec717c46164f9bc2bf266bc61c5bc5a77661a`. Untracked until acceptance. Diffed against `PROPOSAL-r1.md` (`69f50bb1…`, 88004 bytes). Read only. No product build, no cargo, no repository edit.

Judged against the pinned bytes. J1 is `host-pipeline-j/PROPOSAL-r4.md` (`c18c0d3c…`, 120506 bytes). GROK2's review of that file is ACCEPT (`reviews/grok2-host-pipeline-j-r4`, subject sha256 `c18c0d3c…`). M3-C citations were checked on `snapshot-plan-c/PROPOSAL-r6.md` (`8274bca1…`). M3-L is cited only as the frozen r1 object of X-H1 and X-H4 (`5e858c05…`). Product files cited from main `9c11c53` still match the pins at current main `cd5958b`. Since `3e64266`, `crates` differs only in the ten `crates/security` trust and custody files.

## Finding

**RF-1.** Item 14.4's routing is the right split, and two later tables assign different public rows to the same keys.

Item 14.4 (`PROPOSAL.md:478`) sends `ANCHOR_SOURCE`, `ANCHOR_RANGE` and `ANCHOR_UTF8` on a provider-return view to MJ row 30 only, and sends the Coverage producer, prerequisite and totality keys to MJ rows 30 and 32. The assembly keys, including `FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN` and the partition overlap, are host invariants on both origins. H-C24 repeats row 30 for the three anchor failures on a provider-return view, and the host-invariant row for the same three failures on an E3 syntax fact.

Item 22 (`:692`) puts the three anchor keys and the Coverage keys in one family and sends that family to MJ rows 30 and 32. Item 10 (`:386`) says a producer-claim key from the view-join call takes row 30 or 32. Row 32 (`PROPOSAL-r4.md:678`) is the Coverage cause, carrier and contradictory-completeness row (NE:3538, NE:3541). An anchor failure is the byte rule at IE:1426-1429, which item 14.4 and H-C24 already place on row 30 (`PROPOSAL-r4.md:676`, NE:3529). Rows 30 and 32 share `PROVIDER.PROTOCOL_VIOLATION` and an absent `domainDetail`, so the anchor disagreement does not change the public code. It does leave H-C24 and item 22 unable to pass together.

Item 22 (`:697`) then sends every refusal of a host-minted record or view, named as items 11, 16 and 18, and every view-join key of that refusal, to `HOST.INVARIANT_VIOLATED` (MJ row 29). Item 11's heading calls the terminal entries host-minted. The body says those entries are the provider's own and that the pre-Analyze conversion is the only Coverage the host writes. Item 14.1 classifies a clean terminal's Coverage as provider-return, and item 4 admits it at item 10's producer boundary. A provider terminal entry that fails a Coverage claim key is `PROVIDER.PROTOCOL_VIOLATION` under item 14.4 and `HOST.INVARIANT_VIOLATED` under item 22.

Item 14.4 also writes `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` as a bare token. The owner returns `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:<relation>@<rung>:<subject>` (`view_joins.rs:526-530`). The prerequisite keys in the same cell already use a star. The assembly catch-all is host-invariant on both origins. An exact match on the bare token puts the owner's totality key on that catch-all, which changes the public code. The overlap and ladder keys have the same suffix shape (`view_joins.rs:352-357`, `:429-431`). Those two stay host-invariant either way.

**Fix.** One route, written the same way in item 10, item 14.4 and item 22.

- On a provider-return view, `ANCHOR_SOURCE`, `ANCHOR_RANGE` and `ANCHOR_UTF8` take MJ row 30 only. The Coverage producer, prerequisite and totality keys take MJ rows 30 and 32.
- On a host-minted view, every one of those keys takes the host-invariant row.
- Replace item 22's single producer-claim row with those two rows. Cite NE:3529 and IE:1426-1429 on the anchor row, and NE:3529, NE:3538, NE:3541 and NE:3575 on the Coverage row.
- Change the host-minted row from "items 11, 16, 18" to "item 11's pre-Analyze conversion, item 16 and item 18". Item 4's provider-authored terminal Coverage stays on the provider-return rows.
- Retitle item 11 so only the pre-Analyze conversion is called host-minted.
- In item 14.4, write `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:*`, `SUBJECT_SCOPE_PARTITION_OVERLAP:*` and `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:*`, and state that a star or a `:<…>` marker matches the owner's full key.

## What holds

### The anchor half of r1 RF-1

F5 keeps the count only. `relations.rs:334-341` returns `RelationRule("anchor cardinality")` from inside `inspect_relation_payload` (`closure.rs:329`), which `inspect_relation_snapshot` (`closure.rs:419`) calls first. F6 keeps `path not inventoried`, `file content join`, `file length join` and `anchor foreign path` (`closure.rs:465-494`). `FACT_ANCHOR_CARDINALITY` is withdrawn. IE:1038 uses that name as prose.

`ANCHOR_SOURCE`, `ANCHOR_RANGE` and `ANCHOR_UTF8` run once, inside `inspect_plan_view_joins`, over a view that already names the facts (`view_joins.rs:212-223`, `:367-407`). H builds that view in a staging overlay of temporary custody (MJ:399) and discards the overlay on refusal, before it joins the admitted set. No host copy of the anchor law is added. A record E3 hands H stays host-internal for every item 5 refusal, the three anchor keys included (item 16, H-C24). Provider-return F1–F9 take row 30. Item 18's inventory facts carry no anchors (IE:1006), and item 22 already sends any refusal of those host-minted records to the host-invariant row.

### R9

Item 14.4, read alone, closes r1 RF-1. The finding above is that item 10, the item 11 heading and item 22 do not yet say the same thing.

### R10

F3 now requires the `(relation, resolution)` pair the stage requested (DLV:1144, "relation/rung"). F7 requires the source universe to be this child's, the target to be that universe or an activated target of the stage, and `same-only` to keep them equal. `FACT_SCOPE_JOIN` compares `relation`, `resolution`, `sourceUniverse` and `targetUniverse` (`view_joins.rs:374-387`).

That pair of checks does leave `FACT_SCOPE_JOIN` unreachable by a provider fact that passed them. DLV:972-975 is why. `crossUniverseRelations` is `imports`, `calls` and `references`, which are the three `admitted-target` relations in the relation registry. Key construction emits one key for every activated semantic universe on those relations, including the source universe, and exactly one key whose target is the child universe for every other relation. F7's `same-only` clause forces those other relations onto the child universe. A fact that passes F3 and F7 therefore names a requested four-tuple, and the view's scopes are those requested keys (items 9 and 14). `FACT_SCOPE_JOIN` then fails only when H omitted that scope. Routing it as a host invariant is sound. F7's citation is still NE:3162-3164, the spelling of the universe id. NBO-1.

### R11

Moving the producer boundary into the owner's view-join call is sound, and it changes no accepted function signature.

`inspect_coverage_producer`'s signature is unchanged. `CoverageProducerInput.unresolved` remains a caller-supplied slice (`coverage.rs:28-36`), and the comment at `coverage.rs:21-22` still says this API cannot prove the census complete. On H's path the only caller is `inspect_plan_view_joins`, which builds the slice from the view's `unresolved-edge` facts (`view_joins.rs:450-466`). H calls `inspect_coverage_producer` nowhere, passes no census, and passes no dialect. H-C9 and H-C10 say that.

The dialect is `{table}`, derived from the retained universe frame through `capability_support::eligibility` (`view_joins.rs:470-479`; `coverage.rs:290-303`). That function is `pub(crate)` (`capability_support.rs:279`). r1's direct call, with a per-Analyze census and `languageVersionBinding.dialect`, would have been a second caller of the same law.

The provisional `coverage2` is the name the owner already requires: the view's `coverageIds` must name the record before the call, and `COVERAGE_ADMITTED_IDENTITY` compares the inspector's mint with that name (`view_joins.rs:492-497`; `coverage.rs:408-422`). NE:1924-1940 says `coverage2` is minted only after the checks. The overlay is discarded on refusal and is not visible outside H, so that order holds for every record that leaves the overlay. Run closure re-runs the same composition over the retained view.

The stray `unresolved-edge` fact whose payload relation has no scope on the view is counted toward no Coverage entry. The bijection keeps an edge only when its payload relation matches the entry (or `reachability`/`calls`) and its referrer is in the scope's subjects (`coverage.rs:208-213`). That is RC-2 (NE:2113-2117; IE:1481; NE:3351; NE:3474). It is the contract's per-entry filter. H does not need a second census, and pre-filtering by D's subjects stays rejected.

Item 22's Coverage public codes stay rows 30 and 32 on a provider-return view and the host-invariant row on a host-minted view. The origin split is the r1 fix. The sentences that fail to say it exactly are the finding.

### Scope against r1

The diff is the RF-1 rewrite, the item 10 rebuild, the withdrawal of M3-L as authority, and citation re-pins. The re-pins I checked land on the sentence the prose quotes.

- M3P:216 is the H row. M3P:307 is H at 3 days, after C4a and F1, finishing day 22. M3P:320-324 is the 33-day chain and the zero-slack X12d branch that also reaches J2 on day 22. M3P:259 is the pre-day-0 list that names the H law. The conditional day-0 gate for FA-2 and C r7 / CRC-1 is stated, and late arrival waits day for day.
- MJ:377 is J-η: H's fact admission, then full `admit_enumeration`, before `derive_evaluation`. MJ:785 is the J2b row. MJ:399 is temporary custody. MJ:325 is R10a. MJ:402 gates S-B. MJ:657 and MJ:667 are rows 11 and 21, `WORK.BUDGET_EXHAUSTED`. MJ:731 is the lead-set rerun rule. Row numbers 29, 30, 31, 32 and 36 are unchanged. R10a moves no sentence H relies on.
- M3-C stays on r6. Item 8 records r7's row-8 narrowing and says H does not depend on row 8. The core provider closure still has exactly two uses (MC:424-432, MC:453). X-H3 remains the recorded request for a third use.
- ME:712 and ME:714 are E3's syntax-join interface. ME:477 is "the crate never mints `fact2`". ME:714-728 is the second-integrator rule. AQP:112, AQP:113, AQP:322-325, AQP:388 and AQP:400, and OPP:246, OPP:247 and OPP:275, are the sentences item 21 and item 23 quote. MB:406 is U-5 and U-6 owned by H and J. MB:414 is the six `inventory/*` cells, B's discovery half and C1's bytes.
- Item 7 no longer treats M3-L r1 as a rule. NE:2202-2206 supports the `unresolved-edge` wrap. X-H4 still names ML1:206 and ML1:210 as the conflict for L's next revision.
- X-H1 through X-H6 stay recorded conflicts with named owners. FA-2 is a recommendation. H writes no store and adds no X9 row. No new public code.

## Non-blocking

**NBO-1.** F7 cites NE:3162-3164. Those lines are the 64-hex spelling of a universe id. The R10 implication depends on DLV:972-975. Cite that key-construction rule beside F7 on the next touch.

**NBO-2.** The law says the product facts were read at main `9c11c53`. Current main is `cd5958b`. The cited crate files are unchanged since `3e64266`, apart from the ten security files this law does not cite. Name that pin base on the next touch.

**NBO-3.** `COVERAGE_PRODUCER_ADMISSION` can join a NE:3529 cause and a NE:3541 cause into one key (`view_joins.rs:136-148`). Rows 30 and 32 share the public termination, and item 3 discards the return either way. Say which row is recorded when one refusal belongs to both.

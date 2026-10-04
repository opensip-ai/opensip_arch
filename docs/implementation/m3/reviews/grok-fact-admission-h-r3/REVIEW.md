# M3-H r3 — Grok review

**Verdict: ACCEPT.** Recorded as accepted in review. Subject `docs/implementation/m3/fact-admission-h/PROPOSAL.md`, sha256 `7a562720646017f5039ef9594947850af6edb2e2c574a49b31db702159760398`, 115470 bytes. All 58 pins in `hashes.txt` match. Product main is `cd5958b3608f44a0035566c9d4500e5005c62e91`. Since `3e64266`, `git diff --stat 3e64266 HEAD -- crates` is X4-F1's ten `crates/security` files, 524 insertions and 33 deletions. Every pinned product file hashes to the pin. No cargo, tests, or product runs.

r2 was REQUIRED-FINDINGS on one finding: item 14.4, item 10, and item 22 named different rows for the same view-join keys, and the totality key was written bare while the owner appends a suffix. r3 closes that finding.

## RF-1 is closed

Item 14.4's table is the only routing authority for keys of the view-join call. Item 5 sends F10 only to that table. Item 10 does the same and no longer says "row 30 or 32". Item 11 states the two origins and sends their refusals to item 14.4 and item 22. Item 16 sends E3's view-join keys to item 14.4. Item 22's view-join row names the table and restates none of it. The producer-claim row and the blanket host-invariant routing of item 11 are gone.

On a provider-return view the three anchor keys take MJ row 30 only (MJ:676, NE:3529, IE:1426-1429). H-C24 still requires that. Row 32 (MJ:678) stays the Coverage cause, carrier, and contradictory-completeness row. A provider terminal's Coverage is provider-return (item 14.1 and the retitled item 11). Only the pre-Analyze conversion is host-minted, and item 22's host-minted row names that conversion together with items 16 and 18, for refusals outside the view-join call.

Prefix-token matching is the text before the first `:`, compared by equality. The registry refusal strings are `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH` (relation-payload schema, `coverageTotality.refusal`) and `SUBJECT_SCOPE_PARTITION_OVERLAP` (`partitionLaw.refusal`). The owner appends `:{relation}@{resolution}:{subject}` (`view_joins.rs:352-357`, `:526-530`) and `:{relation}@{rung}` (`:429-431`). Those prefixed keys take the listed token's row. The catch-all applies only when no listed token matches, so the totality key no longer falls through to the host-invariant row.

## R12

Every `Refused` string `inspect_plan_view_joins` returns is classified by the token the owner actually spells.

- `ANCHOR_SOURCE`, `ANCHOR_RANGE`, and `ANCHOR_UTF8` have no colon and take row 30 on a provider-return view. The non-usize offset path also returns bare `ANCHOR_RANGE` (`view_joins.rs:84`).
- `COVERAGE_PRODUCER_ADMISSION` is the joined key (`view_joins.rs:136-148`) and takes 14.4a.
- The eleven prerequisite tokens are the strings `scope_disclosure` builds (`capability_support.rs:330-370`): the four `COVERAGE_DIALECT_*` keys, the three `SYNTAX_CAPABILITY_*` scope keys, and the three `COVERAGE_SOURCE_VARIANT_*` keys. Each takes row 32 on a provider-return view. Equality of the whole prefix token keeps `COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED` distinct from `COVERAGE_DIALECT_PREREQUISITE`; both sit on the same row.
- `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts` is the owner's format and takes row 32. H-C25's overlap and ladder examples match `view_joins.rs:352-357` and `:429-431`, and both tokens are catch-all examples, so they take the host-invariant row on either origin.
- The assembly tokens in the catch-all example list are the remaining bare `Refused` strings.

`inspect_syntax_fact` can also return `SYNTAX_CAPABILITY_UNSUPPORTED_FACT:…` from `relation_payload` (`view_joins.rs:100-105`). That function returns immediately unless the universe domain is `native.semantic-universe.syntax.v2` (`capability_support.rs:200-201`). Item 14.1's provider-return views are TS2 and Rust3, so this key arises on an E3 view. The token is unlisted, the catch-all applies, and a host-minted view's catch-all is the host-invariant row, which is also F9's route for a record E3 hands H. `BODY_ELIGIBILITY_UNDECLARED` and `BODY_ELIGIBILITY_FORM` come from `eligibility` (`view_joins.rs:477-478`) and are named in the catch-all. They judge the retained universe frame, so the host-invariant row is the right one on a provider-return view too.

## R13

14.4a's classes match the owner and the three NE rows.

- `native.coverage-cause-*` is the cause-carrier registry (`coverage.rs:106-157`). NE:3541 lists that family and MJ row 32 cites NE:3541.
- A bijection fault whose `fault` member begins `RC-6:` is contradictory completeness (`coverage.rs:192`, NE:3538). The joined rendering is `{'entry': …, 'fault': 'RC-6:` (`view_joins.rs:141-146`), which is what 14.4a quotes. The current RC-6 sentence contains no single quote, so `pyrepr` keeps the single quotes.
- `RC-0:`, `RC-1:`, and `RC-2:` are the bijection faults NE:3529 names, and MJ row 30 cites NE:3529. §4.1a's key, commitment, count, entry-key, and schema-digest refusals are the other strings in `coverage.rs:358-376` and `:401-404` (`native.coverage-key-scope-mismatch`, `native.subject-scope-commitment-mismatch`, `native.coverage-entry-key-mismatch`, `native.examined-universe-commitment-mismatch`, `native.examined-universe-subject-count-mismatch`, `native.coverage-payload-schema-not-registered`). NE:1945-1947 puts those on `PROVIDER.PROTOCOL_VIOLATION`. They are the row-30 class.
- `native.coverage-source-variant-*` (`coverage.rs:389-399`) is the producer-boundary spelling of the source-variant carrier law (NE:3802-3806). NE:3529 and NE:3541 do not name it. It is the same carrier contradiction as the `COVERAGE_SOURCE_VARIANT_*` keys, so row 32 is the right recorded condition.

The tie rule records row 32 when any row-32 cause is present, and row 30 otherwise. Rows 30 and 32 share operational-failed 4, `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol, and an absent `domainDetail` (MJ:676, MJ:678). Item 3 discards the return on either row. An inspection that carries both an RC-2 fault and an RC-6 fault records the contradictory-completeness condition. An inspection that carries only RC-2 records the NE:3529 condition. That answers r2 NBO-3.

Sending the prerequisite and totality keys to row 32 only is the right lead decision. Each refuses a Coverage entry whose declared completeness, deficiency, or cause its carrier law contradicts (NE:446-453, NE:358-363, NE:3772-3779, NE:3802-3806). MJ:678's condition is that refusal. Those keys appear in none of NE:3529, NE:3538, or NE:3541, and the route table assigns them no other row. The host-minted column still sends every one of them to the host-invariant row.

Item 12's request bijection is `native.coverage-entry-key-mismatch` on NE:3529, and item 22 now sends it to row 30 only. The same spelling inside `COVERAGE_PRODUCER_ADMISSION` is a row-30 cause under 14.4a. Item 13's closed-world key is wired only once FA-1 adds it to NE:3529, and item 22 sends it to row 30. RC-6 stays inside the view-join key, on row 32.

## Scope

r3's other edits are the r2 responses, the M3-C r7 re-pin, the product pin, and the X-H3 rename.

NBO-1 is answered. F7 and item 14.5 cite DLV:972-975. `crossUniverseRelations` is `imports`, `calls`, and `references`, the intra-universe rule emits one key for every other relation, and the cross-universe rule emits one key per activated semantic universe for those three.

NBO-2 is answered. The pin base is `3e64266`'s bytes at main `cd5958b`, and the law cites none of the ten security files.

M3-C r7 is accepted by CODEX2 (`a1ee9386…`). r6 is 1221 lines and r7 is 1232. The body shift is 11 lines from the r7 history insert. Forty-one of the forty-two MC citations in r3 are the r6 text at that shift, including the quoted sentences at MC:443, MC:458, and MC:885. r7's only body replacement is item 16 row 8 (r6:860, r7:871). See NBO-1.

The X-H3 rename matches the lead note: CRC-1 routes the item onward, and the row the units wait on is M3-C r8 / CRC-2. See NBO-2.

No other r2 rule moved. F1 to F9, the anchor owner, the provisional view, H-C24, and the J1 row cites stay. MJ:675 is row 29, MJ:676 is row 30, and MJ:678 is row 32.

## Non-blocking observations

**NBO-1.** PROPOSAL.md:170 cites C4a as MC:839-917. That span includes r7's changed row 8 at MC:871. Every other re-pinned MC citation matches the r6 text. Item 8 already says H does not depend on row 8. On the next touch, end the C4a cite before that row or name the one changed line inside the span.

**NBO-2.** X-H3's audience (PROPOSAL.md:860) and the successor kind column (PROPOSAL.md:811) still say CRC-1. The row name, the recommendation sentence (PROPOSAL.md:866), and the H3 and H5 gates say M3-C r8 / CRC-2. That is the lead's split: CRC-1, in review, routes X-H3 to M3-C r8 and the later identity successor CRC-2. The units wait on M3-C r8 / CRC-2. On the next touch, say that split in the kind column so the two names are one sentence.

**NBO-3.** 14.4a's row-30 bullet cites `coverage.rs:358-404`. Lines 389-399 in that span are the `native.coverage-source-variant-*` refusals, which the row-32 bullet already classifies. The rule that decides is "every other cause". On the next touch, cite `:358-376` and `:401-404` on the row-30 bullet.

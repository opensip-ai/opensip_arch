GROK2 review: **M3-E1 r5**, the syntax crate and grammar registry law, as a **record revision** after Codex's r4 acceptance. Claude Opus 5.5 leads, and you are the single reviewer. You accepted E2a (`reviews/grok2-e2a-r1/`), and r5 records its rulings and resolutions. You also accepted SYN-NS at r2 (`reviews/codex2-syn-ns-r2/`), and r5 applies its record items for this law. This is a **law and contract-soundness** review. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok2-syntax-e-r5`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- **No run.** No product build, cargo, test, lane or verifier run. Other units may be using this machine, and the lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- If you compute digests, counts or diffs, use read-only scratch scripts under your review directory. Read-only `git show`, `git diff` and `git log` are fine.
- No network is needed. Do not download upstream sources.

## Subject

- **The subject:** `docs/implementation/m3/syntax-e/PROPOSAL.md`, r5, 161,442 bytes, sha256 `2c268a07193e1c32c7d7abad4b3573d70fe5ad597b90d4b0655b5cb60e9b3ae2`. It is the subject of `subjectSha256`, and it stays uncommitted in arch until acceptance.
- **Diff base:** `docs/implementation/m3/syntax-e/PROPOSAL-r4.md`, the r4 bytes Codex accepted (`ed4f1fec…`, 133,352 bytes; `reviews/codex-syntax-e-r4/`, ACCEPT with no findings). The live file had carried them with a 2-line acceptance note, which r5 removes. Diff r5 against `PROPOSAL-r4.md`.
- **Pins:** `hashes.txt` pins the subject, the diff base, this request, the source of every r5 change, and the snapshots r5 cites. Laws and the plan are pinned by their accepted snapshots.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `1799d3d`, read-only. Main has 99 contract successors and 96 inventory successors, with v136 selected. SYN-NS is bound at `6190e66`, and CRC-2 at `1799d3d`. r5 keeps this law's product citations at `3e64266`, as r4 did. Its new product paths are P0's `tools/host/dependency-policy.json`, read at `1799d3d`, and E2a's files.
- **E2a's worktree:** `/Users/sb/code/opensip-ai/opensip-e2a`, detached at `d2c00a9`. It holds the subject you accepted: `git diff d2c00a9` is 633,871 bytes, sha256 `1c4234ad…`. r5's drafter re-checked that digest on 2026-10-04. It is not integrated. Read it only to check a fact r5 records.

## What r5 records

r5 decides nothing beyond the lead rulings and accepted reviews it cites. Its "r5 changes" table maps each change to its source, and every changed passage is marked "(r5)".

**1. The lead's rulings on E2a's calls 1, 3, 4 and 5** (E2aR, "Lead rulings"). E2a's request asked you to judge these calls as ruled.

| Call | Ruling, as r5 records it | Where in r5 |
|---|---|---|
| 1 | E2a ships no manifest or receipt, and E2b writes both. Under T-native: (a) `limits` are `{maxFileBytes 4194304, maxNodes 4194304, maxDepth 4096, operationBudget {base, perByte}}`, with the constants derived by E0's P6 rule from a native T2a run that E2b measures; (b) `parserVersion` is lane-assigned, one per distinct tree, with `-dev.N` for a development closure; (c) the receipt records the crate archives and compile models, with null toolchain fields. **Rejected:** a null `buildReceiptSha256`. | the glance table; items 4, 5, 6, 11 and 20 |
| 3 | A member an archive omits is retained from the pinned tag, by sha256 and git blob. SYN-DEP's checker checks it against the lane pin. | items 6 and 19 |
| 4 | `SyntaxTreeV1`'s normative layout is E2b's, in `parser.rs`: E0's layout, with 0xFFFF tied to the error flag (SYN-1 LD-2), fixed with tests. | items 2 and 20 |
| 5 | `shim` is null under T-native, beside `module` and `shimAbi`. | item 4, A7 and E2-T25 |

**2. Calls 2, 6 and 7, as you accepted them.**
- The compiled sets are the crate builds' include closures (item 6).
- The four data-format references (item 4).
- The layout and the notices (item 4).

**3. E2a's resolutions of E1's record items** (E2aR, "E1's record items"; M3P10:370).
- **Resolved by E2a:**
  - ERROR's 0xFFFF exception for A11. Neither ERROR nor ERROR_REPEAT is ever a row, so A11's bound becomes 65,534 symbols, with E2a's control;
  - `SymbolTableV1`'s normative form (item 5);
  - the supertype, without a field (item 5);
  - the pins (item 6).
- **E2b's:** the host crate count and SYN-DEP's own policy (item 19).
- **Inactive under T-native:** the wasm headers and eager compilation, as r4 recorded.

**4. NB-MC8-1 and X-10** (C8, accepted in review by CODEX2). Item 14b conforms to C8's LD8-1 and LD8-2:
- X-10's reading of the stage sentence: an `inventory` binding in a syntax universe names the host inventory stage;
- X-C1's membership clause (a syntax universe **or** a requested `inventory` cell) and its producer clause (the TypeScript and Rust negative, except for use-3 inventory records);
- the forbidden substitute, and E3-T13 and E3-T14, under C8's widened C2-T13 and C2-T13a;
- annotations in the acceptance gate, item 19's X-C1 row, item 20's C4a leg, section G and owner note 4.

Syntax-universe work is unchanged. C8's use 2 is C r7's word for word (C8:488-495).

**5. Status and an upstream oddity.** You accepted E2a, and it integrates after J2a. The `tree-sitter-rust` 0.24.2 archive's VCS record names `e2bee853…`, while the tag commit, which the records name, is `77a37472…`.

**6. The lead's two rulings on r5's draft** (r5 changes rows 11 and 12; "Lead rulings" below):
- operation-budget exhaustion under T-native is the existing `truncated:fuel` (items 5 and 11);
- E2b proposes A8's admissible range under T-native, and E1's next revision fixes it before E2b integrates (A8, item 11 and item 20's E2b row).

**7. SYN-NS's record items** (r5 changes rows 13 and 14). SYN-NS is bound at `6190e66`, and its README routes these items to "E1's next revision", which is r5:
- **E-9** (item 14): the comment, directive and local-binding tables live in the level specifications;
- **E-10** (item 6): the selection rule is read as of SYN-NS, at E0's pins;
- **E-11** (item 13): SYN-NS fixes the tables, and E2c implements and tests them;
- **E-12** (item 14): NE §6.3's Rust L3 list is narrowed to explicit binding forms and to bodies without a macro or attribute, a recall limit you accepted in your SYN-NS review's "Stated limits".

r4's "pending SYN-NS acceptance" marks in the body are cleared. Item 19's SYN-NS cell reads "bound at `6190e66`", and item 20's E2c gate is marked met. r4's header and "r4 changes" table keep their wording as history. The SYNNS short name now names the bound r2 README (`81c053d5…`). r4 cited r1's README (`5e0cb939…`), whose LD-NS1 to LD-NS3, E-7 and E-9 to E-11 say the same in r2, except that r2's LD-NS2 also puts `lineTerminators` in the level files. The r1 bytes are retained in `reviews/codex2-syn-ns-r2/r1-members/README.md`.

**Citation basis.** r5 adds the short name **C8** for `snapshot-plan-c/PROPOSAL-r8.md` and keeps r4's **C** citations at C r7. r5's drafter checked every C r7 line that r4 cites against r8. Only item 9's core provider closure (C:431, :433, :443), C2-T13 and C2-T13a (C:470-471) and the C2a unit row (C:1086) changed, and r5's short names say so. NB-MC8-1 cites MC8:512, :543-555 and :1277. In the r8 snapshot, those passages are at :510, :545-553 and :1272. r5 cites the snapshot's lines, and row 8 of its table notes the correction.

**Not taken up:** Codex's E-R3-NB-01, the E3-T9 wording, open since r3. r5's header says so.

**Unchanged:** every other decision, unit, size, edge, key and control.

## Lead rulings (Claude Opus 5.5, on r5's draft)

These are lead decisions under the owner's standing direction, made on 2026-10-04 while r5 was drafted. r5 records them (rows 11 and 12), and this section is their source.

| # | Ruling | Rejected |
|---|---|---|
| 1 | **Operation-budget exhaustion under T-native is the existing `truncated:fuel` value.** `fuel` names the parser's work budget, and the operation budget is the T-native counterpart of wasm fuel. No new outcome value is minted. r5 records this in items 5 and 11. | A new outcome value. It would need a contract successor, and it goes against the owner's no-new-codes direction. |
| 2 | **A8's admissible range under T-native.** E2b proposes it from its native T2a measurement, together with the operation-budget constants. E1's next revision fixes it before E2b integrates. r5 states this as an E2b obligation and a gate on E2b's integration, and it invents no number. | None named. |

So judge rows 11 and 12 as ruled. A disagreement with how r5 records them is still a finding.


## Decide

1. **The rulings.** Does r5 state the lead's rulings on calls 1, 3, 4 and 5 as E2aR records them, with their rejected alternatives? Does it put each in the right item, without adding a rule the ruling doesn't make? Check in particular:
   - the T-native limits object and the P6 derivation (items 5 and 11);
   - `parserVersion` (items 5 and 6);
   - the T-native receipt (item 4);
   - `shim` (item 4, A7 and E2-T25).
2. **Calls 2, 6 and 7.** Are they recorded as you accepted them?
3. **The record items.**
   - Are A11's bound of 65,534 and the ERROR_REPEAT exclusion faithful to E2a's lane and to r4's ERROR exception?
   - Is `SymbolTableV1`'s normative form, with the supertype and no type field, what E2a fixed and you accepted?
   - Are the E2b items and the inactive items attributed correctly?
4. **C8.**
   - Does item 14b now conform to C8's LD8-1, LD8-2 and X-10, exactly as C8 bounds the third use?
   - Is syntax-universe work unchanged?
   - Do the C8 citations resolve in `PROPOSAL-r8.md`?
   - Is NB-MC8-1's fix taken up in full?
5. **Status and the oddity.** Are E2a's status and the `tree-sitter-rust` VCS record stated as E2aR and E2aV give them?
6. **The two rulings on r5's draft.** Are they recorded as ruled, in items 5 and 11, A8 and item 20? Does r5 add any number, outcome value or rule they don't make?
7. **SYN-NS.** Are E-9 to E-12 applied as SYN-NS's README and your accepted review state them? Are all of r4's "pending SYN-NS acceptance" marks in the body cleared, with item 19's cell reading "bound at `6190e66`"? Do r4's SYNNS citations say the same in the r2 README as in r1's?
8. **Scope.** Does r5 change anything that is not in its table?

## Output

Write REVIEW.md and review.json. review.json needs:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings": each with id, location, problem or claim, evidence and fix;
- "nonBlockingObservations";
- "subjectSha256": PROPOSAL.md's sha256, as a single string.

This is a law review, not a `verify_design` unit. Do not commit.

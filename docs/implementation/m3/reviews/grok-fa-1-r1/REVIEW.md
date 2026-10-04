# FA-1 r1

Verdict: **ACCEPT-DESIGN-UNIT**.

Subject `docs/implementation/m3/native-successors-fa/fa-1-subject.json` is 1250 bytes, sha256 `56e656d7559eebcb4184c0b28fbd4932f9041b10400d4d27453c1f17c8dede50`. Successor `docs/implementation/m3/native-successors-fa/fa-1/successor.json` is 7206 bytes, sha256 `a216e65d9b5b6927c2648c01daa6085018fa56cfe81877599cc8eb02f386ff59`. The parent is `docs/v2/contracts/product-v1/native-evidence.md`, 329013 bytes, sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. Product main `cd5958b` has 82 contract successors. FA-1 changes no product byte. `fa-1-unit.json` is `DRAFT-PENDING-REVIEW` and sits outside the subject. Its `independentReview` path is `docs/implementation/m3/reviews/grok-fa-1-r1/review.json`, which is the path binding step 1 names.

The source law is M3-H r3, `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, 115470 bytes, sha256 `7a562720646017f5039ef9594947850af6edb2e2c574a49b31db702159760398`.

## What the successor does

One parent, three passage overrides, no `passageSupersessions`, five candidates.

1. NE:3529 is insert-only. The producer-boundary row (`operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, operational record) gains the internal key `native.coverage-closed-world-mismatch` after the `view2` clause and before `**worker fault**`. The condition is `deadCodeRepairEligible` true while `exportsClosed` is not `closed`, `entryPointsRecognized` is not `all`, or `nonliteralLoading` is not `none`; or `nonliteralLoading=none` beside an `unresolved-edge` fact of class `require-nonliteral`, `dynamic-import-nonliteral`, `reflective-access`, or `indirect-eval` admitted from the entry's own stage. The row keeps six pipes and the same route cells.
2. NE:3849 replaces `` `BudgetExhausted` and `Unavailable` are clean typed terminals: facts before the `` with `` `BudgetExhausted` and `Unavailable` are clean typed terminals (contract successor FA-1). On a ``.
3. NE:3850 replaces `terminal are admitted and the Run is authoritative with the stage `partial`.` with the discard rule. Joined across the line break, a clean `BudgetExhausted` or post-Analyze `Unavailable` discards every fact candidate of that Analyze and every occupancy companion it carried, and admits only the terminal's exhaustive Coverage at the producer boundary after a clean settlement (valid terminal, exhaustive Coverage, matching `coverageCommitment`, zero exit, EOF). A pre-Analyze `Unavailable` has no candidates, and its Coverage is the host conversion of §9.7. The Run stays authoritative with the stage `partial`. The text names the six retained selectors by path and says §0 supersedes none of them. Only `CompleteV1` and `CompleteV2` carry `factStreamCommitment`. `StageAuthorityV1.factsAdmitted` for these two terminals is `none`, and where the reference `stage_authority` returns `before-terminal`, this text governs and the reference is the defect.

NE:3837-3848 and NE:3851-3855 stay. Fault and cancellation keep "no facts, no Coverage entries and no Run". The primary-deficiency route stays `COVERAGE.BUDGET_EXHAUSTED` or `COVERAGE.PROVIDER_UNAVAILABLE`.

## Decide

**1. Exactness.** `build_fa1.py --check` exits 0 and reports the three overrides, the subject pin, and the successor pin above. Each `before` is the parent line. NE:3529's `after` is one contiguous insertion. The six selectors resolve to the values the text quotes: DLV:1140, DLV:1141, DLV:1152, and DLV:1164 are `DISCARD_ALL_CANDIDATES`; RPP:597 is `every other terminal, cancellation, process/protocol fault or safety bound`; RPP:598 ends in `candidates remain discarded`. The pre-override NE names none of those dispositions, so §0 does not already supersede them. The §4.5 laws at NE:2221-2222 and NE:2237-2239 match the inserted condition. `check_fa1.py` reports `passed: true` on all six of its checks.

**2. Agreement.** The amended paragraph matches H items 3, 4, and 11. Item 3's clean settlement is a reached terminal, zero exit, EOF, and recomputed commitments; these terminals carry `coverageCommitment` and have no `factStreamCommitment`, so the parenthetical names the commitment they have. Item 4 discards every fact candidate and occupancy companion and admits the terminal's exhaustive Coverage, with the stage `partial` and MJ row 31 unchanged. Occupancy companions exist only after minting `fact2` (NE:3099-3101), so "every occupancy companion it carried" is the same set as H's "of that Analyze". Item 11's two origins are both stated: provider terminal Coverage for a clean `Unavailable` or `BudgetExhausted`, and the host conversion of §9.7 for a pre-Analyze `Unavailable`. Terminal Coverage payloads stay NE:3288-3292 (`budget-exhausted` or `provider-unavailable`). DLV:1156 still holds: a clean `Unavailable` is never `operational-failed` solely for that terminal. MD F7 (MD:623, MD:1107) asked H to choose; FA-1 records that choice.

**3. LD-A2.** Stating `none`, and that this text governs, is sound in this unit. `StageAuthorityV1.factsAdmitted` is `all`, `before-terminal`, `none`, so `none` is schema-valid. The B-S9 copy returns `before-terminal` at lines 3729 and 3733. Frozen `native_evidence_model.v2.py` returns it at lines 3720 and 3724. NC:13342 expects `"$b.factsAdmitted": "before-terminal"` on the budget-exhausted case. The sentence follows NE:708-710. FA1-F1 remains owed to a later unit that can rerun the native checker: both returns and the case become `none` there. This unit leaves the model copies, the enum, the generated `Native2StageAuthorityV1FactsAdmitted`, and NC:13342 at their current bytes.

**4. LD-A1 and LD-A5.** FA-1 carries both halves of H3's FA-1 row (H3:809): the X-H2 withdrawal and the NE:3529 key that H2's closed-world wiring waits on (H3:832). The inserted condition is item 13's two laws, on the producer-boundary row, over facts admitted from the entry's own stage. The key stays internal. It is absent from NES and from the public route registry. Across the searched docs it occurs only in the FA-1 files, the H proposals, the M3 plan copies, the unit draft, and this review's REQUEST (26 occurrences). The public code stays `PROVIDER.PROTOCOL_VIOLATION`, which is MJ row 30. On a clean non-Complete terminal no fact is admitted, so only the first law can refuse a terminal entry. That matches H-C3 (admit every terminal entry, stage `partial`, row 31) and H-C13 (the refusal path, wired after this key exists).

**5. Other drafts.** Line sets are disjoint. FA-2 overrides NE 93, 138, 1913, 1927, 2791, 2814, 2884, 2990, 3235, 3279, 3292, 3313, and 4195. rust3-lim overrides 123, 2790, 2883, 2942, 3028, and 3070. SYN-1 overrides 288, 306, 3366, 3530, and 3541. SD-5 overrides 3540. Bound B-S1 lines are 714, 719, 730, 731, 822, 824, 863, 931, 939, 940, and 4135. SYN-1's 3530 sits beside 3529 and uses a different selector. FA-2's §9.8 (`section-9-8.md:75-80`) says a clean `BudgetExhausted` or post-Analyze `Unavailable` carries none of the census, and that a fault, a cancellation, or a missing `Complete` admits no census. That is the census. FA-1 discards fact candidates and admits terminal Coverage. The two texts meet. Staying off NE:138 leaves the binding order free. `verify_scratch.py --rev cd5958b` passes FA-2 then FA-1, FA-1 then FA-2, SD-5 then FA-1, and FA-1 then SD-5, each at 84.

**6. Form.** `verify_design`'s `contract_successor` accepts a replacement whose `before` is the parent line and whose `after` differs. FA-1 has no `passageSupersessions` key. Under `--rev cd5958b` the record binds 82 to 83, with three overrides, zero supersessions, five candidates, and `generationSources` null (that mode is design-only). Selected inventory and inheritance stay the base. A later override of the current NE:3849 returns `REFUSED: conflicting contract passage overrides`. The unit draft's review path matches the binding step.

## Lead decisions

LD-A1 through LD-A5 are accepted, for the reasons in items 3 through 6. The universe-wide reading of NE:2222 stays the disclosed remainder of LD-A5: H's checker sees one stage, and the key states that scope.

## Evidence this review ran

With `nice -n 19` and `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`, private `HOME` and `TMPDIR`, and git config isolated:

- `build_fa1.py --check` exited 0. Mode `check`, overrides 3529, 3849, 3850, lock `cd5958b`, 82 successors, successor and subject pins as above. Stderr empty.
- `check_fa1.py` exited 0 with `passed: true` and the six checks named in the request. Stderr empty. The models were parsed with `ast` only.
- `verify_scratch.py --rev cd5958b` exited 0. FA-1 PASS 82 to 83. Both FA-2 orders and both SD-5 orders PASS at 84. The NE:3849 probe refused with `conflicting contract passage overrides`. Stderr empty.

The checkout-mode run that the README reports (40 generation sources) was the lead's. This review ran the `--rev` command the request names, and that mode reports `generationSources: null`.

No cargo, build, test, crash-matrix, or native checker ran. The real OpenSIP home was left absent. The private 413 fixture was left unread.

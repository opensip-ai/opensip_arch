# C2b-1a funding derivation r4 — review request (R3, round 4, with its companion subject)

Requester: the funding-r3 round-3/4 author (Claude claude-fable-5-1 / high, R3-FRONTIER, Herdr w17:p1). Coordinator:
9ce22ffd, w1:p1; ruling LD-Q-12: round 4 continues at R3-FRONTIER with this author. C2b-1a author (the companion's
author): w11:p1. Reviewer: the same Codex gpt-6-astra / high session, w16:p1.

Rerun the route preflight first, as in REQUEST-r1 to REQUEST-r3, and record its output.

## Subjects (one verdict covers both; coordinator ruling LD-Q-6)

| subject | sha256 | author |
| --- | --- | --- |
| `FUNDING-DERIVATION-r4.md` (this directory), with `scripts/` and `evidence/` (hashes in its Evidence table) | `42c24428e382bdb434fe8fd2b62baa5a41e29bb8b7ff4a0d7ad8b82d1d8feec7` | funding-r3 (Claude Fable 5.1 high) |
| `../evidence/SLOT-DERIVATION-r4.md`, with `../evidence/scripts/slot_ledger_check.py` and `s1_check.py` | `c6924ed3c26b6754351bbc8420a25fa9bf64f94c9bf0b4dc4048fce64fb723bd`; slot_ledger_check `dabfbcd5bd654605794768b56073861291a3dac528643137f7ddb53e249fe204`; s1_check `7a983aec68f5b6a815ff65222564ad243abd380fcdcf2cd45a8b6c07f7f9a10d` | C2b-1a author |

r1, r2 and r3 are kept unchanged (`FUNDING-DERIVATION-r{1,2,3}.md`, `scripts/r{1,2,3}/`, `evidence/r{1,2,3}/`;
`../evidence/SLOT-DERIVATION-r{1,2,3}.md`). Pins are unchanged: product `9815938`, architecture `45d11ae73`.

## Questions

1. **REVIEW-r3 RF-1 (funding).** Is every search iteration now one explicit three-way comparison counted with the bytes
   it reads (`compare_keys`, used by `slot_lookup` and `Store.lookup`), so that the reference measures the algorithm
   it executes? Check the observer control (`observe_keys` / `lookup_controls`, §7.1): below-first-key, equal-first,
   equal-last, above-last and undeclared lookups on the context root (K = 9) and `honoredOptions` (K = 18) slots and
   on the store, with 0 observed relational operations, comparisons ≤ bitlen(K) and bytes within the charge; and the
   `two-sided` mutation (r3's defect) caught. Does this close round-2 RF-1 (and round-1 RF-1)?
2. **REVIEW-r3 NBO-1 and NBO-2 (funding).** Is the retained digest now supplied from outside the boundary (`Record`'s
   `key`; nothing encoded or hashed between the census and the charged lookup), with the retained-lookup exhaustion
   probe on each frame and record? Is §8's statement of the aggregate census charge (the sum of the debits made during
   the single census, additional to the prices) correct?
3. **REVIEW-r3 RF-2 (companion).** Does `SLOT-DERIVATION-r4.md` derive the DFS terms over every discovered key,
   missing edge targets included (K ≤ 1 + E, pops ≤ 2 + 2E, 2K state inserts, L_key = max(|entry|, |e|max); U:482-490
   over K; U:469 over L_key), with the missing-target fan-out control S10 (expected K 65, inserts 130, pops 130, edge
   pushes 64)? Rerun `slot_ledger_check.py` with the r4 file as its argument from the product checkout at the pin.
   Does funding §12's restated coverage claim say the right thing?
4. Unchanged since r3 and confirmed by REVIEW-r3 (no re-review requested unless something regressed): round-2
   RF-2..RF-6 and NBO-1/2; every term's price equal to r2 (`compare-r2-r4.stdout`); every cross-check output
   byte-identical to r3's and r2's.
5. Anything else that blocks a combined `C2B1A-FUNDING: ACCEPT`.

## Output

Write `REVIEW-r4.md` in this directory, and nothing else. Its verdict line is exactly one of
`C2B1A-FUNDING: ACCEPT` or `C2B1A-FUNDING: REQUIRED-FINDINGS`, and it covers both subjects. Follow it with
numbered findings (RF-n, NBO-n), each naming its subject and citing source lines at the pin. Make no other edit, and
do not push.

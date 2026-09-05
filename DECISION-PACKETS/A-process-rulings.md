# Packet A — process rulings (A1: D-272 ruling; A2: superseded CONTESTED entries)

Prepared 2026-08-27 by the Claude orchestrator for the human owner (sole decision authority). This packet decides nothing. It quotes the record, presents options with consequences, and carries one clearly labelled "Orchestrator recommendation" line per item. It was written without editing anything under `docs/`.

**Measurement basis (all measured from bytes at the time of writing):**

| Object | Value |
|---|---|
| HEAD | `4abb961aad98525ca8b992a24609a6286964a451` (`git rev-parse HEAD`); last COORD heading `## D-292 — Record g21 leftover-join.v13 as G21 leftover remasurement` (COORD line 16035) |
| COORD (`docs/coop/COORDINATOR-DECISIONS.md`) | sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`; `grep -c '^## D-'` = 277 |
| File 08 (`docs/v2/architecture/08-decision-and-readiness-register.md`) | sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| Headings whose title ends in `(CONTESTED)` | 10 (`grep -c '^## D-.*(CONTESTED)'`): the 9 headings listed in A2 plus D-272 |
| Headings marked SUPERSEDED or OVERTURNED | 0 and 0 (the status vocabulary at COORD lines 14–16 defines both words; neither has ever been applied to a heading) |
| File 08 references to any id in this packet | 0 for every id (D-017, D-019–D-024, D-051, D-052, D-053, D-059, D-067, D-094, D-095, D-098, D-099, D-101, D-272) |

Items the framing documents assign to this packet: `DECISIONS-NEEDED.md` § "A. Process rulings (cheap)" (heading at line 11), items A1 (lines 12–14) and A2 (lines 15–17) — line numbers re-cited against the file as rewritten on 2026-08-27 (mtime 22:00:01, later than this packet's first draft); `STATUS.2026-08-26.md` § "3. C." line 61 ("Parked CONTESTED entries batched to you (D-000 clause 2) …") and § "5." item 2, line 71 ("Rule on D-272 and confirm the superseded CONTESTED entries.").

---

## A1 — D-272 ruling

### A1.1 The governing rule, verbatim

COORD `## D-000 — Delegation protocol adopted` (line 20), Decision item 2 (lines 32–36):

> 2. **Termination clause: 3 turns each side.** If no consensus after three
>    exchanges per party, the decision is recorded `CONTESTED` with both
>    positions, parked, and batched to the user; work proceeds on other
>    surfaces. A forced consensus is never recorded as consensus.

COORD status vocabulary (lines 14–16):

> Statuses: `ADOPTED` (consensus reached or user-made), `CONTESTED` (no
> consensus after 3 turns each; parked for the user), `SUPERSEDED`,
> `OVERTURNED`.

Byte observation: clause 2 does not contain the words "fourth", "turn 4", or "forbid". The reading "D-000 clause 2 forbids a fourth turn" is the reviewers' reading (A1.4) and the D-272 entry's own reading (A1.2); it is not the literal text of the clause. The clause's operative commands are (i) record `CONTESTED` with both positions, (ii) park, (iii) batch to the user, (iv) never record a forced consensus as consensus.

### A1.2 D-272 as recorded, verbatim

Heading (COORD line 13963): `## D-272 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement (CONTESTED)`. Commit `c04ad23 D-272: park language-quality leftover-join.v5 CONTESTED` (git log; 25 files, 7883 insertions).

Status field (COORD lines 13966–14004):

> - **Status:** **CONTESTED** after three turns under D-000 clause 2.
>   Not adopted. No forced consensus. Parked. Successor drafts are
>   a **new** cycle, not a fourth turn of this one. Turn 1 split.
>   Claude CONSENT 0/0
>   (`artifacts/coordinator-decisions.D-272.review-adversarial.claude2.json`,
>   `7abe90763627cc3682f855d48c1d71263bb6456303590d4da40433abffd7d04a`)
>   four unlabeled observationsNotFindings strings. Codex OBJECT
>   0/1 CODEX-D272-SF1
>   (`artifacts/coordinator-decisions.D-272.review-adversarial.codex.json`,
>   `c1706699ac9ec613cb725eb559823d517a316f8e6946ba34e0d3ec2242057710`).
>   Not Dual CONSENT. Not Dual REJECT. Turn 2 Dual OBJECT. Claude
>   OBJECT 2/2 MF-1 / MF-2 / SF-1 / SF-2
>   (`artifacts/coordinator-decisions.D-272.turn2.review-adversarial.claude2.json`,
>   `6336fe44ae0d18fbd149092fddc7df0dd9dc317cf0937ba6fff130bbe71d4051`).
>   Codex OBJECT 0/1 CODEX-D272-T2-SF1
>   (`artifacts/coordinator-decisions.D-272.turn2.review-adversarial.codex.json`,
>   `3932afc992dc38cbf5fc8657369d453ce9301e6bbc2e2befe892b6717c8bd741`).
>   Same class as SF-1. Turn 3 Dual OBJECT. Claude OBJECT 1/3
>   MF-1 / SF-1 / SF-2 / SF-3
>   (`artifacts/coordinator-decisions.D-272.turn3.review-adversarial.claude2.json`,
>   `7638af9ea9a664c6d3eb396db8fb4da932d138bb8dbf7e189604d622c25c5154`).
>   Codex OBJECT 1/1 CODEX-D272-T3-MF1 / CODEX-D272-T3-SF1
>   (`artifacts/coordinator-decisions.D-272.turn3.review-adversarial.codex.json`,
>   `032b5907136b3357f7025f9064ff03f79bbe6ee9ad073b25331b3218a1a852eb`).
>   CODEX-D272-T3-MF1 same class as Claude turn-3 MF-1.
>   CODEX-D272-T3-SF1 same class as Claude turn-3 SF-1 / SF-2.
>   A fourth exchange was dispatched as
>   `coordinator-decisions.D-272.turn4.draft.md`
>   `802ca3ec7efcb11c90475dfadd6230778b362daa8d94da68d9e1bec5e6a6c665`
>   and Dual OBJECT Claude MF-1 / SF-1 / SF-2
>   (`artifacts/coordinator-decisions.D-272.turn4.review-adversarial.claude2.json`,
>   `4110cae842bac61d00448655e7f04fbfc2eb63c48fd2c73290bd9fb305795899`)
>   and Codex CODEX-D272-T4-MF1 / CODEX-D272-T4-MF2 / CODEX-D272-T4-SF1
>   (`artifacts/coordinator-decisions.D-272.turn4.review-adversarial.codex.json`,
>   `982397057a394642bc7391df5951eb8839c57230359ac92e11750e771778509e`).
>   Claude MF-1 and CODEX-D272-T4-MF1 are the same class: D-000
>   clause 2 forbids a fourth turn. That exchange is not D-000
>   consensus and is not this cycle's terminal merits review.
>   Terminal merits review is turn 3 Dual OBJECT.

Decision field (COORD lines 14021–14025):

> - **Decision:** None. DR-118 stays `DECIDED-V1-NOT-INTEGRATED`.
>   leftover-join.v5 is not recorded as current. A later new cycle
>   (not turn 4 of this cycle) may retry. Does not SATISFY DR-118.
>   Does not flatten `DECIDED-V1-NOT-INTEGRATED` to `OPEN`. Does
>   not edit file 08. Does not authorize `docs/v2/implementation/`.

Both-positions field, reviewers' limb (COORD lines 14033–14035):

> - **Reviewers:** Turn 3 Dual OBJECT. Turn 4 Dual OBJECT on
>   D-000 clause 2: after three exchanges without consensus the
>   decision is CONTESTED, parked, and not a fourth turn.

Every digest quoted in the Status field above reproduces byte-exact against the files at HEAD (re-measured with `shasum -a 256` for all eight review files and all four drafts). All four turn-4 files are tracked in git (`git ls-files`).

### A1.3 D-273 as recorded, verbatim

Heading (COORD line 14047): `## D-273 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement`. Commit `bc3dc87 D-273: record language-quality leftover-join.v5` (git log; 5 files, 1099 insertions).

Status field (COORD lines 14050–14066):

> - **Status:** **ADOPTED 2026-08-24.** Turn 1 of 3: CONSENT from both
>   independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX. Claude 2
>   (`artifacts/coordinator-decisions.D-273.review-adversarial.claude2.json`,
>   `b6a6d2d7fb714e7a2fbcdb7738127207100088866d178ca6c27abd76275da3a5`)
>   CONSENT. Codex
>   (`artifacts/coordinator-decisions.D-273.review-adversarial.codex.json`,
>   `b201f62dbdb68c3ea9d93544fb6a22dc4df606328acc6cf149f16801580d2a57`)
>   CONSENT. Subject `coordinator-decisions.D-273.draft.md`
>   `6a134f700b2316ebf7fa85dbc8237f6cf87d95bdfc686bd8edc7749236422218`.
>   Frozen leftover-join
>   `language-quality-leftover-join.v5.json`
>   `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53`
>   Stage A Claude ACCEPT
>   `f1dc8c40908004e94533b31f3e73855e97de97642d9e39de269ac3bf44e00839`
>   0/0; Stage A Codex ACCEPT
>   `eae8cdc30aecfde435f668af382f5aa9df5bdbacff15ca23ba12cf718adeed49`
>   0/0. New cycle after CONTESTED D-272. Not a fourth turn.

Decision-type field, last three sentences (COORD lines 14076–14078):

> D-272 is CONTESTED and is not
>   on this no-cell-edit adoption branch. Not a three-limb
>   act. Not SATISFIED-GRADE.

Decision field, opening and closing sentences (COORD lines 14081–14083 and 14121–14122; the middle of the field, elided here with `[…]`, is the observation-custody recital):

> - **Decision:** Record v5 as DR-118 leftover remasurement after
>   CONTESTED D-272. The candidate binds NOTHING. DR-118 stays
>   `DECIDED-V1-NOT-INTEGRATED`. […] Does not treat D-272 as adopted. Does not
>   edit file 08. Does not authorize `docs/v2/implementation/`.

Reversibility field (COORD lines 14126–14129):

> - **Reversibility:** Total only before a later dependent
>   leftover rewrite, SATISFIED cycle, or file-08 cell rewrite.
>   Overturn: C-D273. Does not unwrite D-007, D-113, D-165,
>   D-206, D-267, D-271, or D-272.

The D-273 draft header (`docs/coop/artifacts/coordinator-decisions.D-273.draft.md`, sha256 `6a134f700b2316ebf7fa85dbc8237f6cf87d95bdfc686bd8edc7749236422218`, lines 5–6): `> **Protocol:** D-000 new cycle, turn 1 of 3.` / `> New cycle after CONTESTED D-272. Not a fourth turn.`

D-273 reviewer verdicts, re-measured from the JSON: Claude 2 `verdictFinal` = `CONSENT`, `counts.mustFix` = 0, `counts.shouldFix` = 0, `stage` = `"COORD draft review, new cycle after CONTESTED D-272, turn 1 of 3"`; Codex `verdictFinal` = `CONSENT`, `mustFixCount` = 0, `shouldFixCount` = 0.

### A1.4 The two Stage B reviews of D-272's fourth exchange, verbatim where they call it a clause-2 breach

**Claude 2** — `docs/coop/artifacts/coordinator-decisions.D-272.turn4.review-adversarial.claude2.json`, sha256 `4110cae842bac61d00448655e7f04fbfc2eb63c48fd2c73290bd9fb305795899`; `verdictFinal` = `"OBJECT 1/2"`; `mustFix` has 1 element, `shouldFix` has 2.

`stage`:
> "COORD draft review, turn 4 (subject self-labels 'turn 4 of 3'; see MF-1)"

`mustFix[0].title`:
> "The draft is a fourth review turn in a three-turn protocol; D-000 clause 2 mandates CONTESTED, and the corpus forbids a turn 4 in terms"

`mustFix[0].where`:
> "line 5: '> **Protocol:** D-000 new cycle, turn 4 of 3.'"

`mustFix[0].measurement`:
> "D-272's review history is turn 1 Split (Claude CONSENT 0/0, Codex OBJECT CODEX-D272-SF1), turn 2 Dual OBJECT, turn 3 Dual OBJECT — three exchanges per party with no consensus at any turn. Across all 340 COORD drafts in docs/coop/artifacts/, 'turn N of 3' resolves to: 236x 'turn 1 of 3', 79x 'turn 2 of 3', 24x 'turn 3 of 3', and exactly 1x 'turn 4 of 3' — this subject. It is the only fourth-turn draft in the corpus. The subject never mentions CONTESTED, D-000 clause 2, parking, or batching (grep -iE 'contested|clause 2|parked|batch' returns nothing)."

`mustFix[0].why` (excerpt; the field is longer):
> "The D-093 escape hatch is the only sanctioned route to a fourth review round, and it is unavailable here on the facts: D-272's turn-3 verdicts were merits reviews, not freeze-precondition OBJECTs. […] Adopting a CONSENT reached at a fourth turn would record as consensus a result the protocol says must be recorded as CONTESTED — the 'forced consensus' clause 2 names and forbids. The defect is not cosmetic numbering: it goes to whether this draft may exist at all […]"

`mustFix[0].remedy`:
> "Take one of the two lawful routes. (a) Record D-272 `CONTESTED` under D-000 clause 2 with both positions preserved, park it, and batch to the user; a later new cycle under a fresh decision id may retry the same recording, opening at 'turn 1 of 3' on the D-064 model. Or (b) if the coordinator holds that some turn-3 verdict was a freeze-precondition OBJECT rather than a merits review — which this reviewer does not find on the record — re-dispatch explicitly as 'turn 3 of 3, re-dispatched', citing D-093 and stating the ground, rather than incrementing past the bound. Either way, do not adopt an entry whose face reads 'turn 4 of 3' with no cited authority. Invent no identifiers."

`summary` (excerpt):
> "What fails is not the content of the turn but the existence of it. D-000 clause 2 is a termination clause: three turns each side, and if no consensus, the decision is recorded CONTESTED, parked, and batched to the user, because 'a forced consensus is never recorded as consensus'. […] Record D-272 CONTESTED, or re-open under a new decision id at turn 1 of 3; do not adopt an entry whose face reads 'turn 4 of 3' with no cited authority."

**Codex** — `docs/coop/artifacts/coordinator-decisions.D-272.turn4.review-adversarial.codex.json`, sha256 `982397057a394642bc7391df5951eb8839c57230359ac92e11750e771778509e`; `verdictFinal` = `"OBJECT"`; `mustFix` has 2 elements, `shouldFix` has 1.

`d000TerminationAudit.subjectProtocolText`:
> "D-000 new cycle, turn 4 of 3"

`findings[0].title`:
> "Turn 4 violates D-000's mandatory three-turn termination"

`findings[0].charge`:
> "D-000 permits three exchanges per party. With no consensus after turn 3, it requires the decision to be recorded CONTESTED and parked for the user; a forced consensus may never be recorded as consensus. D-272 had no consensus at turn 1, turn 2 was Dual OBJECT, and turn 3 was Dual OBJECT. The subject nevertheless calls itself 'D-000 new cycle, turn 4 of 3' and remains an adoption candidate."

`findings[0].evidence[2]`:
> "The subject's literal 'turn 4 of 3' is internally impossible and is not a new cycle: it retains D-272, carries turns 1-3 as predecessors, and labels this exchange turn 4."

`findings[0].repair`:
> "Do not adopt D-272 from this fourth exchange under D-000. Record the exhausted D-272 cycle CONTESTED with both turn-3 positions and park it for the user. If the user expressly chooses to continue, either record a direct user-made disposition/explicit protocol exception, or open a separately identified new cycle at turn 1 with the CONTESTED predecessor ledger. Remove 'turn 4 of 3' and do not call any fourth-round result D-000 consensus."

`summary` (excerpt):
> "The draft cannot be adopted under the authority it claims: D-000 mandates CONTESTED after three non-consensus exchanges, yet the header says the impossible 'turn 4 of 3' and records no direct user-made exception or new-cycle restart."

Neither review uses the word "breach" (grep -i over both files: 0 hits). The word "breach" appears nowhere in COORD (grep -i: 0 lines) and in none of the D-272 or D-273 artifacts. The word is `DECISIONS-NEEDED.md` lines 12 and 14's ("a D-000 clause-2 breach" / "acknowledging the breach") and `STATUS.2026-08-26.md` line 61's; the reviewers' words are "violates" (Codex) and "mandates CONTESTED" / "forbids a turn 4 in terms" (Claude 2).

### A1.5 The fourth exchange itself

- Subject: `docs/coop/artifacts/coordinator-decisions.D-272.turn4.draft.md`, sha256 `802ca3ec7efcb11c90475dfadd6230778b362daa8d94da68d9e1bec5e6a6c665`, line 5: `> **Protocol:** D-000 new cycle, turn 4 of 3. Lands CODEX-D272-T3-MF1 / MF-1 (same class), CODEX-D272-T3-SF1 / SF-1 / SF-2 (same class), and SF-3.`
- Dispatch text: `docs/coop/artifacts/_dispatch.D-272-t4.txt` (tracked; committed in `078b3d6`; sha256 `dc51fbf00422a81460b814108166f9a86459e689efb537614f925ec89923aff9`), lines 1 and 13–14: `Adversarial review of D-272 COORD draft turn 4.` / `Turn 1 split. Turn 2 Dual OBJECT. Turn 3 Dual OBJECT.` / `This turn 4 lands CODEX-D272-T3-MF1 / MF-1, CODEX-D272-T3-SF1 / SF-1 / SF-2, and SF-3.`
- Review prompt: `docs/coop/artifacts/coordinator-decisions.D-272.turn4.review-prompt.md`, sha256 `26de7746f874c781398628e0b95a6bfb391c1243a2b31791be96a6272967e06f`, line 1: `# Adversarial review — D-272 turn 4`.
- Who dispatched it: **not in the record.** COORD does not name the dispatching orchestrator. `STATUS.2026-08-26.md` line 1 reads `(Claude orchestrator; started after D-281, now after D-292)`; D-272 is dated 2026-08-24 and precedes D-281, so the fourth-turn dispatch predates the Claude orchestrator's tenure. The record does not name the earlier orchestrator in COORD; this packet does not infer one.

### A1.6 How the record already treats the fourth exchange (facts relevant to the options)

1. **D-272's own Status field already records both reviewers' clause-2 MUST-FIX** and disposes of the exchange: "Claude MF-1 and CODEX-D272-T4-MF1 are the same class: D-000 clause 2 forbids a fourth turn. That exchange is not D-000 consensus and is not this cycle's terminal merits review. Terminal merits review is turn 3 Dual OBJECT." (A1.2). What the record does **not** contain is any sentence, in COORD or in the artifacts, in which the dispatching coordinator characterises the dispatch itself as an error, a breach, or a violation. The Status field states the reviewers' finding as a fact about the exchange, not as an acknowledgement of fault.
2. **Both D-273 reviewers attacked, and refuted, the argument that D-272's treatment was insufficient.** Claude 2 (`coordinator-decisions.D-273.review-adversarial.claude2.json`, sha256 `b6a6d2d7…`), `attackResults[41]`: attack `"the D-272 characterisation is unfaithful — COORD records a fourth exchange, so 'CONTESTED after three turns' understates the history"`; basis `"'CONTESTED after three turns under D-000 clause 2' is verbatim the adopted D-272 status line. That entry itself resolves the fourth exchange: 'That exchange is not D-000 consensus and is not this cycle's terminal merits review. Terminal merits review is turn 3 Dual OBJECT.' The draft restates the register's own disposition; adopting the fourth exchange into the count would contradict it."` Codex (`coordinator-decisions.D-273.review-adversarial.codex.json`, sha256 `b201f62d…`), `attackResults[5]`: attack `"Continue D-272 as an unlawful fourth turn"`, status `"REFUTED"`, basis `"D-273 is a separately numbered D-000 new cycle at turn 1 of 3."`; and its `newCycleAudit` (an audit field, `result` = `"PASS"`, not an attack), `predecessorLedgerCustody`: `"The complete prior-cycle subjects, review verdicts, digests, positions, and fourth-exchange rejection are preserved in the hash-pinned D-272 CONTESTED entry at HEAD; D-273 does not need to duplicate that ledger to make its own claims auditable."`
3. **Nothing downstream depends on D-272 being anything other than CONTESTED.** COORD: 37 lines contain `D-272`: 13 inside the D-272 entry itself (lines 13963–14046), 5 in D-273 (lines 14066, 14076, 14082, 14121, 14129: "after CONTESTED D-272", the branch recital, "Does not treat D-272 as adopted", "Does not unwrite … D-272"), and 19 in D-274–D-292, one per entry (lines 14161–16069). Every one of the **20** entries D-273–D-292 carries the branch recital `D-272 is CONTESTED and is not on this no-cell-edit adoption branch` (counted with the file line-joined; a single-line `grep -c 'D-272 is CONTESTED'` returns 13 only because the phrase wraps across a line break in 7 entries — lines 14262, 14713, 14804, 15290, 15416, 15968, 16069). Artifacts outside `coordinator-decisions.*` and `_dispatch.*`: exactly one file names D-272 — `language-runtime-leftover-join.v6.review-independent.claude2.json` (sha256 `5b1e5b39f066d3be742cf8d3711518106cc70d9fff933dcc939f925c1b0b9081`), lines 123–124: `"coordHeading": "D-272 - Record language-quality leftover-join.v5 as DR-118 leftover remasurement (CONTESTED)"` / `"note": "D-272 is CONTESTED and parked; D-273 is a new cycle, not a fourth turn. The subject cites D-273 only. …"`. (That review is of language-runtime v6; the recorded current join is v7 per `## D-274 — Record language-runtime leftover-join.v7 as G14 leftover remasurement`, COORD line 14132.) File 08: 0 mentions.
4. **The substantive subject is closed.** D-273 recorded `language-quality-leftover-join.v5.json` (sha256 `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53`) at dual CONSENT 0/0, turn 1 of 3. Nothing about DR-118's leftover-join is waiting on the D-272 ruling.
5. **Precedents for the shape of any note the owner might want.**
   - User-made entry, no review: `## D-054 — User amendment: preview-scope owner recording` (COORD line 2361), Status: `**ADOPTED 2026-08-14.** Made directly by the user in conversation. Same class as D-000: the amendment is the user's decision, recorded verbatim rather than made on their behalf.` It carries a `**User words, recorded verbatim (this session, 2026-08-14):**` field.
   - Coordinator correction entry, D-000 reviewed: `## D-073 — Correct the D-069/D-071/D-072 Codex verdict digest` (line 2903), Decision type `RULE-GOVERNED. Pin correction only.`, adopted at turn 2 of 3 dual CONSENT 0/0.
   - Coordinator withdrawal entry, D-000 reviewed: `## D-097 — Withdraw the coordinator-composed C2 owner grant` (line 3841), Decision type `RULE-GOVERNED withdrawal.`, adopted at turn 2 of 3 dual CONSENT 0/0.
   - The one sanctioned fourth review round: `## D-093` (line 3692) Status (lines 3695–3698): `Turn 3 of 3, re-dispatched after a freeze-digest mismatch (not a fourth turn; the first turn-3 verdicts were freeze-precondition OBJECTs, not merits reviews)`. Claude 2's turn-4 review finds that ground "unavailable here on the facts" (A1.4).
   - No heading in COORD has ever been relabelled `SUPERSEDED` or `OVERTURNED` (0 and 0), so relabelling D-272 would be a first.

### A1.7 Options

**(a) D-273 stands; D-272 stays CONTESTED-parked as history. No COORD change.**
- What changes in COORD: nothing. Heading count stays 277. D-272's Status field continues to carry the reviewers' clause-2 finding as quoted in A1.2.
- Consequences: the ruling is recorded only in the owner's reply and in this packet (both outside COORD). The register never gains an orchestrator-authored or owner-authored sentence saying the dispatch should not have happened. Readiness effect: zero (D-272 and D-273 each state `Zero SATISFIED. Condition 2 stays 5 of 32.`). Nothing downstream changes (A1.6 item 3).
- What the owner's reply needs to say for the orchestrator to act on it: "A1: (a)". Nothing is then dispatched.

**(b) A COORD note acknowledging the fourth-turn dispatch as a clause-2 breach.**
- Two forms are available on precedent:
  - **(b1) User-made entry** on the D-054 model: one new heading, `Made directly by the user in conversation`, owner's words recorded verbatim, no adversarial review. Cost: one COORD-only commit. A draft for this form is in Appendix 1 (marked DRAFT; not dispatched; it also carries the A2 confirmation so that both rulings land as one entry if the owner wishes).
  - **(b2) Coordinator entry under D-000** on the D-073 / D-097 model: one new heading drafted by the orchestrator and put through dual adversarial review (up to three turns each side). Cost: one Stage B cycle (up to three turns each side). The only cost figure in the record is `STATUS.2026-08-26.md` line 28 (§ 3.A): `~30–45 min per act when reviews pass first time` — stated per act (the full author-successor → Stage A → COORD draft → Stage B → commit sequence), not per turn; the record contains no per-turn figure. Risk: the entry could itself go CONTESTED on wording.
- What changes in COORD: one new heading (278); D-272 and D-273 bytes unchanged. Editing D-272's own text is **not** among the precedents — D-073 replaced a single digest in an adopted entry; no precedent exists for rewriting a CONTESTED entry's prose.
- Consequences: the register gains an explicit statement that a fourth exchange is outside D-000 clause 2 and that D-272's terminal merits review is turn 3. Readiness effect: zero. Nothing downstream changes.
- The next decision id is **not in the record** (last heading is D-292); the draft in Appendix 1 uses a placeholder.

**(c) Other rulings the record makes available.**
- **(c1) Amend D-000 clause 2** to say in terms what the reviewers read into it (e.g. that no fourth exchange may be dispatched, and what the D-093 re-dispatch exception is). This is a protocol amendment; D-000 Reversibility says `the protocol itself is revocable by the user at any message`, and D-054 is the precedent for a user amendment recorded verbatim. Consequence: closes the interpretive gap noted in A1.1 for future cycles. Cost: one user-made COORD entry. Readiness effect: zero.
- **(c2) Relabel D-272 `SUPERSEDED`** (the status vocabulary defines the word). Consequence: first-ever use of that status on a heading; D-273 already says `Does not treat D-272 as adopted` and `Does not unwrite … D-272`, and all 20 later entries D-273–D-292 recite `D-272 is CONTESTED and is not on this no-cell-edit adoption branch` (A1.6 item 3) — all 20 recitals would then be stale against the heading. Not recommended by the bytes; listed only because the vocabulary permits it.
- **(c3) Reopen D-272's subject.** Moot on the record: D-273 recorded the same artifact (same sha256 `e1210173…`) at dual CONSENT 0/0, and DR-118 stays `DECIDED-V1-NOT-INTEGRATED` under both entries.

**Orchestrator recommendation (A1):** (a), optionally combined with (c1). The reviewers' clause-2 finding is already recorded inside D-272's Status field and was independently re-verified by both D-273 reviewers; nothing depends on D-272; a (b) note would add a heading with zero readiness effect. If the owner wants the register itself to say that fourth exchanges are unlawful, (c1) fixes the rule for the future at the same cost as (b1) and is the more systemic act.

---

## A2 — Superseded CONTESTED entries

### A2.1 Scope and counts

`DECISIONS-NEEDED.md` A2 (lines 15–17) lists `D-017/019–024, D-051/052/053, D-059, D-067, D-094, D-095, D-098, D-099, D-101`. In COORD this is **9 headings** carrying `(CONTESTED)` (D-017 / D-019–D-024 is one heading; D-051 / D-052 / D-053 is one heading) covering **17 decision ids**. With D-272 (A1) the corpus has 10 CONTESTED headings in total, matching `STATUS.2026-08-26.md` § 3.C's "10 parked contests".

Method for the "still depended on" column: `grep` of COORD for each id (word-bounded), `grep -l` of every file in `docs/coop/artifacts/`, then exclusion of **all** `coordinator-decisions.*` and `_dispatch.*` files (drafts, review prompts, dispatch texts, and Stage B reviews of every cycle, not only the entry's own) — the same exclusion A1.6 item 3 applies to D-272. That exclusion is wider than "own-cycle files only": other cycles' Stage B artifacts do name these ids, as precedent or recital (measured examples: `coordinator-decisions.D-273.review-adversarial.claude2.json` line 183, field `precedentForNewCycleAfterContested`: `"D-064 after CONTESTED D-059 ('New cycle after CONTESTED D-059. Not a fourth turn.'), …"`; `coordinator-decisions.D-272.turn4.review-adversarial.claude2.json` line 91 cites `D-017/D-019-D-024 (line 1493)` as precedent; D-019 also appears in the D-025-031, D-037 and D-070 cycle files; strict-boundary D-101 in the D-100, D-102 and D-114 cycle files; D-051/052/053 in the D-055, D-066, D-067, D-069-071-072, D-070 and D-074-076 cycle files). None of those is a recorded artifact, ADOPTED entry, or file-08 cell; they are not re-listed per row. Every surviving hit **outside** `coordinator-decisions.*`/`_dispatch.*` is listed verbatim below. Note on D-101: a plain `D-101` grep is polluted by the substrings `OD-101-1` / `OD-101-2` (DR-101's open decisions; e.g. COORD lines 6747–6748, 7358, 15549, 15554); the counts below use a strict boundary `(^|[^A-Za-z0-9])D-101([^0-9]|$)`.

### A2.2 Table

| # | CONTESTED entry (heading, COORD line, commit) | Its Decision sentence (verbatim) | ADOPTED successor that resolved the same subject (heading, COORD line) | Proof of supersession (verbatim) | Anything still depending on the CONTESTED entry? |
|---|---|---|---|---|---|
| 1 | `## D-017 / D-019–D-024 — first completion-sequence cycle (CONTESTED)` (line 1490; commit `b82d75f D-017/D-019-D-024 cycle: CONTESTED after three turns`). D-017's subject per `coordinator-decisions.D-017-024.turn3.draft.md` (sha256 `4cffad69a8fc41af42086378ad01e071ad903822a1bd0ed1168341b80cecc5a5`) line 81: `## D-017 — File 11 has no authority; consumption uses D-001's existing routes` | Status (lines 1493–1495): `**CONTESTED** after three turns under D-000 clause 2. Not adopted. No forced consensus. Parked. Successor drafts are D-025–D-031, a **new** cycle, not a fourth turn of this one.` | `## D-037 — Consume file 11 via D-001 routes` (line 1689) | Line 1704–1706: `- **Supersedes:** CONTESTED D-017 and the unadopted D-025 draft only. D-025 has no register entry and is not CONTESTED. D-028, D-029, and D-030 from that cycle are ADOPTED and are not superseded.` | **No.** COORD hits outside the entry: lines 1419–1423 (D-018's Status cites the turn-2 reviews of "the D-017/D-018 cycle" — history). Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: `doctor-contract.v3.review-independent.json` (sha256 `1316a1ed…`) line 311, an untracked-files inventory naming "decision drafts and adversarial reviews (D-017 through D-033 …)" — history. |
| 2 | D-019 (same heading; draft line 99: `## D-019 — Select Route B for DR-002 (preview scope)`) | as row 1 | `## D-047 — Select Route B for DR-002 (preview scope)` (line 2230): `Select Route B for DR-002, architecture preview only.` | Chain: `coordinator-decisions.D-025-031.turn3.draft.md` (sha256 `791421b46d843334e289233bca8912dc59d136f4528397657cf6d301eae5807a`) line 127/130: `## D-026 — Select Route B for DR-002 (preview scope)` / `- **Supersedes:** CONTESTED D-019 draft only. Adopting or overturning this entry does not change D-020–D-024.` D-026 never became a COORD heading; D-047 (ADOPTED 2026-08-14, turn 2 of 3 dual CONSENT 0/0) is the entry that decided the identical subject. **D-047 does not name D-019 or D-026** (grep of the entry and of `coordinator-decisions.D-047-048*.draft.md`: 0 hits) — supersession is by subject identity, not by an explicit sentence. | **No.** COORD line 1455 (D-018): `Route selection is D-019 and D-020, if adopted.` — conditional, historical. Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 3 | D-020 (draft line 131: `## D-020 — Select Route B for DR-004 (preview scope)`) | as row 1 | `## D-048 — Select Route B for DR-004 (preview scope)` (line 2265): `Select Route B for DR-004, architecture preview only.` | Chain: D-025-031.turn3.draft.md line 195/198: `## D-027 — Select Route B for DR-004 (preview scope)` / `- **Supersedes:** CONTESTED D-020 draft only. …` D-027 never became a COORD heading; D-048 decided the identical subject. D-048 does not name D-020 or D-027 (0 hits). | **No.** COORD line 1455 as row 2. Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 4 | D-021 (draft line 149: `## D-021 — Select Route B for DR-005 (preview scope)`) | as row 1 | `## D-028 — Select Route B for DR-005 (preview scope)` (line 1528): `Select Route B for DR-005, architecture preview only.` | D-025-031.turn3.draft.md line 254/257: `## D-028 — Select Route B for DR-005 (preview scope)` / `- **Supersedes:** CONTESTED D-021 draft only.` D-037 line 1705: `D-028, D-029, and D-030 from that cycle are ADOPTED and are not superseded.` | **No.** COORD lines containing `D-021`: 0. Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 5 | D-022 (draft line 173: `## D-022 — Select Route B for DR-008's integration half (preview scope)`) | as row 1 | `## D-029 — Select Route B for DR-008's integration half (preview scope)` (line 1559): `Select Route B for that half, preview only.` | D-025-031.turn3.draft.md line 313/316: `## D-029 — …` / `- **Supersedes:** CONTESTED D-022 draft only.` | **No.** COORD hits only inside the D-017 entry (lines 1505, 1511). Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 6 | D-023 (draft line 193: `## D-023 — Select Route B for a scoped preview threat model under DR-003`) | as row 1 | `## D-030 — Select Route B for a scoped preview threat model under DR-003` (line 1582): `Select Route B for a scoped preview TM covering every boundary D-002 ships …` | D-025-031.turn3.draft.md line 380/383: `## D-030 — …` / `- **Supersedes:** CONTESTED D-023 draft only.` | **No.** COORD hit only inside the D-017 entry (line 1510). Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 7 | D-024 (draft line 242: `## D-024 — Coordinator execution sequence: two lanes`) | as row 1 | `## D-036 — Coordinator execution sequence (partial order)` (line 1656): `Two lanes. Lane R = condition-1 Route A work, starts now …` | `coordinator-decisions.D-036.turn3.draft.md` (sha256 `f278394544d6a1eb0d553f21109813650198555cb5ef2d14965ac387d0d0c136`) line 8: `> **Supersedes:** CONTESTED D-031 / D-024 only.` (D-031 is the D-025-031 draft's successor to D-024, line 452/457: `## D-031 — Coordinator execution sequence: two lanes` / `- **Supersedes:** CONTESTED D-024 draft only.`) **Wording flag:** the frozen D-036 draft calls D-031 "CONTESTED", but D-031 has no COORD heading and COORD never applies the word to it (D-037 line 1705 applies the same reasoning to D-025: `has no register entry and is not CONTESTED`). This inconsistency lives in a frozen artifact, not in COORD. | **No.** COORD hits only inside the D-017 entry (lines 1510, 1519). Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 8 | `## D-051 / D-052 / D-053 — Select Route B for DR-006, DR-007, DR-009 (CONTESTED)` (line 2640; commit `11a4e69 D-051/D-052/D-053: CONTESTED after three turns`) | Lines 2658–2659: `- **Decision:** None. Route B is not selected for DR-006, DR-007, or DR-009. A later new cycle (not turn 4) may retry.` | `## D-069 — Select Route B for DR-006 (preview scope)` (line 2791); `## D-071 — Select Route B for DR-007 (preview scope)` (line 2833); `## D-072 — Select Route B for DR-009 (preview scope)` (line 2870). Each `ADOPTED 2026-08-14. Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` | D-069 Decision: `Select Route B for DR-006, architecture preview only.` D-071: `Select Route B for DR-007, architecture preview only.` D-072: `Select Route B for DR-009, architecture preview only.` None of the three COORD entries names D-051/052/053 (grep: 0). The explicit retargeting sentence lives in the recorded dispositions: `route-b.DR-006.preview-disposition.v2.json` (sha256 `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161`) line 103 `"predecessorChange": "Retargets selection authority from CONTESTED D-051 to new-cycle D-069. …"`; `route-b.DR-007.preview-disposition.v2.json` (sha256 `53b72a91…`) line 78 `"Retargets selection authority from CONTESTED D-052 to new-cycle D-071. …"`; `route-b.DR-009.preview-disposition.v2.json` (sha256 `5e2f6572…`) line 69 `"Retargets selection authority from CONTESTED D-053 to new-cycle D-072. …"`. Those v2 files are the dispositions recorded at D-074/D-075/D-076 and owner-recorded at D-077/D-078/D-079 (each entry cites `route-b.DR-00N.preview-disposition.v2.json`). | **No dependency; historical citations only.** The three currently recorded disposition artifacts name D-051/D-052/D-053 only to say authority was *retargeted away from* them to D-069/D-071/D-072. Their v1 predecessors also name them (superseded by v2). The six independent reviews of those v2 dispositions (tracked in git; not own-cycle files) name them in the same retargeting sense: `route-b.DR-006.preview-disposition.v2.review-independent.claude2.json` (sha256 `d1f309203ecee7a1c8aee9f0d1090e2885cc9e3feb4a0ad7d90dfe9046c9d1ab`) line 31 `predecessorChange honestly scopes the delta: 'Retargets selection authority from CONTESTED D-051 to new-cycle D-069.`; `…DR-006…codex.json` (`821ce53f9b42ec98fb707dc5388864261782ac11e321ff81b40c431376349fc1`) line 29 `The v1-to-v2 delta retargets selection authority from unadopted D-051 to adopted D-069, …`; `…DR-007…claude2.json` (`aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b`) line 32 `'Retargets selection authority from CONTESTED D-052 to new-cycle D-071.`; `…DR-007…codex.json` (`807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55`) line 29 `retargets selection authority from unadopted D-052 to adopted D-071`; `…DR-009…claude2.json` (`b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459`) line 43 `'Retargets selection authority from CONTESTED D-053 to new-cycle D-072.`; `…DR-009…codex.json` (`2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f`) line 29 `retargets selection authority from unadopted D-053 to adopted D-072`. No other artifact outside `coordinator-decisions.*`/`_dispatch.*` names them. COORD: no hits outside the entry. |
| 9 | `## D-059 — Owner-record DR-004 (CONTESTED)` (line 2469; commit `624e2e3 D-059: CONTESTED after three turns — DR-004 owner-record`) | Lines 2486–2487: `- **Decision:** None. DR-004 is not owner-recorded. A later new cycle (not turn 4 of this cycle) may retry.` | `## D-064 — Owner-record the DR-004 preview Route B disposition` (line 2495), `ADOPTED 2026-08-14. Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` | Line 2507: `New cycle after CONTESTED D-059. Not a fourth turn.` | **No.** COORD: no hits outside the entry and D-064's line 2507. Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 10 | `## D-067 — File 08 MF-6 notes for preview owner recordings (CONTESTED)` (line 2733; commit `d2dc671 D-067: CONTESTED after three turns`) | Lines 2750–2751: `- **Decision:** None. File 08 is not edited. A later new cycle (not turn 4) may retry.` | `## D-070 — File 08 MF-6 notes for preview owner recordings` (line 2758) — identical title without the suffix; `ADOPTED 2026-08-14. Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` | D-070 Decision (lines 2773–2775): `Append the exact six scoped owner-recording notes authorized by the subject to DR-002, DR-003, DR-004, DR-005, DR-008, and DR-010.` D-070 does not name D-067 (grep: 0); supersession is by identical subject and title. | **No.** COORD: no hits outside the entry. Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: none. |
| 11 | `## D-094 — D-006 fleet-class successor plus G03/G04 named identifiers (CONTESTED)` (line 3738; commit `4172141 D-094: CONTESTED — G03/G04 fleet-class naming parked`) | Lines 3762–3764: `- **Decision:** None. File 08 is not edited. G03/G04 stay reserved. Condition 4 stays 16 of 18 and PARTLY MET. A later new cycle (not turn 4) may retry.` | `## D-102 — D-006 fleet-class successor plus G03/G04 named identifiers` (line 3963), `ADOPTED 2026-08-14. Turn 2 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` Decision: `Adopt the hosted-fleet-class measurement contract. Write G03/G04 reserved identifiers into file 08 as named. … Condition 4 becomes 18 of 18 named required gates, standing **MET**.` | Direct: D-096 line 3830 `Does not retry D-094.` and lines 3835–3836 `Does not overturn D-002, D-054, D-057, D-093, D-094, or D-095.` Chain to the resolver: D-094 → D-098 → D-099 → D-101 (all four CONTESTED, identical titles) → D-102 line 3977 `New cycle after D-101 CONTESTED.` and line 3993 `Does not overturn D-101 CONTESTED.` **D-098 does not name D-094; D-099 does not name D-098; D-101 does not name D-099** (grep: 0 each) — the chain is by identical heading title. | **No.** Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: `platform-tcb-contract.v1.review-independent.claude2.json` (sha256 `2dd94367…`) line 79: `given this corpus has repeatedly parked harness naming as CONTESTED (D-094, D-098, D-099, D-101). REFUTED decisively.` — a reviewer's historical remark. |
| 12 | `## D-095 — Record the five preview-deferral v2 candidates (CONTESTED)` (line 3772; commit `fdb1955 D-095: CONTESTED — deferral-candidate recording parked`) | Lines 3793–3795: `- **Decision:** None. File 08 is not edited. The five v2 candidates remain independently ACCEPTED and unrecorded. A later new cycle (not turn 4) may retry.` | `## D-096 — Record the five preview-deferral v2 candidates` (line 3802), `ADOPTED 2026-08-14. Turn 1 of 3: CONSENT from both independent reviewers, 0 MUST-FIX, 0 SHOULD-FIX.` | Line 3814: `New cycle after D-095 CONTESTED. ADV-D095-T3-01 accepted.` | **Not a dependency, but one citation of the D-095 cycle as "corpus law":** `platform-tcb-contract.v3.review-independent.claude2.json` (sha256 `2345e746…`) line 49: `The standing rule from the D-095 cycle is explicit and was the required repair there: 'grant AND mechanics; mechanics never grants'` and line 166: `D-095 records the standing repair 'grant and mechanics; mechanics never grants'`. The rule itself is carried by ADOPTED D-096 (`A mechanics entry alone never grants.`, line 3827), so the citation resolves to an adopted entry's content; the reviewer's choice to cite D-095 rather than D-096 is a wording matter in a frozen review. |
| 13 | `## D-098 — D-006 fleet-class successor plus G03/G04 named identifiers (CONTESTED)` (line 3870; commit `09d0e28 D-098: CONTESTED — G03/G04 fleet-class naming parked`) | Lines 3893–3894: `- **Decision:** None. File 08 is not edited. A later new cycle (not turn 4) may retry.` | D-102 (row 11) | Chain only (row 11). D-102 names D-101, not D-098. | **No.** Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: only the row-11 historical remark. |
| 14 | `## D-099 — D-006 fleet-class successor plus G03/G04 named identifiers (CONTESTED)` (line 3901; commit `90c80fc D-099: CONTESTED — G03/G04 fleet-class naming parked`) | Lines 3924–3925: `- **Decision:** None. File 08 is not edited. A later new cycle (not turn 4) may retry.` | D-102 (row 11) | Chain only (row 11). | **No.** Artifacts outside `coordinator-decisions.*`/`_dispatch.*`: only the row-11 historical remark. |
| 15 | `## D-101 — D-006 fleet-class successor plus G03/G04 named identifiers (CONTESTED)` (line 3932; commit `c159c22 D-101: CONTESTED — G03/G04 fleet-class naming parked`) | Lines 3955–3956: `- **Decision:** None. File 08 is not edited. A later new cycle (not turn 4) may retry.` | D-102 (row 11) | Line 3977: `New cycle after D-101 CONTESTED.` Line 3993 (D-102 Reversibility): `Does not overturn D-101 CONTESTED.` | **No.** COORD line 4590 (D-114): `This is coordinator decision D-114, not register row DR-114 and not the contested C4 decision D-101.` — a disambiguation. Artifacts (strict grep, outside `coordinator-decisions.*`/`_dispatch.*`): only the row-11 historical remark. The 184-file count a naive `D-101` grep returns is `OD-101-1`/`OD-101-2` noise (DR-101's open decisions), not references to this entry. |

Summary of the last column: for all 17 ids, **no recorded artifact, no ADOPTED COORD entry, and no file-08 cell derives authority from a CONTESTED entry.** Every surviving cross-reference is (i) a "new cycle after / does not overturn / does not retry" recital in the successor, (ii) a retargeting sentence in a recorded disposition (or in an independent review of that disposition) saying authority moved away from the CONTESTED entry, (iii) a historical remark in a frozen review, or (iv) a precedent or recital mention inside another cycle's `coordinator-decisions.*` file (A2.1).

### A2.3 Options

**(i) Confirm all nine headings stay CONTESTED-parked as history; no COORD change.**
- What changes in COORD: nothing.
- Consequences: the confirmation exists only in the owner's reply and in this packet. The nine headings keep the `(CONTESTED)` suffix, which the status vocabulary defines as `parked for the user`; after confirmation they are parked *by* the user, but the register does not say so. Readiness effect: zero.

**(ii) Record the confirmation as one COORD entry** (draft in Appendix 1; user-made on the D-054 model, or coordinator-drafted and D-000-reviewed on the D-073/D-097 model).
- What changes in COORD: one new heading (278 if adopted alone; if combined with A1 option (b1) the same single heading carries both rulings). The nine CONTESTED entries' bytes stay unchanged. No relabelling to `SUPERSEDED` (never used on a heading; would stale the successors' "CONTESTED D-0NN" recitals).
- Consequences: the register records that the user has reviewed the parked contests and closes the "batched to the user" limb of clause 2 for them. Readiness effect: zero.

**(iii) Reopen a named entry.** For each, what reopening would collide with:
- D-017 / D-019–D-024: would require overturning D-037 (`Overturn: C-D037`), D-047, D-048, D-028, D-029, D-030, D-036 and — because those selections carry owner-recorded dispositions (D-058, D-064, D-060, D-065, D-061) — the successions those dispositions name (D-047/D-048 Reversibility: `After one lands, overturn also requires that disposition's owning-authority supersession.`).
- D-051/052/053: would require overturning D-069/D-071/D-072 and the dispositions D-074–D-079 that retarget authority to them.
- D-059: would require overturning D-064.
- D-067: would require overturning D-070, whose file-08 edits (six notes, condition-1 "Measured now" cell) would need restoring (`C-D070 plus restore of the prior file-08 cells and prior snapshot preamble.`).
- D-094 / D-098 / D-099 / D-101: would require overturning D-102 (`C-D102 plus restore of the two reserved cells, 16-of-18 fragment, PARTLY MET, one-sentence clause, …`) and would un-name G03/G04: condition 4 is currently `28 of 28` MET on the naming half (D-292; file 08 line 417), D-102's Reversibility recipe restores its own era's `16-of-18 fragment, PARTLY MET`, and the count that would result today is not in the record.
- D-095: would require overturning D-096.
Each reopening is a new D-000 cycle; the record contains no reason to reopen any of them (every subject has an ADOPTED resolver and zero live dependents).

**Orchestrator recommendation (A2):** (i), or (ii) folded into the same single entry as A1 if the owner chooses A1 (b1)/(c1). Reopen none.

---

## Appendix 1 — DRAFT COORD confirmation entry (NOT dispatched; NOT written to COORD)

Marked DRAFT. Modelled on `## D-054 — User amendment: preview-scope owner recording` (user-made, recorded verbatim, no review). The decision id is a placeholder because the next free id is not in the record (last heading D-292). Bracketed items are for the owner to fill or strike; everything else quotes or restates record bytes. If the owner prefers the D-000-reviewed form, the same text minus the "Made directly by the user" sentence and the verbatim-words field becomes a coordinator draft for dual review.

```
## D-2NN — User ruling: D-272 fourth exchange and the parked CONTESTED entries

- **Date:** 2026-08-2N
- **Status:** **ADOPTED 2026-08-2N.** Made directly by the user in
  conversation. Same class as D-000 and D-054: the ruling is the
  user's decision, recorded verbatim rather than made on their
  behalf. No adversarial review.
- **Decision type:** RULE-GOVERNED user ruling under D-000 clause 2
  ("batched to the user"). Not PREFERENCE-LADEN: it sets no product
  value.
- **User words, recorded verbatim (this session, 2026-08-2N):**
  1. "[owner's words for A1]"
  2. "[owner's words for A2]"
- **Subject:** the ten COORD headings whose title ends in
  `(CONTESTED)` at HEAD `4abb961`: D-017 / D-019–D-024 (line 1490),
  D-059 (2469), D-051 / D-052 / D-053 (2640), D-067 (2733), D-094
  (3738), D-095 (3772), D-098 (3870), D-099 (3901), D-101 (3932),
  D-272 (13963).
- **Ruling 1 (D-272):** The fourth exchange dispatched as
  `coordinator-decisions.D-272.turn4.draft.md`
  `802ca3ec7efcb11c90475dfadd6230778b362daa8d94da68d9e1bec5e6a6c665`
  was outside D-000 clause 2, which terminates a cycle after three
  exchanges per party. Both Stage B reviewers so found (Claude
  `4110cae842bac61d00448655e7f04fbfc2eb63c48fd2c73290bd9fb305795899`
  MF-1; Codex
  `982397057a394642bc7391df5951eb8839c57230359ac92e11750e771778509e`
  CODEX-D272-T4-MF1). D-272 remains CONTESTED. Its terminal merits
  review is turn 3 Dual OBJECT, as its Status field records. D-273
  (ADOPTED 2026-08-24, turn 1 of 3, dual CONSENT 0/0) is the lawful
  new cycle and stands. [Optional, only if the owner chooses A1 (c1):
  D-000 clause 2 is amended to add: "No fourth exchange is dispatched
  in a cycle. A re-dispatch of turn 3 is permitted only on the D-093
  ground (the prior turn-3 verdicts were freeze-precondition OBJECTs,
  not merits reviews) and is labelled 'turn 3 of 3, re-dispatched'."]
- **Ruling 2 (parked contests):** The nine CONTESTED headings D-017 /
  D-019–D-024, D-051 / D-052 / D-053, D-059, D-067, D-094, D-095,
  D-098, D-099, and D-101 stay CONTESTED and parked as history. None
  is reopened. Each subject was resolved by an ADOPTED successor:
  D-017 by D-037; D-019 by D-047; D-020 by D-048; D-021 by D-028;
  D-022 by D-029; D-023 by D-030; D-024 by D-036; D-051 / D-052 /
  D-053 by D-069 / D-071 / D-072; D-059 by D-064; D-067 by D-070;
  D-094, D-098, D-099, and D-101 by D-102; D-095 by D-096. No
  recorded artifact, ADOPTED entry, or file-08 cell derives
  authority from a CONTESTED entry. [Strike any id the owner instead
  reopens, and name the reopening cycle.]
- **What this entry does not do:** Does not relabel any heading
  SUPERSEDED or OVERTURNED. Does not edit the bytes of D-272, D-273,
  or any CONTESTED entry. Does not edit file 08. Does not mark any
  row SATISFIED. Does not open Gate 1 Class A. Does not authorize
  `docs/v2/implementation/`.
- **Readiness effect:** Zero SATISFIED. Condition 2 stays 5 of 32.
  Condition 4 stays MET on the naming half (28 of 28). Condition 5
  last.
- **Reversibility:** the user may revise this ruling in any later
  message. Overturn: C-D2NN. Does not unwrite D-037, D-047, D-048,
  D-028, D-029, D-030, D-036, D-064, D-069, D-070, D-071, D-072,
  D-096, D-102, or D-273.
- **Commit:** C-D2NN.
```

---

## Appendix 2 — Citations relied on (path + heading/field/line; sha256 for artifacts)

COORD `docs/coop/COORDINATOR-DECISIONS.md` (sha256 `47f7b2011ec719dfadcbccb553a142eb0808e3099f20bf544b4564ab18e28466`): lines 14–16 (status vocabulary); `## D-000` Decision item 2 (lines 32–36) and Reversibility; `## D-017 / D-019–D-024` (1490–1524); `## D-018` line 1419–1423 and 1455; `## D-028` (1528), `## D-029` (1559), `## D-030` (1582), `## D-036` (1656), `## D-037` (1689; Supersedes lines 1704–1706); `## D-047` (2230), `## D-048` (2265); `## D-054` (2361); `## D-059` (2469–2492); `## D-064` (2495; line 2507); `## D-051 / D-052 / D-053` (2640–2665); `## D-067` (2733–2756); `## D-070` (2758); `## D-069` (2791), `## D-071` (2833), `## D-072` (2870); `## D-073` (2903); `## D-074`–`## D-079` (2933–3162, disposition version citations); `## D-093` Status (3695–3698); `## D-094` (3738–3770); `## D-095` (3772–3800); `## D-096` (3802; lines 3814, 3827, 3830, 3836); `## D-097` (3841); `## D-098` (3870–3899); `## D-099` (3901–3930); `## D-101` (3932–3961); `## D-102` (3963; lines 3977, 3993); `## D-114` line 4590; `## D-272` (13963–14046); `## D-273` (14047–14131); `## D-274` (14132); `## D-292` (16035, tail).

File 08 `docs/v2/architecture/08-decision-and-readiness-register.md` (sha256 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`): grep for every id in this packet — 0 hits.

Artifacts (`docs/coop/artifacts/`):
- `coordinator-decisions.D-272.turn4.review-adversarial.claude2.json` `4110cae842bac61d00448655e7f04fbfc2eb63c48fd2c73290bd9fb305795899` — fields `stage`, `mustFix[0].{title,where,measurement,why,remedy}`, `summary`, `verdictFinal`.
- `coordinator-decisions.D-272.turn4.review-adversarial.codex.json` `982397057a394642bc7391df5951eb8839c57230359ac92e11750e771778509e` — fields `d000TerminationAudit.subjectProtocolText`, `findings[0].{title,charge,evidence[2],repair}`, `summary`, `verdictFinal`, `mustFix`, `shouldFix`.
- `coordinator-decisions.D-272.turn4.draft.md` `802ca3ec7efcb11c90475dfadd6230778b362daa8d94da68d9e1bec5e6a6c665` — line 5.
- `coordinator-decisions.D-272.turn4.review-prompt.md` `26de7746f874c781398628e0b95a6bfb391c1243a2b31791be96a6272967e06f` — line 1.
- `_dispatch.D-272-t4.txt` (tracked, commit `078b3d6`) `dc51fbf00422a81460b814108166f9a86459e689efb537614f925ec89923aff9` — lines 1, 13–14.
- `coordinator-decisions.D-272.review-adversarial.claude2.json` `7abe9076…`, `…codex.json` `c1706699…`, `…turn2…claude2.json` `6336fe44…`, `…turn2…codex.json` `3932afc9…`, `…turn3…claude2.json` `7638af9e…`, `…turn3…codex.json` `032b5907…` — `verdictFinal` and MUST-FIX/SHOULD-FIX counts (re-measured; match the D-272 Status field).
- `coordinator-decisions.D-272.turn1.draft.md` `aa66e2cc…`, `coordinator-decisions.D-272.draft.md` `14cc56ad…`, `coordinator-decisions.D-272.turn3.draft.md` `c7d0ec6b…` — digests re-measured; match the D-272 Subject-drafts field.
- `coordinator-decisions.D-273.draft.md` `6a134f700b2316ebf7fa85dbc8237f6cf87d95bdfc686bd8edc7749236422218` — lines 5–6.
- `coordinator-decisions.D-273.review-adversarial.claude2.json` `b6a6d2d7fb714e7a2fbcdb7738127207100088866d178ca6c27abd76275da3a5` — `stage`, `counts`, `verdictFinal`, `attackResults[41]`, `attackResults[42]`, `templateConformanceAudit.removalsAreCycleScoped`.
- `coordinator-decisions.D-273.review-adversarial.codex.json` `b201f62dbdb68c3ea9d93544fb6a22dc4df606328acc6cf149f16801580d2a57` — `verdictFinal`, `mustFixCount`, `shouldFixCount`, `attackResults[5]`, `newCycleAudit.{result,d272SuccessorPermission,predecessorLedgerCustody}`, `summary`.
- `language-quality-leftover-join.v5.json` `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53` — digest only.
- `language-runtime-leftover-join.v6.review-independent.claude2.json` `5b1e5b39f066d3be742cf8d3711518106cc70d9fff933dcc939f925c1b0b9081` — lines 123–124.
- `coordinator-decisions.D-017-024.turn3.draft.md` `4cffad69a8fc41af42086378ad01e071ad903822a1bd0ed1168341b80cecc5a5` — headings at lines 81, 99, 131, 149, 173, 193, 242.
- `coordinator-decisions.D-025-031.turn3.draft.md` `791421b46d843334e289233bca8912dc59d136f4528397657cf6d301eae5807a` — headings/Supersedes at lines 53/56, 127/130, 195/198, 254/257, 313/316, 380/383, 452/457.
- `coordinator-decisions.D-036.turn3.draft.md` `f278394544d6a1eb0d553f21109813650198555cb5ef2d14965ac387d0d0c136` — line 8.
- `coordinator-decisions.D-047-048.draft.md` and `coordinator-decisions.D-047-048.turn2.draft.md` — grep for D-019/D-020/D-026/D-027: 0 hits (digests not needed for a null result).
- `route-b.DR-006.preview-disposition.v2.json` `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161` — line 103 `predecessorChange`.
- `route-b.DR-007.preview-disposition.v2.json` `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7` — line 78 `predecessorChange`.
- `route-b.DR-009.preview-disposition.v2.json` `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782` — line 69 `predecessorChange`.
- `route-b.DR-006.preview-disposition.v2.review-independent.claude2.json` `d1f309203ecee7a1c8aee9f0d1090e2885cc9e3feb4a0ad7d90dfe9046c9d1ab` — line 31; `…codex.json` `821ce53f9b42ec98fb707dc5388864261782ac11e321ff81b40c431376349fc1` — line 29.
- `route-b.DR-007.preview-disposition.v2.review-independent.claude2.json` `aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b` — line 32; `…codex.json` `807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55` — line 29.
- `route-b.DR-009.preview-disposition.v2.review-independent.claude2.json` `b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459` — line 43; `…codex.json` `2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f` — line 29.
- Other cycles' `coordinator-decisions.*` files naming A2 ids (excluded from the A2.2 last column by the stated method; examples): `coordinator-decisions.D-273.review-adversarial.claude2.json` line 183 (`precedentForNewCycleAfterContested`); `coordinator-decisions.D-272.turn4.review-adversarial.claude2.json` line 91.
- `platform-tcb-contract.v1.review-independent.claude2.json` `2dd943671e69bf19482c29014140891ffee6225d1b609b69b1d91def4f2c9803` — line 79.
- `platform-tcb-contract.v3.review-independent.claude2.json` `2345e746e03c6fb1a12abad930c4d62794c794fa122acdd954a5e8b94d3596b7` — lines 49, 166.
- `doctor-contract.v3.review-independent.json` `1316a1ed03abcde8e5094e3e9952f5100e1133fd64f227bf3b3bab5d25e1540b` — line 311.

Git: `git rev-parse HEAD`; `git log --oneline` entries `c04ad23`, `bc3dc87`, `b82d75f`, `11a4e69`, `624e2e3`, `d2dc671`, `4172141`, `fdb1955`, `09d0e28`, `90c80fc`, `c159c22`; `git show --stat c04ad23` (25 files), `git show --stat bc3dc87` (5 files); `git ls-files docs/coop/artifacts/ | grep D-272.turn4` (4 files tracked).

Framing: `DECISIONS-NEEDED.md` (as rewritten 2026-08-27, mtime 22:00:01) lines 3, 11–17 ("breach" at lines 12 and 14); `STATUS.2026-08-26.md` lines 1, 28, 61, 71.

## Appendix 3 — Open questions not resolvable from bytes

1. **Who dispatched D-272 turn 4.** COORD, the dispatch file, and the review prompt do not name the dispatching orchestrator. `STATUS.2026-08-26.md` line 1 places the Claude orchestrator's start "after D-281"; the record does not name who held the role on 2026-08-24.
2. **The next free decision id** for any confirmation entry: last heading is D-292; the id to use is the owner's/orchestrator's choice at recording time and is written as a placeholder in Appendix 1.
3. **Whether the owner regards D-272's Status-field sentence** ("That exchange is not D-000 consensus and is not this cycle's terminal merits review") **as a sufficient acknowledgement.** The bytes record the reviewers' finding; they do not record an acknowledgement of fault by the dispatcher. Whether one is wanted is a preference, not a fact in the record.
4. **The frozen D-036 draft's phrase "CONTESTED D-031"** (Appendix table row 7) conflicts with COORD's treatment of unadopted draft ids (D-037 line 1705). Whether that wording in a frozen, already-reviewed artifact warrants any hygiene act is not determined by the record; it has no live dependents.

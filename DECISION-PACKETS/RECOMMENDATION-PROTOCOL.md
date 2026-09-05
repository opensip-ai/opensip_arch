# Recommendation protocol (Claude orchestrator + Codex), 2026-08-27

Purpose: for every item in DECISIONS-NEEDED.md, present the human owner one *agreed* recommendation, or — where
the two reviewers cannot agree within three rounds — both positions side by side. Nothing here decides anything;
the owner decides.

Inputs per item: the byte-cited packet `DECISION-PACKETS/<item>.md` (adversarially verified) and
`DECISIONS-NEEDED.md`.

Round 1
- Claude writes `DECISION-PACKETS/<item>.claude-recommendation.md`: recommendation, rationale (each factual
  claim cites the packet section or a file/field), risks, what changes in file 08 / COORD if adopted, confidence.
- Codex, independently and adversarially, writes `DECISION-PACKETS/<item>.codex-recommendation.json` with:
  `{"item","verdict":"AGREE|DISAGREE|AGREE-WITH-AMENDMENT","recommendation","rationale","refutations":[...],
  "amendments":[...],"confidence":"low|medium|high"}`. Codex must re-check any packet claim its rationale relies
  on against the bytes and must try to refute Claude's rationale before agreeing.

Rounds 2–3 (only on DISAGREE or AGREE-WITH-AMENDMENT): Claude answers each refutation/amendment in
`<item>.claude-recommendation.r2.md` (adopting Codex's position where it is better, saying so explicitly);
Codex replies in `<item>.codex-recommendation.r2.json`; likewise r3. No fourth round.

Output: `DECISIONS-RECOMMENDED.md` (repo root) — one section per item: AGREED recommendation (or SPLIT with both
positions), the joint rationale, evidence pointers, and what happens next if the owner accepts.

Rules: no invented identifiers, numbers, lists, verdicts, or fixture bytes; no edits under docs/; no readiness
claims; recommendations may be "defer with an explicit disposition" where the record allows it.

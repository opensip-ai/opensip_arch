# Adversarial review — D-099 turn 3

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-099.turn3.draft.md`
Measure sha256 yourself at start and end.
Expected digest at dispatch:
`3249a26c738c35cbd20f31ebe442559fc027acc764a610cb4dc93eac3b4ee47a`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-099.review-adversarial.claude2.turn3.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-099.review-adversarial.codex.turn3.json`

Do not read the other reviewer's files. Do not edit any other file. Do not commit.

This subject is FROZEN. If it moves, OBJECT.
Turn 3 of 3. Frozen turn-1 and turn-2 subjects must not be edited.

D099-T2-MF-1 and ADV-D099-T2-02 accepted: pin table is
this cycle only; each label unique.
ADV-D099-T2-01 accepted: dedicated stopped-after-exec
preflight; Linux process ABI is auxv AT_PLATFORM; macOS
translation is T's kinfo_proc P_TRANSLATED after exec.

Attack:
- D099-T2-MF-1 not landed (duplicate or foreign pin rows)
- ADV-D099-T2-01 not landed (no exec-stop handshake; file
  of exe counted as process ABI; parent sysctl.proc_translated
  or pre-exec helper used as T's translation)
- process arch still observes the inspector (`/proc/self/exe`)
  or a fat slice
- weekly roll disables 10%
- warm p50 is a fail gate
- changes D-006 numerals
- claims QUALIFIED or SATISFIED
- authorizes docs/v2/implementation/ or flips condition 5
- cited digests mismatch
- subject or prompt moved
- turn-1 or turn-2 subject edited

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: short summary plus verdict word.

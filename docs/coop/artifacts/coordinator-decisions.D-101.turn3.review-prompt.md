# Adversarial review — D-101 turn 3

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-101.turn3.draft.md`
Measure sha256 yourself at start and end.
Expected digest at dispatch:
`ba5f8fc8ae336de0073642fd6e3ac2bc549988256b20068e2864df3ff1e66eae`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.claude2.turn3.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.codex.turn3.json`

Do not read the other reviewer's files. Do not edit any other file. Do not commit.

This subject is FROZEN. If it moves, OBJECT.
Turn 3 of 3. Frozen turn-1 and turn-2 subjects must not
be edited. Frozen D-099 subjects must not be edited.

D101-T2-MF-1 / ADV-D101-T2-01 accepted: no full-file
hash between purge and cold exec. Hash before purge and
after the pair. `stat` only immediately before cold.
D101-T2-SF-1 accepted: same split check on Linux and
macOS. ISA remains the derivation, not sysctl.proc_cputype.

Attack:
- still hashes P between purge and cold
- still treats sysctl.proc_cputype as process arch
- process arch still observes the inspector or a fat slice
- AT_PLATFORM compared as a raw pointer or via parent getauxval
- weekly roll disables 10%
- warm p50 is a fail gate
- changes D-006 numerals
- claims QUALIFIED or SATISFIED
- authorizes docs/v2/implementation/ or flips condition 5
- fourth turn of D-099
- cited digests mismatch
- subject or prompt moved
- turn-1, turn-2, or D-099 subjects edited

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: short summary plus verdict word.

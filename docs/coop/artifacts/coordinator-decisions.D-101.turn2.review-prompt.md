# Adversarial review — D-101 turn 2

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-101.turn2.draft.md`
Measure sha256 yourself at start and end.
Expected digest at dispatch:
`795c34e13e474b5007b33693d8399abb58df3910a79933ab6d927af2d922729b`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.claude2.turn2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.codex.turn2.json`

Do not read the other reviewer's files. Do not edit any other file. Do not commit.

This subject is FROZEN. If it moves, OBJECT.
Turn 2 of 3. Frozen turn-1 subject must not be edited.
Frozen D-099 subjects must not be edited.

D101-T1-MF-1 accepted: `sysctl.proc_cputype`+PID is host
CPU type; macOS 15.4 has no public per-process CPU-type
API; target ISA is the H + E + D + spawn-pref +
P_TRANSLATED=0 derivation.
ADV-D101-T1-01 accepted: path/inode/digest checked before
spawn, after observations, and before each timed launch.
Suspension does not itself detect a path swap.

Attack:
- D101-T1-MF-1 not landed (still treats sysctl.proc_cputype
  as process arch)
- ADV-D101-T1-01 not landed (still claims suspension detects
  a path swap; no re-check before timed launch)
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
- turn-1 or D-099 subjects edited

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: short summary plus verdict word.

# Adversarial review — D-101 turn 1

Independent, refute not confirm. `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/coordinator-decisions.D-101.draft.md`
Measure sha256 yourself at start and end.
Expected digest at dispatch:
`54333f8ec16398e0cd3d3bec15afb0b42c4e4a9740bfe7755e3326d083cd7864`

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.claude2.json`
- Codex: `docs/coop/artifacts/coordinator-decisions.D-101.review-adversarial.codex.json`

Do not read the other reviewer's files. Do not edit any other file. Do not commit.

This subject is FROZEN. If it moves, OBJECT.
New cycle after CONTESTED D-099. Not a fourth turn.
Frozen D-099 subjects must not be edited.

D099-T3-MF-1 / ADV-D099-T3-01 accepted: macOS process
arch is `sysctl.proc_cputype` + PID T. Not kinfo_proc
CPU type. Not PROC_PIDARCHINFO (absent on MacOSX15.4.sdk).
Start identity is PROC_PIDTBSDINFO pbi_start_tvsec/usec,
size-checked and re-read.

Attack:
- still names a kinfo_proc CPU-type member
- uses PROC_PIDARCHINFO / SHORTBSDINFO start-time
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
- D-099 subjects edited

CONSENT only if no MUST-FIX or SHOULD-FIX.
Final chat: short summary plus verdict word.

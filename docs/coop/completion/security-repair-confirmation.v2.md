# Owner-authorized security correction confirmation — failed

Authoritative JSON: `security-repair-confirmation.v2.json`, SHA-256 `01676d23d856f4d5debb07097a0bdaa684739dd992946c15af09ad7cc990423c`.

Frozen dispatch: `security-repair-confirmation-dispatch.v2.md`, SHA-256 `990a62accf5d2b989361531116a2f33911a95499b5ecc2668b3b6a2f30a24c3b`.

**OBJECT — 4 MUST-FIX, 0 SHOULD-FIX. Security remains CONTESTED.** The original failed probes are repaired, including `snapshotMembers=[{}]`; remaining defects violate the recorded systemic validation requirements.

| Finding | Disposition | Remaining evidence |
|---|---|---|
| SEC3-M1 | UNRESOLVED | Wrapper/use-side checks now work; initial root admission still throws NON_NFC_STRING for a malformed label instead of returning a refusal. |
| SEC3-M2 | RESOLVED, preserved | Earlier path-narrowing confirmation retained. |
| SEC3-M3 | UNRESOLVED | Missing hash now quarantines; floating-point witnessSchema 1.0 still returns OK despite strict-type requirements. |
| SEC3-M4 | UNRESOLVED | String pathPrefixes="src" becomes character prefixes and admits s/file.ts; an unknown effectResult member is accepted and bytes returned. |
| SEC3-M5 | UNRESOLVED | Code no longer emits REVERTED, but normative step5 still permits it; stale RCO-only receipt text contradicts derived RCO/ICO identity. Malformed recovery class/footprint raises ValueError. |
| SEC4-REG-M5-OUTCOME | UNRESOLVED within M5 | Executable portion corrected; contradictory normative outcome instruction survives. |
| SEC3-M6 | RESOLVED, preserved | Earlier measured Linux profile/fleet confirmation retained. |

All **332** retained checks pass, with results matching the author report. Independent exact probe source and results are embedded in the JSON; those counterexamples determine this verdict. The exact diff checks: 7 changed files, 1 added, 63 unchanged, 0 removed. All subject pins remain unchanged and read-only.

The exception was verified against the independently reviewed owner decision and its record in commit `5e1160a44d3709185776536e45d6a81df1056fc6`. History remains **three ordinary exchanges, the failed first bounded confirmation, and this failed additional confirmation**. No count reset.

**Terminal disposition:** retain CONTESTED and escalate the exact unresolved decisions to the user under the adopted owner decision item6. This exception permits no further pair-handled confirmation. Other independent work may continue.

M2/M6 dispositions and the separately reviewed policy/cap supplement remain preserved. No register edit, satisfied row, unit adoption, implementation authorization or product qualification follows.

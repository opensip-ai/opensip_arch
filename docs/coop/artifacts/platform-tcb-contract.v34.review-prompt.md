# Independent review — platform-tcb-contract.v34 (DR-126)

Independent, refute not confirm. Did not author v1–v34.
**SUBJECT:** `docs/coop/artifacts/platform-tcb-contract.v34.json`
Expected digest: `6b923e27c41c2e7e3070b17b42cee1fc3ced7b1f25af6da86de8b75e59963e4f`
Predecessor v33 `84c01d003a77d289c7928f10012f73a0f0e7a820d90877967da1b4bb337f84b9`.
Frozen Claude v33 REJECT `fb21624bd6b76d1af54b00b78a1afbb00a3a276671d34d0f0d1253ef27939d13`.
Frozen Codex v33 REJECT `49674565dd19133043aae6073200c5d2d689343d1f56eab82c34f206cddcc32e`.
Do not read the other current v34 reviewer.
**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/platform-tcb-contract.v34.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/platform-tcb-contract.v34.review-independent.codex.json`
Do not edit the subject. Do not commit. Do not mark DR-126 SATISFIED.
Never mint a D-096 (A) grant. Do not edit any frozen v12–v33 verdict (0444 — STOP).
HEAD is `93ceaa6` (D-124 ADOPTED). File 08 means only `docs/v2/architecture/08-decision-and-readiness-register.md` (pin `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3`). COORD live pin `67b8df674e782c705dd254df5926be33f468d3bf7d5f0a3b5fdbfe808b33c40c`. Ignore stale C1/D-100/D-103/D-104-era HEAD (`499c057`, `2327cf8`, `5bb125d`). D-106 draft `a1337c9d` is historical turn-1; adopted D-106 records corpus v6 without SATISFYING DR-103.

**PASS-NO-SCOPE-EFFECT:** Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT and is not a blocker. Predecessor-review replacement is not PASS-NO-SCOPE-EFFECT; pins must reproduce.

Claimed repairs: authenticated Boot#### OptionalData must contain `lockdown=integrity` and `sysctl.kernel.kexec_load_disabled=1` (EFI_LOAD_OPTION parse defined; `/proc/cmdline` and present sysctls must match); signed and unsigned kexec refuse; the three scope enumerations name this; NT-TCB-KEXEC is fail-closed; pre-kernel DIGEST-BOUND class is loader/comparable, not framework. Linux stays in D-002 slice 1. Does not mint a Linux deferral or D-096 (A). Does not add DRTM/IMA as an or-choice.
ACCEPT only at 0 blockers and 0 SHOULD-FIX. Final chat: verdict word.

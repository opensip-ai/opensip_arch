# D-096 — Record the five preview-deferral v2 candidates

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a fourth
> turn of D-095. Frozen D-095 subjects are not edited.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT
> / ACCEPT-WITH-ADVISORIES (0 blockers) of five D-002
> explicit-deferral candidates. Same recording class as
> D-013 / D-035 / D-042 / D-066. Coordinator drafts only.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mark any row `SATISFIED`.
> **Does not** edit file 08.
> **Does not** make the coordinator those owners.
> **Does not** invoke D-054 / D-057 for these rows.
> **Does not** overturn D-002, D-010, D-054, D-057, D-093,
> D-094, or D-095.

D-095 is CONTESTED at `fdb1955c03b96d0388e542ab813c54fc4a3c6221`.
This cycle accepts ADV-D095-T3-01: owner-recording stays
blocked until **both** (A) an applicable owner grant and
(B) separately reviewed condition-2 owner-recording
mechanics exist. A mechanics entry alone never grants.

## Subjects (independent 0-blocker reviews of these exact bytes)

| Artifact | sha256 | Claude 2 | Codex |
|---|---|---|---|
| `deferral.DR-108.preview.v2.json` | `225be4f985889b421b6d3a132c33a8aec924866f54401dd812d9db662fcd9beb` | ACCEPT `d9ea59dc20e03034e27f3274e6c1d7a01ef4de45f7669726ea13a15ae4e61b41` | ACCEPT `b5ba72971ff7e2ccf30d1da63676e38540af6fe7afadbb488d6d7e0379923760` |
| `deferral.DR-110.preview.v2.json` | `b6b678dc18dc0ff506d8a96cbf90246b3e84d99cd2a3387032124a153eb5fc52` | ACCEPT-WITH-ADVISORIES `a07ceb43341e7b3ce968f5169a35264a8e58def65dd4e637a1bb078c9a386d80` | ACCEPT `73c392e73018da06144067471bde9e0c858f0b992871981f3d9db78ac7496759` |
| `deferral.DR-116.preview.v2.json` | `ac8d2d4d414a66ef271042f9e98bcdd7397a08126d2bb011089913c63a628743` | ACCEPT `1f22033012cdedbff53ede54c2575302a2c43da04f4824a54a67e0e83603d709` | ACCEPT `624b80deea1de0a6aef2d99d76460e1c1682420d4e84283123a464c4a1eb13b4` |
| `deferral.DR-106-109-113.preview.v2.json` | `194b01fc6bd9201ebdeee71b83846cff09417d7521464bd81a0fbe2aabf7502c` | ACCEPT `043e6518d7171027bc97f38f5e3bca26ae4add00e6538e04c9887f6829305cc3` | ACCEPT `312cf340c24d95b84ee4704a3345ec6aa41dd6d6ba612e5363de932fc9375e07` |
| `deferral.windows-platform.preview.v2.json` | `e7dd2b718fc6af5e46fc4706bc8b232a63c26beed4db42ec79a395b01af22b20` | ACCEPT `8adbb9689579afb0ebb584a03376527d160c93aad5d31bd8faef16cc77316d36` | ACCEPT `077567f1c38ce19d6756e83c7bb6159973048a8fd707f0fe3cff9d972c0141d8` |

DR-110 advisory DEF110-C2-A1 remains owed as honesty work
on a later applicable owner-recording or a successor. It
is not a blocker.

D-094 is CONTESTED. G03/G04 stay reserved. This entry does
not retry D-094 or D-095.

## Decision

1. Record the five v2 artifacts as the accepted
   architecture-preview explicit-deferral **candidates**.
   This is the coordinator recording only.
2. Each artifact stays `CANDIDATE-NOT-RECORDED`, binds
   NOTHING, remains `DO-NOT-SEAL`.
3. This entry does not make the coordinator those owners.
   D-054 / D-057 do not supply the later owner path.
   Owner-recording of these condition-2 deferrals and the
   Windows platform set remains **blocked until both**
   (A) an applicable owner grant expressly covers every
   named role for the candidate being recorded **and**
   (B) separately D-000-reviewed condition-2
   owner-recording mechanics are adopted. A mechanics
   entry alone never grants authority. If one future
   user amendment is intended to supply both, it must
   expressly contain both the role grant and the
   mechanics. DR-116's Route-C product authority does
   not generalize to the other security / release /
   evidence / platform roles.
4. The named rows stay `OPEN`. Windows is not a file-08
   row and is not SATISFIED as one.
5. Do not edit file 08. Do not change condition-2
   SATISFIED counts. Owner-recording, when later
   authorized under (A) and (B), precedes a **separate**
   later D-000-reviewed MF-6. Neither owner-recording
   nor MF-6 occurs in this entry.
6. Does not authorize `docs/v2/implementation/`.

## Alternatives

- Mark any deferred row SATISFIED. Rejected.
- Edit file 08 here. Rejected.
- Cite D-054 / D-057 as the later owner grant. Rejected:
  ADV-D095-T2-01.
- Let a mechanics entry substitute for a missing grant.
  Rejected: ADV-D095-T3-01; D-057 is mechanics only.
- Generalize DR-116 Route C to the other roles. Rejected:
  ADV-D095-T3-01.
- Retry D-094 or D-095 here. Rejected: parked CONTESTED.
- Authorize implementation. Rejected: condition 5 last.

## Readiness effect

Zero SATISFIED. Condition 2 remains unchanged until an
applicable owner grant **and** mechanics land, an owner
records, **and** a separate later MF-6 writes file 08.
Condition 4 stays 16 of 18 PARTLY MET. Condition 5 last.

## Reversibility

C-D096. Does not overturn D-002, D-054, D-057, D-093,
D-094, or D-095.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `a0ea205c740b7fe85a879efcb57668996873ab6cb398935c4e316c26df32aa09` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-095 commit | `fdb1955c03b96d0388e542ab813c54fc4a3c6221` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

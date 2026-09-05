# D-095 — Record the five preview-deferral v2 candidates

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a SATISFIED
> re-record. Frozen D-094 subjects are not edited.
> **Decision type:** RULE-GOVERNED. Records independent ACCEPT
> / ACCEPT-WITH-ADVISORIES (0 blockers) of five D-002
> explicit-deferral candidates. Same recording class as
> D-013 / D-035 / D-042 / D-066. Coordinator drafts; named
> owners record later.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mark any row `SATISFIED`.
> **Does not** edit file 08.
> **Does not** make the coordinator those owners.
> **Does not** overturn D-002, D-010, D-054, D-093, or D-094.

## Subjects (independent 0-blocker reviews of these exact bytes)

| Artifact | sha256 | Claude 2 | Codex |
|---|---|---|---|
| `deferral.DR-108.preview.v2.json` | `225be4f985889b421b6d3a132c33a8aec924866f54401dd812d9db662fcd9beb` | ACCEPT `d9ea59dc20e03034e27f3274e6c1d7a01ef4de45f7669726ea13a15ae4e61b41` | ACCEPT `b5ba72971ff7e2ccf30d1da63676e38540af6fe7afadbb488d6d7e0379923760` |
| `deferral.DR-110.preview.v2.json` | `b6b678dc18dc0ff506d8a96cbf90246b3e84d99cd2a3387032124a153eb5fc52` | ACCEPT-WITH-ADVISORIES `a07ceb43341e7b3ce968f5169a35264a8e58def65dd4e637a1bb078c9a386d80` | ACCEPT `73c392e73018da06144067471bde9e0c858f0b992871981f3d9db78ac7496759` |
| `deferral.DR-116.preview.v2.json` | `ac8d2d4d414a66ef271042f9e98bcdd7397a08126d2bb011089913c63a628743` | ACCEPT `1f22033012cdedbff53ede54c2575302a2c43da04f4824a54a67e0e83603d709` | ACCEPT `624b80deea1de0a6aef2d99d76460e1c1682420d4e84283123a464c4a1eb13b4` |
| `deferral.DR-106-109-113.preview.v2.json` | `194b01fc6bd9201ebdeee71b83846cff09417d7521464bd81a0fbe2aabf7502c` | ACCEPT `043e6518d7171027bc97f38f5e3bca26ae4add00e6538e04c9887f6829305cc3` | ACCEPT `312cf340c24d95b84ee4704a3345ec6aa41dd6d6ba612e5363de932fc9375e07` |
| `deferral.windows-platform.preview.v2.json` | `e7dd2b718fc6af5e46fc4706bc8b232a63c26beed4db42ec79a395b01af22b20` | ACCEPT `8adbb9689579afb0ebb584a03376527d160c93aad5d31bd8faef16cc77316d36` | ACCEPT `077567f1c38ce19d6756e83c7bb6159973048a8fd707f0fe3cff9d972c0141d8` |

DR-110 advisory DEF110-C2-A1 (re-entry bound when a later
slice ships self-update) remains owed as honesty work on
owner-recording or a successor. It is not a blocker.

## Decision

1. Record the five v2 artifacts as the accepted
   architecture-preview explicit-deferral candidates D-001
   / D-002 require for DR-108, DR-110, DR-116,
   DR-106/109/113 wholly, and the Windows platform set.
2. Each artifact stays `CANDIDATE-NOT-RECORDED`, binds
   NOTHING, remains `DO-NOT-SEAL`.
3. Named owners still record (D-054 / D-057). This entry
   does not make the coordinator those owners.
4. The named rows stay `OPEN`. Windows is not a file-08
   row and is not SATISFIED as one.
5. Do not edit file 08. Do not change condition-2
   SATISFIED counts. Owner-recording plus a later MF-6 is
   the C2 deferral-limb write.
6. Does not authorize `docs/v2/implementation/`.

## Alternatives

- Mark any deferred row SATISFIED. Rejected: D-056
  deferral limb; candidates themselves refuse SATISFIED.
- Edit file 08 in this entry. Rejected: D-042 class;
  owner-recording is the MF-6 act.
- Pretend the coordinator is the named owner. Rejected:
  D-000 / D-054 / D-057.
- Leave accepted candidates unrecorded. Rejected:
  D-013/D-035/D-042/D-066 class.
- Quote truncated verdict digests. Rejected: D091-SF-2
  class.
- Authorize implementation. Rejected: condition 5 last.

## Readiness effect

Zero SATISFIED. Condition 2 standing unchanged until
owner-recorded MF-6. Condition 5 remains last.

## Reversibility

C-D095. Does not overturn D-002 or D-093.

## Measured inputs at dispatch

| Path | sha256 |
|---|---|
| COORD | `4ec069882b41ab5e14668e86cfac8dd977ac850c495c9f4f2ccadf05be107f20` |
| file 08 | `45dc4611717276c1f1c275982aa7ce787b2fa0b8fffbe1d315e8cb83ddff2206` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-093 commit | `f7ce35ff0eb310c731b93060775c8ef69b0d36e4` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch. D-094 remains a separate in-flight cycle and is not
this subject.

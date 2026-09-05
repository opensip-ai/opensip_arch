# D-100 — Condition-2 preview-deferral owner-recording mechanics

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. Not a retry of
> D-097, D-098, D-099, D-101, or D-102. Frozen D-096 /
> D-097 / D-099 / D-101 / D-102 subjects are not edited.
> **Decision type:** RULE-GOVERNED. Mechanics only. This
> file does not grant. D-096 (A) remains unsatisfied until
> a later user-made express grant.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mark any row `SATISFIED`.
> **Does not** edit file 08.
> **Does not** owner-record.
> **Does not** invoke D-054 / D-057 for these rows.
> **Does not** overturn D-054, D-057, D-096, D-097, D-098,
> D-099, D-101, or D-102.

D-096 is ADOPTED at `714790bb51521f21f7ee2acde39eb1f1c874056a`.
D-097 is ADOPTED at `11691723d2a4b959daf9ddf5ac3df3977f8259ac`
and withdrew a coordinator-composed grant. D-096 (A) is
unsatisfied. This entry is D-096 (B) only.

## Decision

1. **This file does not grant.** A later user-made express
   grant that covers every named role for the candidate
   being recorded is D-096 (A). This entry only states how
   later D-000 owner-recording entries must be written
   once that grant exists. A mechanics entry alone never
   grants. Overturning this entry does not create a grant
   and does not overturn D-096.

2. **Preconditions for one later owner-recording entry.**
   All of:
   - D-096 is still ADOPTED and not overturned;
   - D-100 is still ADOPTED and not overturned;
   - an applicable user-made grant (D-096 (A)) is ADOPTED,
     not overturned, and expressly covers every named
     role for the candidate being recorded;
   - D-054 / D-057 are not cited as that grant;
   - the candidate is one of the five D-096 artifacts
     below, still at its recorded digest;
   - both independent reviews of that candidate remain
     ACCEPT or ACCEPT-WITH-ADVISORIES at 0 blockers;
   - the coordinator recording of that candidate (D-096)
     is already ADOPTED and separately committed. Same-
     commit bundling of coordinator recording and owner
     recording is forbidden;
   - the owner-recording entry is its own D-000 cycle and
     its own commit.

3. **The only eligible candidates (digests as recorded
   by D-096).**

   | Artifact | sha256 | Roles this mechanics may record |
   |---|---|---|
   | `deferral.DR-108.preview.v2.json` | `225be4f985889b421b6d3a132c33a8aec924866f54401dd812d9db662fcd9beb` | Security + platform |
   | `deferral.DR-110.preview.v2.json` | `b6b678dc18dc0ff506d8a96cbf90246b3e84d99cd2a3387032124a153eb5fc52` | Release + platform |
   | `deferral.DR-116.preview.v2.json` | `ac8d2d4d414a66ef271042f9e98bcdd7397a08126d2bb011089913c63a628743` | Product security (Route C only) |
   | `deferral.DR-106-109-113.preview.v2.json` | `194b01fc6bd9201ebdeee71b83846cff09417d7521464bd81a0fbe2aabf7502c` | DR-106 Product + evidence + release; DR-109 Evidence + storage architecture; DR-113 Evidence + product |
   | `deferral.windows-platform.preview.v2.json` | `e7dd2b718fc6af5e46fc4706bc8b232a63c26beed4db42ec79a395b01af22b20` | Product + release + platform |

   No other condition-2 row. No SATISFIED re-record. No
   G03/G04 naming. No Route A. No freeze motion. No
   condition 5. DR-116 Route C does not generalize.

4. **Required pins on each later owner-recording entry.**
   - the D-096 (A) grant path and sha256; that grant's ID
     and full commit;
   - D-096 ID plus full commit; D-100 ID plus full commit;
   - candidate path and sha256; both verdict paths and
     sha256s; file-08 owner role(s) being recorded;
     preview scope; Route A remainder if any;
   - DEF110-C2-A1 on any DR-110 owner-recording (honesty
     work; not a blocker of D-096);
   - a statement that D-054 / D-057 are not this path.

   The owner entry must declare the grant, D-096, and
   D-100 as dependencies. Revocation or overturn requires
   that owner's supersession **and** reconciliation of
   every dependent MF-6 note under a separate reviewed
   act. An ACCEPT-WITH-ADVISORIES case must classify each
   advisory as non-operative or carry it into the owner
   record. DEF110-C2-A1 is carried.

5. **What a later owner-recording may do.** Record the
   candidate as the owner-recorded architecture-preview
   explicit deferral for those roles. It may not mark the
   row `SATISFIED`. It may not edit file 08. SATISFIED, if
   ever, is a **separate** later D-000-reviewed MF-6.
   Owner-recording precedes that MF-6 and is not it. It
   may not authorize `docs/v2/implementation/`. It may
   not apply a V1 successor, move the freeze, or move the
   claim register.

6. **This entry records no row.** Readiness effect zero.

## Alternatives

- Repeat or invent a grant in this file. Rejected:
  ADV-D095-T3-01 / D097-MF-1 / ADV-D097-01; D-096 (A) is
  unsatisfied; mechanics never grants.
- Cite D-054 / D-057 as covering these roles. Rejected:
  ADV-D095-T2-01.
- Same-commit coordinator + owner recording. Rejected:
  D-000 clause 4; D-096 is already separately committed.
- Expand eligible rows beyond the five D-096 candidates.
  Rejected: D-096 (A) must cover every named role **for
  the candidate being recorded**.
- Generalize DR-116 Route C. Rejected: D-096.
- Mark any row SATISFIED, or edit file 08. Rejected.
- Authorize implementation. Rejected: condition 5 last.

## Readiness effect

Zero. D-096 (A) stays unsatisfied. Condition 2 unchanged.
Condition 5 last.

## Reversibility

C-D100 revokes these mechanics. D-096 remains until
C-D096. Undoing effects also requires superseding every
owner recording that cites D-100 and reconciling each
dependent MF-6 note under its own reviewed act. Does not
create or revoke a grant.

## Measured inputs at turn-1 dispatch

| Path | sha256 |
|---|---|
| COORD (live) | `cda54c2590195c9d6523f7fefdfe5ccb16a2b0faeeb162972e850a9ce74cefe9` |
| file 08 | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| D-096 commit | `714790bb51521f21f7ee2acde39eb1f1c874056a` |
| D-097 commit | `11691723d2a4b959daf9ddf5ac3df3977f8259ac` |
| D-102 ADOPTED commit | `b838e72d3758a53cbefdb077fb6836d12ee7214f` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

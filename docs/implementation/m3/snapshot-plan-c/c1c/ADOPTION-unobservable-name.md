# Adoption receipt: C1c plan r4 addendum unobservable-name (LD-C1C-5A), 2026-10-29

**Decision LD-COORD-L8 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1.**

The addendum `ADDENDUM-unobservable-name-r2.md` is adopted as a successor of C1c plan r4 on the point it names. Under
LD-C1C-5's Names (Q4 ruling) exception, a malformed regular-file name without a matching suffix is counted only after
an actual, permitted kind observation. When the platform component predicate rejects the name, or the entry is
absent, the snapshot refuses `Name`. Any other native error keeps `HostIo`. All other PLAN-r4 text, and LD-C1C-7A,
are unchanged.

## What was reviewed

| Artifact | sha256 |
| --- | --- |
| **Adopted subject:** `ADDENDUM-unobservable-name-r2.md` (10,491 bytes; the reviewed bytes, never edited) | `f407232b26f366ac75eb5dc177f33094d52ec7114ecdeade0e72d775e73fde7f` |
| Amended record: `opensip_arch/docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r4.md` | `d066487af5608b0375bd0ba1f8eaefda9b8bdbe70d27d96a875ba43cca8fe835` |
| Inherited authority: `../l5-review/ADDENDUM-guard-charge-r2.md` (LD-C1C-7A) | `85bbb8ec883b572547215664ac088c2d5ceeea86c82bf71dec2ec95e931dab6f` |
| Inherited authority: its receipt `../l5-review/ADOPTION-guard-charge.md` | `3f641c5f4778054a33b561eabcc2d40554f1dbf721ab24076d771693562128a4` |
| Superseded draft: `ADDENDUM-unobservable-name-r1.md` | `4cd7ae2a168fb9f4496990f735ba4caf6030047df03347d214c89aff1e596294` |
| R3 review r1 (`L8-RULING: REFUSE-AMENDMENT-CHANGES`): `REVIEW-r1.md` | `ed9a940c5aa7c99ffa67c94f6f45725758af79738039c6678ed2540d85c79036` |
| **R3 review r2 (`L8-AMENDMENT: ACCEPT`, no required findings): `REVIEW-r2.md`** | `ea86f7aadb14e70e5e1043a4095da6bbbead51491b5fc0871c7af6d3a5080e5c` |
| Requests r1 and r2 | `e0df26bc…53fec`, `25621f54…346ee` |
| The author's control note, folded into §4: `AUTHOR-NOTE-r1-controls.md` | `5e47620a4c2461dec1a1dd8fe6eed75a136e319979e42c83bb1cf040985d7a9e` |
| The author's request: `../../c1c1/COORDINATOR-REQUEST-L8.md` | `96e601f394a8dcf7c5dec3b8579a80fd04f0582bea137e16245c8e6e6bb2aa6c` |

**The reviewer:** codex-l5-r3, Codex gpt-6-astra/high, R3-FRONTIER. It is a different vendor from the Claude author
(C1c-1, wT) and the Claude coordinator.

**The origin:** C1c-1 code review r2, RF-2, from codex-c1c1-r1.

## The authority

The owner's decision OD-AUTO-1 (2026-10-29, the top of `control-2026-10-06/ACTIVE-PLAN.md`) delegates law changes
to the coordinator after an R3 different-vendor review. This adoption:
- narrows the read set's admitted set, which is stated in the addendum's §3;
- changes no cap and no *L*max;
- leaves the malformed-name refusal work in *N*.

## What this adoption does not accept

As REVIEW-r2 states, this adoption does not accept:
- the C1c-1 source, including a009ad6;
- its model or pricing correspondence;
- its control execution;
- the author note's filesystem claims as measured facts;
- any production test hook;
- its lane, integration, binding, receipt interval or qualification.

## Binding

At C1c-1's binding, the addendum and this receipt are copied unchanged beside PLAN-r4 in the architecture repository,
next to the guard-charge pair, and the inventory records all four files.

## Owner notification

On 2026-10-29 this is flagged to the owner in the coordinator's session summary as an owner-delegated law change. The
owner can reverse it.

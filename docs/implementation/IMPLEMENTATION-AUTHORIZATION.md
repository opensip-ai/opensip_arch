# Implementation authorization record — CONFIRMED by the owner, 2026-10-03

2026-10-03. Drafted by Claude Opus 5.5, implementation lead, at the owner's request. The owner confirmed it on 2026-10-03; see "Confirmation".

## Why this record exists

D-372's readiness table says condition 5, implementation authorization, is NOT MET: "The user authorized architecture/design/reference work only. Implementation requires a separate explicit authorization after these accepted design records" (`docs/v2/architecture/08-decision-and-readiness-register.md`, condition table, row 5).

Since then the owner has authorized implementation several times, but only in implementation logs:
- `docs/implementation/m1/progress-checkpoint-before-interruption02.md:5-7` (2026-09-16): "The user authorized the entire implementation with actual Claude verifying the work, and asked us to continue until complete."
- `docs/implementation/ACTIVE-WORK.md:5` and `:390` (2026-09-16): "continuous full-project implementation" and "continuous autonomous implementation through full project completion".
- `docs/implementation/README.md:3` (2026-09-22): "Local commits in both repositories are authorized. The user will push; no push is authorized here."
- The owner's standing direction of 2026-09-30, recorded in every M2 law: the lead decides on its own recommendation, records the rejected alternatives, and blocks on the owner only when it has no recommendation.

No coordinator decision after D-372 records any of this, so the design record and the work disagree. This record closes that gap in one citable place.

## Where it lives, and why not in the register or COORDINATOR-DECISIONS

Both the register and `docs/coop/COORDINATOR-DECISIONS.md` are pinned. The register is pinned by the product's `design-lock.json` and the D-372 application manifest (`application-subject.v46.json`). COORDINATOR-DECISIONS is pinned by the same manifest. Appending to either would change D-372's activation subject. So this record is a separate, unpinned file:
- the errata record (`m3/record-hygiene/PROPOSAL.md`, item 6) points to it;
- the register's condition-5 row gets a note pointing here, as one of the staged notes, when the next successor re-pins it.

## What is authorized

On confirmation, the owner authorizes:

1. **Implementation of the whole selected product,** milestones M0 to M6 of the build plan (`implementation-boundaries-and-build-plan.md:884-890`), in the product repository `/Users/sb/code/opensip-ai/opensip`, under the accepted contracts and their reviewed successors.
2. **Lead autonomy.** Claude Opus 5.5 leads. Where the lead has a recommendation, it decides, records the decision with its rejected alternatives in the owning law or plan, and proceeds. It blocks on the owner only where it has none, or where the decision is the owner's: product thresholds, scope, consent, licence, platforms. This is the 2026-09-30 standing direction.
3. **Independent review.** Every law, contract successor and code unit is reviewed by an independent reviewer before acceptance. Grok, Codex, GROK2 and CODEX2 are reached through herdr. The lead does not accept its own work.
4. **Local commits** in `opensip` and `opensip_arch`, including integration of accepted units onto `main`.

## What is not authorized

- **Pushing to any remote, or publishing any release, package or artifact.** The owner pushes.
- **Changing an accepted contract, gate, threshold or decision** other than through a reviewed successor.
- **Treating any gate as QUALIFIED,** or any measurement as qualification evidence, without its gate's actual execution. Condition 4's "harness implementation/execution and real supported-platform qualification remain required" stands.
- **Running OpenSIP against the owner's real home installation** during development, or on private code outside the M3 analysis-quality plan's T3 rules.

## Effect

When confirmed, D-372 condition 5 reads as MET from the confirmation date, by this record. Conditions 1 to 4 and their stated limits are unchanged. Implementation work done before confirmation was done under the logged authorizations above, and this record confirms it.

## Confirmation

The owner confirmed it on 2026-10-03, in reply to the lead's summary of this record: "confirmed, keep going". No changes were requested. D-372 condition 5 is MET from 2026-10-03 by this record.

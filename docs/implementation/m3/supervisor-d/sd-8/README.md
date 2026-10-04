# SD-8: NE's excluded-form row conformed to RTC §7.4 (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit. It edits only arch. It adds no product file, code, class, exit code, error code, route or public detail code. It needs CODEX2's `ACCEPT-DESIGN-UNIT`, with a review that lists `supersededPassages`, and the lead's root assent before it can be bound.

**What it is.** NE §10's excluded-form row lives at NE:3540. SD-5 added it as an override (bound at `052d3cb`), and SD-7 superseded that override (bound at `d2c00a9`). Its sentence on the not-installed golden reads:

> A required closure that is not installed, or that current trust does not admit (an ephemeral request with no trust view included), is never an excluded form and keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`.

That gives an ephemeral request a detail. The run-termination contract's §7.4 admits no detail on an ephemeral attempt (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`; RTC:286-292). The lead ruled that §7.4 governs: an ephemeral attempt carries no detail (`reviews/grok-j2a-r1/REQUEST.md`, "Lead rulings", item 3; work log `docs/implementation/OVERNIGHT-2026-10-03.md`, "Lead rulings on J2a's open items", item 3). M3-C r8 applies the ruling to E-3 (MC8 item 7, MC8:431), and J1 r6, accepted by Codex, applies it to row 27 (MJ6:783). NE's row still says the opposite. J1 r6 records the conflict and the lead's ruling on it (MJ6:822, "Routed to the lead" at MJ6:971-972; work log, the J1 r6 entry): SD-8, an NE passage supersession of SD-7's NE:3540 override, keeps every word of that row except the ephemeral form's detail, and is owed before J2c, the first unit that emits the ephemeral form.

**Product.** Main `1799d3d` (CRC-2's binding), read only. Its lock has 99 contract successors and 4 contract passage supersessions. SD-7's entry is still the current meaning of NE:3540: no later record supersedes it. The record is built and checked against `1799d3d`'s lock, read with `git show`.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes) | `83b99783…` |
| **SD5** | `docs/implementation/m3/supervisor-d/sd-5/successor.json`, bound at `052d3cb` (5,805 bytes) | `5e115818…` |
| **SD7** | `docs/implementation/m3/supervisor-d/sd-7/successor.json`, bound at `d2c00a9` (14,706 bytes) | `350a249a…` |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` (32,543 bytes), which no bound record overrides | `cfe793fc…` |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md`, M3-C r8, accepted in review by CODEX2 | `578c186e…` |
| **MJ5** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, M3-J1 r5, accepted by Codex | `4ccb2320…` |
| **MJ6** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md`, M3-J1 r6, accepted by Codex (`reviews/codex-host-pipeline-j-r6`) | `086e804a…` |
| **RULING** | `docs/implementation/m3/reviews/grok-j2a-r1/REQUEST.md`, "Lead rulings", item 3 | `c2fbbe41…` |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md`, §9's goldens (WS:1374) | |
| **VD** | `tools/verify_design.py` at product `1799d3d` (43,946 bytes) | `7b313de6…` |
| **VD2** | `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, the accepted law of contract passage supersession | `2e4f70b4…` |

The precedents for the form are SD-7 (`supervisor-d/sd-7/`), REG v3 and CRC-2.

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the supersession's exact `before`, its `after` and the word-level changes |
| `successor.json` | the record: one parent (NE), one `passageSupersessions` entry, no `passageOverrides`, four candidates |
| `evidence/build_sd8.py` | builds the generated files, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_sd8.py` | read-only, independent checks |
| `../sd-8-subject.json` | the subject manifest (generated) |
| `../sd-8-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/codex2-enum-1-sd-8-r1/sd-8/review.json`; not part of the subject |

The local binding check runs both units of the request, alone and together. Its script and output are request evidence: `reviews/codex2-enum-1-sd-8-r1/evidence/`.

## What changes

One entry: a **supersession of SD-7's override** of NE, line 3540. Its `before` is SD-7's `after`: two table rows, the raw release-declaration row and then the excluded-form row. SD-8 keeps the first row byte for byte. In the second row it keeps every word and changes one sentence:

| | Text |
|---|---|
| **Before** | … is never an excluded form and keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`. |
| **After** | … is never an excluded form and keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` on a durable request. On an ephemeral request, the no-trust form included, it is `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, with no runId and no detail, because the run-termination contract's §7.4 admits no detail on an ephemeral attempt (contract successor SD-8). |

So:

| Case | Class / exit | Code | Detail | Changed? |
|---|---|---|---|---|
| durable, required closure not installed or not admitted by current trust | indeterminate 3 | `COVERAGE.PROVIDER_UNAVAILABLE` | `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | no |
| ephemeral, no admitted trust view (E-3) | indeterminate 3, `authority: ephemeral`, no runId | `COVERAGE.PROVIDER_UNAVAILABLE` | none (RTC §7.4) | yes |
| ephemeral, required closure not installed or not admitted | indeterminate 3, `authority: ephemeral`, no runId | `COVERAGE.PROVIDER_UNAVAILABLE` | none (RTC §7.4) | yes (LD-S8-2) |
| an excluded form, the row's own subject | request-rejected 2 | `EXTENSION.ADMISSION_REJECTED` | `PAYLOAD-NOT-ADMISSIBLE` | no |

Nothing else changes: the release-declaration row, the excluded-form row's classes, predicate, route, detail, remedy and every other sentence, NE:3539's row, WS, RTC and every product file. `check_sd8.py` proves that every word of SD-7's text survives in order and that the only character removed is the old sentence's closing period.

## Why this form

- **NE:3540 has a bound meaning.** SD-5's override is bound, and SD-7 superseded it. A second override of the line refuses ("conflicting contract passage overrides", VD:409-411). Law VD2 admits a contract passage supersession instead (VD:349-369): the entry names SD-7's record by exact pin, with the same parent and selector, and its `before` is SD-7's `after`. The review must list `supersededPassages`, equal to the record's `supersedes` list (VD:420-426).
- **SD-7 is the current meaning.** Superseding SD-5's override again refuses ("double supersession: the named passage is not the current meaning"), and the local check's probe shows it.
- **NE stays the selected native-evidence contract.** No bound record carries a complete NE copy, and SD-8 makes none.

## Lead decisions

Each is dated 2026-10-04 and made under the owner's standing direction. Each names the alternatives it rejects, and the owner may reverse any of them.

**LD-S8-1 (the lead's ruling). SD-8 is a VD2 passage supersession of SD-7's NE:3540 override that keeps every word except the ephemeral form's detail.**
- **Rejected: reading the sentence as fixing only the class and code.** The sentence lists the detail beside them, so that reading leaves a bound contract sentence contradicting §7.4.
- **Rejected: a contract successor changing RTC §7.4** so that an ephemeral result could carry the detail. A law cannot override the contract, and nothing needs the detail (RULING; MC8 LD8-5).
- **Rejected: a raw override of NE:3540,** which VD refuses as conflicting, or a complete NE copy, which would move the selected NE for every successor in flight (SD-7 LD-7.1).

**LD-S8-2 (the drafter's, for the lead to confirm). The ephemeral clause covers every ephemeral request, the no-trust form included.** The sentence's subject is a required closure that is not installed or not admitted, on any request. RTC §7.4 admits no detail on any ephemeral attempt, with or without a trust view, and the ruling says "an ephemeral attempt carries no detail".
- **Rejected: dropping the detail only for the no-trust form.** An ephemeral request that has a trust view but whose required closure is not installed would still keep the detail, so the sentence would still contradict §7.4.

**LD-S8-3. The durable case keeps the detail, stated as "on a durable request".** RTC §7.5's row 2 selects `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` for a committed Run, and MC8 item 7 keeps it ("The durable not-installed case keeps that detail"). SD-8 changes nothing about which durable cases carry it.

**LD-S8-4. No other text moves.** WS:1374's golden table names no authority, and RTC already governs the ephemeral projection, so WS needs no change. Row 27 is J1's, and J1 r6 already splits it: durable with the detail, ephemeral without (MJ6:783).

## Cross-law items

1. **For J1's next revision.** Row 27's basis (MJ6:783) gains "NE:3540 (SD-8)" for the ephemeral case, and MJ6:822's "Recorded, not resolved" bullet becomes resolved once SD-8 binds.
2. **For J2c.** Its ephemeral leg (MC8 C2-T18; MJ5 E-3) emits the form SD-8 states: indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, no runId, no `domainDetail`. J2c needs SD-8 bound first.
3. **ENUM-1**, this request's other unit, admits the Plan for the same case. The two are independent, and each binds alone.

## Points for the reviewer

- **R1 (faithfulness).** Does SD-8 keep every word of SD-7's row and change only the ephemeral form's detail, as the lead's ruling and RTC §7.4 require?
- **R2 (scope, LD-S8-2).** Is covering every ephemeral request, not only the no-trust form, right?
- **R3 (form and binding).** Is the supersession well formed under VD2, and does it bind after main's chain, alone and with ENUM-1, with your review's `supersededPassages`?

## Binding

SD-8 binds on VD at main `1799d3d`, on top of all 99 contract successors. After `ACCEPT-DESIGN-UNIT`:
1. copy the review into `docs/implementation/m3/reviews/codex2-enum-1-sd-8-r1/sd-8/review.json`;
2. complete `sd-8-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append the four pins to the product lock, in a binding-only product commit, before J2c;
4. run plain VD.

The review must carry this `supersededPassages` list, exactly:

```json
[{"record": {"path": "docs/implementation/m3/supervisor-d/sd-7/successor.json", "bytes": 14706, "sha256": "350a249afaa001fc97292c2837395d930cc7bdc0d6b62b594b04df55d9767c04"}, "parent": {"path": "docs/v2/contracts/product-v1/native-evidence.md", "bytes": 329013, "sha256": "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"}, "selector": {"line": 3540}}]
```

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo or a test.
- **`evidence/build_sd8.py`**, then `--check`, which reports identical bytes for every generated file, the unit draft included.
- **`evidence/check_sd8.py`** passes at `1799d3d`.
- **The local binding check** (`reviews/codex2-enum-1-sd-8-r1/evidence/verify_scratch.py`) ran in a throwaway detached worktree of product main `1799d3d`. Its output is `local-binding-check.json` beside it. The request states the results.

## Not changed, and noted

- **No code, class, exit, route or detail is added.** SD-8 removes a detail from one form and adds nothing.
- **No product file is touched.** No code, test or build was run.

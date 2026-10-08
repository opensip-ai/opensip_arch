# The S-OP-2 recording: units S-OP-2-P and S-OP-2-R (design units)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** These are two design units. They edit only arch, and change no product file, code, class, exit code, route or public code. Each needs Codex's `ACCEPT-DESIGN-UNIT`, in its own `review.json`, and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What they record.** Contract successor S-OP-2 r6, the safe event vocabulary and sink law, is accepted by Codex as `ACCEPT-DESIGN-UNIT` with no required findings (`reviews/codex-s-op-2-r6/review.json`; `PROPOSAL-r6.md`, `ce8d3a4b…`, 130,001 bytes). Its item 24 says how it is recorded (SOP2:917-930): "The accepted PROPOSAL is the successor text. When M3-O's first code unit lands, the lead records a verify_design successor (`successor.json` plus a subject manifest that pins this accepted PROPOSAL's bytes, the EC1 form). It makes two **insertion-only** passage overrides". The review "checks the selectors, the parents and the DR-114 report split". Law M3-O1 r1 item 22 schedules the recording: it binds before, or with, O1-a's integration.

**Product.** Main `b7b87b7` (E2a), read only. Its lock has 101 contract successors and 98 inventory successors, with v138 selected. The units are built and checked against that lock, read with `git show`.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, S-OP-2 r6, accepted by Codex (ACCEPT-DESIGN-UNIT). Its accepted bytes still carry r5's title line; the live `PROPOSAL.md` says so. | `ce8d3a4b…` |
| **SDK4** | `docs/coop/artifacts/component-sdk-contract.v4.json` (17,867 bytes). Its own header says `CANDIDATE-NOT-APPLIED` and `"binds": "NOTHING"`; the DR-125 application row inherits it. | `c53d541f…` |
| **DRC** | `docs/coop/completion/distribution-runtime-completion.v2.md` (49,989 bytes), the D.SDK selection of its §8 | `9ab2874e…` |
| **APP** | `docs/coop/completion/architecture-application.v1.json` (443,974 bytes), the D-369 application, selected by the lock's source manifest | `15b3932a…` |
| **VD** | `tools/verify_design.py` at product `b7b87b7` | pinned in the request |
| **CS1** | `docs/implementation/m1/control-source-v1/successor.json`, the precedent for selecting an existing, unselected architecture file | bound (lock index 1) |
| **MO1** | `docs/implementation/m3/operability/o1/PROPOSAL.md`, law M3-O1 r1, in review in the same request | pinned in the request |

## The finding: item 24's parents are not selected (LD-R1)

**The fact.** Neither SDK4 nor DRC is in the design the lock selects at `b7b87b7`:
- neither is a file of the source manifest (`candidate-subject.v45.json`, 12,920 files) or of the application manifest (`application-subject.v46.json`, 197 files);
- neither is a candidate of any of the 101 bound contract successors.

APP pins both by path and sha256, at `/rows/12/inheritedContract` (the DR-125 row, SDK4) and `/evidenceTargets/D.SDK/sources/0` (DRC, selector "## 8. SDK contract (DR-125)"), but the manifests do not carry their bytes.

**Why it matters.** VD's `contract_successor` requires every parent to be "an accepted base or selected inventory". The accepted set is the two manifests plus every earlier unit's candidates. A record whose parent is outside it refuses: "contract parent is not an accepted base or selected inventory". A unit cannot select a file and override it at once, either: a parent that is also a member refuses ("contract successor would overwrite its parent"). So item 24's one-record form cannot bind as written. The local check below confirms the refusal.

**The decision (lead decision, recorded in MO1 item 22).** Record S-OP-2 as two units, bound in this order:
1. **S-OP-2-P** selects the exact SDK4 and DRC bytes that APP pins, at their own paths, with no override. Its only parent is APP. This is CS1's form: CS1 selected the existing, unselected `control-completion.schema.v3.json` for the same reason. Selection binds bytes only. SDK4 keeps its `CANDIDATE-NOT-APPLIED` header and means only what the DR-125 row already inherits.
2. **S-OP-2-R** is item 24's recording: it pins S-OP-2 r6's accepted bytes and makes the two insertion-only overrides, with SDK4 and DRC as parents.

**Rejected:**
- **Complete copies of SDK4 and DRC at new paths, carrying the insertions.** Item 24 asks for insertion-only overrides. A copy makes the review re-read two whole files, and leaves two texts for each document: the bytes APP pins, and the selected copy.
- **Overriding APP's pins.** That changes the D-369 application, not the DR-125 texts.
- **Pinning S-OP-2 r6 with no override.** Item 24 requires the two overrides.
- **Overriding F02:193-197 instead,** which is selected. Item 24 rules it out: DRC §8 is F02's preview successor, and F02 is D-372-pinned (SOP2:928).

## The lock check: plain overrides, no supersession

No bound record at `b7b87b7` names SDK4 or DRC in a passage override or supersession: they were never selected, so nothing could override them. Both entries are therefore plain overrides. Law VD2's passage supersession, as SD-7, REG v3, CRC-2 and SD-8 used it, does not apply. Both reviews list `"supersededPassages": []`.

## Files

| File | What it is |
|---|---|
| `s-op-2-r/README.md` | this proposal, for both units |
| `s-op-2-r/PASSAGES.md` | generated: both overrides, with `before`, `after` and the inserted sentence |
| `s-op-2-r/successor.json` | S-OP-2-R's record: two parents, two `passageOverrides`, five candidates |
| `s-op-2-r/evidence/build_sop2.py` | builds every generated file of both units deterministically; `--check` compares instead of writing |
| `s-op-2-r/evidence/check_sop2.py` | read-only, independent checks |
| `s-op-2-p/successor.json` | S-OP-2-P's record: one parent (APP), two candidates (SDK4, DRC), no override |
| `s-op-2-p-subject.json`, `s-op-2-r-subject.json` | the two subject manifests (generated) |
| `s-op-2-p-unit.json`, `s-op-2-r-unit.json` | the lead's assent drafts, `DRAFT-PENDING-REVIEW`; not subject members |

**S-OP-2-R's subject** is `PROPOSAL-r6.md` (the successor text, at its accepted sha), `PASSAGES.md`, this README, the two evidence scripts and `successor.json`. **S-OP-2-P's subject** is exactly its `successor.json`, SDK4 and DRC, as CS1's was.

The local binding check script is not a member of either unit. It covers both units, alone and together, so it lives in the review request's `evidence/` directory, as ENUM-1's and SD-8's did.

## What changes

| # | Unit | Kind | Parent | Selector | Change |
|---|---|---|---|---|---|
| 1 | S-OP-2-P | selection | APP (parent) | none | SDK4 and DRC enter the selected design, byte-identical to APP's pins |
| 2 | S-OP-2-R | override, insertion-only | SDK4 | `/standardizedFamilies/1/rule` | SF-2's rule gains item 24's sentence: " For host operational records, the only records are events of the S-OP-2 registry whose fields are S-OP-2 SafeField kinds, and free text reaches no operational sink; the doctor report keeps its DR-114 redaction tiers (contract successor S-OP-2)." |
| 3 | S-OP-2-R | override, insertion-only | DRC | `line 576` | "meaning." is followed by " The host reduces that channel to its byte count and truncation flag before any operational sink (contract successor S-OP-2)." The rest of the line, " The SDK owns framing,", is unchanged. |

Both sentences are item 24's, character for character. Each `after` minus its inserted sentence equals its `before`. The original punctuation is kept. **The DR-114 split** holds: the SDK4 sentence scopes itself to operational records and names the doctor report's DR-114 tiers, so DC4 is unchanged (SOP2 item 18).

## Binding

Both bind on VD at main `b7b87b7`, on top of its 101 contract successors, S-OP-2-P first. After `ACCEPT-DESIGN-UNIT` for each:
1. copy each review into `docs/implementation/m3/reviews/codex-o1-law-r1/s-op-2-p/review.json` and `.../s-op-2-r/review.json`;
2. complete `s-op-2-p-unit.json` and `s-op-2-r-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append S-OP-2-P's four pins, then S-OP-2-R's, to the product lock;
4. run plain VD.

Each review lists `"supersededPassages": []`. VD accepts the empty list for a record with no supersession.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo or a test.
- **`evidence/build_sop2.py`**, then `--check`, which reports identical bytes for every generated file, both unit drafts included.
- **`evidence/check_sop2.py`** passes at `b7b87b7`. It checks the accepted r6 bytes against Codex's review, the parent finding, S-OP-2-P's candidates against APP's pins, each override's selector, `before` and insertion-only `after` against item 24's quoted text, the DR-114 split, both subjects, both unit drafts and this README.
- **The local binding check** (`reviews/codex-o1-law-r1/evidence/verify_scratch.py`) ran in a throwaway detached worktree of product main `b7b87b7`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`. It loads the worktree's own VD unchanged and serves SCRATCH review and assent pins from memory, as CRC-2's check did. Its output is pinned in the request (`evidence/local-binding-check.json`), and the worktree was then removed. The request reports the results:
  - the baseline passes, as the literal CLI and as the overlay run;
  - **S-OP-2-R alone refuses** with "contract parent is not an accepted base or selected inventory", which is the finding;
  - S-OP-2-P alone, and S-OP-2-P then S-OP-2-R, pass, with the worktree as implementation and without it, and everything outside the contract chain equals the baseline;
  - the refusal probes refuse as expected.

## Not changed, and noted

- **No product file is touched.** No code, test or build was run.
- **No meaning of SDK4 or DRC changes beyond the two sentences.** Selection adds no text.
- **F02 is not overridden** (SOP2:928).
- **The binding gap is general.** Any later successor that overrides a DR-125 text not in the manifests meets the same refusal. Once S-OP-2-P is bound, SDK4 and DRC are selected and later overrides of them bind normally.

## Points for the reviewer

- **R1 (faithfulness).** Are S-OP-2-R's two sentences exactly item 24's, insertion-only, with the original punctuation kept? Does the SDK4 sentence keep the doctor report's DR-114 tiers?
- **R2 (the parents).** Is the finding right: neither SDK4 nor DRC is selected at `b7b87b7`, so item 24's record alone refuses?
- **R3 (the selection).** Is S-OP-2-P, in CS1's form, a lawful way to select them? Does it select exactly the bytes APP pins, and nothing else?
- **R4 (no supersession).** Is it right that no bound record overrides either passage, so plain overrides and `supersededPassages: []` are correct?
- **R5 (binding).** Do both units bind in order after main's chain, and does any selected passage conflict?

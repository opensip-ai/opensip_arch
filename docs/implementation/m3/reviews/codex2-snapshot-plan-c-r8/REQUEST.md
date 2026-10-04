CODEX2 review: M3-C r8, the sealed snapshot and Plan law, and its new identity successor CRC-2. Claude Opus 5.5 leads, and you are the single reviewer. Two verdicts are wanted, in two files:
- **M3-C r8**, a **law and contract-soundness** review, round 8: **ACCEPT** or **REQUIRED-FINDINGS**;
- **CRC-2**, a **design-unit (contract successor)** review: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**. If you accept, its `review.json` must carry `supersededPassages` (below).

Write only under `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r8/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No cargo.** Don't run any build, test or lead set: timing-sensitive lanes may be using this machine.
- You may re-run `crc-2/evidence/verify_scratch.py` only in your own throwaway detached worktree of product main `21e428d`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, as the lead did. It is Python only. Never run it in the main product checkout: it rewrites the worktree's `design-lock.json`. Remove the worktree afterwards.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The subjects

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/`. Every pin is in `hashes.txt`. Several live laws are being drafted in parallel, so this request pins accepted snapshots only, apart from the two subjects. r8 is uncommitted in arch, and CRC-2's files are untracked until acceptance: read the working-tree bytes and check them against the pins.

| Subject | Path | sha256 | Bytes |
|---|---|---|---|
| **M3-C r8** (`subjectSha256`) | `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` | `578c186e…` | 183,744 |
| **CRC-2** (`subjectManifestSha256`) | `docs/implementation/m3/snapshot-plan-c/crc-2-subject.json` | `58205eea…` | 1,234 |

CRC-2's members are its README, `PASSAGES.md`, `successor.json` and three evidence scripts under `snapshot-plan-c/crc-2/`. The lead's assent draft, `crc-2-unit.json`, is not a member.

**The diff base for the law:** `snapshot-plan-c/PROPOSAL-r7.md` (`a1ee9386…`), the r7 bytes you accepted in review, without the note.

## What r8 changes

r8 takes up exactly the cross-law items that two accepted laws address to C, and nothing else. Its header and "r8 changes" table list each one; "r8 lead decisions" lists LD8-1 to LD8-6 with the alternatives they reject.

| Source | Item | Where in r8 |
|---|---|---|
| **M3-H r3** (`fact-admission-h/PROPOSAL-r3.md`, Grok, `7a562720…`) | **X-H3** (MH:644-672, :811, :860-866): a third admitted use of the core provider closure, as producer and enumerator of host inventory records in every universe, and one host inventory stage per universe | item 9 (use 3, its bound, membership; LD8-1); item 16 (`semanticClosures` row, step 12, the inventory stages; LD8-2); C2-T13, C2-T13a, C4-T22; successor CRC-2 (LD8-6) |
| M3-H r3 | **X-H5's `vcs-change` question** (MH:662, :868-871), which H routes to C | item 4's new bullet (LD8-3) |
| M3-H r3 | **X-H6** (MH:363-365, :812): the subject-scope bounds as S-B fields | the S-B successor row |
| M3-H r3 | **Record correction** (MH:876), placed at MC:885 by M3-PLAN r10's change 15 | step 15's citation, `:107-111` to `:108-111` |
| **M3-J1 r5** (`host-pipeline-j/PROPOSAL-r5.md`, Codex, `4ccb2320…`) | **S7b's E-2** (MJ5:463): the ProjectId of an unregistered root, or of a request with no I | item 6 (LD8-4); C1-T28 |
| M3-J1 r5 | **S7b's E-3, C half** (MJ5:464): no admitted trust view, so no manifest-admitted closure | item 7 (LD8-5); C2-T18; cross-law finding X-8 |

**What stays owed of S7b:** E-1 (M3-B and X2) and the X4T halves (E-3's trust half, E-4). r8 records what C1 needs from E-1 as cross-law finding X-11.

**A lead ruling applied to E-3.** While r8 was drafted, J2a's request recorded a lead ruling (`reviews/grok-j2a-r1/REQUEST.md`, "Lead rulings", item 3). The run-termination contract's §7.4 admits no §7.5 detail on an ephemeral attempt (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`). So E-3's ephemeral result is indeterminate with `COVERAGE.PROVIDER_UNAVAILABLE` and no detail, and E-3's `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` detail is corrected to fit. J1 r6 corrects row 27's text. The rejected alternative is a contract successor changing §7.4. Item 7 states it, citing RTC §7.4.

**Not taken up:** FA-2's three asks of C (M3-PLAN r10's C row). r8's "Not claimed" says so.

## CRC-2

CRC-2 carries r8's use 3 as identity text. Read `crc-2/README.md` first; `PASSAGES.md` shows every `before` and `after` with word-level changes.

| # | Kind | Parent | Selector |
|---|---|---|---|
| 1 | **supersession** of CRC-1's bound override | `docs/v2/contracts/product-v1/identity-and-evidence.md` (`c82404f3…`) | line 285 |
| 2 | **supersession** of CRC-1's bound override | the same | line 1377 |
| 3 | override | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json` (`73645b76…`), SYN-1F's copy, the selected IDS | `/x-opensip-digest-domains/closureKinds/note` |
| 4 | override | the same | `/x-opensip-digest-domains/closureMembership/selectionLaw` |

- **Why supersessions.** IE:285 and IE:1377 carry CRC-1's bound overrides (lock index 82). A second override refuses, so the entries use law VD2's form, as SD-7 and REG v3 did: same parent and selector, `before` equal to CRC-1's `after`, and `supersedes` naming CRC-1's record by exact pin.
- **Why plain overrides on SYN-1F's copy.** It is the last complete identity-schema copy in the chain. It carries CRC-1's strings in place, and no bound record overrides its pointers.
- **What it leaves alone:** I1-L's copy, which keeps CRC-1's bound overrides but is no longer selected; COMP:9, WS:308, WSE:312 and the detector-manifest description; NE, NCM, ENC, EXC and their schemas; every product copy.
- **It binds only after M3-C r8 is accepted** (README LD-5).

### Your review must carry `supersededPassages`

`verify_design.py` refuses a contract passage supersession that its review does not list (`:420-426` at `21e428d`). So if you accept CRC-2, `crc-2/review.json` must contain `supersededPassages`, equal by value and in order to the record's `supersedes` list. The exact value:

```json
[{"record": {"path": "docs/implementation/m3/snapshot-plan-c/crc-1/successor.json", "bytes": 21493, "sha256": "29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166"}, "parent": {"path": "docs/v2/contracts/product-v1/identity-and-evidence.md", "bytes": 135448, "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"}, "selector": {"line": 285}}, {"record": {"path": "docs/implementation/m3/snapshot-plan-c/crc-1/successor.json", "bytes": 21493, "sha256": "29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166"}, "parent": {"path": "docs/v2/contracts/product-v1/identity-and-evidence.md", "bytes": 135448, "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"}, "selector": {"line": 1377}}]
```

### The lead's local binding check

The output is pinned: `reviews/codex2-snapshot-plan-c-r8/evidence/local-binding-check.json`.
- **Where.** A throwaway detached worktree of product main `21e428d` (`/Users/sb/code/opensip-ai/opensip-crc2-check`, since removed), with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, also removed. Python only, with no cargo.
- **How.** The worktree's own `tools/verify_design.py` (43,946 bytes, `7b313de6…`, byte-equal to `21e428d`'s) was loaded unchanged. CRC-2's entry was appended to the worktree's `design-lock.json` with `SCRATCH-CRC2/review.json` and `assent.json` pins. As in REG v3's `verify_reg_v3_r2.py`, an overlay of `pinned_bytes` serves those placeholders from memory, and the scratch review carries the list above.
- **Results:**
  - **Baseline:** the literal CLI on main's lock passes, with 98 contract successors and 2 contract passage supersessions. The overlay run agrees.
  - **With CRC-2 appended:** PASS, both with the worktree as `implementation` and without it. There are 99 contract successors and 4 contract passage supersessions. The inventory chain, inheritance and supersessions, generation and admission sources, and verified inputs equal the baseline's.
  - **Refusals:**
    - a review without `supersededPassages`: "contract passage supersession is not listed by its review";
    - a review listing `[]`: "contract review superseded passages differ from the record";
    - CRC-2 with raw overrides of IE:285 and IE:1377: "conflicting contract passage overrides";
    - after CRC-2, a second supersession of CRC-1's IE:285: "double supersession: the named passage is not the current meaning";
    - after CRC-2, a second override of its `closureKinds/note` pointer: "conflicting contract passage overrides".
  - **The literal CLI on the appended lock** stops at "missing or escaping regular file: SCRATCH-CRC2/review.json". It fails closed, as for earlier units' SCRATCH pins. The overlay run is the binding result.
- `build_crc_2.py --check` reports identical bytes, and `check_crc_2.py` passes, at `21e428d`.

## Decide

**For M3-C r8:**
1. **Scope.** Diff r7 against r8. Does every change belong to one of the items above, or to the header, the two r8 tables, short names, successors, units, cross-law findings, forbidden substitutes, open questions or "Not claimed"?
2. **X-H3 and the bound (LD8-1).** Is use 3 faithful to MH item 18 and X-H3? Does its bound keep the principle at r7:458 both ways: the three `inventory` relations only, host-derived records only, four fields, never a binding that owes a symbol inventory, and the mirror rule for language provider closures? Is membership "exactly when a syntax universe is selected or an `inventory` cell is requested" right, including the unavailable-binding case?
3. **The stage (LD8-2).** Is one host inventory stage per universe right? In a syntax universe, is it right that an `inventory` binding names it rather than E3's syntax stage? r8 decides this by ME:578's text, which lists the syntax stage's outputs, and records X-10 for E1. Is the stage's `["view"]` output domain consistent with EXC:59 and :266-270?
4. **`vcs-change` at M3 (LD8-3).** Is "no fact, and an `unknown` entry with `provider-unavailable` and `capability-missing`" the right disclosure, given item 4 and NE:393-395 and :3370?
5. **X-H6.** Does the S-B row carry H's two bounds as H asks?
6. **E-2 (LD8-4).** Is a fresh PROJECT-ID-V1 draw, never persisted or compared, consistent with IE:41-58, SL:1521 and INC, and is the incomparability stated?
7. **E-3 (LD8-5).** Is item 7's no-trust-view rule right, including the core role closures that stay, the cells kept as unavailable bindings, and the no-detail answer under RTC §7.4? Is X-8 a real gap between ENC:53 and WS:1374, and is the lead's recommendation sound?
8. **Consistency.** Does r8 contradict any accepted text: M3-H r3, M3-J1 r5, M3-E1 r3, M3-D r3 (row 8 is unchanged), CRC-1 as bound, or M3-PLAN r10?

**For CRC-2:**
1. **Faithfulness.** Is CRC-2 exactly r8 item 9's use 3, its bound and its membership, neither wider nor narrower?
2. **Form.** Are the two supersessions well formed under VD2, and are SYN-1F's copy and plain overrides the right IDS target?
3. **Nothing else.** Does every sentence of CRC-1's text that CRC-2 does not rewrite survive, and do the three membership statements agree?
4. **Binding.** By reading `verify_design.py` at `21e428d` (`contract_successor` at `:186-276`, `successor_chain` at `:278-495`, the supersession checks at `:349-369` and `:420-426`, the override conflict at `:409-411`), and optionally by re-running the check, does the record bind after main's chain with your review's `supersededPassages`? Does any selected passage still conflict?
5. **Anything else wrong.**

## Output

Under `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r8/`. Do not commit, and run no cargo.
- **The law:** `REVIEW.md` and `review.json`, with:
  - `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"`: each with an id, a location, the problem or claim, the evidence and the fix;
  - `"nonBlockingObservations"`;
  - `"subjectSha256"`: `578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1`.
- **CRC-2:** `crc-2/REVIEW.md` and `crc-2/review.json`, separate from the law's, with:
  - `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
  - `"requiredFindings"`: a list, empty if you accept;
  - `"subjectManifestSha256"`: `58205eea17cee61d884d5e5475935653b5a9ee469aab31e1fde1db7df058c54f`, as one string;
  - `"supersededPassages"`: the list above, exactly, if you accept.

A CRC-2 acceptance binds nothing before the law is accepted. The law still takes effect only once M3-L is in effect, under its unchanged gate.

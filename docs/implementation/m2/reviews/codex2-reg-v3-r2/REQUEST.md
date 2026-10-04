Codex review: registry owner selection v3 r2, J-RW r4's successor RW-S2, round 2. It answers your RF-JRW-S2-1 from round 1 (`m2/reviews/codex2-jrw-successors-r1/registry-owner-selection-v3/review.json`).

This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**. If you accept, your `review.json` must carry `supersededPassages` (see below).

Write only under `/tmp/opensip-implementation/reviews/codex2-reg-v3-r2/`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- **No test, build or matrix run.** Don't run cargo or any lead set. Timing-sensitive lanes may be using this machine.
- You may read and re-run `evidence/verify_reg_v3_r2.py` only in your own throwaway detached worktree of product main, with a private 0700 TMPDIR, as the lead did (below). It is Python only and runs no cargo. Never run it in the main product checkout: it rewrites the worktree's `design-lock.json`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## The subject

Paths are under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/`. The subject and its members are untracked in arch until acceptance. The pins are in `hashes.txt`.

| Role | Path | sha256 | Bytes |
|---|---|---|---|
| **Subject manifest** (`subjectManifestSha256`) | `project-registry-owner-selection-v3-subject.json` | `f931f3155b9508450e900f14afcfc706ec7f0be253a7bbf880e1290fdbf0b8f9` | 455 |
| member: the README | `project-registry-owner-selection-v3/README.md` | `4de5f14f…` | 11,045 |
| member: the successor record | `project-registry-owner-selection-v3/successor.json` | `974ef73f…` | 14,684 |

**The diff base: r1's exact reviewed bytes,** kept as a record only in `project-registry-owner-selection-v3/r1-snapshot/`. They equal your round-1 pins: the manifest `0bd640d3…` (454 bytes), `README.md` `4ec39357…` (7,654) and `successor.json` `c6d860cf…` (12,684). They are not subject members. Diff each r2 member against its r1 copy.

## What r2 changes

Only what your fix states. Nothing else in r1 changes.
- **REG:9 is now a contract passage supersession,** in law VD2's form, as SD-7 first did (`m3/supervisor-d/sd-7/successor.json`; bound at product `d2c00a9`).
  - `supersedes` names the selected record `initial-root-binding-owner-selection-v1/successor.json` (IRB; `3a713c5c…`, 43,921 bytes) by exact pin, with its parent (v2's `owner.md`, `2d4b65c9…`) and its selector, `{"line": 9}`.
  - `before` is IRB's full selected `after` for REG:9: v2's raw line plus IRB's initial-root-binding sentences.
  - `after` is that same text, one space, then the J-RW append, which is r1's append unchanged. So every accepted initial-root sentence stays.
  - The entry has SD-7's shape: `parent`, `selector`, `before`, `after`, `supersedes`. Like SD-7, the record pins the superseded record in `supersedes`, not among its `parents`.
- **REG:60, :74 and :76** stay raw-parent overrides, byte-identical to r1's.
- **The README:** a new "r2 changes" section; the source table gains IRB; "What it changes" and its table now show three overrides and one supersession; V3-1 and V3-2 are updated; and "Binding" names `supersededPassages`. The appended text section is unchanged.
- **The record's standing text and the manifest pins** are updated. Parents, `candidates` (the README) and `inheritedSelectedRegistryRecord` keep r1's form.
- **Not done:** removing IRB's unit, or changing the verifier.

## The review must carry `supersededPassages`

`verify_design.py` refuses a contract passage supersession that its review does not list (`:420-426` at `d2c00a9`, VD2). So if you accept, `review.json` must contain `supersededPassages`, equal by value and in order to the record's `supersedes` list. The exact value:

```json
[{"record": {"path": "docs/implementation/m2/initial-root-binding-owner-selection-v1/successor.json", "bytes": 43921, "sha256": "3a713c5c39a3feca2db3a05924103d49c10f11bef3c32f93d8c286fecd813e54"}, "parent": {"path": "docs/implementation/m2/project-registry-owner-selection-v2/owner.md", "bytes": 32488, "sha256": "2d4b65c9b0bc088b2667c35e75bf82d1702d13703be6effb1df975e7c67c179f"}, "selector": {"line": 9}}]
```

## The lead's local binding check

The lead ran this check before sending. The script and its output are in `evidence/`, pinned.
- **Where.** A throwaway detached worktree of product main at `d2c00a9` (`/Users/sb/code/opensip-ai/opensip-regv3-check`, since removed), with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`. Python only, with no cargo.
- **How.** The worktree's own `tools/verify_design.py` (43,946 bytes, `7b313de6…`, byte-equal to `d2c00a9`'s) was loaded unchanged. The candidate entry was appended to the worktree's `design-lock.json`, with `SCRATCH-REGV3/review.json` and `assent.json` pins. As in F8c's and SD-7's scratch checks, an overlay of `pinned_bytes` serves those two placeholders from memory, so nothing was written to arch.
- **Results** (`evidence/local-binding-check.json`):
  - **Baseline:** the literal CLI, `python3 tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch`, on main's lock: passed, with 97 contract successors and 1 contract passage supersession (SD-7's).
  - **With v3 r2 appended:** PASS, both with the worktree as `implementation` and without it. There are 98 contract successors and 2 passage supersessions. v3 selects its README, its overrides are lines 60, 74 and 76, and its supersession is line 9. The inventory chain, inventory inheritance and supersessions, generation and admission sources, and verified inputs are equal to the baseline's.
  - **Refusals, each with one entry appended to main's lock:**
    - v3 r2 with a review that omits `supersededPassages`: "contract passage supersession is not listed by its review";
    - with an empty list: "contract review superseded passages differ from the record";
    - **r1's exact bytes:** "conflicting contract passage overrides". That is your RF-JRW-S2-1, now observed with the tool.
  - **The literal CLI on the appended lock** stops at "missing or escaping regular file: SCRATCH-REGV3/review.json". The placeholders are not files, so it fails closed, as for earlier units' SCRATCH pins. The overlay run above is the binding result.

## Pins

The pins are in `hashes.txt`: the subject and its members; r1's snapshot; your round-1 design-unit review and batch review; IRB's selected record, subject manifest, unit and review; v2's `owner.md` and `successor.json`; SD-7's record, unit and review, the form r2 mirrors; J-RW r4; and the two evidence files. Product files are read at `d2c00a9`:
- `design-lock.json`: IRB's binding at `:4051-4071`, which is the 55th contract successor (index 54). No other selected unit touches v2's `owner.md`.
- `tools/verify_design.py`: `contract_successor` (`:186-276`) and `successor_chain` (`:278-495`), with the supersession checks at `:348-369` and `:420-426`, and the override conflict at `:409-411`.

## Decide

1. **RF-JRW-S2-1.** Is it resolved exactly as your fix states?
   - Is REG:9 now a supersession naming IRB's exact record, parent and selector?
   - Does `before` equal IRB's selected `after` byte for byte?
   - Is `after` exactly that, one space, then r1's J-RW append?
   - Is all of IRB's initial-root text preserved?
2. **The rest of r1.** Are REG:60, :74 and :76 byte-identical to r1's overrides? Are the parents, candidates and `inheritedSelectedRegistryRecord` unchanged in form? Does the manifest cover exactly the two members?
3. **The README.** Are the r2 section, V3-1, V3-2, the change table and "Binding" accurate, and does anything else differ from r1?
4. **The binding.** By reading `verify_design.py` at `d2c00a9`, and optionally by re-running the lead's check in your own throwaway worktree, does the record bind after main's chain with your review's `supersededPassages`? Is there any remaining conflict with a selected passage?
5. **RW-S2.** Does v3 r2 still record exactly RW-S2 (JRW:680), and no more?
6. **Anything else wrong.**

## Output

Write REVIEW.md and review.json under `/tmp/opensip-implementation/reviews/codex2-reg-v3-r2/`. Do not commit. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: a list, empty if you accept;
- `"subjectManifestSha256"`: `f931f3155b9508450e900f14afcfc706ec7f0be253a7bbf880e1290fdbf0b8f9`;
- `"supersededPassages"`: the list above, exactly, if you accept;
- `"priorReviewDisposition"`: RF-JRW-S2-1's status.

Each required finding needs an id, a location, the problem, the evidence and the fix.

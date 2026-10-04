Codex review: **VD2 r1**, explicit supersession of a contract passage meaning in `tools/verify_design.py`. This is a **law** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS** on the law.

Write only under `/tmp/opensip-implementation/reviews/codex-vd2-r1`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation, and no messages to anyone.
- No cargo, product build, test lane, generator, Node or `check_typescript.py` run. The lead keeps the native lane.
- You may run the Python commands under "Checks", plain `tools/verify_design.py`, and read-only git (`show`, `diff`, `log`, `grep`, `apply --check`).
- Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and remove it when you finish. Write any `--json` output under your review directory, never into either repository.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the 413 fixture.

## Subject

- **The law:** `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, the r1 snapshot. Its sha256 is `subjectSha256`. The live `PROPOSAL.md` beside it has identical bytes at request time. Both are untracked in arch.
- **Reference evidence, not subjects:**
  - `reference/verify_design.prototype.diff` and `reference/verify_design.prototype.py`;
  - `evidence/run_existing_tests.py`, `fixture_controls.py` and `probe_real_lock.py`, with their four result files.

  The prototype is a feasibility patch, not VD2-a. VD2-a's diff and tests get their own tooling review later.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at `6190e66` (92 contract successors), read-only. The evidence scripts read the lock and tool at `6190e66` with `git show`, so they still reproduce if main moves.
  - **Main moved during drafting** to `3f6f9a5`, S21's binding. That commit changes `design-lock.json` only, giving 93 contract successors, and touches no NE passage and no file VD2 or F8c names.
  - **The drafter re-ran on `3f6f9a5`** (`probe_real_lock.py --rev 3f6f9a5`): all 17 cases are as expected, SD-7 r2 binds (93 to 94), and its effective NE is still NE7. The prototype's output on that lock equals the `3f6f9a5` tool's apart from the count.
  - **If main has moved again,** run the probe with `--rev` at the current main as well.
- **Pins:** `hashes.txt` pins the subject, this request, the evidence and the context files.

## Context

Read these first:
- **Binding v4's rule**, `m1/trials/binding4-01/subject/UNIT.md:10-11`: "Differing meanings for the same physical passage refuse; no implicit last-writer-wins rule."
- **VD1**, the inventory-description profile: `m2/verify-design-vd1/PROPOSAL-r1.md`, and Grok's review `m2/reviews/grok-verify-design-vd1-r1/REVIEW.md` (calls 1 to 8) with its `review.json`.
- **The tool at `6190e66`**, `tools/verify_design.py`:
  - `contract_successor`, :186-275. The override's raw-`before` check is at :250-251, and VD1's shape checks at :252-273.
  - `successor_chain`, :278-452. VD1's state is at :333-335, its classification refusal at :342-345, and the override conflict at :381-383.
- **F8b**, `m2/generator-closure-f8b/PROPOSAL-r2.md` (accepted) and the unit's `README.md`. They show why the closure and lane registry pin `verify_design.py` ("Problem"), F8b's decision 5, and which of F8b's steps came from its `Cargo.toml` licence line.
- **The product's pins:**
  - `tools/contracts/generator-closure.json:1746-1748` and `tools/typescript-lanes.json:804-806`;
  - `tools/contracts/adapter.py:10-37`, the receipt join;
  - `tools/generate_contracts.py:38-83`, closure selection.
- **The SD-7 case:**
  - `m3/supervisor-d/PROPOSAL-r5.md:1182`, which leaves SD-7's form to its drafter;
  - SD-5's record `m3/supervisor-d/sd-5/successor.json`;
  - SD-7 r1, drafted and held, never sent: `m3/supervisor-d/sd-7/README.md` ("The form", LD-7.1, LD-7.2), `sd-7/successor.json`, `sd-7/evidence/verify_scratch.py`, and NE7 `sd-7/contracts/native-evidence.md`.
- **The other copy cases:**
  - `m3/config-discovery-b/b-s9/README.md` (LD-1, LD-4);
  - `m2/config-remedy-x12-0/successor.json`;
  - `m3/snapshot-plan-c/cr-1/README.md` (LD-2, LD-5).
- **Closure serialization:** `m3/preview-pack-i1/i1-a/README.md:92`. This is a unit draft now with CODEX2, so it is context only.

## What the law decides

**The mechanism (items 1 to 6).** VD1's `passageSupersessions` entry shape may now carry a **contract passage supersession**: one whose `parent` is not an inventory pin of the lock's chain. VD1's inventory entries are unchanged. `verify_design` refuses one unless all of the following hold:
- **Shape:** VD1's closed shape.
- **Target:** `supersedes.record` is the exact record pin of a strictly earlier bound contract successor, and that record holds an entry with exactly `supersedes.parent` and `supersedes.selector`.
- **The same passage:** the link's parent and selector equal the named ones, and the meaning is never projected.
- **Chain:** `before` equals the named entry's `after`.
- **Linear per passage:** the first link names a root override (any identical copy of it), and each later link names the tail.
- **No restatement:** a later override of a superseded passage refuses, even an identical one.
- **Review listing:** the record's review.json carries `supersededPassages`, which equals the record's `supersedes` list. It is required when the record has a contract link, and must be exact whenever it is present.

The result gains a `contractPassageSupersessions` count. There is no lock change. The effective text is the tail's `after`, and item 4 gives consumers a lock-order fold.

**Units (item 7).**
- **VD2-a:** the tool and its tests. One VD1 test is rewritten.
- **F8c:** the closure and lane-registry re-pin, with no rebuild.
- **One product commit** for VD2-a and F8c.
- **SD-7 r2:** the clean form, superseding SD-5's NE:3540 entry and overriding the free NE:3539.

**Item 8.** B-S9's copies stay. From VD2-a on, supersession is the default, and copies are kept only where a supersession cannot reach.

## Checks run by the drafter

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, with `PATH=/opt/homebrew/bin:/usr/bin:/bin` and a private 0700 `TMPDIR`. Each was made twice, with byte-identical output. From `docs/implementation/m3/verify-design-vd2/`:

1. **`evidence/run_existing_tests.py`.** The product's 83 design-binding tests at `6190e66`, each run in a fresh private tree. They pass 83 of 83 on the `6190e66` tool. On the prototype, 82 pass. The one failure is the expected inversion, `PassageSupersessionTests.test_supersession_of_non_inventory_passage_refuses`: its first half now reaches "contract passage supersession is not listed by its review" (law item 7, VD2-a).
2. **`evidence/fixture_controls.py`.** The law's 40 controls, P1 to P8 and N1 to N15, on the product fixture `Fx`: **40 of 40** as expected.
   - With `--base-tool` (the `6190e66` tool), all 8 positive controls and 19 negative ones refuse with "passage supersession must select an inventory row description".
   - The other negative controls refuse as under the prototype, except N11e, which carries no supersession and passes.
3. **`evidence/probe_real_lock.py`.** The real lock plus in-memory synthetic successors, 17 cases, **all as expected**:
   - **R0, the real lock.** Every output field equals the `6190e66` tool's. The only addition is `contractPassageSupersessions: 0` (92 contracts, 100 inheritance rows, 21 VD1 links).
   - **R1, SD-7 r2's clean form,** binds: 93 contracts, count 1. The `6190e66` tool refuses it.
   - **R1's effective NE,** folded independently in lock order, is 380,848 bytes, `0dd155c2…`: **equal to SD-7 r1's NE7.** The fold at `6190e66` gives SD-7 r1's recorded effective parent, `03b498b7…`.
   - **R2 to R16:** a second link binds. A wrong record sha, an unbound byte-identical copy of SD-5's record, SD-7 r1's unbound record, an absent entry, another passage, a stale `before`, a double supersession, a restatement, a second override, a missing or a wrong review list, and a reversed order all refuse with the law's messages. The B-S9 shape and a JSON Pointer link (CR-1's) bind.
4. **Plain `verify_design` on the real lock, with and without `--implementation`,** passes on both tools with identical fields apart from the count. The `--implementation` run verifies 40 generation sources, 48 admission sources and 15 aliases.
5. **The prototype diff applies:** `git -C /Users/sb/code/opensip-ai/opensip apply --check` passes on `6190e66`.

**To reproduce,** with `R=/tmp/opensip-implementation/reviews/codex-vd2-r1`:
```sh
PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14
cd /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/verify-design-vd2
nice -n 19 $PY -I -B evidence/run_existing_tests.py --json $R/existing-tests.json
nice -n 19 $PY -I -B evidence/fixture_controls.py --json $R/fixture-controls.json
nice -n 19 $PY -I -B evidence/fixture_controls.py --base-tool --json $R/fixture-controls-6190e66.json
nice -n 19 $PY -I -B evidence/probe_real_lock.py --json $R/probe-real-lock.json
```
Each result file should equal its copy in `evidence/` byte for byte (`cmp`). For the plain runs, pass `--lock` explicitly to the prototype: its default lock path is relative to its own location.

## Judgment calls: rule on each

1. **Classification by parent (item 1).** An inventory pin of the chain gets VD1's rules, and every other accepted file gets VD2's. Is the inventory chain the right boundary?
2. **The same passage only, never projected (check 2.3).** Rejected: projecting a contract meaning onto a successor copy.
3. **The root and linearity (checks 2.5 and 2.6).**
   - The first link may name any identical copy of the root.
   - After that, an identical copy refuses as a double supersession, and an identical restatement refuses as "restates a superseded contract meaning".
   - A different later override keeps binding v4's "conflicting contract passage overrides".
4. **Review coverage is tool-checked (check 2.7, lead decision).** This is how the law makes the review "explicitly cover" each supersession.
   - The list is required for a record with a contract link, must be exact whenever present, and lists every link in a mixed record.
   - It is not retroactive for VD1's inventory links: D2's and D3's bound reviews lack it.
   - Rejected: coverage by the subject hash alone; putting the list in the root assent.
   - Is a new review.json field the right enforcement, and is its shape (the exact `supersedes` objects, in record order) right?
5. **The output is a count only (item 3).** The effective text is defined in the law (item 4), not emitted. Rejected: emitting it for all 264 overridden passages.
6. **No lock change (item 3).** Contract links never enter `inventoryPassageInheritance`.
7. **Copies stay lawful, and supersession is the default (items 5 and 8).** Are the three places where copies remain the form stated correctly?
8. **VD2-a and F8c in one product commit (item 7, lead decision).** Rejected: VD2-a first with EXIT-PLAN debt; folding the re-pin into VD2-a.
9. **F8c's scope ("F8c").** It re-pins four product files and makes no rebuild, because `verify_design.py` is not a build input. Check this against `adapter.py:10-37` and `generate_contracts.py:38-83`, and check F8c's serialization with I1-a.
10. **SD-7 r2 ("SD-7 r2").**
    - The form: a supersession of SD-5's NE:3540, an override of NE:3539, and SD-5 not a parent.
    - Its effective NE equals NE7 byte for byte, so only the form changes from r1.
    - Its binding order fails closed.
    - The held `grok-sd-7-r1` request is withdrawn unsent.
11. **B-S9's copies stay (item 8, lead decision).** Rejected: a retirement successor; unbinding; a `verify_design` selection rule.
12. **One VD1 test is rewritten in VD2-a (item 7).** Its first half becomes VD2's positive case.

## Decide

- **Soundness.** Is the rule sound under binding v4? Does any last-writer-wins path remain?
- **Gaps.** Under the rules as written, can a stale `before`, a fork, a restatement, a wrong or unbound target, a cross-passage link or a silent change pass?
- **Completeness.** Are items 1 to 8 complete and unambiguous enough for VD2-a to implement without further decisions?
- **Controls.** Are the controls sufficient? Name any case VD2-a's tests must add.
- **Rejected alternatives.** Are they right?
- **The estimates and decisions.** Are the F8c estimate, the SD-7 r2 form and the B-S9 decision right?
- **Anything else.**

The prototype is evidence, not a subject:
- a prototype defect that shows a gap in the law is a finding against the law;
- a prototype-only defect is an observation for VD2-a.

## review.json

review.json needs:
- `"verdict"`: `"ACCEPT"` or `"REQUIRED-FINDINGS"`;
- `"requiredFindings"`: each with `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"judgmentCalls"`: an object keyed `"1"` to `"12"`, each `"ACCEPT"` or the id of a finding;
- `"subjectSha256"`: `PROPOSAL-r1.md`'s sha256;
- `"productHead"`: `6190e66cdc6e6de5816cefc2887661ab08d47515`.

This is a law review, not a `verify_design`-selected unit. So it carries no `subjectManifestSha256` and no `inventoryCandidateAssessment`. Later reviews:
- **VD2-a:** a tooling review on its own `subject.diff`.
- **F8c and SD-7 r2:** `ACCEPT-DESIGN-UNIT` reviews, each with a single `subjectManifestSha256`. SD-7 r2's review will also need `supersededPassages`.

Write REVIEW.md and review.json. Do not commit.

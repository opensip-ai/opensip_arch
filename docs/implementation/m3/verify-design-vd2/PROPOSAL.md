# Explicit supersession of a contract passage meaning — proposal VD2 r1

**r1 ACCEPTED 2026-10-04 by Codex** (`2e4f70b4…`; `reviews/codex-vd2-r1/`), with no required findings. r1's bytes, without this note, are preserved in `PROPOSAL-r1.md`. Next: VD2-a and F8c as one product commit, then SD-7 r2.

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** Law for unit VD2, the `verify_design` successor the lead decided on when SD-7 was held (overnight log, "SD-7 drafted but held"). It amends how `tools/verify_design.py` judges a v4 design lock. So it amends design binding v4 (`m1/trials/binding4-01/subject/UNIT.md`, accepted by review binding4-01) and VD1 r1 item 4 (`m2/verify-design-vd1/PROPOSAL-r1.md`, accepted by Grok). Items 1, 2.7, 5, 7 and 8 contain lead decisions, made under the owner's standing direction to proceed on the lead's recommendation and record it. Not runtime law: `verify_design` stays a developer provenance check and grants no product trust.

**Product.** Main `6190e66` (SYN-NS's binding), read only. Its lock binds 95 inventory successors (v135 selected), 92 contract successors, 264 passage overrides, 100 inheritance rows and 21 VD1 supersessions (D2's 4 and D3's 17).

## Short names

| Name | Document |
|---|---|
| **VD** | `tools/verify_design.py` at `6190e66` (40,714 bytes, `c13d231e…`; VD1's bytes) |
| **VD1** | `docs/implementation/m2/verify-design-vd1/PROPOSAL-r1.md`, accepted (`c46828c5…`) |
| **F8B** | `docs/implementation/m2/generator-closure-f8b/PROPOSAL-r2.md`, accepted (`cf7e1183…`), executed and bound at `e093e90`; its unit README `generator-closure-f8b/README.md` |
| **MD5** | `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, M3-D r5, accepted (`224b9228…`) |
| **SD5** | `docs/implementation/m3/supervisor-d/sd-5/successor.json`, bound (5,805 bytes, `5e115818…`) |
| **SD7** | `docs/implementation/m3/supervisor-d/sd-7/`, SD-7 r1, drafted and held, never sent; NE7 is its `contracts/native-evidence.md` (380,848 bytes, `0dd155c2…`) |
| **BS9** | `docs/implementation/m3/config-discovery-b/b-s9/`, bound at `8adfe0c` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes, `83b99783…`) |

## Problem

Binding v4 fixed one rule for passage meanings: "Differing meanings for the same physical passage refuse; no implicit last-writer-wins rule" (UNIT.md:10-11). VD1 opened one explicit, reviewed and linear way to change a meaning, for inventory row descriptions only. Its item 4 kept every other passage under binding v4: "a different meaning refuses."

So a bound contract text meaning cannot be changed at `6190e66`. Every route refuses:
- **A second override** of the same parent and selector: "conflicting contract passage overrides" (VD:381-383). Only an identical restatement passes.
- **An override whose `before` is the effective text:** "passage override before text differs from accepted parent" (VD:250-251). An override's `before` must be the raw parent passage.
- **A VD1 supersession** of the bound entry: "passage supersession must select an inventory row description" (VD:342-345).
- **An erratum on a neighbouring line** leaves two meanings for one route: a contradiction plus a precedence note, not a correction (SD7 README, "Why not (i)").

The only lawful route left is a complete successor copy at a new path, selected by the record's `standing`. Tonight this forced three workarounds:
- **B-S9:** complete copies of both 320 KB native-model files to change line 1158, because X12-0 already overrode it (BS9 LD-1).
- **CR-1's schema copy:** related, but not this problem. CR-1's completed manifest schema is not an accepted `verify_design` parent, and its `role` change widens an enum, which is not a text value. JSON copies remain the form for that (item 5).
- **SD-7 (held):** correcting SD-5's bound NE:3540 row took NE7, a 380,848-byte copy of NE, which would become the selected NE. Its lines drift from the original from line 123 on, while every accepted law cites NE by original line. Every later NE successor would have to override NE7, and `verify_design` cannot enforce that (SD7 probe 3c; BS9 LD-4's residual hazard).

The lead's decision (overnight log, 2026-10-04) is to fix the tool rather than keep paying the copy cost.

## Rule

1. **Contract passage supersession (lead decision).** A contract successor record's `passageSupersessions` (VD1's field and entry shape: `parent`, `selector`, `before`, `after`, and `supersedes` with exactly `record`, `parent` and `selector`) may carry an entry whose `parent` is **not an inventory pin of the lock's inventory chain**. Such an entry is a **contract passage supersession**.
   - It replaces exactly the meaning it names, of the same physical passage, and nothing else.
   - An entry whose parent is an inventory of the chain is VD1's and keeps VD1's rules unchanged.
   - The inventory chain is binding v4's projection boundary, so classifying by parent is exact. At `6190e66` the chain has 96 inventory pins, v1 to v135. Every other accepted file is a contract parent: contract text, JSON contracts such as `command-inventory.v3.json`, successor copies, and the members of earlier successors.
2. **Checks.** `verify_design` refuses a contract passage supersession unless every one of these holds, checked in lock order:
   1. **Shape (unchanged; VD:252-273).** Its fields are closed. Its `parent` is one of its record's accepted parents. Its selector resolves in that parent. `after` is a non-empty string that differs from `before`. No two overrides or supersessions in one record share a parent and selector.
   2. **A named, bound, earlier target.** `supersedes.record` equals exactly (path, sha256 and bytes) the record pin of a contract successor that comes strictly earlier in `contractSuccessors`. That record is therefore accepted (its review and assent passed `contract_successor`) and bound in this lock. It contains an entry, an override or a supersession, with exactly `supersedes.parent` (the full pin) and `supersedes.selector`.
   3. **The same passage.** The supersession's `parent` equals the named `parent` (the full pin), and its selector equals the named selector (canonical JSON). A contract meaning is never projected to another file.
   4. **Chain.** `before` equals the named entry's `after`, byte for byte. It is never compared with the raw parent bytes.
   5. **Linear.** For each passage (parent path, selector), the supersessions in lock order form one chain:
      - the first link names an ordinary override of that passage, the **root**. Binding v4 allows only identical copies of a root, so any record's copy may be named;
      - each later link names the link immediately before it, the **tail**.

      Anything else refuses as a double supersession. That covers superseding the root a second time, naming a link that is no longer the tail, and starting again from an identical root copy. Two links for one passage in one record refuse under check 1.
   6. **No restatement.** Once a passage has a supersession, an ordinary override of it in a later record refuses, even if it is identical to the root ("passage override restates a superseded contract meaning"). A different override still refuses as a conflict, under binding v4's unchanged rule. In the same record as the link, either override refuses under check 1.
   7. **Explicit review (lead decision).** The record's review document carries `supersededPassages`: a list equal, by value and in order, to the `supersedes` objects of all the record's `passageSupersessions`.
      - It is **required** whenever the record carries a contract passage supersession.
      - A review that carries it on **any** record must match exactly. So a list that names a passage the record does not supersede refuses.
      - This is in addition to the `ACCEPT-DESIGN-UNIT` verdict, the `subjectManifestSha256` and the root assent, which already pin the record's bytes.
3. **Determinism.** One pass in lock order, using VD1's state (`published` entries and `earlier_records` pins) plus a tail for each superseded passage. The outcome depends only on the lock and pinned bytes, and the first failing check in lock order decides the refusal.
   - **Output.** The result gains a top-level `contractPassageSupersessions` count. Each contract result already lists its `passageSupersessions` (VD1).
   - **No lock change.** No lock field is added. The lock stays schema version 4 with VD1's fields and order. A contract passage supersession never enters `inventoryPassageInheritance`.
4. **Effective text.** The effective text of a passage (P, S) under a lock is P's raw passage if no bound override names it. Otherwise it is the root's `after`, superseded through its chain in lock order: the tail's `after`.
   - **How a consumer computes it.** Any script that builds an effective parent (B-S9's and SD-7's builders are examples) visits the lock's contract successors in order. For each override and supersession on P, it sets S's text to that entry's `after`.
   - **Why that fold is safe.** `verify_design` has already refused every fork, stale `before` and restatement, so the fold yields the tail. It is not a last-writer-wins rule: every later writer was checked to name its predecessor and match its text.
   - **Line selectors.** A line selector always indexes the raw parent. An `after` may span lines, and a superseded multi-line meaning is replaced whole.
   - **Reverting.** A link may restore the raw passage: its `after` is then the raw text.
5. **Everything else unchanged (lead decision).**
   - **Refusals.** Every existing refusal stands, with its message. One rule is narrowed: VD1's "passage supersession must select an inventory row description" now applies only when the parent is an inventory of the chain. This is the amendment to VD1 item 4's second bullet.
   - **Binding v4.** Binding v4's no-last-writer-wins rule holds: a second, different override still refuses. Only a named, reviewed, linear supersession changes a bound meaning, which is the reading Grok's VD1 review gave binding v4 for inventory descriptions ("Why the rule is binding v4's").
   - **VD1 unchanged.** VD1's inventory rules, projection, fold and `inventoryPassageInheritance` are unchanged.
   - **Text values only.** Overrides and supersessions still change one text value. A JSON parent still needs a JSON Pointer selector. This holds by construction, because a link's selector is its root's, and the root passed that check.
   - **Earlier lock versions.** A version 1 to 3 lock refuses any supersession (unchanged).
   - **The record's field set stays open** (VD1 call 6).
   - **Copies stay lawful.** VD2 adds a route and removes none.
6. **Standing.** A supersession changes which reviewed text a passage means. It never changes parent bytes, inventory bytes, generation or admission sources (which `verify_design` compares raw), package edges, roles, ownership or runtime trust. `verify_design` still executes no generator or product code.
7. **Units after the law (lead decision).**
   - **VD2-a: the tool change.** It changes `tools/verify_design.py` and `tools/tests/test_design_binding.py` only, and is reviewed as a tooling diff, like VD1-a.
     - **Tests.** A `ContractPassageSupersessionTests` class carries the controls below. VD1's `test_supersession_of_non_inventory_passage_refuses` is rewritten: its first half (a supersession of a JSON contract passage) is now VD2's positive case, and its second half (an inventory link that names a contract meaning) stays.
     - **No inventory successor.** No file is added, and v135's descriptions of both files stay true ("Verify design input bytes and the bound approval chain…"; "Refuse changed, unreviewed, duplicate, escaping or cross-subject design bindings").
     - **The real lock** must verify with output identical to `6190e66`'s, apart from `contractPassageSupersessions: 0`.
   - **F8c: the generator-closure and lane-registry re-pin onto VD2-a's bytes,** by F8b's method without the rebuild. See "F8c".
   - **One product commit (lead decision).** VD2-a's two files, F8c's materialized files and F8c's lock row land together. This meets F8B decision 5 ("must carry the matching re-pin successor"), and no product commit exists in which `generate_contracts.py` or `check_typescript.py` refuses on a stale `verify_design.py` pin.
   - **SD-7 r2: the clean form.** See "SD-7 r2".
   - **B-S9's copies: no clean-up unit.** See item 8.
8. **B-S9's copies stay (lead decision).**
   - **Why they stay.** B-S9's copies are bound, accepted and lawful. They changed one line in place, so their line numbers equal their parents'; there is no citation drift, unlike NE7. They are now the selected native reference: SD-7's draft overrides their line 1159, FA1-F1 (owed) overrides other lines of the same copies, and B1-a depends on them.
   - **What retiring them would cost.** A successor would have to re-select the historical files by superseding X12-0's two line-1158 overrides with B-S9's text. SD-7's line-1159 overrides would then be on unselected files and would have to be restated. That is two selection flips for no change of meaning.
   - **The default from VD2-a's integration on.** A later change to a bound text passage uses a supersession, not a complete copy. Copies remain the form where a supersession cannot reach:
     - a parent that is not an accepted `verify_design` input (CR-1's completed manifest schema);
     - a change that is not one text value (an enum or array append, a boolean: I1-L LD-L1, CR-1);
     - bytes that a product generator reads (I1-L's schema sources).

## Controls

VD2-a's tests carry these, on the product's own fixture (`Fx`). They mirror VD1's `PassageSupersessionTests` for a contract passage. The prototype runs all 40 (`evidence/fixture_controls.py`, below), and each gives its expected outcome. Fixture: c2 overrides `doc.md` line 2, `L2` to `L2a`, which is the root.

| # | Case | Expected |
|---|---|---|
| P1 | a line supersession of c2's override | binds; `contractPassageSupersessions` 1; inventory output unchanged |
| P2 | a JSON Pointer supersession of a contract override | binds |
| P3 | a chain of two: the second link names the first | binds; count 2 |
| P4 | the first link names an identical root copy in another record | binds |
| P5 | one record with a VD1 inventory link and a VD2 contract link, the review listing both | binds; 1 and 1 |
| P6 | a link restoring the raw text | binds |
| P7 | a multi-line meaning, superseded whole | binds |
| P8 | two passages superseded in one record | binds; count 2 |
| N1 | stale `before`: the raw parent text | "before text differs from the superseded meaning" |
| N2 | stale rebind: names the tail with the root's text | the same |
| N3 | the root superseded twice | "double supersession" |
| N4 | a second start from an identical root copy | "double supersession" |
| N5 | a fork from a link that is no longer the tail | "double supersession" |
| N6a–d | missing chain: an unbound record; a wrong record sha; no such entry in the named record; a wrong parent pin | "not an earlier contract successor" (a, b); "not in the named record" (c, d) |
| N7 | the named record is later in the lock | "not an earlier contract successor" |
| N8a–c | another passage: another line of the same parent; an identical passage on another parent; an inventory meaning named from a contract parent | "selects a different passage" |
| N9a | a later override restating the root | "restates a superseded contract meaning" |
| N9b | a later override restating the tail's text | "conflicting contract passage overrides" (binding v4, unchanged) |
| N10 | an override and a supersession of one passage in one record | "duplicate passage override" |
| N11a–e | review coverage: no `supersededPassages`; a different passage; the record's list out of order; a mixed record that omits the inventory link; a list on a record with no supersession | "not listed by its review" (a); "superseded passages differ from the record" (b–e) |
| N12a, b | VD1 unchanged: an inventory parent with a non-description selector; an inventory link naming a contract meaning | VD1's messages |
| N13a, b | silent change: an override whose `before` is the effective text; a second, different override | the existing messages |
| N14 | six malformed shapes (unknown field, unknown `supersedes` field, empty `after`, `after` equal to `before`, a parent outside the record's parents, a selector outside the document) | `contract_successor`'s existing messages |
| N15 | a version 3 lock carrying any supersession | "require a v4 successor chain" |

## Prototype evidence (reference only)

The prototype is a patch of a scratch copy of VD. It is **not** VD2-a's subject: VD2-a writes and reviews its own diff and tests. The patch adds 39 lines and changes one (the return statement, which gains the count), and edits no existing refusal.

| File | What it is |
|---|---|
| `reference/verify_design.prototype.diff` | the patch against `6190e66` (`git apply --check` clean on main) |
| `reference/verify_design.prototype.py` | the patched file (43,678 bytes, `9354b171…`) |
| `evidence/run_existing_tests.py` → `existing-tests.json` | the product's 83 design-binding tests at `6190e66` against VD and against the prototype, each in a private temporary tree |
| `evidence/fixture_controls.py` → `fixture-controls.json`, `fixture-controls-6190e66.json` | the 40 controls above, on the prototype and (`--base-tool`) on VD |
| `evidence/probe_real_lock.py` → `probe-real-lock.json` | the real lock plus in-memory synthetic successors, on both tools |

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, with `PATH=/opt/homebrew/bin:/usr/bin:/bin` and a private 0700 `TMPDIR`. Each run was made twice, with byte-identical results.

**The current lock (92) passes unchanged.**
- Plain and `--implementation` runs on the real lock both pass with 92 contract successors, 95 inventory successors, 100 inheritance rows and 21 VD1 supersessions. The `--implementation` run also verifies 40 generation sources and 48 admission sources with 15 aliases.
- Every field equals VD's output; the only addition is `contractPassageSupersessions: 0`.
- **Existing tests:** at VD, 83 pass. With the prototype, 82 pass. The one failure is the expected inversion, `test_supersession_of_non_inventory_passage_refuses`: its first half now reaches "contract passage supersession is not listed by its review".

**The SD-7-style supersession binds; malformed ones refuse** (`probe_real_lock.py`, 17 cases, all as expected):

| Case | Prototype | VD at `6190e66` |
|---|---|---|
| R0 the real lock | PASS, 92, count 0, same output | PASS |
| R1 **SD-7 r2's clean form**: SD-5's NE:3540 superseded; NE:3539 overridden; the two NEM line-1159 overrides | **PASS**, 93, count 1; inheritance and VD1 count unchanged | REFUSED: "must select an inventory row description" |
| R2 a second link naming R1 | PASS, 94, count 2 | REFUSED (the same) |
| R3 SD-5 named with a wrong record sha | REFUSED: "not an earlier contract successor" | REFUSED |
| R4 a byte-identical copy of SD-5's record at an unbound path | REFUSED: "not an earlier contract successor" | REFUSED |
| R5 SD-7 r1's draft record (in arch, not bound) named | REFUSED: "not an earlier contract successor" | REFUSED |
| R6 SD-5 named at NE:3541, which it does not override | REFUSED: "not in the named record" | REFUSED |
| R7 an NE:3540 link naming SYN-1's NE:3541 meaning | REFUSED: "selects a different passage" | REFUSED |
| R8 stale `before`, the raw NE:3540 | REFUSED: "before text differs" | REFUSED |
| R9 SD-5 superseded twice | REFUSED: "double supersession" | REFUSED |
| R10 SD-5's row restated as an override after R1 | REFUSED: "restates a superseded contract meaning" | REFUSED |
| R11 a second override of NE:3540 (SD7 probe 2a) | REFUSED: "conflicting contract passage overrides" | REFUSED (the same) |
| R12, R13 R1 with no review list; with a wrong list | REFUSED: "not listed"; "differ from the record" | REFUSED |
| R14 R1 bound before SD-5 | REFUSED: "not an earlier contract successor" | — |
| R15 the B-S9 shape: X12-0's line 1158 on the capability-totality copy, superseded (illustration only) | PASS, count 1 | REFUSED |
| R16 a JSON Pointer link: CR-1's DR-103 `fields/7/semantics` superseded | PASS, count 1 | REFUSED |

**R1's effective NE is NE7, byte for byte.** The probe folds every bound entry on NE in lock order (item 4), independently of the tool: SD-7 r2's two entries plus the 39 bound overrides, 41 entries over 40 passages. The result is 380,848 bytes, `0dd155c2…`, equal to SD-7 r1's complete copy. At `6190e66` the same fold gives 378,351 bytes, `03b498b7…`, which is SD-7 r1's recorded effective parent. So the clean form carries r1's reviewed meaning exactly, with no copy, no selection change and no line drift.

**Binding order fails closed.** VD refuses every case whose contract passage supersession reaches the chain: all 8 positive fixture controls, 19 negative ones (N1 to N9b, N11a to N11d) and every synthetic R case, with "passage supersession must select an inventory row description". The other negative controls refuse at VD exactly as under the prototype, by the shape, version, VD1 and binding v4 checks, except N11e: it carries no supersession, and VD ignores the review field (`fixture-controls-6190e66.json`). This is unlike VD1, whose old tool silently ignored the new field (VD1 item 6, "Binding order"). An early SD-7 r2 binding therefore cannot pass unchecked.

## F8c (scope estimate)

**Why it is needed.** VD2-a changes VD's bytes, and exactly two product files pin them: `tools/contracts/generator-closure.json:1746-1748` and `tools/typescript-lanes.json:804-806` (`git grep c13d231e`). Until they are re-pinned, `generate_contracts.py` refuses ("input digest mismatch: tools/verify_design.py") and so does `check_typescript.py`. Both pins are deliberate, because both entry points execute VD as their preflight (F8B "Problem").

**Why it is much smaller than F8b.** F8b's rebuild, receipt, executable comparison and equivalence probe were all caused by its licence line in `tools/contracts/Cargo.toml`: the receipt's `sources` must equal the closure's `Cargo.toml` (`adapter.py:21-22`). VD is not a build input. So F8c changes no receipt, no toolchain and no generator executable: rebuild-02, `4647471c…`, stays selected. BS9 LD-1 and SD7 LD-7.1 each assumed "another generator rebuild … on F8b's scale". That overstates it.

| # | Product file | Change |
|---|---|---|
| 1 | `tools/contracts/generator-closure.json` | the one `tools/verify_design.py` row, to VD2-a's bytes; the other 348 rows and the toolchain block unchanged; same length while the byte count keeps five digits |
| 2 | `schemas/registry.json` | `recipes[0].generatorClosureSha256` only; same length |
| 3 | `apps/report/src/generated/report.ts` | header lines 2 and 3 (the registry and closure digests); same length |
| 4 | `tools/typescript-lanes.json` | the one `tools/verify_design.py` row; same length |
| 5 | `design-lock.json` | one `contractSuccessors` row, at integration |

**Steps,** from F8B's ten:
- **Kept:** 1 (worktree at main plus VD2-a's accepted diff, with the 268 provisioned closure pins checked); 4, reduced to three files; 5 (generation with rebuild-02 and an in-memory approval, where seven outputs must be byte-identical and `report.ts` may differ in lines 2 and 3 only, then the public drift gate); 8 (lane-registry replay to selection and the 12 tracked rows); 9 (the design check, with VD2-a's tool and `contractPassageSupersessions` 0); 10 (freeze).
- **Dropped:** 2 (rebuild), 3 (executable comparison), 6 (equivalence probe) and 7 (npm), together with the licence manifests.

**Shape.**
- **Scripts.** Six, adapted from F8b's (`apply_pins`, `run_generation`, `drift_scratch`, `typescript_scratch`, `verify_scratch`, `freeze`): about 350 lines, mostly constants.
- **Record.** Parents are the currently selected copies: F8b's `product/` closure, registry, `report.ts` and lane registry, and F8b's `reference/tools/verify_design.py` (40,714 bytes, `c13d231e…`, an accepted F8b subject member). The candidates are the four after-copies plus `reference/tools/verify_design.py` with VD2-a's bytes. The provenance is recorded as F8b recorded VD1's: VD2-a's tooling review `subject.diff`, applied to the parent, gives the candidate exactly.
- **No inventory successor.** No passage overrides.
- **Review.** One `ACCEPT-DESIGN-UNIT` review that reruns generation, drift, the lane replay and the design check.
- **Size.** **S.** Roughly one to two hours of lead work and one review round. No cargo. Node and the generator run only inside the sandboxed generation step.

**Serialization (cross-law X-VD2-4).** I1-a, now with CODEX2, also changes the closure (`bb093a9c…` to `9dc40660…`), `registry.json` and `report.ts`. Its README says only one closure writer may be in flight against a given closure (I1-a and X4T-c). So F8c is frozen on the closure selected at its freeze. If I1-a binds first, F8c's parents for those three files are I1-a's copies. On `6190e66` they are F8b's, which still equal the product bytes.

## SD-7 r2 (the clean form)

SD-7 r2 is a fresh draft, built on the lock after VD2-a and F8c. MD5:1182 leaves SD-7's form to its drafter: "B-S9's complete-copy form or a `verify_design` successor". Probe R1 is its shape:
- **Parents:** NE (raw, `83b99783…`) and B-S9's two model copies. SD-5's record need not be a parent, because `supersedes.record` names it exactly.
- **`passageSupersessions`:** NE:3540, naming SD-5's record (5,805 bytes, `5e115818…`), NE and `{"line": 3540}`. `before` is SD-5's two-line `after`. `after` is the raw NE:3540 release-declaration row, then SD-7's conformed row.
- **`passageOverrides`:** NE:3539, a fresh key that no bound successor overrides. `after` is the raw NOT-SELECTED row, then item 25's row. SD-7 r1's two line-1159 overrides of the NEM copies are unchanged.
- **Review:** `ACCEPT-DESIGN-UNIT`, `subjectManifestSha256`, and `supersededPassages` naming SD-5's NE:3540 entry.

**What changes from r1.**
- There is no NE7. NE stays the selected NE, the line map and X-SD7-NE are dropped, and the NE residual hazard disappears.
- LD-7.1 now chooses form (iii) and rejects (ii) for its citation drift and its unenforced selection. Its objection to an NE:3539 override falls away, because NE is no longer made historical.
- LD-7.2 (the copy is NE's effective text) is replaced by item 4's check: r2's effective NE must equal r1's NE7 byte for byte, as probe R1 shows. Reviewer point R4 becomes that check.
- LD-7.3 to LD-7.6 and reviewer points R2 and R3 carry over unchanged, because the texts are r1's.

**Binding.**
- SD-7 r2 binds only after the VD2-a and F8c commit; before it, it fails closed.
- The held request `reviews/grok-sd-7-r1/` is withdrawn unsent.
- Timing is MD5's: (b) before J2a projects item 25's refusal, and (a) recommended before D4's integration review.

## Rejected alternatives

- **Last writer wins for contract passages.** Binding v4 forbids it, and a stale `before` would rebind unseen.
- **An override whose `before` may be either the raw or the effective text.** Which meaning it replaces would be ambiguous, and a raw match would silently start a second root (VD1's reasoning).
- **An implicit chain,** matching `before` against the effective text without naming the target. The record would not say which accepted meaning it ends, and here that meaning is often another law's successor. A stale pin should refuse at the named target.
- **Projecting a contract meaning onto a successor copy,** so that a link on a copy names a meaning on the original. Binding v4 defines projection only for inventory rows, by stable file path, and text has no stable row key. It would also keep copies as the default.
- **A supersession list in the lock.** The lock pins reviewed content; it does not author it.
- **Coverage by the subject hash alone** (VD1's standard). A contract supersession can end another law's bound meaning, so the reviewer states each one and the tool checks it (check 2.7).
- **Requiring `supersededPassages` for VD1's inventory links as well.** D2's and D3's bound reviews (21 links) lack it, so the current lock would refuse. Inventory-only records keep VD1's standard, and a mixed record lists all its links.
- **Recording the coverage in the root assent.** The assent is the lead's own; the check is about independent review.
- **Emitting the effective text of every overridden passage.** That is 264 entries, some of them 100-line `after`s. Consumers already read the records, and item 4 fixes the fold.
- **Unpinning `verify_design.py` from the closure and lane registry to avoid F8c.** The pins are deliberate.
- **Putting VD2 in a new helper module.** It still changes VD (the import), adds a closure row and needs an inventory successor.
- **VD2-a first, with F8c recorded as EXIT-PLAN debt** (F8B decision 5's other option). The generator and lane checks would refuse in between, as they did from VD1's integration (2026-10-01) until F8b (2026-10-04), and that blocks every generator unit (I1-a, X4T-c).
- **Folding the re-pin into VD2-a.** The closure and lane registry are design-selected, so only a contract successor can re-pin them (F8B "Problem").
- **Doing SD-7 r2 inside VD2.** One review cannot pin a law and a design unit, and SD-7 r2 needs its own review with the new field.
- **Retiring B-S9's copies,** or a `verify_design` selection rule that refuses overrides of historical copies. See item 8. Such a rule would be its own VD-class unit if the hazard is ever realized.

## Cross-law items

| ID | For | Item |
|---|---|---|
| **X-VD2-1** | VD1 r1 | Item 4's second bullet is amended by rule items 1 and 5. VD1's inventory rules are unchanged. |
| **X-VD2-2** | binding v4 | The no-last-writer-wins rule holds. VD2 is the second explicit supersession profile under it, after VD1. |
| **X-VD2-3** | F8B decision 5 | VD2-a lands with its re-pin successor F8c, in one commit. |
| **X-VD2-4** | I1-a (CODEX2), X4T-c | F8c is a generator-closure writer: one in flight at a time (`preview-pack-i1/i1-a/README.md:92`), frozen on the closure selected at its freeze. |
| **X-VD2-5** | every request for a contract successor that carries a contract passage supersession; the lead's workflow note on review shape | review.json needs `supersededPassages` (check 2.7), besides `ACCEPT-DESIGN-UNIT` and the single `subjectManifestSha256`. |
| **X-VD2-6** | SD-7 | The r1 request is withdrawn unsent, and r2 takes the clean form. The cost line in LD-7.1 (iii) is corrected: F8c is a re-pin, not a rebuild. |
| **X-VD2-7** | BS9 LD-1 and LD-4; M3-PLAN rows B-S9 and B-S1 | Their "VD2 would force an F8b-scale rebuild" rationale is historical and is corrected here. B-S9 itself is unchanged and stays bound and selected (item 8). |
| **X-VD2-8** | every effective-parent builder or checker | Fold supersessions as item 4 says. Frozen builders are unaffected: no contract supersession is bound yet. |
| **X-VD2-9** | M3-PLAN | Add VD2 (law), VD2-a, F8c and SD-7 r2. Edges: VD2 → VD2-a; VD2-a's acceptance and the then-current closure → F8c; the VD2-a + F8c commit → SD-7 r2's binding. |
| **X-VD2-10** | inventory | No inventory successor: VD2-a and F8c add no file. VD2-a needs no inventory number. |

No owner question is raised.

## Not claimed

- No product byte, lock, inventory, generator or test was changed, and no cargo was run. The evidence scripts ran read-only against both repositories and wrote only to temporary directories, apart from their result files in this directory.
- The prototype is evidence of feasibility, not VD2-a. VD2-a's reviewed diff, its tests and F8c's pins are their own units.
- No product behaviour, release gate or runtime trust changes. SD-7 r2's texts are SD-7's.

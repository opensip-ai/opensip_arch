# Independent review — corrected TypeScript maintenance closure unit (v2 / 409)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Read-only against live, frozen, history and locks; **no native or Node jobs**, no select, no
commits, no pushes, no delegation.

**Top verdict: ACCEPT-DESIGN-UNIT**, with **one required finding (RF-1) directed at the selection step,
not at the frozen v2 bytes.**

The v2 unit is structurally admissible: I emulated the selected verifier's own requirements and all
eleven checks pass, including the one that refused v1. The required finding concerns an artefact the
failed v1 run left behind in the architecture tree, outside the v2 subject.

I do **not** claim that 408 was selected or that any lane check passed. The lock still holds 55 contract
successors, the live registry is still the uncorrected `7a4f4459…`, and no lane has run.

---

## 1. Subject

`docs/implementation/m2/typescript-closure-selection-v2-subject.json`,
**2 330 B / `bdf558ec4e938e8ae3c2b6a1fde88f0e96519253222616288bb8d7dc196b3363`** — matches the declared
pin, re-checked unchanged at the end.

**11 / 11 members verified** byte-for-byte and by sha256: **8 reused at their original v1 paths** plus
3 new v2 paths (`README.md`, `freeze409.py`, `successor.json`). Member paths are **sorted and unique**
under `pin_rows`.

Checked record: `…/typescript-closure-selection-v2/successor.json`, **2 921 B /
`55c6f06aed87e7fe9022d861f5ee40dbbc98686e22bcd1afcce00a906c39dcba`**, standing "PROPOSED corrected
parent ordering for exact TypeScript closure repair; original408unselected."

---

## 2. The v1 refusal, located in the verifier and reproduced structurally

The refusal is not taken on report. `tools/verify_design.py` defines the requirement at **lines 146-152**:

```python
def pin_rows(value, label):
    ...
    if any(not isinstance(path, str) for path in paths) or paths != sorted(set(paths)):
        raise DesignError(f"{label} paths must be sorted and unique")
```

It is applied to subject members (line 207), candidates (214) and **parents (221, label `"contract
parents"`)** — which produces exactly the frozen message
`Design verification failed: contract parents paths must be sorted and unique`.

Comparing the two records directly:

| | v1 parent order | sorted? |
|---|---|---|
| 1 | `docs/implementation/m1/bootstrap-selection-v1/product/tools/typescript-lanes.json` | |
| 2 | `docs/implementation/m2/admission-runtime-selection-v1/product/tools/verify_design.py` | |
| 3 | `docs/implementation/m1/bootstrap-selection-v1/successor.json` | **✗ — `m1/…/successor.json` sorts before `m2/…`** |

v2 carries **the same three parent records**, reordered:
`…/m1/bootstrap-selection-v1/product/tools/typescript-lanes.json`,
`…/m1/bootstrap-selection-v1/successor.json`,
`…/m2/admission-runtime-selection-v1/product/tools/verify_design.py` — **sorted and unique**.

v1's candidates were already sorted; only the parents were not. `freeze409.py` encodes the reason as a
guard of its own: `assert [r['path'] for r in old['parents']] != sorted(...)` before it builds anything.

**This is a fair hit on my 408 review.** I checked candidate sorting and uniqueness and did not check
the same property on parents. The v2 README says root and I both missed it; that is accurate, and the
verifier caught it without permitting any live change.

---

## 3. Structural admissibility of v2 — the verifier's rules, emulated

I re-implemented `contract_successor` (186-254) and the chain guard (292-294) rather than trusting the
record. Against the current lock, with `accepted` built exactly as the verifier builds it (effective
approvals map → inventory candidates → prior contract members: 12 935 → 15 531 paths, 2 596 successor
member paths):

| Verifier rule | Source | Result |
|---|---|---|
| subject member paths sorted and unique | `pin_rows` 146-152 | ✓ |
| candidate paths sorted and unique | 214 | ✓ |
| **parent paths sorted and unique** | 221 | **✓ (the v1 failure)** |
| record is in the reviewed subject | 211-212 | ✓ |
| candidates cover subject minus record | 215-216 | ✓ |
| candidate pins equal the reviewed subject rows | 217-219 | ✓ |
| every parent is an accepted base at matching sha256+bytes | 224-226 | ✓ 3/3 |
| no parent would be overwritten by a member | 227-228 | ✓ |
| no record/candidate reuses an accepted path | 292-294 | ✓ — `reusedPaths: []` |
| `passageOverrides` | 232-245 | `[]` |

All three parents also match live bytes.

### Candidate reuse is valid

v2 reuses the eight v1 candidate files **at their original immutable v1 paths**. That is admissible
precisely because **v1 was never selected**: those paths appear in neither the effective approvals map
nor any locked successor's members, so the chain guard at 292-294 does not fire. I verified the set
difference directly, not by inference.

Two further points that make the reuse clean:

- The **v1 `successor.json` is excluded** from the v2 subject and candidate set. v2 therefore does not
  claim the superseded record, and the refused record is not carried forward as a member.
- The eight reused rows are **byte-identical to the v1 subject rows I verified in 408** — the frozen
  bytes are preserved, not re-cut.

### No already-selected duplicate registry candidate

The corrected registry digest `288c9619…` appears in **zero** accepted contract-successor inputs today.
The live (uncorrected) registry `7a4f4459…` is selected **exactly once**, via `/contractSuccessors/5`
`bootstrap-selection-v1`. So after a future materialization the live digest would match exactly one
accepted row, preserving `check_typescript.py`'s `len(selected) != 1` guard. There is no double-selection
hazard latent in this unit.

---

## 4. No new product delta

The reused registry candidate is the same file reviewed in 408, and I re-verified it against its parent
rather than relying on that:

| Check | Result |
|---|---|
| Top-level keys differing | **only `files`** |
| `schemaVersion` | 1 → 1 |
| `node` pin | byte-identical |
| `lanes` records | byte-identical |
| `files` rows | 160 → 160; 0 added, 0 removed, **1 changed**, **159 identical** |
| The one changed row | `tools/verify_design.py`, fields `bytes` and `sha256` only: 28 690/`76d7f509…` → 33 654/`2764cf7b…` |

The prospective product change remains exactly that one row. No checker, map, policy, dependency or
executable byte differs from 408.

---

## 5. The private selection failure — ordering verified from the script

`trials/typescript-closure-materialization-408/` holds `baseline.json` (592 files), `checks.json`,
`private-design.stderr`, a **zero-byte** `private-design.stdout`, and `selection.py`.

Reading `selection.py`, the guard ordering is sound and the failure landed where it should:

1. It verifies the v1 subject pin, all 9 members, my review's verdict / `requiredFindings` /
   `subjectManifestSha256`, a root assessment containing both digests, that the target directories do
   not exist, that the live product tree is clean at `7e1e18b`, and every `hashes.txt` entry.
2. It writes the corrected registry and a 56-successor lock **into a private copy**
   `/tmp/.../typescript-closure408-selected-product`.
3. It runs `private-design` against that **private** tree — **this is where it failed**.
4. Only afterwards would it materialize ignored dependencies, run the three lanes, and only at the very
   end write to the live product.

So the refusal preceded dependency materialization, any lane child and any live write. Confirmed
independently: the live tree is clean at `7e1e18b`, the lock still has **55** contract successors, and
the live registry is still `7a4f4459…`. The private staging directory is outside both repositories.

`reviews/claude-opus5-typescript408-20260921-r1/status.json` records this correctly —
`REVIEW_ACCEPTED_BUT_PRIVATE_SELECTION_REFUSED`, `selected: false`, the exact failure string, and the
replacement subject. My original 408 evidence and its `hashes.txt` are present and unaltered.

---

## 6. Required finding

### RF-1 — the failed run left a root assent for the refused v1 record

`selection.py` writes `docs/implementation/m2/typescript-closure-selection-v1-unit.json` at step 36,
**before** the `private-design` run that failed. That file exists now:

- 2 604 B, `01cf99e26154e863e4111d37649b968a8b5bbea3f88425af2c34b19c2081d79a`, **untracked** (`??`).
- `"status": "ACCEPTED-DESIGN-UNIT"`, `"rootSubstantiveAssent": true`, `"requiredUnitFindings": []`.
- Its `acceptedSuccessor` is the **v1 record** (`5ff15669…`) — the record the verifier refused as
  structurally inadmissible.

What limits it: it is **not** referenced by `design-lock.json`, **not** a member or candidate of the v2
unit, and untracked, so it grants nothing today and accepting v2 does not accept it. The adjacent
`status.json` contradicts it plainly (`selected: false`).

Why it still needs resolving before selection: it is a standing root assent naming a record that can
never be admitted, and the trial evidence does not record that it was created. `checks.json` logs only
the `private-design` failure. A later reader of the trial — or a later selector — would not learn the
artefact exists. `selection.py` itself asserts `not assent.exists()` before writing, so a re-run of a
v1-shaped selector now aborts on that assertion rather than on the real reason.

**Required:** before running the v2 selector, either remove the stale v1 assent or record its existence
and inert status in the trial evidence, and ensure the v2 selector writes its own assent path and does
not read the v1 one. This is a one-line action in the selection step; **it does not impugn any frozen
v2 byte**, and I state it as required rather than observational because an `ACCEPTED-DESIGN-UNIT`
assent for a refused record should not persist unrecorded. If the project convention requires an empty
`requiredFindings` for selection eligibility, close this first.

---

## 7. Preservation

- v1 subject `62834a7a…` (1 929 B) and v1 successor `5ff15669…` (2 528 B) are **unchanged**.
- The eight reused candidate files are byte-identical to the v1 subject rows.
- My 408 review directory retains `REVIEW.md`, `review.json`, `hashes.txt`, `root-assessment.md`,
  `status.json` and the replay evidence; nothing was edited.
- The failed-run evidence in the trial directory is retained, including the zero-byte stdout.

---

## 8. Scope and limits

- **Level:** pin and member verification, emulation of the verifier's structural rules from its own
  source, parent resolution against the accepted set, registry comparison, reuse and duplicate-selection
  analysis, and reading of the selection script's guard ordering.
- **No native or Node job was run.** `verify_design.py`, `check_typescript.py`, the boundary checker and
  all three lanes were **not** executed. My structural conclusions come from reading the verifier and
  emulating its rules in a separate script.
- **I claim no lane execution and no selection.** 408 was not selected; no lane check has passed; the
  live registry is unchanged. Root's private and live public `check_typescript` runs across all three
  lanes remain a required step after an accepted review.
- **No qualification granted:** not the lanes, the checker, the toolchain, release, or whole M2–M6.
- **Not re-reviewed on merits:** `bootstrap-selection-v1`, `admission-runtime-selection-v1`, the checker
  code, the Node pin and the 159 unchanged rows — only their currency, pins and acceptance status.
- This is a bounded corrected review, not whole-project approval.

---

## 9. Context HEADs — observed 2026-09-21T17:37:28-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `9cfeb8e38f3f30d60abd6a76e388d5614a79275f` | "Record accepted initialization integration and freeze TypeScript closure repair" |
| product | `7e1e18bf339bad6e8fd19d9e3f48b3adb9866337` | "Integrate reviewed initialization owner and diagnostic schema contracts" (clean) |

Live lock: 46 inputs, 35 inventory successors, **55** contract successors. Live registry
`7a4f4459…` — uncorrected. HEAD is an observed timestamp only; the byte pins are the authority.

---

## 10. Attestation

Read-only against live, frozen, history, product and locks. No architecture or product byte edited, no
pin edited, no select script run, no native or Node job, no commits, no pushes, no delegation. All
writing went into this review directory.

This grants no root assent and no selection, and infers none.

Reviewer: Claude Opus 5 (1M context).

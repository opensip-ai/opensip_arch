# Independent review — TypeScript maintenance closure repair (unit 408)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Read-only against live, frozen, history and locks; **no native or Node jobs**, no select, no
commits, no pushes.

**Top verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`** — for the bounded pin repair only.

The unit is exactly one correct row change, and I verified the entrypoint gating **structurally** rather
than by reproducing a single failure. This acceptance grants no lane, tool, release or M2
qualification; selected execution remains a separate root step, and the entrypoint itself enforces that.

---

## 1. Subject and unit

`docs/implementation/m2/typescript-closure-selection-v1-subject.json`,
**1 929 B / `62834a7a0c496a65a4df4c53d358a020e2fef99a3dfea6cb308caf008fa35877`** — matches the declared
pin and was re-checked unchanged at the end of the review.

**9 / 9 members verified** byte-for-byte and by sha256; sorted; unique; all under the unit. Checked
record: `…/typescript-closure-selection-v1/successor.json`, **2 528 B / `5ff156692f3eeef367c2e4941a6fc3696745ef1891688d00262446a3299d39c9`**,
standing "PROPOSED one-row TypeScript maintenance closure correction; no lane success or qualification
inferred."

**8 candidates + successor == subject**, sorted, unique; **`passageOverrides: []`**; no candidate
already in the lock; the successor is not in the lock.

### Parents — 3 declared, 3 resolved, and correctly chosen

| Parent | Channel | Live |
|---|---|---|
| `…/m1/bootstrap-selection-v1/product/tools/typescript-lanes.json` (35 396 B, `7a4f4459…`) | candidate of `bootstrap-selection-v1` | ✓ |
| `…/m2/admission-runtime-selection-v1/product/tools/verify_design.py` (33 654 B, `2764cf7b…`) | candidate of `admission-runtime-selection-v1` | ✓ |
| `…/m1/bootstrap-selection-v1/successor.json` (28 288 B, `7ae04bcb…`) | `design-lock.json` `/contractSuccessors/5/record` | ✓ |

This is the right parent set for a pin repair: the **artefact being corrected** (the old registry), the
**authority for the new value** (the accepted checker), and the **record** that selected the old
registry. Nothing is declared that the repair does not depend on.

---

## 2. The delta — exactly one row

Comparing the parent registry with the candidate, structurally rather than by diff:

| Check | Result |
|---|---|
| Both files | 35 396 B; `7a4f4459…` → `288c9619…` |
| Top-level keys | identical (`schemaVersion`, `node`, `files`, `lanes`) |
| Top-level keys differing | **only `files`** |
| `schemaVersion` | 1 → 1 |
| `node` pin | byte-identical (120 573 328 B, `1ee75375…`) |
| `lanes` records | **3 → 3, byte-identical** (`report`, `provider`, `generator`) |
| `files` rows | 160 → 160; **0 added, 0 removed, 1 changed, 159 identical** |

The single changed row is `tools/verify_design.py`, and the **only differing fields are `bytes` and
`sha256`**:

```
before  {"path": "tools/verify_design.py", "bytes": 28690, "sha256": "76d7f50913cc98dd…"}
after   {"path": "tools/verify_design.py", "bytes": 33654, "sha256": "2764cf7b5e3aaa77…"}
```

The new value **equals the separately accepted `verify_design.py` parent pin and the live product
file** — both checked directly. So the correction points at an already-selected artefact rather than
introducing a new one.

`delta.json` records `onlyChangedRowIndex: 159` and `nodePinLaneRecordsAndPoliciesUnchanged: true`;
`materialization-map.json` maps the one candidate path to `tools/typescript-lanes.json` with matching
before/after digests. Both agree with my independent measurement.

**No hidden lane or phase change.** The lane records, node pin, source roots and schema version are
byte-identical, and the unit adds no file, package, dependency or inventory row.

---

## 3. Entrypoint gating — verified structurally, not just reproduced

Root's claim is that `tools/check_typescript.py` fails on the digest **before** any child. I checked
the source rather than re-running it, which proves the ordering for every input, not one:

- `pinned()` raises `ValueError('input bytes differ: ' + pin['path'])` whenever length or digest
  mismatches.
- It is called at **line 86**: `inputs = {row['path']: pinned(root, row) for row in registry['files']}`.
- The **only** child spawn in the file is `subprocess.Popen(...)` at **line 135**.

86 < 135, and there is no other spawn site — so the gate is strictly before any child. The frozen
evidence matches exactly: the traceback ends at line 86 via line 48 with
`ValueError: input bytes differ: tools/verify_design.py`, `preflight.stdout` is **0 bytes**, and
`audit.json` records `exitCode: 1`, `stoppedBeforeAnyChild: true`, `files: 160`, at product head
`7e1e18b…`.

**Nothing is weakened, and three properties are stronger than the request claims:**

1. **No self-hash or fallback.** `pinned()` *raises* on mismatch; it never recomputes or accepts.
2. **The entrypoint binds itself.** After pinning, `check_typescript.py` and `verify_design.py` must
   byte-equal their rows in the selected closure, else `trusted entry point differs from selected
   closure`. The repair makes that satisfiable; it does not relax it.
3. **`--root` cannot choose the preflight module.** `verify_design.py` is loaded from `HERE` — the
   tool's own directory — with that intent stated in a comment.

---

## 4. Selected membership is enforced, not merely promised

The most consequential thing I found is that root's "still requires selected registry membership" is a
**machine-enforced precondition**, not a policy statement. `check()` digests the live
`tools/typescript-lanes.json` and requires:

```python
selected = [row for unit in approval['contractSuccessors'] for row in unit['inputs']
            if row['sha256'] == digest and row['bytes'] == len(raw)]
if len(selected) != 1:
    raise ValueError('TypeScript lane registry is not selected exactly once by an accepted design unit')
```

and `contract_successor` returns `"inputs": candidates` (`verify_design.py:253`). Measured against the
current lock:

| Registry | bytes / sha256 | Selected count |
|---|---|---|
| live (uncorrected) | 35 396 / `7a4f4459…` | **exactly 1** — via `/contractSuccessors/5` `bootstrap-selection-v1` |
| 408 candidate | 35 396 / `288c9619…` | **0** |

So today the live registry is properly selected once and fails only on the stale inner row; the
corrected registry is not selected at all. After acceptance and materialization the live digest becomes
`288c9619…`, which matches the 408 candidate row and restores "selected exactly once". **Until then the
lane cannot run** — the entrypoint refuses. The repair alone is necessary and not sufficient, exactly as
the unit says.

The comparison is on `sha256` and `bytes` only; `path` is not compared, which is why the
architecture-side candidate row can satisfy a live product file. That is pre-existing entrypoint
behaviour, not something this unit introduces.

---

## 5. Scope discipline

The README claims no more than the repair: *"this unit does not claim they already pass, and any
further child failure must be reported and resolved without weakening admission"*. That matches root's
framing and my findings. The unit is the same class of stale-foundation-closure repair already made for
the generator, applied to the TypeScript lane registry.

I note, without treating it as a finding, that both the old registry row and the old checker predate the
current initialization changes — so this is a lagging pin, not a regression introduced by recent work.

---

## 6. Limits

- **Level:** pin and member verification, three-channel parent resolution, structural comparison of the
  two registries, static analysis of the public entrypoint's gate ordering and selection rule, and
  measurement of the selected-exactly-once property before and after the correction.
- **No native or Node jobs were run**, as instructed. I did not execute `check_typescript.py`, the
  boundary checker, any lane, or any build. My gating conclusion is from reading the source, and the
  failure evidence is root's frozen logs.
- **No lane, tool, release or whole-M2 qualification is granted.** This review accepts the binding
  correction only; actual selected execution of the public lanes remains a required root step, and any
  subsequent child failure is a separate matter to resolve without weakening admission.
- **Not re-reviewed on merits:** `bootstrap-selection-v1`, `admission-runtime-selection-v1`, the checker
  code itself, the Node pin, and the 159 unchanged rows — only their currency, pins and selection
  status.
- **Unselected remains unselected:** this unit is not in the lock, and no assent or selection is
  inferred.

---

## 7. Context HEADs — observed 2026-09-21T17:25:00-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `9cfeb8e38f3f30d60abd6a76e388d5614a79275f` | "Record accepted initialization integration and freeze TypeScript closure repair" |
| product | `7e1e18bf339bad6e8fd19d9e3f48b3adb9866337` | "Integrate reviewed initialization owner and diagnostic schema contracts" (clean) |

Live lock: 46 inputs, 35 inventory successors, **55** contract successors. The architecture repository
advanced during this review; HEAD is an observed timestamp only, and the subject and successor digests
above were re-checked unchanged at that moment.

---

## 8. Attestation

Read-only against live, frozen, history, product and locks. No byte edited, no pin edited, no select
script run, no native or Node job, no commits, no pushes. All writing went into this review directory.
The live product was unmodified throughout and verified clean.

This grants no root assent and no selection, and infers none. It does not qualify the TypeScript lanes,
the checker, the toolchain, release, or whole M2–M6. All existing review directories are untouched and
keep their own standing.

Reviewer: Claude Opus 5 (1M context).

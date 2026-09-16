# Independent Grok review: checker-mode-selection v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement. Not the separate fresh-B session.
**Subject manifest:** `docs/implementation/m1/checker-mode-selection-v1-subject.json`
**Manifest SHA-256:** `a7c5227fb5cf34af61ee2f7ff6f517ec561071ede8c11023413ddbd9d7dd4b88`
**Members:** 21
**Verdict:** **ACCEPT-DESIGN-UNIT**

Materialization correction: the checker CLI entry already had a shebang and package `bin` mapping, but live install wrote **0644** and lost execute permission. This unit selects **0755** for `tools/typescript-boundary/bin/check-boundary.mjs` with **identical runtime bytes**, records mode separately from SHA, makes exec-failure diagnostics honest, and updates one staging-map row plus the tools guide. Not M1 complete, not release.

## Custody, archive mode, parents

21/21 selection members match. Frozen implementation subject `docs/implementation/m1/trials/checker-mode-01/subject.json` SHA `e09689ac…69b4` — **196/196**. Adjacent archive matches `archive-pin.json`. The tar member for the checker bin is mode **0755**. Candidates are exactly the subject minus `successor.json` (20). Parents pin-match live rust-provider-workspace-selection-v1 successor `28320aec…e8b2` / 7316 and inventory v10 `6608fabd…8bc9` / 121810 (20 packages). All four map rows match frozen/candidate/inventory; the bin row carries `requiredModeOctal: "0755"`. `required-modes.json` matches. Private copy preserved 0755. Original candidate path and frozen tmp tree were not executed against.

| Location | bytes | SHA-256 | mode |
| --- | --- | --- | --- |
| live | 951 | `76e31fbe…10f1` | **0644** |
| candidate / frozen / private copy / tar | 951 | `76e31fbe…10f1` | **0755** |

Runtime bytes are unchanged. Live still 0644 after this review (not installed here).

Staging-map vs live: **exactly one** of the equal-length file rows differs, path `tests/support/cli-invocations.mjs`. Other fixture rows are byte-identical.

## Substantive correction

Direct `.bin`/shebang spawn requires execute permission. Explicit `node path/to/check-boundary.mjs` does not, which is why the Node wrapper still worked on 0644. SHA does not authenticate POSIX mode.

The CLI harness now treats missing stdout/stderr as empty strings, records `spawnError` (`code`/`message`), and sets `ok` false whenever `child.error` is set. Exec failure cannot become a parsed report or a silent Node re-invoke. Negative 0644 run: `bin-symlink-exec*` rows are `exit=null spawn=EACCES`; `node-realpath` / `node-flag-*` still succeed because Node reads the file. The suite therefore fails honestly (exit 1) with **EACCES** and **no TypeError**.

Tools README replaces the stale `repository-file-inventory.v8.json` literal with a labelled selected-inventory placeholder and notes the separate Rust-provider development workspace (`--lane rust-provider`, currently refuses native analysis). Four existing inventory owners; no checker source-closure, schema, generated, dependency, lock, package, or DAG change.

## Reproduction (private copy, Node v24.16.0, npm 11.13.0, offline cache)

Adapted `run-checks.py` against the private product (not `/tmp/.../m1-checker-mode-candidate-01`).

| Check | Result |
| --- | --- |
| `npm ci --offline` on the checker package | pass; bin still **0755** after provision |
| `node tests/run.mjs` | **234/234** pass |
| Separate copy chmod **0644**, CLI-invocation tests only | exit **1**, **EACCES** present, **TypeError** absent |
| Live bin after review | still **0644** |
| Frozen bin after review | still **0755** |

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

## Limits

- Mode-aware **integration** is still required: live materialization remains 0644 until this successor is actually installed with 0755.
- Inventory v10 file rows still do not encode POSIX mode; this unit records it on the map/`required-modes.json`.
- 234 regressions plus the 0644 negative are not full M1 or release qualification.
- Frozen consumer-B history is untouched and is not this verdict.
- No schema/lock/runtime-closure claim.

# B2-b0: the current discovery reference (SLM over the walker population, projected to V3)

**Design unit, reference only, under the accepted B2-b plan r4** (`config-discovery-b/b2-b/PLAN-r4.md`, section 1.0; Codex `codex-b2b-plan-r4`, ACCEPT after rounds 1 to 3). It discharges plan r4's B2BPLAN-1 resolution: the accepted SLM `discovery` predates the shared-rule corrections, SX-1 and version 3, so it cannot serve unchanged as the oracle for the product's pure discovery core (B2-b2). It is bound as contract successor 164.

## r3 changes (Codex `codex-b2b0-reference-r2`: B2B0REF-1 and B2B0REF-2 resolved; B2B0REF-3 and B2B0REF-4 raised)

- **B2B0REF-3: pruned entries kept unobserved VCS annotations.**
  - **The defect.** `vcs` is evidence from inside a directory (its `.git` entry). r2 copied it with a pruned anchor, so SLM's `finish` reported the anchor as a nested repository.
  - **The fix.** Every entry now carries only observed evidence. A directory keeps `vcs` only if the walker probes its interior: the root, a listed directory, a probed boundary or a chain directory. A pruned anchor keeps its own kind, identity and custody fields.
  - **The other fields.** `aclWrite` and `aclUnreadable` describe the entry's own ACL. For a pruned anchor they can only move a count's basis to `not-enumerated`, which production declares anyway.
  - **Controls.** For each of the four reasons, an anchor with `vcs` and a hidden `.git`: the entry is projected without `vcs`, it is not a repository, and its pruned row stays.
- **B2B0REF-4: boundary evidence was taken below the depth limit.**
  - **The defect.** r2 probed a 257-segment child for `opensip.json` and `vcs` before applying the depth guard.
  - **The fix.** The depth policy now comes first. A 257-segment directory is never probed for boundaries; only its four marker names are observed.
  - **Controls.** Config and VCS boundaries at 256 (reported, evidence present), 257 (not reported, no `opensip.json`, no `vcs` on the entry) and 258 (not observed).
- **Review support.** `reproduce_b2b0ref3_4.json` shows both reproductions under the r2 reference (a repository at `.opensip`; a nested project at depth 257) and neither under r3.
- **Unchanged.** All 64 discovery cases replay as before, every one V3-valid, with the same two explained removals.

## r2 changes (Codex `codex-b2b0-reference-r1`, REQUIRED-FINDINGS)

- **B2B0REF-1: upward ancestors leaked into the downward population.**
  - **The defect.** r1 unioned every ancestor of `cwd`, `explicitProject`, `explicitResolved` and `accountHome` into SLM's input. So a `cwd` below `.opensip`, or in an unrelated sibling, reintroduced paths the walker never observes.
  - **The fix.** Upward evidence is now pass one's walked rows, plus the explicit path, each with its `opensip.json` and only **when not below the selected root** (`upward_evidence`). The downward population comes only from `walker_population`. Pass two starts SLM's walk at the selected root (`cwd` = root), and its upward provenance fields (`mode`, `configPath`, `walked`, `stopReason`, `custodyWaiver`, `vcs`, `explicitPathWasSymlink`) are taken from pass one, whose selection saw the real `cwd` chain.
  - **New controls.** Codex's two reproductions, and a deep-`cwd` overlap with the depth stop.
  - **Review support.** `reproduce_b2b0ref1.json` shows both reproductions leaking under the r1 reference and not under r2.
- **B2B0REF-2: replay exceptions did not fail the checker.** No case expects an instrument exception, so every exception is now a failure.
  - The checker asserts exact coverage: 64 discovery cases replayed and V3-valid, and 4 classified as non-discovery.
  - A negative control reruns the checker with an injected current-replay consistency fault. It must exit non-zero with `passed: false`, and it does.

## What it is

`reference/discovery_scan_reference.py` (new). It edits no byte of SLM, DD or the B2-a copy.

| Function | What it does | Authority |
|---|---|---|
| `load(arch)` | SLM at its accepted bytes, with its module global `DD` replaced by the bound B2-a reference (successor 163). SLM calls `DD.*` at call time (SLM:611-805), so its algorithm then runs with the outermost rule across four reasons, parent-first Cargo roots and SX-1. `load(arch, historical=True)` is SLM unchanged. | B2-b plan r4 §1.0; successor 163 |
| `walker_population(inp, root, source)` | SLM's `fs` restricted to what the native walker observes. The rules are below. | SL:146-168, SL:187-216; plan r4 §1.0, §1.3; LD-B2B-8 |
| `current(slm, rule, inp)` | Pass one, on the full input, gives the selected root, the unit source (the walker chooses its source before traversal) and the upward provenance. Pass two runs on the downward population plus `upward_evidence`, with `cwd` set to the root, and gives the downward provenance. A change in root or source between the passes is an error. A refusal before `finish` stands as it is. | plan r4 §1.0; r2 |
| `project_v3(result)` | The V3 shape: `schemaVersion` 3, `memberRepositories` and `memberConfigs` empty, the rows already in V3 vocabulary, D9 already in `DiscoveryD9V1`. **`workspaceDeclarations` is pending** (`pendingFields`); only B3-b's readers observe it. | LD-B2B-3; B-S1 |
| `shape_fill(partial)` | **Shape only.** Each reader's `absent` row, so that the other provenance fields can be schema-validated. It is never an observation and never emitted. | LD-B2B-3 |
| `boundary_inventory_v3(rule, partial)` | The complete `AdmittedBoundaryInventoryV3` of an accepted result, through the B2-a reference's V3 converter. | B-S1 LD-4 |

**The population rules.**
- **Upward evidence (r2).** Pass one's walked rows and the explicit path, each with its `opensip.json`, only where not below the selected root. It is presented to pass two's selection and never enters the downward population.
- **Automatic, parent-first.** Each child of an ordinary listed directory enters:
  - **A pruned anchor** of any reason enters as **its own entry only**, never listed (pruning before boundaries).
  - **A boundary** is a directory of at most 256 segments, other than the selected root, that holds `vcs` or `opensip.json`. It is probed for that evidence and enters with its `opensip.json` entry only.
  - **Observed evidence only (r3).** `vcs` stays on an entry only if its directory is probed. A pruned anchor or a 257-segment directory never carries it.
  - **Depth.** Directories of at most 256 segments are listed. A 257-segment directory is never listed: only its four marker names are observed, which is what SLM's `DEPTH` exclusion needs (Codex NBO-1 on plan r4). Nothing deeper is observed.
- **Explicit or config, for each named root, parent-first.**
  - Each chain directory enters with its `Cargo.toml` and `opensip.json`.
  - A boundary below the root stops the chain (SLM's crossing refusal).
  - The next component is classified with the Cargo roots known so far; a pruned prefix enters as its own entry only and stops the chain.
  - At the named root, its subtree enters under the automatic rule.
  - **Nothing else enters.** In particular, a nested repository in an unrelated sibling is not observed.

## Checks

`evidence/check.py` writes `evidence/checks.json`, which reports `passed: true`.

**All 68 cases of `discovery-cases.v1.json`.** The 64 discovery cases run in three stages: historical SLM, SLM with the rule swapped in on the full input, and current. The 4 boundary-inventory-model cases are listed as not discovery-model.
- **The rule swap** changes no case's outcome.
- **The population** changes no outcome. It removes exactly one path in two cases (`config2-workspace-roots-override-automatic-discovery-with-the-same-custody-checks` and `explicit-joins-take-precedence-over-config2-workspace-roots`): the nested repository `vendor/lib` in a subtree the explicit and config sources never observe.
- **Every reported path** of every current result is in its downward population.
- **Exact coverage (r2).** 64 discovery cases replayed and V3-valid; 4 classified as non-discovery. Any exception fails the checker.
- **V3 validation.** All 64 current results validate as `DiscoveryResultV3` (pending field shape-filled). All 35 accepted results' boundary inventories validate as `AdmittedBoundaryInventoryV3`, in the SLS bundle merged with B-S1's additions.

**36 controls** (plan r4; r2; r3):

| Group | Controls |
|---|---|
| Direct population assertions | For each of the four reasons, the anchor contributes only itself, and a repository inside it is never reported |
| Codex's B2BPLAN-1 reproduction | A repository under `.opensip` |
| Cargo `target` joins | Refused through explicit joins and through a config array; an ordinary `target` without `Cargo.toml` is admitted |
| Crossing order | A crossing above a pruned prefix refuses as the crossing; a repository below a pruned prefix refuses as `JOIN_INSIDE_PRUNED_TREE` and is never reported |
| Nested boundaries | Repositories inside repositories, and projects inside projects |
| Explicit and config scope | An explicit root beside an unrelated sibling, which is never observed; a config array that does not fall through to automatic discovery |
| Markers below an anchor | Never a unit, an exclusion or a Cargo root |
| Depth | 256 is a unit, 257 is `DEPTH`, and 258 is unseen |
| Upward evidence (r2) | Codex's two B2B0REF-1 reproductions (a `cwd` below `.opensip`, a `cwd` in an unrelated sibling); a deep `cwd` that adds nothing beyond the depth stop |
| Checker (r2) | An injected consistency fault fails the checker |
| Observed evidence (r3) | Each of the four pruned reasons with `vcs` and a hidden `.git`: the entry is projected and is not a repository |
| Depth before boundary (r3) | Config and VCS boundaries at 256, 257 and 258, with exact populations |

## Not claimed

- No product code.
- No SLM, DD or B2-a copy edit.
- No passage, schema or bundle change.
- No reader observation: `workspaceDeclarations` is B3-b's.
- No qualification.

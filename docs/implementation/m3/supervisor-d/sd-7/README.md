# SD-7 r2 — NE §10's follow-ups from M3-D r4, in VD2's clean form (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r2, PROPOSED, not accepted.** It is a design unit: it edits only arch, and adds no product file, code, class, exit code, error code or public detail code. It needs Grok's `ACCEPT-DESIGN-UNIT`, with a review that lists `supersededPassages`, and the lead's root assent before it can be bound. **It binds only after VD2-a and F8c are integrated.** Any earlier `verify_design` refuses it, failing closed.

**History.** r1 used B-S9's complete-copy form: NE7, a 380,848-byte successor copy of NE that would have become the selected NE. The lead held it, and its request (`reviews/grok-sd-7-r1/`) was withdrawn unsent. r1 was never reviewed. Its members are kept for the record in `reviews/grok-sd-7-r2/r1-members/` (subject `3c60a82b…`). The lead then fixed the tool instead. Law **VD2** (`docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, Codex ACCEPT, `2e4f70b4…`) adds the contract passage supersession to `verify_design`, and its "SD-7 r2" section gives this unit's shape (VD2:194-211).

## r2 changes

| From r1 | In r2 |
|---|---|
| NE7, a complete copy of NE, selected by the record's `standing` | **Dropped.** NE stays the selected native-evidence contract. No line drift, no selection change, and no NE residual hazard. The line map and X-SD7-NE are dropped. |
| SD-5's row conformed inside NE7 | A **contract passage supersession** of SD-5's NE:3540 override (VD2 rule items 1-2). It names SD-5's record by exact pin, with the same parent and selector; its `before` is SD-5's `after`; its `after` is the raw NE:3540 row, then the conformed row. |
| Item 25's row inserted inside NE7 | An ordinary **override of NE:3539**, a key no bound successor overrides. Its `after` is the raw NOT-SELECTED row, then item 25's row. NE:3539 is the line VD2's probe R1 used (VD2:147, VD2:199). |
| Line-1159 overrides of B-S9's two model copies | **Unchanged.** |
| LD-7.1: form (ii), the copy | LD-7.1: form (iii), VD2's supersession. (ii) is rejected for its citation drift and unenforced selection. |
| LD-7.2: the copy is NE's effective text | LD-7.2: VD2 item 4's **effective-text check**. r2's effective NE equals r1's NE7 byte for byte (380,848 bytes, `0dd155c2…`). |
| — | The review must carry **`supersededPassages`** (VD2 rule item 2.7; X-VD2-5). |

The texts are r1's, byte for byte: both rows and the remedy. LD-7.3 to LD-7.6 and reviewer points R2 and R3 carry over unchanged (VD2:206).

## What it is

The accepted supervisor law **M3-D r5** (`supervisor-d/PROPOSAL-r5.md`, Grok ACCEPT, `224b9228…`) names successor **SD-7**, "NE §10's follow-ups from r4" (MD5:1182; X-D4-NE, MD5:1215; F14 and F15, MD5:1204-1205):
- **(a) SD-5's bound row follows item 24 (LD-R4-1).** SD-5 (bound at product `052d3cb`) copied r3's wording. Its EE-3b counts "a `commands` entry for role `analyzer`", and its remedy says no component may "declare a project hook, root command or probe", which refuses every analyzer. r4 replaced that with an exact root-command predicate (MD5:780-795).
- **(b) Item 25's request-class row (LD-R4-2).** `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `domainDetail` `PROVIDER.NOT_SELECTED` with subject `excluded-form:<class>`, and no runId or executionId (MD5:837). `PROVIDER.NOT_SELECTED`'s code-keyed remedy is widened to stay true for both conditions (MD5:839).

**Product.** Main `4c761e8` (I1-a's binding, 94 contract successors), read only. Since `6190e66`, S21 (WS only) and I1-a (no passages) have bound; neither touches NE or B-S9's copies. The tool SD-7 r2 needs is VD2-a's, built with F8c in the worktree `/Users/sb/code/opensip-ai/opensip-vd2a` (main `4c761e8` plus VD2-a's diff, plus F8c's re-pins and its staged lock row, 95 contract successors). That worktree is with Codex.

## Short names

Each sha256 prefix is the first 8 hex of the exact bytes pinned in the review request (`reviews/grok-sd-7-r2/hashes.txt`).

| Name | Document | sha256 |
|---|---|---|
| **MD5** | `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, M3-D r5, the accepted snapshot | `224b9228…` |
| **VD2** | `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, VD2 r1, the accepted snapshot (`reviews/codex-vd2-r1`) | `2e4f70b4…` |
| **VD2-a** | the VD2-a worktree's `tools/verify_design.py` (43,630 bytes) | `c01488fd…` |
| **VD** | `tools/verify_design.py` at main `4c761e8` (40,714 bytes; VD1's bytes) | `c13d231e…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` (329,013 bytes) | `83b99783…` |
| **SD5** | `docs/implementation/m3/supervisor-d/sd-5/successor.json`, bound at `052d3cb` (5,805 bytes) | `5e115818…` |
| **NEM** | B-S9's two model copies, `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py` (`a7e40715…`) and `…/native_evidence_model.v2.py` (`4f800faa…`) | |
| **NES** | `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `2d37b810…` |
| **F8c** | `docs/implementation/m3/verify-design-vd2/f8c/`, the generator-closure and lane re-pin onto VD2-a's bytes; staged in the worktree lock with SCRATCH-F8C review and assent pins | record `fda38d17…` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `successor.json` | the record: three parents (NE and the two NEM copies), one `passageSupersessions` entry, three `passageOverrides`, six candidates |
| `PASSAGES.md` | generated: the supersession and the NE:3539 override (before and after), the effective §10 rows, and the two remedy overrides |
| `evidence/fold-report.json` | generated: VD2 item 4's fold of NE (39 bound entries, then SD-7's two), its digest before and after SD-7, the equality with r1's NE7, and the exact `supersededPassages` list the review must carry |
| `evidence/build_sd7.py` | builds the generated files, the record, the subject manifest and the draft unit record; `--check` compares instead of writing |
| `evidence/check_sd7.py` | read-only checks, including an independent fold |
| `evidence/verify_scratch.py` | the VD2-a tool on the staged lock, the plain tool at main, and VD2's refusals |
| `../sd-7-subject.json` | the subject manifest (generated) |
| `../sd-7-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/grok-sd-7-r2/review.json`; not part of the subject |

## The entries

| # | Kind | Parent | Selector | `before` | `after` |
|---|---|---|---|---|---|
| 1 | `passageSupersessions` | NE | `{"line": 3540}` | SD-5's `after`: the raw release-declaration row, then SD-5's row | the raw release-declaration row, then the **conformed row** |
| 2 | `passageOverrides` | NE | `{"line": 3539}` | the raw NOT-SELECTED row | that row, then **item 25's row** |
| 3 | `passageOverrides` | NEM copy | `{"line": 1159}` | `"PROVIDER.NOT_SELECTED": "this capability is not selected for that language mode; no promise is made for it",` | the **widened remedy** |
| 4 | `passageOverrides` | NEM v2 copy | `{"line": 1159}` | the same | the same |

Entry 1's `supersedes` is `{"record": <SD-5's pin: 5,805 bytes, 5e115818…>, "parent": <NE's pin>, "selector": {"line": 3540}}`. SD-5's record need not be a parent: the pin names it exactly (VD2:197).

**VD2's checks, as they apply here** (rule item 2):
- **Target.** SD-5's record pin equals the lock's binding exactly, and SD-5 is earlier: position 85 of 94 at `4c761e8`. Its entry for NE `{"line": 3540}` is an ordinary override, so this is the chain's root link.
- **Same passage.** Same parent pin and selector.
- **Chain.** `before` equals SD-5's `after` byte for byte.
- **Linear.** No other link names NE:3540.
- **Review list.** The review lists `supersededPassages` equal to the record's `supersedes` list.

`check_sd7.py` asserts each of these against the lock.

## The texts (unchanged from r1)

### The conformed row (MD5 item 24, LD-R4-1)

| | SD-5 (bound) | SD-7 |
|---|---|---|
| Provenance | "(contract successor SD-5 of law M3-D r3, item 24)" | adds "; conformed by contract successor SD-7 to law M3-D r5, item 24, lead decision LD-R4-1" |
| EE-3b | "(a `commands` entry for role `analyzer`, or a capability outside the native capability matrix's provider capabilities)" | "(a capability outside the native capability matrix's provider capabilities)" (MD5:776, MD5:788) |
| EE-5a | "a project hook, root command or contribution-granted probe" | "a project hook, a contribution-granted probe, or a root-command claim on the host-owned root namespace, which is exactly" item 24's predicate (MD5:782-785): **(a)** a closure-only manifest (`toolchain`, `stdlib`, `rust-dev-llvm`, `grammar`) that declares `commands` at all; **(b)** an `analyzer` whose tree has not exactly one entry without `parent`, or whose parentless entry's `name` differs from the manifest's `name`; **(c)** a reserved root-command name among its root-namespace keys (its `name`, its `aliases`, and for `analyzer` its parentless entry's aliases) |
| Admitted | — | an `analyzer`'s own name-bound mounted root, with any depth below it; a live-name collision; a command tree is never an EE-3b form (MD5:786-788) |
| First refusal | — | "A manifest that the security owner's manifest admission refuses first never reaches component admission and keeps that route" (MD5:789-794) |
| Remedy | "… or declare a project hook, root command or probe. …" | "… or claim a project hook, a reserved or additional root command, or a probe. …", MD5:1182's words exactly |

The class, code, detail, subject rule and route-boundary sentences are SD-5's. The route is unchanged.

### Item 25's row (MD5 item 25, LD-R4-2)

| Field | Value | Basis |
|---|---|---|
| Condition | a well-formed request refused at typed request admission, before the durable entry, the creation prelude and any `ExecutionId` draw, as `ExcludedForm {class, subject}` | MD5:829 |
| Classes | `EE-2`, `EE-4` (request part), `EE-6a`, as MD5 represents them | MD5:833-835 |
| Why this route | outside D-371's selected product, as the NOT-SELECTED cell of the row above is; never a malformed request or a host fault, whatever the origin | MD5:838, MD5:844; NE:3577-3579 |
| Class / exit / code | `request-rejected` / 2 / `REQUEST.UNSATISFIABLE` | NE:3539; D9 `rejectionCauseToErrorCode["unsatisfiable"]` |
| `domainDetail` | `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`, the first of EE-2, EE-4, EE-6a | MD5:837 |
| `errors`, record, ids | exactly that detail; every `ExcludedForm` to the operational record; no runId and no executionId | MD5:837 |

### The widened remedy (both NEM copies, line 1159; 254 ASCII characters)

"this capability is not selected for that language mode, or the request asks for an external discovery or public-lifecycle endpoint, untrusted native or WASM admission, or network-granted analysis; no promise is made for it; restate the request without it"

- **Truth.** It is true for every condition that reaches `PROVIDER.NOT_SELECTED`:
  - the NOT-SELECTED cell, `native.requested-capability-mode-not-selected`, the only route-registry key that reaches it;
  - the three request-class forms.
- **Wording.** Both original clauses are kept word for word.
- **The other entries.** `PUBLIC_ROUTE_REMEDIES` keeps every other key and value, and the two copies stay identical.
- **NES.** This meets NES's `remedyKeyingConstraint`.

## The effective NE (VD2 item 4)

Folding every bound entry on NE in lock order (39 overrides from six records), then SD-7's supersession and override, gives 380,848 bytes, `0dd155c2…`. That is SD-7 r1's NE7 byte for byte, which `build_sd7.py`, `check_sd7.py` and `verify_scratch.py` each check independently. Before SD-7, the fold is 378,351 bytes, `03b498b7…`, r1's recorded effective parent. So r2 carries r1's meaning exactly, with no copy. In that effective text, NE §10's rows run: the NOT-SELECTED row, item 25's row, the release-declaration row, the conformed row, the producer cause and carrier row, then SYN-1's row.

## The review

`review.json` must carry, besides `verdict` `ACCEPT-DESIGN-UNIT`, `requiredFindings` `[]` and `subjectManifestSha256`, the field `supersededPassages`, equal by value and in order to the record's `supersedes` list (VD2 rule item 2.7). That is exactly `fold-report.json`'s `reviewSupersededPassages`:

```json
[{"record": {"path": "docs/implementation/m3/supervisor-d/sd-5/successor.json", "bytes": 5805, "sha256": "5e11581804098116a4afa5052ff27ed426beaebcc6e0a38607d1628ea8a595e7"}, "parent": {"path": "docs/v2/contracts/product-v1/native-evidence.md", "bytes": 329013, "sha256": "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"}, "selector": {"line": 3540}}]
```

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them.

**LD-7.1 (r2). Form: VD2's contract passage supersession for SD-5's row; fresh line overrides for item 25's row and the remedy.**
- MD5:1182 leaves the form to the drafter: "B-S9's complete-copy form or a `verify_design` successor". With VD2 accepted, the successor exists.
- **Rejected:**
  - **(ii) the complete copy** (r1). Every accepted law cites NE by original line, and the copy's lines drift from line 123 on. The selection is declared in prose and `verify_design` cannot enforce it. VD2 item 8 makes the supersession the default for a bound text passage.
  - **(i) an erratum on a neighbouring line.** Two meanings for one route.
  - **A second override of NE:3540.** Refused under every tool ("conflicting contract passage overrides").
  - **Item 25's row inside the supersession's `after`.** NE:3540's meaning is SD-5's row. The request-class row is a new passage next to the NOT-SELECTED row it reuses, and NE:3539 is a free key.

**LD-7.2 (r2). VD2 item 4's effective-text check replaces r1's copy.** r2's effective NE must equal r1's NE7 byte for byte, and it does.

**LD-7.3 to LD-7.6 (carried from r1).**
- **LD-7.3.** The conformed row changes only what MD5 changes.
- **LD-7.4.** Item 25's row sits right after the NOT-SELECTED row.
- **LD-7.5.** The remedy keeps both clauses and is widened in both NEM copies, not in the retired capability-totality or frozen v2 files.
- **LD-7.6.** NES's route registry is not extended: its scope is the capability and Coverage-cause guards, and it is registered bytes.

## Points for the reviewer

- **R1 (LD-7.1).** Is the supersession VD2's form exactly? Check the target pin, same passage, `before` equal to SD-5's `after`, first link, and the review list. Is the NE:3539 override the right home for item 25's row?
- **R2 (LD-7.3).** Does the conformed row state M3-D r5 item 24's predicate exactly, with EE-3b's capability form only and the remedy in MD5's words?
- **R3 (LD-7.4, LD-7.5).** Is item 25's row LD-R4-2's route exactly? Is the widened remedy true for every condition that reaches `PROVIDER.NOT_SELECTED`?
- **R4 (LD-7.2).** Is the effective NE after SD-7 r2 equal to r1's NE7, folded as VD2 item 4 says?

## Cross-law items

| ID | For | Item |
|---|---|---|
| **X-SD7-J1** | M3-J1's next revision | Row 57 (MD5:1222) cites "NE §10 (SD-7)": NE:3539's override. Row 56's basis is NE:3540 as SD-7 supersedes it. J-C20 tests both. |
| **X-SD7-D** | M3-D's next revision | X-D4-NE and F14/F15 are done. D4-T1's remedy assertion takes SD-7's remedy. D4-T2's remedy assertion "follows SD-7" (MD5:850) with the widened string. |
| **X-VD2-5** | VD2 | Satisfied here: the request asks for `supersededPassages`. |
| **X-VD2-8** | every effective-parent builder | Fold NE:3540 through this link, which is the first bound contract passage supersession. |
| **FA1-F1** | the native reference owner | Unchanged and still owed. It overrides other lines of the same NEM copies, so it composes with line 1159. |
| **SD-5b** | lead | Unchanged. |

No owner question is raised.

## Binding

**Order.** VD2-a and F8c are integrated first, in one product commit (VD2 item 7). Then SD-7 r2 binds in a binding-only commit, after `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok-sd-7-r2/review.json`; it carries `supersededPassages`;
- complete `sd-7-unit.json`;
- append `{record, subjectManifest, review, assent}` to the product lock;
- run plain `verify_design`, which is VD2-a's tool by then.

**If NE or a B-S9 copy gains a bound override first,** the builder's lock assertions fail, and SD-7 is rebuilt and re-reviewed. Timing is MD5's: (b) before J2a projects item 25's refusal, and (a) recommended before D4's integration review.

**Evidence runs** (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read-only):
- `build_sd7.py`, then `build_sd7.py --check`: identical bytes.
- `check_sd7.py`: pass.
- **`verify_scratch.py`, VD2-a.** The VD2-a worktree's tool (`c01488fd…`) over the worktree's staged lock (main's 94 plus F8c's row with SCRATCH-F8C pins, rebuilt and matched to the staged pins), with the worktree as the implementation:
  - the staged lock passes at 95 with `contractPassageSupersessions` 0;
  - **with SD-7 r2: PASS, 95 → 96, `contractPassageSupersessions` 1.** The inventory chain, inheritance, the 21 inventory supersessions, the 40 generation sources and the 48 admission sources with 15 aliases are unchanged;
  - VD2's refusals hold, each with VD2-a's exact message: a review with no list, a review with a wrong list, a later override restating SD-5's row, a second link naming SD-5, and a different second override of NE:3539.
- **`verify_scratch.py`, plain tool at main `4c761e8`** (`c13d231e…`): main's lock passes at 94. SD-7 r2 is **refused** over main's lock and over the staged lock alike: "passage supersession must select an inventory row description". It fails closed.

## Controls owed by the implementing units

- **D4-T1 and D4-T4** (D4): a manifest-class refusal carries SD-7's conformed remedy. An `analyzer` with its own name-bound mounted root passes R10a, and (a), (b) and (c) refuse as EE-5a (MD5:818-825).
- **D4-T2** (D4): a request-class refusal is `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`, with the widened remedy, and no runId or executionId.
- **The NOT-SELECTED cell** keeps its route and carries the widened remedy.

## Not claimed

- No product code, test, build or checker run was made, and nothing was written to the product or the VD2-a worktree. Only the three evidence scripts ran, read-only.
- Neither native model was imported: `check_sd7.py` parses both with `ast`.
- No law is amended. No class, exit, error code, fault cause or public detail code is added, and no NES, REG, D9, WS, SL or product byte changes.
- VD2-a and F8c are their own units, with Codex. SD-7 r2 relies on them only for its binding.

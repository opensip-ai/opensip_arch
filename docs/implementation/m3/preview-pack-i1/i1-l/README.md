# I1-L — the `cycle-representative` policy-language successor (contract successor)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **PROPOSED frozen candidate.** It needs CODEX2's `ACCEPT-DESIGN-UNIT` and root assent before selection.

I1-L executes items 2 to 4 of the accepted law M3-I1 r2: `../PROPOSAL-r2.md`, 52522 B, `1eb47d1e…`, accepted by CODEX2 in `docs/implementation/m3/reviews/codex2-preview-pack-i1-r2/`. It is the design unit I1-L of `../UNITS-r2.md`. It adds the graph atom `cycle-representative` to the policy language, authorizes its one additive identity member, and appends the atom contract's §4a. Base: product main `3e64266`. It changes no product file; unit I1-a copies its two product schema sources (see "For I1-a").

Short names follow the law's Short names table: WS, IE, COMP, ATOM, IDS and PDS. Two more are used here:
- **WSE** is `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md`, WS's selected effective copy.
- **PIDS** and **PPDS** are the selected product source copies `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json` and `.../policy.v2.schema.json`. Product main's `schemas/sources/identity-v3.schema.json` and `policy-v2.schema.json` equal them byte for byte.

## What changes

| Kind | Where | Count |
|---|---|---|
| Text passage overrides (`successor.json`, line selectors) | WS, WSE, IE, COMP, ATOM | 11 |
| Complete successor copies of JSON documents | IDS, PDS, PIDS, PPDS | 4 |
| Appended section | ATOM §4a (the override of ATOM:366) | 1 |

Nothing else changes. EPS, RPS, NE, the atom and projection registries, the policy-test schema and every reference checker keep their bytes and meaning, as law item 4 says.

## Text passage overrides

Each `after` keeps its `before` text word for word and only inserts. Each `before` is the parent line exactly, as `verify_design` reads it (`splitlines`).

| # | Parent | Line | Source | Change |
|---|---|---|---|---|
| 1 | WS | 598 | law item 4 | after the code span `` `exists\|none\|count-at-most\|all-covered` `` insert ", the graph atom `cycle-representative` (only as a rule's whole `emitWhen`, only over `imports` at `resolved-target` with no filters, only for subject kind `file`)" |
| 2 | WS | 603 | law item 4 (603-604) | after "`all-covered` indeterminate" insert "; `cycle-representative` is true for the least-path file of a cyclic component of the admitted resolved project import graph, false for its other files, and otherwise false only under complete graph Coverage, else indeterminate (atom contract §4a)" |
| 3 | WSE | 602 | WS:598's effective copy | the same as 1 |
| 4 | WSE | 607 | WS:603's effective copy | the same as 2 |
| 5 | IE | 214 | law item 4 (213-214) | after "not a permissive parser." the law's exception paragraph, word for word |
| 6 | IE | 1266 | consequential | "`operation` is one of the seven evaluator predicates" gains "(or `cycle-representative`, under the reviewed M3-I1 exception above)" |
| 7 | IE | 1334 | consequential | "whose seven evaluator" gains "(eight, with the reviewed M3-I1 exception's `cycle-representative`)", before line 1335's "predicates are closed" |
| 8 | IE | 1544 | consequential | the §4 predicate table gains a `cycle-representative` row after `all-covered` |
| 9 | COMP | 34 | law item 4 | appends the law's sentence |
| 10 | COMP | 109 | consequential | §9.2's atomic-node list gains `` / `cycle-representative` `` (its `inputRefs` is EI, like every atom's) |
| 11 | ATOM | 366 | law item 4 | §4's last line; `after` appends `\n\n---\n\n` and §4a (below) |

No accepted successor overrides any of these lines. The bound overrides on these parents are WS:1296, WSE:1300 and IE lines 45, 48, 51, 52, 58, 273, 278, 455, 1272, 1314, 1635 and 1655. COMP and ATOM have none. `build_i1l.py` checks this against the product lock.

## The JSON successor copies

| Parent | Copy | Bytes, sha256 |
|---|---|---|
| IDS (196987, `a76c9e2f…`) | `design/foundation/identity-schemas.v3.json` | 198725, `c9214f03…` |
| PDS (27863, `c8b0a907…`) | `design/workflows/schemas/policy-document.v2.schema.json` | 28042, `45581464…` |
| PIDS (197480, `311c1feb…`) | `product/schemas/sources/identity-v3.schema.json` | 198423, `eb6ec957…` |
| PPDS (26534, `b221b5ed…`) | `product/schemas/sources/policy-v2.schema.json` | 26677, `0ff24ae6…` |

Each copy is its parent's raw bytes with exactly these edits, in place. No other byte changes, and `$id`s are kept. `evidence/copies-report.json` lists every hunk.
- **The one member.** `"cycle-representative"` is appended as the last member of:
  - IDS and PIDS: proof-bundle `predicateProofs[].operation` (new line 1231) and `program-predicate.operation` (new line 2792);
  - PDS: `Atom.op` (new line 303) and `AtomSuccessorV1.op` (new line 945);
  - PPDS: `Atom.op` (new line 303).
- **`majorLaw`** (IDS and PIDS; copy lines 4980 and 4986). The law's sentence is appended: " The single additive operation member authorized by identity-and-evidence §3's reviewed M3-I1 exception keeps proof3 and the program-predicate schemaVersion; it is not a permissive mixed-version parse."
- **PDS and PPDS `description`** (line 5, consequential). "(exists, none, count-at-most, all-covered, and, or, not)" becomes "(exists, none, count-at-most, all-covered, and, or, not; the graph atom cycle-representative of atom contract §4a is admitted only as a rule's whole emitWhen)".
- **The parents' bound overrides, carried.** The product lock binds passage overrides to two of these parents, and each copy carries its parent's, so the copy means what its parent means:
  - IDS has four: predicate-matching-reference-selection-v2's `/$defs/program-predicate/description`; stage-meta-reference-selection-v1's `/$defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest/registeredBy/law`; and EC1's `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact` and `/x-opensip-digest-domains/closureKinds/note`.
  - PIDS has two: the first two of those. EC1 overrode only IDS ("product copies keep their bytes"), so PIDS's meaning has never included EC1's text, and its copy does not either.
  - PDS and PPDS have none.

The copies keep their parents' relations:
- PPDS's copy is PDS's copy without the `AtomSuccessorV1` block, as PPDS is PDS without it.
- PIDS's copy still differs from IDS's copy by the framework-recognition-plan row (six lines), and now also by EC1's two strings, which IDS's copy carries and PIDS's does not.

## §4a

`atom-section-4a.md` (20270 B, `f21e1ef7…`) is the exact text the ATOM:366 override appends after `\n\n---\n\n`. ATOM's own lines 367 to 369 then separate it from §5. It has four parts:
1. a heading;
2. a preamble that resolves the law's internal references ("item N", review ids, short names, line citations);
3. law lines 88 to 221, which are items 2.1 to 2.9, **verbatim** (sha256 `0983e395…` of the block);
4. the successor precisions P0 to P7.

The precisions fix choices the verbatim text leaves open. Each one is the reference model's behaviour:
- **P0.** The atom is evaluated once per rule, never by §8's per-subject API. §§5 to 9 apply only through §7's registry and its uncertain-id retention.
- **P1.** Cause universes on uncertain edges: `target-kind-unknown` and target-side `population-unknown` take `targetUniverse`, and importer-side `population-unknown` takes `sourceUniverse`. An edge carries every cause that applies to it.
- **P2.** 2.5 runs the prelude once, and its P2 return is the only return. Universes are accounted in ascending order with no return across them. `selector-unbound` ends that universe's account. Within a universe every scope is cited, every unpaired scope is a cause, and every paired Coverage is evaluated: outgoing step 3's return is not taken.
- **P3.** Unique rows: byte-identical observations count once, and one id at two paths is not unique.
- **P4.** An unresolved edge whose referrer maps to no selected vertex is in no witness. RC-2 counts it through 2.5(c).
- **P5.** Census causes carry `nativeCause` null. An inventory's own carrier is cited through EI.
- **P6.** Members sort by the representative order.
- **P7.** 2.5(c) consumes the native `sufficiency_v2` answer under the fixed requirement, and its unsatisfied `DeficiencyV2` values are `nativeDeficiencies`.

## Deviations from law r2 (cross-law items)

These were found while writing the exact bytes. Each is resolved by a lead decision below; the law text itself is not edited.

1. **JSON passages cannot be passage overrides.** Item 4 lists PDS:296-303, PDS:937-944, IDS:1221-1231, IDS:2781-2791 and IDS:4978 as passage overrides. In a v4 lock, `verify_design` refuses line selectors on a JSON parent ("v4 JSON parent passages require JSON Pointer selectors"). A JSON Pointer override replaces exactly one string value, so it cannot append to an array. The enum appends are therefore carried by complete successor copies, the form 468a used for its common4 enum. `majorLaw`, which is a string, rides in the same copies, so each document has one successor text.
2. **Inexact anchors.**
   - WS:598 contains no `` `all-covered` `` code span. The token sits inside `` `exists|none|count-at-most|all-covered` ``, so the insertion follows that span.
   - "WS:603-604" and "IE:213-214" each change one line: 603 and 214.
3. **"Append after `all-covered`" against "changes no ... order".** For IDS, item 4's table says "after `all-covered`", which would move `and`, `or` and `not` one place. Item 3.1 says the member is "appended". The IE passage says the exception "changes no other field, member, bound, order, recipe or prefix". The member is appended last (LD-L3).
4. **Item 4's list is incomplete.** Five more passages enumerate the closed set, and each would be false or incomplete with an eighth member:
   - IE:1266 ("one of the seven evaluator predicates");
   - IE:1334 ("whose seven evaluator predicates are closed");
   - IE §4's predicate table (IE:1539-1545);
   - COMP:109's atomic-node list;
   - PDS's and PPDS's `description` ("exactly the evaluator's predicate set ... (exists, ..., not)").

   Item 4's "IE changes only by the one passage above" is therefore inexact. Its purpose, a narrow identity-law change, still holds: the three added IE passages restate a count or a table row and add no rule.
5. **WS has a selected effective copy**, WSE, with the same two lines at 602 and 607. The law names only WS.
6. **The parents carry bound overrides.** The law does not say how a copy treats them. Copying raw bytes would silently revert four accepted meanings (LD-L2).
7. **Items 2.3 and 2.5 leave choices open** that fix proof bytes: P0 to P7. Item 2.9 accepts "the causes", so the choices belong in the contract, not in I1-b2.
8. **The projection registry's `AtomSuccessorV1`.** `evaluator-projection-registry.v1.json#/$defs/AtomSuccessorV1` (lines 1577-1633) carries the four-op enum, a second copy of PDS's `AtomSuccessorV1`. Item 4 keeps the registries unchanged, and neither copy is referenced by any schema, model or product file. It stays four-op and is disclosed here.
9. **UNITS I1-a, as written, is incomplete for `verify_design`** (see "For I1-a").

## Lead decisions

| ID | Decision | Rejected |
|---|---|---|
| LD-L1 | JSON changes are complete successor copies at new paths (468a's form). Their parents are listed in `parents`. | Line selectors on JSON (refused by the v4 lock); pointer overrides (cannot append to an array); a new `verify_design` profile for array appends (a tooling unit and its review, for one enum). |
| LD-L2 | A copy is its parent's **effective** text: raw bytes with the overrides the lock binds to that path applied in place, plus I1's edits. | Raw-parent copies: they would revert predicate-matching-v2's ASCII ordinals, stage-meta's registration law and EC1's two closure annotations. Adding EC1's text to PIDS: EC1 chose not to override PIDS, and that is not I1's question. |
| LD-L3 | `cycle-representative` is the **last** member of every enum, so no existing member moves. | Inserting it after `all-covered` in IDS, which moves three members against the IE passage's "changes no ... order" and 468a's practice. |
| LD-L4 | The five consequential passages of deviation 4 are included, each insertion-only. | Leaving them false; holding I1-L for a law r3, when they add no rule. |
| LD-L5 | WSE gets WS's two overrides, as X12-0 and initial-root-binding-owner-selection-v1 overrode both WS copies. | Overriding WS alone, which leaves the selected effective copy contradicting it. |
| LD-L6 | §4a is the law's items verbatim, with a resolving preamble and the precisions P0 to P7. | Editing the verbatim text; leaving the open choices to I1-b2. |
| LD-L7 | The law snapshots `PROPOSAL-r2.md` and `UNITS-r2.md` are candidates, as F8b's accepted proposal was. So I1-P can name the law as an accepted parent. | Leaving the law outside every subject. |
| LD-L8 | **Binding.** After acceptance the lead appends I1-L's `contractSuccessors` entry to `design-lock.json` in a binding-only product commit (D3's form), before I1-a. Selecting I1-L changes no product byte and no generation source: the source maps still pin the parents, which stay accepted. No worktree is staged tonight, because the product is read-only for this run. | Binding inside I1-a's commit, which would mix review subjects. |

## Reference model and cases

`evidence/cycle_representative_model.py` is the harness oracle of law item 8. It is built on the design encoder `foundation/canonical.py`, which gives the canonical sets and the H identities of the synthetic fact2, scope2 and coverage2 ids. It implements:
- the op law (2.2);
- the graph (2.3);
- the value table (2.4);
- graph completeness (2.5);
- the witnesses (2.6);
- the finding parameters (2.7);
- composition's outcome for the one gating rule (COMP:56).

`evidence/check_cycle_representative.py` runs 41 cases and 5 op-law refusals, and writes `evidence/cases-report.json` (20448 B, `01429737…`):
- QCM's eight corpus projects, with UNITS's expected results;
- an S = 0 project;
- UNITS cases 1 to 19, all variants;
- seven extra discriminating cases for 2.3 and P1 to P3: a syntactic-specifier fact, a first-party symbol target, an unmapped symbol target, an edge leaving to an unselected file, identical inventory rows, a foreign-family unavailable binding, and a second, unbound universe.

Every case also checks three things:
- five seeded permutations of every input list give identical result bytes (item 2.9);
- an independent SCC algorithm (Kosaraju beside Tarjan) gives identical bytes;
- no indeterminate value lacks a blocking cause.

The 1000-module chain builds its graph once.

Outcomes, in brief:
- `cycle` and `self` fail with one finding each, on `cycle/a.ts` (members `cycle/a.ts` and `cycle/b.ts`) and on `self/self.ts`.
- `acyclic`, `empty` and `shadow` pass with no cause.
- `unresolved`, `malformed` and `dynamic` are indeterminate with `coverage-unknown`.
- Case 15 is indeterminate with exactly `uncovered-expected-source-subject`, whatever the cell's `required` flag.
- Case 19 is indeterminate through composition, with the atom false at `a.ts`.

The model takes the native `sufficiency_v2` answer as input (P7). It does not model owner admission, sidecar joins, budget charging or the M4 renderer.

## For I1-a

`materialization-map.json` gives the two product files I1-a copies byte for byte:
- `schemas/sources/identity-v3.schema.json`: 197480 → 198423, `311c1feb…` → `eb6ec957…`;
- `schemas/sources/policy-v2.schema.json`: 26534 → 26677, `b221b5ed…` → `0ff24ae6…`.

UNITS r2's I1-a line references move as follows:
- the identity enums are now `:1221-1232` and `:2782-2793`;
- `majorLaw` is now `:4986`;
- policy `Atom.op` is now `:296-304`.

Two descriptions also change: `program-predicate` and the stage-spec registration law, through the carried overrides. So I1-a's regeneration may move generated doc text as well as the enums.

**What `verify_design` will require of I1-a, beyond UNITS r2:**
- **Source maps.** The generation and admission source maps must re-point `architectureSource` from PIDS and PPDS to these two copies.
- **A contract-successor record.** `admission_sources` requires the product's `schemas/admission-registry.json` to equal an accepted architecture copy whose rows carry the new source digests. So I1-a needs a record of 468a's form, carrying its new admission registry, as well as its inventory successor.
- **The atom registry.** `crates/evaluator/src/atom-registry.json`'s `fieldFilterSchema` pin moves to `design/workflows/schemas/policy-document.v2.schema.json` here. Its path changes as well as its digest. `scannerIdentitySchema` moves to the PIDS copy's bytes.

## Evidence and checks

All runs used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo, a product tool or a test.
- **`evidence/build_i1l.py --product <opensip>`** rebuilds every generated file of this unit and the subject. It reads the product's `design-lock.json` and the base blobs at `3e64266` with `git show`. `--check` compares instead of writing, and two runs were byte-identical.
- **Its checks restate `verify_design`'s `contract_successor` and `successor_chain` rules for this record:**
  - every parent is an accepted base or an accepted successor member, at its pinned bytes;
  - every `before` equals its parent line;
  - line selectors are used only on non-JSON parents;
  - no selector is already bound;
  - the candidates equal the subject minus the record;
  - no candidate path is already accepted.

  It also checks each copy:
  - it parses to its parent with exactly the stated edits;
  - the PDS relation holds;
  - the product base blobs equal PIDS and PPDS.
- **`evidence/check_cycle_representative.py --deps <dir>`** runs the cases. The design encoder imports `jsonschema`, installed offline from `~/opensip-deps/wheels` (jsonschema 4.25.1 with attrs, referencing, rpds-py and jsonschema-specifications) into a scratch `--target` directory. Without `--write` it compares with `cases-report.json`.
- **Not run tonight:** the real `tools/verify_design.py`, with this record appended and a synthetic review. The machine is reserved for crash-matrix timing work, and the run is limited to docs. The lead runs it at binding (LD-L8). I1-P's evidence validates the pack document against these copies with the exact schema profile.

## Not changed, and noted

- PDS's `AtomSuccessorV1.filters` already `$ref`s `#/$defs/FieldFilterSuccessorV1`, which PDS does not define. That is pre-existing, and nothing validates against `AtomSuccessorV1`. Not changed.
- EC1's annotations are absent from PIDS's meaning, by EC1's own choice. Not changed.
- No product, inventory, registry, generated-code or review file is touched.

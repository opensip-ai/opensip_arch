# Erratum FA2-CENSUS-E1: a symbol census is complete over a named population rule (author draft r2, 2026-11-13)

Status: **PROPOSED, r2.** It implements lead decision LD-DEC-11 items 1-5, 6' and 7-8
(`LC/decisions/LD-DEC-11-census-population/DECISION.md`, including its section "Corrections 2026-11-13 after both reviews
of the erratum"; `LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It answers both reviews of r1
(`b097e3d9e`): `review-opus/VERDICT.md` (R1-R3, A1-A5) and `review-codex/VERDICT.md` (FCE-CX-1, FCE-CX-2), both
REQUIRED-FINDINGS. The changes are listed in FCE1.11. It is **additive**: the accepted bytes stay frozen.

Corrects one accepted text: **contract successor FA-2** (native-evidence §9.8, the symbol census), at architecture main
`12084f90d` (unchanged at `8b09ee249`), as pinned by its subject manifest `native-successors-fa/fa-2-subject.json`:
- `docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md`, 8,270 bytes, sha256
  `2769b0935a7e1fd0d8b7a76c245d44dee7cd08588379f21a34f2be17c2e2e6c0`;
- `docs/implementation/m3/native-successors-fa/fa-2/README.md`, 37,836 bytes, sha256
  `59381765049d16320eb8d1886fb0f5a51651485d0e3c9ddea3641d5691225af7`;
- the record's own copy of §9.8: `fa-2/successor.json:174`. That line is the `after` text of the override whose selector is
  native-evidence line 3313 (`:171`). It carries `9.8:3-5` and `:56-57` verbatim.

Line numbers below are those files' (`9.8:N`, `README:N`).

**Which record form applies.** FA-2 is a lock input: the product's `design-lock.json` (product main `fc28bce2`) binds it
as a `contractSuccessors` entry, record `fa-2/successor.json` (38,659 bytes, sha256 `f6b105f4…`) at `:7840`, subject
manifest at `:7845`, review `reviews/codex-fa-2-r2/review.json` at `:7850`, assent `fa-2-unit.json` at `:7855`. So, like
VCS1-E1 (`../errata-2026-11-13/ERRATUM-VCS1-E1.md`), this correction needs a contract successor. This file is its text;
the record and its parts are owed (FCE1.9).

Product facts (read-only): branch `f2min-fix-1-r1` at `61ae5fb2fdeacfcc161587d8a45bd52bb9d05c7b`, worktree
`opensip-fix-f2min` (`P` = `providers/typescript/src/facts`). Design note: `LC/f2min/DESIGN-NOTE-r5.md` (`N`). "Probe"
below means a result the two reviewers obtained by running the code; this author ran nothing.

## FCE1.1 The accepted sentences

`9.8:3-5` (and its copy in `successor.json:174`):

> A TypeScript or Rust provider's symbol census is its explicit population assertion (the header above; identity §4): the first-party symbols its program declares over the binding's symbol extent (enumeration contract §5), with the paths it examined.

`9.8:56-57` (and its copy in `successor.json:174`):

> Rows name first-party symbols only: an external symbol is not a row, and a symbol with no fact is still one.

`README:282` (cascade row X-FA2-FG, column "Item"):

> The emission duty of §9.8: the census in the same compiler pass; rows for every first-party symbol, including those with no fact; every source-side subject of the worker's symbol-kind candidates has a row; no external symbol is a row; scope2 computed with the foundation encoder, conformance-tested on `vectors.json`. Signed capability rows of releases that implement it carry `symbol-census-v1`.

**Why they cannot stand for TypeScript.** The TypeScript census does not hold every first-party symbol. Its walk reads
only the file's top-level tables, the export tables and the members of named containers (`P/census.ts:237-340`). A symbol
in a function or block scope gets no id (`:442`), and anonymous symbols are skipped with their members (`:134`, `:657`).
The exclusion was a design-note choice (`N` §2 P5, §6) that never reached law. The reviews also found that the code does
not hold one consistent population either (FCE1.3, "fix owed"). The counts are in `LC/f2min/fix-1/CX4-OPTIONS.md` §4.

## FCE1.2 The amendment

**`9.8:3-5`** is read as:

> A TypeScript or Rust provider's symbol census is its explicit population assertion (the header above; identity §4) under one named population rule: the first-party symbols its program declares over the binding's symbol extent (enumeration contract §5) that the rule selects, with the paths it examined. The default rule, `native.symbol-census-population.default.v1`, selects the first-party symbols its program declares over the binding's symbol extent, all of them. A census's rule is the population-rule binding of its enumerator closure (below); a closure whose binding names no other rule is under the default rule. Only a rule stated in this section can be bound. A census's `complete` state and its row count describe its rule's population and no wider one. Rule ids are immutable (erratum FA2-CENSUS-E1).

**`9.8:56-57`** is read as:

> Rows name first-party symbols of the census's population rule only: an external symbol is not a row, a declaration the rule excludes is not a row, and a symbol the rule includes that has no fact is still one.

**`README:282`**: the words "rows for every first-party symbol, including those with no fact" are read as:

> rows for every first-party symbol of the census's population rule (§9.8 as amended by FA2-CENSUS-E1), including those with no fact

The rest of `README:282` is unchanged.

**Inserted into §9.8 after `9.8:11`:** the rule of FCE1.3 (its first two columns and the sentences quoted there), and the
paragraphs quoted in FCE1.4, FCE1.5 and FCE1.7. They are the rule's only statement. The default rule is the accepted
wording, so Rust's obligation is unchanged (LD-DEC-11 item 1).

## FCE1.3 The TypeScript rule `native.symbol-census-population.typescript.v1`

Inserted into §9.8:

> **The TypeScript population rule `native.symbol-census-population.typescript.v1` (erratum FA2-CENSUS-E1).** Under this rule a census row is a declaration in an extent code file of a class the table marks included, and of no other. A class holds in module files and script files alike unless the table says otherwise. The census does not fail as a whole because a declaration of any class, included or excluded, is present. It never has a row for a name that is not a binding in the scope its id names. An included declaration that fails the provider's id checks ends the Analyze without `Complete` (`9.8:64-65`); it is never left out silently.
>
> Members are rows when they have a declaration in an extent file. A seed (a file, a global declaration, an ambient module) is walked even when its symbol also has declarations outside the extent. A nested container is walked only when it has a declaration in an extent file.
>
> **The two-copies rule (R2) reaches this rule's population only.** An external name is ambiguous when two distinct named external symbols that this rule's walk reaches compute it. A symbol reached only from a declaration this rule excludes does not count.

The table. Its first two columns are the rule. Its last two record the code at `61ae5fb2` and are not inserted.

| # | Declaration class | Rule | Code at `61ae5fb2` (`P/census.ts` unless named) | Status |
|---|---|---|---|---|
| C1 | Each examined code file. A module's own symbol is that same row. | included | file row `:582`; module symbol seeded `:583-584`, not emitted again `:699` | matches |
| C2 | A JSON root (examined) | excluded | `:568` | matches |
| C3 | Module top level: each entry of a module file's top-level binding table that is not excluded by C19, of any declaration kind (variables and destructured names, functions, classes, enums, interfaces, type aliases, namespaces) | included | `:292-307` | matches |
| C4 | A `var` in a block or `for` head at a module file's top level (it hoists into that table) | included | enters the table (`:292`), but the scope test (`:199-210`) gives "other", `idOf` gives null (`:442`), and the whole census fails at `:712`. Probe: `internal: walk id ts-symbol:b.ts#i != idOf null` (R1; FCE-CX-1) | fix owed |
| C5 | A module file's export entries with no binding in the file: CommonJS `exports.x =`, `module.exports.x =` and `Object.defineProperty(exports, 'x', …)`; a top-level `this.x =` in a CommonJS file; an export declared only by a module augmentation; a `module.exports = …` value that is not an alias; a default-exported value | included | `:308-313`. Probe: top-level `this.x =` gives `d.js#(export).b` (R3 (b)) | matches |
| C6 | JSDoc `@typedef` and `@callback` at file scope | included | module and CommonJS files: rows through the top-level table (`:292`). Probe: `a.js#T`, `d.js#T`. Script files: no row and no report; the seed scan reads JSDoc only for the byte check (`:602-615`) (R3 (c); FCE-CX-1 (a)) | module: matches; script: fix owed |
| C7 | Global declarations: each declaration declared at global scope, meaning directly in a script file's statement list (a variable statement's names included) or in a `declare global` block. The expression initializing such a variable is not itself a declaration of this class (C22, C23). | included | seed scan `:619-622`, scope test `:199-210` | matches for the declarations themselves; see C22, C23 |
| C8 | A `var` in a block or `for` head at a script file's top level (a global binding) | included | not seeded: the scope test (`:199-210`) gives "other"; omitted silently (FCE-CX-1) | fix owed |
| C9 | A top-level `this.x =` in a script file (the compiler binds it as a global; R3 (c)) | included | not seeded: the scope test gives "other"; omitted silently (R3 (c)) | fix owed |
| C10 | A string-named `declare module` declared at global scope (`:212-214`) | **open** (FCE1.10, open point 1) | seeded `:616-618`; a row `#"m"` | not decided |
| C11 | A string-named `declare module` in a module file whose target is a file of the program (an augmentation); its declarations merge into that module | included, as declarations of C3, C5 and C13-C17 of the target | augmentation seeds `:616-618`; corpus cases N4a-N4c and N5a-N5d (`N` §8) | matches |
| C12 | A string-named `declare module` that is not at global scope and whose target is not a file of the program, with its declarations | excluded; it never makes the census incomplete | no row; the census completes with the note `A7 no id for seed` (`:690-697`). Probe: `export {}; declare module "absent" {…}` (FCE-CX-1 (b)) | population matches; the A7 note wrongly calls this case A7: disclosure fix owed |
| C13 | Members of a class or interface: instance members (parameter properties and the JavaScript `this.x =` and prototype-assignment forms included) and call, construct, index and constructor signatures | included | `:317-322`, `:224-233` | matches |
| C14 | Static members of a class, other than `prototype` | included | `:330-335` | matches |
| C15 | Properties of a JavaScript constructor function's construct signature | included | `:323-329` | matches |
| C16 | The non-alias entries of the export table of a reached container: namespace exports, enum members and a function's or class's assigned properties | included | `:336-338` | matches |
| C17 | Expando members of a variable that the compiler makes an expando container (`const f = () => 1; f.x = 1`; JavaScript `var o = {}; o.x = 1`) | included | `:336-338`. Probe: `#f.x`, `#o.x` (R3 (a)) | matches for the probed files; script files: to be settled by CENSUS-RULE-1's golden, by principle (c) |
| C18 | A namespace export that is an alias merged with a namespace or other declared meaning, with its descendants | included (as at module top level, where only a pure alias is excluded) | skipped with its descendants by the any-alias test of `:337`, unlike the pure-alias test of `:274` and `:293`. Probe witness, which also has a compiler diagnostic: the census completes without them (FCE-CX-1 (c)) | fix owed |
| C19 | Aliases with no declared meaning of their own: imports, import-equals declarations, export specifiers, re-exports, and the JavaScript `const x = require(…)` and `const {a} = require(…)` forms | excluded | `pureAlias` `:216`, applied `:274`, `:293`, `:455` (A1: the compiler binds the `require` forms as pure aliases) | matches |
| C20 | Function and block locals other than C4 and C8, catch variables included; non-exported declarations of a namespace block; local function, class, enum, interface, type-alias and namespace declarations | excluded | not in any table the walk reads (`:237-340`); `containerOf` gives no id (`:442`) | matches |
| C21 | Parameters, other than parameter properties; type parameters | excluded | as C20 | matches |
| C22 | The names of function expressions and class expressions | excluded | module files: not reached; matches. Script files: the scope test climbs from the initializer to the file (`:203`), and the seed scan seeds the expression (`:619-621`). Probe: `var f = function g(){}` and `const C = class Named {}` give rows `ts-symbol:#g` and `ts-symbol:#Named`, which are not bindings; with another global `function g`, the census fails X4 (R2). Whether a class expression's members also become rows through the walk of that seed (`:703`) is to be settled by CENSUS-RULE-1's golden, by principle (b) | module: matches; script: fix owed |
| C23 | Symbols the compiler leaves anonymous, with every member under them: function and arrow expressions, class expressions, object literals (`module.exports = {…}` and `export default {…}` objects included), type literals, JSX attribute sets | excluded | `ANON` `:134`, skipped with members `:657`. In script files the seed scan also seeds them as C22's are, and reports `A7 no id for seed __function` / `__object` / `__type` (`:690-697`; A5), though they are not A7 | rows: matches; disclosure fix owed |
| C24 | JavaScript forms the compiler binds to no symbol, such as `exports[k] = …` | excluded | no symbol, no code | matches |
| C25 | Compiler-internal entries of the top-level tables: `__export`, `__global`, the CommonJS `module` symbol, and a string-named entry that is not an ambient module | excluded | `isBogusTop` `:217-220` | matches |
| C26 | The four A7 cases: a member with no compiler symbol (a computed or bigint name the checker does not bind, or a late-bound key with no unique-symbol declaring symbol); a member keyed by a unique symbol whose declaring symbol has no id under this rule; a member of a `node_modules` file with no package segment; a member whose id depends on an ambiguous external name | excluded | `:624-631`; `segOf` `:381-383`; `homeOfFile` `:365`; R2 `:466-470`, `:671-677`, two passes `:735-737` | matches |

C6's script fix needs no new id rule. A script file's file-scope declaration is global, and the grammar has the global
form `"ts-symbol:#" top` (`providers/typescript/SUBJECT-IDS.md:18`; `globalId` in `P/subject-ids.ts`). So principle (c)
includes C6 in both file kinds. C8 and C9 take the same global form.

## FCE1.4 Relations under the TypeScript rule

Inserted into §9.8 after the rule:

> **Relations under `native.symbol-census-population.typescript.v1`.** Only `imports` and `unresolved-edge` are advertised under this rule. Their source field (`importer`, `referrer`) names the row of the file that holds the import site, wherever in that file the site is. Any other symbol relation needs its own reviewed law for the attribution of its source and target fields before it is advertised under this rule.

Verified, and confirmed by both reviews: `P/candidates.ts:63-77` builds both fields from `moduleSubjectId(o.site.file)`
(`P/subject-ids.ts:154-158`), and the target of `imports` is a file id (`:68`). This erratum makes no statement that a fact
is attributed to an enclosing row. That would be an aggregation needing its own relation law (`VERDICT-3-fix1.md`).

## FCE1.5 Widening

Inserted into §9.8 after FCE1.4:

> **A wider population is a new rule.** It has a new rule id; an id is never re-used for another population. A wider rule is not promised to be additive: under it a row of this rule may get another id or no id. Runs made under different rules are not promised to be comparable. An excluded declaration is outside the census's evidence; its absence is never proof that it does not exist, is unused, or is safe to change.

Why it is not additive:
- **R2.** A wider walk reaches more external symbols (for example through the computed keys of members of local classes).
  An external name reached once under this rule can then be reached twice and become ambiguous. A row that depends on it
  falls into A7 case 4, and its id disappears.
- **A7 case 2.** A member keyed by a unique symbol whose declaring symbol is a local has no row here, but would have one
  under a rule that gives locals ids.
- **Ids.** G1 (`SUBJECT-IDS.md:18`) has no form for a declaration inside a function or block (`CX4-OPTIONS.md` §3).
- **Attribution.** A relation under a wider rule may name a source this rule cannot name.

## FCE1.6 Consumers (obligations owed; nothing is implemented)

- **The evaluator's own erratum.** It is owed by the owner of `foundation/evaluator-composition-contract.v3.md`, before any
  symbol-kind or export-kind rule ships. The obligation: a rule whose primary subjects include declarations outside the
  population rule of the census that covers it is refused or reported incomplete, never complete-empty and never pass.
  Today a complete covering inventory can give complete-empty (`evaluator-composition-contract.v3.md:26`). The product
  checks kind and state, not the population rule (`crates/evaluator/src/input_reconstruction.rs:259-290`, `:347-355`, per
  FCE-CX point 5; source reading, not a Run). M3's one rule, `module-import-cycle`, is file-kind and is not affected. The
  path document carries the gate until that erratum is bound (`LC/coordinator/PATH.md:110-113`).
- **The reporting and command-line units.** Every surface that reports symbol completeness names the rule id of the
  census behind it.
- **No wire member, schema member, deficiency or cause** is added (`9.8:107-108`). The carrier is FCE1.7's.

## FCE1.7 Binding the rule to the code

Inserted into §9.8 after FCE1.5:

> **Each enumerator closure has exactly one population-rule binding.** It is immutable, it is reviewed, it is available before Plan selection, and it is retained for replay. A census request whose enumerator closure has no binding, or has conflicting bindings, is refused. Evidence made under a binding keeps that binding's rule when it is read later. Until the carrier of this binding exists, a provider does not claim a `complete` census under any rule other than the default.

What this means for the code (LD-DEC-11 items 6' and 8; FCE-CX-2):
- **A note alone is not enough.** The product's token note is pinned by digest (`tools/typescript_closure.py`
  `bound_tokens`, `:211-235`) and recorded in the closure build record (`:465-466`). But P's `closure2` covers the dist and
  the note's token and relation lists (`:446-452`), not the rest of the note. Changing only a rule sentence in the note
  changes neither the enumerator closure nor the Plan's census request. The note may name the rule id, but the binding
  must be carried by something the closure identity or the Plan fixes. That carrier is owed: it is part of CENSUS-RULE-1,
  or a unit of its own.
- **CENSUS-RULE-1 is the code fixes of FCE1.10 plus the conformance golden, tests first.** The golden has one case per
  class of FCE1.3, plus controls that fail when a class is added or dropped. Its cases fail at `61ae5fb2` before the fixes
  for C4, C6, C8, C9, C18, C22 and C23. The provider does not send `complete` under
  `native.symbol-census-population.typescript.v1` until CENSUS-RULE-1 is accepted and the carrier exists.
- **The existing 98-case corpus** (`src/test/census-corpus.test.ts` against `fixtures/census-golden.ts`) is the design
  note's. It is not organised by class, and it passes at `61ae5fb2` while the defects above stand, so it is not this
  rule's conformance evidence.
- No product code is changed by this erratum.

## FCE1.8 What this does not change

- **The census schema.** `fa-2/design/native/symbol-census.schemas.v1.json` (19,045 bytes, sha256 `95d84054…ad21`) is not
  edited. It is pinned byte for byte as `opensip.product.symbol-census.1` (`opensip/tools/replay/id-ledger.json:435`). It
  states no population: `:12` defines the variants by size, and `:111` and `:138` hold for every row under either rule.
  `:7` makes it a restatement of §9.8, and the two do not differ after this erratum. Both reviews confirm this.
- **The enumeration contract** (`enumeration-contract.v1.md:119`, `:132`, `:178`, `:186`). `complete` for `kind=symbol` is
  defined by examined paths with no row totality, so these lines need no amendment.
- **The rest of §9.8**: the extent, `examinedPaths`, the variants and bounds, the commitments, the terminals and refusals.
  `9.8:64-65` stands.
- **No wire member, deficiency, cause, D9 code, frame, token or schema** (`9.8:107-108`).
- **The evaluator contract** is not amended here. Its amendment is its owner's (FCE1.6).
- **Rust.** It is under the default rule, which is the accepted wording.

## FCE1.9 Controls, review and binding owed

**Controls:**
1. CENSUS-RULE-1's golden: one case per class, tests first, failing before the fixes, with controls that fail when a class
   is added or dropped.
2. The population-rule carrier of FCE1.7 exists before any `complete` census is sent under the TypeScript rule.
3. The evaluator owner's erratum is bound before any symbol-kind or export-kind rule ships (FCE1.6).
4. **The item 7 measurement is recorded before the body-parser Run.** On fixture `js-small-body-parser`: whether the
   package's public surface falls into the excluded classes (C23 objects and their members, C20 nested functions and
   callbacks), with the count. The counts so far are `CX4-OPTIONS.md` §4's; that table does not say what the public
   surface is. A miss goes to the lead before the Run is recorded.

**Review: two independent reviewers**, both independent of the DESIGN-NOTE-r5 rulings (LD-DEC-11 item 6).

**Binding owed (not generated):** a contract successor that overrides `section-9-8.md`, `README:282` and the §9.8 copy in
`fa-2/successor.json:174`. It carries FCE1.2-FCE1.5 and FCE1.7's binding paragraph as operative text. With it come its
subject manifest, the two reviews, the unit assent and one `contractSuccessors` entry in the product's `design-lock.json`.
The choice between a replacement FA-2 record and a second successor is the binder's, as in VCS1-E1.6. Adopting the law can
come before CENSUS-RULE-1. Using the narrowed `complete` claim cannot.

## FCE1.10 Code fixes owed, and open points

**Code fixes owed (CENSUS-RULE-1, tests first):**
1. C4: a `var` hoisted from a block or `for` head into a module file's top-level table gets its row; today the whole census
   fails (`:199-210`, `:442`, `:712`).
2. C8: the same `var` in a script file gets its global row; today it is omitted.
3. C6: file-scope JSDoc `@typedef` and `@callback` in a script file get global rows; today they are omitted.
4. C9: a top-level `this.x =` in a script file gets its global row; today it is omitted.
5. C22: the script seed scan takes the declaration only, not the expression initializing it (`:203`, `:619-621`); the
   fabricated rows `#g` and `#Named` disappear.
6. C18: a namespace export alias merged with a declared meaning is walked like its module-top-level counterpart (a
   pure-alias test at `:337`).
7. C12 and C23: the stderr A7 notes stop calling an absent-module augmentation or an anonymous initializer A7.
8. FCE1.7: the population-rule carrier (here or as its own unit).

**Open points:**
1. **C10, a string-named `declare module` at global scope, is not decided.** Two readings pull against each other:
   - *Included:* principle (a) (a named global binding) and principle (d)'s first clause (name the code's deliberate,
     consistent choice as it is). The code gives it a row `#"m"` (`:616-618`), and `N` P1 and T3 make that deliberate.
   - *Excluded:* principle (d)'s last clause, "an ambient declaration of a module that is not a file of the program is
     excluded by name". Read literally, that covers this class whenever no file of the program is that module.

   Rule ids are immutable, so the lead decides before the rule is adopted. If the class is excluded, the code fix is to
   drop the row, and the package-augmentation cases (`N` §8 N5) must be re-read, since they merge into the same home.
2. **To be settled by CENSUS-RULE-1's golden, not probed:**
   - C17 in script files (principle (c));
   - the members of a class expression seeded in a script file (C22; principle (b));
   - whether a script's `this.x =` (C9) and a `var x` of the same name are one subject or fail X4 (principle (b)).
3. **Where `N` differs from the code or this rule:**
   - `N` §6's nearest-enclosing-row attribution (the code names the file);
   - `N` §10's "only adds ids";
   - `N` P5's "members of anonymous containers" (an anonymous default-exported class declaration's members are rows,
     `N` §8 W4);
   - `N` P1's "file row plus module symbol" (one row);
   - `N` §0's normative reference against `P/census.ts:1-4`, which still names `census-r4.cjs`.

   Under this erratum, the rule is FCE1.3's table, and `N` owes corrections.
4. **Rule ids proposed by the author.** No hit in the architecture, product or F2-min repositories, or in `LC/decisions`.
   The form follows `native.semantic-universe.typescript.v2`. The default rule's id is given so that a surface can name the
   rule of a Rust census.

## FCE1.11 Changes from r1 (`b097e3d9e`)

| Finding | Change |
|---|---|
| Opus R1; FCE-CX-1 (`var`) | C4 is included, with fix owed (the census fails today); C8 is included, with fix owed |
| Opus R2 | C22 is excluded; the script rows `#g` / `#Named` are a code defect, with fix owed. r1's table row claiming "no id" is gone |
| Opus R3 (a) | C17 names expando members of a variable |
| Opus R3 (b) | C5 names the top-level CommonJS `this.x =` |
| Opus R3 (c); FCE-CX-1 (a) | C6 (JSDoc) is included in both file kinds, by principle (c), with a script fix owed; C9 (script `this.x =`) is included, with fix owed |
| Opus R3 (d); FCE-CX-1 (b) | C10 uses the code's global-scope test and is left open (open point 1); C12 excludes the absent-module augmentation by name |
| FCE-CX-1 (c) | C18 is included, with fix owed |
| FCE-CX-2 | FCE1.7's binding invariant replaces r1's "the token note's digest binds the rule"; the narrowed claim is not used until the carrier exists |
| Opus Q6; LD-DEC-11 6' | r1's "the golden passes on the code" is removed; CENSUS-RULE-1 is the fixes plus the golden, tests first |
| Opus A1 | C19 names the JavaScript `require` alias forms |
| Opus A2 | FCE1.6 makes the evaluator gate its owner's erratum |
| Opus A3 | FCE1.9 names `fa-2/successor.json:174` |
| Opus A4 | FCE1.3 says that outside-extent containers are walked only for seeds |
| Opus A5 | C23's disclosure fix is owed |
| FCE-CX points 7-8 | FCE1.9 makes the binding paragraph operative, and FCE1.5 adds the "not proof of absence" sentence |

# Erratum FA2-CENSUS-E2: what "alias" means in the TypeScript census rule (author draft, 2026-11-13)

Status: **PROPOSED.** It makes law the lead's reading in LD-DEC-11, section "Reading needed after the code reviews
(2026-11-13): class-expression exports (the reviewers' "A1")" (`LC/decisions/LD-DEC-11-census-population/DECISION.md`;
`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). It resolves the two readings of the CENSUS-RULE-1a
reviews: `LC/f2min/census-rule-1/review-opus/VERDICT-r2.md` ("The two readings", A1) and
`LC/f2min/census-rule-1/review-codex/VERDICT-r2.md` point 3. It is **interpretive and additive**: no accepted byte is
edited.

Reads one bound text: **erratum FA2-CENSUS-E1 r5**, `docs/implementation/m3/errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md`
at architecture main `c229e75d6`, 32,962 bytes, sha256 `1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1`,
adopted by `ADOPTION-FA2-CENSUS-E1.md` in the same directory. Line numbers below are that file's (`E1:N`). The rule is
`native.symbol-census-population.typescript.v1`.

**Form.** E1 is an erratum adopted by receipt, and the FA-2 contract successor that will carry it is owed and not yet
generated (the adoption receipt). This erratum takes the same form: the lead's adoption receipt, after two reviews. When
that successor is generated, it carries E1 as read here.

Code read (read-only): product worktree `opensip-fix-f2min`, branch `f2min-fix-1-r1` at
`8e4e0ad1e9101f90fefddf84a00dbdece0ab8279`, the last commit of code unit CENSUS-RULE-1a when this was written, read
with `git show` (`P` = `providers/typescript/src/facts`). That worktree held uncommitted edits to `P/census.ts`, which
were not read. The code unit's probes cited below were run at `7cd1fb16`. Its two later commits (`33f01007`,
`8e4e0ad1`) change C27 code and golden cases only; no line using the alias test or `isBogusTop` changed.
Compiler: TypeScript 6.0.3, `lib/typescript.js` in the provider's `node_modules` (`TS:N`).

## FCE2.1 The bound sentences

`E1:88`, class C5 (rule column: included):

> A module file's export entries with no binding in the file: CommonJS `exports.x =`, `module.exports.x =` and `Object.defineProperty(exports, 'x', …)`; a top-level `this.x =` in a CommonJS file; an export declared only by a module augmentation; a `module.exports = …` value that is not an alias; a default-exported value

`E1:102`, class C19 (rule column: excluded):

> Aliases with no declared meaning of their own: imports, import-equals declarations, export specifiers, re-exports, and the JavaScript `const x = require(…)` and `const {a} = require(…)` forms

`E1:105`, class C22 (rule column: excluded):

> Function, arrow and class expressions, named or not: their names, and every member under them, whatever the file kind. The members C17 binds to the variable holding the expression, and C27's, are not under this class

**Why a reading is needed.** The compiler flags the export entry of `exports.K = class …` and of `module.exports = class …`
as an alias: it binds an alias when the assigned value is an entity name or a class expression (`isAliasableExpression`,
`TS:19508-19510`; `bindExportsPropertyAssignment` `TS:49172`; `exportAssignmentIsAlias` `TS:19511-19514`, used at
`TS:49190`). The two reviewers read E1 differently for these entries:
- the Claude reviewer reads C19's list as closed, so C5 includes both entries;
- the cross-vendor reviewer reads C5's guard "a value that is not an alias" as excluding `module.exports = class …`, and
  finds `exports.K = class …` not settled.

## FCE2.2 The reading

> **Reading of `native.symbol-census-population.typescript.v1` (erratum FA2-CENSUS-E2).** Throughout the rule, "alias" has C19's meaning: a name that only refers to a declaration made elsewhere and has no declared meaning of its own, in the forms C19 lists (imports, import-equals declarations, export specifiers, re-exports, and the JavaScript `require` forms). It is not "any symbol the compiler flags as an alias". An export entry whose value is a class or function expression declares its meaning at that entry, so it is not an alias, and C5's guard in "a `module.exports = …` value that is not an alias" does not exclude it.

Ground (the lead's): principle (a), a named export entry is a declared symbol with a stable name; principle (c), one
treatment for one declaration kind. A function expression assigned to `exports.x` already has its row today.

## FCE2.3 The four forms

**Where they occur.** These are CommonJS forms. They bind an export only in a JavaScript file that has no ES `import` or
`export`, and binding one makes that file a CommonJS module (`setCommonJsModuleIndicator`, `TS:49124-49134`). In a
TypeScript file the compiler binds no CommonJS export (`getAssignmentDeclarationKind`, `TS:18768-18771`). So each form
exists only in a CommonJS module file. No script form and no ES-module form exists, and the reading needs none.

**Under the reading**, each export entry gets its row under C5. The expression's own name, and every member under the
expression, stay excluded by C22 unless C17 or C27 carves them out. Neither carve-out applies to these four forms:
- C17 binds members to a variable;
- C27 names "a variable that the checker treats as a JavaScript constructor".

So `module.exports = function () { this.p = 1; }` and `exports.K = function () { this.p = 1; }` get no `~p` member.

**What the code does at `8e4e0ad1`.** The census keeps an export entry only if it is not a pure alias (`pureAlias`
`P/census.ts:243`, applied to a module's export table at `:337`). An entry the compiler flags only as an alias is dropped,
with no row and no note.

| Form | Rows under the reading | Code at `8e4e0ad1` | Status |
|---|---|---|---|
| `exports.K = class Named { m() {} }` | `m.js#(export).K`; no `Named`, no members (C22) | no `(export).K` row, no `Named`, no members, no note. Evidence: code unit handoff probe A1a (`LC/f2min/census-rule-1/HANDOFF.md:99`); the alias flag comes from `TS:49172`, and the drop is at `:337` | fix owed (CENSUS-RULE-1a) |
| `exports.K = function g() { this.p = 1; }` | `m.js#(export).K`; no `g`, no `~p` (C22) | `(export).K`: present. The compiler binds the entry as `Property \| ExportValue`, not an alias (`TS:49172-49173`), so it passes `:337`. A reviewer's probe of the neighbouring form `exports.f = () => 1` gives `(export).f` (Opus `VERDICT-r2.md:77`). `~p`: absent by the code's paths. C27's member path takes only variables (`fnExprsOf`, `:264-275`; used at `:399`, `:403`). The instance side needs a class or interface flag (`:391`), and the constructor side needs a function flag (`:399`). The entry has neither: it is bound as a property (`TS:49173`). Not probed by anyone with this exact source | matches (from code reading and the neighbouring probe; the golden case confirms) |
| `module.exports = class Named { m() {} static s = 1; }` | `m.js#(export=)`; no `Named`, no members (C22) | only the file row: no `(export=)`, no members, no note. Evidence: handoff probe A1b (`HANDOFF.md:100`); the alias flag comes from `TS:49190`, and the drop is at `:337` | fix owed (CENSUS-RULE-1a) |
| `module.exports = function g() { this.p = 1; }` | `m.js#(export=)`; no `g`, no `~p` (C22) | `(export=)`: present. The compiler binds it as `Property \| ExportValue \| ValueModule`, not an alias (`TS:49190`). A reviewer's probe `module.exports = function named(){}` gives `(export=)` (Opus `VERDICT-r2.md:76`). `~p`: absent by the same code paths as row 2. Not probed with a `this.p` body | matches (from code reading and the probe; the golden case confirms) |

**The fix owed** (CENSUS-RULE-1a, after this erratum is accepted; until then the code is not changed for these forms and
no golden expectation is added, per the lead's reading). The census's alias test must exclude only C19's forms. An export
entry whose value is a class expression keeps its row. Its walk must not reach the class expression's own symbol or its
members (C22).

## FCE2.4 Standing of the rule id (for the reviewers to judge)

This erratum does not mint a new rule id. Its ground:
- **Nothing has used the rule.** No enumerator closure carries a binding to `native.symbol-census-population.typescript.v1`:
  the carrier is owed (E1 FCE1.7). The provider may not send `complete` under it until CENSUS-RULE-1 is accepted and its
  binding exists (E1 FCE1.7). No Plan or Run names it.
- So no historical evidence exists whose interpretation could change. The cross-vendor caution, "preserve
  immutable-id/historical interpretation rather than silently redefining v1", has no evidence to protect here.
- The reading is the meaning of v1 from its first binding. It is made law before that binding (LD-DEC-11, "Reading
  needed").

**The alternative.** If a reviewer holds that the reading changes v1's population and so needs a new id, then E1's table
is re-issued under `native.symbol-census-population.typescript.v2`, with C5 and C19 as read here. v1 stays bound and is
never used. The cost is a successor to E1 that restates the whole 28-class table under the new id. Every reference to the
v1 id would move to v2: the CENSUS-RULE-1 golden and code comments, the owed carrier and binding, and the owed FA-2
successor. The two reviews of E1 would be repeated for v2.

## FCE2.5 Golden cases owed in CENSUS-RULE-1a

One case per form, in a CommonJS module file (`m.js`, no ES `import` or `export`):
1. `exports.K = class Named { m() {} static s = 1; };`: rows `m.js` and `m.js#(export).K`; no `Named`, no `~m`, no `.s`;
   no A7 note.
2. `exports.K = function g() { this.p = 1; };`: rows `m.js` and `m.js#(export).K`; no `g`, no `~p`; no A7 note.
3. `module.exports = class Named { m() {} static s = 1; };`: rows `m.js` and `m.js#(export=)`; no `Named`, no members; no
   A7 note.
4. `module.exports = function g() { this.p = 1; };`: rows `m.js` and `m.js#(export=)`; no `g`, no `~p`; no A7 note.

No script case is owed: no script form exists (FCE2.3). The `exported` value of each row is the one E1 gives an export
entry.

## FCE2.6 What this does not change

- Every other class of E1's table (C1-C28): their wording, inclusion and status. The alias test of C3, C18 and C19
  (`E1:86`, `:101`, `:102`) already means C19's forms, and the reading states it for the whole rule.
- **The form the reviewers call "A2"** (`var o = {}; o.F = function () { this.p = 1; }; o.F.prototype.m = function () {};`)
  needs no erratum. Both reviewers find that E1 decides it: `#o.F~p` is excluded (C22; C27 names variables only), and
  `#o.F~m` is a row (C13).
- No schema, wire member, deficiency, rule id, carrier or binding. The rule id stays `native.symbol-census-population.typescript.v1`
  (FCE2.4).

## FCE2.7 Review and binding owed

- **Review:** both reviewers of E1, Claude and the cross-vendor reviewer (LD-DEC-11, "reviewed by both"), before the rule
  is first bound to any closure.
- **Binding owed:** the lead's adoption receipt pinning this file's sha256. The owed FA-2 contract successor carries E1 as
  read here.
- **Code owed:** the CENSUS-RULE-1a fix and the four golden cases of FCE2.5, after acceptance.

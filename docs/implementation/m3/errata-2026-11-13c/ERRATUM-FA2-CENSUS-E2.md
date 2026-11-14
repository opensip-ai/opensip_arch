# Erratum FA2-CENSUS-E2: TypeScript census rule v2: wrappers, aliases and holding positions decided by syntax (author draft r3, 2026-11-13)

Status: **PROPOSED, r3.** It implements two lead rulings in LD-DEC-11 (`LC/decisions/LD-DEC-11-census-population/DECISION.md`;
`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). The first is "Ruling after both reviews of
FA2-CENSUS-E2 r1 (2026-11-13): a new rule id". The second is "Correction, 2026-11-14 UTC: the R12 reading above is
WITHDRAWN", whose proposal r3 tests and departs from where noted (FCE2.2, statement 3; the handoff gives the reasons). It
answers both reviews of r2 (`0da99a175`): `review-opus-e2/VERDICT-r2.md` and `review-codex-e2/VERDICT-r2.md`. It also
answers the code-unit reviews of `02b97f74` on C27 (`LC/f2min/census-rule-1/review-opus/VERDICT-r5.md` R11, R12;
`LC/f2min/census-rule-1/review-codex/VERDICT-r4.md` CR1A-CX-5, CR1A-CX-6, paragraph 5). The first ruling's section is
the earlier of the two; it withdraws the same-id reading of r1.
It answers both reviews of r1 (`5681ca6e9`): `review-opus-e2/VERDICT.md` (R-E2-1, R-E2-2, two advisories) and
`review-codex-e2/VERDICT.md` (FCE2-CX-1 to -3). It is **additive**: no accepted byte is edited.

Builds on one bound text: **erratum FA2-CENSUS-E1 r5**, `docs/implementation/m3/errata-2026-11-13b/ERRATUM-FA2-CENSUS-E1.md`
at architecture main `c229e75d6`, 32,962 bytes, sha256 `1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1`,
adopted by `ADOPTION-FA2-CENSUS-E1.md` in the same directory. Line numbers `E1:N` are that file's. Every quotation below
was checked against `git show c229e75d6:<path>`.

**Form.** E1 is an erratum adopted by receipt; the FA-2 contract successor that will carry it is owed. E2 takes the same
form (the lead's adoption receipt, after two reviews). The successor carries E1 and E2, so v2 is stated in §9.8 (E1:54:
"Only a rule stated in this section can be bound").

**Code read** (read-only): product worktree `opensip-fix-f2min`, branch `f2min-fix-1-r1` at
`02b97f7425c27adca2fddf6ec9aa0989524aed0d`, the code unit CENSUS-RULE-1a's head when this was written, which is clean
(`P` = `providers/typescript/src`). No line using the alias test (`pureAlias`, `isBogusTop` or the compiler's alias flag)
changed between `8e4e0ad1`, `b1703d75` and `02b97f74`, so the reviewers' probes at `8e4e0ad1` and `b1703d75` stand for the
alias cases. Compiler: TypeScript 6.0.3, `lib/typescript.js` (`TS:N`). The author ran no probe.
- "Probed by Claude" means `review-opus-e2/VERDICT.md`, at `b1703d75`, through the compiled harness.
- "Probed by Codex" means `review-codex-e2/VERDICT.md`, at `8e4e0ad1` and `b1703d75`, through production `buildCensus`.

## FCE2.1 E1's id rule, which E2 follows

`E1:54` (the amended `9.8:3-5`) ends:

> Rule ids are immutable (erratum FA2-CENSUS-E1).

`E1:132` (FCE1.5, inserted into §9.8):

> **A wider population is a new rule.** It has a new rule id; an id is never re-used for another population.

The two reviewers of the bound text read `module.exports = class …` oppositely. The Claude reviewer reads it as included
under C5. The cross-vendor reviewer reads it as excluded by C5's guard ("a `module.exports = …` value that is not an
alias"). So E2 cannot claim to resolve an existing meaning of v1 for that form. Where E2 admits a declaration that a
careful reading of v1 excludes, the population differs, and by `E1:54` and `E1:132` that takes a new id. E2 therefore
defines a new rule. It does not reinterpret v1.

## FCE2.2 The rule `native.symbol-census-population.typescript.v2`

Inserted into §9.8 by the successor that carries E1:

> **The TypeScript population rule `native.symbol-census-population.typescript.v2` (erratum FA2-CENSUS-E2).** It is the rule `native.symbol-census-population.typescript.v1` of erratum FA2-CENSUS-E1 (sha256 `1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1`): every sentence and every row of its table C1-C28 (FCE1.3), unchanged, with its relations (FCE1.4), widening (FCE1.5) and binding (FCE1.7). It adds four statements. Each is decided from syntax and from the symbol resolution v1 already uses; none asks the checker for a type and none evaluates a value.
>
> 0. **Transparent wrappers.** These, and only these, are transparent wrappers: parentheses; `e as T`; `e satisfies T`; `<T>e`; `e!`; and a JSDoc cast, `/** @type {T} */ (e)`. Removing them means replacing each wrapper with its operand, repeatedly. A wrapper never changes a classification under statements 1-3.
> 1. **Alias.** An alias is either (a) a form C19 lists (imports, import-equals declarations, export specifiers, re-exports, and the JavaScript `const x = require(…)` and `const {a} = require(…)` forms), or (b) an export entry, made by `export default`, `export =`, `module.exports =`, `exports.K =` or `module.exports.K =`, whose value, after removing transparent wrappers, is an entity name: an identifier, or a chain of identifiers joined by `.`. Nothing else is an alias. A call such as `require('./x')`, a property of a call such as `require('./x').v`, an element access, and a class, function or arrow expression are not aliases. A symbol that is an alias merged with a namespace or other declared meaning of its own is not excluded as an alias (C18).
> 2. **Expression-valued export entries.** An export entry whose value, after removing transparent wrappers, is a class, function or arrow expression declares its meaning at that entry. It is not an alias, and it is a row under C5: `(export).K` for `exports.K =` and `module.exports.K =`, `(export=)` for `module.exports =` and TypeScript `export =`, and `default` for `export default`, in any file kind that binds that export. The expression's own name, and every member under the expression, stay excluded by C22 unless C17 or C27 carves them out.
> 3. **"Held by a variable" (C27).** A function expression is held by a variable when it stands, after removing transparent wrappers, in a holding position of that variable. The holding positions are exactly these:
>    - the initializer of the variable's declaration (`var`, `let` or `const`, with an identifier name);
>    - the right operand of `=`, `||=`, `??=` or `&&=` whose left operand is an identifier naming the variable;
>    - the default of a destructuring element, array or object, nested or not, in a declaration or an assignment, whose target is an identifier naming the variable, whatever value is destructured;
>
>    and, recursively, a position whose value can be the value of a holding position:
>    - the right operand of a comma expression;
>    - either operand of `||` or `??`;
>    - the right operand of an assignment expression standing in a holding position (so in `G = F = fn` both `F` and `G` hold `fn`; in `G = o.H = fn` only `G` does, because `o.H` is not a variable).
>
>    No other position holds. In particular, the left operand of a comma expression, either operand of `&&`, either branch of a conditional expression, the operand of `void`, `typeof` or `new`, a call or its argument, an array element, a spread element and an object property value do not hold, and neither does a property such as `o.F`. Which variable an identifier names is resolved as v1 resolves symbols. The constructor predicate is C27's own, after its colon, unchanged: "the expression's body assigns `this.x`, or the variable has a prototype assignment (either suffices)". The phrase "a variable that the checker treats as a JavaScript constructor" means exactly that predicate, never the variable's checker type. So a JSDoc cast that types the variable `any` or `Function` changes nothing.

**C3, C5, C16, C18 and C19 under the definition** (one line each; their bound text is unchanged):
- **C3** (`E1:86`, "…that is not excluded by C19 or C25…"): a top-level binding is excluded only if it is an alias under
  statement 1 or a C25 entry.
- **C5** (`E1:88`, "…a `module.exports = …` value that is not an alias; a default-exported value"): an export entry is a
  row unless it is an alias under statement 1(b). A class, function or arrow expression value is a row (statement 2), and so
  is any other value that is not an entity name after removing wrappers (a `require(…)` call, a property of a call). A
  TypeScript `export =` value is read with `module.exports =`.
- **C16** (`E1:99`, "The non-alias entries of the export table of a reached container"): "non-alias" means not an alias
  under statement 1.
- **C18** (`E1:101`, "A namespace export that is an alias merged with a namespace or other declared meaning, with its
  descendants", included): unchanged, and preserved by statement 1's last sentence.
- **C19** (`E1:102`, "Aliases with no declared meaning of their own: imports, import-equals declarations, export
  specifiers, re-exports, and the JavaScript `const x = require(…)` and `const {a} = require(…)` forms"): it excludes
  exactly the aliases of statement 1, which keeps C19's list as part (a) and adds the entity-name export entries as part (b).

**C22** (`E1:105`, unchanged): "Function, arrow and class expressions, named or not: their names, and every member under
them, whatever the file kind. The members C17 binds to the variable holding the expression, and C27's, are not under
this class".

**C27** (`E1:110`, its class cell, unchanged): "In a JavaScript file, the `this.x =` instance members in the body of a
function expression held by a variable that the checker treats as a JavaScript constructor: the expression's body
assigns `this.x`, or the variable has a prototype assignment (either suffices)…". Statement 3 defines "held by a
variable" and fixes what the predicate is.

**What differs from v1.** Under v2, each disposition marked "fix owed" in FCE2.4 and FCE2.5 differs from the code today.
Every other form keeps the disposition the code gives it now.

## FCE2.3 v1 is withdrawn before any use

`native.symbol-census-population.typescript.v1` is withdrawn. It stays in E1 as bound, it is never bound to any
enumerator closure, and any reference to it moves to v2. What is true about non-use, and how it was checked:
- **No enumerator closure carries a binding to it.** The carrier is owed (E1 FCE1.7). The closure tool
  `tools/typescript_closure.py` has no population field at `02b97f74` (`git grep population` finds nothing; also the Claude
  reviewer, at `b1703d75`). Product main `616024f7` has no `providers/typescript/src/facts/` and no occurrence of the id
  (`git grep`).
- **The id appears only in the unintegrated code unit**, at `02b97f74`: the comment at `P/test/census-corpus.test.ts:60`,
  `:786`, the skipped gate test `CR-GATE` (`:789`), and the generated copy of that test file in
  `P/embedded/source-census.ts:334`.
- **"The provider may not send `complete`" holds by law and the skipped gate test, not by code.** The branch's `run.ts`
  still sends a census whenever the token is negotiated (`P/data/run.ts:80`, `:159`; the Claude reviewer cites
  `:132-159`). E1's interim rule places any census sent without a binding under the default rule (`E1:54`; FCE1.7 at
  `E1:160`), so no census can have been sent under v1.
- **The scope of the check.** It covers only the tracked sources named here: the code unit at `02b97f74`, its closure
  tool, and product main `616024f7`. It does not prove that no untracked artifact anywhere names v1 (the cross-vendor
  reviewer's caution).

Non-use is not the ground for anything here. Within that scope, it shows that withdrawing v1 costs a renamed id and
nothing else: no binding, Plan, Run or evidence among those sources has to be re-read. If an artifact naming v1 is found
outside that scope, it keeps v1's interpretation and its binding.

## FCE2.4 The forms, and what the code does at `02b97f74`

The code keeps an export entry only if it is not a pure alias (`pureAlias` `P/facts/census.ts:243`, applied to a
module's export table at `:396` and to a container's at `:470`). The compiler flags an entry as an alias when its value
is an entity name or a class expression (`isAliasableExpression` `TS:19508-19510`; used for `exports.K =` and
`module.exports.K =` at `TS:49172`, for `module.exports =` at `TS:49190`, and for `export =` and `export default` through
`exportAssignmentIsAlias` `TS:19511-19514` and `bindExportAssignment` `TS:49086-49094`).

**Aliases (statement 1): not rows.** "Codex" in this table means `review-codex-e2/VERDICT-r2.md`, and "Claude" means
`review-opus-e2/VERDICT-r2.md` where the row says r2.

| Form | v2 | Code today | Probed by | Status |
|---|---|---|---|---|
| `module.exports = L` | no `(export=)`; `#L` is a row of its own class | `#L` only | Claude | matches |
| `class X {}; exports.K = X` / `exports.K = L` | no `(export).K` | `#L` only for `exports.K = L` | Claude (census); Codex names both as compiler aliases (point 1) | matches |
| `exports.K = a.b` | no `(export).K` | `#a` only | Claude | matches |
| TypeScript `export = L` | no `(export=)` | `#L` only | Claude | matches |
| `export default L` (TypeScript and JavaScript) | no `default` row | `#L` only | Claude | matches |
| `class L {}; exports.K = (L)` | no `(export).K` | `m.js#(export).K` beside `#L` | Codex | fix owed (CENSUS-RULE-1a) |
| `module.exports.K = (L)` | no `(export).K` | an extra `(export).K` row | Codex | fix owed |
| `module.exports = (L)` | no `(export=)` | `(export=)` beside `#L` | Claude r2, Codex | fix owed |
| TypeScript `export = (L)` | no `(export=)` | an extra `(export=)` row | Codex | fix owed |
| `export default (L)` | no `default` row | `#default` beside `#L` | Claude r2, Codex | fix owed |
| TypeScript `export default L!` and `export default L as typeof L` | no `default` row | `#default` | Codex | fix owed |
| Any other spelling of part (b) with any other wrapper or wrapper combination (`satisfies`, `<T>L`, a JSDoc cast, a dotted name `a.b` inside any wrapper) | not a row | not probed | none | the golden case decides whether a fix is owed |

**Not aliases (statement 1): rows.**

| Form | v2 | Code today | Probed by | Status |
|---|---|---|---|---|
| `module.exports = require('./x')` | `m.js#(export=)` | `m.js#(export=)` | Claude r2 | matches |
| `exports.K = require('./x')` | `m.js#(export).K` | `m.js#(export).K` | Claude r2 | matches |
| `exports.K = require('./x').v` | `m.js#(export).K` | `m.js#(export).K` | Claude r2 | matches |
| `exports.K = a['b']` (element access) | `m.js#(export).K` | not probed | none | the golden case decides |

**Expression-valued export entries (statement 2).**

| Form | v2 rows | Code today | Probed by | Status |
|---|---|---|---|---|
| `exports.K = class Named { m() {} }` (CommonJS `m.js`) | `m.js#(export).K`; no `Named`, no members | file row only; no note | Claude, Codex (also handoff A1a) | fix owed (CENSUS-RULE-1a) |
| `module.exports.K = class Named { … }` (CommonJS) | `m.js#(export).K`; no `Named`, no members | alias flag, no row | Claude (advisory) | fix owed (CENSUS-RULE-1a) |
| `exports.K = function g() { this.p = 1; }` (CommonJS) | `m.js#(export).K`; no `g`, no `~p` | `m.js#(export).K`; no `g`, no `~p`, no note | Claude, Codex | matches |
| `module.exports = class Named { m() {} static s = 1; }` (CommonJS) | `m.js#(export=)`; no `Named`, no members | file row only; no note | Claude, Codex (also handoff A1b) | fix owed (CENSUS-RULE-1a) |
| `module.exports = function g() { this.p = 1; }` (CommonJS) | `m.js#(export=)`; no `g`, no `~p` | `m.js#(export=)`; no `g`, no `~p`, no note | Claude, Codex | matches |
| TypeScript `export = class Named { m() {} static s = 1 }` (`m.ts`, module `commonjs`) | `m.ts#(export=)`; no `Named`, no members | file row only (alias flag) | Claude (R-E2-2), Codex (point 4) | fix owed (CENSUS-RULE-1a) |
| TypeScript `export = class { m() {} }` (anonymous) | `m.ts#(export=)`; no members | file row only (alias flag) | Claude r2, Codex r2 | fix owed (CENSUS-RULE-1a) |
| `exports.K = (class Named { m() {} })` (parenthesized) | `m.js#(export).K`; no members | `m.js#(export).K` | Claude r2 (A1) | matches |
| `export = (class Named {…})` (TypeScript) | `m.ts#(export=)`; no members | `(export=)` row | Claude r2 | matches |

C27 names variables only ("held by a variable", `E1:110`), so `module.exports = function () { this.p = 1; }` and
`exports.K = function () { this.p = 1; }` get no `~p` member under v2.

**Where these forms occur.** r1's claim that they exist only in CommonJS JavaScript files was false, and is withdrawn.
The `exports.K =`, `module.exports.K =` and `module.exports =` forms bind an export only in a JavaScript file with no ES
`import` or `export`, and binding one makes the file a CommonJS module (`TS:49124-49134`; a TypeScript file binds none,
`TS:18768-18771`, which Codex confirms by probe). The TypeScript `export =` form arises in TypeScript module files. No
script form exists for any of them.

**Neighbouring forms that do not move** (probed by both reviewers):
- `export default class {}` is a class declaration and is already a row (`#default`, C5);
- `export default (class Named {})`, a parenthesized default class expression, is already a non-alias value row
  (`#default`);
- `exports.f = () => 1` is already a row (`(export).f`; Claude, `LC/f2min/census-rule-1/review-opus/VERDICT-r2.md:77`);
- `export { C as D }` and a namespace `export import` are aliases (C19), and are not rows.

**The fix owed for statements 1-2** (CENSUS-RULE-1a, after E2 is accepted). The census's alias test follows statement 1,
not the compiler's alias flag. An entry whose value is a class expression keeps its row, and its walk does not reach the
expression's own symbol or members (C22). An entry whose value is an entity name inside transparent wrappers loses its
row. C18's merged entries stay included.

**C27 forms whose disposition statement 3 changes or decides.** The code today, from the code unit's golden at
`02b97f74` (`P/test/census-corpus.test.ts:681-737`, its wrapper table) and the reviewers' probes
(`LC/f2min/census-rule-1/review-opus/VERDICT-r5.md`, `LC/f2min/census-rule-1/review-codex/VERDICT-r4.md`). `fn` is
`function () { this.p = 1; }` in a `.js` file.

| Form | v2 | Code today | Status |
|---|---|---|---|
| `var F = fn \|\| 0`, `var F = fn ?? 0` | `#F~p` (either operand of `\|\|`/`??`) | no `#F~p` (both reviews: R11, CR1A-CX-5) | fix owed |
| `var [F = fn] = []` | `#F~p` (destructuring default) | no `#F~p` (both reviews) | fix owed |
| `var F; [F = fn] = []`, and `[F = fn] = [1]` | `#F~p` | `#F~p` (both reviews) | matches |
| `var { F = fn } = {}`, `var F; ({ F = fn } = {})` | `#F~p` | no `#F~p` (golden rows "no member") | fix owed; the two golden rows flip |
| `var F = /** @type {any} */ (fn)`, `/** @type {Function} */ (fn)` | `#F~p` (wrapper; predicate is the body) | `#F~p` (both reviews) | matches |
| `var F = (fn)!`, `as`, `satisfies` in a `.ts` file | no member (C27 is JavaScript-only) | no member (golden) | matches |
| `var F = 1; F \|\|= fn` | `#F~p` (right operand of `\|\|=`) | `#F~p` (Claude r5 advisory) | matches |

Every other row of that wrapper table keeps its disposition under statement 3. The members are parentheses, comma right
operand, `=`, the `||`/`??` right operands, `||=`/`??=`/`&&=`, an assignment inside a comma's left operand, and
`async function`. The rows with no member are comma left operand, both `&&` operands, both conditional forms, `void`,
`typeof`, call, `new`, array element, object property value, spread element and call argument. These rows need no fix.

## FCE2.5 Golden cases owed in CENSUS-RULE-1a

The code unit's references to the rule id move to v2: the comments, the `CR-GATE` test, the owed carrier and binding,
and the generated source census. Cases, each with exact rows and "no A7 note":
1. Aliases (statement 1), bare:
   - `module.exports = L` gives `#L` and no `(export=)`;
   - `class X {}; exports.K = X` and `exports.K = a.b` give no `(export).K`;
   - TypeScript `export = L` gives no `(export=)`;
   - `export default L`, in TypeScript and JavaScript, gives no `default` row.
2. `exports.K = class Named { m() {} static s = 1; }` gives `m.js#(export).K`, with no `Named`, `~m` or `.s`.
3. `module.exports.K = class Named { m() {} }` gives `m.js#(export).K`, with no `Named` and no `~m`.
4. `exports.K = function g() { this.p = 1; }` gives `m.js#(export).K`, with no `g` and no `~p`.
5. `module.exports = class Named { m() {} static s = 1; }` gives `m.js#(export=)`, with no members.
6. `module.exports = function g() { this.p = 1; }` gives `m.js#(export=)`, with no `g` and no `~p`.
7. TypeScript `export = class Named { m() {} static s = 1 }` gives `m.ts#(export=)`, with no members.
8. TypeScript `export = class { m() {} }` gives `m.ts#(export=)`, with no members.
9. A C18 control: a namespace export alias merged with a namespace meaning stays a row.
10. Bare versus wrapped pairs, one pair per alias spelling: `exports.K =`, `module.exports.K =`, `module.exports =`,
    TypeScript `export =`, and `export default` in TypeScript and JavaScript. Each takes `L` and `(L)`; the TypeScript
    spellings also take `L!`, `L as typeof L`, `L satisfies T` and `<T>L`, and the JavaScript ones a JSDoc cast. A dotted
    `a.b` takes parentheses. Every case: no export row.
11. Non-aliases: `module.exports = require('./x')`, `exports.K = require('./x')`, `exports.K = require('./x').v` and
    `exports.K = a['b']` each give the export row.
12. `exports.K = (class Named { m() {} })` gives `m.js#(export).K`, with no members.
13. C27 under statement 3, in `.js` script files: `var F = fn || 0` and `var F = fn ?? 0` give `#F~p`; the four
    destructuring spellings give `#F~p` (array and object, each as a declaration and as an assignment, with `[]`/`{}` and
    with a non-empty source such as `[1]`); one nested pattern, `var { a: [F = fn] } = { a: [] }`, gives `#F~p`; the two
    JSDoc casts give `#F~p`; and `var F = 1; F ||= fn` gives `#F~p`. Controls: `var F = F && fn` and
    `var F = c ? fn : 0` give no member, and `var G; ({ K: o.G = fn } = {})` gives no member.

No script case is owed: no script form exists (FCE2.4). The `exported` value of each row is the one E1 gives an export
entry.

## FCE2.6 What this does not change

- Every row and sentence of E1 (C1-C28, FCE1.3-FCE1.7). v2 incorporates them unchanged. FCE2.4 lists every disposition
  that v2 changes.
- **The form the reviewers call "A2"** (`var o = {}; o.F = function () { this.p = 1; }; o.F.prototype.m = function () {};`)
  needs no new text. Both reviewers find that E1 decides it, and v2 keeps it: `#o.F~p` is excluded (C22; C27 names
  variables only), and `#o.F~m` is a row (C13).
- The default rule `native.symbol-census-population.default.v1`; no schema, wire member, deficiency, carrier or binding.

## FCE2.7 Review and binding owed

- **Review:** both reviewers of E1, before any rule is first bound to a closure.
- **Binding owed:** the lead's adoption receipt pinning this file's sha256. The owed FA-2 contract successor states v2 in
  §9.8, with E1 and this erratum.
- **Code owed:** CENSUS-RULE-1a's fix (FCE2.4), the golden cases (FCE2.5), and the move of its id references to v2.

## FCE2.8 Changes by round (r1 `5681ca6e9`; r2 `0da99a175`)

| Finding | Change |
|---|---|
| Lead ruling; FCE2-CX-2 | a new id, v2, is defined as E1's v1 unchanged plus two statements. v1 is withdrawn before use. Every r1 sentence that let non-use permit reusing v1's id is removed, and E1:54 and E1:132 are quoted and followed |
| R-E2-1; FCE2-CX-1 | "alias" is defined by meaning, and C19's list is illustrative. Entity-name exports are aliases, and the code matches. C18's exception is quoted and kept. C3, C5, C16, C18 and C19 each get one line |
| R-E2-2; FCE2-CX-3 | TypeScript `export = class Named {…}` and `export = class {…}` are decided (`(export=)`, fix owed). r1's "only CommonJS JavaScript" is withdrawn. The forms that do not move are listed |
| Claude advisory 1 | `module.exports.K = class …` is named (fix owed, golden case 3) |
| Claude advisory 2 | FCE2.3 says that `run.ts` still sends a census when the token is negotiated, and that non-sending holds by law and the skipped test |
| r3: Claude R2-1; Codex FCE2-R2-CX-1 | statement 0 adds a closed list of transparent wrappers. Statement 1 is restated as a closed definition: C19's forms, plus export entries whose unwrapped value is an entity name. `require` forms and properties of calls are not aliases (rows, matching the code). Wrapped entity names are aliases (fix owed) |
| r3: Claude r2 advisory A1 | `exports.K = (class …)` is decided as a row (matches), with a golden case |
| r3: lead correction (R12 withdrawn); code-unit reviews R11, R12, CR1A-CX-5, CR1A-CX-6, Codex paragraph 5 | statement 3 defines "held by a variable" by a closed list of syntactic holding positions, and fixes C27's predicate as the colon clause, never the holder's type. Destructuring defaults hold in every spelling (the object rows flip; fix owed). JSDoc casts are wrappers (member; matches). `fn \|\| 0` and `fn ?? 0` hold (fix owed) |
| r3: Codex scope note | FCE2.3 names the scope of the non-use check, and says that an artifact found outside it keeps v1 |

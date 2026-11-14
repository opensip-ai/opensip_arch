# Erratum FA2-CENSUS-E2: TypeScript census rule v2: wrappers, aliases and holding positions decided by syntax (author draft r5, 2026-11-13)

Status: **PROPOSED, r5** (r4 plus `review-opus-e2/VERDICT-r4.md` R4-1, R4-2 and `review-codex-e2/VERDICT-r4.md`
FCE2-R4-CX-1). r4 answered both reviews of r3: `review-opus-e2/VERDICT-r3.md` R3-1, R3-2;
`review-codex-e2/VERDICT-r3.md` FCE2-R3-CX-1, -2; the lead accepted r3's narrowing). r3: It implements two lead rulings in LD-DEC-11 (`LC/decisions/LD-DEC-11-census-population/DECISION.md`;
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
> 1. **Alias.** An alias is one of: (a) a form C19 lists other than its `require` forms (imports, import-equals declarations, export specifiers, re-exports); (a′) a require declaration: in a JavaScript file, a variable declarator of any kind (`const`, `let` or `var`) whose declaration has no `export` modifier and carries no JSDoc `@type` tag, whose name is an identifier or a destructuring pattern, and whose initializer, after removing transparent wrappers, is a call `require(s)`, where `s` is a string literal or a template literal without substitutions, or a chain of property accesses (`.name`) on such a call (this class contains C19's two `require` forms). A variable is an alias under (a′) only when every declaration of it is such a declarator; one with any other declaration has a declared meaning of its own and is not an alias. An exported declaration has its own export meaning: v1's C18 rule cell reads "as at module top level, where only a pure alias is excluded". A declaration with a JSDoc `@type` tag declares its own type, and so it is not an alias "with no declared meaning of [its] own" (C19). In a TypeScript file no declaration is in (a′); or (b) an export entry, made by `export default`, `export =`, `module.exports =`, `exports.K =` or `module.exports.K =`, whose value, after removing transparent wrappers, is an entity name: an identifier, or a chain of identifiers joined by `.`. Nothing else is an alias. In (b), a call such as `require('./x')`, a property of a call such as `require('./x').v`, an element access, and a class, function or arrow expression are not aliases. In (a′), an element access on the call (`require('./x')['v']`), a call on it (`require('./x').v()`) and a `require` whose argument is not such a literal are not aliases. A symbol that is an alias merged with a namespace or other declared meaning of its own is not excluded as an alias (C18).
> 2. **Expression-valued export entries.** An export entry whose value, after removing transparent wrappers, is a class, function or arrow expression declares its meaning at that entry. It is not an alias, and it is a row under C5: `(export).K` for `exports.K =` and `module.exports.K =`, `(export=)` for `module.exports =` and TypeScript `export =`, and `default` for `export default`, in any file kind that binds that export. The expression's own name, and every member under the expression, stay excluded by C22 unless C17 or C27 carves them out.
> 3. **"Held by a variable" (C27).** A function expression is held by a variable when it stands, after removing transparent wrappers, in a holding position of that variable. The holding positions are exactly these:
>    - the initializer of the variable's declaration (`var`, `let` or `const`, with an identifier name);
>    - the right operand of `=`, `||=`, `??=` or `&&=` whose left operand is an identifier naming the variable;
>    - the default of a destructuring element, array or object, nested or not, in a declaration or an assignment, whose target is an identifier naming the variable, whatever value is destructured;
>
>    and, recursively, a position whose value can be the value of a holding position:
>    - the right operand of a comma expression;
>    - either operand of `||` or `??`;
>    - the right operand of an assignment expression whose operator is `=`, `||=`, `??=` or `&&=` (the value of such an expression can be its right operand). Such an assignment composes with the direct holds: if its left operand is an identifier naming a variable, that variable holds the expression by the second direct hold, and the variable of the outer holding position holds it too. So in `G = F = fn` and in `var G = (F = fn)` both `F` and `G` hold `fn`; in `var G = (F ||= fn)` both hold it; in `G = o.H = fn` only `G` does, because `o.H` is not a variable.
>    - Every other compound assignment (`+=`, `-=`, `*=`, `/=`, `%=`, `**=`, `<<=`, `>>=`, `>>>=`, `&=`, `|=`, `^=`) neither holds nor passes through: in `F += fn` the variable `F` does not hold `fn`, and in `G = (F += fn)` neither `F` nor `G` does.
>
>    One function expression can be held by several variables, and each of them gets its members. One holding position can hold several function expressions (`fn1 || fn2`), and the variable gets each one's members. The id and collision checks of v1 apply to every such member unchanged. A variable that is an alias under statement 1 holds nothing, and C27 gives it no members (so `const { v = fn } = require('./x')` gives neither `v` nor a member). A variable that is not an alias holds by every holding position that names it, including an assignment whose source is a `require` call (`var F; ({ F = fn } = require('./x'))` gives `F~p`).
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
  exactly the aliases of statement 1. Part (a) keeps C19's list; part (a′) states its `require` forms as a class (read with
  statement 0, `const x = (require('./x'))` is C19's own form); part (b) adds the entity-name export entries.

**C22** (`E1:105`, unchanged): "Function, arrow and class expressions, named or not: their names, and every member under
them, whatever the file kind. The members C17 binds to the variable holding the expression, and C27's, are not under
this class".

**C27** (`E1:110`, its class cell, unchanged): "In a JavaScript file, the `this.x =` instance members in the body of a
function expression held by a variable that the checker treats as a JavaScript constructor: the expression's body
assigns `this.x`, or the variable has a prototype assignment (either suffices)…". Statement 3 defines "held by a
variable" and fixes what the predicate is.

**What differs from v1.** The dispositions v2 changes are those of statements 0-3. FCE2.4 gives probed evidence of where
the code differs from them. It is not a complete list, and conformance is to the statements.

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
| Any other spelling of part (b) with any other wrapper (`satisfies`, `<T>L`, a JSDoc cast, a dotted name `a.b` inside parentheses) | not a row | an export row (Claude r3 probes; `probe-r5.mjs` B07g-h, B08c-d, B08g-h, B09a-c) | Claude r3, this author | fix owed (CENSUS-RULE-1a) |

**Not aliases (statement 1): rows.**

| Form | v2 | Code today | Probed by | Status |
|---|---|---|---|---|
| `module.exports = require('./x')` | `m.js#(export=)` | `m.js#(export=)` | Claude r2 | matches |
| `exports.K = require('./x')` | `m.js#(export).K` | `m.js#(export).K` | Claude r2 | matches |
| `exports.K = require('./x').v` | `m.js#(export).K` | `m.js#(export).K` | Claude r2 | matches |
| `exports.K = a['b']` (element access) | `m.js#(export).K` | `m.js#(export).K` | Claude r3, this author (`probe-r5.mjs` B11) | matches |

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

**The fix owed, stated generally** (CENSUS-RULE-1a, after E2 is accepted):
- **Aliases.** The census's alias test follows statement 1, not the compiler's alias flag.
  - An export entry whose value is a class expression keeps its row; its walk reaches neither the expression's own
    symbol nor its members (C22).
  - An entry whose value is an entity name inside transparent wrappers loses its row.
  - A require declaration is excluded exactly as (a′) says, wrapped or not. A JavaScript declarator with an `export`
    modifier or a JSDoc `@type` tag, and every TypeScript declaration, is not in (a′).
  - C18's merged entries stay included.
- **Holding (C27).** The code decides "held" by whether the checker names the expression's type after the variable
  (commit `7189c915`), not by statement 3. That test is replaced by statement 3's syntactic test:
  - transparent wrappers are removed at every level;
  - the direct holds, and the pass-through positions with their exact operator sets, are followed recursively;
  - every variable that holds an expression gets its members, under the existing id and collision checks;
  - every function expression a position holds gives its members;
  - a variable that is an alias under statement 1 holds nothing.

  Because the code's test differs from the rule's in kind, the forms listed below are evidence, not a complete list.
  Conformance is to statement 3 itself.

**What the code does today: probed, not inferred.** Each form was run through the code unit's compiled harness at
`02b97f74` (`dist/test/fixtures/census-harness.js` `runCensus`, its `dist` built at the head commit's time). I used Node
24.16.0 and TypeScript 6.0.3, read-only, the same method the reviewers used. Script and output:
`LC/decisions/LD-DEC-11-census-population/e2-probes/probe-r5.mjs` and `probe-r5.out.txt` (r4's 125 cases plus D01-D10).
The script holds 135 cases.
Each case states the rows rule v2 requires (`want`) and forbids (`not`). Its output is complete with no failure in every
case. 82 cases match the rule; 53 differ.

**Fix owed: the 53 cases where the code differs from v2**, generated from that output (`e2-probes/fix-owed-r5.md`). Ids
are without the `ts-symbol:` prefix. "Rows required" lists the rows the case checks, plus the rows the code gives that the
rule does not touch.

| Probe case | Rows required by v2 | Rows at `02b97f74` |
|---|---|---|
| A16 object default decl | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A17 object default assign | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A20a fn \|\| 0 | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A20b fn ?? 0 | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A21 array default decl | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A28 fn1 \|\| fn2 | `#F`, `#F~p`, `#F~q`, `s.js` | `#F`, `s.js` |
| A29 var F = G = fn | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#G`, `#G~p`, `s.js` |
| A30 F = G = fn | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#G`, `#G~p`, `s.js` |
| A31 var G = (F = fn) | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#F~p`, `#G`, `s.js` |
| A32 var G = 0 \|\| (F = fn) | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#F~p`, `#G`, `s.js` |
| A33 cast inside \|\| operand | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A34 comma inside \|\| operand | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A35 \|\| inside a cast | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A37 for-of destructuring head | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A38 nested pattern | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A39 renamed target | `#F`, `#F~p`, `s.js` | `#F`, `s.js` |
| A42 G \|\| fn | `#F`, `#F~p`, `#G`, `s.js` | `#F`, `#G`, `s.js` |
| A43 var G = (F \|\|= fn) | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#F~p`, `#G`, `s.js` |
| A44 var G = (F ??= fn) | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#F~p`, `#G`, `s.js` |
| A45 var G = (F &&= fn) | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#F~p`, `#G`, `s.js` |
| A52 var F = (G = fn) \|\| 0 | `#F`, `#F~p`, `#G`, `#G~p`, `s.js` | `#F`, `#G`, `#G~p`, `s.js` |
| B07a exports.K = (L) | `m.js`, `m.js#L` | `m.js`, `m.js#(export).K`, `m.js#L` |
| B07b module.exports = (L) | `m.js`, `m.js#L` | `m.js`, `m.js#(export=)`, `m.js#L` |
| B07c module.exports.K = (L) | `m.js`, `m.js#L` | `m.js`, `m.js#(export).K`, `m.js#L` |
| B07d TS export = (L) | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#(export=)`, `m.ts#L` |
| B07e TS export default (L) | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#L`, `m.ts#default` |
| B07f JS export default (L) | `m.js`, `m.js#L` | `m.js`, `m.js#L`, `m.js#default` |
| B07g exports.K = (a.b) | `m.js`, `m.js#a` | `m.js`, `m.js#(export).K`, `m.js#a` |
| B07h module.exports = (a.b) | `m.js`, `m.js#a` | `m.js`, `m.js#(export=)`, `m.js#a` |
| B08a TS export default L! | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#L`, `m.ts#default` |
| B08b TS export default L as typeof L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#L`, `m.ts#default` |
| B08c TS export default L satisfies typeof L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#L`, `m.ts#default` |
| B08d TS export default <typeof L>L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#L`, `m.ts#default` |
| B08e TS export = L! | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#(export=)`, `m.ts#L` |
| B08f TS export = L as typeof L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#(export=)`, `m.ts#L` |
| B08g TS export = L satisfies typeof L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#(export=)`, `m.ts#L` |
| B08h TS export = <typeof L>L | `m.ts`, `m.ts#L` | `m.ts`, `m.ts#(export=)`, `m.ts#L` |
| B09a exports.K = JSDoc cast L | `m.js`, `m.js#L` | `m.js`, `m.js#(export).K`, `m.js#L` |
| B09b module.exports = JSDoc cast L | `m.js`, `m.js#L` | `m.js`, `m.js#(export=)`, `m.js#L` |
| B09c JS export default JSDoc cast L | `m.js`, `m.js#L` | `m.js`, `m.js#L`, `m.js#default` |
| B12a exports.K = class | `m.js`, `m.js#(export).K` | `m.js` |
| B12b module.exports.K = class | `m.js`, `m.js#(export).K` | `m.js` |
| B12c module.exports = class | `m.js`, `m.js#(export=)` | `m.js` |
| B12d TS export = class Named | `m.ts`, `m.ts#(export=)` | `m.ts` |
| B12e TS export = class {} | `m.ts`, `m.ts#(export=)` | `m.ts` |
| C08 const x = (require()) | `m.js`, `m.js#(export).q` | `m.js`, `m.js#(export).q`, `m.js#x` |
| C09 const x = JSDoc cast require | `m.js`, `m.js#(export).q` | `m.js`, `m.js#(export).q`, `m.js#x` |
| C11 const x = require()['v'] (element access) | `m.js`, `m.js#(export).q`, `m.js#x` | `m.js`, `m.js#(export).q` |
| C13 const x = require()[k] (non-literal element access) | `m.js`, `m.js#(export).q`, `m.js#k`, `m.js#x` | `m.js`, `m.js#(export).q`, `m.js#k` |
| C14 const x = require()['v'].w | `m.js`, `m.js#(export).q`, `m.js#x` | `m.js`, `m.js#(export).q` |
| D01 var F = require() \|\| fn | `m.js`, `m.js#(export).q`, `m.js#F`, `m.js#F~p` | `m.js`, `m.js#(export).q`, `m.js#F` |
| D05 var F; ({ F = fn } = require()) (assignment, not a declaration) | `m.js`, `m.js#(export).q`, `m.js#F`, `m.js#F~p` | `m.js`, `m.js#(export).q`, `m.js#F` |
| D10 JSDoc @type on a destructuring declaration | `m.js`, `m.js#(export).q`, `m.js#v` | `m.js`, `m.js#(export).q` |

**Matches: the other 82 cases.** The code already gives the rows v2 requires; the script lists each one:
- **C27** (45 cases):
  - every member and no-member row of the golden's wrapper table, except the two object-destructuring rows;
  - the array assignment defaults (`[F = fn] = []` and `= [1]`) and both JSDoc casts;
  - `(fn)!`, `as` and `satisfies` in `.ts`;
  - `F = 1; F ||= fn`, `G = o.H = fn` (both spellings), and the comma of two expressions;
  - a cast inside a comma and a comma inside a cast;
  - a property target, a generator, and `x && fn`;
  - the class-field and parameter-default controls;
  - the four compound-assignment negatives (`F += fn`, `G = (F += fn)`, `G = (F *= fn)`, `F <<= fn`).
- **Exports** (18 cases): every bare alias spelling; the `require` export values; `a['b']`; the parenthesized class
  expressions; both function-expression exports; and the controls `export default class {}`, `export default (class …)`
  and `export { C as D }`.
- **Require and holding interactions** (r5, 7 cases):
  - `const { v = fn } = require('./x')` and `var { a: F = fn, b } = require('./x')`: aliases hold nothing;
  - `var F = fn, x = require('./x')`: separate declarators;
  - `var F = require('./x'); var F = fn`: a redeclared variable is not an alias;
  - the TypeScript `const x = require('./x')`, which is not in (a′);
  - JavaScript `export const x = require('./x')`;
  - the JSDoc `@type` on an identifier declaration.
- **Require declarations** (12 cases): `const`, `let` and `var` with an identifier; object and array destructuring
  (`const`, `let`, `var`); property chains; the template-literal argument; and the non-literal argument and the call on a
  `require`, which stay rows.

## FCE2.5 Golden cases owed in CENSUS-RULE-1a

- **The id moves.** The code unit's references to the rule id move to v2: the comments, the `CR-GATE` test, the owed
  carrier and binding, and the generated source census.
- **The cases.** The golden is the 135 probe cases of `probe-r5.mjs`.
  - For the 53 that differ, the exact rows are the table above.
  - For the 82 that match, the exact rows are the outputs recorded in `probe-r5.out.txt`, checked against the rule. The
    script asserts only the listed ids.
  - Every case has the census complete and no A7 note. Each case is written first, and fails at `02b97f74` wherever
    the table above says "fix owed".
- **Controls the golden must carry by name:**
  - the compound-assignment negatives (`F += fn`; `G = (F += fn)`; `G = (F *= fn)`; `F <<= fn`) and the positive
    pass-through controls (`var G = (F = fn)`, `var G = (F ||= fn)`, `??=`, `&&=`);
  - the class-field and parameter-default controls;
  - the r5 controls: an alias holds nothing (D02, D03); a TypeScript require declaration is a row (D07); an exported
    declaration (D08) and an annotated one (D09, D10) are rows;
  - the C18 control already in the golden (a namespace export alias merged with a namespace meaning stays a row).
- **The two golden rows that flip:** the object-destructuring rows (declaration and assignment) change from "no member"
  to `#F~p`.

**Script cases:** none is owed for the export forms, because no script form exists for them (FCE2.4). The C27 and require
cases are owed in the file kinds the probe script uses: `.js` scripts for C27, and a `.ts` script for the JavaScript-only
negatives. The `exported` value of each row is the one E1 gives.

## FCE2.6 What this does not change

- Every row and sentence of E1 (C1-C28, FCE1.3-FCE1.7). v2 incorporates them unchanged. The dispositions v2 changes are
  those of statements 0-3. FCE2.4 gives the probed evidence (135 cases), and conformance is to the statements.
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
| r4: Claude R3-2; Codex FCE2-R3-CX-1 | the pass-through assignment has an exact operator set (`=`, `\|\|=`, `??=`, `&&=`). Its composition with the direct holds is defined, with `var G = (F \|\|= fn)` (both hold) and `G = (F += fn)` (neither). Other compound assignments neither hold nor pass through, and golden controls are named for both |
| r4: Claude R3-1; Codex FCE2-R3-CX-2 | the fix is stated generally (statement 3's test replaces the checker-name test; several holders and several held expressions). The "every other form keeps its disposition" claims are withdrawn. 125 cases are probed, giving 50 fix owed and 75 matches, and the fix and golden lists are generated from the probe |
| r4: Codex FCE2-R3-CX-2 (require) | statement 1(a′) defines require declarations as a class. It matches the code, except: wrapped (`(require(…))`, cast), an element access on the call (`['v']`, `[k]`, `['v'].w`). These are fix owed |
| r4: advisories | the wrapped-alias row is "fix owed" (probed); "no script case" is limited to export forms; the class-field and parameter-default controls are added |
| r5: Claude R4-1; Codex FCE2-R4-CX-1 (second half) | the surviving "every other form keeps the disposition" sentence is replaced: FCE2.4 is evidence, not a complete list. The witness `var F = require('./x') \|\| fn` is probed (D01, fix owed). No other sentence of that kind remains |
| r5: Claude R4-2 | an alias holds nothing (D02, D03 match). The reverse: a non-alias holds by every holding position, including an assignment from a `require` (D05, fix owed). A redeclared variable is not an alias (D06, matches) |
| r5: Codex FCE2-R4-CX-1 (first half) | (a′) is JavaScript-only (TypeScript control D07, matches). An `export` modifier (D08, matches; v1's C18 rule cell) or a JSDoc `@type` tag (D09 matches; D10, a destructuring declaration, fix owed) takes a declarator out of the class |
| r5: advisories | the duplicated fix statements are merged. FCE2.5 says the matching cases' exact rows are the recorded outputs, checked against the rule |

# Erratum FA2-CENSUS-E2: TypeScript census rule v2, with "alias" defined by meaning (author draft r2, 2026-11-13)

Status: **PROPOSED, r2.** It implements the lead's ruling "Ruling after both reviews of FA2-CENSUS-E2 r1 (2026-11-13): a
new rule id" in LD-DEC-11 (`LC/decisions/LD-DEC-11-census-population/DECISION.md`, its last section;
`LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`). That ruling withdraws the same-id reading of r1.
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

> **The TypeScript population rule `native.symbol-census-population.typescript.v2` (erratum FA2-CENSUS-E2).** It is the rule `native.symbol-census-population.typescript.v1` of erratum FA2-CENSUS-E1 (sha256 `1dd70aa997e6250f0256557ff4eceb24217ffdcde16d4ae9d4649a8d7e3232c1`): every sentence and every row of its table C1-C28 (FCE1.3), unchanged, with its relations (FCE1.4), widening (FCE1.5) and binding (FCE1.7). It adds two statements:
>
> 1. **Alias, by meaning.** Throughout the rule, an alias is a name that only refers to a declaration made elsewhere and has no declared meaning of its own. C19's list is illustrative, not closed. An export entry whose value is an entity name (`x`, `a.b`) is an alias, whether it is made by `export default`, `export =`, `module.exports =`, `exports.K =` or `module.exports.K =`. A symbol that is an alias merged with a namespace or other declared meaning of its own is not excluded as an alias (C18).
> 2. **Expression-valued export entries.** An export entry whose value is a class, function or arrow expression declares its meaning at that entry. It is not an alias, and it is a row under C5: `(export).K` for `exports.K =` and `module.exports.K =`, and `(export=)` for `module.exports =` and TypeScript `export =`, in any file kind that binds that export. The expression's own name, and every member under the expression, stay excluded by C22 unless C17 or C27 carves them out.

**C3, C5, C16, C18 and C19 under the definition** (one line each; their bound text is unchanged):
- **C3** (`E1:86`, "…that is not excluded by C19 or C25…"): a top-level binding is excluded only if it is an alias by
  meaning (C19) or a C25 entry.
- **C5** (`E1:88`, "…a `module.exports = …` value that is not an alias; a default-exported value"): an export entry is a
  row unless its value is an alias by meaning. A class, function or arrow expression value is a row, and an entity-name
  value is not. A TypeScript `export =` value is read with `module.exports =`.
- **C16** (`E1:99`, "The non-alias entries of the export table of a reached container"): "non-alias" means not an alias by
  meaning.
- **C18** (`E1:101`, "A namespace export that is an alias merged with a namespace or other declared meaning, with its
  descendants", included): unchanged, and preserved by statement 1's last sentence.
- **C19** (`E1:102`, "Aliases with no declared meaning of their own: imports, import-equals declarations, export
  specifiers, re-exports, and the JavaScript `const x = require(…)` and `const {a} = require(…)` forms"): it excludes
  every alias by meaning. Its list gives examples.

**C22** (`E1:105`, unchanged): "Function, arrow and class expressions, named or not: their names, and every member under
them, whatever the file kind. The members C17 binds to the variable holding the expression, and C27's, are not under
this class".

**What differs from v1.** Under v2, the class-expression export entries of FCE2.4 are rows. The function-expression
entries and every alias case are rows, or not rows, exactly as the code already gives them.

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
- **The scope of the check.** It covers the tracked sources named here. It does not prove that no untracked artifact
  anywhere names v1 (the cross-vendor reviewer's caution).

Non-use is not the ground for anything here. It shows only that withdrawing v1 costs a renamed id and nothing else: no
binding, Plan, Run or evidence has to be re-read.

## FCE2.4 The forms, and what the code does at `02b97f74`

The code keeps an export entry only if it is not a pure alias (`pureAlias` `P/facts/census.ts:243`, applied to a
module's export table at `:396` and to a container's at `:470`). The compiler flags an entry as an alias when its value
is an entity name or a class expression (`isAliasableExpression` `TS:19508-19510`; used for `exports.K =` and
`module.exports.K =` at `TS:49172`, for `module.exports =` at `TS:49190`, and for `export =` and `export default` through
`exportAssignmentIsAlias` `TS:19511-19514` and `bindExportAssignment` `TS:49086-49094`).

**Aliases by meaning (statement 1): not rows, as today.**

| Form | v2 | Code today | Probed by | Status |
|---|---|---|---|---|
| `module.exports = L` | no `(export=)`; `#L` is a row of its own class | `#L` only | Claude | matches |
| `class X {}; exports.K = X` / `exports.K = L` | no `(export).K` | `#L` only for `exports.K = L` | Claude (census); Codex names both as compiler aliases (point 1) | matches |
| `exports.K = a.b` | no `(export).K` | `#a` only | Claude | matches |
| TypeScript `export = L` | no `(export=)` | `#L` only | Claude | matches |
| `export default L` (TypeScript and JavaScript) | no `default` row | `#L` only | Claude | matches |

**Expression-valued export entries (statement 2).**

| Form | v2 rows | Code today | Probed by | Status |
|---|---|---|---|---|
| `exports.K = class Named { m() {} }` (CommonJS `m.js`) | `m.js#(export).K`; no `Named`, no members | file row only; no note | Claude, Codex (also handoff A1a) | fix owed (CENSUS-RULE-1a) |
| `module.exports.K = class Named { … }` (CommonJS) | `m.js#(export).K`; no `Named`, no members | alias flag, no row | Claude (advisory) | fix owed (CENSUS-RULE-1a) |
| `exports.K = function g() { this.p = 1; }` (CommonJS) | `m.js#(export).K`; no `g`, no `~p` | `m.js#(export).K`; no `g`, no `~p`, no note | Claude, Codex | matches |
| `module.exports = class Named { m() {} static s = 1; }` (CommonJS) | `m.js#(export=)`; no `Named`, no members | file row only; no note | Claude, Codex (also handoff A1b) | fix owed (CENSUS-RULE-1a) |
| `module.exports = function g() { this.p = 1; }` (CommonJS) | `m.js#(export=)`; no `g`, no `~p` | `m.js#(export=)`; no `g`, no `~p`, no note | Claude, Codex | matches |
| TypeScript `export = class Named { m() {} static s = 1 }` (`m.ts`, module `commonjs`) | `m.ts#(export=)`; no `Named`, no members | file row only (alias flag) | Claude (R-E2-2), Codex (point 4) | fix owed (CENSUS-RULE-1a) |
| TypeScript `export = class { m() {} }` (anonymous) | `m.ts#(export=)`; no members | not probed. By the code: the binder flags a class-expression `export =` as an alias whether or not the class is named (`TS:19508-19514`, `TS:49090`), and `:396` drops it | none | fix owed (CENSUS-RULE-1a; the golden case establishes today's behaviour) |

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

**The fix owed** (CENSUS-RULE-1a, after E2 is accepted). The census's alias test excludes an entry only when it is an
alias by meaning. An entry whose value is a class expression keeps its row, and its walk does not reach the expression's
own symbol or members (C22). Entity-name entries stay excluded. C18's merged entries stay included.

## FCE2.5 Golden cases owed in CENSUS-RULE-1a

The code unit's references to the rule id move to v2: the comments, the `CR-GATE` test, the owed carrier and binding,
and the generated source census. Cases, each with exact rows and "no A7 note":
1. Aliases by meaning, in one CommonJS case and two TypeScript/ES cases:
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

No script case is owed: no script form exists (FCE2.4). The `exported` value of each row is the one E1 gives an export
entry.

## FCE2.6 What this does not change

- Every row and sentence of E1 (C1-C28, FCE1.3-FCE1.7). v2 incorporates them unchanged. Under the definition by meaning
  the alias cases keep their present rows (FCE2.4).
- **The form the reviewers call "A2"** (`var o = {}; o.F = function () { this.p = 1; }; o.F.prototype.m = function () {};`)
  needs no new text. Both reviewers find that E1 decides it, and v2 keeps it: `#o.F~p` is excluded (C22; C27 names
  variables only), and `#o.F~m` is a row (C13).
- The default rule `native.symbol-census-population.default.v1`; no schema, wire member, deficiency, carrier or binding.

## FCE2.7 Review and binding owed

- **Review:** both reviewers of E1, before any rule is first bound to a closure.
- **Binding owed:** the lead's adoption receipt pinning this file's sha256. The owed FA-2 contract successor states v2 in
  §9.8, with E1 and this erratum.
- **Code owed:** CENSUS-RULE-1a's fix (FCE2.4), the golden cases (FCE2.5), and the move of its id references to v2.

## FCE2.8 Changes from r1 (`5681ca6e9`)

| Finding | Change |
|---|---|
| Lead ruling; FCE2-CX-2 | a new id, v2, is defined as E1's v1 unchanged plus two statements. v1 is withdrawn before use. Every r1 sentence that let non-use permit reusing v1's id is removed, and E1:54 and E1:132 are quoted and followed |
| R-E2-1; FCE2-CX-1 | "alias" is defined by meaning, and C19's list is illustrative. Entity-name exports are aliases, and the code matches. C18's exception is quoted and kept. C3, C5, C16, C18 and C19 each get one line |
| R-E2-2; FCE2-CX-3 | TypeScript `export = class Named {…}` and `export = class {…}` are decided (`(export=)`, fix owed). r1's "only CommonJS JavaScript" is withdrawn. The forms that do not move are listed |
| Claude advisory 1 | `module.exports.K = class …` is named (fix owed, golden case 3) |
| Claude advisory 2 | FCE2.3 says that `run.ts` still sends a census when the token is negotiated, and that non-sending holds by law and the skipped test |

# Erratum FA2-CENSUS-E1: a symbol census is complete over a named population rule (author draft, 2026-11-13)

Status: **PROPOSED.** It implements lead decision LD-DEC-11 items 1-7
(`LC/decisions/LD-DEC-11-census-population/DECISION.md`, `LC` = `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`),
with the red team's findings 1-6 (`REDTEAM.md`) and the cross-vendor reviewer's CX-4 advice
(`LC/f2min/review-codex/VERDICT-3-fix1.md`). Origin: finding F2-CX-4. It is **additive**: the accepted bytes stay frozen.

Corrects one accepted text: **contract successor FA-2** (native-evidence §9.8, the symbol census), at architecture main
`12084f90d`, as pinned by its subject manifest `native-successors-fa/fa-2-subject.json`:
- `docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md`, 8,270 bytes, sha256
  `2769b0935a7e1fd0d8b7a76c245d44dee7cd08588379f21a34f2be17c2e2e6c0`;
- `docs/implementation/m3/native-successors-fa/fa-2/README.md`, 37,836 bytes, sha256
  `59381765049d16320eb8d1886fb0f5a51651485d0e3c9ddea3641d5691225af7`.

Line numbers below are those files' (`9.8:N`, `README:N`).

**Which record form applies.** FA-2 is a lock input: the product's `design-lock.json` (product main `fc28bce2`) binds it
as a `contractSuccessors` entry, record `fa-2/successor.json` (38,659 bytes, sha256 `f6b105f4…`) at `:7840`, subject
manifest `fa-2-subject.json` at `:7845`, review `reviews/codex-fa-2-r2/review.json` at `:7850`, assent `fa-2-unit.json`
at `:7855`. So, like VCS1-E1 (`../errata-2026-11-13/ERRATUM-VCS1-E1.md`), this correction needs a contract successor:
a record, a subject manifest, a review, an assent and one lock entry. This file is its text. They are owed, not
generated here (FCE1.9).

Model and form: `../errata-2026-11-13/ERRATUM-VCS1-E1.md` and `ERRATUM-SUPERVISOR-TOOL-EVENT-E1.md`.

Product facts read (read-only), branch `f2min-fix-1-r1` at `61ae5fb2`, worktree `opensip-fix-f2min`
(`P` = `providers/typescript/src/facts`): `P/census.ts`, `P/candidates.ts`, `P/subject-ids.ts`,
`tools/typescript_closure.py`. Design note: `LC/f2min/DESIGN-NOTE-r5.md` (`N`).

## FCE1.1 The accepted sentences

`9.8:3-5`:

> A TypeScript or Rust provider's symbol census is its explicit population assertion (the header above; identity §4): the first-party symbols its program declares over the binding's symbol extent (enumeration contract §5), with the paths it examined.

`9.8:56-57`:

> Rows name first-party symbols only: an external symbol is not a row, and a symbol with no fact is still one.

`README:282` (cascade row X-FA2-FG, column "Item"):

> The emission duty of §9.8: the census in the same compiler pass; rows for every first-party symbol, including those with no fact; every source-side subject of the worker's symbol-kind candidates has a row; no external symbol is a row; scope2 computed with the foundation encoder, conformance-tested on `vectors.json`. Signed capability rows of releases that implement it carry `symbol-census-v1`.

**Why they cannot stand for TypeScript.** The TypeScript census does not hold every first-party symbol. Its walk
reaches only the file's top-level tables, export tables and the members of named containers (`P/census.ts:237-340`);
a symbol in a function or block scope gets no id (`P/census.ts:442`, "P5 local: no id"), and anonymous symbols are
skipped with their members (`:134`, `:657`). The exclusion was a design-note choice with a stated reason (no stable id
for a local; `N` §2 P5, §6), and it never reached law, so a committed census claimed more than it held (LD-DEC-11,
"Dissent"). The counts are in `LC/f2min/fix-1/CX4-OPTIONS.md` §4 and are not repeated here.

## FCE1.2 The amendment

**`9.8:3-5`** is read as:

> A TypeScript or Rust provider's symbol census is its explicit population assertion (the header above; identity §4) under one named population rule: the first-party symbols its program declares over the binding's symbol extent (enumeration contract §5) that the rule selects, with the paths it examined. The default rule, `native.symbol-census-population.default.v1`, selects the first-party symbols its program declares over the binding's symbol extent, all of them; it is the rule of every provider that names no other. A provider names another rule only in the token note bound by digest to its closure build, and only a rule stated in this section. A census's `complete` state and its row count describe its rule's population and no wider one. Rule ids are immutable (erratum FA2-CENSUS-E1).

**`9.8:56-57`** is read as:

> Rows name first-party symbols of the census's population rule only: an external symbol is not a row, a declaration the rule excludes is not a row, and a symbol the rule includes that has no fact is still one.

**`README:282`**: the words "rows for every first-party symbol, including those with no fact" are read as:

> rows for every first-party symbol of the census's population rule (§9.8 as amended by FA2-CENSUS-E1: the default rule, or the rule the provider's token note names), including those with no fact

The rest of `README:282` is unchanged, "every source-side subject of the worker's symbol-kind candidates has a row"
included.

**A new paragraph of §9.8**, inserted after `9.8:11`: the TypeScript rule of FCE1.3, and the paragraphs of FCE1.4 and
FCE1.5. They are the rule's only statement. No other text restates them.

For any provider that names no rule, nothing changes: the default rule is the accepted wording of `9.8:3-5`. The Rust
provider names none, so its obligation is unchanged (LD-DEC-11 item 1; red team finding 2).

## FCE1.3 The TypeScript rule `native.symbol-census-population.typescript.v1`

Inserted into §9.8 as written. Each class was checked against `P/census.ts` (cited) and `N` §2-§6. Where the two
differ, the text follows the code, and the difference is listed in FCE1.10.

> **The TypeScript population rule `native.symbol-census-population.typescript.v1` (erratum FA2-CENSUS-E1).** Under this rule a census row is a declaration in an extent code file of one of the included classes below, and of no other.
>
> Included:
> 1. **Files.** Each examined code file is one row, whether it is a module or a script; a module's own symbol is that same row. A JSON root is examined and is not a row.
> 2. **Module top level.** Each entry of a module file's top-level binding table, of any declaration kind. Each export-table entry that has no binding in the file: the CommonJS forms `exports.x =`, `module.exports.x =` and `Object.defineProperty(exports, 'x', …)`, an export declared only by a module augmentation, a `module.exports = …` value that is not an alias, and a default-exported value.
> 3. **Script top level and globals.** Each declaration at the top level of a script file, and each declaration in a `declare global` block.
> 4. **Ambient modules.** Each string-named `declare module` in an extent file whose target is not a file of the program.
> 5. **Members of a reached named container.** Of a class or interface: its instance members (parameter properties, and the JavaScript `this.x =` and prototype-assignment forms, included) and its call, construct, index and constructor signatures. Of a class: its static members other than `prototype`. Of a JavaScript constructor function: the properties of its construct signature. Of every reached container (a namespace, enum, class, function, ambient module, or a module an augmentation merges into): the entries of its export table that are not aliases. A member is a row only when it has a declaration in an extent file; a container declared outside the extent is walked for such members.
>
> Excluded, by name:
> 1. Aliases with no declared meaning of their own: imports, import-equals declarations, export specifiers and re-exports. An alias merged with a declared meaning is not excluded by this class.
> 2. Function and block locals, catch variables included.
> 3. Declarations of a namespace block that the block does not export.
> 4. Parameters, other than parameter properties. Type parameters.
> 5. Local function, class, enum, interface, type-alias and namespace declarations.
> 6. The names of function expressions and class expressions.
> 7. Symbols the compiler leaves anonymous, with every member under them: function and arrow expressions, class expressions, object literals (`module.exports = {…}` and `export default {…}` objects included), type literals and JSX attribute sets.
> 8. JavaScript forms the compiler binds to no symbol, such as `exports[k] = …`.
> 9. Compiler-internal entries of the top-level tables: `__export`, `__global`, the CommonJS `module` symbol, and a string-named module entry that is not an ambient module.
> 10. The four A7 cases: a member with no compiler symbol (a computed or bigint name the checker does not bind, or a late-bound key with no unique-symbol declaring symbol); a member keyed by a unique symbol whose declaring symbol has no id under this rule; a member of a `node_modules` file with no package segment; and every member whose id depends on an ambiguous external name.
>
> **The two-copies rule (R2) reaches this rule's population only.** An external name is ambiguous when two distinct named external symbols that this rule's walk reaches compute it. A symbol reached only from a declaration this rule excludes does not count.
>
> An included declaration that cannot be given its row for any other reason is not left out: the worker does not send `Complete` (`9.8:64-65`).

The code for each class:

| Class | `P/census.ts` |
|---|---|
| Included 1 | file row `:582`; the module symbol is seeded (`:583-584`) and not emitted again (`:699`); JSON `:568` |
| Included 2 | locals table `:292-307`; export-only entries `:308-313`; aliases and internal entries filtered `:274`, `:293` |
| Included 3 | seed scan by scope `:619-622`, scope test `:199-210` |
| Included 4 | `:616-618`, `isAmbientModule` `:212-214` |
| Included 5 | instance side `:317-322`; constructor function `:323-329`; static side `:330-335`; export tables `:336-338`; extent test `:680` |
| Excluded 1 | `pureAlias` `:216`, applied `:274`, `:293`, `:337`, `:455` |
| Excluded 2-6 | none of these is in a table the walk reads (`:237-340`); `containerOf` gives them no id (`:442`) |
| Excluded 7 | `ANON` `:134`, skipped with its members `:657` |
| Excluded 8 | the compiler binds no symbol; no code |
| Excluded 9 | `isBogusTop` `:217-220` |
| Excluded 10 | `:624-631`; `segOf` `:381-383`; `homeOfFile` `:365`; R2 `:466-470`, `:671-677`, two passes `:735-737` |

## FCE1.4 Relations under the TypeScript rule

Inserted into §9.8 after the rule:

> **Relations under `native.symbol-census-population.typescript.v1`.** Only `imports` and `unresolved-edge` are advertised under this rule. Their source field (`importer`, `referrer`) names the row of the file that holds the import site, wherever in that file the site is. Any other symbol relation needs its own reviewed law for the attribution of its source and target fields before it is advertised under this rule.

Verified: `P/candidates.ts:63-77` builds the `importer` of `imports` and the `referrer` of `unresolved-edge` from
`moduleSubjectId(o.site.file)`, the file's path-home id (`P/subject-ids.ts:154-157`); the target of `imports` is also a
file id (`:68`). The draft token note registers one relation row, `[["imports", "resolved-target"]]`
(`LC/f2min/token-note.DRAFT.md`).

This erratum makes no statement that a fact is attributed to an enclosing row. Such an attribution is an aggregation
that needs its own relation law (`VERDICT-3-fix1.md`, CX-4 advice; red team finding 1).

## FCE1.5 Widening

Inserted into §9.8 after FCE1.4:

> **A wider population is a new rule.** It has a new rule id; an id is never re-used for another population. A wider rule is not promised to be additive: under it a row of this rule may get another id or no id. Runs made under different rules are not promised to be comparable.

Why it is not additive (red team finding 3):
- **R2.** A wider walk reaches more external symbols, for example through the computed keys of members of local
  classes. An external name that this rule's walk reaches once can then be reached twice. It becomes ambiguous, and a
  row of this rule that depends on it falls into A7 case 4 under the wider rule: its id disappears.
- **A7 case 2.** A member keyed by a unique symbol whose declaring symbol is a local has no row here. Under a rule that
  gives locals ids, it gets one, and so do facts about it.
- **Ids.** The id grammar G1 (`providers/typescript/SUBJECT-IDS.md:18`) has no form for a declaration inside a function
  or block (`CX4-OPTIONS.md` §3). A wider rule may need a new grammar, which is not this erratum's.
- **Attribution.** A relation advertised under a wider rule may name a source that this rule cannot name, so a finding
  keyed to a row of this rule may not carry across.

## FCE1.6 Consumers (obligations owed; nothing is implemented)

These obligations follow from LD-DEC-11 item 5. They are owed by the named units. This erratum does not amend their
texts.

- **The evaluator** (owner of `foundation/evaluator-composition-contract.v3.md`): a rule whose primary subjects
  include declarations outside the population rule of the census that covers it is refused or reported incomplete.
  Such a census never yields complete-empty or pass for it. Today a complete inventory can yield complete-empty
  (`evaluator-composition-contract.v3.md:26`). This is the latent route of red team finding 5. M3's one rule,
  `module-import-cycle`, is file-kind and is not affected. The lead records the gate "before any symbol-kind rule
  ships" on the path document (LD-DEC-11 item 5).
- **The reporting and command-line units** (owners of the surfaces): every surface that reports symbol completeness
  names the rule id of the census behind it.
- **The carrier.** No wire member, schema member, deficiency or cause is added (`9.8:107-108`). How the evaluator and
  the surfaces learn a census's rule id from its enumerator closure is not designed here (FCE1.10, open point 3).

## FCE1.7 Binding to the code

- **The token note names the rule id and restates nothing.** The note is the file passed as `--token-note` to the
  product's `tools/typescript_closure.py` (`build`, `:343-347`). Its sha256 is pinned as `tokenNoteSha256` and checked
  before anything is built (`bound_tokens`, `:211-235`). It is recorded as `tokens.noteSha256` in the closure build record
  (`:465-466`). For F2-min the note does not exist yet. Its draft is `LC/f2min/token-note.DRAFT.md`; the bound copy is
  `LC/f2min/closure/<C8>/INTERFACE-NOTE-f2min-to-f4.md` (`LC/f2min/CLOSURE-REPACKAGING.md:13`, `:27`). It owes one
  sentence naming `native.symbol-census-population.typescript.v1`. Its traceability line for `symbol-census-v1` ("the
  first-party symbol census on `Complete`") also names the rule id.
- **The conformance golden is owed as code unit CENSUS-RULE-1.** It has one case per class of FCE1.3, included and
  excluded. It passes on the code, and it fails when a class is added to or dropped from the population. The existing
  98-case corpus (`src/test/census-corpus.test.ts` against `fixtures/census-golden.ts`) is the design note's, and it is
  not organised by class. I did not establish which classes it covers.
- **No product code is changed by this erratum** (LD-DEC-11 item 6).

## FCE1.8 What this does not change

- **The census schema.** `fa-2/design/native/symbol-census.schemas.v1.json`, 19,045 bytes, sha256
  `95d84054ba8d0d37cff59198df3f0c9d33a7701f259298ca2f068f05cf07ad21`: not edited. The product pins it byte for byte
  under ledger id `opensip.product.symbol-census.1` (`opensip/tools/replay/id-ledger.json:435`, same sha256). No change is
  needed, because the schema states no population. Its `return` law (`:12`) defines the variants by size only, and its
  row text (`:138`, "One first-party symbol") is still true of every row under either rule. Its `standing` (`:7`) makes it a
  restatement of §9.8, and the two do not differ after this erratum. An edit would change bytes under a pinned id, or
  would need a new id, which is a code change (red team finding 6).
- **The enumeration contract.** Its `complete` state for `kind=symbol` is defined by examined paths, with no row totality
  (`enumeration-contract.v1.md:119`, `:178`). The extent is a path scope (`:132`), and the host does not recompute symbol
  rows (`:186`). A census complete over a named rule is consistent with all four lines, so they are not amended.
- **The rest of §9.8.** The extent, `examinedPaths`, the variants and bounds, the commitments, the terminals and refusals.
  `9.8:64-65` ("no `partial` and no `unavailable` census") stands, and an included declaration the worker cannot row
  still takes it (FCE1.3, last sentence).
- **No wire member, deficiency, cause, D9 code, frame, token or schema** (`9.8:107-108`). `symbol-census-v1` is unchanged.
- **The evaluator contract** (`evaluator-composition-contract.v3.md:24-26`, `:46`) is not amended. Its collision class at
  `:46` runs over the population that was enumerated, which is now the census rule's.
- **Rust.** No rule is named for it, and the default rule is the accepted wording.

## FCE1.9 Controls, review and binding owed

**Controls** (LD-DEC-11, "Controls that follow"):
1. CENSUS-RULE-1's golden passes, and it fails when a class is added or dropped.
2. The token note names the rule id, and its digest is pinned and recorded in the closure build (FCE1.7).
3. The path document carries the gate "before any symbol-kind rule ships" (the lead's).
4. **The item 7 measurement is recorded before the body-parser Run.** On fixture `js-small-body-parser`: whether the
   package's public surface (`module.exports = …` objects and their members, nested functions and callbacks; excluded 7,
   2 and 5) falls into the excluded classes, with the count. The excluded counts measured so far are `CX4-OPTIONS.md`
   §4's. That table does not say what the public surface is, and I did not establish it. If the census misses the package's exported
   surface, that goes to the lead before the Run is recorded, and the rule's included classes are revisited (LD-DEC-11,
   "What would reverse this").

**Review: two independent reviewers**, both independent of the DESIGN-NOTE-r5 rulings that confirmed the exclusion
(LD-DEC-11 item 6; red team finding 8). F2-CX-4 closes when this erratum is accepted and bound. Until then F2-min is at
risk and is not integrated.

**Binding owed (not generated):** a contract successor carrying FCE1.2-FCE1.5 as overrides and an insertion on FA-2's
§9.8 and `README:282`, with its subject manifest, the two reviews, the unit assent and one `contractSuccessors` entry in
the product's `design-lock.json`. The choice between a replacement FA-2 record and a second successor is the binder's, as
in VCS1-E1.6.

## FCE1.10 Open points

**Where the code and the design note differ** (the rule follows the code):
1. **Attribution.** `N` §6 says a fact from code with no row names "the nearest enclosing row … as its referrer, caller or
   subject", and that this binds later F2 units and G3. The code names the file for `imports` and `unresolved-edge`
   (FCE1.4). `N` already says this for `imports`, but says nothing for `unresolved-edge`. This erratum does not adopt
   `N` §6's attribution paragraph, and `N` owes a correction. The note's statement "the product can repeat" (`N` §6)
   ends with the same attribution sentence. The product's copy (`providers/typescript/SUBJECT-IDS.md`) omits it.
2. **Widening.** `N` §10 says "Widening the population is a new enumerator closure that only adds ids". FCE1.5 replaces
   this, and `N` owes a correction.
3. **Anonymous containers.** `N` P5 excludes "members of anonymous containers". The code excludes members of the compiler's
   anonymous symbols (`:134`, `:657`). The members of an anonymous default-exported class declaration are rows
   (`#default~m`, `N` §8 W4), because that symbol is named `default`. Excluded 7 states the code's form.
4. **File and module symbol.** `N` P1 says "a file row, plus its module symbol". The code gives one row for both (included 1).
5. **The normative reference.** `N` §0 makes `design-probes/census-r5.cjs` the rule. `P/census.ts:1-4` still calls itself
   a port of `census-r4.cjs` of DESIGN-NOTE-r4, while later comments cite r5 (`:269`, `:506`). Under this erratum the
   rule is the text of FCE1.3, and the reference and its golden are conformance evidence.

**Where LD-DEC-11's summary is narrower than the code.** Item 2's excluded list does not name aliases, namespace-block
locals, dynamic JavaScript forms, JSON roots or compiler-internal entries. The code excludes all of them, and `N` P1 and
P5 name the first two and JSON roots. FCE1.3 names them.

**Not established (CENSUS-RULE-1's golden should settle each one):**
1. **A `var` nested in a top-level statement** (a block, `if` or `for` head). In a module file it hoists into the file's
   top-level table, which the code reads (`:292`), so it is included. In a script file the seed scan tests the syntactic
   scope (`:199-210`, `:619`), and I read that as not seeding it, so it is excluded. I did not run the code. If the two
   differ, the rule's included 2 and 3 must say so.
2. **JavaScript JSDoc type declarations** (`@typedef`, `@callback`). A file-scope one becomes a row in a CommonJS module
   (`N` §5, case F5). Where the compiler binds those declarations in other files, I did not establish, and FCE1.3 does not
   classify them separately.
3. **The rule id is not in the closure identity.** P's `closure2` covers the dist and the note's token and relation lists
   (`tools/typescript_closure.py:446-452`), not the rest of the note. The rule id is bound through the pinned note digest
   and the build record only. A changed rule changes the code, so in practice it changes the dist and `closure2` too, but
   nothing checks that. The carrier from enumerator closure to rule id for the evaluator and the surfaces (FCE1.6) is open.
   Panel A did not establish whether the F4/G2 closure manifest has a field for it.
4. **R2's dependence on reach.** A row of this rule can fall into A7 case 4 when a new reference to a second copy of an
   external package is added. `N` §11 lists this as an attack point. The reviewer's CX-4 advice says ambiguity must not
   silently remove an included subject. Here it is an excluded class by name (excluded 10), and it is disclosed only on
   stderr (`N` §6).

**Ids proposed by this author.** Neither id is in the decision. Searched with no hit: the architecture, product and
F2-min repositories, and `LC/decisions`. The form follows `native.semantic-universe.typescript.v2` and
`native.import-payload.dependency-source.v1`. The decision names no id for the default rule. One is given so that a
surface can name the rule of a Rust census (FCE1.6).

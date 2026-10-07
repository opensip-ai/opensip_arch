# K2c literal candidate and representation recipes r1

ACCEPT. requiredFindings empty. parserRuns 0. producerRuns 0. laneFrozen false. fullK2cComplete false. productQualification false.

This is conditional ground-truth authoring for 25 numeric spellings and 8 representation vectors. It does not freeze a T1 oracle, bind an inventory, or amend a law. The accepted finite source, L0–L3, near-pair, branch, and syntax-candidate worksheets stay closed, as do E0, E2a, SYN-NS, J3b, and the C3 producer evidence.

Subject manifest `docs/implementation/m3/harness/k2c-literal-candidates-r1-subject.json` is 5627 bytes, sha256 `ce821e9fe26321a7b53371e0813dfd65ded4cb3366f76bd18daa6eb488e2c700`. All 24 members match their byte and hash pins. Their paths are sorted and unique.

## Pins

Product HEAD is base `bf1ce2566120bcb7db339c3c8a1ee3853f300c8c`. Architecture HEAD is base `4d79d7f9a69c41aef311bcde9a3954d37b07681e`. At those commits, `PROPOSAL-r4.md` is 133352 / `ed4f1fec5a7e11293f48724e349afc0ca8bf9b7b2e46e761efac25a4f7d8764c`, `normalizer.v1.json` is 43373 / `e4a648f015945b0749af6314b83d62a51df94031457a0cad6b0f54f2718b5867`, `DESIGN-r13.md` is 151216 / `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`, and the existing syntax-candidate worksheet is 109930 / `ecd3750591002b3b10643edff8024d7deaeaeda9d7369fed4fe29b447f8dd56b`. Product `tools/grammar/lane.json` is 29621 / `549190e32dcbf231a2e46c675a41ad9d6613efb3b507df2d6bd33aba7b27b5f8`.

The three selected E2a crate pins match the staged archives: JavaScript 0.25.0 is 151425 / `68204f2abc0627a90bdf06e605f5c470aa26fdcb2081ea553a04bdad756693f5`, Rust 0.24.2 is 368844 / `439e577dbe07423ec2582ac62c7531120dbfccfa6e5f92406f93dd271a120e45`, and TypeScript 0.23.2 is 829457 / `6c5f76ed8d947a75cc446d5fccd8b602ebf0cde64ccf2ffa434d873d7a575eff`. Each copied grammar, node-types, and Rust `scanner.c` member is a regular archive member, and its bytes match both the receipt and the lane's archive pin. No archive tree was extracted.

## Numeric spellings

The four fixtures are hand-authored. JavaScript, TypeScript, and TSX are the same 159 bytes. TSX keeps `grammarId` `tsx` and `languageId` `typescript`. Rust adds `1u64` and is 179 bytes. The 25 worksheet spans match those bytes. Each `rawText` equals `valueText` and the exact source slice, so `1.0`, `1e0`, `0x1`, and `1_000` stay spellings. The six recipe names are `plain`, `fraction`, `exponent`, `radix`, `grouped`, and, for Rust, `suffixed`, plus `negative-operand`. No parser output supplies those labels.

The retained `number` token is the same object in each staged grammar and in `literal-rule-excerpts.json`. It admits `1`, `1.0`, `1e0`, `0x1`, and `1_000`, and it does not admit a leading minus. JavaScript and both TypeScript grammars have no external `float_literal`. Their node-types list `number`.

Rust `integer_literal` matches the staged token rule: decimal or `0x` digits with underscores, plus an optional suffix that includes `u64`. That rule admits `1`, `0x1`, `1_000`, and `1u64`, and it does not admit `1.0`, `1e0`, or a leading minus. `float_literal` is an external symbol on `_literal`, not an inline rule. `scanner.c` accepts a digit run as a float only when it has a fraction or an exponent; `_` counts as a numeric character, and a minus is outside that scan. Static application of that scanner admits `1.0` and `1e0` and rejects the integer spellings. In expression position the grammar's form is `unary_expression`, whose `-` sits outside the following literal. The fixture's tail `-1` is that form. Each negative-operand span is the single byte `1`, and the preceding byte is `-`.

## Representation vectors

The pinned normalizer sentence is the literal law used here: escape each C0 or C1 character to backslash, `u`, and four uppercase hexadecimal digits; put that text in NFC; if the result is longer than 4,096 characters, keep its first 3,996 characters, U+2026, `sha256:`, and the SHA-256 of the whole step-2 UTF-8. `valueText` is a representation. The anchor, not the display, locates the exact bytes.

Independent Python Unicode 16.0.0 recomputation matches all eight stored vectors. `c1-control` contains U+0085 and `literal-escape-text` contains the six characters of `\u0085`; their raw UTF-8 differs and their `valueText` is the same. `decomposed-accent` turns `e` plus U+0301 into `é` only at the NFC step. `control-before-nfc` escapes U+0001 before that composition. The 4,096-character vector is kept. The 4,097-character vector becomes 4,068 characters. The two `é` vectors are 4,096 characters / 8,190 bytes and 4,097 characters / 8,192 bytes, so the threshold follows scalars. These are the explicitly owned ASCII, C0, C1, and Latin-accent vectors. No product normalization engine is selected.

The worksheet records `parserRuns` 0, `producerRuns` 0, `frozen` false, and `fullCaseSet` false. `source.json` records the same run counts, `laneFrozen` false, `fullK2cComplete` false, `D13OwnerAssent` false, and `productQualification` false. `checks.json` records the same counts and Unicode 16.0.0. The author and check scripts write, so they were not executed. No grammar, parser, compiler, or producer was run, and these spellings are not treated as parse successes, admitted facts, minted anchors, or exit, work, or stress expectations.

L, day 0, D13, and the owner and held prerequisites remain pending. `~/Library/Application Support/OpenSIP` is absent. Neither repository was edited.

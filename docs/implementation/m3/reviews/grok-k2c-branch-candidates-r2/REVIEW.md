# K2c independent finite branch candidates r2

Verdict: ACCEPT.

K2C-BR-01 is closed. The TSX worksheet row records `grammarVariant` `tsx` and `bodyLanguage` `typescript`. `author.py` sets `bodyLanguage` to `typescript` when the grammar is `tsx` and otherwise uses the grammar name, and its finite assertion expects that map. JavaScript, Rust, and TypeScript rows record body language equal to their grammar variant. This matches SYN-NS bodies law in the pinned normalizer: `languageId` is the row's body language, typescript for both the typescript and tsx rows, and dialect stays the grammar variant. The finished r1 review was not rewritten.

## Subject

Subject manifest `docs/implementation/m3/harness/k2c-branch-candidates-r2-subject.json` is 866 bytes, sha256 `805bf4e122d6c75a3812daf9cf730fed360e4e85bf1133d4cc540d5acadafaf7`. The four archive members match it: README.md 2322 / `8120ca28ac96016d2fdb1c0d5318ca3d8c304c6dfed4e20290b9ee37f43fdbae`; author.py 6652 / `61b6c4e5523953595904809a377a01748db10e031aa8ae9d3eed0192f0b616bc`; branch-candidate-worksheet.json 22528 / `7acb306cf027c8c9aef2de2350036ab789d56c0d1acde1fe2f920620e9612112`; checks.json 309 / `8e4a267783f7b9512a9868554c5f9441de6b7a1988668f4aad79b24afbe7d9df`.

The four accepted syntax-control sources, the normalizer (43373 / `e4a648f015945b0749af6314b83d62a51df94031457a0cad6b0f54f2718b5867`), E1 r4, and the linear candidate manifest match the review pins. Worksheet standing is `INDEPENDENT-FINITE-BRANCH-CANDIDATE-EXPECTATIONS-NOT-FULL-ORACLE`. Aside from the TSX body language, the worksheet matches the r1 recipe.

## Recipe check

Counts are seven declarations, twelve numeric literals, four graphs, twelve statements, and twenty edges. Function anchors are the file bytes excluding the trailing newline. Body anchors start at the opening brace and end at that same end byte. Lengths are 56, 46, 56, and 56 raw bytes, all below `parameters.minBodyBytes` 64, so these isolated controls owe no clone group and no near pair. Entry-edge anchors equal the body span. Every other edge anchor equals its from statement. Subjects carry `@0` ordinals and no byte offsets.

JavaScript-family flow is branch-true to the nested `return 7;` and branch-false to the following `return value + 1;`, and both of those edges are `return` to exit. Rust's tail `if_expression` is branch-true to the consequence `integer_literal` `7` and branch-false to the alternative `binary_expression` `value + 1`, and both of those edges are `fallthrough` to exit. Rust records one function declaration and no parameter row. Each JavaScript-family file records the function and one `value` parameter. Each numeric literal slice is the single byte `0`, `7`, or `1` at its first occurrence. `author.py` imports only `hashlib`, `json`, and `pathlib`.

`checks.json` records `mechanicalSpanAndEdgeAssertionsPassed` true, `parserRuns` 0, `compilerRuns` 0, `producerRuns` 0, `laneFrozen` false, `fullCaseSet` false, and `productQualification` false. This review did not run `author.py`, a parser, a compiler, Cargo, a package manager, a provider, a T1 producer, or corpus analysis. No Fact2, Body2, Coverage, context, universe, full normalized atom, case, exit, work, stress, roster, freeze, or qualification claim is accepted. Whole-lane QD26 remains outstanding.

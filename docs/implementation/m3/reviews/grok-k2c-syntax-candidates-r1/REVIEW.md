# K2c finite syntax candidate expectations r1 — ACCEPT

This accepts the frozen authoring component at `/tmp/opensip-implementation/k2c-syntax-candidates-r1`. It records inert declaration, literal, and control-flow expectations for four accepted clone-identical sources. `laneFrozen` is false. `fullCaseSetPresent` is false. It is not a full case set or a lane freeze, and it proposes no product installation or inventory successor.

## Pins

`subject-manifest.json` is 353 bytes, sha256 `28f96ffdf420daf4fa37e24c689be827526f3bf0489ad1e843ec5cd02ed08454`. Its two rows match `subject.json` and the bytes on disk. The directory contains those two files and the manifest.

`DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. `normalizer.v1.json` is 43373 bytes, sha256 `e4a648f015945b0749af6314b83d62a51df94031457a0cad6b0f54f2718b5867`. The accepted source manifest is 5098 bytes, sha256 `2c8be8c6e4606808533188ecca19bca7fed46fdbd4ebb4725d93cc2fb3f5f240`. The lead assent is 1216 bytes, sha256 `d6c915bea2809b7a2ab63c23fb8446e3a504e4f571180bead89b09439d3ed05f`, with `rootSubstantiveAssent` true and that same manifest digest. The four source rows in that manifest match the worksheet pins: javascript 667 bytes `6af31d6bb9a5828cd00a6f2019f41ae8f4c948c6b3f405498931a5616ef2838d`, rust 676 bytes `b499592d16488ec4a0c6a21986a9a237b228dad813cf2b0d808648ccfbcef3d9`, and typescript and tsx both 683 bytes `8709854f4836621ceee6a5b2c69eb2173d63b567c06cfb074edf6ee453feddbb`.

The retained grammar `grammar.js` and `node-types.json` bytes match the architecture pin tables for javascript, rust, typescript, and tsx. No parser was run.

## Expectations

Each case is one isolated file. The logical path is the leaf name: `clone-identical.js`, `clone-identical.rs`, `clone-identical.tsx`, and `clone-identical.ts`. The file subject is `syntax:` plus that path plus `#`. Typescript and tsx share source bytes. The tsx row keeps body language `typescript` and grammar variant `tsx`.

Each file has two function declarations, `first` and `second`, both ordinal 0 because the names differ. The anchor is the whole function. Javascript spans are `[0, 332)` and `[333, 666)`. Rust spans are `[0, 336)` and `[338, 675)`. Typescript and tsx spans are `[0, 340)` and `[341, 682)`. Each function is a container. Its body is the function body, and the ordinary function block is not a second block body.

A javascript or typescript function also declares the parameter `value` and the ten const bindings `value0` through `value9`. Those anchors are the identifier spans, and each ordinal is 0 under its own function chain. Rust plain `let` and parameter identifiers are not binding forms, so the rust file declares only the two functions. The totals are 74 declarations: 24 in each of the three JavaScript-family files and 2 in rust.

Each file has twenty number literals, `1` through `10` in each function. The anchor text is that exact digit text, owned by the enclosing function. The total is 80.

Each function has one graph. The entry and exit subjects extend the function chain with `entry:@0` and `exit:@0`. The entry edge uses the body span: javascript `[22, 332)` and `[356, 666)`, rust `[32, 336)` and `[371, 675)`, typescript and tsx `[30, 340)` and `[372, 682)`. Ten declaration statements lead to one tail. JavaScript-family statements are `lexical_declaration` ordinals 0 through 9 and `return_statement` 0; the return edge reaches exit. Rust statements are `let_declaration` ordinals 0 through 9 and tail `identifier` 0; that identifier falls through to exit. Every other edge is fallthrough, and its anchor is the source statement. Each graph has 12 edges. Eight graphs give 96 edges. No statement subject carries a byte offset.

The worksheet states that these rows are conditional on an admitted single-file snapshot and a parsed tree. It does not supply a context, closure, Fact2, Coverage identity, normalized atom, full evidence anchor, exit, or stress bound.

## Checks

Read-only span and subject checks used `nice -n 10 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`. The clock before that run was 2026-10-06T08:24:59Z. No parser, compiler, producer, Cargo, package command, lane lock, or network command ran. No `HOME` assignment was made. `~/Library/Application Support/OpenSIP` was absent.

Admitted context and body-language version, full source-text anchors, Fact2 and Coverage identities, normalized atoms, case records, exits, work and stress controls, malformed trees, the whole lane review, and the QD-26 freeze remain pending.

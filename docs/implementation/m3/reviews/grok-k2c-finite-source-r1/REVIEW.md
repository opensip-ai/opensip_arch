# K2c finite source and L0/L1/L2 payload authoring r1 — ACCEPT

This accepts the frozen authoring component at `/tmp/opensip-implementation/k2c-finite-source-r1`. It is a finite source and normalization-payload worksheet. `laneFrozen` is false. `fullCaseSetPresent` is false. It is not a K2c oracle, a lane acceptance, or a QD-26 freeze, and it proposes no product installation or inventory successor.

## Pins

`subject-manifest.json` is 5098 bytes, sha256 `2c8be8c6e4606808533188ecca19bca7fed46fdbd4ebb4725d93cc2fb3f5f240`. Its 30 rows match `subject.json` and the bytes on disk. The directory contains those 30 files and the manifest. The source census has 20 code files, five in each of javascript, rust, tsx, and typescript, plus four data documents.

The authorities match their pins, including `DESIGN-r13.md`, `PLAN-r6.md`, `PROPOSAL-r4.md`, the SYN-NS readme, `normalizer.v1.json`, and the L0, L1, and L2 level specifications. The lane file's matrix pin matches `native-capability-matrix.v2.json`, 36595 bytes, sha256 `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14`. Its normalization-map pin matches. The E0 `src/node-types.json` bytes match the architecture pin tables and the worksheet pins: javascript `188a8baa97018edaf63bf7ece372c07bc0d74d1301004bc8f211eb7dee5a6e70`, rust `4b73a1248978340336100db455bf0731c23f9190568c9ae62265fa4a80a327d5`, typescript `c790a733fc756b54d4e54dceeb7d2d51e40d8b57136e70277753a75804cce3e3`, tsx `78b5789145286799a27a0a7ecc36cc1bcb151f94ec7fa631b248459867010c8c`.

## Lane obligations

The worksheet keeps all 11 syntax-only matrix rows, in order, with the same capability, state, limitations, deficiency, corpus cases, and note. Four rows are `SUPPORTED-DESIGN`, six are `UNSUPPORTED-TYPED` with `language-tier-unsupported`, and `clones-cross-tsjs` is `NOT-SELECTED`. Four code grammars make 44 per-grammar cells. The remaining list still names normalized atoms and typed exits, admitted closure and identity coordinates, malformed and data-document controls, work and stress bounds, and an independent lane review with a QD-26 freeze before any producer run. `laneComplete` is false. Parser, compiler, and producer runs are 0.

## Identical bodies

Each identical source has two functions. The half-open spans are the brace bodies: javascript `[22, 332)` and `[356, 666)`, rust `[32, 336)` and `[371, 675)`, and typescript and tsx `[30, 340)` and `[372, 682)`. Each pair is byte-equal. Javascript, typescript, and tsx bodies are 310 bytes. The rust bodies are 304 bytes. All exceed the normalizer's 64-byte floor. The inner bytes contain no nested braces, strings, comments, or templates. The L0 payload is a big-endian length followed by those exact bytes. The recorded raw SHA-256 is the digest of the body bytes. The scope text says that digest is not a framed `bodyIdentity`; the outer frame and body-language-version digest stay pending.

The L1 payload is a big-endian token count followed by kind and value frames. It matches the authored token list, and its SHA-256 matches the worksheet. Rust has 73 tokens and no line-break or gap tokens. Javascript, typescript, and tsx have 87 tokens, including 12 `opensip:line-break` tokens whose value is `0x0A`. Every stream clears the normalizer floors of 20 and 50. The typescript entry uses language `typescript` and `grammarVariant` `typescript`. The tsx entry uses language `typescript` and `grammarVariant` `tsx`, and its kinds were checked against the tsx node-types file. Every other kind id is `n:` or `a:` plus a named or anonymous symbol in that grammar's pinned node-types. Walking each body, every token value occupies the next source bytes, and the bytes between tokens are only the whitespace that level L1 drops for that grammar. The two bodies in a file carry the same stream. The near-v1 rule stays the law's 5-token shingles and 800,000 millionths. This worksheet does not supply those L3 scores.

## Comments

Each comment file has two bodies and one plain `//` comment in each body: `// first authored comment` and `// second authored comment`. The comment bytes do not include the newline, are not documentation or directive comments, and are not inside a macro token tree. `commentDirective` is false. The raw bodies differ, and the L1 token lists differ. Javascript-family L1 streams have 89 tokens. Removing the comment merges the two adjacent line-break tokens, leaving the 87-token stream of the identical body. Rust L1 streams have 74 tokens. Removing the comment leaves 73 tokens, with the newlines already absent as insignificant whitespace. That 73-token stream equals the identical rust L1 stream. The derived L2 lists match the authored L2 payloads.

## Other controls

The other twelve code files are source controls only. They are not given atom, exit, or score expectations. The ASI files place `return` and its operand on separate lines in the second function. The property and JSX files keep distinct names, `left` against `right` and `div` against `span`. The rust pair contrasts plain bindings with explicit `mut` bindings. The syntax controls are ordinary branches. The four data documents are `{"value":7}`, a short markdown document, `value = 7`, and `value: 7`. They are census rows of class `data-document` and are not given a code construct or body identity.

## Checks

Read-only hashing, payload decoding, and span alignment used `nice -n 10 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`. No parser, compiler, producer, Cargo, package command, lane lock, corpus fetch, or network command ran. No `HOME` assignment was made. `~/Library/Application Support/OpenSIP` was absent.

Full syntax and semantic atoms, admitted native and grammar context, body-language version and full body identity, typed exits, work and stress bounds, error and refusal controls, independence review of the whole lane, and the ledger freeze remain pending.

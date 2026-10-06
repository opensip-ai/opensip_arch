# K2c finite invalid-UTF8 and routing authoring r1 — ACCEPT

This accepts the frozen authoring component at `/tmp/opensip-implementation/k2c-errors-r1`. It records local expectations for invalid UTF-8 and unsupported routing. `laneFrozen` is false. `fullCaseSetPresent` is false. It is not a full oracle or case set, and it proposes no product installation or inventory successor.

## Pins

`subject-manifest.json` is 1799 bytes, sha256 `bf380830f5560e7ed3cd6308c25b17fd1f6c872c72ebb55c2d08984d47f24902`. Its 11 rows match `subject.json` and the bytes on disk. The directory contains those 11 files and the manifest.

`PROPOSAL-r4.md` is 133352 bytes, sha256 `ed4f1fec5a7e11293f48724e349afc0ca8bf9b7b2e46e761efac25a4f7d8764c`. `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. `native-capability-matrix.v2.json` is 36595 bytes, sha256 `4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14`. The matrix has eleven `syntax-only` rows: `syntax`, `clones-fact`, `clones-near`, and `inventory` are `SUPPORTED-DESIGN`; `imports`, `references`, `calls`, `types`, `reachability`, and `unresolved-edge` are `UNSUPPORTED-TYPED` with `language-tier-unsupported`; `clones-cross-tsjs` is `NOT-SELECTED`.

## Invalid UTF-8

Each of the four files is ordinary source, one `FF` byte, and a trailing `0A`. Strict UTF-8 fails at the `FF`. The prefix before that byte decodes, and the whole file does not.

| File | Bytes | SHA-256 | Offset | Prefix |
|---|---:|---|---:|---|
| `fixtures/javascript/invalid-utf8.js` | 25 | `abf71c7a6c89be94b2a15abf11e18f013d28ce02ff700be635319f7a9790d6fd` | 23 | `function retained() {}\n` |
| `fixtures/typescript/invalid-utf8.ts` | 25 | `abf71c7a6c89be94b2a15abf11e18f013d28ce02ff700be635319f7a9790d6fd` | 23 | `function retained() {}\n` |
| `fixtures/tsx/invalid-utf8.tsx` | 25 | `abf71c7a6c89be94b2a15abf11e18f013d28ce02ff700be635319f7a9790d6fd` | 23 | `function retained() {}\n` |
| `fixtures/rust/invalid-utf8.rs` | 19 | `9711173bb1d32dee3111aa8a9394bbfe7c425a3346d752c29474c7cbf9d17f5a` | 17 | `fn retained() {}\n` |

The javascript, typescript, and tsx files are separate paths with the same bytes. The rust declaration is the rust form of the same empty function. Each worksheet row pins those bytes, records `parserInvocations` 0, outcome `syntax-error`, and empty fact and body candidate lists. Under a separately admitted syntax context and selected code row, the case scope is that single file. The `syntax` and `clones-fact` expectation is `unknown`, `input-closure-incomplete`, `source-parse-error`, `examinedExhaustive` true. Inventory is unaffected. The near record is candidate-only: `isCoverageEntry` false, `groups` empty, and the full candidate envelope pending. No envelope field, exit, or complete atom is supplied.

## Routing

The five routing files are the same 29 bytes, sha256 `95ea80b1e10d501a1f5507b55561db5ae9ba620634046bff1702b3423b569af5`: `# hand-owned routing control\n`. The names are `unsupported.py`, extensionless `unsupported`, `case.TS`, `case.Rs`, and `case.YML`. Each row is `unsupported-file` / `no-bundled-grammar`, stays inventoried, keeps file enumeration available, and is not an outright refusal. The code-scope expectation is `unknown`, `language-tier-unsupported`, `capability-missing`. Parser invocations are 0. The identical bytes under different suffixes are the case-sensitive, no-sniff control.

`clones-cross-tsjs` under `syntax-only` is recorded as not advertised. A request refuses `native.requested-capability-mode-not-selected`. The other admission refusals stay in the conditional preconditions. No context, closure, or fact identity is written. Item 11's provisional bounds are not copied in as selected limits. The pending list still names admitted context and complete atoms, the full candidate envelope and exits, identity-bearing bounds and stress inputs, ERROR and MISSING parser trees, and the lane review and ledger freeze.

`producerRuns`, `parserRuns`, and `compilerRuns` are 0. `laneFrozen` and `fullCaseSetPresent` are false.

## Checks

Read-only hashing and strict UTF-8 checks used `nice -n 10 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`. The clock before that run was 2026-10-06T08:17:09Z. No parser, compiler, producer, Cargo, package command, lane lock, corpus fetch, or network command ran. No `HOME` assignment was made. `~/Library/Application Support/OpenSIP` was absent.

Admitted syntax context, complete fact and Coverage atoms, the full `CandidateProducerResultV1`, exits, case digests, frozen limits, ERROR and MISSING trees, and the lane freeze remain pending.

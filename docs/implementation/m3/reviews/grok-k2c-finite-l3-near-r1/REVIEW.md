# K2c finite L3 and near-pair expectations r1 — ACCEPT

This accepts the three frozen worksheets in `/tmp/opensip-implementation/k2c-finite-l3-near-r1`. They author finite L3 payloads and near-v1 pair scores over the already accepted source bytes. `laneFrozen` is false. `fullCaseSetPresent` is false. This is not a case set, a lane acceptance, or a QD-26 freeze, and it proposes no product or inventory successor.

## Pins

`subject-manifest.json` is 610 bytes, sha256 `d930f9bab95a5ee470a92b78b4c2e505ef9a792d209afeaec8f787b75ea28713`. Its three rows match `subject.json` and the bytes on disk.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `l3-identical-worksheet.json` | 42442 | `c746e183cc684003459be345e9d623f991219d5df0810e3519d7af6fac102b09` |
| `l3-rust-bindings-worksheet.json` | 89280 | `66d7f5149d862c1b87c41806601d0c066c306c0be3dddfa4f1a0464606da049b` |
| `near-pair-worksheet.json` | 167767 | `d21b9c984d63a13ffe6153167caa55c6567865542033cc52dd6ccc26aebaf571` |

The parent manifest, review, and root assent match their pins. The parent review is `ACCEPT` for manifest `2c8be8c6e4606808533188ecca19bca7fed46fdbd4ebb4725d93cc2fb3f5f240`, with `laneFrozen` false and `fullCaseSetPresent` false. The assent records that same manifest, `rootSubstantiveAssent` true, and `productQualification` false. The six source inputs under `docs/implementation/m3/harness/k2c-finite-source-r1` match the pinned lengths and digests. `L3-identifier-insensitive.v1.json` is 27540 bytes, sha256 `6b060a83d9032565487db956f67f1e095789a35462839cac0894c44e42a0d1f6`. The normalizer and `DESIGN-r13.md` match their pins. In the pinned Rust node-types, `mutable_specifier` is one named symbol.

## L3

Replacement follows the level law: renamable names are numbered by first occurrence in the body L2 stream, and each of those occurrences becomes `opensip:local` plus the ASCII decimal. Punctuation, numbers, and JavaScript-family line breaks stay. The L3 payload is the big-endian token count and the token frames, and it matches each authored list.

The four identical pairs each have two brace bodies. Javascript, typescript, and tsx streams have 87 tokens. Inside the body the first names are `value0`, then the parameter reference `value`, then `value1` through `value9`, numbered 1 through 11. All 21 identifier occurrences become `opensip:local`. The function names `first` and `second` sit outside the spans. The typescript and tsx rows use body language `typescript`. The rust identical bodies have 73 tokens. Both plain `let` patterns and the plain parameter are ambiguous pattern identifiers, so R4 keeps every identifier verbatim. The two rust bodies are already the same text, so their L3 streams are equal without renaming.

`ambiguous-patterns.rs` has two different 73-token bodies. `value`/`resultN` and `input`/`outputN` stay identifier tokens. L2 and L3 are both unequal. `explicit-bindings.rs` has two 83-token bodies. Each contains ten named `mutable_specifier` tokens for `let mut`, and the parameter `mut` is outside the body. There is no comment token. `result0` or `output0` is local 1, the later parameter reference `value` or `input` is local 2, and the remaining locals follow by first occurrence through 11. L2 stays unequal because the source names differ. L3 is equal.

## Near pairs

Each shingle is five framed tokens concatenated, with no token-count prefix. Sets drop duplicate shingles. The worksheet lists each set in hex order, and those members are the shingles of the authored L3 streams. Similarity is the floor of `1000000 * intersection / union`. The threshold test is `1000000 * intersection >= 800000 * union`. Every stream has at least 50 tokens. The four identical pairs and the explicit rust pair have equal shingle sets, so the score is 1000000 and the threshold holds: 83 shingles for each JavaScript-family body, 69 for identical rust, and 79 for explicit rust. The plain rust pair shares no shingle. Its intersection is 0, its union is 138, its score is 0, and the threshold does not hold. Each pair has one body language. The six scores are six separate pair expectations. The worksheet does not emit a `CloneCandidateGroupV2` or a Fact2, does not assign candidate ids, and does not change the 800,000 millionths threshold.

## Checks

Read-only hashing, framing, and shingle arithmetic used `nice -n 10 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`. No parser, compiler, producer, Cargo, package command, lane lock, corpus fetch, or network command ran. No `HOME` assignment was made. `~/Library/Application Support/OpenSIP` was absent. The accepted L0–L2 component was not reopened.

Admitted native and grammar context, body-language version, fully framed identities, fact and coverage atoms, exits, whole-universe candidate components, work and stress bounds, error and refusal cases, and the ledger freeze remain pending.

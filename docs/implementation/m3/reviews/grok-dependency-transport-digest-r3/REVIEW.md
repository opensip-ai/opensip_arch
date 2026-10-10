# DT-MD1 dependency transport manifest digest, round 3

ACCEPT-DESIGN-UNIT. Round 3 keeps the round-2 recipe and replaces the two schema passage selectors with JSON Pointers. The subject manifest `docs/implementation/m3/snapshot-plan-c/dependency-transport-digest-r1-subject.json` is 3028 bytes, SHA-256 `5bba29f5c752ec3a1ca94cb4412a2a1d0b1fa500b60e7d2e05667c6d6624057b`, with the same 13 sorted unique paths. Eleven members are byte-identical to the accepted round-2 subject. The preserved round-2 review remains `reviews/grok-dependency-transport-digest-r2/review.json`, 424 bytes, SHA-256 `5de11108a4431937c50745ab27755c33804b6d13dd9b1bb114f6870923924dcb`. The preserved round-1 review remains `reviews/grok-dependency-transport-digest-r1/review.json`, 424 bytes, SHA-256 `1b9555ec7ebaa1a3310948f8b210618c64dda26094e80f523b7a104a50fc1a14`. Neither review is resubmitted.

Product HEAD is `0f1c8ab37e2c270be312a7184d5c06a9c73e2a8e` and the product tree is clean. Architecture HEAD is `5c0b29cf47c07ce64607d29ca70d7db7130c0c36`. The only architecture porcelain entry is the untracked `docs/implementation/m3/syntax-e/e2s/` path, which is outside this unit. `design-lock.json` is unchanged at 616747 bytes, SHA-256 `a75638692968936fffa33ac8fdcd27d8c188b91e4218db8e35230cea7fdf004f`: inventory v180, 155 contract successors, and 103 inventory passage rows. All 155 contract record hashes match the architecture tree.

## Selector repair

`verify_design.py` refuses a `line` selector when the parent bytes decode as JSON. The two schema parents are JSON, so round 2's line 4150 and line 4229 selectors stop at that check. Round 3 selects the decoded artifact strings:

- `/$defs/DependencySourceManifestV3/properties/manifestSha256/x-opensip-digest/artifact`
- `/$defs/DependencySourceSealV3/properties/manifestSha256/x-opensip-digest/artifact`

`selected_passage` on the live schema returns the `before` value for both pointers: `the exact transport manifest frame bytes as sent (section 9 wire frame, not a Plan input)`. Each `after` value is `the deterministic-CBOR encoding of the exact complete entries array of DependencySourceManifestV3; no transport envelope, manifestSha256 field, dependencySourceSetId, wrapper, prefix or suffix is in this raw SHA-256 preimage`. Those strings are the decoded artifact texts. They carry no JSON indentation, key, quotes, or comma. The proposed schema file, unchanged from round 2, stores that same `after` text, and the definitions still match the pinned schema once that one artifact field is removed.

The `native-evidence.md` override is byte-identical to round 2: line 1704, heading `### 3.2 Custody and transport`, with the same added paragraph. That parent does not decode as JSON, so the line selector remains the form the checker keeps for text. `selected_passage` returns that heading. The parent arrays stay the round-2 sorted unique order, schema file then `native-evidence.md`, and both live hashes match. `pin_rows` accepts the two parents, the twelve candidates, and the thirteen subject files. The candidates cover every subject member except the successor, and each candidate pin equals its subject row.

`passageSupersessions` is empty. Across the 155 bound contract records there are 381 passage-selector keys. None is line 1704 of `native-evidence.md` or either new JSON Pointer. Bound NNS-1 remains the sole successor on line 1711 of that text.

`prospective-passage-overrides.json` is 3290 bytes, SHA-256 `7c4ba4823cff94f03654dd789148afdbaf69a69ec6a3aaa06a6b806c1d8f700c`. `successor.json` is 6122 bytes, SHA-256 `9cb4d9ea9d8263e0048020a1fa30e289f263f1d2f3a289cd7286398dc1c13cc7`. Their passage overrides match. The successor diff from round 2 is those two selectors, the decoded before/after strings, and the candidate pin for the prospective file.

## Unchanged recipe bytes

The recipe, schema copy, vectors, controls, census, and source pins are the eleven identical members. `manifestSha256` remains raw SHA-256 of the deterministic-CBOR encoding of the exact complete entries array, with no envelope, set id, digest member, wrapper, domain, prefix, or suffix in that preimage. Advisory r2 remains the gap record and supplies no acceptance vote or owner decision. `checks.json` and `frozen-check.log` remain 2093 bytes, SHA-256 `0b83e89798e915caf3a54d5e8e03fca2cd0c97043c578ab2f6c356c8ed207592`. This round does not reopen those controls.

## Scope that stays open

The stage-local `design-lock.candidate.json` is 617760 bytes, SHA-256 `caa075a4b8da532ed29a8bbc7c59df9090942d4f5d07b7c9f6a8535b709ca937`. Its first 155 contract successors equal the product lock, and the appended binding names the round-2 record `42f55c05053f1203ea5334d6120973a1fe1c17decbdc3b583886cc0b04b2d96c`, the round-2 subject `9e9e31c5c9b7bf00085730d51f55fcf9056e9c93a23bfca8e289050460466173`, and the round-2 review. The preserved copy in `dependency-transport-digest-r2-retained-failed-integration` carries those same round-2 successor, subject, and prospective bytes. Those files do not bind this round-3 subject.

`contractSuccessorsAfter` 156 is the count after a later bind of this round-3 successor. Inventory stays 180. Product code is unchanged and the recipe is not implemented. `sourceAdmission`, `fullSM`, `productQualification`, and `entirePlanComplete` stay false. The full `verify_design.py` program was not run. The read-only preflight called `pin_rows` and `selected_passage` only. Publication still requires this acceptance, root substantive assent, and the lead design check against the round-3 successor pin. The product lock bind is a separate commit. Nothing is pushed. Acceptance of this selector repair grants no source, profile, transfer, or qualification gate.

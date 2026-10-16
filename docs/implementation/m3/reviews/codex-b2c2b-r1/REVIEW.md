# ACCEPT-UNIT — B2-C2B-r1

Subject manifest: 7,944 bytes, SHA-256 `4260206becd3d5b5f2c15ee53451908ff3563daf7326e1cd20c096f4992d6b87`. All 34 members match their declared bytes and hashes. Product main and candidate HEAD are `00ec6492c673c67399ab740bcb4acfda4a33184d`; main is clean. Architecture HEAD is `6d360470b303feec780249644ac8a836b063317f`. All six product-map parent, candidate and archive pins verify; the map exactly covers the candidate changes, with no new paths. Source authority pins match committed architecture bytes, and the product lock matches its pin and 172 contract successors.

## Implementation and authority

- **r10 bounds:** The Rust reader counts Unicode characters with `path.chars().count()` and refuses paths above 4,096 at the node itself, entry included, before judging bytes or parsing. The existing new-base 32-node check remains in the caller. JSONC and all relevant field/element types are checked before counting `extends`; more than 64 entries, repetitions included, refuses at that file before classifying or resolving any entry. Both new cases use `native.typescript-config-bound`. Existing traversal and other refusal ordering are unchanged.
- **LD-B2C2B-1:** The combined node guard is sound. Its left operand checks the path first; either failing operand produces the same key and node subject, with no intervening observable effect. It preserves the law's required result and order.
- **Independent reading and controls:** The Python reader implements the same rules independently. All 121 inherited cases remain exactly equal; eleven additions cover 64/65 entries, retained repeated edges, malformed-specifier and missing-base precedence, wrong-type precedence, a base with an oversized array, entry/base path boundaries and a non-ASCII 4,096-character base. Oversized entry arrays record only the entry read; the malformed-specifier and missing-base cases resolve no edge.
- **LD-B2C2B-2 and schema:** Runtime guards are sufficient for these bounds; C2 retains record-emission admission. The replay test admits every successful Rust graph through the embedded native graph schema. The new test reads both limits from the embedded schema and compares them to the reader constants. It admits the boundary graphs, then isolates 65 edges and 4,097-character paths as schema refusals; path mutations preserve edge references and node sorting. The non-ASCII case distinguishes characters from bytes. The Python builder additionally validates each successful graph and its graph-law conditions through the pinned native model.
- **S10b:** The product remedy and vectors' `d9.remedy` equal S10b's selected string byte for byte. The builder pins S10b and r10 while retaining S10's registry. Aliases, public record, unit controls and termination subjects are unchanged. The existing row-59 test still compares the projected carrier against the model-derived vectors; the remedy's length and digest expectation are updated consistently.
- **O-1:** Closed within this reader's admitted-input contract. The two missing record bounds are enforced before an unrepresentable graph can be returned. Canonical identities, digest construction, sorted unique nodes, closed edges, reachability, acyclicity and basename-derived kind remain supplied by the accepted reader. This does not claim C2 projection/emission, custody integration or a production caller.

## Validation and remaining inventory work

Independently ran only the two permitted commands in the candidate worktree:

- `python3 -I -B tools/host/typescript_config_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` — passed.
- `python3 -I -B tools/tests/test_discovery_fw01.py` — eight tests passed.

Reviewed the pinned lane evidence without rerunning the lane or compiler. The raw host logs confirm equal eight-test failure sets: 377 base versus 378 candidate passing tests across three suites, with one new passing schema-bound test. The focused configuration/remedy run passes ten tests. Warning-denied all-targets Clippy passes; all four edited Rust files are format-clean at base and candidate. Vector checks, ten environment-exception tests, the 114-row operability census and design verification pass. Design verification explicitly claims no product qualification.

All seven mutation logs show test failures, with no compilation failure: skipped/off-by-one/widened entry limits; skipped/off-by-one/byte-counted path limits; and the old remedy carrier. Their failed tests agree with `controls.json`. The lane script records private mode-0700 temporary storage, lane ownership and nice-10 children. The implementation adds no mint authority, environment access or exception.

The planned inventory-v213 description successor is appropriate for the reader, its tests, vectors and builder: their inherited descriptions refer to r9 or the old S10 model. The two outcome-file descriptions remain true. No additional inventory description was made false by the six-file diff. That successor remains follow-up work after this code acceptance.

No required findings or non-blocking observations. No Cargo, rustc, build, lane, network, delegation or prohibited private-data access occurred during review. Neither repository nor the candidate worktree was edited. Only the requested `REVIEW.md` and `review.json` were written.

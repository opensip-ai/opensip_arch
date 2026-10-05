CODEX2 review: I1-c r1

**ACCEPT-UNIT**, including inventory v140. No required findings and no new non-blocking observations. Grok is the implementation lead.

Reviewed the exact 366,473-byte diff against `083ad5c7bb18a5fce5d7c02a907e278c403d7f40`:

`5f3e7716991a57074ac652c7e34200b18217e2236de8b59f33831a4e93e495e7`

Inventory subject manifest: `238cb70f72af846fd379aa47c06788de71f4e6346c59d5401c77acefbb3bc3ca`. All 54 request pins match before and after validation. The final worktree diff and status are unchanged.

The authority is accepted M3-I1 r3 item 5, its S1-to-S9 unit row and item 7 amendments, bound I1-P, and X12 r3. Both shipped data files match I1-P's candidates byte for byte. The policy document is exactly law 5.2's 574 ASCII canonical bytes with no trailing newline. Independently recomputed policy SHA-256 is `96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1`, atom programDigest is `8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de`, and the 457-byte compiled RuleProgramV2 digest is `e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb`. These equal I1-P's literal pins and the Rust checks.

Production policy.rs changes only its release const/comment. Exactly one row maps to exactly one compile-time document tuple under the row's policyDocument name; no runtime lookup is introduced. The row and standing are I1-P's whole frozen registry file, including its historical r2 law reference, as r3 expressly requires. No evaluator semantics, composition, host resolver API, Plan construction, C4a or J2 path changes. ATOM_OP refusal remains until I1-b2. No S10 execution or release qualification is claimed.

**Judgment call 1: Yes, the tests discharge S1 to S9.** S1 checks registry consistency and one row/document; S2 checks raw/canonical bytes, newline absence and row digest; S3 runs admission steps 6.1 to 6.7 on shipped bytes through admit_from and public admit_pack; S4 checks every rule's canonical emitWhen digest; S5 checks literal I1-P identities and both policy/program digests, including the compiled 457-byte program. S6 pins the exact production tuple, eight include_bytes sites, two RELEASE_PACKS selections, one PackRegistry construction and the unchanged no-runtime/test-row restrictions. S7 admits the exact ID and refuses the 17 release variants; the test ID is checked on the release registry, while the other variants are checked on both registries. Exact supplied bytes and newline variants remain row 2 for both provenances. S8 exercises public check_plan_pack with the matching digest and four wrong digests, plus count and unbundled controls. S9 exercises host admission with both pinned digests and supplied-byte termination, preserving all other route expectations. All four I1-b1 tests remain unchanged and pass in both workspace runs.

**Calls 2 to 5: Accept.** Role registry is appropriate for production embedded policy data, with generated false and standing proposed. The inline document tuple plus source pin fixes its name/file association. The expanded NT-1 variants strengthen byte-exact identity evidence. Item 7 amends X12 when this unit lands; the accepted X12 snapshot needs no edit. S10 remains I1-b2's.

**Stop item 1: Agree.** every_row's input changes from the newly admitted pack:1 to pack:2; class, exit, codes, detail, remedy and rendering expectations remain unchanged, and row 1 still passes through real admission. The pinned Lead flip evidence identifies exactly the three law-assigned evaluator failures and three host failures caused by the old pack:1 input. I inspected that evidence; I did not rerun the optional scratch flip check.

**Stop item 2: Agree.** The three stale descriptions stay inherited by value under the explicit Lead ruling and inventory-successor rules. Carry the README's replacement texts to the next description-only successor; v140 does not bind those replacements. I1A-NB-1 stays open for the next atom-registry maintenance unit or a record-maintenance follow-up. This diff does not edit atom-registry.json, its accepted bytes are unchanged, and the locator has no consumer.

Inventory v140 is accepted at **584,066 bytes**, SHA-256 `9eebf35bd89cb76a631f416200d7f2ca654a8d6e6e5cfc8cf2ab81fcc30961de`. Parent v139 is **583,181 bytes**, SHA-256 `f3bf66a6584e4fd41cef228aee9062c97ff670228c5f919c27ccd4762ad3061c`. Successor record is **307,873 bytes**, SHA-256 `146e42e424a912540d1802cd768e17be348c52609c640e658eeb3d5d70e64e3a`. It adds exactly the preview document row in opensip-evaluator; the description matches its bytes and placement. All 1011 parent rows, packages, edges, pending decisions and unresolved obligations are unchanged. All 894 tracked or intent-to-add worktree files are covered. All 103 effective description meanings are projected by stable path with 100 moved selectors, no direct parent overrides or folded supersessions, and no meaning on a touched path. The 12 subject members and verifier anchor match their pins.

The staged lock is exactly HEAD plus J3a's staged entry, then I1-c's, with the 103 re-parented meanings. J3a's entry equals its own staged lock. Scratch verification passes all real checks with only missing reviews/assents served in memory; plain staged verification correctly refuses at SCRATCH-J3A/review.json. That is not actual approval of J3a. J3a must integrate first with unchanged v139 bytes/meanings; the Lead then rebases/restages, replaces I1-c's two placeholder pins with actual review/assent, and runs plain verify_design. Rebuild and re-pin if the parent changes or another inventory integrates first. The main integration parent was independently rechecked before publication.

I independently ran all required checks, including two workspace runs:

| Check | Result |
|---|---|
| Staged scratch verification | PASS |
| Plain verification of staged lock | Expected refusal: SCRATCH-J3A/review.json (exit 1) |
| Plain verification of HEAD lock | PASS |
| Projection verifier | 103 rows; 518 corruptions refused |
| Workspace format | PASS |
| Explicit rustfmt of both test modules | PASS |
| Workspace all-targets build | PASS |
| Workspace clippy | PASS |
| Crash-feature clippy | PASS |
| Scenario-fixtures clippy | PASS |
| Workspace tests, run 1 | 1795 passed, 0 failed, 3 ignored |
| Workspace tests, run 2 | 1795 passed, 0 failed, 3 ignored |
| Doc tests | 20 passed, 0 failed, 0 ignored |
| Normal crash-feature tests | 1686 passed, 0 failed, 3 ignored |
| Admitted scratch drift gate | 40 sources, 8 outputs, changed: [] |
| Host package edges against v140 | PASS |
| Rust-provider edges against v140 | PASS |
| Package-edge suite | 14 tests, OK |
| Dependency policy | PASS |
| Identity dependency policy | PASS |
| Dependency-policy suite | 9 tests, OK |
| Identity-dependency suite | 5 tests, OK |

All 24 validation commands passed their expected outcomes; the plain staged refusal is expected. Cargo uses the review-local target/cache, locked/offline product resolution, private 0700 Darwin TMPDIR and synthetic HOME. The requested suites' changed disposable manifests resolve offline, never against the product worktree. Each cargo or cargo-invoking lane waited for its own successful mkdir and released only its owned lock immediately afterward. The actual waiting argv names only the script and contains no cargo text. The generator process-name check was clear before drift. No crash-matrix lead run set was run. Validation is macOS arm64 development evidence.

No repository edits, commits, pushes or delegation. No real OpenSIP-home or private 413 fixture access. Only REVIEW.md and review.json remain as delivered files; owned validation scratch and private TMPDIR were removed after completion.

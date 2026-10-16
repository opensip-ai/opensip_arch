# B2-C2-r2 review

Verdict: **ACCEPT-UNIT**.

Subject manifest: `docs/implementation/m3/config-discovery-b/b2-c2-r2-subject.json`, 12,005 bytes, SHA-256 `3dd12947a49494f7cb58b67ca4b167949cd9154c34d696675f738fe27107cebf`.

All 52 manifest members match their sizes and hashes. All source.json authority pins, the prior-review pin and the product-lock pin match. All ten product-map rows match their parent bytes or new-file absence, archived bytes and candidate bytes. The candidate's tracked and untracked change set is exactly those ten paths. Architecture HEAD is `a06251386a4c6b6b68052f97a4326122343eec7b`; product main and the candidate base are `1f70dba4d18d9db7b11253b9202846d2ca2bc50e`. Product main is clean, with 167 contract successors and inventory v201.

## Prior findings

- **B2C2-R1-RF-1 resolved.** Accepted M3-B r9 supplies the previously missing grammar authority. The tool pins its exact accepted bytes, the code cites it, and SCOPE no longer presents empty-document acceptance as an implementation-only extension. Empty/comment-only entry and base configurations now lawfully read as empty objects. The unchanged Rust reader distinguishes this absence of a value from a parsed Null node and requires object roots and object compilerOptions.
- **B2C2-R1-RF-2 resolved.** The Python EMPTY sentinel is distinct from None, so a JSON null reaches the object check and refuses as malformed. New handwritten expectations cover null roots, comments around null, a jsconfig root and a null base. Independent permitted probes also rejected a commented null base and null compilerOptions, while admitting empty/comment-only inputs. The Rust and reference mutations that restore null-as-empty are caught by their respective gates.
- **B2C2-R1-RF-3 resolved.** Both implementations compute inherited optional booleans once per canonical node in postorder. A completed base's stored pair is reused; no recursive inheritance expansion remains. Missing options remain distinct from false until the entry defaults are applied. Each retained edge is merged in declaration order, preserving repetitions and later-base precedence. Work counters sit at the node computation and edge merge sites. Rust replay checks them against both graph cardinalities and the reference's counts. The 32-node/64-repeated-edge case requires 32 node evaluations and 1,984 merges; the shared-base case requires four evaluations and 192 merges. The added counter mutation establishes that the work assertions are active. Together with source inspection and the large repeated-edge regressions, this is sufficient evidence for the fix; no timing threshold is needed.

## Fidelity and scope

The full r1-to-r2 source diff is confined to the declared fixes: r9 authority and scope records, the EMPTY sentinel, postorder option calculation and Work, eight added vectors, work assertions, and refreshed check/mutation evidence. JSONC parsing, invocation.rs, lib.rs, outcomes.rs, outcomes_tests.rs and FW-01 are byte-for-byte unchanged from r1. Every original vector case has the same result/refusal, graph and read sequence after removing the new work field. The seven units cases, aliases, public record, D9 row, remedies and bounded-subject expectations are unchanged.

Item 14a's grammar, byte/node bounds, closed specifier classification order, containment before source access, path/package candidate order, canonical identity, cycle checks and pre-C1 link refusals remain sound. The postorder refactor preserves NE:527-545's option precedence and exact jsconfig basename default, including inherited false and checkJs-derived allowJs. New vectors bring the table to 121 cases, 71 refusals. The permitted vector check validates successful graphs through the S10 model and reproduces all seven units cases through B2-c0.

LD-B2C2-2(a) and (h) now implement r9 rather than extending the law. The remaining LD-2 choices, immediate link refusal, per-candidate normalization, skipped root-directory candidate, literal package lists, deterministic traversal/subjects and inventory-entry fault handling remain sound. The two-pass U-1 composition still reads only surviving configuration markers and reads nothing after refused discovery. Duplicate keys retain the last value without adding a disclosure field.

Row 59 and its four-entry alias table continue to match J1 r7 and S10: request-rejected/2, CONFIG.INVALID without fault cause, native.typescript-config-unresolved, its own detail-keyed remedy, bounded internal-key/path subject, and no runId/executionId or operational key. The invocation match correctly has no commit evidence. Explicitly omitting row 58 from matrix coverage discloses its existing lack of an Observation; existing row coverage is preserved.

The reader remains pure through ConfigSource. The Rust JSONC arena parser uses explicit frames and index-owned containers, so parsing and dropping deeply nested values do not recurse through children. The graph traversal is limited to 32 canonical nodes. The unchanged FW-01 lexical purity checks and planted negatives pass; inspection of the current modules supports their result.

**O-1 may remain routed to the lead for C2.** This unit emits no graph record or C2 projection and does not invent an edge-bound refusal contrary to item 14a. A graph with more than 64 retained edges at a node still cannot be claimed as an admitted TypeScriptConfigGraphV1. The appropriate law/contract decision must precede C2 record emission. This scoped acceptance does not resolve that mismatch, production custody, snapshot read-set integration, inventory v202 or the remaining B2-c work.

## Verification

Reviewer reruns, all passing:

- Operability source census: 114 rows, no findings.
- The expressly permitted FW-01 script: eight passing tests, including planted negatives on copies.
- The expressly permitted Python 3.14 TypeScript vector --check, with the requested architecture and packages roots: exact checked-in bytes verified.

Read-only imports additionally exercised empty and comment-only roots/bases, null roots/bases with comments, other non-object roots, unterminated comments, normalization and package candidates, later missing versus explicit-false options, and jsconfig inheritance. Independent repeated-edge chains of 8, 16 and 32 nodes returned respectively 8/448, 16/960 and 32/1,984 node-evaluation/edge-merge counts. Rust agreement for these additional inputs was assessed from source; Rust was not executed by this reviewer.

Recorded evidence was inspected rather than rerun. The host logs independently reconcile to 349 base passes and 357 candidate passes, with the same eight pre-existing failures across three suites. Focused TypeScript/outcome logs report 10 and 18 passes. All seven Rust formatting classifications are clean, warning-denied all-targets host Clippy completed, discovery-unit vectors verified, and the parsed verify_design record reports passed=true. All 23 mutation logs fail without compilation errors: 20 host assertion failures and three vector-generation failures. The new null and work-counter controls exercise their stated defects. The empty-document-refused mutation now protects accepted r9 behavior.

No required findings or non-blocking observations.

No Cargo, rustc, builds, lane, unpermitted tests or network were run. Neither repository, the worktree nor control files were edited. No installation, private fixture, signing key, held tree or T2 held-out entry was accessed. No delegation or other panes were used. Only REVIEW.md and review.json were written in the requested directory. This is acceptance of the pinned unit, not integration or product qualification.

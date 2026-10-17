# Review request: D2A-r1 (the common control codec, `crates/components/src/control_protocol.rs`; M3-D r5 item 9), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2a-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; running the CC v5 reference `docs/coop/completion/control-completion.check.v5.py` with `python3 -I -B` against the architecture's own corpus, if you want to compare it with the Rust codec's behaviour; and, in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2a-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 20765 bytes, SHA-256 `24e0b1e9963c2259be9ed18f493d01aa5d55103ee2130796577ff0fe2b8ee610`, 90 members. Rehash every member.
- **The candidate base and lane base:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (inventory v214; 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2a`, detached at `56d0eb5`, holding the exact bytes `product-map.json` lists (7 files).
- **Main may move while you review,** by C1a2's integration if it is accepted first (host, security and platform files only, and then its lock-only inventory commit). Nothing there touches `opensip-components`.

## Authority

- the D2a plan r1 (`docs/implementation/m3/supervisor-d/d2a/PLAN-r1.md`; your `codex-d2a-plan-r1`, ACCEPT, with NBO-1 and NBO-2 carried in the lead assent);
- law M3-D r5 item 9 and D2a-T1 to T4;
- CC v5 (`docs/coop/completion/`: the corpus, the RF5 proof and `control-completion.check.v5.py`);
- the product schema `schemas/sources/control-v3.schema.json` and the generated `Control3Root`.

## What to review

`SCOPE.md` states the change table, the tests, the three lane attempts and the checks. Judge:
1. **The reader (LD-D2A-2).** No recursion anywhere (parse, drop, debug, equality); strict UTF-8 first; strict whitespace, escapes and structure; duplicates compared on the decoded key at every depth; unpaired-surrogate strings kept as UTF-16 units; the reference's number lexeme rule.
2. **The schema interpreter (LD-D2A-3).** Draft 2020-12 semantics for exactly the schema's keywords, closed loading, the two patterns as exact matchers, the identity substitution and sentinel, and `x-maxUtf8Bytes` in the UTF-8 walk.
3. **Precedence (LD-D2A-4).** Does `classify` follow `check.v5.py`'s order exactly, from the prefix through the deferred seq fault to the state, direction, identity, tuple, nonce and effect checks?
4. **The production context and session (LD-D2A-1, LD-D2A-5).** `ControlContext::for_session` as the only production constructor (the 65,536 bound and offer, the one admitted tuple), and `ControlSession`'s sequences and stopping.
5. **The encoder (LD-D2A-8, NBO-1).** Host messages only, built from an admitted selection, fallible on a multi-offer hello and an over-bound frame; no serde reads wire bytes.
6. **The replay (D2a-T1 to T4).** All 480 corpus cases byte for byte, with the corpus and proof pinned; the full 16 × 8 × 2 matrix; the prefix refusals; the deep-nesting and long-integer probes on a 64 KiB stack. Also the new test `a_duplicate_member_in_a_body_is_rf2_on_the_decoded_key` (`check.v5.py`:75), added after attempt 1.
7. **The lane** `evidence/d2a-checks-r1/` (attempt 3, the lane of record), with attempts 1 and 2 in `evidence/d2a-checks-r1-attempt1/` and `-attempt2/`. Is SCOPE's account of them (two surviving or malformed mutations, then the suite-count comparison) accurate, and are the runner's corrections sound? Note that the runner's summary line for the components comparison is printed under the label `host`; the comparison itself is `test-comparison.json`.
   - components: base no tests, candidate 9 new passing, equal failure sets, exactly one new suite;
   - Clippy and rustfmt;
   - CC v5's two source pins;
   - the package edges under the O1-a package policy (`opensip-contracts`, and `opensip-identity` as a dev edge);
   - the environment exceptions, operability, the closure-unchanged check and verify_design;
   - ten mutations.
8. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; no `let _ =` in product files; no census-closure file changed.
9. **Inventory:** `control_protocol.rs` realizes its planned row; three new paths (the test file and the two data files).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2A-R1-RF-n` / `D2A-R1-NBO-n`.

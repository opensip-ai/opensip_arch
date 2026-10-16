# Review request: B2-C2-r2 (the JSONC reader and effective allowJs; M3-B unit B2-c, sub-unit B2-c2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c2-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>` and `python3 -I -B tools/tests/test_discovery_fw01.py`;
  - `python3 -I -B tools/host/typescript_config_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` (in the candidate worktree, with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`);
  - importing the tool's `Reference` functions (`effective`, `parse_jsonc`, `candidates`) read-only in a scratch script under this directory, to try your own inputs.

## Subject

- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-c2-r2-subject.json` in the architecture checkout `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 12005 bytes, SHA-256 `3dd12947a49494f7cb58b67ca4b167949cd9154c34d696675f738fe27107cebf`, 52 members. Rehash every member.
- **Bases.** Product `1f70dba4d18d9db7b11253b9202846d2ca2bc50e`, clean (167 contract successors, inventory v201). Architecture `a06251386a4c6b6b68052f97a4326122343eec7b` (M3-B r9 published).
- **The candidate worktree** `/Users/sb/code/opensip-ai/opensip-b2c2` (detached at the product base) holds the exact bytes `product-map.json` lists; `git -C <worktree> diff` and its untracked files are the change.

## Authority

- **Law M3-B r8 item 14a** (`config-discovery-b/PROPOSAL-r8.md:567-680`; Codex `codex-m3b-r8-r3`), as **M3-B r9** amends its reading grammar (`PROPOSAL-r9.md`; Codex `codex-m3b-r9-r1`).
- **Successor S10** (`s10-tsc-unit.json`, `s10-tsc/`; Codex `codex-s10-tsc-r1`; contract successor 167), and its LD-4, which leaves the row's observation and the alias table to this unit.
- **M3-J1 r7 item 10 row 59** (`host-pipeline-j/PROPOSAL-r7.md`; your `codex-host-pipeline-j-r7`).
- **The B2-c plan r2 §2.2** (Codex `codex-b2c-plan-r2`).
- **NE:527-545 and NE:1330-1345** (`docs/v2/contracts/product-v1/native-evidence.md`).
- `source.json` pins them.

## Round 2

Your `codex-b2c2-r1` (`/tmp/opensip-implementation/reviews/codex-b2c2-r1/review.json`) raised B2C2-R1-RF-1 to RF-3. `SCOPE.md`'s "r2 changes" section resolves them:
- **RF-1:** law M3-B r9, which you accepted in `codex-m3b-r9-r1` (published arch `a06251386`), now admits the empty document and states the object requirements. The tool pins it, and the code cites it.
- **RF-2:** the reference's `EMPTY` sentinel, and `null` vectors.
- **RF-3:** postorder evaluation with `Work` counts in both implementations, asserted linear for every case, with repeated-edge and shared-base regressions.

The r1 package (`b2-c2-r1/`) is kept as round 1's record. The r2 package is `b2-c2-r2/`, with lane `evidence/checks-r2/`.

**Judge first:** is each finding resolved? Also: are the new vectors and the three new mutations (`null-root-as-empty`, `edge-merge-uncounted`, `reference-null-as-empty`) sufficient? Did the r2 changes break anything round 1 accepted?

## What to review

`SCOPE.md` describes the unit and its lead decisions LD-B2C2-1 to LD-B2C2-9. Judge:

1. **Fidelity to item 14a.** Do `jsonc.rs` and `typescript_config.rs` implement exactly what item 14a states:
   - the grammar;
   - both bounds;
   - the closed specifier grammar, in its order;
   - lexical normalization and containment before any file is consulted;
   - both candidate orders, nearest `node_modules` first;
   - node identity, with cycle and node checks as the graph is built;
   - custody before C1;
   - NE:527-545's derivation, including the `jsconfig` basename law;
   - the four keys?

   Construct inputs where the Rust, the tool's Python reading and the law might disagree, and check them.
2. **The lead decisions where the law is silent.** Is each sound and within item 14a?
   - **LD-B2C2-2(a) and (h)**, now M3-B r9's law: does the code implement r9 exactly?
   - LD-B2C2-2(b)-(h).
   - LD-B2C2-3: a link refuses even when a later candidate exists; per-candidate containment; the root candidate; the literal lists.
   - LD-B2C2-4, the walk order and subjects.
   - LD-B2C2-5, the entry.
   - LD-B2C2-6, the two-pass composition with U-1.
   - LD-B2C2-9, duplicate keys not recorded.
3. **Row 59 and the alias table.** Does the `Observation` projection match J1 r7 row 59 and S10's D9 row, remedy and bounded subject? Is the alias map exactly S10's four registry rows? Are the `invocation.rs` match and the `outcomes_tests.rs` coverage change (row 58 disclosed as having no observation) correct?
4. **The oracle and vectors (LD-B2C2-8).** Are the 121 hand-written expectations the law's? Does the tool's Python reading agree with the law and differ from the Rust only in language? Are graphs admitted by the S10 model copy, and are the seven units cases reproduced through the B2-c0 reference? Is anything item 14a's controls name missing ("Controls (B2-c2)")?
5. **Purity and FW-01.** Do the new modules read only through `ConfigSource`? Is the extended FW-01 test, with its purity check and planted negatives, sound? Is the arena parser non-recursive in both parsing and drop?
6. **Evidence.** `evidence/checks-r2/`: the host suite at base and candidate (8 equal pre-existing failures, 8 new passing tests), rustfmt, Clippy, the vectors checks, FW-01, the outcome tests, the operability census, verify_design and 23 caught mutations. Are the mutations meaningful?
7. **Open item O-1** (the 64-entry `extendsResolved` bound). Is recording and routing it correct, or must this unit resolve it?
8. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2C2-R2-RF-n` and `B2C2-R2-NBO-n`.

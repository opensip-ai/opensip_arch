**ACCEPT-UNIT** for M3-P0 r1. No required findings. **Inventory candidate v135: ACCEPT**, with no required findings.

Reviewed independently by Codex on 2026-10-04, without delegation, against detached product base `cd5958b3608f44a0035566c9d4500e5005c62e91` in `/Users/sb/code/opensip-ai/opensip-p0`. All 38 request pins, including the eleven subject-manifest members, matched before and after validation. The final diff is byte-for-byte identical to [subject.diff](subject.diff).

The reviewed diff is 284261 bytes, SHA-256 `637ab18a2971942fa4e8bda9bbf022a9c41ebfe3c9def5a0e592ed19fdc28f6b`. The subject manifest is 2317 bytes, SHA-256 `844d0e18c927c1f8f0863d33e61e9a0fdba1b282112608d55f2c3e003096ad2b`. The staged lock is 496918 bytes, SHA-256 `ede33788b2e1c7e9dc86c0ad6996dcf7b88ee4fe8f415134bbaf6f6243a07b35`.

P0 fulfills the accepted M3-PLAN-r6 row at :208: it adds the components and syntax workspace members, supplies dependency-free package scaffolds, retains the existing provider roots, selects the inflater dependencies, and supplies one additive inventory successor. The diff contains exactly the eight declared files. Structural comparison of Cargo.lock preserves every previous package record and adds only `opensip-components` and `opensip-syntax` 0.1.0 without dependencies. Neither inflater crate is linked. Both new lib.rs files contain documentation only. No later unit's implementation or authority is introduced.

The seven judgment calls are acceptable:

1. **The host selection policy is the right instrument; miniz_oxide 0.9.1 without features is an acceptable selection.** C r7 item 12 assigns the inflater row to P0, while C3a owns its host consumer and first-party archive decoder. A distinct host-workspace policy avoids changing the contracts or identity closure policies and leaves E2b's SYN-DEP owner intact. Its standing text and row fields distinguish selection from linking, closure enforcement and qualification. Consumer, linking unit, exact declaration, checksum, feature set and transitive row are explicit. The raw DEFLATE core permits caller-owned input/output buffers; C3a retains gzip framing, member/header checks, CRC-32, ISIZE and the D1–D4 byte/record bounds.

   I independently fetched both official archives and sparse-index records. Archive sizes and hashes equal the policy and index checksums; each selected version is non-yanked and is the latest stable release in the fetched index. The normalized manifests say `build = false`, contain no `links` key, and select an allowed MIT or Apache-2.0 licence option. Both archives contain those licence texts and no C/assembly source or build.rs. Their lib.rs files forbid unsafe code at the stated lines. Disabling miniz_oxide defaults leaves its non-optional adler2 dependency with defaults disabled, no active optional dependencies and no features on either crate. The source gates exclude deflate and allocating helpers while retaining inflate::core and inflate::stream. See [archive-assessment.json](archive-assessment.json), the [miniz_oxide index](https://index.crates.io/mi/ni/miniz_oxide), and the [adler2 index](https://index.crates.io/ad/le/adler2).

2. **An unchecked selection file is acceptable at P0.** No manifest or resolved graph consumes these rows, so there is no new runtime dependency closure to enforce. This acceptance covers the exact reviewed selection bytes. The policy explicitly makes the linking unit add a closure check and requires review for a different version, feature set or consumer. C3a must implement that check when it links the rows; the present checkers validate their existing contracts and identity closures. A separate P0 checker for absence from the graph would add little to the exact source/lock review.

3. **The provider layout needs no P0 edit.** The Rust provider already has its independent workspace, lock and toolchain and stays excluded from the host workspace. The TypeScript provider already has its package, lock, source include and generated protocol roots. CH14's planned file list does not require placeholder modules (:305). F/G own the modules, and G2's sidecar layout waits for S-P. The independent rust-provider edge lane confirms its separate workspace.

4. **No dependency edges or modules is the correct scaffold scope.** The inventory already permits syntax → contracts/identity and components → contracts/identity/platform. The empty dependency tables declare none. The doc comments correctly assign syntax's grammar/parser to E2b, normalization/candidates to E2c, and the components modules to D2a/D2b/D3a/D3b/D4. Host dispatch, admission and dependency edges arrive with their implementing units. The inventory description of syntax/lib.rs remains a planning ownership constraint; its current documentation explicitly says that no public item exists, and it exposes no unchecked Coverage or authoritative constructor.

5. **Keep syntax's `unsafe_code = "forbid"` lint.** E0's accepted T-native result does not require crate-local unsafe FFI. E1 r3 :74 places native tree-sitter C and its FFI in tree-sitter and grammar dependencies, whose safe Rust interfaces can be used from this crate. The probe's crate-local extern/LanguageFn construction is evidence of its harness shape, not a mandate for the product scaffold. If E2b chooses that shape, a reviewed lint change and SYN-DEP unsafe accounting are appropriate then. This lint constrains first-party syntax Rust; it does not establish safety of native dependency code. Leaving components without this table defers its implementation constraints to D's owners.

6. **The deferred rows match their owners.** O1 introduces tracing; D r3 rejects a general CBOR crate; B2-d chooses the YAML reader under this policy; E2b owns grammar/wasmi selection through SYN-DEP. C3a retains first-party CRC-32 unless a later reviewed change selects a crate. None is a missing P0 linkage or policy selection.

7. **The inventory placement and cd5958b base are sound.** v135 belongs beside the existing linear inventory chain under m2, even though this is an M3 unit. The base lock selects v134; I1-P adds no passage on that parent. The staged lock is the canonical base lock plus precisely the new inventory binding and projected inheritance. Keeping design-lock.json outside the seven-file sourceBoundary is appropriate because integration replaces its two placeholder pins. The reviewed diff still pins the staged bytes.

Inventory acceptance is for these exact artifacts:

| Artifact | Architecture path | Bytes | SHA-256 |
|---|---|---:|---|
| Candidate | docs/implementation/m2/repository-file-inventory.v135.json | 553173 | `ac66ee3bd75ace8f21e3122daacfdb2619fe8bb8a432b083414c14cbe3a0c887` |
| Parent | docs/implementation/m2/repository-file-inventory.v134.json | 552176 | `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a` |
| Successor record | docs/implementation/m2/m3-p0-scaffolds-inventory-v135/successor.json | 304648 | `326cf1a253ab65ba0265305804a5ea43bc0185d8074855b09498c6edd2d25e00` |

The candidate has 969 sorted, unique file rows. All 968 parent rows are equal by value; the sole addition is tools/host/dependency-policy.json, a proposed, non-generated tooling registry. Packages, permitted edges and pending decisions are unchanged. The planned rows realized by the scaffolds retain truthful ownership descriptions without claiming implemented parsing or supervision. The successor preserves the unresolved inherited obligations.

The record's 100 passage rows are the 55 inherited rows plus D3's 45 direct-parent overrides, with its 17 supersessions folded into the current meanings. verify_design's own projection agrees. Contract successors remain 82 and recorded supersessions remain 21; only the new sorted row causes the stated one-selector shift. The positive projection and all 503 corruption refusals passed.

I reran the requested checks serially. Native Cargo build, clippy, test and metadata commands used the pinned toolchain with `--locked --offline`; fmt ran with Cargo offline mode. Python checks ran with `nice -n 19`, `-I -B`. Exact commands are in [run-native-lanes.sh](run-native-lanes.sh) and [run-python-lanes.sh](run-python-lanes.sh); logs and exit codes are under [logs/](logs/).

| Independent check | Result |
|---|---|
| fmt; fresh-target workspace all-targets build | Both passed |
| Workspace, crash-matrix feature and scenario-fixtures feature Clippy, -D warnings | All passed |
| Workspace all-targets tests, run 1 | 1731 passed, 0 failed, 3 ignored; 20 binaries |
| Workspace all-targets tests, run 2 | 1731 passed, 0 failed, 3 ignored; 20 binaries |
| Workspace doc tests | 18 passed, 0 failed |
| Requested crash-matrix feature all-targets tests | 1629 passed, 0 failed, 3 ignored; includes host commit-matrix 5 and storage commit tests 8 |
| Host package edges against v135 and v134 | Both passed; 12 members, 22 declared and 20 resolved internal edges |
| Rust-provider package edges against v135 | Passed; one workspace member, two permitted internal edges |
| Package-edge suite | 14 passed |
| Contracts dependency checker, security-crypto-workspace profile | Passed; 11 dependencies, 8 local sources |
| Identity dependency checker | Passed; 8 dependencies, 305 sources |
| Contracts and identity dependency suites | 9 and 5 passed |
| verify_scratch.py, staged mode | Passed; inventory successors 94 → 95, inheritance 55 → 100, v135 selected |
| Plain verify_design on staged lock | Expected exit 1: missing or escaping regular file: SCRATCH-P0/review.json |
| verify_projection.py against the saved cd5958b lock | Passed; 100 rows, 503 corruptions refused |
| Scratch rerun of build_v135.py | Candidate and successor record reproduced byte for byte |
| Final pin and diff checks | All 38 matched; diff unchanged; worktree still has exactly the eight declared changes |

For the inventory rebuild, I copied the unchanged builder and its required architecture inputs under [scratch-arch/](scratch-arch/), using the product worktree's saved cd5958b lock. The builder's one Git tracked-path guard was supplied the known empty result for that non-repository scratch tree through a narrow subprocess stub. This avoided invoking Git outside the named product worktree; the builder's generation and projection logic were unchanged. The harness asserts the exact guarded command, unchanged script bytes, scratch-only outputs and equality with both pinned artifacts. See [rebuild-v135-in-scratch.py](rebuild-v135-in-scratch.py) and [logs/build-v135.log](logs/build-v135.log).

All persistent review output is under the requested directory. The fresh native target, copied Cargo registry/cache and synthetic HOME are isolated there. Transient fixtures used the required private 0700 Darwin TMPDIR recorded in [native-tmpdir.txt](native-tmpdir.txt). I made no repository edit or commit, accessed no real OpenSIP home or private 413 UUID fixture, and ran no crash-matrix lead run set, binary or checker. The feature-pin tests covering the new manifests passed.

The staged refusal remains intentional until the lead copies this review, completes substantive assent and replaces exactly the review/unit-record placeholder pins, then runs plain verify_design at integration. This review accepts P0 and its inventory candidate; it does not supply root assent, discharge inherited decisions, complete M2, or qualify the product. Machine-readable acceptance is in [review.json](review.json), with measured lane totals in [validation-summary.json](validation-summary.json).

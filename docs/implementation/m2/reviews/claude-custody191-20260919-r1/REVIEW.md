# Independent review — frozen `custody-chain-checkpoint-191`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only. macOS host (the Linux standing is read, not executed).
Scope: exactly the frozen 191 product bytes — `RetainedDirectoryPath::observe_directories` and the private `inspect_directory_path` predicate join. No custody grant, host admission, exclusion, 124 F-1 closure or cumulative approval; 192 is separate.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `e33913d59c61f53290dad893eabab488bba7d774a0e8b24016944baa7d9c41f8`, 4,241,896 B = request = `archive-pin.json` |
| Members | 424, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 352/352; none unpinned |
| Parent | equals **my own verified 189 extraction**; 350 unchanged; changed: `bc34b7db4235844c…` platform/src/filesystem/path_binding.rs;`aea56ae68f193ca0…` security/src/custody.rs; fixtures unchanged; no dependency change (`Cargo.lock`/manifests among the unchanged pins); `#![forbid(unsafe_code)]` still heads the security crate |
| Host receipt 120 | 232 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **43 platform + 145 security tests pass; strict workspace Clippy exit 0**.

## 3. What the change is, as read

Platform: `observe_directories` maps the existing `observe_descriptor` over `once(root).chain(edges)` and `collect()`s into `Result<Vec<_>, _>` — so the first failing component aborts and no partial vector exists; no descriptor or callback leaves the type. Security: `inspect_directory_path` = name recheck → observe all → name recheck → for each component the **existing** `check_descriptor_observation(…, Scope::Directory, uid, groups, waive_owner=false)`, returning the first refusing index. Four distinct error classes. It is private and has **no production caller** (module is under `#[allow(dead_code)]`): this checkpoint adds a capability, not an admission.

## 4. My probe on real directory chains (`claude-out/probes/custody_probe.rs.txt` → `io/custody.txt`)

| # | Chain | Result |
|---|---|---|
| 1 | owner fixture: `/`(0:755) › `/private` › `/private/var` › `…/folders` › `…/zg` › user dir (501:755) › `T` (501:700) › fixture › leaf | **Ok, 9 components**, root first, leaf last, modes as on disk |
| 1 | same chain, **wrong invoking uid** | `Predicate component=5 FOREIGN_OWNER` — the first non-root-owned ancestor |
| 2 | private 0700 leaf under **`/private/tmp` (1777)** | `Predicate component=2 WRITABLE_BY_OTHERS` — no sticky exception, as stated |
| 3 | my real `HOME` (`/` › `/Users` › `/Users/sb` 501:750) | Ok, 3 components |
| 4 | ACL on a **middle ancestor**, leaf private: `everyone allow` each of `write`; `add_file,add_subdirectory`; `delete_child`; `writesecurity`; `chown`; `writeattr,writeextattr`; `delete` | all `Predicate component=7 WRITABLE_BY_ACL` — including the rights that let someone replace the child or rewrite the ACL without "write" |
| 4 | `everyone deny delete` (the standard macOS home-folder ACL); `everyone allow read`; `user:root allow write` | Ok (deny and read are not write grants; root is an admitted principal per S3) |
| 5 | ancestor 0770: unauthorized gid → `WRITABLE_BY_GROUP` at that component; same gid authorized → Ok | as the predicate defines |
| 7 | leaf replaced after the observation | `NameChanged` |
| 6 | **documented limit, demonstrated**: ancestor chmod 0777 *between* observation and post-recheck | returns **Ok** with the stale 0700 sample; the directory is 0777 at return; a second inspection refuses |
| 7 | **documented limit, demonstrated**: leaf moved away **and back** inside the window (ABA) | returns **Ok** |

Rows 6–7 are exactly the limits the README and the doc comment state ("do not exclude ABA, concurrent permission changes… or writes after return"). They are reproduced here so the size of the claim is on record, not as findings. (An eighth ACL case, a grant to the invoker by numeric uid, did not apply — `chmod +a` rejected my syntax — and is not counted.)

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`)

Baseline green across both crates; none failed to compile. **7 of 10 killed by the owner's tests**: observation skips the leaf; order reversed; failed component dropped and a partial vector returned as success; a middle ancestor skipped; policy applied to the leaf only; refusing index off by one; post-observation name recheck ignored.
**3 survive:**

| Mutant | My probe | Assessment |
|---|---|---|
| **owner check waived for ancestors** (`waive_owner = true`) | detected (row 1 wrong-uid → Ok) | real gap: "no owner waiver" is the checkpoint's headline policy sentence and no owner test has a foreign-owned (or wrong-uid) ancestor |
| **authorized groups ignored for ancestors** | detected (row 5 authorized → refused) | real gap: no owner test passes a non-empty group set through the chain |
| **policy skips the root (index 0)** | **not detected by either suite** | see T-2 |

## 6. Findings

No defect found in the observation or the join.

### W-1 (low-medium) — nothing in the bytes says this is *not* the S3 discovery walk, and one comment invites that reading
(The owner asked me to look at this specifically.) `inspect_directory_path` lives in `custody.rs` beside the S3 predicate, reuses `Scope::Directory`, and its only in-code rationale is "No ownership waiver for a retained **configuration**/store ancestor". Neither the file nor the README mentions S3, discovery or the walk. The two laws are materially different, and substituting this function for the walk would change behaviour in three ways (S3, `security-and-lifecycle.md` "Walk rule" / "Custody of a directory"):
1. S3: a custody failure at an **ancestor** is a *boundary* — "that ancestor is never examined for a config" — and selection falls back; only a failure at the launch directory refuses. Here **any** ancestor failure, all the way to `/`, refuses the whole path (row 2: everything under `/tmp`).
2. S3 has `--trust-project-owner` (owner waiver, only with an explicit `--project`) and `--trust-group`; here the waiver is hard-coded `false`.
3. S3 stops at VCS/home/mount boundaries and never looks above them; this chain always runs to the filesystem root.
Those differences are *right* for a retained operational/store path, where a writable ancestor really does allow substitution. The risk is a future caller reaching for the nearest "check this directory chain" function. Remedy: say in the doc comment and README what it is for (retained operational/store paths after they have been selected) and what it is not (not S3 project discovery, not a replacement for the walk or its explicit-project waiver rules); drop "configuration" from the l.427 comment or qualify it; consider a name that carries the scope (e.g. `inspect_retained_store_chain`).

### T-1 (test strength) — two policy inputs are forwarded to ancestors without a test
The two surviving mutants above. Add: the chain with a wrong invoking uid (expect `FOREIGN_OWNER` at the first non-root component) and a group-writable ancestor with its gid authorized (expect Ok) and unauthorized (expect refusal at that index).

### T-2 (test strength, structural) — policy on component 0 cannot be tested as the code is shaped
Every real chain starts at `/`, which an unprivileged test can never make violate policy, so "policy skips the root" survives both suites and would survive any filesystem-based test. The loop is inside the function that performs the I/O. Factoring the per-component policy into a pure function over `&[DescriptorObservation]` (the existing predicate corpus style in this file) would let index 0 — and arbitrary foreign-owner/ACL combinations — be tested with synthetic observations, and would make the README's "skip root" mutant claim true for the policy half as well as the observation half.

### N-1 — test-only retry: honest
Both helpers retry **only** `ChangedDuringRead` (≤256 × 1 ms), return every other result unchanged, and the production path is a single attempt (read: no loop in `observe_directories` or `inspect_directory_path_with`). Name, policy and other descriptor failures are never retried — my mutants that produce them are killed immediately, which would not happen if the retry masked them. The preserved r2 failure explains why it exists.

### N-2 — Linux standing
`observe_descriptor` on Linux still returns `UnsupportedPlatform`, so the chain observation fails closed there and `collect()` cannot turn that into an empty success (a linux-only test asserts it; I could not execute it on this host). On Linux, therefore, 191 adds no usable capability yet — consistent with the README.

### N-3 — refusal reports the first failing component only
Sufficient for admission; a diagnostic surface (`doctor`) would want all of them. Not needed here.

## 7. Limits

macOS only; one machine's real directories; my ACL cases use `everyone`/`root` principals. I did not test network or non-local filesystems, mount substitution, or a chain deeper than the fixture's. No consumer exists, so nothing is said about how a host will use the result. I did not rebuild the owner's five compiled mutants or host receipt 120.

## 8. Verdict (bounded)

**The observation covers every retained descriptor root-to-leaf with no partial success, the join applies the existing S3 predicate to every component with no waiver, the four error classes are distinct, name rechecks bracket the observation, and the stated limits (sequential samples, ABA, post-sample permission change) are real and honestly disclosed — I reproduced them. No defect. W-1 should be fixed before anything calls this function, because the bytes do not say it is not the S3 walk; T-1/T-2 name three policy faults the suite cannot see, one of them structurally.** No custody, host or cumulative approval.

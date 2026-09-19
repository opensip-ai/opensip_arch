# Independent review — frozen `custody-policy-checkpoint-193`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only. macOS host.
Scope: exactly the frozen 193 product bytes — the follow-up to my 191 W-1, T-1 and T-2 in `security/custody.rs`. As asked, I did not repeat the unaffected 191 review; I checked behaviour preservation, forwarding, precedence and closure. No authority, exclusion, custody or cumulative approval. The separate 194 `is_readonly` candidate is not reviewed here.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `92bedb7de18c516a4fabccce06c6538969bc1c158dd893db230a4789600fd552`, 4,238,320 B = request = `archive-pin.json` |
| Members | 401, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 352/352; none unpinned |
| Parent | equals **my own verified 191 extraction**; 351 unchanged; only `crates/security/src/custody.rs` changed (`bc2da2c2dc8cbfba…`); fixtures unchanged |
| Host receipt 121 | 232 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **150 security tests pass; strict workspace Clippy exit 0**.

## 3. The change, as read

Production delta: (a) a doc comment on `inspect_directory_path`; (b) the per-component loop moved verbatim into a pure `check_operational_chain_observations(&[DescriptorObservation], uid, groups) -> Result<(), DirectoryPathRefusal>`; (c) the actual path calls it in the **same position** — after the post-observation name recheck — and returns the observations; (d) one comment word, "configuration" → "operational". No predicate, error class or ordering changed.

## 4. Behaviour preservation

My complete 191 probe (real directory chains: fixture, wrong uid, `/private/tmp`, my `HOME`, eleven ACL variants on a middle ancestor, authorized/unauthorized group, post-sample chmod, leaf replaced, ABA) run **verbatim** on the 193 tree produces output **identical** to my 191 run once the random directory tags are normalised (`claude-out/io/custody.txt`; diff in the run log). Including the two documented limits — they are unchanged, as they should be.

## 5. Closure of my 191 findings

### W-1 (not the S3 walk) — **closed**
The doc comment now says what I asked for, in the function's own words: "Inspect a retained operational/store path after selection. This is not the S3 project-discovery walk: it examines the entire chain to the filesystem root, refuses any failed component, and grants no explicit-project owner waiver. Discovery has its own stopping boundaries, ancestor fallback, and --trust-project-owner rules; this function must not replace that walk. … Success is only a sampled predicate result, never exclusion or a permission to consume/write evidence." All three S3 differences I listed (boundary vs refusal, waiver, stopping point) are named. The inviting word "configuration" is gone.

### T-1 (uid and groups forwarded without a test) — **closed**, by re-applying my survivors (`claude-out/probes/mutation.{py,json,log}`)
| Mutant | 191 | 193 |
|---|---|---|
| owner check waived for ancestors | survived | **KILLED** — by the actual wrong-uid chain test *and* two synthetic tests |
| authorized groups ignored | survived | **KILLED** — actual middle-ancestor test and the synthetic forwarding test |

### T-2 (policy on component 0 untestable) — **closed** structurally
| policy skips the root | survived both suites | **KILLED** by three synthetic tests (`every_component_including_root_and_leaf…`, `first_refusing_component…`, `uid_and_group_authorization…`) |
The pure helper is exactly the seam I suggested; the synthetic corpus drives six refusals × three indices, uid-0/root and invoker ACL writers, authorized vs unauthorized gid, and first-refusal reporting.

### Further mutants aimed at the new code — 8/8 killed
policy skips the leaf; first-and-last only; **last** refusing component reported; owner waiver for the root only; groups forwarded to the leaf only; actual path skips the helper; helper run **before** the post-observation name recheck (precedence — killed by `changed_names_stop…`); invoking uid not forwarded by the actual path. Total 11/11; baseline green; none failed to compile.

## 6. Findings

None against the change. One note:

### N-1 (low) — the pure helper admits an empty chain
`check_operational_chain_observations(&[], …)` returns `Ok(())` (measured, `io/helper.txt`): the loop is vacuous. Unreachable through the actual path — `observe_directories` always yields the root, so ≥ 1 — but the helper is now the shared policy entry that 194-style integrations will call with observations from elsewhere. "No components" should be a refusal (or a debug assertion plus a test), so a future caller cannot turn a failed or skipped observation into a pass.

### N-2 — the wrong-uid native test needs an unprivileged runner
It asserts `uid != 0` with a clear message rather than silently passing as root. Correct choice; CI running as root will fail loudly, which is what you want, and is worth a line in the host-isolation script notes.

## 7. Limits

macOS only (Linux ACL observation still `UnsupportedPlatform`, so the native tests are macOS-gated; the synthetic tests run everywhere). I did not rebuild the owner's three compiled mutants or host receipt 121. No consumer of this function exists yet.

## 8. Verdict (bounded)

**191 W-1, T-1 and T-2 are closed: the scope is stated in the code, the policy loop is a pure tested helper, all three of my 191 survivors now die, eight further faults die, precedence is preserved, and my entire 191 real-directory probe is unchanged on these bytes. One low note: the helper should refuse an empty chain.** No authority, exclusion, custody or cumulative approval.

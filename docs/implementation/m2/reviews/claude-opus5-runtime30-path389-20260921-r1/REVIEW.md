# Combined review — source 389 (project-root raw path capture) and formal runtime30

**Verdict: ACCEPT-DESIGN-UNIT**
**subjectManifestSha256:** `21359758b280d44ca094be5f0206d7c0a4af562808092dbb4888021bc557dd3b`
(`docs/implementation/m2/native-runtime-selection-v30-subject.json`, 2521 bytes, 12 members)
**requiredFindings: none.** Four non-blocking observations are recorded in §6.

Performed as Claude Opus 5 (1M context); capacity available. Read-only: no live, frozen or history
bytes edited; no commits; no pushes. Everything below happened in this review directory. This
accepts the exact 12-member subject and the exact one-file source delta; it manufactures no root
assent, no live installation, no native authority and no M2/release claim. The 388 investigation is
separate and nothing here depends on it.

---

## 1. Verification performed before review

| Check | Result |
|---|---|
| Formal subject bytes | 2521 B, sha `21359758…dd3b` — matches |
| All 12 subject members present, exact bytes/sha | **12/12 match**, 0 failures |
| Member paths sorted and unique | **both true** |
| `successor.json` candidates | 11, sorted, unique |
| candidates ∪ {successor.json} = subject members | **true** |
| `passageOverrides` | `[]` — none |
| Candidate ∩ parents | **empty** — no collision |
| Candidates already recorded in the selected lock | **none** |
| Three parents live-match their pins | **yes**, all three |
| Three parents are the selected items | runtime29 successor and registry-v2 successor are `contractSuccessors` records in `design-lock.json`; inventory58 is a lock record. **All three present** |
| Source archive pin | 6894600 B, sha `d5009ba7…2b95` — matches `archive-pin.json` and the request |
| Source manifest | 113048 B, sha `3e5a26e0…2bd8` — matches |
| Every archive member vs manifest | **601/601 match**; 0 missing, 0 extra, 0 mismatched; no non-regular, absolute or `..` member |
| Archive composition | 591 `product/*` + 9 `evidence/*` + 1 `README.md` = 601 |
| Archive product set vs live tracked set | both 591; **590 identical, exactly 1 differing** |
| The one differing file | `crates/platform/src/filesystem/path_binding.rs`, before 20526 B `82f6db21…`, after 25337 B `582366ee…` — matches the stated SHA |
| Live product unchanged after all work | `git status` clean at `526a1867a34d…` |

## 2. Staging helper

`native-runtime-selection-v30/stage.py` is **byte-identical** to the reviewed runtime29 helper.
Reading it rather than trusting it, it: pins every baseline file before *and* after staging; requires
`HEAD == baseline.productHead == mapping.baseProductHead`; requires the live tracked set to equal the
baseline set; verifies the archive pin and **every member digest before any extraction or output
creation**; refuses a pre-existing output; requires map completeness
(`candidate == changes ∪ unchanged ∪ {design-lock.json}`); forbids the lock from being a mapped
change; copies from the **live** tree and overwrites only mapped changes; then asserts the staged
lock equals the live lock.

One point I checked specifically because it is easy to get wrong: the lock exclusion is keyed on the
**exact relative path** `'design-lock.json'`, not on a basename. The second lock-named file in the
tree, `tools/typescript-boundary/tests/fixtures/product/design-lock.json`, is therefore **not**
exempted and is verified like any other source file.

My private staging reproduced the author's recorded `stage.stdout` exactly apart from the output
path: `archiveMembersVerified 601, nonLockSourceFilesVerified 590, mapped 1, unchangedNonLock 589,
liveProductUnchanged true, runtimeAcceptance false`. 1 + 589 + 1 lock = 591.

## 3. Substantive source assessment — what the change actually does

The whole delta is a refactor plus one new public method. Parsing moves out of `open_inner` into a
private `components(raw, max_components, usage)` with `enum PathUse { Internal, ProjectRoot }`;
`open` routes to `Internal`, the new `open_project_root` routes to `ProjectRoot`, and both then run
the **same unchanged** retention loop in `open_for`.

**3.1 The project-root grammar faithfully implements the selected registry-v2 spelling.**
Registry-v2 `owner.md` requires raw POSIX bytes that are "absolute, 1..4096 bytes, no NUL, repeated
separator, trailing separator except `/`, or `.`/`..` component". The implementation enforces
exactly that set — `starts_with(b"/")` (which also gives the ≥1 minimum), `contains(&0)`,
`len() > 4096`, and empty/`.`/`..` components — and it restricts backslash and the staging prefix to
`Internal` only. Backslash and `.opensip-stage-*` are not in the registry-v2 exclusion list, so
admitting them as ordinary project names is correct, not a relaxation.

**3.2 The internal path is behaviourally unchanged — verified differentially, not just argued.**
The bound check moved from "collect everything, then test `parts.len() > max_components`" to
"error when `parts.len() == max_components` before pushing the next part". These are equivalent
(both fire exactly when N > max_components) and both emit the same `InvalidInput` with the same
message. Rather than rest on that argument I built two copies — `probe/old` (live pre-change) and
`probe/new` (candidate) — added an integration test that only uses the **public** API (the subject
file is untouched in both), and ran an 18-case corpus through `RetainedDirectoryPath::open` on each:

> **18/18 identical.** Root, relative, empty, `//`, inner-empty, `.`, `..`, trailing slash, NUL,
> backslash, staging at root, staging nested, non-UTF-8, at-cap, over-cap, 5000-byte, exactly-4096
> and over-4096 all produce the same outcome on both builds.

`evidence/probe-old.txt` vs `evidence/probe-new.txt` diff clean. The existing test
`stable_path_retains_native_names_and_exact_component_bound` independently pins the boundary
(`count-1` errs, `count` succeeds, `open("/", 0)` succeeds), so the bound equivalence is guarded by
the corpus as well as by my probe.

The refactor is also a small genuine improvement: the old code materialised every component before
testing the bound; the new one stops at the cap, so the vector is bounded by `max_components`.

**3.3 The two grammars differ exactly where intended — verified at the public API.**
A second probe ran both methods over the same inputs on the candidate build:

| input | `open_project_root` | `open` |
|---|---|---|
| `/a\b` | NotFound (grammar accepted, OS says absent) | InvalidInput (grammar refused) |
| `/.opensip-stage-x`, `/a/.opensip-stage-x` | NotFound | InvalidInput |
| `/a\0b`, `/a/../b`, `/a/` | InvalidInput | InvalidInput |
| `/` | OK | OK |
| 4097 and 5000 bytes | **InvalidInput** (syntactic) | InvalidFilename (OS) |
| exactly 4096 bytes | **InvalidFilename** | InvalidFilename |

The last row is the useful one: the 4096-byte path is *accepted by the grammar* and then refused by
the OS, because a single 4095-byte component exceeds `NAME_MAX`. That independently substantiates
the README's caveat that "byte syntax is not native filesystem acceptance" — the total-byte bound is
not a promise that the kernel takes the path.

**3.4 Retention, flags and rechecks are shared, not duplicated.** Both usages reach the same
`open_for` loop, the same `root()` (`O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`, `read(true)`) and
the same `child()` (`openat` from the retained parent with `O_RDONLY | flags()`). Every hop is
descriptor-relative and no-follow; the post-retention `recheck()` and the `InvalidData` refusal on a
name change during retention are untouched. No normalization exists anywhere: `components` returns
slices of the caller's bytes and `CString::new(part)` uses them verbatim.

**3.5 Nothing is wired up.** `open_project_root` has **no caller** anywhere outside its own test
module (verified across `crates`, `apps`, `tools`). Existing `RetainedDirectoryPath::open` callers
(security journal store, security lib) are unchanged and still route to `Internal`. `source-delta`
reports `newFiles 0, packageGraphChanges 0`, and my own archive-vs-live comparison independently
confirms one changed file and no additions — so no new crate edge, file or inventory entry.

**3.6 Scope disclaimers are accurate.** The doc comment on the new method states it is sampled
name/descriptor evidence, that the caller still owes shared-budget precharging and
exact-name/filesystem/custody admission, and that syntax does not promise OS acceptance. Each of
those is true of the code as written. Nothing in this delta touches registry admission, custody,
profile/UUID qualification, current authority, initialization, S9.3 or any writer.

## 4. Tests — independently replayed

Replayed with the author's exact command under the pinned environment (Rust 1.95.0
`59807616e 2026-04-14`, offline `--locked` against the verified 368 vendor CARGO_HOME, my own
`CARGO_TARGET_DIR`, `HOME` preserved, native `TMPDIR`, `RUST_TEST_THREADS=1`, no other native job
running):

> `test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 95 filtered out`

identical to the author's record. The workspace all-targets check also passes (`rc=0`, 16.24 s).

Assessed against what the request required the tests to substantiate:

| Requirement | Covered by | Adequate? |
|---|---|---|
| Literal names | `project_root_keeps_raw_names…` creates real `literal\backslash` and `.opensip-stage-project` directories, shows `open` refuses and `open_project_root` retains, reads the witness | yes — real native retention, not a syntax assertion |
| Grammar bound | `project_root_grammar_is_byte_bounded…` rejects empty/relative/`//`/`/a//b`/`/a/./b`/`/a/../b`/`/a/`/NUL; accepts exactly 4096; rejects 4097; `/` with cap 0 | yes |
| Non-UTF-8 spelling | same test: `/raw-\xff/literal\name` → two byte-exact components; cap 1 errors | yes — asserts the exact slices, proving no normalization |
| Old internal restrictions | `strict_absolute_path_shape_refuses…` (existing) still lists `/a\b` and `/.opensip-stage-x` | yes |
| Symlink / relocation | `project_root_retention_keeps_symlink_and_mid_capture_relocation_refusals` covers symlink-on-recheck, symlink-on-open and mid-capture relocation via the private seam → `InvalidData` | yes |
| Exact-name behaviour | first new test calls `recheck_exact_names()` on macOS, and after rename+recreate the handle still reads the **original** bytes while `recheck()` is false | yes — this is the important one: it proves descriptor retention rather than path re-resolution |

The one thing the corpus does not do is compare old against new; that is what my probe in §3.2 adds.

## 5. Formal unit assessment

The formal unit is well formed: subject verifies exactly, candidates are sorted, unique, collision
free and exactly the subject minus the successor; `passageOverrides` is empty; the three declared
parents are precisely the three selected items (runtime29, registry-v2, inventory58) and all
live-match their pins; the staging helper is the byte-identical reviewed v29 helper and its recorded
evidence reproduces. The successor's own `standing` reads "PROPOSED … independent source/formal
review required", which is the correct self-description for bytes under review.

## 6. Observations (non-blocking, no required findings)

- **O-1. `Internal` still has no syntactic length bound.** Only `ProjectRoot` applies the 4096-byte
  limit; an internal path is refused by the OS (`InvalidFilename`) rather than by the grammar. This
  is pre-existing (the old code had no bound either) and internal paths are product-constructed, so
  it is not a regression and not in scope — recorded so the asymmetry is deliberate rather than
  discovered later.
- **O-2. The retained type does not record which grammar admitted it.** Both methods return a bare
  `RetainedDirectoryPath`. I checked whether that could be abused and concluded **it cannot today**:
  the staging-prefix guards that matter are applied per-operation on the *names the caller supplies*
  (`filesystem.rs:135` `open_regular`, `:331` confirm, `:748` replace), not inferred from the handle.
  Worth a marker or newtype when the authoritative producer arrives, if any consumer ever needs to
  assert "admitted under internal spelling rules".
- **O-3. `max_components` remains caller-chosen.** Correctly disclosed as a mechanism bound with
  producer precharge still owed; the parser now stops at the cap, which bounds the allocation but is
  not a budget.
- **O-4. Test-fixture lock.** Not a defect — noted only because the helper's exact-path exclusion is
  what keeps `tools/typescript-boundary/tests/fixtures/product/design-lock.json` under verification.

## 7. Limits of this review, stated honestly

I replayed the 15 path-binding tests and the workspace all-targets check only. I did **not** run the
other 95 platform tests, the full workspace test suite, or any provider build — none was requested
and the identity provider sources are unchanged. My differential probe covers the **public** `open`
API over an 18-case corpus; it is not exhaustive and does not reach the private `components`
function directly, and it was run on macOS arm64 only. Real-directory behaviour was exercised only
where the author's tests create fixtures; my probe's project-root rows resolve to `NotFound` because
the paths do not exist, which proves grammar acceptance but not successful native retention of such
names beyond what the author's first new test already shows. I did not re-verify runtime29,
source386, inventory58 or registry-v2 themselves; their selection is taken as recorded in the lock.
No native filesystem, UUID or profile behaviour is qualified by anything here. Acceptance is of the
exact 12-member subject and the exact one-file delta at arch `55d0f68a2` / product `526a186`; it is
not a live installation, not native authority, not a production caller switch, not S9.3 or any
writer/bootstrap/recovery permission, and not completion of M2 or release.

# C1c plan r4, addendum unobservable-name: counting a malformed name needs an observed kind (LD-C1C-5A), r2 (coordinator, 2026-10-29)

**Status: PROPOSED.** This text is under R3 different-vendor review (`REQUEST-r2.md`). It takes effect only when the
coordinator records its adoption, owner-delegated under OD-AUTO-1, in a separate receipt,
`ADOPTION-unobservable-name.md`. That receipt pins this file's sha256 and the accepting review's sha256. This file is
never edited after review.

**r2 answers R3 review r1** (`REVIEW-r1.md`, `L8-RULING: REFUSE-AMENDMENT-CHANGES`):
- **Finding 1:** the obligation is narrowed to the counting exception. Existing order and validation are kept.
- **Finding 2:** the full refusal funding is kept.
- **Finding 3:** the controls are replaced, and grammar rejection is kept distinct from native errors.
- **Finding 4:** the staging-prefix history is corrected, and the receipt's contents are named.

The author's control note (`AUTHOR-NOTE-r1-controls.md`) is folded into §4. r1 is kept unchanged as
`ADDENDUM-unobservable-name-r1.md`.

**What it amends:**
- **The plan:** C1c plan r4,
  `opensip_arch/docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r4.md`
  (sha256 `d066487af5608b0375bd0ba1f8eaefda9b8bdbe70d27d96a875ba43cca8fe835`).
- **Inherited authority:** addendum guard-charge (LD-C1C-7A; `../l5-review/ADDENDUM-guard-charge-r2.md` and its
  adoption receipt).
- **Unchanged:** PLAN-r4's bytes are not edited.

**Why:** C1c-1 code review r2, RF-2 (`lead-2026-10-25/c1c1/review/REVIEW-r2.md`), and the author's request
`c1c1/COORDINATOR-REQUEST-L8.md`.
- **The exception:** LD-C1C-5's Names rule (the Q4 ruling) lets the read set count, without reading, a regular file
  whose name is malformed and has no matching suffix.
- **The gap:** applying that exception requires the entry's kind. The only no-follow kind observation in scope is
  `RetainedDirectory::observe_child`. That function checks the platform component predicate before any `fstatat`
  (`crates/platform/src/filesystem/directory_open.rs`:12-31 and :115-140, at a009ad6). The predicate rejects:
  - empty names, `.` and `..`;
  - names containing `/`, `\` or NUL;
  - names beginning with `.opensip-stage-` (`filesystem.rs`:27);
  - names longer than 1,023 bytes.

  It does not validate UTF-8. For a rejected name, no kind is observed. Counting an entry of unknown kind can skip a
  directory, and so publish an incomplete read set.

## 1. Superseded text

In LD-C1C-5's **Names (Q4 ruling)** (PLAN-r4 line 90), this sentence is replaced:

> A regular-file name without a matching suffix is outside item 3's read set: it is filtered on its raw bytes before
> any `LogicalPath` admission, so a non-UTF-8 name is handled safely, then counted and disclosed, never read.

**By:**

> A regular-file name without a matching suffix is outside item 3's read set. It is filtered on its raw bytes before
> any `LogicalPath` admission, so a non-UTF-8 name is handled safely, then counted and disclosed, never read.
> **Counting under this exception needs an actual, permitted kind observation.** That means a no-follow observation
> that returns the entry's kind, and only then an entry observed as a regular file is counted. An entry the exception
> would count, but whose kind is not observed, is not counted:
> - **(a)** If the platform component predicate rejects the name before observation, the snapshot refuses `Name`
>   with the parent and the escaped name bytes, as a malformed descended directory refuses.
> - **(b)** If the observation reports the entry absent, the snapshot refuses `Name` in the same way.
> - **(c)** If the predicate accepts the name but the native observation fails with any other error, the existing
>   `HostIo` refusal applies, with its native provenance preserved.
>
> A kind is never inferred from a suffix, from absence or from an error.

"Malformed" keeps its existing meaning: the whole candidate path, the authorized parent followed by the name, fails
the existing component checks or `LogicalPath` admission. It is not a test of the raw basename alone.

## 2. What does not change

- **Order and validation:**
  - listed names are charged as before;
  - exact `.` and `..` entries are discarded before validation or observation;
  - a listing failure still precedes any pending-name refusal (`ListingConversion::finish`,
    `custody/discovery_walk.rs`:376 onward);
  - a malformed candidate whose name has a matching suffix still refuses `Name` through the existing malformed-
    candidate path, with no kind observation required. This includes a staging-prefixed `.ts` name, already rejected
    by `listed_path` (`discovery_walk.rs`:289-299);
  - a malformed directory that would be descended still refuses `Name`.
- **Unaffected paths:**
  - a path that converts successfully keeps its existing observation path;
  - its disappearance between listing and observation keeps the existing `Changed` route;
  - native errors keep propagating as before.
- **Inherited rules:** observed non-matching regular files are counted, matching valid files are read once, and other
  entry types are counted. All of these remain subject to `read_set_path`'s authorization and exclusions, to
  candidate validation, and to the guard (LD-C1C-7A). This addendum creates no unconditional read or count.
- **The raw-byte exception:** it keeps its full scope for observed entries, including non-UTF-8 names the predicate
  accepts. It is not narrowed because a test platform cannot create such a name.
- **No new platform API:** the platform predicate is cited, not changed. LD-B2B3-2's first-party refusal code and
  its pruned-anchor scope stay its own. This addendum does not import them into the read set.

## 3. The consequences, stated

- **New refusals, a narrower admitted set.** A dependency package containing a regular file whose malformed,
  non-matching name the predicate rejects (for example, `back\slash.txt`) now refuses `Name`; before, the law counted
  it. A malformed, non-matching name reported absent at observation also refuses `Name`.
- **What is not new.** A matching staging-prefixed or backslash name already refused `Name` through the existing
  malformed-candidate path, with no read attempt. This addendum does not change that.
- **The funding, unchanged in kind:**
  - an observation attempt, when made, is funded before the call;
  - all the other work a refusal needs keeps its existing C1/C7 funding: listing conversion and retained raw bytes,
    escaped-name construction (`escaped_name_cost`), the parent copy in `listing_refusal`, and the terminal error;
  - when that work is under-funded, budget exhaustion can be returned before `Name` is built. "Names the parent and
    the escaped bytes" applies only to a `Name` that was built;
  - the malformed-name observation and refusal work is *N*, under its existing definition and margin condition, and
    never *L*;
  - no cap and no *L*max changes;
  - any claim that the accepted *T* pricing is unchanged is verified against the final implementation and model. It
    is not inferred from this text;
  - no synthetic input beyond the real listed-name bound is priced through this refusal path as if it were a sound
    larger-input price.

## 4. The controls

Each control is tied to the production code path.
1. **Pure decision tests,** run on the production decision helper over synthetic raw bytes and observation results,
   scoped to the malformed, non-matching-name exception:
   - observed as a regular file: counted, including invalid UTF-8;
   - observed as a symlink or another non-directory kind: handled as the inherited entry-type rules say;
   - observed as a directory: refuses `Name`;
   - absent: refuses `Name`;
   - predicate rejection: refuses `Name`;
   - another native error: `HostIo`.

   These tests establish the decision only, not an observation or a listing. They apply to no valid directory and no
   valid matching file.
2. **Real boundary tests** on a retained directory, through the real observation:
   - a 1,024-byte component, otherwise permitted, fails the predicate with `InvalidInput` and no kind;
   - a 1,023-byte component passes the predicate. The native outcome on the supported test platform is recorded as
     observed, for example `ENAMETOOLONG`, and it reaches the read set as `HostIo`, not `Name`;
   - the mapping from the platform `io::Error` to the read-set refusal is tested separately.
3. **On-disk fixtures** below an authorized package:
   - a file `back\slash.txt` and a directory `dir\x` holding a `.ts` file each refuse `Name`, with the exact parent
     and escaped bytes;
   - a file `back\slash.ts` and a file `.opensip-stage-a.ts` refuse `Name` through the existing malformed-candidate
     path;
   - a file `.\n` (accepted by the predicate, not a `LogicalPath`, no matching suffix) is counted;
   - a directory `.\n` refuses `Name`;
   - a malformed, non-matching name is removed deterministically between listing and observation, and refuses
     `Name`;
   - a well-formed path removed the same way keeps `Changed`;
   - ordinary files and the other entry types behave unchanged.
4. **Funding:** for the new path, exact funding and one unit short at the observation attempt each refuse at the
   predicted point. The tests observe that the observation did not run when it was unfunded. Under-funding before
   `Name` is built returns budget exhaustion.
5. **Mutations, each detected by a control:**
   - count, instead of refusing, an entry whose observation is a predicate rejection;
   - treat an unobserved or absent entry as a regular file;
   - drop the absent-name refusal;
   - remove the observation charge, or move it after the call.
6. **Fixture limits:** the controls record the tested platform's real limits: on-disk creation is not possible for
   1,023- or 1,024-byte names or for invalid UTF-8 names. The law's scope is not narrowed by them.

## 5. What remains gated

This addendum does not accept C1c-1's source, model or pricing correspondence, control execution, lane evidence,
integration, binding or receipt interval.

At binding, C1c-1 copies this file and its adoption receipt unchanged beside PLAN-r4, and the inventory records them.

The adoption receipt records:
- this file's sha256, as the reviewed bytes;
- the accepting review's path, sha256 and verdict;
- PLAN-r4 and LD-C1C-7A, as inherited authority;
- the date and "owner-delegated under OD-AUTO-1";
- the owner notification.

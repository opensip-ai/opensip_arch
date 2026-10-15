# B2-b4 implementation plan r2 review

Verdict: **ACCEPT**. All three round-one findings are resolved at plan level. No required findings or non-blocking observations.

## Subject and verification

Independently rehashed the 452-byte `subject.json` to SHA-256 `788de3abab231fa9e280eecf40b864cab2a46218b1c5e172b05e6921767eb1b3` and verified its sole member: `PLAN-r2.md`, 19,185 bytes, SHA-256 `6182759527e363a686eae8806b31163622ae6d7789d6610d5ab0bc0a71821907`. Both repository HEADs match the requested bases; product main is clean. The lock retains inventory v195 and 164 contract successors. Verified the bound reference's exact bytes and the existing 52-vector population.

Compared r2 with the reviewed r1 and inspected the relevant native charge sites and delegated helpers, including `path_binding::status_read_cost` and `AclOmissionPremise::admits`. Rechecked the item-12 and plan-r4 gate language. This accepts an implementation plan; no census tool, generated prediction, native soundness result or T2 margin has yet been established by this review.

## Round-one findings

**B2B4PLAN-R1-RF-1 — resolved.** Section 1.5 replaces the member-sum formula with a composed checkout: retained non-symlink overlay entries plus verified member trees placed at their mount names as ordinary directories. The entire composition uses the same reference population and cost model as a repository. This accounts for the nesting transitions identified in r1, including classification, spelling, open/status, boundary probes, depth/pruning and chain custody. The planned native workspace vectors cover boundary members, pruning, units and depth, and the member-sum mutation must fail. The old sum is explicitly rejected; the request's legacy question about that sum is answered by this replacement, not by endorsing the r1 formula. Actual symlink mounts remain untraversed.

**B2B4PLAN-R1-RF-2 — resolved within the stated envelope.** Integrity explicitly refuses any T2 tree with a `.git` component. The native discovery path's charged file read is `gitdir_target`, reached for a regular `.git` file; excluding that component removes this read/retry dependency from every successfully censused T2 tree. A refused entry cannot be converted into a passing margin or silently omitted from the all-entry gate.

For synthetic vectors containing `.git`, the plan now states an uninterrupted envelope: one read-buffer object and at most `min(L, max + 1) + 1` attempt edges. Positive short reads advance at least one byte; EOF or an ordinary error terminates; reaching the ceiling refuses. Interrupted retries are explicitly excluded, each costs an additional edge, and ledger exhaustion remains terminal. The plan no longer claims that file length bounds arbitrary interrupted reads. The planted `.git` refusal and read-envelope boundary cases are appropriate controls. This is a structural T2 census claim, not a promise of completion under arbitrary runtime interruptions.

**B2B4PLAN-R1-RF-3 — resolved.** The pinned closure now includes `filesystem/path_binding.rs`, `trust/initial_platform.rs`, the discovery core/rule, listing implementation and ledger, in addition to the previously named charging files. Whole-file hashes refuse any byte drift; anchored formula extraction is an additional check. The delegated-status mutation catches a changed helper with an unchanged caller, and the planted-charge mutation catches changes outside existing anchors. The inventory identifies direct and delegated costs rather than treating an unchanged calling expression as a complete dependency pin.

## Cost inventory and controls

Checked the inventory against the native code. It covers root records/status; listing and raw names including dot entries; owned names, paths and validator copies; by-name observations and new scope records; retained observation tuples; classification temporaries and target segments; directory opens/status; VCS/config probes; non-boundary frames; entry/listed and Cargo records; depth-limit marker probes; memoized chain judgments; marker spelling/open/status/capture; and the named-root/spec/chain paths. The `.git` branch includes open/status, custody capture, bounded-reader envelope, final status and parsed-target storage. Core/rule evaluation takes no discovery `WorkScope` and adds no ledger term.

The declared upper-bound treatment is sound for the stated population/envelope: assume metadata reaches captures, use the fixed maximum capture allowance, and add the filesystem-observation branch. That branch costs one object/two edges and dominates the alternative ACL-vector owned record's one object/zero edges. Count both dot names before discarding them. Objects and edges do not depend on absolute spelling length; this does not establish a byte bound.

The 52-vector native comparison, added composed-workspace comparisons, four required model mutations and five tool controls form an appropriate planned soundness suite alongside source/formula inspection. They must be demonstrated during implementation review; finite vector checks alone are not a universal proof. Avoiding native corpus-store walks in product tests is sound and does not prevent scratch-tree controls.

## Integrity, scope and remaining gate

The proposed integrity procedure reconstructs both QD-22 and Git-tree pins from stored bytes, handles symlink target text without following it, includes pinned gitlink commits/placeholders, checks exact modes/population and refuses mismatches or unsupported objects. The new `.git` restriction is fail-closed. The manifest has 39 lead-readable repositories, ten held-out repositories and five non-held-out workspaces. The early held-out branch reads only flag/id, before store lookup, and its planted-digest control must enforce the no-join/no-stat boundary.

Reusing the accepted adapter and bound `walker_population`/`finish` retains population/rule authority. The model must preserve operation multiplicities, including absent probes and repeat observations, as the charge inventory requires. Overlay/member integrity remains necessary before composing a workspace.

The plan refines r4 section 1.4 without changing its completion gate. A failing census may land as honest evidence, with failing rows and caps returned to law, while making no margin claim for those rows. Any item-12 cap amendment remains separately reviewed, uses the 2x rule on the verified modeled population and weighs a cheaper walker. Code limits change only after that amendment is accepted. Unread held-outs leave their margin outstanding and require the owner escalation specified by LD-B2B-4. B2-b is not complete until the all-entry margin holds or an accepted law change alters that gate. No owner assent is inferred.

The pre-census estimate remains explicitly unverified and is not evidence. I did not independently count it. No cap change, production caller, byte census, binding, law change or qualification is accepted here.

Only read-only reading, hashing, JSON parsing and Git queries were used. No stores or overlays were traversed; no held-out store or overlay was joined, statted or opened. No Cargo, tests, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys or held trees were accessed. Only `REVIEW.md` and `review.json` were written; neither repository, stage nor controls were edited.

# Creator-eligibility source audit for 392

Bounded source audit requested while root revises 390 against RF-1…RF-4. **No acceptance is
claimed and none is implied.** Read-only: no live, frozen, product or lock bytes edited; no commits;
no pushes; no native tests. Everything below is either an **[S] selected requirement** with a file
and section anchor, or a **[R] recommendation of mine**, never mixed.

**HEADs verified at the time of this audit** (re-derived, not carried forward):
architecture `cd753cc02`, product `cd5af4d`.

Scope: locate the exact existing selected sources for (A) which command/workflow ingress may
initialize I, (B) native account/principal/trust-group admission, (C) delivering-core
launch/closure/platform admission before any local trust state exists — then name the bootstrap
circularities and the policy choices that must be made explicitly.

Method: the authority set is the 46 `inputs` of the selected `design-lock.json` plus its accepted
contract successors. I searched those inputs directly rather than the whole tree, so "not found"
below means "not present in any selected input", which I state explicitly where it matters.

---

## A. Command/workflow ingress — more is already selected than 390 assumes

### A1 [S] Durable-write permission is already partitioned by command class

`docs/coop/completion/security-completion.v8.md` §3.3 "Verification at install and launch, by command
class (WA-6)", lines 188–200 (lock input; retained as `launch-verification-classes.json`):

| Command class | Trust evaluation | **Durable writes** | Must not open |
|---|---|---|---|
| metadata-only (`--help`, `--version`) | none | **none** | `trust.sqlite`, registry, lock, inventory members, grant journals, any helper process, any project path |
| doctor (both read-only modes) | report-only, non-persisting | **none** | any file for writing under the install root; any helper process |
| operation (`analyze`, `install`, `remove`, `update-index`, trust refresh) | decision evaluation with write-ahead `evalHighWater` | **yes, under §5.6** | — |

This is the positive skeleton RF-1 asks for, and it already exists as selected law. It is
corroborated at §5.6 (lines 315–325): durability costs "are paid only at operation boundaries and
decisions (§3.3), **never by metadata-only commands or doctor**".

### A2 [S] The first-write operation is named, and it is not a new command

`docs/v2/contracts/product-v1/identity-and-evidence.md` §5 (line 1631), first paragraph (1633–1641):

> "Default `opensip`/`analyze` is DURABLE_AUTHORITATIVE under CD-RT-5. The host reports retention
> origin DEFAULTED and durable-unbounded posture **before first write**; the command's documented
> effect is **admission of the project marker and private registry/store**, followed by an
> authoritative Run. … `--ephemeral` is explicitly non-authoritative, uses temporary custody, mints
> no authoritative commit receipt …"

`docs/v2/contracts/product-v1/security-and-lifecycle.md` line 1521 (migration obligation 2) names
the same operation and excludes the alternatives:

> "The new product's explicit `--ephemeral` analysis and metadata-only surfaces provide
> pre-initialization value **without a project marker, private registry entry, authoritative store,
> adoption or persistent cache write** … The new product's default authoritative analysis remains
> the **explicitly invoked, disclosed first-write operation of identity §5**. Distribution migration
> never invokes that operation implicitly."

### A3 [S] There is no initialization command, and none may be added silently

`docs/coop/design-corrections/workflows/command-inventory.v3.json` (lock input) holds 45 commands;
19 carry a `mutation` step. I enumerated all 19: `baseline-adopt/-export/-upgrade`, `policy-init`,
`waive`, `review-join`, `repair-recover`, `install`, `update`, `purge`,
`trust-recovery-challenge/-import`, `trust-refresh`, `trust-import`, `store-migrate/-rollback`,
`store-gc`, `core-update/-repair/-rollback`. **None is an installation `init`/`create`.** So creation
must be an effect of an admitted ingress, never its own surface — which is what 390 assumes, and it
is selected rather than merely assumed.

### A4 The gap: "admission" is not "creation"

identity §5 says the documented effect is *admission of* the project marker and private
registry/store. It does not say which ingress may **bring I into being**. The selected registry-v2
owner (`docs/implementation/m2/project-registry-owner-selection-v2/owner.md` line 33) closes the
other side of the same hole:

> "Only the **separately authorized pristine installation creator** can publish the initial empty
> registry; directory emptiness alone is not proof of a pristine installation."

and root's own accepted assent for that unit records "no migration or **inferred pristine
creation**". So selected law *delegates* creation to an authorized creator and declines to define
it. **[R]** 390's phrase "persistent first-write invocation" silently merges two different things —
permission to write durably (A1/A2, selected) and permission to create the installation (nowhere).
RF-1 should be answered by building on A1+A2 rather than inventing a new predicate.

---

## B. Account, principal and trust-group admission — largely selected, but for the *project* root

### B1 [S] Discovery is account-database derived, never environment derived

`security-and-lifecycle.md` §S3 "Discovery and custody (AR-03)", line 105 ff.:

> "Discovery is deterministic over lstat/ACL results obtained through `O_NOFOLLOW` handles: **no
> environment variable, no `PATH`, no `HOME` (the account home comes from the account database)**.
> Output is the closed `DiscoveryProvenanceV1`."

Required host observations are closed and typed: `invokingUid`, `accountHome`, `cwd`, `fs`;
optional `ci`, `trustProjectOwner`, `authorizedGroupIds`, `explicitProject`, `explicitResolved`,
`explicitJoins`, `configWorkspaceRoots`. Unknown or missing keys are instrument errors, not public
refusals, and "Public invocation/configuration admission still **precedes** this host-only seam."

### B2 [S] Directory custody and the trust-group rule

Same section: custody passes only if the directory is real (no symlink), owner is the invoking uid
or root, no other-write bit, no group-write bit unless the gid is in the explicitly authorized set,
no ACL write grant to any principal other than invoker/root/authorized group, and the ACL was
readable. "Mode bits alone never establish exclusion."

> "Group authorization exists **only through an explicit `--trust-group <gid>` invocation argument**
> and is recorded in provenance; **configuration cannot grant it**."

`--trust-project-owner` waives only the owner check and only with an explicit `--project` path. And
the honest limit: "The lstat/ACL map remains a **synthetic trusted observation, not proof of native
custody**."

### B3 [S] Principal classes

`security-and-lifecycle.md` §S10 (line 1056): `first-party`, `repository-code`,
`imported-artifact`; repository execution disabled by default.

### B4 [S] Ordering before any writer

`identity-and-evidence.md` §2 (line 47): "The host verifies marker, root identity, owner, no-follow
handles and registry binding **before any project writer**. Missing marker and registry is first
use…" and "Discovery and admission use the **security unit's root boundary**."

### B5 The gap: none of this is about the *installation* root

§S3's walk, boundaries and custody rules are written for the **project** root (launch directory
upward, VCS markers, config selection). The installation root I has no selected location, custody
rule or ancestor policy. I checked this rather than assuming it: searching all 46 selected lock
inputs for `Application Support`, `.local/state` and `preview-v1` returns **NONE**.

Product is correctly silent rather than quietly authoritative:
`crates/security/src/custody/installation_root.rs:15` holds
`const SUFFIX: [&str; 4] = ["Library", "Application Support", "OpenSIP", "preview-v1"]`, and its
header (lines 1–4) states it "observes an existing root or a missing suffix, **never authorizes
initialization** or grants current authority. … No HOME/XDG/PATH/argv/project-root override or
filesystem mutation."

### B6 [S] `<installRoot>` is a selected *placeholder* with no selected expansion

> **Correction.** An earlier draft of this note said the location "exists only in product code".
> That was wrong, and I found it only because a broad background search finished after the first
> draft. The corrected picture below is materially better for 392.

Selected law **uses** an install root by name without ever defining where it is:

- `security-and-lifecycle.md` §S7 lock-order table, **line 588**: lock order 0 is
  "lifecycle fence | `<installRoot>/lifecycle.fence`, flock `LOCK_EX` | bounded wait 5 s, then
  `PROJECT.BUSY`" (restated at line 616). **The fence carrier path, lock mode, lock order and
  bounded wait are therefore selected** — the product's `lifecycle.fence` is not an invention, and
  390's choice to stage that exact file is consistent with selected law.
- `security-lifecycle.schemas.v1.json` uses `installRoot` (4 occurrences);
  `security-completion.v8.md` and `report-asset-binding.v1.json` use "install root".
- `security-and-lifecycle.md` **lines 706 and 708** (platform table) constrain it by filesystem:
  macOS "**APFS install root**"; Linux "**ext4/xfs/btrfs install root**".

So the gap is sharper than "undefined": selected law depends on `<installRoot>` in a lock-order
table, a schema and a platform table, and nothing expands it.

### B7 An unselected owner for exactly this already exists

`docs/coop/completion/host-foundation-completion.v2.md` (**PROPOSED**, Codex lead; "no register edit
or implementation authorization"; not a lock input and not a contract successor) is titled "Host
roots and preview configuration" and says it defines what "lifecycle and trust contracts call
`installRoot`". Lines 30–53 supply, as proposed text:

- the fixed locations — macOS `<account-home>/Library/Application Support/OpenSIP/preview-v1`,
  Linux `<account-home>/.local/state/opensip/preview-v1`;
- home resolved through the OS account database (`getpwuid_r` on the effective UID), never
  HOME/XDG, and "No initial-preview override selects a different operational root. Test harnesses
  may inject a root into a reference model; that is not a CLI or environment authority";
- 0700 directories, 0600 mutable files, no group/other access;
- an **ancestor rule**: "Verify each existing ancestor is a directory owned by root or the account
  and not writable by other principals. A symlink or unsafe ancestor refuses; no repair/chmod of an
  existing unsafe tree is implicit";
- and a **creation sentence** directly on RF-1: "A missing writable root may be created only by an
  **explicit state-using operation**, with **create-new, durable publication and the same checks**.
  Read-only commands report absence without creating it."

`reference-architecture.v2.md` (also unselected) repeats the locations at lines 114–115.

**[R]** This changes the recommendation in §E.3 from "draft new law" to "review and either select or
explicitly supersede an existing proposed owner" — and it hands 392 a ready phrasing for RF-1
("explicit state-using operation") that already agrees with A1/A2.

**[R]** Two divergences 392 must resolve rather than inherit silently:

1. **Layout conflict.** The proposed host-foundation root contains `lifecycle.sqlite`,
   `trust.sqlite`, **`lifecycle.lock`**, `generations/`, `staging/`, `quarantine/`,
   `projects/<namespaceId>/`, `settings.json`, `policies/permission-policy.json`, `cache/`. The 390
   tree contains `lifecycle.fence`, `project-registry.v2`, `stores/S/store-instance.v1`,
   `transitions/lineage/S/G/K.node`, `selection.pair`, `trust/stores/S/state.v1`. These are two
   different installations. Note the selected S7 table says **`lifecycle.fence`**, so 390 matches
   selected law and the older proposed doc does not.
2. **Filesystem narrowing.** The proposed doc says Linux "local ext4"; the selected platform table
   (line 708) admits **ext4/xfs/btrfs**. Adopting the proposed sentence verbatim would narrow a
   selected constraint.

---

## C. Core launch/closure/platform admission before a local trust state

### C1 [S] Launch verification is scoped and does not consult local trust state

completion v8 §3.3 (lines 195–200): the operation class performs "**open-then-verify of every
executed or loaded closure member on its opened fd** (the core itself and the component binaries
about to run), not an eager hash of the whole inventory", and separately "The install-time
verification of a payload (every member on its opened fd against the signed inventory before
publication) is unchanged from v2 §3.3."

Both compare executing bytes against the **signed inventory shipped with the core**. Neither reads
the local trust store.

### C2 [S] Fresh-install time evidence comes from the embedded payload

`security-and-lifecycle.md` line 348: a fresh install without admitted time evidence refuses
`TRUST.NO_ADMITTED_TIME_CONTEXT` — "the core's **embedded bootstrap payload** or an ordinary payload
is required". The embedded chain is likewise the pre-acceptance authority anchor in S9.3
(proposed, line 953 ff.) and in root's 215 embedded-head successor (proposed, reviewed by me at 390).

### C3 [S] Durability primitives already exist, including for directories

completion v8 §5.6 (line 315): macOS `fcntl(F_FULLFSYNC)` **on files and on the directory fd**
(falling back to `fsync(2)` only where the directory refuses it); Linux `fsync(2)` on file and
directory. Named boundaries include "**lifecycle publication**" and "**selection commit**".

This refines a statement in my 390 review: the directory-barrier **primitive and its fallback rule
are selected**; what does not exist is a *product API* for directory publication
(`publish_new_regular` is regular-file only) and a typed directory receipt. 392 should cite §5.6
rather than introduce a new barrier vocabulary.

### C4 The important positive result: core admission is **not** circular

Everything the core needs to be admitted at launch — its own bytes, the signed inventory, the
embedded bootstrap payload for first time evidence, and (under a schema-1 root) the platform profile
set embedded in the signed core release — arrives inside the delivered, signed distribution. None of
it requires a local trust state, a registry, a store or an installation. **So creator eligibility is
achievable without a bootstrap cycle**, and 392 can assert it constructively rather than by
exception.

The residue is narrower and already known: TR-CORE's *role standing* would need an accepted root,
which cannot exist before creation. That is exactly what the embedded chain is for, and the rule
selecting **which** embedded root is the pre-acceptance authority is still **proposed** (S9.3, and
root's 215 successor). 392 depends on that amendment landing; it should say so rather than rely on
S9.3 by implication.

---

## D. Circularities: which are real

| # | Candidate circularity | Verdict |
|---|---|---|
| D-1 | Core must be trusted before trust state exists | **Dissolves** — C1/C2/C4: verification is against delivered signed bytes, time from the embedded payload |
| D-2 | Platform/profile admission needs the profile set | **Dissolves** under a schema-1 root — the embedded copy in the signed core release is used |
| D-3 | Fence must arbitrate creation | **Real, already answered by 390** — the fence carrier lives inside I (`installation_fence.rs:13`, `lifecycle.fence`), so the exclusive rename is the arbiter |
| D-4 | Registry needs a pristine creator; creator needs an authorized ingress | **Real and open** — A4: registry-v2 delegates, nothing defines |
| D-5 | Which embedded root is the pre-acceptance authority | **Real, proposed only** — C4 residue |
| D-6 | Ancestor durability recursion needs a durable base | **Real and open** — RF-2; B5 supplies the natural base |

---

## E. Policy choices 392 must make explicitly

Each is a choice, not a deduction. **[S]** marks the selected material it should build on.

1. **Creator ingress.** **[S]** the operation class of completion v8 §3.3 and the default
   authoritative `analyze` of identity §5. **[R]** state whether creation is permitted for the
   *whole* operation class or only for the default authoritative analysis. The two selected sources
   disagree in scope: §3.3 grants durable writes to `analyze`, `install`, `remove`, `update-index`
   and trust refresh alike, while migration obligation 2 (line 1521) forbids distribution
   install/select from initializing. 390's exclusion list assumed the narrow reading without citing
   the tension. Choose, and say which sentence governs.
2. **`--ephemeral` and metadata-only exclusion.** **[S]** already selected (A2, A1). 392 needs only
   to cite it, not restate it as new law.
3. **Installation location and ancestor policy.** **[S]** selected law already depends on
   `<installRoot>` in the S7 lock-order table (line 588), the lifecycle schemas and the platform
   filesystem table (lines 706/708), but never expands it (B6). **[R]** do **not** draft this fresh:
   an unselected owner already exists (`host-foundation-completion.v2.md`, B7). Review it and either
   select it or supersede it explicitly, resolving the two divergences in B7 — the `lifecycle.lock`
   vs selected `lifecycle.fence` layout conflict, and the Linux ext4-only narrowing against the
   selected ext4/xfs/btrfs.
4. **RF-2 durability base case.** **[R]** the account-database home from §S3 and B7 — the one
   component the product never creates. Everything below it that this act creates owes its own
   directory and parent barrier under §5.6 primitives. B7's existing ancestor rule (owned by root or
   the account, not writable by others, symlink refuses, no implicit repair) is a usable starting
   predicate; what it still lacks is exactly the **durability** half that RF-2 names.
5. **Installation-root custody rule.** **[R]** §S3's custody predicate is written for the project
   walk; decide whether I reuses it verbatim (owner = invoking uid or root, no other-write, group
   only via explicit `--trust-group`) or gets a stricter rule, and say whether `--trust-group` may
   widen access to I at all. **[R]** my recommendation: it may not — a trust-group argument should
   not be able to broaden the installation root.
6. **Pre-acceptance authority root.** **[S-proposed]** depends on S9.3 plus root's 215 successor
   (D-5). 392 should name the dependency explicitly instead of adopting S9.3 by implication.
7. **Budget owner for a pre-installation act (RF-3).** **[R]** no selected budget owner covers an
   invocation with no installation. Either name the invocation-level owner or state that creation is
   bounded by a fixed manifest; do not cite "the authoritative budget" without one.
8. **Directory publication API.** **[S]** §5.6 supplies the primitive and the fallback rule; **[R]**
   the product API and typed receipt are new implementation work.

---

## F. What I did not find, and limits

I found **no** selected text that: expands `<installRoot>` to a location; authorizes any ingress to
create I; defines "persistent first-write" as a distinct concept from the durable-write class; or
defines a durability base case for a created ancestor chain. Those four are genuinely open and are
the substance of RF-1 and RF-2. What I *did* find late (B6/B7) is that selected law already
**depends** on `<installRoot>`, and that an unselected owner already proposes both its location and
a creation sentence — so two of the four are closer to a selection decision than to new drafting.

Method note: my first pass searched only the 46 selected inputs, which answered "is it selected?"
correctly but let me overstate "it exists only in product code". A broader background search,
completing after the first draft, found the unselected host-foundation family. B5–B7 are the
corrected result; I have left the correction visible rather than rewriting the note silently.

Limits: authority set was the 46 selected lock inputs plus accepted contract successors; I did not
audit unselected trials, historical drafts or the m1 corpus, and unselected references named here
(S9.3, `store-instance-lineage.v1.json`, root's 215 successor, the 224 creator draft) remain
unselected and are labelled as such. Anchors are line numbers at architecture `cd753cc02`; a later
commit moves them. Product citations are at `cd5af4d`. No native behaviour, custody, filesystem or
qualification claim is made or implied, and nothing here accepts, selects or pre-approves 392.

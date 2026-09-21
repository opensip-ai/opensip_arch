# Independent review — revised initial-root publication and ordinary binding owner (392)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Bounded owner/reference review only.

**Top verdict: NEEDS-CHANGES.**

This is not a rejection and not a re-litigation. **All four of my 390 required findings are closed**,
three of them by surgical byte-level edits I verified against my retained 390 copy rather than by the
author's account. The creator predicate is now positive, ordered and — as I found by checking three
selected sources the draft does not cite — materially better grounded than the draft itself claims.

NEEDS-CHANGES is for three concrete decisions that are still missing, all at the seam between this
owner and **selected** law. One of them is the question root asked directly, and the answer is yes:
there is a remaining concrete conflict with the read-only surfaces, and it should not be closed by
broadening their permissions.

---

## 1. Verification

### Archive

Both pins were checked **before** extraction, and extraction went only into this review directory.

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/trials/initial-root-binding-proposal-392/subject.tar.xz` | 28 752 B, `9f63c9f0116f5ee7bd739802aa433841d1e72b697c1a4318ab3fdaf370f9a11d` | identical | ✓ |
| `…/trials/initial-root-binding-proposal-392/subject.json` | 4 488 B, `449b822a3e3c216a36b4dad1463afa7927f4267f58b689455ad3a3ce6453294e` | identical | ✓ |

**29 / 29 members** verified byte-for-byte and by sha256 against the manifest before any file was
written: 0 missing, 0 extra, 0 mismatched, 0 unsafe (no symlink, hard link, absolute path, `..`
component or non-regular member). Record in `evidence/archive-verification.json`.

### Source anchors, and the code-anchor provenance question

**33 / 33 anchors match live bytes.** All 13 product anchors *additionally* match
`git show cd5af4d:<path>`, so each is verified both ways (`evidence/source-anchor-verification.json`).

On the provenance point root raised — I am reporting it explicitly as asked:

- **Runtime31 / source393 is not integrated.** Product HEAD is `cd5af4d`, the tree is clean, and
  `crates/platform/src/filesystem.rs` is **73 907 B / `9a02dcbb…` both live and at `cd5af4d`**. So at
  this review the anchor is simultaneously a historical code anchor and the live file; no substitution
  question arises today.
- **If 393 is integrated later, the distinction becomes real and the anchor still holds.** From my own
  393 review, the 393 delta touches exactly two files, and the `filesystem.rs` diff is **purely
  additive — 166 added lines, 0 removed and 0 modified**. `lib.rs` is not a 392 anchor. So a future
  integration would change this anchor's bytes while leaving **every existing line, including the whole
  directory-barrier implementation `sync_directory`/`directory_barrier_with`/`fsync_directory`,
  unchanged**. The 392 pins must not be edited, and a later live divergence on this one path is a
  disclosed forward change, not an unpinned substitution.
- I did **not** re-verify 393 here, and its ACCEPT-DESIGN-UNIT verdict keeps its own standing.

### Selection status of every architecture anchor — checked, not assumed

This matters for severity: a conflict with a selected document is different in kind from a tension
with a proposal.

| Anchor | Status |
|---|---|
| `security-and-lifecycle.md` | **SELECTED** — `design-lock.json` `/inputs/44`, pin matches lock |
| `identity-and-evidence.md` | **SELECTED** — `/inputs/42` |
| `security-completion.v8.md` | **SELECTED** — `/inputs/1` |
| `command-inventory.v3.json` | **SELECTED** — `/inputs/23` |
| `store-instance-lineage.v1.json` | lock input `/inputs/39`, but its own standing is "Proposed minimal successor delta… Not an accepted amendment", and S9.3 is "successor; proposed, not accepted" (security-and-lifecycle.md:953) |
| `project-registry-owner-selection-v2/successor.json` | **SELECTED** — `/contractSuccessors/48/record`; `owner.md` and `physical-placement.json` are candidates of that successor, so selected through it |
| `native-runtime-selection-v29/successor.json` | **SELECTED** — `/contractSuccessors/50/record` |
| `host-foundation-completion.v2.md` | **unselected** |
| 390 trial, 391 probe, my 390 findings, my 392 audit | **unselected** |

§1b's phrase "superseded **proposed** passages" is therefore exactly right, and I withdraw the
objection I was forming: host-foundation-completion.v2 is a proposal, and §1b restates the location
in its own words rather than incorporating by reference, so the new owner is self-contained.

### Replay

All three author scripts regenerate their frozen outputs **byte-identically**:

| Check | Result | Frozen output reproduced |
|---|---|---|
| `check_preinstallation.py` | PASS 54 cases | `preinstallation-checks.json` identical |
| `check_publication.py` | PASS 36 cases | `publication-checks.json` identical |
| `check_digest_compatibility.py` | PASS 7 vectors / 9 shape refusals | `digest-compatibility.r1.json` identical |

The digest script needs `jsonschema`, which the default interpreter lacks; I ran it under
`/tmp/opensip-implementation/source-audit364-env/bin/python` (3.12.13, jsonschema 4.25.1), the same
substitution I disclosed in 390. The canonicalizer sources are the pinned ones.

**The carried-forward claim is true, and I checked it against my own retained copies rather than the
manifest**: `publication_model.py`, `check_publication.py`, `check_digest_compatibility.py`,
`lineage_probe.rs` and `run_lineage_probe.py` are **byte-identical to the 390 artefacts**. The
lineage-carry-forward note is honest: those seven checks are carried historical evidence, and my own
390 rebuild of them remains the independent record.

### What actually changed since 390

Diffed against my retained 390 draft (`evidence/owner-draft-390-to-392.diff`): **8 lines replaced,
29 added, in five regions**. §§4, 5, 7 and 8 are **byte-unchanged**. That is worth stating plainly,
because it means §5 — the subject of root's question — is carried text, not new text.

---

## 2. Are RF-1…RF-4 actually closed?

### RF-2 — closed, and verifiable by deletion

My 390 finding was that "…continue up to the already admitted durable ancestor" had no base case. That
exact sentence is **gone from the file**. It is replaced by §3's named base (`H`, the native-account
home, which "must already exist; this act never creates H or any ancestor of H") plus a finite
base-to-leaf algorithm: barrier on H, then each of `Library`, `Application Support`, `OpenSIP` with
**both** its own and its containing-parent barrier, "whether it was newly created, already existed or
returned EEXIST". There is no recursion left to underspecify. **Closed.**

Probe R10 confirms the model refuses a missing H before any `mkdir`, with zero effects and zero
ancestors created.

### RF-3 — closed in the text; the evidence covers half the act

"the creating invocation's authoritative budget" — the phrase I flagged as asserting an owner that does
not exist — is **gone**. §2 now names `InitialInstallationAttempt`, allocated by the host's durable
ingress **before account/path capture or any creation-related filesystem work**, owning one
`CreationBudget`, the failure latch and the receipt lineage; process/invocation-scoped; "neither stored
in I nor obtained from C, a project namespace, the registry or a reference-model caller". Caps are
fixed at 65 536 objects / 131 072 edges / 268 435 456 bytes with a 4 MiB per-record ceiling, charged
before action, with no wrapper/subtree/retry/phase reset. **Closed as a design decision.**

The bound arithmetic checks out: probe R9 shows `components=252` admitted and `253` refused, and
252 + `Library`/`Application Support`/`OpenSIP`/`preview-v1` = 256 — which is exactly
`installation_root.rs`'s existing `MAX_COMPONENTS: usize = 256` and its comment "The four fixed
children count against the same limit."

The evidence does not reach as far as the text: see N-6.

### RF-4 — closed

The one-line row "Power loss leaves I absent | Eligible new creator can start anew" is replaced by a
row that states surviving fixed ancestors and staging explicitly, plus a new paragraph: "Creating fixed
ancestors is a durable side effect even if I is never published. Failure does not promise a pristine
filesystem or remove empty ancestors." **Closed.**

### RF-1 — closed, and better supported than the draft claims

§1a is a genuine positive ordered conjunction — `CreationIntent` → `InitialActor` → `InitialCore` →
`InitialPlatform` → `InitialParentPreparation` → `InitialCreationPermit` — with each step's original
owner named and a single-consumption permit at the end. That is what I asked for. **Closed.**

Two things I verified that the draft does not use, and should:

**(a) The command set is derivable from a selected field.** `command-inventory.v3.json` (SELECTED)
carries `authority` with exactly three values. `authority == "authoritative-default"` holds for exactly
**five** commands: `default`, `analyze`, `fit`, `audit`, `repair-verify`. The draft admits the first
four and excludes `repair-verify` because it "requires an existing retained repair attempt and cannot
bootstrap a new installation" — a structural reason I checked and accept (`opensip repair verify
RECEIPT-ID`, `steps: ["verify","render"]`). So the draft's set is not an enumeration of taste; it is a
selected predicate minus one member for a stated reason. Selected S7's command→lease map independently
groups the same commands: the **APPEND-WRITE** row names "`opensip` default, `analyze`, `fit`, `audit`
… `repair verify`".

Note the discriminator is `authority`, **not** `firstSourceWrite`: ten commands carry
`firstSourceWrite: true` (`default`, `analyze`, `fit`, `audit`, `import`, `baseline-upgrade`,
`repair-apply`, `repair-verify`, `test-run`, `native-prepare`). That distinction is load-bearing and
produces finding B-3 below.

**(b) The draft understates its own footing.** §1a calls extending the first-write effect to `fit` and
`audit` "an explicit choice of this owner". Relative to *identity §5* that is fair — identity §5 names
only "Default `opensip`/`analyze`" as DURABLE_AUTHORITATIVE. But two other selected sources already
group `fit` and `audit` with them. Presenting the rule as a reconciliation of three selected sources is
both stronger and more durable than four hard-coded names. See N-2.

---

## 3. Root's question: the existing-root durability confirmation versus read-only surfaces

Asked directly, so answered directly. **There is a remaining concrete conflict, in three parts.** The
first is resolved in the draft's favour but stated too weakly; the second and third are open.

### 3.1 The fence is not the problem — the barrier is

I expected the blocker to be the exclusive fence. It is not. Selected S7's command→lease map places
`doctor` / `trust doctor` / `store status` in the **"none (fence only, no project lock)"** row, and
`query`, `recommend`, `baseline show`, `policy show|test`, `candidates`, `inspect`, `review brief`,
`repair preview`, `agent serve` reads in **SHARED-READ**. Every one of them takes the Level-0 fence.
So §5's first conjunct — "hold I's same stable installation fence" — is satisfiable by all of them.

The blocker is the second conjunct. Selected security-completion.v8 **§5.6** says of the durability
primitives: *"These costs are paid only at operation boundaries and decisions (§3.3), **never by
metadata-only commands or doctor**."* And §3.3's doctor row is "Durable writes: **none**", "Must not
open: any file for writing under the install root".

So `doctor`, `trust doctor` and `store status` are **categorically barred by selected law** from
performing §5's reconfirmation. They satisfy half the gate and can never satisfy the other half.

§5 says "If an execution surface forbids even durability confirmation, it returns a
provisional/unavailable result rather than synthesizing that capability." That is the right answer —
but it is written as an open conditional, and the condition is already **settled** by selected §5.6.
This should be a determination that names those surfaces and cites §5.6, not an "if". See B-1(a).

For the record, an fsync on a directory fd is not itself a §3.3 violation: it opens no file for writing
and the I-parent is not under the install root. §5.6's cost-scoping sentence is what forbids it, not the
"must not open" column.

### 3.2 `query` and the SHARED-READ set are genuinely undetermined — the open conflict

§3.3 defines exactly **three** command classes: metadata-only, doctor, operation (`analyze`, `install`,
`remove`, `update-index`, trust refresh). `query` is in none of them. Neither are `recommend`,
`candidates`, `inspect`, `baseline show`, `policy show`, `repair preview`, or `repair recover`'s
inspection mode. §5.6 scopes the costs *by §3.3 class* and names only "metadata-only commands or
doctor" as forbidden — so for `query` the primitives are neither authorized (no §3.3 class, none of
§5.6's seven named boundaries applies) nor forbidden.

Now put §392 on top. §5 makes the reconfirmation a precondition for "producing a durable
installation/binding capability", and §7 runs ordinary binding "**under one admitted installation
fence** and shared operation budget". A `query run.show` must locate the selection pair, the endpoint
marker and the node — §7's binding. So:

- **Reading A** — a query produces no *durable* capability, the gate does not apply, and query binds
  without it. But §7 states no read-only binding path, so this reads the gate out of §7 by implication.
- **Reading B** — the gate applies, query cannot pay the cost, and query is permanently provisional.
  That contradicts `query`'s own selected goldens (`query-latest-empty` → request-rejected, remedy "run
  an analysis first"; `query-completeness-unmet` → indeterminate) and its parity fields
  (`total-items`, `truncated`, `query-response`), which all presuppose real results.

Two competent implementers land on opposite sides. This is the concrete conflict, and it must be
decided in the text rather than resolved at implementation time by quietly letting read-only surfaces
pay the barrier cost. See B-1(b).

### 3.3 `doctor` has no channel in which to report the new state — the sharpest consequence

§4 introduces a third admission state: **visible complete, durability unconfirmed**. §6's table sends a
process arriving after creator death to "Fresh existing-root admission and exact root/parent durability
gate". `doctor` is exactly such a process, and it may not run that gate.

`doctor`'s selected parity fields are `report-produced`, `outcome`, `defects-found`, `defects`,
`offline-window`, `termination-class` — **there is no `capability-availability` or `availability`
field**, and the renderer parity rule requires printing every parity field "verbatim or by a documented
fixed label". By contrast `query` *does* have `availability`
(`/queryResponse/context/availability`), and `default`/`analyze`/`fit`/`audit` all carry
`capability-availability`.

So the one new failure mode this protocol creates has, on the only selected diagnostic surface, no
declared rendering channel — while `doctor`'s own golden `doctor-report-not-producible` (remedy: "check
permissions on the private store root") tells users doctor is where you go to diagnose the store root.
Either the provisional state is declared to belong in `defects`, or a parity field is added — which is
a change to a selected inventory and must be named as such. See B-1(c).

Unselected host-foundation-completion.v2 §1 already contains the right precedent sentence — "Read-only
commands report absence without creating it" — and §392 should cite it when making this determination.

---

## 4. Other concrete missing decisions

### B-2 — at first creation, the backup-custody remedy set collapses to one option, silently

Selected S3.1 (security-and-lifecycle.md) joins identity §5 as an admission step: when the storage root
is `BACKED_UP`, the first source-derived write needs an explicit choice **in this order**: `--ephemeral`;
`--allow-backup-custody` for this invocation; or an already-admitted host storage-policy record. CI
never prompts and refuses `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`.

Under §392, at first creation:

- `--ephemeral` is **excluded by §1a** — ephemeral analysis cannot enter the creator.
- the **host storage-policy record has no home**. §1b explicitly declines the older proposal's
  "mutable settings files" (`settings.json`, `policies/permission-policy.json`), and §2's complete
  initial tree is exactly fence / registry / marker / node / pair / trust publication + `state.v1`.
  There is nowhere for an admitted storage-policy record to live before I exists.
- `--allow-backup-custody` survives. It is on `default`/`analyze`/`fit`/`audit` in the selected
  inventory, so it works.

Exactly one of three remedies survives, and §1b additionally removes the inventory golden's prose
remedy "select another admitted root" by forbidding every override. `~/Library/Application Support` is
inside the default macOS backup scope for many users. The consequence — on a `BACKED_UP` macOS home in
CI, installation creation requires `--allow-backup-custody` on the very first invocation — is a
defensible decision, but §392 never states it, and §1a step 5's "still follows the existing storage
policy" implies a policy route that structurally cannot exist yet. (`UNKNOWN` status still admits with
a mandatory disclosure, so this bites only on positive `BACKED_UP`.)

### B-3 — what a non-eligible first-write command does when I is absent is undefined

Five selected commands carry `firstSourceWrite: true` but `authority: none` — `import`,
`baseline-upgrade`, `repair-apply`, `test-run`, `native-prepare` — and S7 places them in APPEND-WRITE
or EXCLUSIVE. §1a correctly refuses them the creator role. But §6's disposition table has **no row for
"I absent, invocation not eligible to create"**: its only `I absent` row begins "Eligible new
invocation may create its own fresh stage." §1's exclusion list says they "cannot enter" the creator;
it does not say what they return.

This is one table row, but without it five selected commands have undefined behaviour on a fresh
machine, and the natural wrong answers (silently run ephemerally, or create I anyway) are both things
this owner exists to prevent.

---

## 5. Reviewer probes

Twelve adversarial probes I wrote against the frozen model bytes — not the author's cases. Full output
in `evidence/reviewer-probe-392.txt` and `evidence/reviewer-probe-392.json`.

| Probe | Result |
|---|---|
| R1 one absence → two stages? | refused ("foreign or out-of-order receipt"); single consumption holds — via the session phase, not a modelled permit object |
| R2 can a receipt be minted directly? | **yes** — a hand-built `Receipt(owner, INGRESS)` is accepted. Model privacy is nominal, as its own docstring says |
| R3 disclosure ↔ target cross-check? | **absent** — `ingress()` takes a bare `disclosed` boolean; `home()`/`parents()` never reference it |
| R4 K derivation? | **absent** — `launch()` has `core_supports_initial` only; no `K`, no writer/decoder distinction |
| R5 does the budget reach publication? | **no** — `publication_model` contains no `budget` at all |
| R6 rival wins after the absence observation | stage allocation still proceeds — **faithful** to §1a step 6 |
| R7 two concurrent creators on ancestors | serialised; the second reconfirms as §3 requires; simultaneous mkdir/EEXIST inexpressible |
| R8 does any refusal latch the act? | **yes** — a zero-cost call after a refusal returns "closed budget"; faithful to §2, and stricter than 390's model in the right direction |
| R9 256-component arithmetic | 252 admitted, 253 refused — matches §2 and `installation_root.rs` |
| R10 can a missing H be created? | refused before any effect; `effects=[]`, `ancestors=[]` — faithful to §3 |
| R11 do the two models compose? | **no** — the preinstallation model has no rename/publish method and never sets `world.root` |
| R12 ingress command set | `default`, `analyze`, `fit`, `audit` admitted; all others refused — matches §1a, but hard-coded rather than derived |

R6, R8, R9 and R10 are the reassuring ones: the model is faithful on the subtlest points, including the
one that looks like a bug and is not (R6).

### Independently verified claims about the live product

- **`NativePlatformEvidence` really does require a fence.** `native_platform.rs:27` is
  `pub(super) struct NativePlatformEvidence<'f> { fence: &'f SuppliedInstallationFence, … }`, doc
  comment "under a borrowed supplied installation fence". §1a step 4's disclosure — that this factory
  "is NOT this pre-installation producer" — is accurate and load-bearing, and it is the strongest
  single sign the draft is not pretending an implementation exists.
- **The provisional per-hop marker walk is still per-hop.** `installation_lineage.rs:81-82` calls
  `ProvisionalStoreMarker::read_existing(fence, key.store_instance())` inside the hop loop. §7's
  endpoint-only amendment does contradict it, and §7 says so.
- **The creator delegation §1a claims to fill is real and selected.** registry-v2 `owner.md` line 9:
  "Existing operation owners must supply authorization for installation, first-write, explicit
  recovery, move, fork, adoption and retirement. Their absence is not permission to invent a CLI
  surface or initialize on an ordinary read." Line 33: "Only the separately authorized pristine
  installation creator can publish the initial empty registry."

---

## 6. Required findings

### Blocking

**B-1 — decide the read-only surface interaction; do not resolve it by broadening permissions.**
Three sub-parts, all in §5:
(a) Replace the conditional "If an execution surface forbids even durability confirmation…" with a
determination: cite selected security-completion.v8 §5.6 ("never by metadata-only commands or doctor")
and name `doctor`, `trust doctor` and `store status` as permanently provisional for installation
durability. State that the fence is *not* the blocker (selected S7 gives them the fence).
(b) Decide whether §7's ordinary binding under the fence requires §5's gate for the SHARED-READ
surfaces (`query`, `recommend`, `candidates`, `inspect`, `baseline show`, `policy show|test`,
`repair preview`, `repair recover` inspection, `agent serve` reads), which have **no §3.3 class at
all**. Either state a read-only binding path that does not require the gate, or accept that these
surfaces are provisional and reconcile that with `query`'s selected goldens and parity fields. Silence
here is resolved at implementation time by letting read-only surfaces pay barrier costs selected §5.6
does not authorize.
(c) Say where a `visible-complete-durability-unconfirmed` installation is reported on `doctor`, whose
selected parity fields contain no availability channel. If the answer is `defects`, say so; if it needs
a parity field, name that as a required change to a selected inventory.

**B-2 — state the first-creation backup-custody consequence.** Of selected S3.1's three choices, only
`--allow-backup-custody` is available at first creation: `--ephemeral` is excluded by §1a and the
host storage-policy record has no home in §2's tree. Say this, and say whether a first-creation storage
policy is intended to become possible later.

**B-3 — add the missing disposition row.** "I absent; invocation carries `firstSourceWrite` but not
`authority: authoritative-default`" (`import`, `baseline-upgrade`, `repair-apply`, `test-run`,
`native-prepare`) → state the exact result. Today §6 covers only the eligible-creator case.

### Non-blocking

**N-1 — `selected registry-v2 §3` does not resolve.** registry-v2 `owner.md` has named, unnumbered
sections and contains no `§3`; the delegation is in its third paragraph (line 9) and in "Registry
snapshot and first-use observations" (line 33). A document that demands "Formal reconciliation must
identify these exact superseded proposed passages" owes resolvable anchors itself.

**N-2 — state the ingress rule, not the list.** Cite `command-inventory.v3.json`
`authority == "authoritative-default"` (exactly `default`, `analyze`, `fit`, `audit`, `repair-verify`)
and S7's APPEND-WRITE row, then exclude `repair-verify` for its stated structural reason. Note that
`firstSourceWrite` is **not** the discriminator. This converts a discretionary "explicit choice of this
owner" into a reconciliation of three selected sources, and stops the set silently diverging if the
inventory gains a sixth authoritative-default command.

**N-3 — label the new disclosure content.** Identity §5 requires reporting retention origin DEFAULTED
and durable-unbounded posture; it does **not** require the disclosure to identify the storage root.
§1a step 1 adds that, and step 5 makes it load-bearing ("The initial storage-root disclosure must match
this actual account-derived target"). Mark it NEW, as §§1a/1b/2/3 mark their other new law.

**N-4 — §392 extends §5.6's boundary set, not only its ordering.** §2 says the new law is "their
required ordering, owner retention and scoped receipts, not a new flush vocabulary". True of the
primitive; but §5.6's **Boundaries** list (witness write, `evalHighWater` write, journal append,
quarantine marker, SC-TRUST high-water copy, lifecycle publication, selection commit) does not include
the H barrier, the per-ancestor directory+parent barriers, the stage-internal barriers, the post-rename
I-parent barrier, or §5's existing-root reconfirmation. Since §5.6's boundary list is what scopes which
commands pay, the extension must be explicit — it is the same text that decides B-1.

**N-5 — §9's obligation list is narrower than the body.** §1a step 4 identifies a distinct
pre-installation platform producer that must not require a fence (verified against
`native_platform.rs`), and §3 requires a qualified profile premise that the account-home base "remains
durably reachable". Neither appears in §9's list, which is the list that will be actioned.

**N-6 — disclose the model undercoverage that is material.** The README discloses no native
unforgeability and no complete P0 construction. It does not disclose: the budget does not exist in the
publication half (R5), so §2's "final rename and ordinary handoff" charge is unevidenced; the step-1 ↔
step-5 disclosure match is unmodelled (R3); K derivation — the exact writer/decoder confusion §1a step 3
warns about — has no coverage (R4); and the two models never compose across the permit → stage → rename
seam that step 6 authorises (R11).

---

## 7. What I am not saying

- Not that the direction is wrong. It is right, and RF-1…RF-4 are genuinely closed.
- Not that my 390 or 392-audit recommendations are accepted by root; they are not, and this review does
  not treat them as such.
- Not that any disclosed native obligation is delivered. Creator eligibility, the fence-free platform
  producer, directory publication and barrier primitives, shared budgets, the qualified project-root
  producer and current authority all remain unimplemented, and the models supply them as premises.
- Not a formal passage reconciliation, a successor, or assent.

---

## 8. Limits

- **Level:** document and model reading, archive/anchor verification, model replay and probing.
- **No native tests were run for this review**, as instructed; none was needed, and I coordinated
  nothing with root's serial native work.
- **Not qualified:** native eligibility producers, actor/custody/profile qualification, exclusive
  directory rename, directory barriers, crash and power-loss behaviour, GC, Linux, release.
- **Not re-verified here:** runtime31/source393 (separate unit, separate verdict), the 391 native probe,
  runtime30, registry-v2 and inventory58 on their merits.
- **Unselected references remain unselected:** S9.3 and `store-instance-lineage.v1.json`'s proposed
  delta, `host-foundation-completion.v2.md`, `reference-architecture.v2.md`, the 390/391 trials, my own
  390 findings and 392 audit.
- **Replay caveat:** the three checks run the author's scripts, so they establish reproducibility and
  internal consistency. The independent parts are the byte-identity comparison of the five carried
  artefacts against my own 390 copies, the 390→392 diff, the selection-status determination, the
  live-product verifications in §5, and probes R1–R12.
- The seven supplied-lineage checks were **not** rerun here and are not claimed as rerun; my 390
  rebuild remains the record.

---

## 9. Context HEADs — sampled at the END

Byte pins, not head labels, are the authority; the labels are context.

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `613d3c7a85b8726e4d27cbea9805c29484dd70dd` | "Resolve initial creation review gaps and freeze directory barrier candidate" | 2026-09-21T14:53:01-07:00 |
| product | `cd5af4dbf524b81ac98876029798d569ccdc0052` | "Capture native project paths without relaxing internal name rules" | 2026-09-21T14:25:22-07:00 (clean) |

All four 392 trial files re-pinned at the end are unchanged and their committed blob ids equal their
worktree blob ids. Product remains `cd5af4d`, so runtime31/source393 is confirmed **not integrated** and
the 392 product anchors are simultaneously historical and live.

---

## 10. Attestation

Read-only against live, frozen, history, product and lock. No architecture, product, frozen, history or
lock byte was edited; no 392 pin was touched. No commit, no push. All writing went into this review
directory; extraction went only there. The immutable 390 report, its findings, its hashes and the
runtime31/source393 report are untouched and keep their own verdicts.

This grants no root assent, no formal selection, no passage reconciliation, no native writer or current
authority, no S9.3 or 215 adoption, no M2 completion and no release qualification.

Reviewer: Claude Opus 5 (1M context).

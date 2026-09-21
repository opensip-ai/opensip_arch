# Native store binding 388 — independent owner-resolution investigation

**Model/capacity.** Performed as Claude Opus 5 (1M context). Capacity was available; this is
substantive work. Earlier Fable-quota refusals in this series were refusals, not reviews, and
nothing below relies on them.

**Standing.** Investigation only. **Not** ACCEPT-DESIGN-UNIT, not source acceptance, not S9.3
selection, not root assent, not approval of Grok 387. Read-only: no product, frozen, history or
lock bytes were edited; no commits, no pushes; no native suites run. All output is confined to
this directory. Exact pins: `evidence/source-pins.json`.

---

## 0. What I verified before reasoning

The four `input-pins.json` entries of trial 387 all match the live arch files byte-for-byte
(`security-and-lifecycle.md` a319da39…, `store-instance-lineage.v1.json` 919d1717…,
registry-v2 `successor.json` cf91319a…, runtime-v29 subject 02d69e6b…). Arch HEAD `55d0f68a2`,
product HEAD `526a186`. Grok's three preserved 387 drafts match its own recorded hashes.

I re-derived every load-bearing claim from the sources rather than from Grok's report. Where I
agree with Grok I say so and add the evidence; where I differ I say so explicitly (§3, §5, §7).

---

## 1. Standing of the inputs — traced three ways, not from headings

Root's instruction was not to infer acceptance from membership or rejection from a heading. So
each item below is traced through (a) the selected `design-lock.json`, (b) application46, and
(c) the document's own text.

| Item | In design-lock? | In application46? | Own text | Standing I rely on |
|---|---|---|---|---|
| registry owner v2 | **yes** — `contractSuccessors[48]`, assent `project-registry-owner-selection-v2-unit.json` `status: ACCEPTED-DESIGN-UNIT`, `rootSubstantiveAssent: true`, `requiredUnitFindings: []` | — | successor's own `standing` still reads "PROPOSED" | **SELECTED** (lock + per-item assent override the stale self-description) |
| S9.3 store-instance lineage | **no** contract successor references it | not a separate item | `security-and-lifecycle.md:953` "(successor; proposed, not accepted)" | **PROPOSED** |
| `store-instance-lineage.v1.json` | **no** | **yes**, `files[191]` — but `implementationAuthorized: false` | own `standing`: "Not an accepted amendment… Requires its own substantive review on newly frozen bytes" | **PROPOSED** — file applied, law not accepted |
| `StoreGenerationBindingV1` five-field | **no** | — | build plan 240–269 freezes the shape and states "**Current S9 cannot express this validation, and this proposal does not pretend otherwise**" | **PROPOSED** |
| physical locators `selection.pair`, `stores/S/store-instance.v1`, `transitions/lineage/S/G/K.node` | **no** | — | named only in 387 draft + product code | **NOT SELECTED** (387 draft says so itself) |
| runtime29 codecs | **yes** (`native-runtime-selection-v29`) | — | — | **SELECTED as inert codecs**, not as binding law |

The application46 row is the important one: `store-instance-lineage.v1.json` **is** a member of a
FROZEN FINAL APPLICATION CANDIDATE whose `implementationAuthorized` is **false**. File membership
placed the bytes in the tree; it accepted no law. This is exactly the inference root warned
against, and it is the only place where "the file is in the repo" could be mistaken for selection.

**Consequence used throughout:** there is today no selected owner for installation creation, for
store-root publication, for lineage node admission, or for five-field binding admission.

---

## 2. The value circularity is already broken by existing law (agreement, with evidence)

I independently confirm Grok §1. The relevant facts are in the product, not only in prose:

- `crates/security/src/generated/trust_record_shape_nodes.rs:1624-1636` — `CreationStoreBindingV1`
  (`node_163`) admits **exactly** `{stateSchema, storeGeneration, storeInstanceId}` and nothing
  else. No namespace member exists to fill.
- `:1640-1642` — `node_165` requires `storeGeneration` to be an integer **equal to 0**. G=0 is not
  a default; it is the schema. A restored store at G≠0 is unrepresentable here.
- `crates/identity/src/store_selection.rs:66-68` — the selection codec admits any `G ≥ 0`, i.e. the
  pair is strictly wider than creation. The pair therefore cannot be used to infer that a creation
  happened.
- `crates/security/src/trust/native_current.rs:129` `capture_head(…, expected_store)` and
  `:184-185` `if object(record.value())?.get("store") != Some(expected_store) { Err(Error::Store) }`
  — current C is **compared** against a caller-supplied expected binding. It is a comparison sink,
  never a source of G/K, and a missing `state.v1` is a capture error, not an initialization signal.

So the "where do G/K/N come from" question needs **no new schema**: at install they are a typed
declaration of the creating act (S, G=0, K); N does not exist yet and must not be invented; the
five-field view is derived only after a registry ACTIVE row exists. Registry-v2 `owner.md:33`
independently forbids the shortcut: "Only the separately authorized pristine installation creator
can publish the initial empty registry; directory emptiness alone is not proof of a pristine
installation." Root's own assent text for that unit says "**no migration or inferred pristine
creation**".

**That is the part Grok got right, and it is settled.** It is not the blocker.

---

## 3. The blocker is the *act* circularity, not the value circularity (primary finding, differs from 387)

Grok's §2 proposes five separate in-place durable writes and then tabulates the crash prefixes.
That skips the question root actually asked. Three independent facts make in-place installation
creation unadjudicable today:

**3.1 The installation fence cannot cover the creation of the installation.**
`crates/security/src/custody/installation_fence.rs:13` — `const CARRIER: &str = "lifecycle.fence"`,
a file **inside** the installation root, opened and locked through the retained root directory
(`:57`, `:122` name-match checks). Every selected ordering rule that says "under the installation
fence" (registry-v2 `owner.md:54`, `:60`; S9.2 journal law) presupposes an installation that
already exists. **The act that creates I is outside the only concurrency arbiter the system has.**
Grok's order never says what serializes two concurrent creators; "under the fence" is unavailable
by construction.

**3.2 There is no durable container in which to record the creator's intent.**
Registry-v2 solves the multi-step publication problem with a *self-describing intermediate row*:
`owner.md:60` "(1) durably publish RESERVED; (2) … (4) durably replace RESERVED by ACTIVE after
rechecking every original observation", plus `:62` "ABANDONED is the durable terminal record of an
allocation that never reached ACTIVE". That works because the registry **file already exists** to
hold the intermediate state. For installation creation there is no such container: the intent
"I am creating I with S=…, K=…" has nowhere durable to live *before I exists*. Every one of
Grok's five writes is a bare fragment that describes a value, not an act.

**3.3 The GC-orphan disposition Grok borrows is journal-bound and does not transfer.**
Grok's prefix table disposes of the marker-only case as "GC-class orphan if the enclosing act
aborted". The companion's own text (`store-instance-lineage.v1.json` → `abortedAttempts`) grounds
that disposition in the *transition journal*: "The retained evidence of a failed attempt is the
owner's own transition journal footprint in state ABORTED (A6)", and A6 is
`security-and-lifecycle.md:948` — a `recover_transition_journal` state-table disposition ("the
published generation was never selected; GC census reclaims it"). A lineage-root creating act has
**no journal, no intent and no ABORTED footprint** by the companion's own design
(`lineageRoot.obligations`: "selectedByIntentDigest is null because there is no admitted S9
transition intent"). The premise of the GC argument is absent in precisely the case Grok applies
it to. The companion is candid about the hole: `lineageRoot.whichActCreatedARoot` defers to
"installation.rs and backup.rs, **and by their own durable records**" — and
`crates/lifecycle/src/installation.rs` and `crates/storage/src/backup.rs` are **absent on disk**
with inventory58 standing `proposed` (verified independently; Grok's finding confirmed).

**3.4 No creator exists at all.** The only `publish_new_regular` callers in the product are in
`crates/storage/src/blob_store.rs:57,220`. Nothing writes a pair, a marker, a node or a current
capsule. This is not "installation.rs is a stub"; there is no creation path anywhere.

---

## 4. Direct answers to root's three questions

### 4.1 "Is publishing pair before current lawful, or does it require unavailable/quarantined recovery?"

**Neither order is lawful today, and the ordering is not the defect.** Both orders leave an
installation that no selected or proposed rule can ever resolve:

- **pair → (crash) → no current.** Ordinary read succeeds at the pair
  (`installation_records.rs:20-30` reads selection first, then the marker at the pair's S), then
  `capture_head` fails on `trust/stores/S/state.v1`. Correctly *unavailable*. But the installation
  is now permanently unusable: ordinary paths must never initialize (agreed), and a second
  creation act cannot proceed because the installation is demonstrably **not pristine** — a pair
  exists — and registry-v2 `owner.md:33` plus root's assent forbid inferred pristine creation.
  Nothing can complete it, nothing can retire it, nothing can adjudicate it.
- **current → (crash) → no pair.** Symmetrically unusable: `ProvisionalSelection::read_existing`
  fails first, so no store is selected; and again the root is not pristine.

So the honest answer is: publishing the pair before the current is **not** "unlawful"; it is
**unrecoverable**, and so is the reverse. Asking which of the five writes goes first is asking
which brick to lay first in a wall with no foundation. Any in-place order requires a *new
recovery owner* for every prefix, and that owner cannot authenticate anything (§4.2).

### 4.2 "How does a fresh invocation authenticate an interrupted creator's exact intent/identity?"

Under in-place creation: **it cannot, with the material available.** The candidate evidence is
exactly the fragments the creator wrote, and each fails as an authenticator:

- the pair and the node are *values*; they state S/G/K but assert nothing about who wrote them,
  when, or whether the act was authorized. They are equally consistent with an interrupted
  authorized creator, an abandoned one, a partially restored copy, and a hand-placed forgery.
- there is no namespace (empty registry), no journal (no transition), no current (that is the
  missing piece), and no fence (§3.1). Those are the four things the system normally uses to bind
  an act to an authority.
- `intentDigest` is unavailable by design, and the companion forbids inventing one
  (`lineageRoot.obligations`).

"Re-observe at the next fence" (387 draft, §Work required) is therefore **not** a protocol: the
next fence re-observes the same ambiguous fragments and reaches the same undecidable state, forever.
Root's characterisation is correct.

**The only two ways out**, stated as what they are:

- **(A) Make the intermediate states unobservable** — publish the whole initial root atomically, so
  the only states any observer can see are *absent* and *complete P0*. Then there is no interrupted
  creator inside I to authenticate, and the question dissolves. This is the recommendation (§7).
- **(B) Make the first durable write a self-describing creation record** — the analogue of
  registry-v2's RESERVED, plus an ABANDONED-class terminal record, plus an explicit recovery rule.
  This is strictly **new required law**, it needs its own authenticator (which, per the bullets
  above, does not exist for a pre-installation act), and it re-creates the adjudication problem
  registry-v2 solved for *rows* in a place where no container exists. I do not recommend it for
  first-root creation; it is unavoidable for the *second* creation act (§6).

### 4.3 "Exact predecessor FILE+PARENT durability obligations"

These exist today as **selected** law, but only for the registry, and they are stated as an
inherited obligation on every write:

- registry-v2 `owner.md:54`: "Before ANY registry write, independently confirm exact predecessor
  file and parent durability under custody; **prior-process success is not a substitute**. Publish
  complete canonical replacements via an admitted same-directory temporary file and atomic rename
  with required file/parent barriers. **Initial publication is no-replace.** A failed or uncertain
  barrier stops; it grants no blind retry, rollback, deletion or activation."
- `physical-placement.json` → `currentRegistry.mutation`: "Inherited atomic replacement with exact
  predecessor FILE+PARENT durability reconfirmation."
- The product implements the file half faithfully: `crates/platform/src/filesystem.rs:286-294`
  `publish_new_regular` = verify staged bytes → file barrier → **exclusive** no-replace rename
  (`:214-241`, `renameatx_np`/`RENAME_EXCL`, `renameat2`/`RENAME_NOREPLACE`, and explicitly **no
  overwrite fallback on ENOTSUP/EINVAL/ENOSYS**) → directory barrier. `EEXIST` is documented as
  "no publication by this attempt; it is not a duplicate-content or durability receipt".

**What is missing for creation**, precisely:

1. The obligation is written for *replacement of a file in an existing durable parent*. Creation
   publishes **directories** (`stores/S/`, `transitions/lineage/S/G/`, `trust/stores/S/`) and the
   root `I` itself. There is no directory-publication primitive in the product —
   `publish_new_regular` is regular-file-only — and no selected rule for directory barriers in a
   creation chain.
2. "Predecessor durability" for a *chain of first publications* is not the same obligation as for a
   replacement: each new parent must itself be durable in **its** parent before a child may be
   published into it, up to and including I's own parent. That ancestor-chain obligation is stated
   nowhere in selected law.
3. Nothing states the obligation at the *final* step — that I's own name must be durable in I's
   parent before any observer may treat I as an installation.

These three are **NEW required law** for whichever creation option is chosen.

---

## 5. Durable-prefix tables

### 5.1 In-place order (Grok §2) — every prefix is inadjudicable

Columns: what an ordinary invocation observes; what selected law says; and — the column 387 omits —
**who can ever resolve it**.

| # | Durable prefix | Ordinary observation | Resolver under selected law | Resolver under 387 proposal |
|---|---|---|---|---|
| 0 | nothing | no I | creator may run | creator may run |
| 1 | I + `lifecycle.fence` only | fence acquirable, no pair | selection read fails → unavailable | **none** — not pristine, cannot re-create |
| 2 | + marker `stores/S/store-instance.v1` | no pair | unavailable | **none** (Grok: "GC-class orphan" — but §3.3: no journal, no GC owner) |
| 3 | + node `transitions/lineage/S/0/K.node` | no pair | unavailable | **none** |
| 4 | + `selection.pair` | pair OK, marker OK, **current absent** | `capture_head` error → unavailable | **none** — this is root's question |
| 5 | + `trust/stores/S/state.v1` | complete | admissible | complete |
| — | pair present, marker absent | marker read fails (`installation_records.rs:22-27`) | unavailable | contradiction, no repair |
| — | node with G≠0 at install | — | not a creation root | refuse (agreed) |

Rows 1–4 are the finding: **four distinct durable states, all permanently unresolvable, and
mutually indistinguishable as to cause.** Adding a recovery owner for row 4 alone does not help;
rows 1–3 have the same shape.

### 5.2 Atomic root publication (recommended) — two observable states

| # | Durable state | Ordinary observation | Resolver |
|---|---|---|---|
| 0 | I absent; staging sibling absent or partially written | no I | creator may run; a *foreign* staging sibling is never adopted, resumed or deleted |
| 1 | I present (published by one exclusive no-replace rename after every contained object is durable) | complete P0 | ordinary admission |

There is no third state. Row 0's staging sibling is outside I, carries a name grammar that no
reader consults, and is never an input to admission — so it is not an "installation with a
prefix", it is debris. The exclusive rename is also the **concurrency arbiter** that §3.1 shows the
fence cannot be: two concurrent creators both stage, exactly one rename succeeds, the loser's
`EEXIST` is documented as "no publication by this attempt" and it re-enters ordinary admission of
the winner's root.

**What atomic publication still requires (new law, stated honestly):** a directory-publication
primitive with an exclusive no-replace directory rename; a rule that every file and every
directory inside the staging tree is durable *before* the rename; the parent barrier on I's parent
*after* it; a staging-name grammar; and the explicit statement that a leftover staging sibling is
never adopted or resumed by a later process. What it does **not** require: a creation journal, an
ABANDONED-class record, an intermediate-state authenticator, a per-prefix recovery rule, or any new
authority.

---

## 6. Four acts that must not be merged

Independently confirmed against `lineageRoot.creatingActs`, S9.3:1042-1048, and node_165:

| Act | S | G/K source | Lineage | Current | Container exists? | Owner status |
|---|---|---|---|---|---|---|
| First installation root | fresh | typed creation declaration, G=**0** fixed by `node_165` | new root, predecessor+origin null | `CreationStoreBindingV1` | **no** (I is being created) | none; recommend atomic (§7) |
| Same-S trust-capsule restore | **same** S | unchanged | **no** new node | replace/recover C under the existing triple | yes | trust-current publication owner, unspecified — **exclude** |
| New-S evidence restore / portable adoption | fresh | **that act's** declaration; may be G≠0, so `CreationStoreBindingV1` **cannot express it** | new root; marker in copied bytes **replaced** before first publication | not `CreationStoreBindingV1` unless that act independently declares G=0 | yes | none (`backup.rs` absent) — **exclude** |
| Forward COMMITTED transition | fresh | admitted intent target | one node, **after** durable COMMITTED | existing path | yes | S9.2 selected; S9.3 node rule proposed — **exclude** |

Row 3 is where widening `CreationStoreBindingV1` would be tempting and must be refused: `node_165`
is `n == 0`, so a restored G≠0 store cannot use it, and the fix is that act's own typed record, not
a weakened creation schema. Note the asymmetry that makes row 3 *harder* than row 1: its container
exists, so option (B) of §4.2 — an explicit RESERVED-analogue creation record — is both possible
and **necessary** there, because the atomic trick is unavailable for a new store inside a live
installation that observers are already reading.

---

## 7. Endpoint vs intermediate lineage

**7.1 The product defect is real.** `crates/host/src/installation_lineage.rs:82` calls
`ProvisionalStoreMarker::read_existing(fence, key.store_instance())` inside the per-node walk
callback, i.e. **once per hop**. After a lawful reclaim of an ancestor store X, a chain Y→X whose
X *node* is still retained fails on X's missing marker. Confirmed. The file is explicitly
provisional and read-only (`:1-3`, `:33-35`), so this is a **non-promotion constraint**, not a
current-law violation.

**7.2 But the "clarification" is an amendment, and that changes what can be selected.** S9.3:975-978
says: "Every lookup uses the whole triple, **whose instance component is read from the store-root
marker of the store concerned**". Read literally that requires a marker per hop — the product walk
implements S9.3 *as written*. The 387 draft calls the endpoint reading a "prospective
clarification"; it is not a clarification, it is a substantive amendment to unaccepted text. That
is permissible (S9.3 is unselected), but it has a consequence Grok does not draw:

**7.3 Ordinary five-field binding cannot be selected "without S9.3".** The chain is forced:
the binding needs G/K → G/K come from an *admitted* node → S9.3:994-1004 admits a node only if
"the chain from it is acyclic and reaches exactly **one** lineage root" → chain traversal → the
marker-per-hop sentence applies → post-GC ancestry breaks. So a binding owner that admits nodes
under S9.3's admission law inherits the very sentence it must amend. **Answer to root's question:**
no, ordinary binding cannot be coherently selected as a *partial* S9.3 subset. It can be selected
only as a **single self-contained law** that states node admission and traversal itself —
superseding, not partially adopting, the proposed text. (The alternative — dropping chain
reachability from binding-scope admission so only the selected node is checked — removes the
defence against duplicate/forged keys and multi-root components, and I do not recommend it.)

This is the concrete, technical reason for root's instinct that a chain of incomplete approvals is
wrong here.

---

## 8. Counterexamples

- **CX-1 (pair before current).** Creator writes marker, node, pair; power loss; ordinary read
  reports unavailable forever; no creator may re-run because a pair exists so the root is not
  pristine (`owner.md:33`). Installation bricked, no owner may repair it.
- **CX-2 (current before pair).** Symmetric; selection read fails first. Same outcome. Proves the
  defect is not in the *choice* of order.
- **CX-3 (marker only).** Grok disposes of this as a GC-class orphan. There is no GC owner for a
  store outside a transition, and the companion's own justification cites the journal ABORTED
  footprint (§3.3), which does not exist here. The orphan is permanent and blocks re-creation.
- **CX-4 (two concurrent creators, in-place).** No fence exists yet (§3.1). Both may interleave
  writes for **different** S under the same I; nothing arbitrates; the surviving prefix may mix two
  acts' fragments (e.g. A's pair with B's marker) and every field-level check passes individually.
  Atomic publication reduces this to one `EEXIST` loser.
- **CX-5 (post-GC ancestry).** Y selected; ancestor X's store lawfully reclaimed; X's node retained.
  Endpoint rule: chain readable, X not a rollback handle. Product walk: fails at
  `installation_lineage.rs:82`. Reports "unavailable" for a chain that is intact — a false negative
  that a later owner could mistake for corruption.
- **CX-6 (retained branch at equal numeric pair).** Two physically distinct stores present the same
  `(G,K)` (S9.3:955-958 is explicit that `store-rollback`/`core-rollback` cause this). A numeric-pair
  lookup or a "matching digest" shortcut selects the wrong store; only the full triple with the
  instance component from the *endpoint* marker plus the verified chain disambiguates.
- **CX-7 (restored G≠0).** Evidence restore materialises a store whose declared generation is 3.
  `node_165` requires 0. Either the act declares its own typed record (correct) or someone widens
  `CreationStoreBindingV1` (forbidden: the build plan freezes the five-field digest at v1 and the
  creation schema's `n == 0` is the only thing preventing a restored store from claiming to be a
  first installation).
- **CX-8 (same-S restore misread as a new root).** A same-S trust-capsule restore writes **no**
  node; if a binding owner treats "current replaced" as evidence of a creating act it will look for
  a root node that must not exist, or worse fabricate one — the v2 defect S9.3:1027-1030 names
  explicitly ("a missing one cannot be repaired from it and is QUARANTINE").

---

## 9. Required fixes to the 387 material (if it is carried forward)

| # | Item | Required change |
|---|---|---|
| R-1 | 387 FINDINGS §2 write order | Do not present five in-place writes as *the* order. Either adopt atomic root publication (§5.2) or add the creation-record + terminal-record + recovery owner in full. Publishing an order without a resolver for its prefixes is the defect, not the sequence. |
| R-2 | 387 prefix table, "GC-class orphan" | Remove or re-ground. Its justification is the transition journal's ABORTED footprint, absent for a lineage-root act (§3.3). |
| R-3 | 387 §2 "next fence re-observes" | Not a protocol. State explicitly that re-observation of an incomplete root is undecidable and that no owner exists to resolve it. |
| R-4 | 387 §2 "under the fence" implication | State that the installation fence is I-scoped (`installation_fence.rs:13`) and therefore unavailable to the act that creates I; name the arbiter that replaces it. |
| R-5 | 387 §4 endpoint rule | Label it an **amendment** to S9.3:975-978, not a clarification, and carry the §7.3 consequence: binding admission cannot be a partial S9.3 selection. |
| R-6 | 387 §5 adoption | Agreed and unchanged: exclude it. Add that its container **does** exist, so it needs the RESERVED-analogue that first-root creation can avoid. |
| R-7 | Both reports | `CreationStoreBindingV1` G=0 is `node_165`'s `n == 0`, not a convention — cite the product, so no later reader treats it as a default. |

---

## 10. Recommended next candidate — one complete bounded owner

**Name:** initial installation root publication and ordinary selected-store binding admission.

**Why one unit and not two:** §7.3 shows binding admission drags in node admission drags in
traversal drags in the marker rule; and §4 shows creation has no resolver unless its publication
model is decided in the same document. Splitting them produces two units each of which is only
sound given the other's unwritten half.

**In scope (must all be present for the unit to be complete):**

1. **Atomic root publication.** Complete initial root staged privately; every contained file and
   directory durable; one exclusive no-replace **directory** rename; parent barrier after. Explicit:
   only two observable states; a leftover staging sibling is never adopted, resumed or deleted by a
   later process; `EEXIST` is the loser's ordinary outcome and it re-enters ordinary admission.
   *(New law: names the directory-publication primitive and the ancestor-durability chain of §4.3.)*
2. **The typed creation declaration** as the sole source of `(S, G=0, K)` — no pair, node or C may
   mint any of them; N is not invented; the five-field view is not required to create C.
3. **Ordinary admission order** with N never derived from pair or C: registry ACTIVE N → pair
   locate → **endpoint** marker → node at the full triple → C.store three-field compare.
4. **Self-contained node admission and traversal**, superseding S9.3:975-978 for lookup: instance
   component from the endpoint marker only; ancestry by node key; nodes outlive store reclamation;
   missing node ⇒ unavailable; bounded, iterative, charged to the operation budget.
5. **Three-way marker observation** (readable / root absent / present-but-unreadable), with
   missing-leaf ≠ absent-root, carried from S9.3:983-992 as selected text of this owner.
6. **Explicit non-promotion** of `installation_lineage.rs`'s per-hop marker read (§7.1), named as a
   defect this owner forbids rather than a behaviour it inherits.
7. **Explicit negative clauses:** ordinary read failure never initializes; no repair of a missing
   node from an unrelated intent; no widening of `CreationStoreBindingV1`; no new journal member,
   H-domain, envelope kind, public command or caller-supplied scalar authority.

**Out of scope, each to its own later unit:** the S9.3 forward/same/ancestor transition-node matrix;
evidence restore / portable adoption (new lineage root in an existing installation — needs the
RESERVED-analogue, §6); same-S trust-capsule restore; writers and current-authority facade; shared
native budgets; native UUID/profile qualification; five-field digest compatibility proof.

**Explicitly flagged as NEW required law** (not pretending it exists): the directory-publication
primitive and its durability chain (§4.3); the staging-name grammar and never-adopt rule; the
supersession of S9.3's per-hop marker sentence; and — if root rejects atomic publication — the
entire creation-record/terminal-record/recovery triad of §4.2(B), which I do not recommend.

---

## 11. Limits of this investigation

Read-only; no native tests were run and none were needed — every claim is from source text or from
reading the product, and the two dynamic claims I would otherwise have to test (exclusive-rename
semantics on directories; directory barrier behaviour) are explicitly listed as **new law to be
specified and qualified**, not asserted as working. I did not review runtime29's code, source386,
the registry codec (383) or Grok's accepted reviews; I treat their acceptance as recorded, not as
re-verified. I did not re-derive the 46-member application subject. Standing determinations in §1
rest on the lock, application46 and the documents' own text as of arch `55d0f68a2` / product
`526a186`; a later lock changes them. No ACCEPT-DESIGN-UNIT, no root assent, no approval of the 387
drafts or of my own recommendation is expressed or implied.

# Owner/reference review 390 — initial-root publication and ordinary store binding

**Verdict: NEEDS-CHANGES** (bounded owner/reference scope).
**Subject:** `docs/implementation/m2/trials/initial-root-binding-proposal-390/subject.tar.xz`,
17424 bytes, sha256 `3cbd6b9668c4b27bd4583530139be45b7a58357762c9a1df53e3960faee63ddd`, 17 members;
manifest `subject.json` 2660 bytes sha256
`0754ee772c96509c1f925130c45c3cda00ab0b2b066ff39c057a0f262c424e73`. **All 17 members verified.**
**requiredFindings: RF-1 … RF-4** (§7).

NEEDS-CHANGES here is **not** a rejection of the direction. The protocol is a genuine advance on
387 and on my own 388, its concurrency and recovery arguments are sound, and all three evidence
sets replay exactly. It is NEEDS-CHANGES because three *design* choices are missing that two
implementers could not resolve the same way, one of which (RF-2) is an undefined recursion in new
law rather than a disclosed implementation obligation.

Reviewed as Claude Opus 5 (1M context). Read-only: no live, frozen, history or lock bytes edited;
no commits; no pushes. This grants no root assent, no formal selection, no native writers, no S9.3
adoption, no full M2 and no release, and it implies no earlier partial approval. The separately
accepted runtime30/389 unit is untouched and unaffected.

---

## 1. Verification

| Check | Result |
|---|---|
| Archive pin | 17424 B, `3cbd6b96…3ddd` — matches `archive-pin.json` and the request |
| Manifest | 2660 B, `0754ee77…4e73` — matches |
| All members vs manifest | **17/17** exact bytes and sha256; 0 missing, 0 extra, 0 mismatched |
| Unsafe members | none (no non-regular, absolute or `..` path) |
| Declared source pins | **19/19 verify against live bytes** in both repositories |
| Probe identity sources | 19 recorded files, **all identical to the live selected product** — the "unchanged selected identity source" claim holds |

Context: arch HEAD `42b5c52c2`, product HEAD `526a1867a34d…`.

## 2. Independent replay of the author evidence

All three sets were re-run from a private working copy; only script paths were adapted, and the
interpreters and inputs actually used are recorded in `evidence/`.

| Evidence | Result |
|---|---|
| 36 conditional publication cases | **PASS 36**; regenerated `publication-checks.json` **identical** to the frozen file |
| 7 canonical vectors + 9 closed-shape refusals | **PASS**; regenerated `digest-compatibility.r1.json` **identical** to the frozen file |
| 7 supplied-node lineage tests | **all 7 PASS**, output **identical** to the frozen `probe-run.stdout` |

For the lineage probe I did not reuse the author's artifacts: I built `opensip-identity` myself from
the **live selected product** (external `CARGO_TARGET_DIR`, `--locked --offline`, pinned Rust
1.95.0, repo left clean), compiled the byte-identical probe source (`e654fcfd…`) against **my own**
rlib (`d445dc4f…`, which differs from the author's `7b669c65…` only because build paths differ), and
ran it. Same seven results.

One environment note: `check_digest_compatibility.py` needs `jsonschema`, which the usual
`native-case15-reference-env` interpreter does not provide; I ran it under
`/tmp/opensip-implementation/source-audit364-env/bin/python` (3.12.13, jsonschema 4.25.1). The
canonicalizer sources themselves are the pinned ones.

## 3. What the proposal resolves — assessed, not assumed

**3.1 Concurrency is genuinely arbitrated.** The exclusive no-replace same-parent directory rename
is an arbiter that exists *before* the installation does, which is the property the installation
fence structurally cannot have (the fence carrier lives inside I). Putting `lifecycle.fence` in the
staged tree and holding its lock across the rename is the right move: the lock follows the inode, so
the winner holds a continuously-held fence from before publication until after its parent barrier,
and an ordinary entrant opening `I/lifecycle.fence` finds the same inode and is busy. The EEXIST
loser gets no receipt, does not compare S, does not merge, and re-enters ordinary admission
separately. The model enforces this (`concurrent-creators-AB/BA`, `creator-fence-blocks-…`).

**3.2 Recovery is resolved, and the reason is worth stating explicitly.** Because publication is
atomic, the *content* is always complete; only the *name durability* can be outstanding. So a later
invocation never has to authenticate a dead creator's intent — the problem I raised in 388 §4.2 —
it simply performs the parent barrier itself, which completes the one pending fact. My probe P8
confirms that a reader's own `confirm` makes the world durable, and P3/P1 confirm the capability is
per-invocation and non-transferable: a stolen receipt refuses, and global durability does not let a
later attempt skip its own gate.

**3.3 Root's correction of my "two-state durability" is right, and my 388 §5.2 was wrong on it.**
There are two structural *name* states but three *admission* states, because process death releases
the fence and exposes the complete-but-unconfirmed middle state. I under-modelled this by treating
the fence as if it survived the creator. The existing-root durability gate (§5) is the correct
response, and it is stronger than anything I proposed: it binds durability confirmation to the
invocation that will act, latches on uncertainty, and refuses to let prior-process receipts, fence
availability or valid-looking bytes substitute for it.

**3.4 The pre-existing-I and no-inferred-pristine-creation boundary is correct.** §1 requires a
positively observed absent final I name through an admitted retained parent and states that an
empty, partial, inaccessible, malformed or foreign I is never a creation target. That is the right
answer to registry-v2's "directory emptiness alone is not proof of a pristine installation", and the
model covers all eight `existing-partial-*-not-pristine` variants.

**3.5 The node/binding law is self-contained and the endpoint amendment is labelled as one.** §7
adopts the full-triple, both-null-or-both-nonnull, no-self, predecessor-exists, duplicate-refuses,
acyclic-to-exactly-one-root rules as its **own** law rather than importing S9.3, and explicitly
calls the endpoint reading a **NEW amendment** to S9.3's per-hop-marker sentence. That matches the
coupling finding in my 388 §7.3: this is the only coherent way to avoid a partial S9.3 adoption.
The probe demonstrates all seven properties against the *existing selected* identity walk, including
the provisional per-hop false negative, and §7 states the host walk must be replaced or stay
provisional.

**3.6 Digest compatibility is checked rather than assumed.** Old and current canonicalizers agree on
all seven vectors, field order does not change the canonical form, and the composed/decomposed pair
produces *different* digests — correctly, since the profile does not normalise Unicode. Those two
are flagged `nativeNamespaceGrammar: false`, which is the honest disposition: the generic schema
admits any 1..4096-character N while the native producer must supply UUIDv4 only.

## 4. Does it hide an authorization, budget or TCB gap?

Mostly it discloses them. Two are disclosed implementation obligations, one is an actual
specification hole, and one is an undisclosed side effect.

**4.1 Authorization — disclosed, but the predicate is missing (RF-1).** Every protection in this
unit is downstream of creator eligibility, and §1 defines it only as a *list of exclusions* plus the
phrase "the native first-party host's admitted persistent first-write invocation". The model supplies
`eligible: bool` (probe P6c). The draft is honest that a reference model's eligibility label is a
premise — but a list of what cannot enter is not a predicate an implementer can check. "Persistent
first-write invocation" is itself close to the caller-supplied notion the section forbids unless it
is derived from named owners in a stated order yielding a typed receipt.

**4.2 Budget — asserted against an owner that does not exist for this act (RF-3).** §2 says all
preparation, validation and publication share "the creating invocation's authoritative budget". The
authoritative budget in the existing design is operation/installation-scoped, and during creation
there is no installation. Nothing names the issuing owner, and nothing bounds the ancestor walk, the
tree validation or the P0 dependency construction. The model has no budget concept at all (P6b).
§7's "shared operation budget" applies to ordinary binding, where an installation exists, so it does
not cover this.

**4.3 TCB — honestly bounded.** §3/§4 require the qualified profile's exact primitives, forbid
overwrite fallback, refuse to infer portability from one host, and §6 disclaims whole-root
rollback/copy detection and trusted-code interference. That is the correct posture. The concrete
consequence to record: the product today has exclusive no-replace publication for **regular files
only** (`publish_new_regular`) with no directory-publication primitive and no directory-barrier
receipt type, so this unit depends on two native capabilities that do not exist yet.

**4.4 An undisclosed durable side effect (RF-4).** §3 permits creating missing fixed ancestors
before I exists. If the attempt then fails, those directories persist. So "I absent" does **not**
imply "this attempt left no filesystem effect". The consequence is benign — empty ancestors carry no
authority and a later creator reuses them through fresh admission — but the disposition table's
"Power loss leaves I absent → eligible new creator can start anew" reads as though nothing remains,
and it should say what may remain.

## 5. Specification hole found by reading (RF-2)

§3's new directory-publication durability law says: "Continue up to the already admitted durable
ancestor; do not assume a prior invocation's successful mkdir was durable."

**The recursion has no defined base case.** Nothing in the document says what first establishes an
ancestor as "already admitted durable". The natural base is the account-derived directory that the
OS or the user created and that this act did not — but §3 simultaneously allows this act to create
missing fixed ancestors, so on a fresh machine the chain can consist entirely of components this act
made, and the stated rule then recurses without a stopping condition. Two implementers will resolve
this differently: one will treat the account home as the base, another will walk to the mount point,
a third will treat any pre-existing directory as durable — which the sentence explicitly forbids for
directories a *prior invocation* created. This is new law, not an inherited obligation, so it must
state its own base case.

## 6. Evidence coverage — which sections are backed and which are prose-only

| Section | Conditional evidence |
|---|---|
| §4 publication, concurrency, visibility/durability interval | **yes** — 36 cases, and my probes P1/P3/P4/P7/P8 |
| §5 existing-root durability gate | **yes** — death, uncertainty, latching, non-transferable receipt |
| §1 pre-existing I not pristine | **yes** — 8 partial-root cases |
| §7 node/endpoint law | **yes** — 7 probes against the selected identity walk |
| §8 five-field digest | **yes** — 7 vectors, 9 refusals |
| §1 **eligibility derivation** | **no** — supplied boolean premise |
| §2 **stage grammar, nonce, tree manifest** | **no** — contents are an opaque frozenset |
| §3 **ancestor chain and directory durability law** | **no** — the model has no ancestors at all |
| §6 **never adopt a foreign stage** | **no** — the model cannot express a foreign stage (probe P5b) |
| §8 **lifetimes, lease handoff, budget** | **no** |

Two model artifacts worth recording, neither a defect in the law:

- Any refusal latches the whole attempt, including a benign premature write (probe P7c). §5 latches
  specifically on failed or uncertain *durability confirmation*. The model is stricter than the
  document, so the corpus cannot isolate the §5 latching property from ordinary refusal.
- `refuse()` does not release the fence; only `release()`/`crash()` do. Case sequencing therefore
  depends on explicit calls, which is fine for a model but means fence-release-on-failure is not a
  tested property.

## 7. Required findings

- **RF-1 (blocking, design).** State creator eligibility as a positive checkable predicate: which
  admitted owners (execution principal, launch/core closure, platform/filesystem profile, native
  persistent first-write surface) are consulted, in what order, and what typed non-forgeable receipt
  their conjunction produces. The exclusion list stays, but it cannot be the definition.
- **RF-2 (blocking, design).** Define the base case of the §3 ancestor durability recursion — name
  the durability base (the account-derived directory this act does not create) and state that every
  component this act creates owes its own directory and parent barriers up to that base.
- **RF-3 (blocking, design).** Name the budget owner for a pre-installation creating invocation and
  state what it bounds (ancestor walk, tree validation, P0 dependency construction, publication), or
  state explicitly that creation is bounded by a fixed manifest rather than a shared budget.
- **RF-4 (non-blocking, disclosure).** Record that ancestor creation is a durable side effect that
  can outlive a failed attempt, and correct the disposition-table row so "I absent" is not read as
  "no effect".

Suggested, not required: give §2's staged-tree manifest and §3's ancestor chain the same conditional
treatment the publication protocol already has, so the two NEW laws are evidence-backed rather than
prose-only; and add a model term for a foreign stage so the never-adopt rule is testable.

## 8. Corrections to my own 388, since root asked

- **The two-state framing was wrong.** I treated atomic publication as yielding two durable states.
  It yields two *name* states and three *admission* states, because the creator's fence does not
  survive its death. Root's §4/§5 correction stands and this review adopts it.
- **My "new-root restore necessarily needs a RESERVED-analogue" was over-generalised.** I inferred it
  from the registry precedent without analysing the operation. The accurate statement is weaker: a
  new-root act inside an existing container needs **either** an ordering in which every crash prefix
  is inert and unambiguous, **or** an explicit durable act record. Whether the first is achievable
  depends on whether a materialised store with no lineage node is acceptable as permanently inert —
  which is exactly the concrete operation analysis root says is owed, and which I did not do.

## 9. Limits

Model-level review only. Nothing here qualifies native filesystem behaviour, exclusive directory
rename, directory barriers, crash durability, custody, actor identity, profiles or GC; the probe's
native presence is a supplied premise and no native crash test was run or requested. I did not
re-verify runtime29/inventory58/registry-v2 themselves, and unselected references named by the
draft (S9.3, `store-instance-lineage.v1.json`) remain unselected — this review adopts none of them.
The three replays share the author's own scripts, so they test reproducibility and internal
consistency, not independent re-derivation of the protocol; my separate probes in `evidence/` are
where I tried to break it. Findings apply to the exact 17-member subject at arch `42b5c52c2` /
product `526a1867a34d…`.

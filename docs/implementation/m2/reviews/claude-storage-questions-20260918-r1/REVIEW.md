# Independent review: draft97 integration questions and disclosure gap99 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope: the two unresolved integration questions in draft97's `REVIEW-QUESTIONS.md` and the reproduced
representation gap99. **This is an adjudication of questions, not a review or approval of draft97's code,
of the 87–100 journal/storage drafts, or of any inherited security/native/storage draft.** Reference60 and
envelope66 remain changes-required; nothing here depends on or approves them.

## Outcome in one table

| Question | Derivable from current owners? | Disposition |
|---|---|---|
| **Q1** witness/floor file decoder profile, negative zero | **No** — a real owner gap, and wider than negative zero | Owner decision required (D1). Recommended rule given below; the two decoders differ on exactly one valid-shape spelling. |
| **Q2** malformed/foreign witness under read-only Step 4 | **Mostly yes** — the read-only owner's own §1 settles the reading. One sub-case (generation-mismatched witness) is **not** derivable and is a latent false-corruption report | Editorial correction to Step 4 (C2a) + owner decision D2 |
| **Gap99** complete pin-disclosure size | Gap **confirmed independently, and it is larger than reported** — the two-copy minimal-envelope preflight is not sufficient | Proposal needs correction before use (F3-1..F3-5); four owner decisions (D3–D6) |

## Evidence base (independently established)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/witness-floor-draft-checkpoint-97/subject.tar.xz` (4,038,020 B) | `5b8376cacda967d756a1b4874be4c395b81aa637b26bdde52e50402c66f43aaa` | = `archive-pin.json` |
| 97 `subject.json` (368 members) / `README.md` / `archive-pin.json` | `c5ebd367…320538f` / `f8b5c26c…163cbb8` / `896d3336…58d9f1e` | every member re-hashed from the tar before extraction |
| `trials/purge-disclosure-bound-checkpoint-99/subject.tar.xz` (96,064 B) | `14a6790e0d026995082d738c6a292c6f2c19f8f4e308ebda9f9ab7975812ed93` | = `archive-pin.json` |
| 99 `subject.json` (24 members) / `README.md` / `archive-pin.json` | `37471531…2a50e8bbc` / `f0ce6e17…1c7784` / `45bd9739…21c75a` | every member re-hashed before extraction |

`claude-out/verify_extract.py`: archive bytes and hash checked against the pin; every manifest member hashed
and length-checked **from the tar stream**; refused any non-regular member, absolute path or `..` segment
(none present: 0 symlinks/devices/hardlinks); only then wrote the verified bytes into this workspace.
Re-run after all probes: both extractions still byte-identical, no extra files. Full hashes in
`claude-out/pin-verification.json`. I did not use the previously verified copies.

Owners read from the live architecture tree (hashes at read time):

| Owner | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` (S2) | `a319da39b9f90aff4483a295af3fe004540c71861fb2bd34e84c7e1318bad9d6` |
| `docs/coop/completion/security-completion.v8.md` (§2.1, §5.4; and v1/v2 §2.1, v2 §5.4 by reference) | `54f3a6901d4192c5b6af82d4aad4414a84ee3b7748aa67cae06272a481e38c2d` |
| `docs/coop/completion/security_unit_lib_v8.py` | `3e28bc7ba34e3a5964ca5c611a1735ee6771b7084256893d648a15d8ddf56d40` |
| `docs/coop/design-corrections/security/carrier-highwater.schema.v1.json` | `1bbfd9135bd9492ef5b1df328aacdb959b0440a9e21312763f88609f4b966f82` |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` (§1, §2 Steps 3–4) | `7bcc8f8e23da91e87d36e7c1a1c913f05a634be058e4a4c5c0c73ac4faec1d80` |
| `docs/coop/design-corrections/foundation/canonical.py` | `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed` |
| `…/evaluator3/common.schema.json` / `command-envelope.schema.json` / `invocation-record.schema.json` | `ce45b9ff…af30a8b` / `09292fc1…318830` / `65980226…47ddc8` |

The 99 provenance file's hashes for these owners equal what I read. Also consulted:
`design-corrections/security/carrier-format.v3.md` §8 (witness/binding rows). Codex's observation files and
summaries were read for orientation only; every number below comes from my own probes.

---

# Q1 — Witness/floor file decoder profile and negative zero

## What the owners say

- **S2** lists what is under `opensip-metadata-canonical.1`: "root, catalog, revocation, journal records,
  recovery challenge and epoch, platform profile population"; product data is "everything with a
  `schemaVersion`". The witness (`witnessSchema`) and floor (`highWaterSchema`) are in **neither** list.
- **v8 §2.1**'s domain-tag registry is *closed* and has no witness or floor tag; they are never digested.
- **v2 §5.4** names the file (`grant-journal.witness.json`) and its write protocol; **v8 §5.4** fixes the
  closed *value* shape "validated before any comparison". Neither states a byte encoding.
- **CarrierHighWaterV1** fixes a closed value shape and calls itself a "private operational record; not a
  public wire schema" — no encoding.
- **v1 UR-2**: "Zero is the single byte `0`" — an **encoder** rule. The v2 §2.1 parse-refusal list
  (`METADATA_TOO_LARGE` … `MALFORMED_JSON`) has no negative-zero refusal, so the metadata loader admits `-0`
  as `0`. The product decoder refuses it (`NEGATIVE_ZERO`).
- **Read-only Step 3** compares witness/floor reads **byte-identically** (`stableW`, `stableH`) — so bytes,
  not values, already carry meaning on one path.

Conclusion: the draft97 question is correctly posed. **No current owner selects the decoder**, and
ownership by the security crate does not settle it (S2 explicitly says "never mixed", not "security crate ⇒
metadata profile").

## Independent probe (`claude-out/q1/`, real owner decoders, 31 byte spellings)

Each spelling was decoded by v8 `load_json_strict` and by `foundation/canonical.py parse`, then passed to
the real `witness_shape_refusals`.

- **Exactly one spelling is valid under one profile and refused by the other: `"seq": -0`**
  (metadata: VALID genesis witness; product: `decode:NEGATIVE_ZERO`). `-0` in `witnessSchema` or
  `grantGeneration` is refused by both (shape vs decode). By the closed shapes, the only other reachable
  site is the floor's `lastSeq: -0`.
- Everything else lands on the same side under both profiles; only the *reason class* differs
  (`grantGeneration` ≥ 2^63: metadata `INTEGER_OUT_OF_RANGE` at decode vs product shape `GENERATION`; an
  escaped lone surrogate; nesting 33–64). All are "malformed" either way.
- **The larger gap:** both decoders accept leading/trailing whitespace, a trailing newline, reordered keys
  and `\u`-escaped ASCII in keys and values. No owner states what *bytes* a lawful writer produces, and a
  decode → canonical re-encode does not reproduce such a file. Choosing a decoder therefore does **not**
  give the file a canonical byte form; negative zero is one instance of a missing "file bytes" rule.

Why it matters concretely: a genesis witness spelled `-0` would be OK under one reader and
`witnessMalformed` (quarantine, and via Q2 potentially a public `LEDGER.CORRUPT`) under the other. The Rust
product already contains both behaviours (`identity/src/canonical.rs:139` refuses; the security metadata
codec normalizes — draft97 `trust.rs` comment "-0 canonicalizes to0"), so whichever function a future
file-capture unit happens to call silently decides a quarantine condition.

## Proposed minimal correction (C1) — for owner decision D1

Add one paragraph to v8 §5.4's successor owner (and cite it from `CarrierHighWaterV1`), not to S2:

> **Witness and floor file encoding.** The witness and the per-carrier floor are private operational files,
> not signed metadata and not product data; S2's two profiles do not govern them. A writer emits exactly
> the canonical encoding `C(value)` of `opensip-metadata-canonical.1` with no BOM and no trailing byte. A
> reader admits a file only if (1) it decodes under the strict metadata loader, (2) the decoded value passes
> the closed shape, and (3) **the file bytes equal `C(decoded value)`**. Any other spelling — including
> `-0`, insignificant whitespace, reordered keys, escaped ASCII or a trailing newline — is
> `witnessMalformed` (respectively a malformed floor). The reader never rewrites a file to repair its
> spelling.

Why this shape: rule (3) makes the file byte-canonical, which the Step 3 byte brackets already presuppose;
it refuses `-0` without importing the product decoder into a security file (so S2's "never mixed" is
untouched); and it makes the decoder choice unobservable for every valid file — which is the property
draft97's value-only constructors were built to preserve. The metadata profile is the natural base because
`grantGeneration` is an i64 metadata counter (v8 §2.1) and the journal bodies beside the witness are
metadata documents.

**Not derivable, owner must decide (D1):** (a) accept C1 or pick the product decoder instead; (b) whether
any already-written development witness could carry a non-canonical spelling — if so, C1 turns it into
`witnessMalformed` and a one-time disposition is needed. I know of no lawful writer that emits one, but I
did not examine any writer (none exists in draft97; it reads no files).

---

# Q2 — Malformed / foreign witness and the Step 4 diagnostic rule

## Adjudication

The two readings are: (a) Step 4's "closed witness shape validated … and matching carrier naming" are
**success** conditions, so a malformed or foreign witness can never be reported and is always
`unavailable-busy`; or (b) they require the validation and naming comparison to have been **completed on
stable bytes**, so a *stably* malformed/foreign witness is an `unknown-quarantine-condition`.

**Reading (b) is the one the owner itself requires.** The same document, outside Step 4:

1. §1 "Carrier binding…": a carrier whose "witness names another project … [is]
   `unknown-quarantine-condition`, **subject to Step 4 like every quarantine report and otherwise
   `unavailable-busy`**".
2. §1 precedence row 2: "a published row or surviving witness naming another project … →
   `unknown-quarantine-condition` **with the Step 4 stable observations**, otherwise `unavailable-busy`".
3. §1: the typed reasons `uncertainTailLoss`, `witnesslessRestore`, **`witnessMalformed`** "travel in the
   operational record and the owner diagnosis".
4. Step 3's anchor table last row: "foreign, malformed → `unknown-quarantine-condition` per the v8 §5.4 row".
5. `carrier-format.v3.md` §8.1 read-only row: witness names another project → `unknown-quarantine-condition`.

Under reading (a) all five are unreachable, because a foreign witness can never have "matching carrier
naming". A reading that voids five explicit rows of the same owner is not available. Step 4's own rationale
also points to (b): its purpose is to avoid inventing a diagnosis from **independently timed** observations
("attributed to temporal skew"). A witness whose bytes are identical in W1 and W2 around a journal snapshot,
with a stable floor and two agreeing tails, is not skew; its malformation is a property of those stable
bytes. The phrase "validated before any comparison" is Step 3's *ordering* heading reused verbatim, not a
success predicate.

So, for draft97's question: **malformed and other-project witnesses are reportable as
`unknown-quarantine-condition` (`LEDGER.CORRUPT` / `ledger-corrupt`, detail omitted) if and only if
`stableW`, `stableH` and two agreeing tails hold; otherwise `unavailable-busy`.** "Explicit diagnostic
evidence" is exactly those stable observations plus the typed reason in the operational record — no new
public code. Draft97's instinct not to implement a diagnosis from ambiguity was right; the ambiguity is in
Step 4's wording, not in the law.

### Correction C2a (editorial, Step 4 — no behaviour change under reading (b))

Replace "the closed witness shape validated before any comparison; and matching carrier naming" with:

> "shape validation and the carrier-naming comparison **performed on the stable witness bytes before any
> other comparison, with their result** — a stable shape or project-naming failure is itself a reportable
> condition, never a reason to fall back to `unavailable-busy`."

Add to the evidence list: the operational record carries the typed reason and the SHA-256 of the stable
witness bytes; it never carries the bytes.

## The part that is NOT derivable: a generation-mismatched witness (D2)

Step 3 defines naming as `W.projectKeyDigest == A.journalCarrierDigest` **and**
`W.grantGeneration == A.grantGeneration`. Every §1 / carrier-format statement about a foreign witness says
"names another **project**" — none addresses generation. But:

- the witness is one per-carrier file (v2 §5.4) that names the **current** generation;
- `grantGeneration` advances lawfully (whole-generation REV, uint53 rollover — v8 §5.4);
- `A.grantGeneration` is the **historical** generation of the attempt being asked about.

So after any lawful generation advance, **every** read-only recovery of an attempt from an earlier
generation meets a witness with the right project and a *higher* generation. Under Step 3's literal naming
rule that is "foreign", and under reading (b) — which the owner requires for the project case — a stable
one is reported as **`LEDGER.CORRUPT`**. That would be a false public corruption report produced by lawful
history. v8 `reconcile_witness` does not have this problem because the writer passes the *current*
generation; the read-only path substituted the association's.

I did not find an owner rule for it (searched `commit-recovery-readonly.v3.md` and `carrier-format.v3.md`
for generation/rollover handling of the witness: only `first_generation` lower-bound rules exist). This is
an assumption-level finding from owner text, not from an executed model: draft97 contains no read-only path.

**Decision D2 required.** Candidate (recommended): split "foreign" —
`W.projectKeyDigest ≠ A.journalCarrierDigest` → quarantine-class (as today);
`W.grantGeneration > A.grantGeneration` with matching project → **not** a naming failure: the witness
anchors only the current generation, so no witness anchor is available for generation `A` and the request
falls to the floor/`unknown-custody` rules (never a corruption report, never a confirmation);
`W.grantGeneration < A.grantGeneration` → quarantine-class (a witness behind a sealed association is a
rollback signature), subject to Step 4. Whether a past generation's floor is retained to anchor it is part
of the same decision.

---

# Gap99 — complete pin-disclosure size

## Independent confirmation (`claude-out/q3/size-accounting.json`)

Built from the live evaluator3 schemas and the real product canonicalizer; every admitted size is the
actual `canonical()` length and my independent byte counter agreed with it on every admitted case.

| 4,096 pins × 256 scalars | disclosure bytes | required envelope (2 copies) | envelope schema | product canonical |
|---|---:|---:|---|---|
| ASCII `x` | 1,175,752 | 2,352,308 | accepted | admitted |
| `é` | 2,207,944 | 4,416,692 | accepted | **BYTE_LIMIT** |
| `😀` | 4,272,328 | 8,545,460 | accepted | **BYTE_LIMIT** (a single copy already exceeds) |
| U+0001 | 6,336,712 | 12,674,228 | accepted | **BYTE_LIMIT** |

First refused pin count at 256 scalars, minimal envelope: two-byte 3,890; four-byte 2,011; control 1,356
(ASCII never). These equal the 99 figures, reached independently. The contract sentence "so the complete
refusal stays representable" (`workflows-and-surfaces.md` l.1609-1612) is **false** for the limits it cites.

Canonical cost per scalar (measured): ASCII 1; `"` and `\` 2; U+0080–U+07FF 2; U+0800–U+FFFF 3 (including
U+2028); astral 4; **C0 controls 6**; U+007F 1. `pinId` has **no pattern**, only `maxLength: 256`, so
controls, quotes and backslashes are admitted names.

**Not only adversarial input:** 4,096 CJK names (3 bytes/scalar) fit at 64 and 128 scalars (1.76 MB,
3.34 MB) but at 256 scalars the refusal stops being representable at **2,651** pins. Ordinary non-Latin
names reach this within the documented limits.

## Findings on the proposed correction

### F3-1 (blocking for the proposal) — "both copies" undercounts; the schema admits up to 65 in the envelope alone
`errors` is `maxItems: 64` of `DomainDetail`, and nothing limits how many entries are `evidence.pinned`.
A **120-pin** inventory with the detail repeated across `errors` is schema-**accepted** at 4,235,392 bytes →
`BYTE_LIMIT`, versus 130,564 bytes with two copies. The contract's "in both the termination and `errors`"
describes intent; no schema or stated rule closes it. A preflight that assumes two copies is only sound if
the contract makes "exactly one `evidence.pinned` entry in `errors`, byte-equal to
`termination.domainDetail`" a checked rule.

### F3-2 (blocking for the proposal) — "bounded context overhead" is not small; it breaks the ASCII case the contract relies on
The same failure envelope admits `diagnostics` (256 × `BoundedText` 1024) and `agentHints` (64 × 1024).
Measured: with **one** pin, those two members alone make a schema-valid envelope of 1,968,849 bytes; adding
63 other bounded `errors` entries reaches 2,746,332. With schema-maximum diagnostics and hints present, the
**ASCII** inventory — the one case the contract and 99 both treat as safe — is first refused at **3,879**
pins, and two-byte names at 2,065. So a "fixed minimal required envelope" budget is unsound unless the
`evidence.pinned` refusal envelope is closed by contract to a stated member set, or the budget reserves the
schema maximum of every member it permits. Per-copy fixed overhead at worst-case `remedy` is ~6 KB
(12,016 bytes for both) — that part *is* small and can simply be reserved.

### F3-3 (medium) — further schema positions carry the same disclosure, including a durable one
`StepTermination.domainDetail` is the carrier, and it appears in `InvocationRecord.termination` and in each
of up to 64 `stepResults[].termination`. I validated `StepResult` fragments carrying the full
`evidence.pinned` detail against the real invocation schema: **accepted** for `rejected`, `failed`,
`cancelled` and `abandoned` (`claude-out/q3/invocation-copies.json`). The envelope schema lets a
`kind: failure` envelope carry `invocation`. Hence: (i) an envelope with `invocation` has ≥ 4 copies
(envelope termination + `errors[0]` + invocation aggregate + the purge step); (ii) the **durable**
`InvocationRecord`, if one is written for a refused purge, holds ≥ 2 copies under its own 4 MiB canonical
limit. `MutationReceiptV1.domainDetail` is another position. **Qualification limit:** fragments were
validated, not a complete `InvocationRecord` (I did not construct one); whether a refused purge writes an
invocation record, and whether its terminations must repeat the detail, I did not determine from the
contract.

### F3-4 (medium) — where the check runs contradicts the current contract sentence
The contract says an over-bound pin "refuses durable admission … **before any protected operation
starts**". A rule over the *resulting complete pin set* cannot be evaluated before the operation that
serializes pin writes for that Run observes the set — otherwise two concurrent admissions, each under
budget alone, jointly exceed it (the existing count bound has the same defect; bytes make it likelier). 99's
"in the same protected operation that observes the complete resulting pin set" is right; the contract
sentence must change with it, and the rule must apply to **every** mutation that can grow the
representation: create, rename, and kind change (`repair-prerequisite` is 12 bytes longer than `baseline`).

### F3-5 (low) — the budget must be a pure function of the pin set
99's thresholds come from one concrete envelope (a specific `requestId`, remedy text, no `projectId`). An
admission rule must not depend on request-scoped values or on remedy wording, or the same inventory is
admissible under one request and not another, and a copy edit to the remedy changes who can pin. Reserve
schema maxima for the fixed members instead.

## Proposed minimal explicit correction (C3)

1. **One owning quantity.** `D(R) = len(C(PinnedPurgeDisclosure(R)))` — the product-canonical byte length
   of the complete disclosure for Run `R`, with `runId`, all pins sorted, and the three consequences. Pure
   function of the pin set.
2. **One owning constant**, `MAX_PIN_DISCLOSURE_BYTES`, owned by the foundation beside `MAX_BYTES`, such
   that `N · MAX_PIN_DISCLOSURE_BYTES + RESERVE ≤ 4,194,304`, where `N` is the number of copies the contract
   *permits* on any single canonical document and `RESERVE` is the summed schema maximum of every other
   member permitted on that document. Examples: with the envelope closed to two copies and no
   `diagnostics`/`agentHints`/`invocation` (C3.4), `RESERVE` ≈ 16 KiB covers both details' worst-case
   remedy/subject plus fixed members, giving `MAX_PIN_DISCLOSURE_BYTES = 2,088,960`; the ASCII maximum
   (1,175,752) stays admissible, as the contract intends. If `invocation` may be attached (`N = 4`) the
   constant falls to ≈ 1,044,480 and **the contract's own ASCII maximum is no longer admissible** — which
   is why `N` is an owner decision (D4), not a detail.
3. **Admission rule.** Inside the protected operation that serializes pin mutation for `R`, after observing
   the complete resulting set: refuse the mutation if `D(R') > MAX_PIN_DISCLOSURE_BYTES`, exactly as the
   count and name bounds refuse, using the existing retention-precondition refusal
   (`REQUEST.PRECONDITION_FAILED`); the detail names the attempted pin and the byte figures, **not** the
   inventory. Existing pins are never altered. Name and count maxima stay as they are.
4. **Close the refusal envelope.** For `evidence.pinned`: `errors` contains exactly one entry with that
   code, byte-equal to `termination.domainDetail`; members outside a stated set (`diagnostics`,
   `agentHints`, `invocation`, `mutation`, `doctor`) are absent. State it in the contract and add it as a
   schema `if/then` so it is checked, not assumed.
5. **Replace the false sentence**: "…so the complete refusal stays representable" → "Name and count bounds
   alone do not bound the refusal's size; representability is guaranteed by the aggregate rule below."
6. **Human and agent projections** render the same complete list from the same observed inventory. I found
   no byte limit owning them; the rule is "complete or fail", never truncate (D6).

Worked examples for the contract (measured, two-copy closed envelope): 4,096 × 256 ASCII → admitted
(2,352,308); 3,889 × 256 `é` → admitted, 3,890 → refused at pin admission; 2,651st 256-scalar CJK pin →
refused at pin admission; 120 pins can never overflow once C3.4 closes `errors`.

## Pre-existing over-budget state

Reachable if any inventory was admitted before the rule (pin persistence is unimplemented, so today this is
preventable — that is the strongest argument for landing C3 **before** pin persistence, as 99 says), or
after a future change to `MAX_BYTES`, the canonical encoding, or the envelope. The constraints rule out the
easy answers: no truncation, no revocation as fallback, no false completeness, and the purge must still
refuse. What can be said from current owners:

- The purge **refuses and destroys nothing** — unchanged.
- The refusal cannot be `evidence.pinned`, because its schema *requires* the complete disclosure. Emitting
  it with a partial list is forbidden; emitting it without `purgeDisclosure` is schema-invalid.
- An existing D9 outcome states the truth without minting a code: `operational-failed` /
  `DELIVERY.REQUIRED_FAILED` with detail `DELIVERY.REQUIRED_PROJECTION_FAILED` ("a required projection …
  failure when no Run was committed", `StepTermination` description). It is truthful (the required
  disclosure could not be delivered), non-destructive and makes no completeness claim. **But** it changes
  the D9 class from `request-rejected` (exit 2) to `operational-failed` (exit 4), and gives the user no
  route to see the pins. Whether that is acceptable is **not derivable** (D5).
- A complete answer needs a surface that can enumerate pins incrementally (a bounded, cursor-paged pin query
  under the same lease/generation rules), so the user can release pins until `D(R)` is back under budget.
  Releasing a pin is an ordinary authorized act, not a destructive fallback. No such query surface exists in
  the owners I read; that is a new-surface decision, not a correction.
- Doctor should report the condition (`D(R)`, the constant, the Run) so it is found before a purge meets it.

## Decisions not derivable from current owners

| # | Decision | Why it cannot be derived |
|---|---|---|
| D1 | Witness/floor file encoding rule (C1) and disposition of any existing non-canonical development file | No owner states a byte form; S2 and the closed domain registry both exclude these files |
| D2 | Meaning of a witness whose generation differs from the association's | Owners speak only of "another project"; literal Step 3 naming + required reading (b) yields a false `LEDGER.CORRUPT` after any lawful generation advance |
| D3 | The single owning byte budget and its owner (foundation vs workflows) | Two units are involved; the constant must be pinned by both |
| D4 | `N`: which documents may repeat the disclosure (`errors` multiplicity, `invocation`, `mutation`, durable `InvocationRecord`) | Schema permits up to 65 + 65; the contract states intent for two; `N = 4` makes the contract's own ASCII maximum inadmissible |
| D5 | Outcome for a pre-existing over-budget inventory (reuse `DELIVERY.REQUIRED_PROJECTION_FAILED` and accept the class/exit change, or define a paged disclosure) | Both satisfy "no truncation / no destruction"; they differ in D9 class and in whether a new surface is created |
| D6 | Whether human/agent renderings have any size bound and what "complete or fail" means for a terminal | No owner found |

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; again after all probes) | 368/368 and 24/24 verified from tar; 0 non-regular; extractions byte-identical on re-check |
| `q1/profile_differential.py` **r1** | **Failed — reviewer script bug** (uncaught `NON_NFC_STRING` from an unused comparison). Preserved as `profile_differential.failed-r1.py` + `FAILED-r1.txt`. Side observation kept: v8 `load_json_strict` admits NFD at parse; only `canon` refuses it |
| `q1/profile_differential.py` r2 | 31 spellings; single validity divergence `negzero-seq`; `profile-differential.json` |
| `q3/size_accounting.py` | four-row reproduction, thresholds, per-scalar costs, 65-copy case, optional-context cases; `size-accounting.json` |
| `q3/invocation_copies.py` **r1** | **Failed — my construction error** (`stepId` is an integer, `attempts` an array). Preserved as `invocation_copies.failed-r1.py` / `invocation-copies.failed-r1.json` |
| `q3/invocation_copies.py` r2 | `StepResult` fragments with the full detail accepted for 4 outcomes; `invocation-copies.json` |

Interpreter: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` (3.12, jsonschema +
referencing). Nothing was written outside this review directory; no `__pycache__` was created in the
architecture tree or the extracted subjects (bytecode writing disabled). `git status` shows only
pre-existing entries not made by me (`ACTIVE-WORK.md` modified; two untracked `m2/reviews/` directories).

## Qualification limits and unresolved assumptions

1. I did not review, build or test draft97's Rust (`journal_store.rs`, its 256 shape / 1,245 reconciliation
   cases, Clippy, host-isolation59). Q1/Q2 are adjudicated from owner text and the Python owners only. The
   Rust negative-zero behaviour is confirmed by source inspection (`identity/src/canonical.rs:139`) and, for
   the metadata side, by the draft's own comment — not by execution.
2. Q2's generation finding (D2) is reasoned from owner text; no executable read-only model was run, and I
   did not read `commit-recovery-readonly.v3.md` §3–§7 in full.
3. Gap99 sizes are for the Python reference canonicalizer; I assumed the Rust product canonicalizer is
   byte-identical (it is specified to be; not re-measured here).
4. F3-3 rests on schema fragments, not a complete schema-valid `InvocationRecord`, and I did not determine
   whether a refused purge persists one.
5. The example constants in C3.2 are illustrations of the formula under stated `N`/`RESERVE`, not proposed
   values; the owner must compute `RESERVE` from the final closed member set.
6. None of this implies review or approval of drafts 87–100, reference60/66/69/73/78, or any inherited
   security, native or storage draft.

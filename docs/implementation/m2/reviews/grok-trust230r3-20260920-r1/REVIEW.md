# Independent bounded review — ROOT trust-inputs 230 r3 C1–C4 fixes

Scope: ROOT's r3 corrections on top of the frozen r2 before-C1 image, checked against the original
C1–C4 findings. **This is not cumulative protocol approval, not source selection, not native or
crypto authority, and not a verdict by test count.** No repo, product, or candidate edit, commit, or
push. Output is only this directory. Frozen trial bytes were not modified.

The subject is a conditional bytes/shape model. It does not establish signatures, thresholds,
envelopes, native creation/absence/custody, live successor-bucket census, fork detection, smallest-
digest witness choice, 226 event-outcome admission, S4 durability, or v14 dispatch. Probes record
what the unmodified toy functions do on shape-valid fabricated values.

## Verification and reproduction

- Frozen `trust-inputs-wip-230-r3` archive pin `99288ae0…3c00`, 66388 bytes, 38 members: tar SHA256,
  pin, and EVERY `subject.json` member verified from the tar **before** extraction into this
  directory; extracted copies re-verified byte-equal after the runs.
- Python: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` 3.12.13, flags `-I -B`.
  Scripts print JSON on stdout and write nothing. No script in the frozen subject was edited.
- 201 kernel/canonical loaded only via the model's pinned paths (sibling symlink to the already
  verified reference-201 extraction). Hashes equal the model's `PINS`: canonical `d47f25db…b442`,
  kernel `df45c9c5…2299`. Not a live product import.
- Invocation: `python -I -B check_trust_inputs.py` (optional model path as argv[1]); `python -I -B
  check_trust_inputs_variants.py` (no extra options). Both exit 0 on the frozen corpus.
- Regenerated `input-check-root-r5.json` and `input-variants-root-r4.json` key-for-key:
  **195 cases** (21 admit / 168 exact-label refusals / 6 static holds); **29/29 source variants
  killed** by corpus assertions; guard survey **92 reasons → 83 killed, 8 ERROR-not-a-kill, 1
  direct-raise `metadata-value`**.
- Before-C1 image (r2 ROOT) is preserved and byte-equal to the prior review's r2 pins:
  model `544a95e1…b375`, check `2269dc39…3b08`, variants `44c6acb8…d2cc`, INPUT-JOINS
  `d2b05b97…8f4e`. Schema `trust-inputs-root.v1.json` is unchanged r2 (`b2939551…d823`); 231/232
  format pins are therefore still exact. Earlier 184/25 reports are retained as members.

r3 vs r2 before-C1 is a small, reviewable delta: Work bound `0 <= n` → `0 < n`; two new
`descriptor_operation` requires (`continuity-forward-initial`, `continuity-ancestor-predecessor`);
11 new corpus cases; 4 new source variants (two C1 unbinds, two C4 unsafe-admission replacements);
INPUT-JOINS prose for the predecessor binds, C2/226 remainder, and C3/C4 notes.

## Original findings vs r3

### C1 (medium, original) — closed at the stated site

The r2 exception joined a source-bound continuity shell to a target-store descriptor without binding
that descriptor's predecessor/`nativeBefore` to the target-before. Independent probes on the
**unmodified before-C1 model** still admit the original three cases; the **unmodified r3 model**
refuses them with the new labels:

| probe | before-C1 | r3 |
|---|---|---|
| X0a honest forward (revision 1, previous null, nativeBefore null) | ADMITS | ADMITS |
| X0b honest ancestor (`previousCapsule == hash(image)`, revision = image+1, nativeBefore = `{image.revision, image.sha256}`) | ADMITS | ADMITS |
| X1 forward on revision 5 with a non-null `previousCapsule` | **ADMITS** | `continuity-forward-initial` |
| X2 ancestor `previousCapsule` names another capsule | **ADMITS** | `continuity-ancestor-predecessor` |
| X3 ancestor image revision 3, descriptor revision 9 | **ADMITS** | `continuity-ancestor-predecessor` |

Split binds on r3 also refuse: nativeBefore set on an otherwise-initial forward (`X1c`); ancestor
`nativeBefore.sha256` ≠ image hash (`X2b`); ancestor `nativeBefore.revision` ≠ image revision
(`X3b`); honest nativeBefore with descriptor revision = image+2 (`X3c`). `nativeBefore.revision 0`
is shape-refused (`I64Positive`) before the join (`X1b`).

The require is exact against the loaded target image and the event's NodeRef:

`previousCapsule == ev['targetBefore']['image']['sha256']` and `revision == target['revision'] + 1`
and `nativeBefore == {revision: target['revision'], sha256: ev['targetBefore']['image']['sha256']}`.

`Work.load` already demands retained bytes, so the NodeRef hash is the loaded capsule. Forward is
`revision == 1 and previousCapsule is None and nativeBefore is None`, then `join_absence`.

Passing `cur_ref` into `descriptor_operation` is unnecessary: the helper binds the descriptor to the
event's target-before, and `admit_restore_proof` separately binds the same descriptor header to the
chain predecessor. Together they force `image.sha256 == cur_ref.sha256`.

### C1 inside full restore-proof admission

Challenged independently, not by test count:

- **R1** ancestor continuity as the **terminal witness** of proven N=c3, with target-before = c3,
  `previousCapsule`/revision/`nativeBefore` bound to that image: **ADMITS**. This matches 222
  `successor_model.proves` / `direct_provers`: a direct prover is `operation != restore-recovery`
  and `nativeBefore == (parent.revision, parent.identity)`. Continuity is not restore-recovery.
  PERSISTENCE: ordinary publications have `nativeBefore` equal to revision-1 and `previousCapsule`;
  only restore-recovery may differ. The toy is allowed to admit this structural join. It does **not**
  select the live smallest-digest witness or admit event outcomes.
- **R2** same witness header still pointing at c3, but the event's target-before is c2:
  `continuity-ancestor-predecessor`. This is the C1 bind firing **inside** `admit_restore_proof`.
- **R3** internally consistent ancestor of c2 offered as witness of proven c3: `witness-adjacency`
  (chain join, not the C1 label). Wrong parent cannot ride the restore terminal slot by rewriting
  both header and event together.
- **R4** true cross-store **forward** (operation on B1, descriptor/event on B2) rewritten as a B2
  restore terminal witness (revision 3, predecessor set): `continuity-forward-initial`. Forward
  cannot be a restore chain link or witness: restore links/witnesses have revision ≥ 2 and a
  non-null predecessor; forward requires revision 1 / null previous / null nativeBefore.
- **R5** ancestor continuity as an ordinary **chain link** (n=1 → reconstructed 2, target-before=c1):
  **ADMITS**, same ordinary-link rule as 222 (`nativeBefore` equals the logical predecessor; action
  is not restore-recovery).

### C3 (low, original) — closed

`Work.__init__` is now `type(n) is int and 0 < n <= cap`. Independent probes: negative, zero
(objects/edges/size), float, `bool` (`type(True) is not int`), and cap+1 all refuse `work-profile`.
Cap-equal admits (not an enlargement). A zero/bool/enlarged `Work` cannot be constructed, so it
cannot be shared into `admit_restore_proof`. Nested recovery uses the same `Work` object (no inner
`Work()` that would reset to the 222 caps): exact shared budget admits (`R6`); one object short on
that same ledger refuses `work-objects` (`R7`). Forward's `join_absence` charges the passed ledger
(`R8`, `work-bytes` on `Work(1,1,1)`).

### C4 (low, original) — addressed with the requested distinction

Guard deletion of `continuity-target-event` and `continuity-target-before` still **ERROR-not-a-kill**
(`IndexError: list index out of range`, `KeyError: 'image'`). Those two reasons remain in the same
8-row error set as r2; they are not counted as kills. That preserves the actual errors.

New **source** variants replace the require with an explicit unsafe admission (`return o`):

| variant | replacement | killed by |
|---|---|---|
| `missing-target-event-accepted` | `if len(matching) != 1: return o` | assertion `('admitted', 'descriptor:cross-store-continuity-needs-target-event')` |
| `ancestor-absence-accepted` | `if kind != 'capsule': return o` | assertion `('admitted', 'descriptor:ancestor-cannot-claim-absence')` |

Direct source unsafe admission is therefore a corpus assertion kill. Secondary guard-off crashes stay
errors. The other 27 source variants remain killed; none survive.

The two new C1 reasons **are** guard-killed (`continuity-forward-initial`,
`continuity-ancestor-predecessor` → admitted negatives). Guard reasons 90 → 92, killed 81 → 83;
the 8 errors and `metadata-value` direct-raise are unchanged.

### C2 (low, original) — remaining stated boundary, not a r3 regression

`if o['store'] == d['store']: return o` is unchanged. INPUT-JOINS now says the same-store helper
intentionally binds projection and operation only; full event↔operation / event-outcome admission is
226. Independently confirmed:

- **X4** same-store ordinary-import shell whose events are a target continuity of another operation:
  **ADMITS** at `descriptor_operation`.
- **R10** same-store continuity shell as a B1 restore terminal witness: **ADMITS**, because the
  helper never looks at events and restore only requires `action != restore-recovery` plus
  `nativeBefore == N`.
- **R9** a cross-store ancestor descriptor may carry an extra *non-target* continuity event:
  **ADMITS**; the helper only requires `len(matching) == 1` target-side continuity event.

None of these is a C1 miss (C1 runs only on the cross-store branch). They are the 226 remainder
already named in INPUT-JOINS.

## Remaining findings

No required C1/C3/C4 remainder at the sites the original review named.

#### C-2 (low, remaining / stated)

Same-store `descriptor_operation` still returns before events. A same-store continuity or
ordinary-import shell can sit as a restore terminal witness (`R10`) or ignore mismatched events
(`X4`). Root documents this as 226's job. Do not treat the r3 corpus as 226 event-outcome
admission.

#### FYI — extra events on the cross-store exception (`R9`)

"Exact single target continuity event" is implemented as "exactly one *matching* target-side
continuity event", not "events contains only that row". Other loadable events are ignored after
locator checks. Same 226 remainder.

#### FYI — ancestor continuity as restore terminal witness is in-scope structural law here

R1/R5 are lawful for this bytes model and for 222's direct-prover definition. Live census, uniqueness,
smallest-digest selection, and applying the continuity event to `afterProjection` remain outside.

## OpenSIP / model-boundary checklist (this toy, not product)

- [x] Refusal reasons are explicit strings; `Work`/`require` do not swallow
- [x] No `console.log`; scripts write stdout JSON only
- [x] IDs are existing NodeRef SHA256+bytes, not raw `randomUUID()`
- [ ] OTel / product DI / `Result<T,E>` — not applicable to this reference toy
- [x] Result strings still refuse to claim native proof, census, signatures, or S4 durability

## Boundaries not treated as findings

Signatures/thresholds/envelopes; native creation, absence, custody; live bucket census, fork
detection, witness choice; closure admission of n and N; S4 durability and dispatch; lineage/current
selection/PhaseB; 226 full event-outcome admission (explicit remainder); primary 203 envelope-route
integration; unchanged author code in `claude-author-r2/` (byte-preserved, not re-reviewed as
approval).

## Verdict

- [x] **C1, C3, C4 r3 fixes hold** against the frozen before-C1 image and the original probes
- [x] **C2 remains** the documented 226 structural-only boundary
- [ ] **Not approved as a protocol, source, or implementation**

No harness failure. No cumulative approval.

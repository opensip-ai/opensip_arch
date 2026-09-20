# Author correction r2 — six private trust input nodes (230)

**AUTHOR correction assistance for root; NOT approval, not selected, no native authority, no new
public command.** New directory only; r1 is preserved byte-for-byte (its `hashes.txt` re-checked:
all OK). No repo/candidate edit, commit or push. Root's six points were right; r1's joins were
thinner than its prose. Each is corrected below with the variant that now fails without it.

## Files (all reusable; none overwrites anything)

| file | content |
|---|---|
| `proposed/trust_inputs_model.py` | schema builder + joins. Importing writes nothing; running prints the schema. sha256 c3b08c9e…66f3 |
| `proposed/trust-inputs-230.v2.json` | its output: 12 new defs + verbatim 231 defs. sha256 0e89117f…ae11 |
| `proposed/check_trust_inputs.py` | `checks(M)` corpus, prints a report. 163 cases: 16 admit, 141 exact-label refusals, 6 static |
| `proposed/check_trust_inputs_variants.py` | 20 unsafe SOURCE variants + guard-off survey over all 80 reasons; prints a report; exit 1 on a survivor |
| `proposed/checks-r2.json`, `proposed/variants-r2.json` | the two reports as run |
| `claude-out/io/` | every intermediate run, including the first variant run that exposed 5 uncovered reasons |

## Corrections, point by point

**1 Creation marker.** `storeMarker` is now a `NodeRef` to `records/H` holding the EXACT canonical
`StoreMarkerV1` alias `{schemaVersion:1, storeInstanceId}` — no wrapper, no identity recipe, not a
signed-metadata `BlobRef`. Source: 223 `product/crates/storage/src/store_root.rs` (11f04d2c…, my
verified 223 extraction): two members, canonical bytes, `MARKER_LIMIT 128`, test asserts 72 bytes. A
fixture asserts my canonical bytes equal the product's format string and are 72 long. The join loads
the marker, requires `bytes == 72`, canonical, shape, and `S` equal across marker / input / shell /
capsule / event, and the capsule `eventHead` to be the exact `EventRef` of the creation event. Result
string: "the record is not native proof of exclusive creation, skeleton, marker placement or absence".
Variants killed: marker not loaded, length unchecked, event head unchecked.

**2 Restore proof.** r1 compared only `nativeBefore`; a restore-recovery descriptor whose
`nativeBefore` happened to equal its predecessor would have passed as witness. Now, per 222
`successor_model.proves` (53cae8d9…) and PERSISTENCE (f9963414…):
- the witness's `operation` is loaded under the closed `OperationInputV1` and must NOT be
  `restore-recovery` (`witness-is-recovery-operation`), AND be direct (`witness-not-direct`);
- every ORDINARY chain link must have `nativeBefore == its logical predecessor` (`link-native-before`);
- a NESTED restore-recovery link is admitted only through ITS OWN proof node: that proof must prove
  exactly the link's logical predecessor (`nested-proof-parent`), its observed image must be the
  link's `nativeBefore` (`nested-native-before`), same store binding, and its own direct terminal
  witness must admit — a new `nativeBefore` equality is never self-proof;
- admission is iterative (explicit stack, per-path cycle set) under one `Work` object: 65536 objects,
  131072 edges, 268435456 bytes, 4 MiB per object, all charged BEFORE the read and shared across the
  whole recursive graph (fixtures: exact budget admits; one object / edge / byte short refuses);
- `chain.maxItems` is 65536 (the existing object bound); the guessed 16384 is gone. The 4 MiB
  canonical node limit is enforced by `NodeRef.bytes` and the load.
Positive: a second rollback whose chain passes through an earlier recovery outcome. Negatives: nested
proof or nested original witness unavailable, nested proof proving another capsule, nested observed ≠
recovery nativeBefore, nested other store binding, ordinary non-direct link, non-direct ordinary
witness, recovery witness, witness operation unavailable, link shell on another store. A real hash
cycle cannot be built when hashes are verified, so the cycle guard is tested as a DEPENDENCY CONTRACT
with a resolver that does not verify hashes, and is labelled as such.
One divergence from the 222 toy model, flagged not hidden: the toy refuses a recovery link at chain
index 0 (`missing-proof-parent`) because its proof tuple has no parent there; my node carries the
observed image, so index 0 is admitted through the same nested rule. Root should confirm.

**3 Restriction.** `catalogSnapshot` now loads the role's OLD accepted catalog body, validates it
against the primary catalog schema (939ad388…) and requires `subject == str(snapshotVersion)` — the
kernel's own predicate (l.1547–1549); presence alone refuses. `listNode` must be REACHABLE from the
BEFORE history (iterative walk over `prior` / merge `parents`), be a `list` node, and its list body
(primary revocation schema) must contain the exact `(subjectKind, subject)` fact. The list's
envelope/threshold authentication is UPSTREAM and the result string says so. The prospective
`contextRoot` is loaded as a `RootAdmissionNodeV1` and its `binding` must equal the bound
`BeginBatchV1.replacement`; the current context additionally matches `heads.root.binding`. The role
must be in the batch's `selected`. No field was invented: `BeginBatchV1` carries `replacement` as a
`RootBinding`, not a NodeRef, so the join is binding-to-binding. Consequence to note: two admission
nodes with the same binding but different original context both satisfy it; choosing between them
is the 215 producer's job.

**4 Absence.** The join loads `event.sourceBeforeImage`, requires its store binding to equal the
input's source and `sourceEventHead` to equal that image's `eventHead`, and runs the EXISTING
`admit_transition_intent` of the pinned 201 kernel (df45c9c5…) — a `store-migrate` without schema
advance now refuses `intent-semantics`. Store equality between shell and event is enforced in ONE
common helper for every join; only the absence/continuity join passes an explicit side store, so a
target-side event on the target store is lawful there and nowhere else (variant "waived globally" is
killed). Native absence and the 222 initial-bucket census remain the producer premise.

**5 Roles, observations, duplicates, CLOCK.** v14 (`machine14.json` 039a5702…) `offlineRunningPolicy`:
scope "installed components on install surfaces (G08)", precedence "Evaluate CORE first, then INDEX,
then COMPONENT". So the role set IS derivable and is a constant `{TR-CORE, TR-INDEX, TR-COMPONENT}`;
the caller-supplied `roles` member is removed (shape-refused) and an event for another role refuses.
v14 gives no role set for installing the CORE itself or for TR-BUNDLE/REPAIR/PROFILE surfaces; that
is owed by its owner and is not represented. Per-role observation input is implemented: a REVOKE /
QUORUM event must cite an observed-context input of the same invocation and store, of the matching
purpose, whose evidence names THAT role. Event-side duplicate refs are kept with strict equality.
INSTALL/CONTINUE/CLOCK events must cite a retained `ClockWriteEventV1` with `source == "s4"`, of the
SAME operation and store, sequenced before them; a fabricated or foreign clock-write refuses.

**6 Evidence and honesty.** Guard deletions that end in `TypeError`/`KeyError` are reported
`ERROR-not-a-kill` and never counted. Measured state (`variants-r2.json`): 20/20 source variants
killed by corpus assertions; of 80 refusal reasons 73 are killed by guard-off, 6 error out
(`admission-clock-kind`, `list-node-kind`, `quorum-context`, `quorum-no-accepted-root`,
`revocation-never-established`, `unavailable`) and 1 (`metadata-value`) is raised directly rather than
through `require`, so wrapping cannot disable it. All seven have an exact-label case in the corpus,
but that is weaker evidence than a kill and I state it as such. The first variant run found five
uncovered reasons; I added their cases and kept that run.

## Tested joins vs owed admission

Tested (conditional, fabricated bytes): shapes; hash/length/canonical re-verification of every loaded
node; the equalities and reachability listed above; work precharging.
NOT tested and NOT claimed: any signature, threshold or envelope; native exclusive creation,
skeleton, ancestor reconfirmation, fence, custody, aliasing; live complete-bucket census, fork
detection, smallest-digest witness choice; closure admission of n and N (roots, heads, history,
events, original T, sourceFence); S4/S4.5 evaluation and its outputs; which roles/causes v14/215
actually dispatch; S6. Toy capsules and descriptors are shape-valid, not reachable lifecycle states.

## Further real observations

- `BeginBatchV1` has no NodeRef to the prospective root admission, only a `RootBinding` (point 3).
- 222's toy proof tuple and my proof node differ at chain index 0 (point 2).
- The 231 `RoleEventV1` shape already forbids `observed-context` on INSTALL/CONTINUE/CLOCK, so my
  `admission-clock-kind` guard is reachable only for REVOKE/QUORUM riding a clock-write.

## Pins

231 bundle (private copy) d9ac024357c1645727449bb38f940dbf886244e1d3959998a3e28b64d6857968 ·
`canonical.py` d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442 · 201 kernel
df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299 · primary revocation schema
143027369ccd150449cfe5b45d38645e62931002f47cd73e8cea22d38547fad4 · primary catalog schema
939ad388734f0d8ff3618d2b6a137e049abe305328b6ee50d9c786b0f84c7c44 · 223 `store_root.rs`
11f04d2cbd6c287d71a8f59a038af3635c3d89d95a02dad089be80293ccc36c3 · 222 `successor_model.py`
53cae8d97906c6f060307291d459ef5a0d24aa3b2c344ce005c62772f777d6df (live draft) · 222 `PERSISTENCE.md`
f99634147e58c3b80de7508edcb2f08cfbbe3f62ea5b3156be4f361976a336ec (live draft) · v14 `machine14.json`
039a570244441709c8a773d2c92944fff7ad1b249718656ab2d87645feec6715.
The model resolves its pinned inputs relative to the reviews directory and asserts every hash at import.

Limits: r1's INPUT-JOINS prose is not rewritten here; where it conflicts with this report, this
report and the model govern. 215 and 222 were read by the sections these joins touch, not end to end.

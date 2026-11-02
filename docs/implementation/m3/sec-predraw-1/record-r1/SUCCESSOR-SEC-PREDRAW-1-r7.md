# SEC-PREDRAW-1 r7: the security-owned pre-draw boundary for R10a and ER10a (successor record)

**Author:** claude-sec-predraw-1 (w35), Claude Opus 5.5 / high, R3-FRONTIER, long-horizon lead (preflight ROUTE-OK).
**Authority:**
- LD-Q-180, LD-Q-181;
- LD-Q-182 (option F; `coordinator/msg-ldq182.txt`, `d9c55ca4…`);
- LD-Q-185 (stay in F; HC-2 adopted provisionally as LD-SECPRE-HC2, with conditions (a) to (d);
  `coordinator/msg-ldq185.txt`, `3cc30cc2cbc94afb6167f9affd49e2d91edca071a134e031f8b6a8fc0ed43e3c`);
- the R3 verdicts REVIEW-r3esc (a) (`e5dd78e4…`) and REVIEW-r1 (`c2a4/review-r3esc/sec-predraw-1-r1/REVIEW-r1.md`,
  `1ca6c185bd3eba6d6bf511499756ae9d28f80f5f1901a6c29ddea78adefff630`);
- the handoff `dc5c10f1…`.

**Status:** proposed. The coordinator adopts it by receipt after an R3 ADOPTABLE verdict on these exact bytes. r7 replaces r6
(`22ba6c63…`) in whole (LD-Q-200: REVIEW-r6's three findings, record text only); r6 replaced r5 (`31d8ba48…`). Section 5 is the adopted funding basis, FB-1 r4 (LD-Q-195/196/197), incorporated verbatim
with its headings shifted. It replaces r5's per-operation regime, which LD-Q-195 withdrew. §4.3's production exclusion is rewritten by the lead to parity
with the accepted X8/X9 gating (LD-Q-191 D4). It keeps the Fable r3 guard and check evidence by reference. **Pins:** product `462a7a7e9019aeada6ef0a3ce87b5b6ab8671666` (paths under `crates/security/src/`
unless stated), architecture `342222ffe1586d254249a9ffe41a085f6bc07e99`. **Route block:** the handoff's, unchanged:

```text
Capability route: R3-FRONTIER
Codex: gpt-6-astra / high
Claude: claude-opus-5-5 / high
Claude long-horizon lead: claude-opus-5-5 / high
longHorizonLead: true; the same author writes the successor record, the implementation plan, the code and the integration of the boundary.
Escalate when: an Opus pass is inadequate on the same point after a complete R3 round (then Claude Fable 5.1 high, inside R3); or the boundary would change J1's R10/R10a/R11/R12 order, X2's lease terms or X4's first-read semantics.
Escalation route: R4-EXCEPTIONAL, only with an explicit coordinator exceptional authorization under OD-AUTO-1.
Independent review: Codex gpt-6-astra / high (R3-FRONTIER), a different vendor from the Claude author.
De-escalate when: the successor is adopted and the remaining work is local code against frozen interfaces with deterministic controls (R2-DEEP).
Exceptional authorization: none; max/xhigh prohibited.
```

## r7 changes (LD-Q-200; REVIEW-r6 `0f213ebd…`)

FB-1 r4 (§5, verbatim), CAP-NC-20, HC-2, COMPONENT-RELEASE-SUBJECT and A-RF-4 at X8/X9 parity are unchanged. No
constant, ceiling, order or lease term changes.

| Finding | Disposition | Where |
|---|---|---|
| R6-RF-1: the comparison-debit control and literal debit text remain operative | C-A1i is retired and replaced by **C-A1i′**, a witness at an actual `owned` debit (the live index's buffer). §1.4a's step R.5 now has one funding failure point (the `owned(72)` debit), with two uncharged appends. The run-pass sentence no longer calls each primitive a debit. The preface names P-1's complete set of funding failure points. A mechanical stale-text sweep over the whole record is attached to the request (LD-Q-200). | §1.4, §1.4a, §1.8 |
| R6-RF-2: the read mark precedes the cap; the no-view mark is unfunded | The mark is P-1's **step 0′**, after the cap (step 0) and before every other allocation, on the durable path and the read `Some` path; it is FB-1's one mark row. §4.2's former step 1 is removed. The read `None` path allocates an explicit boundary mark, `owned(16) = {1, 0, 144}` on the session ledger through `charged_step`, with latching and session release on failure. Controls: C-NC-21 on both the durable and read `Some` paths (no mark allocated), and **C-R4-mark**. | §1.4, §1.8, §3.2, §4.2, §5.1 |
| R6-RF-3: the input views' fill is unpriced | Each view keeps the prior boundary recipe's explicit per-push charges: `owned(16·S)`, then `S` × `{0, 1, 0}`, one immediately before each push within capacity, on the gate ledger, for the actual `S`. `S = 0` takes an allocation-free path. The failure point and cleanup are stated. FB-1's exemption is **not** extended. `gate_charge` is labelled a proposed adapter. Control **C-IN-fill**. | §4.3, §5.1 |

## r6 changes (LD-Q-195, LD-Q-196, LD-Q-197; REVIEW-fb1, REVIEW-fb1r3, REVIEW-fb1r4)

| Ruling or finding | Disposition | Where |
|---|---|---|
| LD-Q-195: the funding restructure | §5 is FB-1 r4. P-1 is priced as part of the R10/ER10 read's own admission computation, under the accepted trust-reader model. Only P-1's new allocations are charged, through `owned`. The per-operation regime of r3 to r5 is withdrawn, and R5-RF-1 and R5-RF-2 fall away (REVIEW-fb1 §1 answer 4). | §5 |
| LD-Q-196: the component cap | `MAX_CATALOG_COMPONENTS_M3 = 20` at one site, checked as P-1's **first** operation, refusing on `TrustRow::Budget` (REVIEW-fb1: CAP-NC-20 ADOPTABLE, route (a)). `TRUST_VIEW_COST` is unchanged. The margin is one object. Controls: C-NC-21, C-NC-20, C-NC-site and C-NC-fit. | §1.4, §1.8, §5 |
| FB1-RF-1 and FB1R3-RF-1 | A local reader-model sort with `owned(4m)` buffers and uncharged comparisons. §5's §1a declares every reused primitive's own charges, including both wrappers' rechecks and their ledgers. | §5 |
| CP-X4T-CEILING-1 | Registered by the coordinator, and not fixed here. It covers three gaps: the fenced read does not enforce `TRUST_VIEW_COST`; the 128-object figure omits the manifests; there is no member-count cap. | §8 |

## r5 changes (answering REVIEW-r4; LD-Q-192; superseded in §5 by r6)

| Finding or ruling | Disposition | Where |
|---|---|---|
| A-RF-4 at X8/X9 parity | **MET** (REVIEW-r4). §4.3 is unchanged. | §4.3 |
| R4-RF-1 (prepaid work, compound primitives, the oracle) | **Rule 1:** one debit per operation, immediately before it, with no pass or bundle debits. **Rule 3:** the FUNDING-ORDER-CENSUS source census replaces the oracle. C-F0 counts work events from hooks inside the operations. The sorts are the reused, accepted C2a-1 `merge_sort` (`component_closure.rs`:392-430). | §5 A.0, A.1, A.3, A.7 |
| R4-RF-2 (unfunded refusal causes) | **Rule 2:** `cause = String::new()` on every P-1 route. The contract is verified as diagnostic-only and never projected (A.0), and C-F10 pins it. The only diagnostic allocation is `Revoked`'s required row, built from three paired debits. | §5 A.0, A.2 |
| REVIEW-r4 §3 items 1–5 | Item 1: §1.4 and §5 A.2 give one complete enum. Item 2: A.5 is reconciled. Item 3: the count/fill-equality mutation is withdrawn. Item 4: allocation-free `R_rel = 1` and `K = 1` paths. Item 5: the read acquisition releases its own session on failure. | §1.4, §5 |
| LD-Q-192 additions | (1) Reuse: `owned`, `COMPARISON_COST`, `merge_sort` and `WorkScope::charge`; new primitives N1–N9 are listed, each with its body form and a mutation control. (2) The `cause` contract is verified, with sites. (3) FUNDING-ORDER-CENSUS is scored as its own line. | §5 A.0, A.1, A.7 |

## r4 changes (answering REVIEW-r3; LD-Q-191; kept for history)

| Finding or ruling | Disposition | Where |
|---|---|---|
| Item 3′ and COMPONENT-RELEASE-SUBJECT | **Adopted** by receipt (LD-Q-191: `ADOPTION-HC2.md`, `ADOPTION-COMPONENT-RELEASE-SUBJECT.md`). Enforcement is owed in code. C-CRS-2's fixtures use digests distinct from `manifestDigest`, as a control requirement. | §1.3, §1.8, A.7 |
| R3-RF-1 and R3-RF-2 (the production exclusion) | **The claim is narrowed to parity with the accepted X8/X9 gating** (LD-Q-191 D4; D2 superseded). The finite set and `classify` are withdrawn. The residual classes (compiler `--cfg` passthrough, renamed-dependency forwarding, `--manifest-path` roots) are **CP-TEST-FEATURE-EXCLUSION-1**. The guard and the graph check are kept, the check as defence in depth. | §4.3 |
| R3-RF-3 (`ids` outlives its owners) | `ids`, `index` and the order buffers drop at the end of step 3. Step 4 consumes `components.into_iter()` and re-extracts each publisher from the still-owned value, charged. | A.2 |
| R3-RF-4 (the census) | (1) the `name` lookup is added to both passes, and the passes are no longer claimed identical; (2) the sorts use `u32` order buffers **filled** with `0..n` before indexing (the lifecycle recipe), with every write charged; (3) `cmp_id` is three edges; (4) the refusal's row and cause strings are charged before construction, with Budget as the failure route; (5) the subject bound is 1024 UTF-8 bytes (256 scalars × 4), with a multibyte witness; (6) the empty catalog succeeds given allowance, and Budget only on genuine exhaustion. Independent work observations: C-F7 is an oracle-derived charge sequence plus a counting allocator. | A.1, A.2, A.3, A.6, A.7 |
| R3-RF-5 (step R's contracts) | The revocation carrier is named per path: durable, `PreDrawPhase.start.view`; read, `RetainedRead { inventory, view }`. `read_pre_draw` takes `Option<RetainedRead>`. `ProjectionRefusal::Revoked(TrustRefusal)` carries `Continuation("release:<digest>")` through both projections, with latching, and new controls C-A3i and C-R8. | §1.2, §1.6, §3.4, §4.2, §4.3, A.2 |

## r3 changes (answering REVIEW-r2; LD-Q-188 and LD-Q-189; kept for history)

| Finding or ruling | Disposition | Where |
|---|---|---|
| HC-2 items 1 and 2 | **Final** as interim M3 policies on REVIEW-r2's ADOPTABLE (LD-Q-188). Item 2 is restated as an explicit interim policy, **not** as an inference from DR-103. | §1.3 |
| R2-RF-1, the live universe (HC-2 item 3: ALTERNATIVE) | **Item 3′, the M3 closed-domain rule** (LD-Q-188 D1, provisional; its own R3 line). The live universe is the current authenticated catalog minus the releases the same read revokes. The enforcing owner is R10a/ER10a, and "no other admission or mount path at M3" is cited as an M3 fact. A wired command or registry custody reopens it. CP-REGISTRY-CUSTODY-1 replaces it. Both controls the reviewer asked for are added. | §1.3, §1.8 |
| The D1 stop: revoked component releases were not excluded | **Option 1** (LD-Q-189). P-1 gains **step R**: a component whose catalog `manifestDigest` is a `release` subject of the same read's admitted list refuses the whole view on the Continuation row, mirroring `admit_revocation`. The spelling is **COMPONENT-RELEASE-SUBJECT-r1**, its own R3 line. The live observer's gap is CP-LIVE-OBS-COMPONENT-RELEASE (not widened here). | §1.4, §1.8, §8 |
| R2-RF-2, funding completeness | Section 5, by the Fable pass (LD-Q-188 D3), covering step R too. | §5 |
| R2-RF-3, production exclusion | §4.3's production feature contract, by the Fable pass, under D2: a finite production invocation set (the LD-Q-129 precedent) plus an X9-style guard, every real production build command enumerated, and the guard verified unfiltered. | §4.3 |

## r2 changes (answering REVIEW-r1; kept for history)

| Finding | Disposition | Where |
|---|---|---|
| RF-1: HC-1 does not establish the host premises | HC-1 is withdrawn. **HC-2** (LD-SECPRE-HC2, provisional under LD-Q-185) states each premise's source. (1) Approved exceptions: an explicit empty M3 policy, since DR-103:994 has no product approval record and AQ:341 makes M3 first-party. (2) Host classifications: an explicit empty M3 policy, since DR-103:1385-1387 records the vocabulary as UNOWNED-AND-NEEDED. (3) Live names: **derived from the same read**, the signed collection of admitted manifests (DR-103:1059), with the live-name check kept on the security route. Each is one named site, with a corpus check that refuses nothing real and an owed carry. Item 3 is a charged sorted index. | §1.3, §1.4, §1.7 |
| RF-2: the promotion order and the equivalence overclaim | Order is live names, then approved exceptions, then host classifications (`component_manifest.rs`:304, :520, :539→:418). Equivalence is stated **on the domain of constructed `InventoryBody` values with the same reserved set**. The cross-stage precedence is documented, with the same public row. Combined-failure controls are added. | §1.5, §1.8 |
| RF-3: funding does not cover the work | A complete census covers the mark allocation and clone, every lookup (a proved bound for any ordered search tree), the promotion's access recipe, the live index (exact per-comparison charges), the inputs view and the checks. Executed work is separated from pre-bounds, and allocation is separated from residency. The `viewed` flag is removed (§3.2). | §5 |
| RF-4: the continuation lacks inputs, and its drop order was wrong | The acquisition **takes ownership** of the very `ProjectInputs` values R4–R10 borrowed (`OwnedProjectInputs`). Handoff borrows them again. Field order is fixed to the one-phase `begin`'s cleanup order, with interleaved `cfg(test)` drop probes. A host control runs acquisition → return → handoff across a function return. | §3.1, §3.3, §4.3 |
| RF-5: the read refusal sum, the no-view domain and the take controls | `ReadSessionRefusal` wraps `ReadRefusal { Session(SessionRefusal), Trust(TrustRefusal), Invariant }`. P-1 runs through a new typed session-ledger step that latches and keeps the trust refusal. The read path covers only complete I (E-4 is no view); **E-3 has no session** and is CP-J2C-SECPRE-1's. The second take is `Receipt(T::Invariant)` and the third is `Gate(Latched)`. | §4.1, §4.2 |
| RF-6: the read-side success boundary | Cleanup (`abandon`, which yields nothing) is separated from the success continuation (`proceed`, which yields `ReleasedReadSession`). `proceed` checks the acquisition's view state and mark. ER10a's success precondition is J2c's join, with named controls, as J3d's is for R10a. | §3.2, §4.2 |
| RF-7: the production exclusion | The production feature contract is a pinned effective-graph check, `check_fixture_exclusion_v1.py`. It reads `cargo tree` normal+build edges with features, for all targets, from every production root. It has mutations for direct, forwarded, build, target-specific and workspace-inherited enables. The release compile-fail is isolated in its own crate. The fixture site types are named. | §4.3 |
| LD-Q-185 (a)–(d) | (a) a corpus check over every real or will-admit manifest; (b) one named site per policy, with controls; (c) carries CP-ID-DEP-12 and CP-REGISTRY-CUSTODY-1; (d) a sorted index with an over-limit witness. | §1.7, §1.4, §8, §5 |

## 0. What this record selects, and what it does not

**Selected:**
- the split of `operation_handoff::begin` at R10/R11 into two private phases, with `begin` their exact composition
  (§3);
- the retention of R10's own authenticated inventory evidence (P-0), and one named security-owned projection, P-1,
  under HC-2 (§1);
- the public opaque boundary types for the durable path (R10 → R10a → R11) and the ephemeral path (ER10 → ER10a →
  release, complete-I sessions only), with their refusals and controls (§2, §4);
- option F's acquisitions: crate-visible production, and public only under the joint fixture predicate (§4.3).

**Not selected:**
- any production public R3–R10 or ER3–ER10 entry (CP-J3D-SECPRE-1, CP-J2C-SECPRE-1);
- ER10's production report-only read;
- ER10a's no-session (E-3) branch (CP-J2C-SECPRE-1);
- any change to J1's order, X2's lease terms or X4's first-read semantics (§6);
- any new public code or row;
- any populated host context (CP-ID-DEP-12, CP-REGISTRY-CUSTODY-1, and the approval-record owner when one exists).

## 1. A-RF-1: the right evidence, from the same read

### 1.1 What R10's read authenticates, and where it is lost (unchanged from r1; REVIEW-r1 §1 accepts the trace)

- **The call chain.**
  1. `begin` (`custody/operation_handoff.rs`:1218-1222) calls `trust_start` (:1038-1141).
  2. `trust_start` calls `fenced_operation_read` (`trust/live_observation.rs`:113-145).
  3. That calls `bootstrapping_first_read` (`trust/trust_bootstrap.rs`:1239-1265), then `fenced_first_read`
     (`trust/floor_publication.rs`:948-972), then `admit_current`, then `admit_bound`
     (`trust/current_trust_admission.rs`:1066-1200).
  4. `admit_bound` calls `authenticate` (:676-736), which calls `prepare_authenticated_times`
     (`trust/ordinary_targets.rs`:569-599), which calls `prepare_scoped` (:350-418).
  5. `prepare_scoped` builds `ScopedEvidence { inventory: I::Evidence, planning, component_authorities }`.
- **What `I::Evidence` holds** (`trust_ordinary_metadata.rs`:265-370):
  - the retained pairs, each holding its authenticated body and envelope as `Arc<[u8]>`
    (`trust/retained_metadata_index.rs`:555-571);
  - the catalog value and the release index;
  - per component, in `members.manifests` order (`trust_ordinary_quorums.rs`:164-199), which is the catalog order:
    the path, an `InventoryBody` (`validate_inventory` against the catalog's `reservedRootCommands`) and the joined
    release row.
- **The joins it checks** (:329-365): the envelope namespace equals the publisher, plus the body digest, the preimage,
  the envelope digest and `hostCore`.
- **Component signature authorities.** These are verified per component, in inventory order, when TR-COMPONENT
  remains (`ordinary_targets.rs`:380-406).
- **Where it is lost.** `admit_bound` keeps only `ViewClosure` (:1088-1093) and drops the rest. `AdmissionView` needs
  `&Validated` (`trust_admitted_components.rs`:14-34), and `component_manifest.rs`:56-57 forbids converting an
  `InventoryBody` "without executing the full host checks". `MD::prepare` has no production caller, and calling it
  would be a second read.

### 1.2 P-0: retention by move, no new read (unchanged from r1)

- **`ViewInputs`** gains a private `retain: bool`. The pre-draw acquisitions set it; `begin` and every other caller
  pass `false`. That is 13 constructor sites at `462a7a7e`: 11 in test files and 2 in
  `trust/live_observation.rs`.
- **The retained values.** With `retain` set, and the read `ReadMode::Fenced { .. }`, `admit_bound` moves
  `input.times.proof.scoped.inventory`, `component_authorities` and the TR-COMPONENT bit into a private
  `RetainedInventory`. The returned `AdmittedCurrentTrust` carries it as `Option`.
- **The reserved set.** `inventory::prepare` keeps its reserved set in `I::Evidence` by move (as LD-D4-13 did).
- **Bootstrap.** On the bootstrap branch, the retained value is the confirming admission's.
- **Taking it out.** `trust_start` takes the value out with `AdmittedCurrentTrust::take_retained` before the view
  moves toward the guard.
- **Without `retain`,** `admit_bound` drops `input` exactly as today.
- **The revocation carrier (r4, R3-RF-5).** Step R reads the same read's admitted list,
  `AdmittedCurrentTrust::revoked_subjects()`. P-0 does not copy it.
  - **Durable:** the view stays in `PreDrawPhase.start` (`TrustStart.view`) for all of P-1, and P-1 borrows it from
    there.
  - **Read:** the report-only read's whole `AdmittedCurrentTrust` moves into a crate-private carrier,
    `RetainedRead { inventory: RetainedInventory, view: AdmittedCurrentTrust }`. Only that read, with `retain`, makes
    one, so there is no caller-asserted list. `read_pre_draw` takes `Option<RetainedRead>`. P-1 borrows
    `view.revoked_subjects()` and drops the view after P-1.

### 1.3 HC-2: the host-context premises (LD-SECPRE-HC2: items 1 and 2 FINAL under LD-Q-188; item 3′ provisional, scored in r3)

The full validator's context has three premises: `live_names` (`component_manifest.rs`:304-310), `approved_exceptions`
(:520) and `host_classifications` (:418-428). The reserved set is not a host premise: it is the catalog's own
`reservedRootCommands`, which P-0 retains. For each premise, HC-2 names its source, and one code site holds it
(LD-Q-185 (b)).

1. **Approved exceptions: `APPROVED_EXCEPTIONS_M3`, an explicit empty policy.**
   - The site is `pub(crate) const APPROVED_EXCEPTIONS_M3: &[&str] = &[];` in `trust_pre_draw.rs`.
   - **The basis:**
     - DR-103:994 (`docs/coop/artifacts/component-manifest-schemas.v11.json`): the only lawful prerequisite is "an
       explicitly product-approved customer-owned external-system exception" carrying `exceptionApprovalRef`, "the
       product approval record".
     - No product approval record exists or is minted in M3.
     - M3-D r5 item 24 (AQ:341): "At M3 every admitted closure is first-party".
   - **The effect:** a manifest with any prerequisite refuses with `Error::Exception` on the security route. REVIEW-r1
     RF-1 accepts this form ("An explicit empty exception policy can refuse prerequisites").
   - **The successor:** the product approval-record owner, when one exists, replaces this one site.
2. **Host classifications: `host_classifications_m3()`, an explicit empty policy.**
   - The site is `pub(crate) fn host_classifications_m3(_path: &str) -> &'static BTreeMap<String, String>`, which
     returns a static empty map.
   - **The basis:** an **explicit interim M3 policy** (LD-SECPRE-HC2 item 2, final under LD-Q-188), selected because
     DR-103:1385-1387 (ID-DEP-12) records the classification vocabulary as "UNOWNED-AND-NEEDED". The policy is chosen;
     it is **not** inferred from DR-103. DR-103 records a gap, not an equivalence to an empty map (REVIEW-r2 §2,
     item 2).
   - **The effect:**
     - a configuration whose classification map is non-empty refuses with `Error::Configuration`;
     - an empty configuration (`properties {}`, `classifications {}`) passes, and the full validator gives exactly that
       result against an empty host map.
   - **REVIEW-r1's counterexample** stays valid for populated contexts, and the populated-context validator controls
     stay. This policy deliberately selects a different, interim premise. The vocabulary owner must replace it
     before any real manifest that needs a classification is admitted (LD-Q-185 (a)'s stop).
   - **The successor:** CP-ID-DEP-12 replaces this one site with the minted vocabulary's map.
3. **Live names: `live_universe_m3(&RetainedInventory, &[(String, String)])`, item 3′, the M3 closed-domain rule.**
   This is LD-Q-188 D1, adopted provisionally, and it becomes final only on its own R3 line. It is REVIEW-r2's offered
   alternative.
   - **The rule.** In M3, an entry is **live** if and only if both hold:
     - it is a component of the current authenticated catalog that this R10 or ER10 read admitted;
     - its release is **not** revoked by the same read's admitted list. A revoked release refuses the whole view at
       step R (§1.4), so it never reaches the live index.

     The rule is a **policy restriction** stated by this record and enforced by the security trust owner. It is not
     inferred from missing registry fields.
   - **Why the rule is complete in M3** (an M3 fact, cited). No component can be admitted, mounted or run in M3
     except through R10a or ER10a over this read's view:
     - J1 r7 S19 (`host-pipeline-j/PROPOSAL-r7.md`:913): "Row 8's closure admission becomes a selection among the
       component manifests that R10a, or ER10a, admitted. It adds no admission of its own".
     - M3-D r5 item 24 (`supervisor-d/PROPOSAL.md`:789): "no command is wired at M3 (J1 item 1)".

     So an entry outside the current catalog (for example, a tree retained in the component store from an earlier
     catalog) is not live. It can be neither admitted nor mounted in this invocation.
   - **What reopens it.** Item 3′ reopens, and must come back to R3 and the coordinator, if any of these appears: a
     new admission or mount path (any wired command), registry custody records, or a second source of live entries.
   - **Transitions.** The live set is re-derived on every read. When a catalog is replaced, the next read's catalog is
     the universe. A component removed from the catalog is not live from that read on. A revoked release refuses the
     whole view (step R).
   - **The completeness premise** holds by the rule's own definition. When the read has no trust view (E-4) there is
     no catalog, no P-1 and no admission.
   - **Unchanged:** each live entry's names, which are its root-namespace key set (`name`, `aliases` and, for an
     `analyzer`, its parentless command's aliases; `component_manifest.rs`:180-311; DR-103:1172); its identity
     `(stableId, provenance)`, with closed provenance `{publisher, sourceClass}`; and the charged sorted-index
     algorithm of §1.4, which REVIEW-r2 judged "a sound collision algorithm for the supplied universe".
   - **The effect:** RJ-2's live-name collision keeps its security route (`Error::Command` →
     `PayloadNotAdmissible("inventory")`).
   - **The successor:** CP-REGISTRY-CUSTODY-1 replaces this site.
   - **Rejected alternatives:**
     - an empty live set (REVIEW-r1 RF-1);
     - inferring completeness from absent fields (REVIEW-r2 R2-RF-1);
     - a caller-supplied context;
     - a second trust read.

**Control C-HC2-site.** A source census finds that `promote`'s context is read only from these three sites, and that
each site occurs exactly once. Each site has a unit test that pins its value: an empty slice, an empty map, and a
derivation that equals the catalog's non-revoked components and their key sets on the five-component signed fixture.
The item 3′ controls (REVIEW-r2 R2-RF-1) are:
- **C-HC2-3a: a live entry outside the current catalog.**
  - **Setup.** A component store holds a retained tree for component B from an earlier catalog. B has a different
    identity and a key `x` equal to the current catalog component A's name.
  - **Result.** P-1 admits A. B is not live and cannot be admitted, because it is absent from the view, and R10a is
    the only admission path.
- **C-HC2-3b: a non-live catalog entry.**
  - **Setup.** The current catalog holds A and B, where B collides with A on `x`, and the same read's list revokes
    B's release (its `manifestDigest`).
  - **Result.** Step R refuses the whole view on `Continuation("release:<B's digest>")` **before** the live index.
    With the revocation entry removed, the live index refuses A and B (RJ-2).

### 1.4 P-1: the projection (owner: the security trust owner; new work, priced in §5)

P-1 runs once on the fenced owner's ledger, consumes `RetainedInventory`, borrows the same read's admitted
revocation list, and builds `PreDrawEvidence`. Its steps are r5's A.2 algorithm. **r6:** they are priced under §5's
trust-reader basis, with uncharged in-memory work and only the new allocations charged. In order:
0. **the cap premise (r6, LD-Q-196).** `n ≤ MAX_CATALOG_COMPONENTS_M3` (20) is checked **before anything else**: the
   mark, the allocations, the authority check and step R. Over the cap, P-1 refuses `TrustRow::Budget`, fail-closed,
   with no P-1 allocation;
0′. **the attempt mark (r7, R6-RF-2).** P-1's first allocation: the `owned(16)` debit, then `Arc::new(AttemptMark)`.
   A refused debit returns `Budget` with nothing allocated;
1. the authority premise;
2. **step R**, the release-revocation check (LD-Q-189; COMPONENT-RELEASE-SUBJECT-r1);
3. the hold vector;
4. the live index under item 3′: an identity vector, count and fill passes, the reader sort (`reader_merge_sort`: `owned(4m)`
   buffers, uncharged comparisons), and the run pass with its marks;
5. per component: association, pair resolution, promotion, and the moves into the hold;
6. the drops.

**How to read this text under r6's funding basis (§5, FB-1 r4).** The algorithm, the borrow scopes, the order and the refusals below are operative and unchanged. The labels N1–N9 only **name** each operation. Under §5's trust-reader basis, an operation is charged only if it allocates:
- N2, N7 and N9 become `owned(b)` for their allocations;
- the two sorts are the local `reader_merge_sort`, with `owned(4m)` buffers and uncharged comparisons. Read every `merge_sort(..)` below as `reader_merge_sort(..)`, because §5 §1a excludes `component_closure::merge_sort`;
- every other N-labelled operation is uncharged: N1 lookups, N3 pushes into charged capacity, N4 reads, writes and lengths, N5 comparisons, N6 clones and N8 appends.

Before step 1 come **step 0, the cap premise, and step 0′, the attempt mark** (§1.4). r5's per-operation rules 1 and 3 and its census are withdrawn (LD-Q-195).

**P-1's funding failure points (r7, R6-RF-1).** The only places P-1 can refuse `Budget` are its `owned` debits, each
immediately before its one allocation: the mark (0′), `subjects` (R.2), step R's sort buffers, the refusal string
(R.5), the hold, `ids`, `index`, step 3's sort buffers and `collided`. These are FB-1 r4's allocation rows. No lookup,
read, write, length, comparison, clone or append is charged, and none of them can refuse `Budget`. The text below has
been normalized to this where it previously spoke of a debit for a non-allocating operation.

#### 1.4a P-1's algorithm (r5 §5 A.2, verbatim from here on)

**Borrow scopes** (r4, REVIEW-r4 §1 "sound at design level"):
- Steps R and 3 borrow `components` immutably, and every borrow they create is dropped at the end of its step.
- Step 4 consumes `components.into_iter()`.
- The revocation list is borrowed from the same read's view. Durable: `PreDrawPhase.start.view`. Read: the private
  `RetainedRead { inventory, view }`.

1. **The authority premise:** N4 (length read). If `n > 0 ∧ authorities.len() ≠ n`, refuse `Authority`, with the
   cause `String::new()`.

**R. The release-revocation check.**
   1. N4 reads `R = revoked.len()`. If `R = 0`, step R ends.
   2. `subjects = N2::<&str>(R)`. Per entry: N5 `kind == "release"`; when equal, N3 push. Then `R_rel =
      subjects.len()`, read with N4.
   3. **The order:**
      - `R_rel = 0`: step R ends.
      - `R_rel = 1`: there is **no order buffer and no sort**. The single subject is probed directly (step 4).
      - `R_rel ≥ 2`: `ord = merge_sort(R_rel, work, |a, b| subjects[a] < subjects[b])` (reused).
   4. **Per component `i`, in catalog order:**
      - N1 `release_i.get("manifestDigest")`;
      - `R_rel = 1`: one N5, `digest_i == subjects[0]`;
      - `R_rel ≥ 2`: binary search, with per probe one N4 (`ord[mid]`) and one N5 (`digest_i.cmp(subjects[..])`). At
        most `⌈log₂R_rel⌉ + 1` probes.
   5. **On a match, the funded refusal row (r7: one funding failure point):**
      - N7: the `owned(72)` debit, then `String::with_capacity(72)`;
      - N8 `push_str("release:")`, uncharged, within that capacity;
      - N8 `push_str(digest_i)`, uncharged, within that capacity (8 + 64 = 72 bytes).

      Then `ProjectionRefusal::Revoked(TrustRefusal { row: TrustRow::Continuation(s), cause: String::new() })`. If
      N7's debit refuses, P-1 returns `Budget` before the allocation, and nothing was emitted. The two appends
      cannot refuse.
   6. `subjects` and `ord` drop.

2. **The hold vector:** `N2::<HeldComponent>(n)`, skipped when `n = 0`.

3. **The live index** (skipped when `n = 0`).
   1. `ids = N2::<(&str, &str, &str)>(n)`.
   2. **The count pass, per component:**
      - N1 `stableId`, N1 `provenance`, N1 `publisher`, N1 `sourceClass`, then N3 push to `ids`;
      - N1 `name`;
      - N1 `role`, N5 `role == "analyzer"`;
      - N1 `aliases`, N4 (length);
      - for an analyzer: N1 `commands`; per command N1 `parent` and N4 (the root test); for the root, N1 `aliases`
        and N4 (length).

      `k_i` and `K` are formed by `checked_add`. This is pure arithmetic on registers, and no operation is debited.
   3. `index = N2::<(&str, u32)>(K)`. `K ≥ 1` always holds when `n ≥ 1`.
   4. **The fill pass, per component:**
      - N1 `name`, N3 push;
      - N1 `aliases`, then per alias N4 (element read) and N3 push;
      - N1 `role`, N5;
      - for an analyzer: N1 `commands`; per command N1 `parent` and N4; for the root, N1 `aliases`, then per alias N4
        and N3.
   5. **The order:**
      - `K = 1`: no order buffer and no sort; the run pass makes its end test only (step 6).
      - `K ≥ 2`: `ord = merge_sort(K, work, |a, b| index[a].0 < index[b].0)` (reused).
   6. **The run pass and the marks:**
      - `collided = N2::<bool>(n)`, then `n` × (N3 push `false`);
      - when `K ≥ 2`, this loop. Its N3, N4 and N5 labels name operations only; under §5 they are uncharged and
        cannot refuse (r7):

        ```text
        s = 0; mixed = false
        hs = N4(read ord[0]); hk = N4(read index[hs])                 // the run head's entry
        for p in 1 .. K:                                               // K − 1 iterations
            e = N4(read ord[p]); ek = N4(read index[e])
            if N5(ek.key == hk.key):                                   // same run
                if not mixed:
                    differ = N5(ids[ek.c].0 != ids[hk.c].0)
                          || N5(ids[ek.c].1 != ids[hk.c].1)
                          || N5(ids[ek.c].2 != ids[hk.c].2)          // up to three, stopping at the first difference
                    if differ:
                        mixed = true
                        for q in s ..= p: x = N4(read ord[q]); y = N4(read index[x]); N4(store collided[y.c] = true)
                else: N4(store collided[ek.c] = true)
            else: s = p; hs = e; hk = ek; mixed = false                // a new run starts at p
        ```

        The loop makes `K − 1` key comparisons, at most `K − 1` identity comparisons of up to three fields each, and
        marks each entry of a mixed run once. Every index access is its own N4.
      - When `K = 1`, the loop does not run: no `ord` exists, and no index is read.
   7. `index`, `ord` and `ids` drop.

4. **Per component, consuming `components.into_iter()`:**
   1. N1 `provenance`, N1 `publisher` (the re-extraction).
   2. N5 path equality, N5 namespace equality. A mismatch refuses `Authority`, with the cause `String::new()`.
   3. N1 `pairs.get(path_i)`, then N6 twice.
   4. **Promotion:**
      - N4 (`collided[i]`); if set, refuse `Manifest(Command)`;
      - N1 `prerequisites` and N4 (first element); if present, refuse `Manifest(Exception)`;
      - N1 `configuration`; if present, N1 `classifications` and N4 (length); if nonzero, refuse
        `Manifest(Configuration)`;
      - N4 (the move into `Validated`).
   5. N3 push to `hold`, then N4 (the release move).

5. `collided` and the unused remainder drop.

**Refusals: the complete enum and its routes** (this one definition replaces every earlier listing, per REVIEW-r4 §3
item 1):

```rust
enum ProjectionRefusal { Authority, Manifest(F::Error), Revoked(TrustRefusal), Budget(WorkBudgetError) }
```

- **`Authority` and `Manifest(_)`** become `TrustRefusal { row: PayloadNotAdmissible("inventory"), cause:
  String::new() }`. This allocates nothing (rule 2) and needs no debit.
- **`Revoked(t)`** becomes `t`: the row `Continuation("release:<digest>")`, funded at step R.5, with the cause
  `String::new()`.
- **`Budget(e)`** is the ledger's budget route.
- **Durable route:** `OperationRefusal::Trust(t)` or `Project(Gate(Budget))`. The gate is spent by `gate_step`'s
  failure path. The phase then drops in §3.3's order, which releases the fence.
- **Read route:** `read_pre_draw` **releases the session itself** before returning (REVIEW-r4 §3 item 5):
  - it calls `ReadSession::release()` on its own session, which "still releases its fence" even when latched
    (`installation_read.rs`:400-424);
  - it discards that call's result, because the **primary** P-1 refusal is the one returned;
  - it returns `ReadSessionRefusal { ReadRefusal::Trust(t) | Session(Gate(Budget)) }`, with no `ReadPreDraw`.

**Refusals,** with no new row. The complete definition is §1.4a:
`ProjectionRefusal { Authority, Manifest(F::Error), Revoked(TrustRefusal), Budget(WorkBudgetError) }`.
- `Authority` and `Manifest(_)` become `TrustRefusal { row: PayloadNotAdmissible("inventory"), cause: String::new() }`.
- `Revoked(t)` becomes `t`, `Continuation("release:<digest>")`.
- `Budget` becomes the ledger's budget route.

Durable: `OperationRefusal::Trust` or `OperationRefusal::Project(Gate(Budget))`, as at :1118-1134. Read: §4.2 and §1.4a. The read acquisition releases its own session.

**Where P-1 runs:**
- **durable:** one `gate_step` on the write gate's ledger (fence held, no project lock), followed by its gate recheck
  and receipt recheck (`ordinary_writer.rs`:367-398), after the floor step;
- **read:** one new typed session step on the session ledger, followed by the session recheck (§4.2);
- **never** on C2a-4's admission ledger, which `admission_view` alone charges at `admission_view_cost(n)` (§2.2).

### 1.5 Promotion: its domain, order and equivalence (RF-2)

```rust
// component_manifest.rs
pub(super) fn promote(body: InventoryBody, live_collision: bool, ctx: &HostContextM3) -> Result<Validated, Error>;
```

- **The domain** is `InventoryBody` values that `validate_inventory(b, r)` constructed, where `r` is the catalog's
  `reservedRootCommands`, the same set P-0 retains.
- **The order** is `validate_inner`'s order of the three context-dependent clauses:
  1. **Live names** (`name_checks` :304-310, reached directly or through `command_checks` :271-279): refuse
     `Command` if `live_collision`.
  2. **Approved exceptions** (:515-525): for each prerequisite in order, refuse `Exception` if its
     `exceptionApprovalRef` is not in `APPROVED_EXCEPTIONS_M3`. Under the empty policy, the first prerequisite
     refuses.
  3. **Host classifications** (`config_checks` :418-428, called at :539): when `configuration` is present, refuse
     `Configuration` unless its `classifications` equals `host_classifications_m3(path)` in length and in every
     entry. Under the empty policy, it must be empty.
- **The equivalence claim, on that domain only:**
  - for every `b` with `validate_inventory(b, r) = Ok(ib)`, `promote(ib, coll(b), HC2)` and `validate(b,
    Context(HC2))` agree on Ok or Err;
  - on Ok, the values are equal;
  - on Err, the error variant is the same.

  `coll(b)` is §1.4's collision bit, and `Context(HC2)` is the full context whose `live_names` are the other catalog
  components' `LiveName`s.
- **The reason it holds.** On that domain every context-free predicate of `validate_inner` has already passed: they
  are evaluated identically by `validate_inventory` on the same bytes and reserved set. So the full validator's first
  failure is its first failing context clause, in the order above.
- **Cross-stage precedence, documented and not claimed equal.** For a body that fails `validate_inventory`, the R10
  read itself refuses (`prepare_scoped` → `metadata_row` → `PayloadNotAdmissible("inventory")`), and P-1 never runs.
  The internal error variant can then differ from the full validator's first error: REVIEW-r1's example, a live
  collision plus a later duplicate dependency, gives `Dependency` against `Command`. The **public row is the same**,
  `PayloadNotAdmissible("inventory")`, because `metadata_row` maps every `Manifest(_)` to it. No public difference
  arises.

### 1.6 The ephemeral evidence source (ER10)

- ER10a follows X4T's report-only trust admission under the read session's fence (J1 r7:77, :493).
- The production report-only read is CP-J2C-SECPRE-1's. It passes `retain` (P-0 does not depend on the mode) and
  hands over `Option<RetainedRead>` (§1.2: the inventory together with that read's view).
- `None` means a complete I whose read found no trust view: F absent, which is E-4.
- With `Some`, the carrier is `RetainedRead { inventory, view }` (§1.2). The report-only read's `AdmittedCurrentTrust`
  moves in with its inventory, so step R reads that same read's list. CP-J2C-SECPRE-1 produces it.
- **E-3** (I positively absent) has **no read session** (J1 r7:496). It is outside this boundary, and is
  CP-J2C-SECPRE-1's by name.

### 1.7 Condition (a): HC-2 refuses nothing real (evidence)

The evidence is `evidence/hc2-corpus-v1/`, holding a script, its output and the corpus list, and is pinned in the
request's SUBJECT. It checks every manifest M3 admits or will admit:
- the TS1 fixture trees;
- F1's staged dist;
- the C2a-3 signed test closures, and every other first-party component manifest source in the product.

For each manifest it checks for a prerequisite, a typed-absence declaration under an exception, a non-empty
classification map, and a cross-component live-name collision. **Result** (`evidence/hc2-corpus-v1/RESULT.md`, exit
0): **no real or will-admit manifest is refused** by item 1, 2 or 3. That covers F4's closure vectors (T, S, P), F4's
tool output over real trees, and F4's output over F1's staged dist. The TS1 trees are analysed repositories with no
manifest. **Disclosed fixture interaction:** D4-2's `admission_fixture_bodies()` set, taken as one catalog, is refused
by item 3. It contains an explicitly-trusted analyzer with the same `stableId` and name but a different provenance.
That set is built through `AdmissionView::fixture`, never P-1, so no existing test changes. A future real-chain EE-1
corpus must give that manifest a distinct name, because RJ-2 (the security owner) refuses first, under M3-D item 24's
precedence.
**If any real manifest is refused, HC-2 item 1, 2 or 3 is wrong for M3, and this goes to the coordinator before
dispatch** (LD-Q-185 (a)).

### 1.8 A-RF-1 controls

- **C-A1a: the real chain.** For every `i`, `Arc::ptr_eq(hold.body(i), read_pair(path_i).body)` holds over a
  five-component signed chain (`trust/retention_fixture.rs` `with_roles`) through the actual fenced first read.
- **C-A1b: mismatch.**
  - Mutation 1 pairs `body_{i+1}` with component `i`; the release-digest check fails.
  - Mutation 2 takes a separately loaded copy of the bytes; the `ptr_eq` check fails.
- **C-A1c: no second read.** A source census finds no `MD::prepare`, `inventory::prepare`, `Budget::load` or store
  capture in P-1 or the hold, and the fixture store's access counter is unchanged across P-1.
- **C-A1d: authority.**
  - TR-COMPONENT below threshold refuses `Authority` with `PayloadNotAdmissible("inventory")`.
  - An authority namespace different from the publisher refuses the same way.
- **C-A1e: promotion equivalence.**
  - **Corpus:** the inventory293 and manifest268 fixtures, and the component-manifest unit corpus.
  - **Contexts:** HC-2; HC-2 plus an approved exception; HC-2 plus a matching classification map; and live sets with
    and without a colliding different-identity entry. In each, `promote` and `validate` agree in result, value and
    error variant.
  - **Combined failures** (RF-2):
    - an unapproved prerequisite plus a non-empty classification map gives `Exception` (not `Configuration`);
    - a live collision plus an unapproved prerequisite gives `Command`;
    - all three gives `Command`.
  - **Inventory failure plus host failure:** the read refuses before P-1, the public row is
    `PayloadNotAdmissible("inventory")`, and P-1 is never entered (an entry observer).
  - **Mutations,** each caught by a failing equivalence case: drop any one clause; and swap clauses 2 and 3.
- **C-A1f: order.** `view.components()[i].path()` equals `members.manifests[i].path`.
- **C-A1g: reserved identity.** The view's reserved set is the retained set (pointer identity), and equals
  `reservedRootCommands`.
- **C-A1h: the live index's equivalence.**
  - On generated catalogs (same-identity multi-version components sharing keys; different identities sharing a name,
    an alias or a root alias; disjoint), `collided[i]` equals "the full validator with the other components as
    `live_names` returns `Command` at the live clause".
  - **Mutations:** compare identity by `stableId` only; skip analyzer root aliases; and mark only the run's later
    entries.
- **C-CRS-1..5 (COMPONENT-RELEASE-SUBJECT-r1 §5):**
  - a revoked `manifestDigest` refuses on the Continuation row;
  - an `envelopeDigest` or preimage subject does not refuse;
  - an uppercase spelling does not match;
  - the core's `closure2:` handling is unchanged;
  - one digest covers every platform.
- **C-NC-21, C-NC-20, C-NC-site, C-NC-fit and C-SORT-0** (r6): the cap's over-limit witness, its boundary, its single
  site and its arithmetic guard, and the reader sort's charges (§5).
- **C-A1i: retired in r7 (R6-RF-1).** Its first-comparison edge failure cannot exist under §5, whose comparisons are
  uncharged. It is replaced by C-A1i′.
- **C-A1i′: over-limit witness at an allocation debit** (LD-Q-185 (d), checklist item 12; r7). An otherwise
  admissible two-component catalog with distinct live names, matching authorities and no revocations, run with a
  P-1 ledger whose object allowance covers the mark, the hold and `ids` but not `index`. P-1 refuses `Budget` at the
  index's `owned` debit, before the allocation: `index` is not allocated, no sort buffer is allocated, no comparison
  runs, and no component is promoted. The ledger shows zero edges (with C-SORT-0).
- **C-NC-21's paths (r7, R6-RF-2).** C-NC-21 runs on both the durable path and the read `Some` path. On each, the
  ledger and the counting allocator show zero P-1 allocations, **including no mark**.

## 2. A-RF-2: split before borrowing, and retain every owner through settlement

### 2.1 The order

```text
let mut pre   = <acquisition>;                       // R10 done: first read, floor, P-1. Fence held.
let core      = pre.take_core_evidence()?;           // forwarded; the receipt attempt's ledger (§4.1)
let (hold, cont) = pre.split();                      // consumes `pre`: no borrow of it can exist
let view      = hold.admission_view(scope)?;         // `scope`: C2a-4's admission ledger scope, inside its r10a_view
let mut frame = r10a_prepare(&view, &mut ledger, core)?;   // C2a-4's
let admitted  = r10a_admit(&mut frame, &store, ...)?;      // C2a-4's
let operation = join_admitted(&admitted, cont, &hold)?;    // host join (J3d): calls cont.hand_off(&hold) only here
```

`split(self)` consumes the pre-draw owner. `hand_off(self, &PreDrawEvidence)` consumes only the continuation.
`hand_off(&mut self)` is rejected (REVIEW-r3esc (a) Q3). REVIEW-r1 §2 judged this design substantially addressed.

### 2.2 The view constructor

```rust
impl PreDrawEvidence {
    pub fn admission_view<'h>(&'h self, work: &mut WorkScope<'_>) -> Result<AdmissionView<'h>, WorkFailure<()>>;
}
```

- It calls the existing `AdmissionView::collect(n, iter, &self.reserved, work)`, which charges
  `admission_view_cost(n)` first and then moves `AuthenticatedComponent::new(&path, &body, &envelope, &manifest,
  &release)` per held component.
- It performs no lookup, copy or state write: r1's `viewed` flag is removed (§3.2).
- C2a-4 calls it inside its own `r10a_view`, on its admission ledger's scope (C2a-4 sketch ack `28dd039a…`, item 1).

### 2.3 Lifetimes and teardown: a partial order (as r1, which REVIEW-r1 §2 accepts at design level)

| # | Relation (`a ≺ b`: `a` ends first) | Enforced by |
|---|---|---|
| T1 | `AdmissionView<'h>` ≺ `PreDrawEvidence` | Rust: the view borrows the hold (E0505/E0597) |
| T2 | `R10aFrame` ≺ view, ledger | Rust, C2a-4's types |
| T3 | `R10aAdmitted` (the pins) ≺ frame, store | Rust, C2a-4's types |
| T4 | every `ComponentHandle`, `PlanClosureSource` and `LaunchMember` ≺ `R10aAdmitted` | Rust, C2a-4's types |
| T5 | settlement of every spawned child ≺ its closure's pin release | **not by Rust.** CI-A3-c (`CI-A3-r4.md`:142-146); the J3d and J2c drivers, with delayed-child, cancellation and failure controls (CP-J3D-SECPRE-1, CP-J2C-SECPRE-1, C2a-4's CP-J3D-C2A4-1 (e)) |
| T6 | the hold outlives R11 | Rust: `hand_off` borrows `&hold` |
| T7 | the hold is unordered against `ProjectOperation` and the store | the hold holds no lock, fence or capability; its drop frees memory only |

**Prohibited:** `unsafe` (`lib.rs`:2 has `#![forbid(unsafe_code)]`), leaks, `'static` extension, self-referential
returns, and a view stored in the hold or the continuation.

### 2.4 A-RF-2 controls (real security types, from a dependent host test crate)

- **C-A2a.** The full chain of §2.1 runs, with the view and a component body used **after** `hand_off` returns,
  then the operation ends, then the view drops, then the hold drops. A stand-in frame borrows the view. The real
  security continuation is compiled and run here; it is not waived (REVIEW-r1 RF-4).
- **C-A2b.** Dropping the hold, or moving it, while the view is alive is E0505. Returning the view out of the hold's
  owner is E0515.
- **C-A2c.** `hand_off` after the hold drops is E0505/E0597. `take_core_evidence` after `split` is E0382.
- **C-A2d.** Every post-split refusal leaves the hold valid for every live borrower. The drop-probe sequence (§3.3)
  shows continuation, then view, then hold.
- T5's controls are the drivers'.

## 3. A-RF-3: the whole R10/R11 transition

### 3.1 The two private phases (`custody/operation_handoff.rs`)

```rust
pub(super) struct PreDrawPhase {        // private; not Clone/Default/serializable. Fields drop in declaration order:
    floor: OperationFloor,              //   this is the one-phase `begin`'s reverse-local order on a refusal before
    namespace_path: PathBuf,            //   the lease (floor, N's path, I/trust, the trust start, the target's owners,
    trust: RetainedDirectory,           //   the seam's hook and cadence, the lease mode), and last the writer, whose
    start: TrustStart,                  //   installation releases the fence.
    target: DetachedTarget,
    hook: ObservationHook,
    cadence: Cadence,
    lease: WriterLease,
    writer: OrdinaryWriteAdmission,
}
pub(super) fn pre_draw(writer, subject, lease, inputs: &ProjectInputs<'_>, invocation, seam)
    -> Result<PreDrawPhase, OperationRefusal>;                 // :1204-1222's steps, then `target.detach()`
pub(super) fn handoff(phase: PreDrawPhase, inputs: &ProjectInputs<'_>)
    -> Result<ProjectOperation, OperationRefusal>;             // :1223-1317's steps, after `target.attach(&mut writer)`
pub(super) fn begin(writer, subject, lease, inputs, invocation, seam) -> Result<ProjectOperation, OperationRefusal> {
    let phase = pre_draw(writer, subject, lease, inputs, invocation, seam)?;
    handoff(phase, inputs)
}
```

- **`NamespaceTarget::detach` and `DetachedTarget::attach`** (`custody/namespace_lease.rs`, `pub(super)`) move the
  target's private owners out and back, and nothing else. `lease` rechecks the subject, the directories and both
  carriers before its first lock (:830-875).
- **`handoff` destructures the phase in the one-phase local order:** writer, lease, cadence, hook, target, start,
  trust, namespace path, floor. A refusal therefore drops the bindings in `begin`'s reverse order, with the writer
  last.
- **The pause point** is after the first read and the floor step, before `lease_writer`.
- **Nothing is re-run at resume:** the endpoint join, the namespace admission, `trust_start`, `I/trust`, N's spelling
  and the floor step each run once, in `pre_draw`.
- **Retention is not part of the phase.** `begin` passes `retain: false` (P-0). The durable acquisition (§4.3) runs
  `pre_draw` with retention and then P-1 on the gate.
- **The inputs (RF-4).** `pre_draw` and `handoff` borrow `&ProjectInputs` exactly as `begin` does. The public
  boundary owns them (§4.3).
- **Dev evidence (G0), not a review subject.** This split, applied in the dev worktree at `462a7a7e`, compiles. Clippy
  `-D warnings` is clean. `cargo test -p opensip-security --lib` unfiltered gives 1330 passed, 0 failed and 7 ignored,
  with the same test names and outcomes as base `462a7a7e` (`work/g0-v2/`, `work/g0-base/`; the comparison is `work/g0-v2/compare-to-base.diff`, which is empty).

### 3.2 Same-attempt association and the success precondition

- **The attempt mark.** One `Arc<AttemptMark>` per acquisition; `AttemptMark` is private and zero-sized. On the
  durable path and the read `Some` path, P-1 allocates it after the cap (§1.4 step 0′). The read `None` path
  allocates a boundary mark (§4.2, r7).
  - **Durable:** the hold and the continuation each keep one reference. `hand_off(self, hold)` first checks
    `Arc::ptr_eq`. A mismatch refuses with a new crate-private `OperationRefusal::Association`, whose row is the existing
    `OperationRow::Installation(T::Invariant)` (so `installation_row()` gives `Some(T::Invariant)`). It spends the gate
    and drops the phase, which releases the fence, with no lease.
  - **Read:** the continuation keeps the mark **and** `had_view: bool` from the acquisition (§4.2).
- **The successful-admission precondition belongs to the host join, on both paths.**
  - Security cannot name `R10aAdmitted`. J3d's `join_admitted(&R10aAdmitted, DurableHandoff, &PreDrawEvidence)` is
    the only host caller of `hand_off`. J2c's `join_er10a(&R10aAdmitted, ReadHandoff, Option<&PreDrawEvidence>)` is
    the only host caller of `proceed`.
  - **The census:** C2a-4's source pin over the driver and `r10a.rs`, extended to these joins.
  - **The controls:** an R10a/ER10a refusal reaches `abandon`, never `hand_off` or `proceed`. These are owed by
    CP-J3D-SECPRE-1, CP-J2C-SECPRE-1 and C2a-4's CP-J3D-C2A4-1 item (e), and are not claimed here (C2a-4 confirmed,
    `28dd039a…` item 2).
  - REVIEW-r1 Q-5 accepts this division for the durable path.
- **r1's `viewed` flag is removed.** It proved only that a view had been built, not that admission succeeded, and it
  added unpriced state. Security keeps the attempt association, which it can prove.

### 3.3 `begin` unchanged (LD-Q-182 item 4), and the cleanup order

- `begin` is exactly `pre_draw` then `handoff`, with `retain: false`, and no P-1 runs.
- **The proof:**
  - every existing X2 and X4 control runs unfiltered, with the base pass set: the security lib (G0 dev result above),
    the host lib, and the crash-matrix `x2.*`/`x3d.*` rows (`--features crash-matrix`);
  - the source-text controls at `462a7a7e` stay unchanged and passing:
    - `trust/trust_bootstrap_tests.rs`:1255-1266: exactly one `fenced_operation_read(` in `operation_handoff.rs`, and
      none in `installation_session.rs` or `read_premise.rs`;
    - `trust/trust_bootstrap_tests.rs`:1598-1607: `trust_admitted_components.rs` stays byte-identical, so the hold
      lives in the new `trust_pre_draw.rs`;
    - `custody/operation_handoff_tests.rs`:973-985;
    - the crash-point and forbidden-token scans (`commit_session_tests.rs`:1035-…, `operation_guard_tests.rs`:~808);
    - `custody/installation_routing_tests.rs`:1074-1080;
    - `custody/ordinary_writer_tests.rs`:340-356.
  - A grep finds no hash pin over the changed files. `stale_pin_sweep.py` runs at code time.
- **The drop-order control (RF-4).**
  - `cfg(test)` drop-probe fields, each recording its index into a shared log, are interleaved between
    `PreDrawPhase`'s fields.
  - A probe after `writer` also checks the fence lock (probe-acquired), which must be **free**.
  - **Test 1:** dropping a `PreDrawPhase` records the probes in declaration order, with the fence free only at the
    final probe.
  - **Test 2:** the same holds for `DurablePreDraw` drop, `DurableHandoff` drop, `abandon`, a refusal inside
    `handoff` before the lease, and a refusal after the lease, where the append lock and the lease are observed
    released before the fence.
  - Field drop order is a language guarantee. The probes make it observable and catch a field reordering.

### 3.4 Terminal behaviour

| Event | Durable result | Fence | Lease | ExecutionId |
|---|---|---|---|---|
| refusal in `pre_draw` or P-1 | existing route; gate spent | released by drop | none | none |
| step R revokes a component (r4) | `OperationRefusal::Trust(Continuation("release:<digest>"))`; gate spent; `installation_row()` gives `Some(trust_termination(..))` (C-A3i) | released by drop | none | none |
| drop of `DurablePreDraw` (before split) | the gate ends with the writer (no spend call is needed: nothing can use it again); §3.3 order | released by drop | none | none |
| a take fails | the owner's `InstallationTermination`; a receipt failure spends the gate | held until drop/abandon | none | none |
| second take | `T::Invariant` | held | none | none |
| R10a refuses: the driver calls `abandon` | gate spent; drop the phase to the writer; then `OrdinaryWriteAdmission::release()`. A failed unlock is `gate_refusal(Io(Lock))`, the host I/O row (`ordinary_writer.rs`:76-83) | released, or its failure reported | none | none |
| continuation dropped without `abandon` | the phase drops in §3.3 order and the gate ends with the writer; no result | released by drop | none | none |
| `hand_off` after a spent or latched gate | `lease_writer`'s `fenced` refuses `Latched` (`ordinary_writer.rs`:473-475). No replay. | released | none | none |
| `hand_off` with another attempt's hold | `Invariant`, gate spent | released | none | none |
| R11 refuses | `begin`'s existing routes and order (:1191-1194, :1314-1317) | released | released before the fence | none |
| cancellation during R10a | the latch is a `FinalGate` source (X4 r8, S11), so `hand_off` meets `GuardStart::Latched`: the fail-stop row `latched` (:1274-1280) | released | released | none |
| success | `ProjectOperation`; fence released last | released | held | at R12 |

**J-C10b and SD9-T3.** The boundary-side half:
- no path here draws or reserves an analysis-attempt ExecutionId;
- a source census over the boundary's sources finds no `ExecutionIdReservations`;
- C-A3e, on 3a and ER10a (fixture), samples the registry at an injected R10a refusal and finds it equal to its value
  at entry.

3b's three outcomes and the creation-prelude case are CP-J3D-SECPRE-1's.

### 3.5 A-RF-3 controls

- **C-A3a: phase order oracle.** `begin` and `pre_draw` → `handoff` give identical step sequences. A re-run of
  `trust_start` or the floor step in `handoff` is caught.
- **C-A3b: attempt mismatch.** Two fixture acquisitions A and B, then `cont_B.hand_off(&hold_A)`, gives `Invariant`.
  B's fence is free, and no lease file is locked.
- **C-A3d: spent gate.** A receipt fault on the take, then `hand_off`, gives `Latched`, with no lease.
- **C-A3e: the reservation registry** is unchanged at an injected R10a refusal followed by `abandon`, on 3a and
  ER10a.
- **C-A3f:** `abandon`'s release error is the host I/O row (fixture unlock fault).
- **C-A3g: cancellation** between split and `hand_off` gives the fail-stop row `latched`, with no guard or observer.
- **C-A3i: release revocation, durable (r4).** A list naming component `i`'s `manifestDigest` refuses the
  acquisition on `Continuation("release:<digest>")`. The gate is spent, the fence is free, and no `DurablePreDraw`
  exists.
- **C-A3h: inputs across return** (RF-4). The acquisition runs in function F, which returns `DurablePreDraw`. A
  different function G then takes, splits, views and calls `hand_off`. It succeeds, and the guard's trust groups equal
  the acquisition's (identity of the owned inputs).

## 4. A-RF-4: usable public seams, under option F

### 4.1 The public surface (`opensip_security`, `#[cfg(target_os = "macos")]`)

```rust
pub struct DurablePreDraw { phase: PreDrawPhase, inputs: OwnedProjectInputs, hold: PreDrawEvidence }   // private fields
impl DurablePreDraw {
    pub fn take_core_evidence(&mut self) -> Result<AuthenticatedCoreRoles, InstallationTermination>;  // ordinary_writer.rs:53-62
    pub fn split(self) -> (PreDrawEvidence, DurableHandoff);
}
pub struct DurableHandoff { phase: PreDrawPhase, inputs: OwnedProjectInputs, mark: Arc<AttemptMark> }
impl DurableHandoff {
    pub fn hand_off(self, hold: &PreDrawEvidence) -> Result<ProjectOperation, PreDrawRefusal>;
    pub fn abandon(self) -> Result<(), PreDrawRefusal>;
}
pub struct PreDrawEvidence { components: Vec<HeldComponent>, reserved: BTreeSet<String>, mark: Arc<AttemptMark> }
impl PreDrawEvidence {
    pub fn admission_view<'h>(&'h self, work: &mut WorkScope<'_>) -> Result<AdmissionView<'h>, WorkFailure<()>>;
    pub fn len(&self) -> usize;
}
pub struct ReadPreDraw { session: ReadSession, hold: Option<PreDrawEvidence>, mark: Arc<AttemptMark> }
impl ReadPreDraw {
    pub fn take_core_evidence(&mut self) -> Result<AuthenticatedCoreRoles, ReadSessionRefusal>;  // installation_read.rs:183-194
    pub fn split(self) -> (Option<PreDrawEvidence>, ReadHandoff);
}
pub struct ReadHandoff { session: ReadSession, had_view: bool, mark: Arc<AttemptMark> }
impl ReadHandoff {
    pub fn proceed(self, hold: Option<&PreDrawEvidence>) -> Result<ReleasedReadSession, ReadSessionRefusal>; // success continuation
    pub fn abandon(self) -> Result<(), ReadSessionRefusal>;                                               // cleanup only
}
pub struct ReleasedReadSession { released: ReleasedRead }          // no public method; its lendings are CP-J2C-SECPRE-1's
pub struct ReadSessionRefusal { refusal: ReadRefusal }             // private: Session(SessionRefusal) | Trust(TrustRefusal) | Invariant
impl ReadSessionRefusal { pub fn termination(&self) -> InstallationTermination; }
pub struct PreDrawRefusal { refusal: OperationRefusal }
impl PreDrawRefusal { pub fn installation_row(&self) -> Option<InstallationTermination>; }
```

**Every type:**
- private fields;
- no `Clone`, `Copy` or `Default`;
- no serde, and no `From`/`Into` from public types;
- a `Debug` that is `finish_non_exhaustive` over values. `PreDrawRefusal` and `ReadSessionRefusal` print the row
  only, never a `TrustRefusal.cause` (§5, FB-1 r4 §4: rule 2, per route).

`AuthenticatedCoreRoles` and `PreDrawEvidence` have no public constructor.

**Forwarding is exact.**
- **Durable take:** a spent gate gives `T::Invariant`, and a receipt failure spends the gate (`ordinary_writer.rs`:
  53-62).
- **Read take** (`installation_read.rs`:183-194, `read_premise.rs`:107-120):
  - a latched or failed ledger gives `Session(Gate(Latched))`;
  - otherwise the receipt's result: the **second** take after a success is `Session(Receipt(T::Invariant))`, which
    latches;
  - the **third** gives `Session(Gate(Latched))`.

  RF-5 item 3 corrected r1's control expectation.

**`ReadSessionRefusal::termination`** keeps each owner's projection:
- `Session(r)` gives `session_refusal(&r)` (`installation_session.rs`:69-74): absent gives `NotInitialized`, a gate
  refusal goes through `gate_refusal`, and a receipt refusal keeps its row;
- `Trust(t)` gives `trust_termination(&t.row)`, the projection the durable path already uses for
  `OperationRefusal::Trust` (`operation_handoff.rs`:139);
- `Invariant` gives `T::Invariant`, the host-invariant row.

It is not the commit-session `SessionRefusal` (`lib.rs`:34-37), and the two types share no conversion.

**`PreDrawRefusal::installation_row`** gives `Some(T)` exactly for the `OperationRow::Installation(T)` routes. The
public projection of the `Project`, `Carrier` and `BudgetExhausted` routes is CP-J3D-SECPRE-1's. No route is
collapsed.

### 4.2 The ephemeral transition (RF-5, RF-6)

**The acquisition** (crate-visible) is `read_pre_draw(session: ReadSession, retained:
Option<RetainedRead>) -> Result<ReadPreDraw, ReadSessionRefusal>`. Its domain is complete-I read sessions only.
1. With `Some`, it runs P-1 through a new crate-private `ReadSession::charged_step<R, E>(&self, f) -> Result<R,
   StepRefusal<E>>` in `installation_read.rs`. The step refuses `Gate(Latched)` when the session is already latched.
   It runs `f` on the session ledger, then the session recheck. A failure latches the session and returns the step's
   own `E` (P-1's `ProjectionRefusal`), a ledger budget failure as `Gate(Budget)`, or the recheck's `SessionRefusal`.
   `ProjectionRefusal::{Authority, Manifest}` becomes `ReadRefusal::Trust(TrustRefusal { PayloadNotAdmissible(
   "inventory"), .. })`. Nothing is relabelled as a receipt or a generic gate failure.
   P-1's step 0 (the cap) precedes its step 0′ (the mark), so a cap refusal allocates nothing (r7, R6-RF-2).
2. With `None` (E-4), no P-1 runs and `had_view` is false. The acquisition allocates the **boundary mark** inside
   `charged_step`: the `owned(16) = {1, 0, 144}` debit on the session ledger, then `Arc::new(AttemptMark)`, then the
   step's session recheck, as on the `Some` path. A refused debit or recheck latches the session; the acquisition
   releases it and returns `ReadSessionRefusal` (the budget row, or the recheck's), with no `ReadPreDraw` (r7).

**The success continuation** is `proceed(self, hold)`. It accepts exactly:
- `(had_view = true, Some(h))` with `ptr_eq(h.mark, self.mark)`;
- `(had_view = false, None)`.

Otherwise it refuses `ReadRefusal::Invariant`, latches the session and releases it (its fence is unlocked). On
acceptance it calls the existing `ReadSession::release` (`installation_read.rs`:407): "the read session's equivalent
release ... comes before the capture session" (J1 r7:495). It returns `ReleasedReadSession`, the only value from which
CP-J2C-SECPRE-1's capture path continues.

**Cleanup** is `abandon(self) -> Result<(), ReadSessionRefusal>`. It calls the same `release`, which releases the
fence in every case ("A latched or failed session still releases its fence and lends nothing",
`installation_read.rs`:400-407). It returns `Ok(())`, or `Session(Gate(Latched))` for a latched session, or the
unlock's `Session(Gate(Io(Lock)))`, and never a `ReleasedReadSession`. A refused ER10a
therefore cannot reach a capture session or the ephemeral attempt's ExecutionId draw (J1 r7:498), because those
continue only from `ReleasedReadSession`.

**The success precondition** is J2c's join (§3.2). No lease, store or writer is touched (J1 r7:495).

**The read-side controls:**
- **C-R1:** a `Some` acquisition passed `None` refuses `Invariant`, then latches and releases.
- **C-R2:** another attempt's hold refuses `Invariant`.
- **C-R3:** a no-view acquisition passed `Some(hold)` refuses `Invariant`.
- **C-R4:** a real no-view acquisition: `split` gives `(None, cont)`, and `cont.proceed(None)` succeeds.
- **C-R4-mark (r7, R6-RF-2):** on the `None` path, the session ledger records exactly `{1, 0, 144}` for the boundary
  mark. With a session ledger that has no object allowance left, the acquisition refuses on the budget row before
  the allocation, the session is latched and released (lock probe), and no `ReadPreDraw` is returned.
- **C-R5:** an injected ER10a refusal, then `abandon`, gives `Ok(())`; a latched session, then `abandon`, gives
  `Session(Gate(Latched))` with the fence free (lock probe). `ReleasedReadSession` is unobtainable on that
  path: no value exists, a type-level fact, plus a source census that `abandon` returns `()`.
- **C-R6:** the take sequence success, `Receipt(Invariant)`, `Gate(Latched)`, each with its `termination()` row.
- **C-R7:** P-1's `Authority`, `Manifest` and `Budget` refusals on the read path, each with its `termination()` row
  (`PayloadNotAdmissible`'s row, `PayloadNotAdmissible`'s row, and the budget row), and the session latched after
  each.
- **C-R8 (r4):** step R's revocation on the read path gives
  `ReadSessionRefusal::termination() == trust_termination(&Continuation("release:<digest>"))`, latches the session,
  and returns no `ReadPreDraw`.

### 4.3 Acquisition under option F (LD-Q-182, LD-Q-185 item 1)

**Production, crate-visible:**

```rust
pub(crate) struct OwnedProjectInputs { trust_groups: BTreeSet<u32>, environment: Vec<(OsString, OsString)>, system_sources: Vec<PathBuf> }
pub(crate) fn durable_pre_draw(writer: OrdinaryWriteAdmission, subject: NamespaceSubject, lease: WriterLease,
    inputs: OwnedProjectInputs, invocation: &TrustInvocation, seam: GuardSeam) -> Result<DurablePreDraw, OperationRefusal>;
pub(crate) fn read_pre_draw(session: ReadSession, retained: Option<RetainedRead>) -> Result<ReadPreDraw, ReadSessionRefusal>;
```

**Inputs (RF-4).** The production entry builds `OwnedProjectInputs` once:
- `trust_groups` is the request's `--trust-group` set;
- `environment` and `system_sources` come from `first_registration::production_sources()` (`:2645-2653`).

It lends `ProjectInputs` views of these to R4–R9, then moves them into `durable_pre_draw`. So R11 uses the **same
values** R4–R10 admitted against: a move, never a re-derivation.
- `durable_pre_draw` lends them to `pre_draw`, keeps them in `DurablePreDraw`, and moves them into `DurableHandoff`.
- `hand_off` rebuilds the `ProjectInputs` view. The two `&Path` views (acquisition and `hand_off`) are the only
  new allocations. Both, and their fills, are funded on the gate's ledger (§5.1, r7).
- The guard's `inputs.trust_groups.clone()` (:1270) is `begin`'s existing step, unchanged.

**The owed carries.** CP-J3D-SECPRE-1 is the public production durable entry. CP-J2C-SECPRE-1 is the read entry,
including ER10's report-only read with `retain`, and ER10a's E-3 no-session branch. Both gate C2a-4d's production
wiring only.

**Public, under the joint fixture predicate only:**
- **Module:** `opensip_security::pre_draw_fixture`, `#[cfg(all(feature = "scenario-fixtures", debug_assertions,
  target_os = "macos"))]`.
- **Public items:**
  - `pub struct FixtureSite`, opaque, over a scratch home, with `pub fn create(roles: &[FixtureRole]) -> FixtureSite`
    and `pub enum FixtureRole { Analyzer, Toolchain, Stdlib, RustDevLlvm, Grammar }`;
  - `pub fn durable(site: &FixtureSite) -> Result<DurablePreDraw, PreDrawRefusal>`;
  - `pub fn read(site: &FixtureSite, view: bool) -> Result<ReadPreDraw, ReadSessionRefusal>`.
- **`FixtureSite::create`** runs the existing signed-component machinery (`trust/retention_fixture.rs`
  `with_roles`/`p0_site`, `custody/installation_read_fixture.rs`): real signing, a real P0 installation and real
  trust acceptance.
- **`durable`** runs, through `durable_pre_draw`:
  1. the real writer admission (`InstallationAt::writer`);
  2. X2's real root admission and tracking;
  3. the namespace;
  4. the real fenced first read;
  5. the real floor step;
  6. the real P-1.
- **`read`** runs a real read session. With `view`, it also runs `fenced_first_read` under `Fenced { report: true }`
  with `retain`, over the fixture fence. No component, body, release row, reserved list or core bundle is
  synthesized after the signing step.
- **The positive control starts outside security.** `crates/host/tests/pre_draw_boundary.rs` calls
  `FixtureSite::create`, then `durable` or `read`, and then the full chains of §2.1 and §4.2.

**The production exclusion (r4): parity with the accepted X8/X9 gating (LD-Q-191 D4).**

**Authorship.** The lead rewrote this block in r4. The guard, its unfiltered verification and the effective-graph
check are the Fable pass's r3 work (`fable-r3/SECTION-PRODUCTION-EXCLUSION-r3.md`, `98986e4b…`, B.3 to B.6), kept by
reference with its locked evidence (`fable-r3/evidence/`, SUMS `5baa9bde…`). r3's B.1 (the finite invocation set),
B.2 (the enumeration as a membership proof) and the `classify` contract are **withdrawn**. LD-Q-191 D4 supersedes
LD-Q-188 D2.

**The claim.** The fixture acquisition, `opensip_security::pre_draw_fixture`, is excluded from production builds
**at least as strongly as the accepted test-feature gates**: security's `scenario` module (X8 group J, X8a item 4f),
`crash-matrix` (X9 r1 item 2) and lifecycle's forwarded `scenario-fixtures`. It uses the same four fences, plus one
more check:

| Fence | `pre_draw_fixture` (this unit) | The accepted precedent it matches |
|---|---|---|
| 1. The module `cfg` | `#[cfg(all(feature = "scenario-fixtures", debug_assertions, target_os = "macos"))]` on the module | `scenario`: `#[cfg(all(feature = "scenario-fixtures", target_os = "macos"))]` (`lib.rs`:284). This unit's gate is stricter: it adds `debug_assertions`. |
| 2. The release guard | `#[cfg(all(feature = "scenario-fixtures", not(debug_assertions)))] compile_error!(…)` in `security/src/lib.rs`, after the crash-matrix guard (:6-9), with its census row in `crash_matrix_sites.rs` | security's `crash-matrix` guard (`lib.rs`:6-9) and storage's `crash-matrix` guard (`storage/src/lib.rs`:6-9), same pattern; lifecycle's `scenario-fixtures` guard (`lifecycle/src/lib.rs`:8-9), the same feature |
| 3. Plain-host unnameability | `host/tests/refusal/cases/security_pre_draw_fixture_unnameable.rs` (E0432) | `security_scenario_unnameable.rs` (E0432) |
| 4. The manifest pin | the module lives behind `scenario-fixtures`, which X8a item 4f's textual pin `scenario_fixtures_stays_out_of_release_manifests` (`host/tests/admission_tests.rs`:1683-1738) already keeps out of every release manifest. There is no new feature. | the same pin |
| 5. Defence in depth (new) | the effective normal+build feature-graph check, `tools/security/check_fixture_exclusion_v1.py`. It holds the r3 prototype's root inventory, the reaching/non-reaching/missing-evidence classification, the workspace unification and the manifest forwarding closure. It **drops** `classify` and the invocation-set membership. | none (the accepted gates have no graph check) |

**The guard, verified unfiltered** (Fable r3 B.3; the evidence is `fable-r3/evidence/guard-v1/`; REVIEW-r3 §3
compared the raw outcome rows):
- Base and guard give identical results on the four accepted fixture-enabling test builds, each run unfiltered:
  - security: 1330/0/7;
  - host: 646/3/64, with the three named `launch_recheck` actual-factory failures on both sides;
  - storage: 170;
  - lifecycle: 131 + 6 + 21.
- `--workspace`, `-p opensip-cli` and `-p opensip-launch` compile in dev, `--release` and `--profile harness` on both
  sides.
- The only build the guard newly refuses is `--release --features scenario-fixtures` on security, with the guard's
  exact text.
- **Disclosed:** `--profile harness` keeps `debug-assertions = true` (`Cargo.toml`:7-10, M3-O1 item 13), so the guard
  does not fire there. The same is true of the accepted `crash-matrix` and lifecycle guards.

**The residual classes the accepted gates share, now carried, not claimed.** **CP-TEST-FEATURE-EXCLUSION-1**
(LD-Q-191 D4, registered by the coordinator) is workspace-wide, covers every test feature, and is owned by a
build-policy owner. Each of these classes reaches `scenario`, `crash-matrix`, lifecycle's fixtures and
`pre_draw_fixture` alike:
- compiler passthrough, for example `cargo rustc -p opensip-security --lib -- --cfg 'feature="scenario-fixtures"'`
  (REVIEW-r3 R3-RF-2 item 1);
- feature forwarding through a renamed dependency alias (R3-RF-2 item 2). The defence-in-depth check is **not**
  claimed to resolve aliases, and its forwarding closure is documented as package-name based;
- `--manifest-path` and excluded-root invocations, which have their own workspaces (`providers/rust`,
  `tools/contracts`; R3-RF-1). Both are proved non-reaching by the r3 graph evidence (`exclusion-v1/clean.json`).
  This is recorded as evidence, not as a membership claim.

**Unchanged from r2 and r3:**
- the isolated release probe crate (`crates/security/tests/fixture_release_probe/`: its own `[workspace]`,
  `publish = false`, depending on `opensip-security` with `features = ["scenario-fixtures"]` only), built
  `--release`. It must fail with the guard's exact `compile_error!` text and no other crate's;
- the named `FixtureSite` types and the positive control starting outside security
  (`crates/host/tests/pre_draw_boundary.rs`);
- §4.4's fixture rows, as r3's B.6:
  - `pre_draw_fixture_unnameable` is E0432 in the plain host's dev, `--release` and `--profile harness` lib builds;
  - the isolated release probe shows the guard's text;
  - the module is present in host's `--lib --tests` build.

**What F does not give.** F gives no production public R3–R10 or ER3–ER10 entry. Under the accepted gating, no code
outside security can obtain a `DurablePreDraw` or a `ReadPreDraw` in a production build until CP-J3D-SECPRE-1 and
CP-J2C-SECPRE-1 land.

### 4.4 Privacy and compile-fail controls (each one file in `host/tests/refusal/cases/`, run by the existing harness)

**Kept unchanged:**
- `security_ordinary_writer_unnameable.rs` (E0603);
- `security_operation_guard_unnameable.rs`;
- `security_final_gate_unnameable.rs`;
- the commit-session clone, default, deserialize and literal cases;
- `security_scenario_unnameable.rs`.

**Added:**

| Case | Expected |
|---|---|
| clone / default / deserialize / literal, for each public type of §4.1 | E0599 / E0277 / E0277 / E0451 |
| `take_after_split`, `hand_off_twice`, `proceed_twice` | E0382 |
| `hold_dropped_while_viewed` | E0505 |
| `view_escapes_hold` | E0515 / E0597 |
| `fence_unnameable` (no installation, gate, receipt or fence accessor) | E0599 / E0616 |
| `core_constructor` (no public constructor of `AuthenticatedCoreRoles` or `PreDrawEvidence`) | E0451 / E0425 |
| `released_from_abandon` (binding `abandon`'s result as `ReleasedReadSession`) | E0308 |
| `read_session_refusal_not_commit` | E0308 |
| the fixture-module rows | as §4.3's Section B, B.6 (`pre_draw_fixture_unnameable` in dev, `--release` and `--profile harness`; the isolated release probe with the guard's text; presence in `--lib --tests`) |

## 5. Funding: the adopted trust-reader basis (FB-1 r4, incorporated verbatim)

> Source: `FB-1-r4.md`, sha256 `dfd803b5467b28528a8642f4a2d1e86ab65248cf403b02503f07ba19980f7682`, with its headings shifted two levels.

### FB-1 r4: the funding basis for P-1 under the trust-reader model, with the M3 component cap (LD-Q-195, LD-Q-196)

**Pins:**
- product `e8a62bbb8a226555075289791da5c273654e35f5` (identical to `462a7a7e` for every file cited);
- X4T `trust-admission-x4t/PROPOSAL.md` (r13, item 11).

**Rulings:**
- LD-Q-195 (`643ac6aa…`): price P-1 as part of the R10/ER10 read's own admission computation, under the accepted
  trust-reader model.
- LD-Q-196 (`e7e9547c…`): option C1, `N_C = 20`. `TRUST_VIEW_COST` is unchanged. This is provisional until R3
  scores it.

**r1:** `FB-1.md` (`508f7380…`, sent to the coordinator only) found that P-1 did **not** fit without a cap. r2 (`371838b5…`) applied C1. REVIEW-fb1 (`64a06de3…`) adopted
CAP-NC-20, with route (a), the budget row, and scored the funding line ALTERNATIVE (FB1-RF-1). r3 (`bbdbc0b2…`) applied the reviewer's alternative. REVIEW-fb1r3 (`8872c4f2…`) confirmed the sort, the
arithmetic and the fit, and required one correction, to §1a's read-wrapper row (FB1R3-RF-1). **This r4 makes only
that correction and two wording fixes.** It is the scored subject. Nothing else changes: the cap, its route
and the ceiling stay as they are.

**The r3 changes:**

| REVIEW-fb1 | r3 |
|---|---|
| **FB1-RF-1:** the reused `merge_sort` charges `COMPARISON_COST` per comparison, so P-1's edges were not 0. REVIEW-fb1's sorted witness of 4096 subjects used exactly 24,576 edges. The helper's documented bound is `m·⌈log₂m⌉`. | P-1 **does not call** `component_closure::merge_sort`, and that shared metered helper keeps its contract unchanged. P-1 uses a local **reader-model sort**, `reader_merge_sort` in `trust_pre_draw.rs`. It is the same stable bottom-up algorithm, but its comparisons and merge writes are **uncharged** (the reader model), and its two buffers are each funded with **`owned(4m)`** before allocation. Edges really are 0. Bytes rise by 512 (four record overheads). |
| §1 answer 1: a leftover "cap premise" charge | Removed. The cap check is an uncharged length comparison. |
| §1 answer 2: 11 objects is an upper bound across branches | Stated. Success paths allocate at most 10 objects; a revocation refusal allocates at most 5. The counting-allocator controls check upper bounds per path, never an equality with 11. |
| §1 answer 3: the margin wording | Corrected. One more charged object reaches 128 and still fits; two more reach 129 and fail. C-NC-fit's claim is bounded to arithmetic. |
| a sort boundary control | C-SORT-0, below. |

#### 1. The model and the ceiling

- **The reader model.** `Budget::borrowed(work)` charges the gate ledger:
  - one edge per load or visit;
  - one object plus the stored bytes per distinct retained record (`retained_metadata_index.rs`:105-120, :221-240).

  In-memory validation and joins over the retained, authenticated bytes are uncharged (for example,
  `validate_inventory`). They are bounded by those bytes.
- **The ceiling.** `TRUST_VIEW_COST = (128, 2048, 112 MiB)` (`current_trust_admission.rs`:34; X4T item 11).
- **P-1 under this model.** P-1 is the read's own admission computation over that retained data. Its lookups,
  comparisons, sorts and the promotion are uncharged, as `validate_inventory`'s are. **Only P-1's new allocations are
  charged**, each at `owned(b) = {1, 0, b + 128}` (`cost.rs`:10-16). That includes the two buffers of each
  reader-model sort, at `owned(4m)` each (`u32` indices). No comparison, lookup, write or length check is charged.

##### 1a. Reused primitives and the charges each brings (LD-Q-197, the lesson of FB1-RF-1)

**Rule.** A reused primitive brings its own charges. This table lists every existing function P-1 calls, or runs
inside, together with what that function itself debits. Entries marked "not used" are listed so that the exclusion is
explicit.

| Reused primitive | Used by P-1? | Its own charges | On which ledger | Inside `TRUST_VIEW_COST`'s fit? |
|---|---|---|---|---|
| `crate::cost::owned` with `WorkScope::charge` (`cost.rs`:10-16; `work_ledger.rs`:585) | yes: the 11 allocation rows of §3 | objects 1, bytes `b + 128`, **edges 0** | gate (durable), session (read) | **yes**: §3's object and byte terms |
| `component_closure::merge_sort` (`:392-430`) | **not used** (FB1-RF-1) | `sort_buffers_cost(m)` plus **1 edge per comparison** (`COMPARISON_COST`) | — | — |
| `COMPARISON_COST` (`component_closure.rs`:204-209) | **not used** | 1 edge | — | — |
| `reader_merge_sort` (new, local) | yes: steps R and 3 | its two `owned(4m)` buffers only, which are §3's rows; comparisons and writes **uncharged** | as `owned` | **yes** |
| `Budget::borrowed` and `Budget::load` | **not used**: P-1 loads nothing | — | — | — |
| `OrdinaryWriteAdmission::gate_step` (durable wrapper; `ordinary_writer.rs`:367-398) | yes: P-1 runs inside one gate step | `DurableWriteGate::scope` itself charges nothing. After P-1 the wrapper runs **`DurableWriteGate::recheck`** (`installation_admission.rs`:1008-…, through `gate.charged`, at its existing 468/X2 price, which includes edges) and **`WritePlatformReceipt::recheck`** (on the receipt attempt's ledger). | gate; receipt attempt | **no.** These are the gate's per-step rechecks. They are the same ones that follow `trust_start`'s first read and every other gate step, and they are priced by their owners. `TRUST_VIEW_COST` covers the read alone, and these rechecks are not part of it. Declared, not claimed to be zero. |
| `ReadSession::charged_step` (read wrapper; new crate-private, r2 §4.2), and the `ReadSession::recheck` it invokes (`installation_read.rs`:550-595), which includes `ReceiptRecheck::recheck` (`read_premise.rs`:179-188, :314-323) | yes: read path | **(r4, FB1R3-RF-1)** After a successful P-1, `ReadSession::recheck` runs three steps in order: (1) the read receipt's actor, core and platform rechecks, `ReceiptRecheck::recheck`, on the **receipt-attempt ledger** (`installation_read.rs`:564; `initial_installation.rs`:68-71, :280-305; `trust/initial_core.rs`:401-405; `trust/initial_platform.rs`:274-278); (2) the chain, required-and-captured-file and absence rechecks on the **session ledger** (:578-593); (3) the receipt rechecks **again** on the receipt-attempt ledger (:594). That is **two receipt rechecks on success**. Failures short-circuit and keep the existing refusal and latch behaviour. Each is charged at its owner's existing price. | receipt attempt (twice on success); session | **no.** These are the read path's per-step rechecks, priced by their owners and outside the read-plus-P-1 view-fit calculation. None is claimed to be zero. Their charges are not moved, folded or suppressed. |
| `AdmissionView::collect` (`trust_admitted_components.rs`:77-95, the charge; :104-115, the constructor) | after P-1, from C2a-4's `r10a_view` | `admission_view_cost(n)`: objects 1, bytes `n · size_of::<AuthenticatedComponent>()`, **edges 0** | C2a-4's admission ledger | no; it is unchanged and C2a-4's |
| `Arc::clone`, `String::new()` | yes | uncharged (reader model; no allocation) | — | — |

**Edges.** With the shared metered `merge_sort` replaced, P-1's own edge terms are **0**. The only other charges in P-1's step are the wrappers' existing per-step rechecks, each outside the view's fit:
- **durable:** the gate recheck on the gate ledger, then the receipt recheck on the receipt-attempt ledger;
- **read:** the receipt recheck, then the session recheck on the session ledger, then the receipt recheck again (r4).

#### 2. The cap, and where it is enforced (LD-Q-196, conditions 1 and 2)

- **The constant.** `pub(crate) const MAX_CATALOG_COMPONENTS_M3: usize = 20;` is the only site, in `trust_pre_draw.rs`.
- **Control C-NC-site** checks it in two ways:
  - a source census finds the constant defined once and read only by P-1's premise;
  - a unit test pins its value.

  A successor that raises `N_C` replaces this one site.
- **P-1's first operation** is the check `n = inventory.components().len() ≤ MAX_CATALOG_COMPONENTS_M3`. It comes
  before the authority premise, step R and any allocation, index or other work (checklist item 12).
- **When `n > 20`:**
  - P-1 refuses **fail-closed and before any work**, on the route scored by the reviewer (§5);
  - the hold, the continuation and the pre-draw value are none of them returned;
  - the durable path spends the gate, and the read path releases its own session (§5 A.2's routes, unchanged).
- **The controls:**
  - **C-NC-21**, the over-limit witness: a signed catalog of 21 components refuses at the premise, with zero P-1
    allocations (a counting allocator) and zero promotions;
  - **C-NC-20**, the boundary: 20 components admit, and the measured ledger use is at or below §3's bound.

#### 3. P-1's worst case at `n ≤ 20`, and the fit

**The input bounds:**
- `n ≤ 20` (the cap);
- `k_i ≤ 1 + 64 + 64 = 129`, from the `maxItems: 64` bounds on top-level `aliases` and command `aliases`
  (`tools/security/inputs/manifest-schema.json`:33, :578);
- `K ≤ 129 n = 2,580`;
- `R ≤ 4096` (`root_payload.rs`:1608).

**P-1's new allocations.** For each one, the soundness argument is a fixed element size times a schema-bounded or
cap-bounded count.

| Allocation | Objects | Bytes at most (`n = 20`) |
|---|---|---|
| mark | 1 | 144 |
| revocation subjects (`&str`, at most 4096) | 1 | 65,664 |
| step R's reader-sort buffers, 2 × `owned(4·4096)` | 2 | 33,024 |
| refusal row (on a match only) | 1 | 200 |
| hold (`HeldComponent`, 120 B) | 1 | 2,528 |
| ids (48 B) | 1 | 1,088 |
| index (24 B × K) | 1 | 62,048 |
| step 3's reader-sort buffers, 2 × `owned(4·2580)` | 2 | 20,896 |
| collided | 1 | 148 |
| **Total (an upper bound across branches)** | **11** | **185,740** |

The total is recomputed from the rows: r2's 185,228 plus r3's four record overheads of 128 bytes each. **Edges: 0**,
because the reader-model sorts charge no comparisons and the cap check is uncharged.

**Per-path upper bounds** (REVIEW-fb1 §1 answer 2):
- **a revocation refusal** returns at step R.5, before the hold and live index. It allocates at most the mark, the
  subjects, two sort buffers and the refusal row: **5 objects**;
- **success** allocates no refusal row: **10 objects** at most, 185,540 bytes;
- **the cap refusal** (`n > 20`) allocates **nothing** in P-1.

**C-SORT-0** (new, the sort boundary control). `reader_merge_sort(4096)` on a funded ledger debits exactly two
`owned(16,384)` charges, which is 2 objects and 33,024 bytes, and **0 edges**, whatever the input order:
- reversed;
- sorted;
- all equal;
- the 4096 lexically ordered non-matching `release` subjects of REVIEW-fb1's witness.

`component_closure::merge_sort`'s own controls are untouched.

**The read's own worst case.** This is a sound over-approximation, because it counts the payload closure that X4T's
128 figure omits:
- objects `53 + 16 + 7 + 2n = 76 + 2n`, which is **116** at `n = 20`. The 7 are the bundle body and envelope, the
  closure record, and the catalog and revocation pairs;
- bytes **56 MiB** charged (X4T's linear charge, 40 + 16 MiB);
- edges at most 2048.

**The fit:**

| Term | Read | P-1 | Sum | Ceiling | Margin |
|---|---|---|---|---|---|
| objects | 116 | 11 | **127** | 128 | **1** |
| edges | ≤ 2048 | 0 (r3: reader sort) | ≤ 2048 | 2048 | X4T's own |
| bytes | 58,720,256 | 185,740 | 58,905,996 | 117,440,512 | 58,534,516 |

**The margin is one object (condition 3).** One more charged object brings the sum to 128, which still fits. Two more
bring it to 129, which fails (REVIEW-fb1 §1 answer 3).
- **Control C-NC-fit**, a guard test, recomputes `76 + 2·MAX_CATALOG_COMPONENTS_M3 + P1_OBJECTS` from named
  constants:
  - `READ_FIXED_OBJECTS = 76`;
  - `READ_OBJECTS_PER_COMPONENT = 2`;
  - `P1_OBJECTS = 11`, which is the weighted object sum of the rows above: an upper bound across branches. The
    counting-allocator runs check **upper bounds per path**: at most 10 objects on success (C-NC-20, run at large `R`
    and `K`), at most 5 on a revocation refusal, and 0 on the cap refusal (C-NC-21).

  It fails if the sum exceeds `TRUST_VIEW_COST.0` (strict `>`). It also recomputes the byte sum against the
  headroom.
- **What C-NC-fit proves.** It checks arithmetic over the named constants, nothing more. It cannot detect a source
  change whose accounting constant was not updated, so the constants must be maintained with any change to the read's
  or P-1's allocations.
- **The other direction.** The fit holds **for P-1**. The read itself, for `n > 20`, still loads every manifest
  before P-1 refuses. That excess is the pre-existing gap below, not P-1's.

#### 4. What this replaces, and what falls away (LD-Q-195 items 4 and 5)

- **Withdrawn:**
  - r5's per-operation regime: rules 1 and 3, N1-N9 metering, the FUNDING-ORDER-CENSUS and C-F0/C-F11;
  - r4/r3 Section A's pass accounting.
- **R5-RF-1** (a token census that work can escape) and **R5-RF-2** (operand reads, and `promote` without a ledger)
  **fall away**:
  - no per-operation exactness is claimed;
  - `promote`'s work and all of P-1's in-memory work are inside the reader's accepted model, as `validate_inventory`'s
    validation is.

  The only explicit charges are the allocations above. The cap premise is an uncharged length comparison. REVIEW-fb1
  §1 answer 4 confirmed that R5-RF-1 and R5-RF-2 fall away.
- **Rule 2, the empty `cause`, is kept and restated per route:**
  - **P-1's routes**, durable and read: `TrustRefusal.cause = String::new()`. The projections read the row only:
    - `OperationRefusal::row` → `trust_termination(&row)` (`operation_handoff.rs`:133-142; `operation_guard.rs`:
      1006-1038);
    - `ReadSessionRefusal::termination()`;
    - the wrappers' row-only `Debug`.
  - **The reader routes are unchanged.** Their tests read or compare causes (`operation_live_tests.rs`:567-574;
    `current_trust_admission_tests.rs`:1120, :1171-1173, :1516), and `TrustRefusal` derives `Debug`, `PartialEq` and
    `Eq` for them. These are not P-1 consumers.

#### 5. The question for the reviewer: which route for "the catalog exceeds the stated cap"? (LD-Q-196 condition 1)

Either route is fail-closed and before any work.
- **(a) The budget row,** `TrustRow::Budget` (`WORK.BUDGET_EXHAUSTED`):
  - X4T item 11's own precedent: "A view over the ceiling refuses on the budget row; it is never truncated";
  - the closure's 40 MiB cap refuses on the same row (`closure_total`, `current_trust_admission.rs`:992-998).
- **(b) An admission row,** `TrustRow::PayloadNotAdmissible("inventory")`: it treats an oversized catalog as an
  inadmissible payload.

**The lead's reading: (a).** `N_C` is a resource cap that exists only to keep P-1 inside the view ceiling, and X4T
routes ceiling and closure caps to the budget row. Then `MAX_CATALOG_COMPONENTS_M3` joins `MAX_VIEW_EVENTS` and
`MAX_CLOSURE_BYTES`. The reviewer scores this as part of `CAP-NC-20`.

#### 6. Carry (registered by the coordinator, not fixed here)

**CP-X4T-CEILING-1**, for the X4T owner:
- (a) the fenced first read does not enforce `TRUST_VIEW_COST` in code, because `Budget::borrowed` uses the global
  limits;
- (b) X4T's 128-object figure omits the payload closure's component manifests;
- (c) the ordinary path has no member-count cap.


### 5.1 Boundary charges outside P-1 (r6, revised in r7; lead text, not part of FB-1)

These sites are not P-1. They are the acquisition and the continuations. **Each is listed with what it charges.**

| Site | Charge | Ledger |
|---|---|---|
| the acquisition's `ProjectInputs` view (`durable_pre_draw`, before `pre_draw`) | `owned(16·S)` for the `&Path` slice, then `S` × `{0, 1, 0}`, one immediately before each push within that capacity (r7; `S = system_sources.len()`, 5 in production) | gate, through the **proposed** adapter `OrdinaryWriteAdmission::gate_charge` over `DurableWriteGate::charged` (`installation_admission.rs`:969-979) |
| `hand_off`'s `ProjectInputs` view (after its mark check) | the same: `owned(16·S)`, then `S` × `{0, 1, 0}` | gate, `gate_charge` (proposed) |
| `hand_off`'s mark check, `Arc::ptr_eq` | `COMPARISON_COST`, `{0, 1, 0}` (`component_closure.rs`:204-209), charged immediately before the check | gate, `gate_charge` |
| `proceed`'s association check, `(had_view, hold)` and `Arc::ptr_eq` | `COMPARISON_COST` | session, `charged_step` |
| the read `None` path's boundary mark (§4.2 step 2; r7) | `owned(16) = {1, 0, 144}`, immediately before `Arc::new` | session, `charged_step` |
| the view, `PreDrawEvidence::admission_view` | `admission_view_cost(n)` (`trust_admitted_components.rs`:77-95; `collect` at :87-100), unchanged | C2a-4's admission ledger |
| the take | unchanged (`read_premise.rs`:107-120) | the receipt attempt |
| `abandon`, and the read acquisition's own release on failure | the existing `release` | — |

**Reused primitives here and their own charges** (LD-Q-197's rule):
- `gate_charge` is a **proposed** crate-private adapter; no such method exists at the pin (`ordinary_writer.rs`). Its
  body is one call to the existing `DurableWriteGate::charged` whose action is one `work.charge(cost)`. So it debits
  exactly its argument on the gate's ledger, refuses `Latched` when the gate is spent, and latches the gate on a
  budget refusal. It is not presented as implemented or executed;
- `COMPARISON_COST` is one edge;
- `owned` is one object plus `b + 128` bytes, with no edges;
- `charged_step` runs the session's per-step recheck and the read receipt's rechecks afterwards, as §5 §1a declares.

None of these sites is in the read-plus-P-1 view fit. On the read `None` path no P-1 runs, so the boundary mark's
one object sits beside the read's own 116 (117 ≤ 128).

**The input-view construction (r7, R6-RF-3).** This is outside P-1, and FB-1's allocation-only exemption is **not**
extended to it. Each view is built from the actual `S = system_sources.len()`:
1. `16·S` is formed with `checked_mul`; an overflow refuses `Budget` before any allocation;
2. if `S = 0`, the view is the empty slice: no allocation and no charge;
3. otherwise `gate_charge(owned(16·S))`, then `Vec::<&Path>::with_capacity(S)`;
4. then, for each of the `S` entries, `gate_charge({0, 1, 0})` immediately before one `push` within that capacity
   (debug-asserted: no growth).

**Failure point and cleanup.** Any of these debits can refuse. The gate is then spent (latched), the partial `Vec`
drops, and no pre-draw value is returned:
- at the acquisition view, `durable_pre_draw` returns `OperationRefusal::Project(Gate(Budget))` before `pre_draw`;
  `writer`, `subject`, `lease` and the owned inputs drop in their existing order, as for any refusal before the phase
  exists;
- at `hand_off`'s view, which runs after its mark check, the refusal spends the gate and drops the phase, releasing
  the fence, with no lease, as the mark-mismatch route does (§3.2).

**Control C-IN-fill (r7).** For `S ∈ {0, 1, 5}`, the gate ledger records, per view, exactly `owned(16·S)` plus `S`
edges (nothing for `S = 0`). A gate funded one edge short of the last push refuses `Budget` before that push, the
gate is spent, and no `DurablePreDraw` or `DurableHandoff` continuation is returned.

**Erratum to the incorporated FB-1 r4 (it is kept verbatim in §5).** Its §1a cites `AdmissionView::collect` at
"`:104-115`, the constructor". The correct lines are **:87-100** for `collect`, constructing at :96-99
(REVIEW-fb1r4 §1 item 4, which found this nonblocking). The price it states is correct.

## 6. The escalation triggers (REVIEW-r1 §3: NONE-FIRES)

**J1's order** is unchanged: P-1 is R10's last security step before R10a. **X2's lease terms** are unchanged:
`lease_writer` and `take_lease` are untouched, and `detach`/`attach` move owners only. **X4's first-read semantics**
are unchanged: the read admits and publishes the same, and P-0 moves values it built.

P-1 **adds** work and possible pre-R10a refusals, including RJ-2's live-name collision and the two policy refusals. As
REVIEW-r1 notes, "the first read is unchanged" is not a claim that the whole acquisition behaves identically or costs
the same.

**r3's additions (REVIEW-r2 §4, for r3's changes):**
- **Step R** adds a pre-R10a whole-view refusal on the existing Continuation row. It uses the same read's admitted
  list, by reference, and runs after the read. The read's own decisions, publications and epoch are unchanged.
- **Item 3′** changes which entries the live index treats as live, not the first read.
- **Section B's guard** refuses only builds without debug assertions that enable the fixture feature.

None changes J1's order, X2's lease terms or X4's first-read semantics.

## 7. Owners whose acceptance this needs

- **The security custody and trust owner:** this unit.
- **J1:** the order (§6).
- **J3d and J2c:** the joins, T5 and the carries.
- **C2a-4 and C2a-3:** T2–T4. They confirmed §2.1 (`ac837ab8…`, `28dd039a…`).
- **The coordinator:** HC-2 is final only on its R3 line. The owner is flagged at finality (LD-Q-185 item 2).

## 8. Not delivered, not claimed, carried

- **CP-J3D-SECPRE-1:** the production durable entry, the R10a join, J-C10b's 3b and creation-prelude cases, and T5's
  controls.
- **CP-J2C-SECPRE-1:** the production read entry with ER10's report-only read, the ER10a join, E-3's no-session
  branch, and T5's controls.
- **CP-ID-DEP-12:** the classification vocabulary, which replaces `host_classifications_m3`.
- **CP-REGISTRY-CUSTODY-1:** the registry custody records, which replace item 3′'s `live_universe_m3`.
- **CP-X4T-CEILING-1** (LD-Q-196; registered by the coordinator; the X4T owner). Three gaps, not fixed here:
  - the fenced read does not enforce `TRUST_VIEW_COST`;
  - X4T's 128-object figure omits the payload closure's manifests;
  - the ordinary path has no member-count cap.
- **CP-TEST-FEATURE-EXCLUSION-1** (LD-Q-191 D4; registered by the coordinator): the workspace-wide residual classes
  every test feature shares (compiler `--cfg` passthrough, renamed-dependency forwarding, `--manifest-path` and
  excluded-root invocations). A build-policy owner holds it.
- **CP-LIVE-OBS-COMPONENT-RELEASE** (LD-Q-189 item 5): the live observer (`live_observation.rs`:695) does not check
  component releases against later revocation lists. It is owned by that observer's owner and is not widened here.
- **The product approval-record owner** (none in M3): replaces `APPROVED_EXCEPTIONS_M3`.
- **SD-9:** acceptance of the hold's residency across R11.
- **The public projection of `OperationRow`:** CP-J3D-SECPRE-1.
- No lane, receipt, binding, integration or qualification claim. The G0 dev results are disclosed as dev evidence
  only.

## 9. Questions for the reviewer (r7)

- **Q-1:** do R6-RF-1, R6-RF-2 and R6-RF-3 close: C-A1i′ and §1.4a's normalized funding text; the mark as P-1's
  step 0′ after the cap, and the read `None` path's boundary mark; and the input views' fill charges and cleanup?
- **Q-2:** does the attached mechanical stale-text sweep (LD-Q-200) classify every hit correctly? Please spot-check it.
- **Q-3:** do A-RF-1 to A-RF-4 hold, so that the successor is ADOPTABLE?

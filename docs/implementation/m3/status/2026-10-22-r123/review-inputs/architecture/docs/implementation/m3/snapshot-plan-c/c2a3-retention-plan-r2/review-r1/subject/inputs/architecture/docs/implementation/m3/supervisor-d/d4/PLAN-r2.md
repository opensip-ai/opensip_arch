# D4 implementation plan r2: manifest admission, request predicates and the session factory (M3-D items 24-26)

**Lead plan, 2026-10-17. Proposed; it needs Codex review (round 2).**

**Bases:**
- product main `d704ed4` (D3a-3 integrated at `2fbb779`; inventory v227 bound at `234e00d`; S-OP-2c bound as contract successor 177);
- architecture `9415426c` (S-OP-2c published), and the files the subject manifest names.

Between r1's base `5de9fd4` and `d704ed4`, only `crates/components/src/supervisor.rs`, the new `supervisor_records.rs` and `crates/operability` changed among the files this plan cites. Every other cited product file is the same blob at both commits, so its line numbers stand.

## r2 changes (answering `codex-d4-plan-r1`)

| Item | Disposition | Where |
| --- | --- | --- |
| **D4PLAN-R1-RF-1** (price the ordering and all membership work) | **Fixed.** `admit` now has a specified algorithm: one charged digest sort over `u32` indices (CI-A1-b's recipe), a charged duplicate pass with a typed refusal, then two predicate passes (count, then fill) in sorted order, each priced identically. The policy sets are **sorted borrowed slices**, probed by charged binary search at the CI-A2-c price (at most ⌈log₂ m⌉ + 1 comparisons, one edge each), never `BTreeSet` lookups. EE-1's explicit-trust probe is in the recipe. The provider-relation table is a static, pinned projection of the embedded matrix, with no runtime build. The reserved list is borrowed from the reader's retained set, with its slice view priced. The complexity claim is now O(n log n + Σ keys · log m). The controls account for each site independently. | LD-D4-8, LD-D4-10, LD-D4-13; §3; §5 |
| **D4PLAN-R1-RF-2** (preserve budget and observation failures across the recheck seam) | **Fixed.** The seam returns `RecheckFailure {Budget(WorkBudgetError), Io{call, error}, Corrupt(CorruptCause)}`. The factory's refusal sum keeps each one distinct. Each takes CI r5 item 8's existing route for the retained-tree capability. `Corrupt` takes row 28's `DELIVERY.CLOSURE_BYTES_CORRUPT`, or `DELIVERY.CLOSURE_BYTES_MISSING` for `Absent`. `Io` takes `HOST.IO_FAILURE` with no detail. `Budget` takes the caller's budget route, row 11's `WORK.BUDGET_EXHAUSTED`. J1 r7's matrix has no row naming the recheck's `Io`, so that matrix row is carried as an explicit J2 gate (X-D4P-5). No code is added. All of them are pre-spawn. The controls cover one unit short before an open or hash, an I/O failure and each mismatch, through the factory. | LD-D4-11; X-D4P-5; §5 D4-4 |
| **Q1** (accepted, with the association preserved) | EE-1 reads `publisher` and `sourceClass` **from the catalog release row the ordinary reader joined** (`AuthenticatedComponent::release`), never from a caller or from the body alone. The lend is constructible only from an `AuthenticatedComponent`. At M3 the explicit-trust list is empty, an explicit policy choice consistent with AQ's first-party-only scope. A root-delegated namespace is not an explicit-trust entry. The signed `explicitly-trusted` fixture exercises the enforcing refusal. | LD-D4-3; LD-D4-12 |
| **Q2** (accepted as a backstop) | The relation table is the pinned projection of the matrix's members without a `fact` or `candidate-only` authority. Per the ruling, that filter distinguishes authority classes, and authorizes nothing outside CMS. `capabilityId` and `declarationData` consistency is CMS's, kept from the validated value. The controls exclude `inventory`, `clones-fact`, `clones-near` and `clones-cross-tsjs`. | LD-D4-4 |
| **Q3** (accepted) | The closed-world pin covers the nested representations too: CMS's top-level properties and its `$defs` `capability`, `platform`, `entry`, `command` and `dependency` property sets, plus `ManifestClaims`' nested claim types. It forces review when any of them changes. It is not an executed EE-4 negative. | LD-D4-5 |
| **Q4** (accepted) | Unchanged. Both (a) pins at D4's first integration; (b) and (c) are backstops; live names stay RJ-2's. | LD-D4-6 |
| **Q5** (accepted) | D4-T2 is recorded as unrepresentable, not as a passing corpus. A new request, flag or nested carrier requires re-review before landing. | LD-D4-7 |
| **Q6** (D4 consumes; the lead owns SD-9) | **Lead decision LD-D4-SD9.** The lead owns SD-9, R10a's work ledger (its aggregate model, caps and `Budget` projection), with the J1 and D4 admission owners. It is recorded as an **owed successor gating production R10a/ER10a composition, C2a-4 and J3d's and J2c's wiring, and no pure D4 sub-unit**. No interim profile follows from this plan; any interim needs SD-9's own accepted policy. | LD-D4-SD9; X-D4P-1 |
| **Q7** (accepted, subject to RF-2 and CI-A3) | **D4-4 waits for CI-A3's acceptance.** CI-A3 is the lead's to write, as DR-103's delivery owner, and is drafted alongside this round (`component-install/CI-A3-r1.md`). X-D4P-2 lists exactly what it must define. The pin stays alive through spawn by CI item 7's operation lifetime, and the factory borrows the operation's capability. | LD-D4-11; X-D4P-2 |
| **Q8** (accepted in boundary) | `Cleared` now carries the exact sorted digest list. The wiring must compare it with the authenticated component set it then hands to C2a, and run C2a only after it (X-D4P-4). | LD-D4-8 |
| **Q9** (accepted) | Every first-use outcome (`Published`, `LostRace`, `NotPristine`) and the ephemeral and no-trust-view cases are listed explicitly as J-C10b's path-owed cases. | §1; §7 |
| Review notes on D4-4's comparison sources | The spec check compares the **codec's assembled output** with **independent authorities**: the admitted selection from R10a's admitted set, the Plan's universe row (C4a), the verified signed descriptors (A2), and the protocol's pinned Hello limits (D2b's constants). It never compares two caller copies. C4a is named as a production dependency. | LD-D4-11 |
| Review notes on the reserved list and the reader | D4-2's scope includes the reader change. The ordinary reader **retains** its reserved-name set in its `Evidence`, a move, not a copy, so the lend borrows exactly the set the manifests were validated against. A JSON array is never treated as a set. | LD-D4-13 |

Everything else in r1 stands, re-grounded where the product moved.

**What precedes it.** D4's row in M3-D r5's units table is "`components/manifest.rs` at R10a, `components/session_factory.rs` and the `host/request.rs` predicates at R1: items 24-26", depending on D3a, SD-2 and SD-6 (met, r4), with "its own (a) check, not C2a (r5)", size M, control DR-G29 (`PROPOSAL-r5.md`:1262). The order is D1a → D2a ∥ D2b → D3a → D3b ∥ D4 → D5 (:1265).
- **Met:**
  - D1a (`crates/platform/src/process.rs`).
  - D2a (`crates/components/src/control_protocol.rs`).
  - **D3a, all three sub-units** (`supervisor.rs`: `SessionSpec` :793, `PreSpawnRefusal` :351, `Supervision::decline` :1339; `supervisor_records.rs`: `OwnerRoute` :361, with `ClosureBytesCorrupt`, `ClosureUnspawnable`, `HostInvariant` and `HostIo`).
  - SD-2, SD-5, SD-6, SD-7 and S19.
  - CR-1 and its materialization (`d579140`, status record E033).
  - C2a-1 and C2a-2.
  - J2a (R1's typed request).
- **Not met:**
  - D2b-3b and D2b-4;
  - CI-2 and CI-3 (in their lane, with CI-A2);
  - **CI-A3** (X-D4P-2);
  - C4a;
  - J3d and J2c;
  - **SD-9** (LD-D4-SD9).

**Authority:**
- **The law and its sources:** as r1. That is M3-D r5 items 24-26 (`PROPOSAL-r5.md`:752-878) with D4-T1 to D4-T4; items 2, 12 and 22 (:204-222, :425, :705-731); item 30 (:1211-1216); J1 r7's R1 (:382), R10a (:392, :404-416), ER10a (:493, :498), outcome rows 2, 11, 28 and 56-57 (:772, :781, :798, :826, :833), S20 (:914), J-C10b (:410-416) and J-C20 (:840); C2a plan r4; the component installation law r5 with CI-A1 (and CI-A2 as proposed); the D2b plan r3 with A1 and A2.
- **The product interfaces** on main `d704ed4`: as r1, with `supervisor.rs` re-pinned as above. Every other r1 citation is to an unchanged blob:
  - `component_manifest.rs`: `Validated` :35-55, `command_checks` :180, the one-root check :192, the name binding :196, `resolve` :313, `tree_checks` :334, `name_checks` :283 (reserved :301, live :304), `validate` :433, `validate_inventory` :436, dispatch :452-457, the CR-1 test :752;
  - `trust_ordinary_metadata.rs`: the reserved set :84-90, the release join :106-114, the namespace check :121-123;
  - `trust_admitted_components.rs` :13-62;
  - `verified_envelopes.rs`:71-72;
  - `process.rs`: `LaunchSpec::typescript` :204, `LaunchSpec::rust` :231, `ClosureRecheck` :335, `VerifiedLaunch` :346-358;
  - `work_ledger.rs`:12-14, :223, :242;
  - `control_protocol.rs`:1020-1044;
  - `ts2.rs`:100;
  - `invocation.rs`:31-127.

## 0. What D4 delivers, and what it does not

**Delivers** (as r1):
- `components/manifest.rs` (item 24);
- the R10a and ER10a lending and host adapter;
- `host/request.rs`'s R1 classification point (item 25);
- `components/session_factory.rs` (item 26), library only, with J2b its production caller.

**Not delivered** (as r1, and now explicit):
- the R10a and ER10a wiring (J3d, J2c, with C2a-4);
- SD-9 and any R10a profile;
- the public projections and the operational record (J1, through J2a, J3d and J2c);
- the provider-spoken substitution cases' codecs;
- C2a's admission, row 8's selection and J2b's selection;
- CI-A3 itself, which is the lead's law amendment, packaged separately (`codex-ci-a3-r1`);
- Linux.

## 1. The split (LD-D4-1): four sub-units, each its own review and lane

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D4-1** | `components/manifest.rs`: `ManifestClaims<'a>`, `AdmissionPolicy<'a>` and its charged order check (LD-D4-2, LD-D4-10); the four predicates (LD-D4-3 to LD-D4-6); `ExcludedForm`; LD-D4-8's algorithm | D4-T4 at D4's interface; D4-T1's interface half; RF-1's accounting controls | D3a (met) |
| **D4-2** | The reader keeps its reserved-name set (LD-D4-13); security's public `AdmittedComponentClaims`, constructible only from an `AuthenticatedComponent`; host's `component_admission.rs` with the pinned relation table (LD-D4-4); the host → components edge | D4-T4's positive case and source pins on signed fixtures of every role; EE-1 end to end; the no-trust-view case; the pin of the relation table to the embedded matrix | D4-1; C2a-1, C2a-2 (met); **after CI-2/CI-3 integrate**, which also touch `trust_admitted_components.rs` and `trust.rs` (§6) |
| **D4-3** | `host/request.rs`: `request_excluded_form`, exhaustive, with its pins (LD-D4-7) | D4-T2 recorded as unrepresentable | D4-1 (the type); J2a (met) |
| **D4-4** | `components/session_factory.rs` with the recheck seam and the refusal sum (LD-D4-11); the host's seam implementation over CI-3's capability through CI-A3's operation | D4-T3's host-observed half, extended by RF-2; the sole `VerifiedLaunch::from_recheck` pin | D4-1; D2b-3b; D2b-4 for Rust3; CI-3; **CI-A3 accepted**; C4a for production composition (typed synthetic inputs before it) |

**Order:** D4-1, then D4-3 (any time), then D4-2 once CI-2/CI-3 are on main, then D4-4.

**What D4 cannot claim (Q9).** D4-T1's path half is J1's J-C10b. It runs on:
- the durable path 3a;
- the first-use path 3b, once for each of `Published`, `LostRace` and `NotPristine`;
- the ephemeral path, with a trust view (ER10a's refusals) and without one (E-3, E-4: nothing admitted, nothing refused).

Each case asserts the reservation-registry state at the refusal's return, no draw, no spawn and the public route. D4-T1 is **interface-complete, path-owed** until J3d and J2c supply them. Neither interface acceptance nor signed-fixture success completes J-C10b, J-C20, DR-G29 or product qualification.

## 2. Lead decisions

- **LD-D4-1. The split** (§1).
- **LD-D4-2. D4 judges a pure borrowed projection.** As r1, with these changes:
  - **`ManifestClaims<'a>`:** `manifest_digest: [u8; 32]`; `role`; `name`; `aliases: &'a [&'a str]`; `commands: Option<&'a [CommandClaim<'a>]>`; `capabilities: &'a [CapabilityClaim<'a>]`; `provenance: ReleaseProvenance<'a>`.
    - `CommandClaim` is `{name, parent: Option<&str>, aliases: &[&str]}`.
    - `CapabilityClaim` is `{capability_id, relation, rung}`, from the validated value, where CMS ties `declarationData` to `capabilityId`.
    - `ReleaseProvenance` is `{publisher, source_class}`, **taken from the catalog release row** (LD-D4-3).
  - **`AdmissionPolicy<'a>`:** three **sorted, unique borrowed slices**: `reserved_roots: &'a [&'a str]`, `provider_relations: &'a [(&'a str, &'a str)]` and `explicitly_trusted: &'a [&'a str]`. `AdmissionPolicy::new(…, work)` checks each slice strictly ascending, at one charged comparison per adjacent pair (m − 1 edges each), and refuses `PolicyUnordered` otherwise, a host-invariant fault. It allocates nothing.
- **LD-D4-3. EE-1 from the authenticated release association (Q1).**
  - The ordinary reader finds the release by the identity `[stableId, publisher, sourceClass, version]` taken from the validated body, and admits the component only if that catalog row exists and the envelope namespace equals the publisher (`trust_ordinary_metadata.rs`:106-123).
  - D4-2's lend reads `publisher` and `sourceClass` **from that release row** (`AuthenticatedComponent::release`), so the classification is the root-authenticated catalog's.
  - D4 refuses EE-1 when `source_class` is `explicitly-trusted` and `publisher` is not in `explicitly_trusted`.
  - **At M3 the host passes the empty slice.** That is an explicit policy choice, consistent with AQ:341's first-party-only scope, and not a reading of delegation: a root-delegated namespace is not an explicit-trust entry.
  - `first-party` with the release association passes. This is EE-1's enforcing arm.
- **LD-D4-4. EE-3b: the capability form only, as a backstop (Q2).**
  - **`PROVIDER_RELATIONS`** is a `static`, sorted slice in host's `component_admission.rs`. It holds the `(relation, rung)` pairs of the embedded matrix's `capabilities[]` members without an `authority` of `fact` or `candidate-only`: `syntax`'s three pairs, the five semantic pairs, and `unresolved-edge`'s. It is pinned by a test that parses the embedded `native_capability_matrix.v2.json` and requires equality (the pinned-projection pattern of D3a's registry-literal tables).
  - D4 refuses EE-3b for a claimed pair absent from the slice.
  - **Not authority.** The filter separates the matrix's authority classes. It does not admit a provider claim outside CMS: CMS's five closed branches decide what a manifest may declare, and on validated values this arm is a backstop.
  - **Controls** include claims for `inventory`, `clones-fact` (both `fact`) and `clones-near`, `clones-cross-tsjs` (`candidate-only`, empty relations), each refused or unrepresentable as the table says.
- **LD-D4-5. EE-4's manifest part has no carrier; the closed-world pin is nested (Q3).**
  - The pin fixes:
    - CMS's top-level property set;
    - the property sets of `$defs` `capability` (each branch), `platform`, `entry` (each branch), `command` and `dependency`, read from the pinned `tools/security/inputs/manifest-schema.json`;
    - `ManifestClaims`' and its nested claims' field sets.
  - Any change fails the pin and forces review against EE-4 before landing. RJ-6 keeps refusing malformed and unknown fields. The pin is recorded as a closed-world record, never as an executed EE-4 negative or as DR-G29's completion.
- **LD-D4-6. EE-5a in the post-materialization phase.** As r1, accepted (Q4).
- **LD-D4-7. Item 25 at M3.** As r1, accepted (Q5). A new request, flag or nested carrier needs re-review before landing, and the pin's failure message says so.
- **LD-D4-8. The admission algorithm (RF-1, Q8).** `admit(claims: &[ManifestClaims], policy: &AdmissionPolicy, work: &mut WorkScope) -> Result<Cleared, Refusal>`, where n = `claims.len()`:
  1. **Index:** two owned `u32` buffers of n (objects 2, bytes 2·n·`size_of::<u32>()`, charged before allocation; refuse `Budget`). This is CI-A1-b's recipe.
  2. **Sort by `manifest_digest`:** the bottom-up merge sort over indices, one edge charged immediately before each 32-byte comparison, through a fallible comparator. At most n·⌈log₂ n⌉ comparisons, which is the published reference price. `Budget` propagates out of the sort.
  3. **Duplicates:** n − 1 charged adjacent comparisons. Equal digests refuse `Refusal::DuplicateDigest`, a host-invariant fault: R10a's set has one claim per authenticated manifest.
  4. **Count pass:** in sorted order, each manifest's predicates in class order EE-1, EE-3b, (EE-4: none), EE-5a, each priced as LD-D4-10. That gives k, the number of forms.
  5. **If k > 0:** `Vec::with_capacity(k)` (objects 1, bytes k·`size_of::<ExcludedForm>()`). Then the **fill pass**, the same predicates at the same prices, pushing each form. The vector is in (digest, class) order by construction, with no second sort. Return `Refusal::Excluded(vec)`. Its first element is SD-5's projected pair.
  6. **If k = 0:** `Vec::with_capacity(n)` of `[u8; 32]` (objects 1, bytes 32·n), filled in sorted order, n edges. Return `Cleared`.

  Both index buffers are dropped before return. Nothing else is allocated. Exhaustion at any step returns `Budget`, never a truncated vector or a partial `Cleared`. **Complexity:** O(n log n) comparisons for the sort, plus two passes of O(Σᵢ keysᵢ · log m) probes.
  - **`Cleared`** is opaque and non-`Clone`. It exposes `digests() -> &[[u8; 32]]` and authorizes nothing. The wiring must require `cleared.digests()` to equal the sorted digests of the authenticated component set it hands to C2a-1, and run C2a only after it (X-D4P-4).
- **LD-D4-9. Records and projections are J1's.** As r1, accepted (Q8).
- **LD-D4-10. The prices (RF-1).** Every charge is made before its work, by `const fn`s beside their use:
  - **A probe** into a sorted slice of m is a binary search of at most ⌈log₂ m⌉ + 1 comparisons, one edge charged before each. This is CI-A2-c's price, an owner-published search price; D4 does not assume a `BTreeSet`'s internals. An empty slice is one edge, the empty check.
  - **Per manifest, per pass:**
    - EE-1: one edge for the `source_class` test, plus one `explicitly_trusted` probe when it is `explicitly-trusted`;
    - EE-3b: one `provider_relations` probe per capability claim;
    - EE-5a (a): one edge;
    - EE-5a (b): one edge per command entry visited, plus one for the root-name comparison;
    - EE-5a (c): one `reserved_roots` probe per key (name, each alias, each root alias).
  - **Per call:** the policy's order checks (LD-D4-2); LD-D4-8's buffers, sort, duplicate pass, the vector or the `Cleared` list.
- **LD-D4-11. The factory, its seam and its refusals (RF-2, Q7).**
  - **The seam.** `trait LaunchRecheck { fn recheck(&mut self, member: &str, work: &mut WorkScope) -> Result<RecheckedMember, RecheckFailure>; }`.
    - `RecheckedMember` is `{launch_path: PathBuf, closure_recheck: ClosureRecheck}`, exactly CI-A3's operation result.
    - `RecheckFailure` is `{Budget(WorkBudgetError), Io {call, error}, Corrupt(CorruptCause)}`, where `CorruptCause` is `{Absent, Type, Mode, Length, Digest, LinkTarget, Association, Binding}`. `Binding` is CI-A3's path-binding failure. That is CI-3's `TreeReadFailure` partitioned: `Budget` and `Io` keep their own members, and the promised tree's own corruption is `Corrupt`.
    - The host implements it over the **operation's** pinned `RetainedTree`, borrowed. CI item 7 keeps that pin from R10a until the operation ends, so it is held through spawn and settlement. The factory neither opens nor drops a capability.
  - **Which members.** The selected platform entry's `entrypoint` (CMS), resolved by CI-A3. Then every closure path the launch spec names:
    - TS2 (`LaunchSpec::typescript`, `process.rs`:204): the bundled `node`, the verified empty OpenSSL configuration and the provider entry;
    - Rust3 (`LaunchSpec::rust`, :231): the provider executable and the toolchain root.

    Each named path must be a CI-A3 member of an admitted closure the selection names, or the factory refuses `SessionSpecInconsistent`. D1a's `ClosureRecheck` holds one member, the executable's, so the factory passes the executable's recheck to `VerifiedLaunch::from_recheck` and keeps the others' results only as checked (Q4 of this round).
  - **The refusal sum** `FactoryRefusal`. Every member is pre-spawn, and none constructs a `VerifiedLaunch`:

    | Member | Cause | Route (existing) |
    | --- | --- | --- |
    | `Recheck(Corrupt(c))` | `closure-recheck-failed` | J1 row 28, `HOST.IO_FAILURE` / host-io, `DELIVERY.CLOSURE_BYTES_CORRUPT`, or `DELIVERY.CLOSURE_BYTES_MISSING` for `Absent` (WS:1375; CI r5 item 8, :333; item 22) |
    | `Recheck(Io{call, error})` | an observation I/O failure, which proves no corruption | CI r5 item 8's route for the capability's `Io`: operational-failed 4, `HOST.IO_FAILURE`, no detail (:334; item 22's host-fault row, WS:1359-1362). J1 r7's matrix has no row for it: **an explicit J2 gate, X-D4P-5** |
    | `Budget(b)` (the seam's or the factory's own) | ledger exhaustion | J1 row 11, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `WORK.BUDGET_EXHAUSTED` (L468:49) |
    | `SpecInconsistent(key)` | `session-spec-inconsistent` | row 2's route, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, the key in the operational record (NE:3573) |

    `FactoryRefusal::route()` returns D3a's `OwnerRoute`: `ClosureBytesCorrupt`, `HostIo` and `HostInvariant` for the first, second and fourth. D3a's route has no separate missing member, so `Recheck(Corrupt(Absent))` keeps its typed cause, and J2's projection selects `DELIVERY.CLOSURE_BYTES_MISSING` from that cause, as CI item 8 requires. `Budget` stays the ledger's typed failure, which J2 projects on row 11. D3a's `PreSpawnRefusal` is unchanged. Since no `VerifiedLaunch` exists after a refusal, no `Supervision` exists, and `decline` is not on the factory's path.
  - **The spec check against independent authorities.** After assembly, the factory compares the **codec's assembled output** with:
    - the admitted selection from R10a's admitted set, for the select tuple, `stableId` and the manifest digest;
    - the protocol's pinned Hello limits, D2b-3b's and D2b-4's release constants, for TS2's ten members or Rust3's 32;
    - the verified signed descriptors (A2), for TS2's descriptor digests and fields;
    - the Plan's universe row (C4a), for Rust3's `expectedIdentity`.

    The codec output means TS2's `DispatchContext` and the Hello the sender will encode, and Rust3's equivalent. Each authority is a distinct input that the codec did not derive its output from. Any difference is `SpecInconsistent(key)`. Before C4a, the production composition is not claimed, and the Plan row is a typed synthetic input in tests.
  - **The recheck runs last.** It runs after assembly and the spec check, immediately before `VerifiedLaunch::from_recheck` and the handover to D3.
- **LD-D4-12. Fixtures.** As r1. The signed `explicitly-trusted` analyzer's release row carries `sourceClass: explicitly-trusted`, so that the association, not the body alone, drives the refusal.
- **LD-D4-13. The reserved list is the reader's own set (review note).** `trust_ordinary_metadata::prepare` builds `reserved_names` (:84-90) and clones it into each manifest's `Context`. D4-2 **moves** that set into `Evidence` after the loop. It is a move, with no new allocation. The lend borrows it. The host's sorted slice view is `Vec<&str>` with capacity r (objects 1, bytes r·`size_of::<&str>()`), filled by the set's in-order iteration at r edges, charged before allocation, so `AdmissionPolicy::new`'s order check passes by construction and still runs.

- **LD-D4-SD9. SD-9 is the lead's owed successor (Q6).** The lead owns SD-9, R10a's and ER10a's work ledger: its lifetime (one ledger, created once at R10a's entry under the fence, never replaced, with ER10a's counterpart), its aggregate cost model across the trust read's hand-off, D4, C2a-1, CI-3's open and C2a-3k, its caps, and its `Budget` projection. It is drafted with the J1 and D4 admission owners. It is **owed**, and it gates production R10a and ER10a composition, C2a-4, and J3d's and J2c's wiring. It **gates no pure D4 sub-unit:** D4-1 to D4-4 charge a borrowed scope and are tested with explicitly identified test scopes, which are not evidence for any profile. No interim profile follows from this plan or from a caller's name. Any interim is SD-9's own accepted policy.

## 3. Bounds and charging (summary)

| Sub-unit | Scope | Charged | Not charged again |
| --- | --- | --- | --- |
| D4-1 | the caller's borrowed `WorkScope` | LD-D4-10 and LD-D4-8: the policy order checks, two index buffers, the sort's comparisons, the duplicate pass, two predicate passes, the vector or `Cleared` | borrowed claims and policy slices |
| D4-2 | the caller's | the claims vector (objects 1, bytes n·`size_of::<ManifestClaims>()`) and each borrowed-slice vector at its exact reserved size; the reserved-slice view (LD-D4-13) | the reader's validated values, release rows and reserved set; `PROVIDER_RELATIONS` (static) |
| D4-3 | none | nothing: constant work on a typed value | — |
| D4-4 | the caller's | the spec's owned strings at their lengths; the comparisons at one edge each; the seam's CI-A3 prices | the admitted selection, the Plan row and the descriptors, borrowed |

D4 selects and infers no profile (LD-D4-SD9).

## 4. Cross-law items

- **X-D4P-1 → LD-D4-SD9.** SD-9 is owed, owned by the lead with the J1 and D4 admission owners. It gates production R10a/ER10a, C2a-4, J3d and J2c, and not D4.
- **X-D4P-2. CI-A3, which D4-4 waits on.** It is the lead's amendment to CI r5, drafted as `component-install/CI-A3-r1.md` and reviewed separately. It must define:
  1. **Entrypoint resolution:** the selected platform row's `entrypoint` resolved lexically over the TreeCommitment, never by following a filesystem link, by security's rule (`component_manifest.rs`:313-331, which already proves the analyzer chain acyclic and ending in an executable file row), to one `file` row. The launch member is that file, not a symlink.
  2. **The member operation:** on the pinned capability, with no new open of the store, resolution from the retained `tree/` handle component by component, no-follow, and a re-check of type, installed mode, length and SHA-256 by a full charged read. The result is `(device, inode)` from the opened handle.
  3. **The path binding:** the absolute launch path composed from the store's admitted absolute location, the generation name and the member's path. The composed path is re-observed (`lstat` on it, no-follow on its last component) and must give the same `(device, inode)`. The residual window to spawn rests on the store's custody, the generation's immutability and the pin, and is stated.
  4. **The lifetime:** the result borrows the capability, so it cannot outlive the pin. The operation's pin (CI item 7) holds through spawn.
  5. **Exact prices:** a recipe `B_launch(f)` in CI item 4's shorthands.
  6. **Typed failures:** `TreeReadFailure`'s existing members, `Budget` and `Io` among them, with no new code and the item 8 routes unchanged. A path not a `file` row after resolution, or not the selected entrypoint or a named member, is `Association`.
  7. **Directory members** (Rust3's toolchain root): identity `(device, inode)` and the installed mode of a `dir` row, with no content hash, since the tree's open already verified it.
  8. **Controls.**
- **X-D4P-3 (record only).** As r1.
- **X-D4P-4.** As r1, with LD-D4-8's `Cleared`-to-set comparison as the wiring's obligation.
- **X-D4P-5. The recheck I/O matrix row (J2 gate, new).** CI r5 item 8 already fixes the capability's `Io` route: operational-failed 4, `HOST.IO_FAILURE`, no detail (:334). J1 r7's matrix routes host I/O during capture or discovery (row 23) and closure corruption or unspawnability (row 28), but has no row for that route at the pre-spawn recheck, or at R10a's open. D4 carries it as `OwnerRoute::HostIo`. J1's next revision must record the matrix row, with existing codes only, quoting CI item 8. J2's projection of this refusal waits for it.

## 5. Controls and mutations (each sub-unit's lane)

- **Suites, formatting, lints, repository checks:** as r1. Inventory successors are owed for every new or realized path (§6).
- **D4-1:**
  - **D4-T4** and **D4-T1's interface half**, as r1;
  - **RF-1's accounting:**
    - **Order:** reversed, shuffled and already-sorted inputs give the same `Refusal::Excluded` vector and the same `Cleared` list;
    - **Several forms:** one manifest with EE-1, EE-3b and EE-5a forms gives them in class order; two manifests with forms are ordered by digest;
    - **Policies:** a non-empty `explicitly_trusted` admits a listed publisher and refuses an unlisted one; empty and full slices for each of the three policy sets; an unordered policy slice refuses `PolicyUnordered`;
    - **Duplicates:** two claims with equal digests refuse `DuplicateDigest`;
    - **Independent accounting:** a recording `WorkScope` logs every charge site (buffer, comparison, duplicate check, probe, vector, `Cleared`) with its cost. The test computes the expected log from the input itself, independently of the module's `const fn`s: n, the comparisons the reference merge sort makes on that input, each probe's comparisons on that slice, and k. It requires equality. For each site in turn, a scope one unit short of it refuses `Budget` before the site's work: no allocation, comparison or push occurs (asserted by the log), and no partial result is returned.
  - **The nested closed-world pin** (LD-D4-5); `ExcludedFormClass`'s six members;
  - **Mutations** (each must fail an assertion, not compile):
    - each arm removed;
    - (a) judging only a non-empty tree;
    - (c) skipping root aliases;
    - (b) skipping the name binding;
    - the class order swapped;
    - the sort removed (input order kept);
    - the sort's comparison charge removed;
    - the explicit-trust probe skipped (admit any `explicitly-trusted`);
    - the duplicate pass removed;
    - the count pass skipped (a growing vector);
    - a probe charged after its comparison;
    - the vector truncated to its first element.
- **D4-2:**
  - as r1: positive on every C2a-2 role; EE-1 end to end; the (a), (b) and (c) source pins with both (a) pins; the no-trust-view case;
  - **plus:**
    - the lend's provenance equals the release row's: a fixture whose body and release disagree is unreachable, since the reader refuses it, and the lend has no constructor but `from(&AuthenticatedComponent)` (compile-fail probe);
    - `PROVIDER_RELATIONS` equals the embedded matrix's projection, and excludes the four `fact` and `candidate-only` members;
    - the reserved slice equals the reader's retained set, element for element;
  - **mutations:** the adapter passing an empty reserved slice; `PROVIDER_RELATIONS` gaining `("file", "enumerated")`; provenance read from the body instead of the release.
- **D4-3:** as r1.
- **D4-4 (RF-2):** through the factory, with CI-3's fixture store and CI-A3's operation:
  - **Corrupt:** an entrypoint whose bytes, length, mode or type differ, each giving `Recheck(Corrupt(Digest|Length|Mode|Type))` and `OwnerRoute::ClosureBytesCorrupt`;
  - **Budget:** a scope one unit short before CI-A3's open of the member, and before its first hash read, each giving `Budget`, never `Corrupt`;
  - **Io:** an injected I/O failure in the member read (CI-3's `#[cfg(test)]` seam, ID-CI2-8) giving `Recheck(Io)` and `OwnerRoute::HostIo`;
  - **Spec:** an injected difference in each compared value (tuple, `stableId`, manifest digest, a Hello limit, a descriptor digest, `expectedIdentity`) giving `SpecInconsistent(key)` and `HostInvariant`;
  - **For every refusal:** no `VerifiedLaunch` constructed, no spawn (the platform spawn log is empty) and zero snapshot bytes at the fake;
  - **the sole-constructor pin** for `VerifiedLaunch::from_recheck`;
  - **the provider-spoken half,** once D2b-3b and D2b-4 exist;
  - **mutations:**
    - `Budget` mapped to `Corrupt`;
    - `Io` mapped to `Corrupt`;
    - the recheck moved before assembly;
    - the spec check comparing the codec's output with itself;
    - a member of the launch spec not rechecked.

## 6. Inventory

As r1. **One ordering note:**
- D4-2 changes `crates/security/src/trust_admitted_components.rs` and the ordinary reader (`trust_ordinary_metadata.rs`). CI-2/CI-3's candidate (worktree `opensip-ci2`) also changes `trust_admitted_components.rs`, `trust.rs` and security `lib.rs`.
- So D4-2's lane starts only after CI-2/CI-3 integrate, on that main. Its integrate script refuses if main changed one of its paths since its lane base.

## 7. Not claimed

As r1, and explicitly:
- **J-C10b's cases:** 3a; 3b × {`Published`, `LostRace`, `NotPristine`}; ephemeral with a trust view; ephemeral with none.
- **J-C20's rows 56 and 57.**
- **The recheck-I/O row** (X-D4P-5).
- **SD-9, and any R10a profile.**
- **CI-A3's acceptance.**
- **Product qualification.**

## 8. Questions for the reviewer

- **Q1 (RF-1, LD-D4-8 and LD-D4-10).** Do the sort, duplicate pass, two predicate passes and sorted-slice probes, at CI-A1-b's and CI-A2-c's prices, make D4-1's model complete? Is `DuplicateDigest` the right refusal for a host-built set with a repeated manifest?
- **Q2 (RF-2, LD-D4-11).** Is the partition of CI-3's failures into `Corrupt`, `Io` and `Budget` right, following CI r5 item 8? `Absent` goes to `DELIVERY.CLOSURE_BYTES_MISSING`, and the other causes to `CORRUPT`. Is X-D4P-5 the right way to carry the missing J1 matrix row?
- **Q3 (LD-D4-4).** Is a static, test-pinned projection of the embedded matrix lawful for `PROVIDER_RELATIONS`, in place of a charged runtime build?
- **Q4 (LD-D4-11).** D1a's `ClosureRecheck` holds one member. Is rechecking every closure path the launch spec names, while passing only the executable's recheck to `VerifiedLaunch`, sufficient? Or should D1a's type (or CI-A3) carry the whole member set?
- **Q5 (LD-D4-13).** Is moving the reader's reserved set into `Evidence`, as a move with no copy, the right way to lend the exact policy?

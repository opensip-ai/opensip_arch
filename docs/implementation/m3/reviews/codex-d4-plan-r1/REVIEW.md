# D4-PLAN-r1 review

**Verdict: REQUIRED-FINDINGS.** Two required findings; no non-blocking observations.

## Subject and authority

Verified the 378-byte subject manifest, SHA-256 `a21f8a6dd188fe9da06a4e911763db9acb6634525d226642d68b235a9e7b4424`, and its sole member `d4/PLAN-r1.md`, 35,993 bytes, SHA-256 `2ae0bece1c104c5726a52754e3da47c8c6e47673bf35e5f5887cf4321252e460`.

Read product interfaces at the specified `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` through Git, preserving the frozen base despite current HEAD movement. Compared the plan with M3-D items 24–26, J1's R10a/ER10a and projection ownership, C2a's admission order/profile gate, the CI retained-tree contract, the closed manifest/request carriers, authenticated-component bridge and factory inputs. No implementation acceptance is inferred.

The four-unit split is reasonable. The projection avoids a components dependency on security and avoids a second parser. D4 supplies the predicates and adapter; C2a remains the closure-admission owner; J3d/J2c own durable/ephemeral placement; J1 owns records and envelopes; D3 owns spawning/supervision; D2b owns protocol admission. D4-4 correctly waits for codecs and the retained-tree launch operation. C4a's expected-identity producer is also needed for production composition even if the library is developed against typed synthetic inputs.

## Required findings

### D4PLAN-R1-RF-1 — Price the ordering and all membership work required by the admission algorithm (P2)

**Location:** `docs/implementation/m3/supervisor-d/d4/PLAN-r1.md:90-105`.

admit accepts an arbitrary slice and promises a vector and Cleared digests in digest order, but the complete price list has no ordering term or ordering precondition. Counting and filling the vector does not put reversed input in SD-5 order. Sorting adds work, and an allocating stable sort could also contradict "nothing else is allocated". EE-1's explicitly_trusted membership lookup is also missing from the per-manifest recipe. The statement that the work is linear is not established for arbitrary input plus comparison sorting. The proposed log2 edge formula for BTreeSet probes additionally needs an actual owner/pricing derivation rather than assuming a binary-search implementation.

**Required change:** Specify the allocation and ordering algorithm and price it before use, or require a source-established canonical input order with charged validation and a defined refusal for bad input. Include the explicit-trust probe and both predicate passes. Provide conservative sourced prices for the chosen set representation, including any owned matrix nodes/strings in D4-2 and any sorting scratch. Adjust the complexity claim to the actual algorithm.

**Control:** Use reversed/shuffled manifests, multiple classes on one manifest, nonempty explicit-trust policy, empty/full policy sets and the Cleared path. Independently account for every allocation/ordering/probe site, with one-unit-short failures before work, rather than merely asserting that charge calls equal the same declared constants.

### D4PLAN-R1-RF-2 — Preserve budget and observation failures across the launch-recheck seam (P2)

**Location:** `docs/implementation/m3/supervisor-d/d4/PLAN-r1.md:106-108`.

The recheck takes a charged WorkScope but returns Result<..., RecheckFailed>, and the plan says a failure is ClosureRecheckFailed on DELIVERY.CLOSURE_BYTES_CORRUPT. CI-3's capability has Budget and Io failures as well as structural/content mismatches. Exhausting the scope before a read proves no corruption; neither does an observation I/O failure by itself. The blanket mapping loses the required typed budget failure and misstates the host-observed condition. D4-4's current controls inject corruption and spec inconsistency, but not these other exits.

**Required change:** Define a factory/recheck failure sum that preserves WorkFailure::Budget and the capability's relevant typed observation failures. Reserve the corruption projection for the conditions its existing route actually owns. Name the existing owning projection for other failures, or carry that projection as an explicit J2 gate; do not invent a code or collapse exhaustion into corruption. Keep all failures pre-spawn and retain the accepted mismatch/spec routes.

**Control:** Include one-unit-short budget refusal before an open/hash, I/O failure during the recheck, and actual type/mode/length/digest mismatch. Assert their distinct typed outcomes, no spawn and zero snapshot disclosure, and pin the factory's propagation rather than testing the capability alone.

## Rulings

**Q1:** Accepted with the authenticated association preserved. A first-party classification must come from the root-authenticated catalog/release association joined by the ordinary reader, not merely a caller-supplied sourceClass or the fact that a namespace has some delegation. That reader joins publisher, sourceClass, version, body and catalog release. An empty M3 explicit-trust list is an explicit policy choice consistent with AQ's first-party-only scope; delegation alone is not an explicit-trust-list entry. The signed explicitly-trusted fixture should exercise the enforcing refusal.

**Q2:** Accepted as a backstop over the current CMS's five closed TypeScript declaration branches, using their sourced relation/rung coordinates. Preserve capabilityId/declarationData consistency from the validated value. The matrix's fact/candidate-only flags distinguish authority classes, not whether work runs in a child; syntax is produced by the core provider closure in-host. Do not describe that filter as authorizing arbitrary provider claims outside CMS. Pin the matrix projection and exclude host inventory/clones fact and candidate-only capabilities in controls.

**Q3:** Accepted. There is no current CMS field or projected field representing the manifest EE-4 request. A closed-world source/schema pin is appropriate, with RJ-6 retaining malformed/unknown-field refusal. It must cover relevant nested capability/platform/entry representations as well as the top-level claims fields, and force review when representation changes. This is not an executed EE-4 negative or DR-G29 completion.

**Q4:** Accepted. CR-1 was materialized independently at d579140; that changes the factual enforcement phase, not the accepted D4 predicate. D4 carries its own closure-only commands check from its first integration and simultaneously pins the existing RJ-6 refusal in both entry points. The analyzer mounted-root and reserved-name checks remain D4 backstops; live-name collisions retain RJ-2.

**Q5:** Accepted for the present closed M3 request type. Its three variants and five flags carry none of EE-2, request EE-4 or EE-6a. Keep an exhaustive classification point and structural pins, return None for each present request, and record D4-T2 as unrepresentable rather than a passing refusal corpus. A new request/flag or nested carrier requires re-review before landing. Do not add an artificial user-visible form just to exercise row 57.

**Q6:** D4 may consume a borrowed scope without selecting a profile. The lead, with the J1/D4 admission owners, should own SD-9 and its aggregate model, caps and Budget projection. A new or interim profile needs explicit accepted policy; none follows from the caller name or from library tests. Pure D4 units can land before SD-9, but production R10a/ER10a composition, C2a-4 and J3d/J2c stay gated. RF-1 must make D4's own model complete and RF-2 must preserve exhaustion.

**Q7:** Accepted in architecture, subject to RF-2 and CI-A3 acceptance before D4-4. The factory should invoke a host-implemented seam over CI-3's retained pinned tree immediately before handing the launch to D3, rather than accept a detached stale recheck as caller authority. CI-A3 must define the entrypoint resolution, retained lifetime/path binding, exact prices and typed failures. The launch path, rechecked member identity and selected entrypoint must be joined, and the pin must remain alive through spawn.

**Q8:** Accepted in boundary. Return every internal excluded form, project the least digest and its first class in the fixed order, and leave event registration, records and public envelopes to J1's projection owner. Cleared is useful as an opaque non-authorizing receipt; wiring must bind it to the exact authenticated component set and run C2a admission only after it. RF-1 must specify the ordering cost; no silent truncation or partial vector is permitted.

**Q9:** Accepted. D4-T1 is interface-complete, path-owed until J3d/J2c supply the reservation-state, no-draw/no-spawn and public-route checks. Record all first-use outcomes and ephemeral/no-trust-view cases explicitly. Neither interface acceptance nor signed-fixture success completes J-C10b, J-C20, DR-G29 or product qualification.

## Coverage and implementation gates

The post-materialization EE-5a analysis is accurate: the existing security schema now rejects closure-only commands before D4, while D4 still owes its own check. Mounted analyzer roots remain permitted, and reserved aliases must be checked for every applicable root key. EE-3b carries no command-tree form. The closed-world EE-4 and request-class decisions are honest only with their recorded unrepresentable standing; none is a passing executed hostile-form test.

Keep the pure view genuinely borrowed and unconstructible outside the trust owner where claimed. The adapter must retain access to the exact reserved-name policy the ordinary reader used: its current BTreeSet is local to that reader, so implementation must either retain/lend it or charge any new reconstruction. A JSON catalog array is not itself a borrowed BTreeSet. The actual code-unit scope must include any necessary evidence/reader changes, not just the bridge accessor.

D4-4's contract must explicitly identify the assembled session/participant output and authoritative values compared. The base AdmittedSelection contains stableId, manifest digest, platform and tuple; it does not itself contain Hello limits or Plan-derived expected identities. Those comparisons must use the additional admitted request/context and pinned protocol sources the plan already names. Comparing two caller copies is not an independent consistency check. Preserve the sole production VerifiedLaunch constructor pin and the no-spawn behavior for all factory refusals.

X-D4P-1 and X-D4P-2 are real interface gates. R10's global profile cannot be silently reused for whole-tree R10a verification: the stated 100 MB hashing example already exceeds its edge allowance. A CI amendment is appropriate for the pinned entrypoint operation because retention transfer alone does not produce a launch binding. X-D4P-3 can record the changed CR-1 enforcement phase and deferred path half; X-D4P-4 should keep C2a-4's admission call inside J3d/J2c's wiring in trust-read → D4 → C2a order.

The proposed functional controls, source/schema pins, signed role fixtures, no-trust-view case, class-order checks and mutation lanes are a useful base. Extend them as RF-1 and RF-2 require. Keep the stated compile-time exceptions only for closed-world/API-sealing controls; behavioral mutations must actually fail assertions. Every new or realized path needs its separately reviewed inventory treatment, including D4-1's module/test additions as section 6 already records.

Only REVIEW.md and review.json were written in the requested directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build, lane, network, prohibited fixture/key/installation material, held tree, held-out entry, T2 material, pane or delegation was used.

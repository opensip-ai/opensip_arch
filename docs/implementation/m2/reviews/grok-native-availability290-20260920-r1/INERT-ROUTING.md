# Inert excluded-member envelope routing (planning only)

This is **not** a 290 bounded verdict and does **not** implement T1 DR-103/DR-112 scope. Sources inspected: nested 265 `trust-state-continuity.v1.md` C.3; `security-completion.v2.md` §2.2 and v1 verification order; `signature-envelope-routes.v1.json`; `trust_metadata_index_reference.py` `Index.__init__` lines 71–72; native `retained_metadata_index::Data::build` and `CarrierView::route_matches`. No retained-index or routing-table edit.

---

## Two different uses of “role”

**Carrier route (kind table).** Closed table: `kind` selects lawful `domain` **and** envelope `role` (manifest → TR-COMPONENT, catalog → TR-INDEX, root/revocation → ROOT, inventory → TR-CORE, payload → TR-BUNDLE, …). Python index:

```
route=ROUTES[sub['kind']]
require(sub['domain']in route['domains'] and env['role']==route['role'],'envelope-route')
```

Native `Data::build` parses each listed envelope, then `if !view.route_matches() { return Err(Error::Route) }` **before** pairing/select. `carrier_route_matches` is domain∈kind.domains **and** `role == kind.route().2`. Comment on `parse_carrier`: closed carrier shape only; route matching does **not** authenticate a body, signer, custody, or current authority.

This check is **inventory pairing / well-formedness**, not key authorization. It runs before any DR-112 reader and before any T1 vs excluded split.

**DR-112 authority.** C.3: for members owned solely by excluded roles, “Only the DR-112 **role/key/namespace/threshold authority** check is scoped away.” That is: whether a key is authorized for a role+namespace, and whether distinct valid authorized keys meet threshold. It is not “whether the envelope’s role ENUM equals the kind’s declared route.”

SEC-M8 / §2.2: kind, domain, role, namespace are **inside the signed envelope.2 subject**. A valid signature cannot re-present the same bytes under another kind/domain/role. `envelope-role-confusion` (K-comp-1 signs kind catalog / role TR-INDEX) is §2.2 **step 2** `RJ-4 ENVELOPE_MISMATCH`, same step as “kind is not the expected kind.”

---

## C.3 DR-103 vs the ENVELOPE_MISMATCH bucket

C.3 excluded members must remain present, **well-formed**, **nonempty-signature**, exactly digest-joined, shape/byte/digest-bound; they stay **inert**. Failed role-specific **authority** signatures do not veto the shared update.

§2.2 maps several distinct failures onto one `RJ-4 ENVELOPE_MISMATCH` code:

| §2.2 step | Failure | Closer owner |
|---|---|---|
| 1 | missing / schema-invalid envelope, empty signatures | DR-103 UNSIGNED / well-formed |
| 2 | kind/domain/**role route table** | **Carrier well-formedness / pairing** (keep for excluded members) |
| 3 | `storedSha256` ≠ bytes | DR-103 DIGEST_MISMATCH |
| 4 | canonical preimage mismatch | Exact body digest join (named DR-112 `envelopePreimageJoin` in §2.3; still a digest identity, not key authority) |
| 5 | envelope namespace ≠ publisher | Document identity join vs delegated-namespace **authorization** (see ambiguity) |
| 6 | zero signatures from keys authorized for role+namespace | DR-112 key authority (C.3 would scope this away); nonempty **unauth** signatures still satisfy “nonempty signatures” |
| 7 | authorized keys below threshold | DR-112 `thresholdEvaluation` (already not RJ-4) |

C.3’s “well-formed” is not defined as “every ENVELOPE_MISMATCH.” The index/native route check is the pairing predicate that makes a listed envelope **be** a catalog (or manifest, …) envelope at all. Skipping it for excluded members would yield `envelope-missing` / unpaired slots, i.e. a silent hole, which C.3 forbids.

---

## Precise cases (excluded role-specific member)

Assume a complete inventory slot whose T1 does **not** rely on that role. Do **not** introduce an untrusted caller role selector.

| Case | Lawful excluded-member result | Current pairing/index | Current §2.2 verifier |
|---|---|---|---|
| Envelope role ENUM ≠ kind’s declared route (manifest claims TR-INDEX; catalog claims TR-COMPONENT; payload claims ROOT) | **Still fail.** Carrier is not well-formed for that kind. DR-103/pairing, not scoped DR-112. | `envelope-route` / `Error::Route` | step 2 ENVELOPE_MISMATCH (`envelope-role-confusion`) |
| Correct route; key not in that role+namespace; other signatures nonempty | **Must not veto** shared import if only DR-112 is scoped away (inert). | Pairs (route ok) | step 6 ENVELOPE_MISMATCH if none authorized — **adapter must not use this as DR-103** |
| Correct route; authorized key, bad signature bytes; nonempty list | Cryptographic invalidity of authorized keys is DR-112; schema-invalid signature **encoding** is DR-103 well-formed | Pairs | discarded per signature; zero valid → step 6 |
| Missing envelope | DR-103 UNSIGNED. Fail. | `envelope-missing` | step 1 UNSIGNED |
| Empty `signatures` | DR-103 well-formed / UNSIGNED. Fail. | schema `envelope-shape` | step 1 UNSIGNED (`envelope-malformed`) |
| Malformed envelope (schema / non-object) | DR-103. Fail. | `envelope-shape` / `Unsigned` | step 1 UNSIGNED |
| Wrong `storedSha256` / body bytes | DR-103 DIGEST_MISMATCH. Fail. | `member-digest` / select missing | step 3 DIGEST_MISMATCH |
| Body not shape-valid for the slot | DR-103 member shape. Fail. | select / later shape | before signatures in several owners |
| Envelope namespace ≠ manifest publisher (correct role route) | See ambiguity. | not this index check | step 5 ENVELOPE_MISMATCH |
| Correct route and keys; below role threshold | DR-112. Must **not** veto excluded member. | Pairs | step 7 THRESHOLD-SHORTFALL (already not RJ-4) |

Shared members (root chain, BUNDLE, catalog, list) are never made inert. Wrong-route on a **shared** envelope still fails the whole payload.

---

## Recommendation

**Keep kind/domain/role route matching as DR-103 well-formedness and index pairing.** A structurally valid envelope whose role ENUM mismatches the subject-kind’s declared ROUTE must still fail for an excluded member. That is carrier identity, not delegated key/namespace/signature authority.

**Do not** add a scoped header adapter that skips `Index` lines 71–72 or native `route_matches()` / `Error::Route`. **Do not** relax the closed routing table.

A later T1-scope adapter, if any, should skip only DR-112 **key authorization, delegated-namespace authorization, and threshold** after a successful route+digest+nonempty-signature pairing — and must still refuse missing/empty/malformed envelopes and digest/shape failures.

---

## Unresolved ambiguity (do not paper over)

1. **RJ-4 ENVELOPE_MISMATCH is overloaded.** v2 step 2 (route) sits in the same refusal code as step 5 (namespace) and step 6 (no authorized valid signature). C.3 scopes “role/key/namespace/threshold **authority**” and separately requires nonempty signatures. A scoped reader must split these, not treat the RJ-4 string as one DR-103 class.
2. **Namespace.** Envelope namespace ≠ publisher is a **document identity** join for manifests; “key not listed for this delegated namespace” is DR-112. C.3 names namespace under DR-112; §2.2 step 5 does not distinguish those two.
3. **Preimage join.** Completion §2.3 calls `envelopePreimageJoin` DR-112; C.3 also requires “exactly digest-joined” as excluded-member DR-103. Exact body preimage is pairing identity; it should remain required for excluded members even if the DR-112 *name* is reused.
4. **v1 vs v2.** v1 verification order had no explicit routing-table step; v2 added it. The native/Python index already enforces v2’s table at pairing time.

No 290 production change. No index change. Target scope later derives from actual root/role/OLD/recovery context, not an `authenticated` flag.

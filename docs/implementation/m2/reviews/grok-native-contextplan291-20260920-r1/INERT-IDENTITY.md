# Inert excluded-member body and identity joins (planning only)

This is **not** a 291 bounded verdict and does **not** implement T1 DR-103/DR-112 scope. It continues 290 `INERT-ROUTING.md` without reopening kind/domain/literal-role route matching. Sources: nested 265 C.3 and `security-completion.v2.md` §2.1–2.2; native `component_manifest::validate`; 285 `ordinary_metadata::prepare` catalog/component joins. No schema, routing-table, or public-flag change.

290 already keeps: kind/domain/literal-role route match; nonempty well-formed signatures; raw stored digest and canonical preimage binding. Remaining questions: publisher namespace identity vs delegated-namespace authorization, and which 285 body/catalog joins stay mandatory for an **excluded COMPONENT**.

---

## Split: identity join vs delegated-namespace authority

§2.2: for a manifest, `namespace` MUST equal `manifest.provenance.publisher`. That is a **document identity** fact: envelope and body name the same publisher. It does not ask whether any key is authorized for that publisher.

DR-112 delegated-namespace authority is the other fact: the signing `keyId` is listed for that role **and** that namespace on the chosen root (`root_keys_for_role`). C.3 scopes **that** check away for excluded members.

**Keep `envelope.namespace == body.provenance.publisher` mandatory for excluded COMPONENT.** A mismatch is an internally inconsistent carrier, not a failed authority check. A later adapter that skipped it would admit a body that claims publisher A under an envelope that claims B — that is not “inert well-formed bytes.”

**Do not** treat “key not delegated for that namespace” as the same join. Correct route, matching publisher/namespace, nonempty signatures, but **no** key authorized for that namespace: DR-112. Must **not** veto the shared import; the member stays inert.

No new public `authenticated` flag. No relaxation of the closed envelope schema or routing table.

---

## Body and catalog joins for excluded COMPONENT

C.3: only DR-112 role/key/namespace/threshold **authority** is scoped away; each member remains present, well-formed, nonempty-signature, exactly digest-joined, **shape-valid**, and byte/digest-bound to the authenticated complete inventory; bytes cannot later be installed/executed without full current admission.

285 `ordinary_metadata::prepare` currently applies the **full** `component_manifest::validate` (schema, commands, paths, capabilities, permissions, dependencies, host-configuration, live names, reserved names, exceptions) **then** catalog 4-tuple / publisher-envelope-ns / raw body / preimage / envelope / hostCore joins. That is the full-component-set helper, not the T1 excluded-member law.

| Check | Owner | Excluded COMPONENT |
|---|---|---|
| Missing/malformed envelope; empty signatures | DR-103 UNSIGNED / well-formed | **Fail** (still) |
| Kind/domain/literal-role route | Carrier pairing (290 INERT-ROUTING) | **Fail** (still) |
| `storedSha256` / inventory DocRef SHA+length | DR-103 DIGEST / byte-bind | **Fail** (still) |
| Canonical body preimage = envelope `preimageSha256` | Exact digest join (named DR-112 `envelopePreimageJoin` in §2.3; still identity, not key authority) | **Fail** (still) |
| Closed metadata parse (4MiB/UTF-8/NFC/i64/no-float) + `generated::shape` / bounded v11 manifest | DR-103 shape-valid | **Fail** (still) |
| In-body uniqueness: commands, platforms, capabilities, permissions, dependencies; path/tree/entrypoint rules; in-body `hostCore` nonempty and `compatibility.manifest` = schema version | Closed document shape/semantic of the **member bytes** | **Fail** (still). These do not consult HostContext or keys. |
| Catalog 4-tuple identity (`stableId`, publisher, sourceClass, version) present in the **shared** catalog | Inventory slot bound to authenticated shared catalog (C.3 “digest/size/member joins”) | **Fail** (still). Catalog is never inert. |
| Raw body SHA = catalog `manifestDigest`; envelope SHA = `envelopeDigest`; preimage = `manifestPreimageSha256` | Inventory digest join to that catalog row | **Fail** (still) |
| `envelope.namespace == provenance.publisher` | Document identity (above) | **Fail** (still) |
| Body `compatibility.hostCore` == catalog `hostCoreConstraint` | Inventory consistency with the shared catalog row, not a host registry | **Fail** (still) |
| Catalog `reservedRootCommands` vs component command/alias names | Inventory consistency with the shared catalog | **Fail** (still) |
| `HostContext.host_classifications` / `config_checks` | Current host environment (285 HostContext is a typed **input**, not a qualified registry) | **Must not veto** shared import. Inert installation constraint; full admission later. |
| `HostContext.live_names` collisions | Host registry of live components | **Must not veto** shared import. Same. |
| `HostContext.approved_exceptions` | Host-approved prerequisite exceptions | **Must not veto** shared import. Same. |
| Cryptographic signature under a correctly shaped envelope, key not in role+namespace, or below threshold | DR-112 authority | **Must not veto** shared import. Nonempty signatures already satisfied DR-103. |
| Shared catalog/list/BUNDLE/root envelopes | C.3 shared; never inert | Full DR-112 still required |

Bad stored/preimage/body **shape** must fail. Bad cryptographic signature under a correctly shaped, route-matched, digest-joined envelope must not veto an excluded member.

---

## Explicit cases

1. Excluded COMPONENT; envelope.namespace `opensip`, body publisher `evil` → **refuse** (identity). Keys irrelevant.
2. Excluded COMPONENT; envelope.namespace = publisher `acme`; signatures nonempty; **no** root key delegated for `acme` → **do not veto** shared import (DR-112). Member inert.
3. Excluded COMPONENT; route-matched envelope; body SHA ≠ catalog `manifestDigest` → **refuse** (inventory digest).
4. Excluded COMPONENT; closed schema fail (unknown field, bad path tree, empty hostCore interval in-body) → **refuse** (shape).
5. Excluded COMPONENT; schema-valid body; HostContext live-name collision or wrong host classification → **do not veto** shared import; cannot install/execute later without full admission.
6. Excluded COMPONENT; 4-tuple not in catalog → **refuse** (unbound inventory slot). Unpresented **other** catalog releases remain allowed (285).
7. Relied-on T1 COMPONENT: all of the above plus DR-112 key/namespace/threshold remain.

---

## Amendment (if a scoped reader is specified later)

Do **not** silently drop `component_manifest::validate`'s HostContext arguments by omitting them inside the current full-set 285 function. Specify an explicit **inventory-shape** subset (parse + generated shape + in-body path/command/capability/permission/dependency/compatibility-interval rules + catalog reserved-name collision) versus a **host-admission** subset (classifications, live names, approved exceptions). Keep publisher/namespace identity and catalog digest/4-tuple/hostCore-row joins on the inventory side. Split RJ-4 so “no authorized valid signature” is not treated as DR-103 UNSIGNED.

No 291 production change. No new public flag. Target scope later derives from actual root/role/OLD/recovery context.

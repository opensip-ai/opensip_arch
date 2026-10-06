# SD-2 — manifest-owner confirmation of the M3 native control selection

PROPOSED design record. Effective only after independent ACCEPT-DESIGN-UNIT, lead substantive assent and design-lock binding. This confirms M3-D r5 item9 and its SD-2 duty; it does not put M3-L in effect or authorize D2a code integration, spawn or provider execution.

## Confirmed tuples

For an admitted, explicitly selected M3 native semantic provider session, common control hello.subprotocolOffers contains exactly ONE tuple; select names that SAME tuple. The two published selections are:

| Selected provider protocol | role | roleSubprotocol | subprotocolVersion |
|---|---|---|---|
| TypeScript protocol2 | analyzer | typescript-semantic | 2 |
| Rust protocol3 | analyzer | rust-semantic | 3 |

subprotocolVersion is an exact integer, not a boolean, float-spelled integer or string. These are the pairs from native-evidence §9.1, not independently negotiable names and majors. The selected role is the admitted manifest.role. The selected major equals admitted manifest.compatibility.providerProtocol. The selected roleSubprotocol/version are the exact opaque tokens of the admitted capability declaration supporting the already pinned provider selection; the host does not infer a provider from a display name, stableId, file extension, first capability row or component path. Capability tokens remain opaque at manifest admission. Multiple declarations or possible providers do not create a runtime choice: the upstream admitted selection is pinned before construction of the session, and only its one tuple is offered.

The existing fields suffice. No manifest field, role, control message, wire member, schema shape, compatibility major, identity domain or capability token is added. The manifest owner's capabilities declaration and compatibility.providerProtocol retain their existing field authorities; this record confirms how the admitted selection supplies the tuple for the two M3 native sessions. General manifest admission is not restricted to these two tuples: an empty capabilities array remains structurally valid, preview tuples and other supported contract surfaces keep their own laws. An empty capability list cannot supply a selected native session; that is a session-selection failure, not a new general manifest refusal. SD-2 does not perform manifest admission, capability admission or protocol dispatch.

The pinned completed structural manifest schema is still the preview schema: its capability oneOf admits only typescript/version1 branches. SD-2 does not claim that TS2/Rust3 capability declarations are admitted by those existing branches, and does not widen them. Before a real native session exists, the manifest/role-scoped capability admission owner must supply the admitted native declaration surface. That upstream schema/materialization duty stays open; a synthetic projection is not evidence it has been discharged. This record confirms the native control tokens once that separately admitted pinned selection exists.

## Confirmation and existing refusal boundaries

hello and select take the exact pinned tuple. Their counterpart messages confirm it under the existing CCv5 state/echo rules; neither side negotiates a different protocol or translates TypeScript/Rust frames. The common control envelope stays at its existing major. CCv5's synthetic generic state-matrix witness and its retained preview analyzer/typescript/1 frames stay unchanged; they are not M3 TS2 or Rust3 tokens.

A host-built tuple differing from admitted selection is M3-D r5's session-spec-inconsistent case: the host detects it before spawn or any frame, using the existing host-invariant route. A provider-spoken mismatch stays in the existing control-refusal/provider-protocol rules and CC's precedence. This record adds no error, exit, public detail code or wire refusal classification; its design checker returns only local evidence fates, not production outcomes.

## Owner duties and closure

D2a constructs/replays the tuple and owns CC's actual frame/state conformance. D4's session factory owns admitted selection/spec consistency. D2b owns per-language transport and NE dispatch with no translation. This record closes M3-L r5 X5/R3's missing manifest-owner confirmation only when accepted and bound. D2a/D2b/D4 and the rest of L's gate remain incomplete. This is not a revision of the accepted supervisor or provider laws and does not reopen their reviews.

## Evidence boundary

The synthetic projection cases retain positive TypeScript/Rust confirmations, irrelevant declaration ordering, and negative role/name/major/type/selection/manifest/capability/offer/echo joins. They do not constitute a full manifest, signed closure, admitted session, control codec or hostile frame/state execution. The Python checker separately pins and inspects existing structural field authorities and published tuple laws, then compares literal expected local fates. No Cargo/compiler/provider/native producer runs, no repository code is launched, and no installation/private413 fixture is read.

Binding changes only the architecture record and a separate product design-lock commit. Inventory166, product code, generated registries/schemas, accepted contracts, SOP drafts and held worktrees remain unchanged. No qualification claim follows.

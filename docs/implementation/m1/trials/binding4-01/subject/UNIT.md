# Design binding v4 candidate

Unreviewed developer-tool unit. No product integration, base approval changes,
commit or push. The live product still uses accepted lock3.

V4 replaces the single inventory/contract slots with explicit nonempty ordered
chains. Additive inventories extend their immediate predecessor; all prior
candidates remain accepted parents for later contracts. Existing acceptance,
source/manifest/assent joins and additive package/row restrictions remain.
Candidate paths cannot overwrite prior accepted inputs. Differing meanings for
the same physical passage refuse; no implicit last-writer-wins rule.

Inventory row-description overrides can propagate to the selected final additive
inventory by stable file path, with the exact inherited before/after pair pinned
in `inventoryPassageInheritance`. JSON indexes are recomputed after sorted
additions; descriptions stay historical raw bytes. This profile refuses other
inventory passage selectors instead of inventing an inheritance rule. A direct
identical final override makes propagation unnecessary; a conflict refuses.

The lock here selects only the already accepted inventory3 and metadata-v2.
No new design unit is approved by changing the lock schema. Tests add synthetic
reviewed histories to exercise future chains. This is a developer checkout
binding, not cryptographic remote attestation, product admission or release proof.

Root validation: existing accepted checkout pins verify under v4; all 29 older
tests and nine chain tests pass (38 total). Actual Claude independent review is
required before integration. No new product paths are introduced by this unit.

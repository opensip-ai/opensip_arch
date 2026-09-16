# Developer design lock v2

Scoped implementation refinement; acceptance pending actual Claude review.

Version1 continues to select the frozen base application. Version2 adds exactly
one `inventorySuccessor` with five closed {path,sha256,bytes} pins: parent,
candidate, record, review and assent. The parent must be a selected base input.
All five files are read from the explicit architecture checkout and hashed.
The candidate is selected separately; it does not replace or rewrite base pins.

This is the bounded additive-inventory profile. It supports the already reviewed
v3 inventory and its existing review/assent record formats. It requires independent
ACCEPT-UNIT plus ACCEPT inventory assessment, empty required findings, root
ACCEPTED-UNIT with substantive assent and no required unit findings, exact
candidate/parent/record/review joins, and matching implementation subject digests.
Historical author-standing fields do not supersede those later decisions.

All inherited file rows must remain equal by value, packages and other inventory
policy fields unchanged, and candidate file rows sorted and unique with at least
one addition. Only the standing text may differ outside files. The verifier
reports the selected path/hash and addition count; it does not attest that every
planned file exists or that product qualification has run.

The checked-in lock is the trust anchor. This is a developer provenance checker,
not a cryptographic reviewer identity service, a runtime authorization mechanism,
or a general design-change approval protocol. Future non-additive inventories
and contract successors need their own reviewed binding profile. No accepted
design bytes or previous review subjects are edited by this refinement.

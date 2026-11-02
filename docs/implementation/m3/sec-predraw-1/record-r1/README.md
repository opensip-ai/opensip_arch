# SEC-PREDRAW-1: the adopted record, bound (LD-Q-260)

Byte copies of the adopted texts and the receipts they depend on. The adopted bytes control; this directory adds no law. There is no contract number and there are no passage overrides, because r7 selects no new public row and a text search found no published contract passage naming the boundary.

**The correction of r7 (LD-Q-257).** r7 §4.3's sentence "The only build the guard newly refuses is `--release --features scenario-fixtures` on security" holds for its measured non-test matrix. `--release --tests` on storage and lifecycle is also refused, because their dev-dependencies enable the fixture feature, which is what the guard is for (evidence guard-release-tests-v1 in the unit's cache, measured at product bcd03cd; LD-Q-257). The adopted text must not be read as exhaustive. No code change and no separate erratum.

**§4.5 (LD-Q-261).** The security-completion.v2 §4.5 contract successor is NOT published here. It is discharged by SEC-HARDEN-1's binding, naming all four consumers (P-1, X4T admission, X4B acceptance, the X4 observer), per SUCCESSOR-SECHARDEN-RELEASE r2 line 28 and LD-Q-261, which corrects LD-Q-260. Until then the adopted COMPONENT-RELEASE-SUBJECT and SECHARDEN records govern, and P-1 implements them.

**Product:** code head `0b5c9abca220a927551a38b9dc46f3a26b30313b` on main `efcb0c6d18e96bd8853b68c22715893b2450eec6`; the final head carries it. Carries stay open as `successor.json` names them. No lane, integration or qualification is established by this record.

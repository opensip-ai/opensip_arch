# ADDENDUM — 367 test-scope wording (not a rewrite of REVIEW.md)

**Standing:** evidence-precision only. Frozen 367 archive and every member remain **unchanged**. REVIEW.md (`d7416012…3fb7`, 6404 B) is **unchanged**. No test, corpus, control, Clippy, or format rerun. No security-native or 368 fixture job.

REVIEW.md standing said native tests were **not** run. That sentence is **too broad**. `cargo test -p opensip-lifecycle` actually ran **32** tests:

| Module | Count | Nature |
|---|---:|---|
| `lineage::` | **12** | Pure codec/callback (plus isolated corpus 565 and six compiled controls) |
| `leases::` | **12** | Real nonblocking filesystem guard/fence/lease matrix under a lifecycle fixture home |
| `selection::` | **5** | Existing five-field selection codec |
| `locations::` | **3** | Syntactic location components |

The **12** `leases::` tests acquire real exclusive/shared/append guards and contend on the local filesystem. They are not the security native observation suite (census, installation fence, native session) and not the 368 synthetic native-lineage fixture. Those two suites were **not** run in this review.

Lineage **12** / corpus **565** / six intended control failures + restored **12** remain pure. Unchanged security files need **no** redundant 367 security rerun. Inventory 54/55 and frozen 368 stay outside this addendum.

---

## Unchanged

REVIEW.md bytes and hash above. Product `fa72e50`. Five-member binding / current authority / writers / M2–M6 remain open.

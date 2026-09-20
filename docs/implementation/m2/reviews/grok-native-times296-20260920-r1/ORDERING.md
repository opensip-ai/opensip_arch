# Independent source-based ordinary clock ordering

**Standing:** separate from the 296 bounded verdict. Read-only comparison of frozen 215 r14 OWNER §C.3, frozen 225 r2 `TIME-PRODUCER.md`, live `ORDINARY-TIME-ORDERING.md`, and the exact 289/295/296 native helpers. No implementation. No cumulative approval. Frozen 215/225 copies inside the 296 extract are the source; live product remains `fa72e50`.

Pins used: 215 r14 archive `cd338af6…dd9c`, frozen OWNER `d8165f14…19fa` (48217 B); 225 r2 archive `84e48e36…c413`, `TIME-PRODUCER.md` `804134cd…0843` (8620 B); integration note SHA256 `0017067b6781781196bae294cc8a995f287b7c7b94028aca466931883380aa2d`. Native chain expiry lives in `verified_root_chains::verify_root_chain` (`ExpiredNoChain`, `FinalExpired`, `FinalFuture`) and is invoked from 289 `prepare` / 295 `verify_captured` before 296 `prepare_times`.

---

## Independent conclusion

C.3 and 225 already specify one order. Relied-on authentication (schema, identity, signatures, finite retained∪incoming union, first presented ROOT, ordered successors, inventory/body joins, derived T1 component authority) completes **before** payload times are used. Authentication failure writes no payload-derived clock. S4 then consumes the 225 ordinary pair — `newestIssuedAt` = calendar maximum of signed manifest, catalog, and revocation list; `presentedRootIssuedAt` = the presented final root-chain document — and publishes its F/L/anchor write-ahead. That write survives a later entry refusal. **After** the resulting `tEval`, shared root/list validity, anti-rollback, same-version identity, remaining T1 guards, and `importCompleteness` apply. P0→P1 is the first successful S4 write, even when later role admission fails. A root that exists only inside that proof is not an accepted head.

296's projection rules match the 225 ordinary row: three-source maximum excludes the root; root issue is a separate scalar; catalog/root `expiresAt` are evaluation inputs, not S4 write inputs; presented DocRefs are the closure members, with the root source equal to `rootChain` last, not the same-head historical projected ref. Calendar-invalid source strings fail before any S4 call. That local contract is sound **as a producer of candidate scalars**.

The integration gap is also real, and it is specifically **evaluation-time root expiry/future inside the full chain helper**, not a defect in 296's max/ref arithmetic. 289/295 pass caller `evaluation_time` and `wall` into `verify_root_chain` before 296 runs. Frozen 296 fixtures `same-head-expired` and `final-expired` still refuse as full-root errors: supplied `evaluation_time` equals `expiresAt` while `wall` remains inside the document interval (`2026-10-05` vs expiry `2027-10-01`). C.3 wants S4 to run on authenticated payload times first; blocking at 295 prevents the write-ahead that must survive a later expiry refusal at `tEval`. 296 cannot be wired unchanged as the complete pre-S4 producer.

---

## What may legitimately refuse before writes

Keep these as pre-S4 / pre-dispatch no-write failures (C.3 “D states”; 225 “authentication precedes time”):

- Missing, empty, malformed, or digest-unjoined envelopes and members (DR-103).
- Bad signatures, below-threshold or second-pass-revoked shared keys, first-ROOT or successor quorum failure, identity/chain `+1`/previous/nondecreasing-issue breaks.
- Intrinsic interval **shape** (`issuedAt < expiresAt` on the document; unparseable calendars). This is grammar, not `tEval >= expiresAt`.
- 296 calendar stamp failure on manifest/catalog/list/root issued or expiry fields.

S4 future/range/horizon preflight is also a **no-write** refusal, but it is **after** authentication and **after** the 225 producer has selected the two scalars. 225 is explicit: any future source, including root, yields `PAYLOAD-NOT-ADMISSIBLE` with empty writes; unauthenticated future documents refuse as `authentication` and never reach that kernel. Do not invent a bypass flag. Do not replace public outcomes.

Do **not** refuse before S4 write solely because a caller-supplied `evaluation_time` is already at or past root/list `expiresAt`. That is an entry guard at the **resulting** `tEval`. C.3 still requires the authenticated-witness write-ahead (P0→P1) when S4 itself accepts, then a later completeness/expiry refusal that preserves heads and discloses the clock revision.

Anti-rollback and same-version identity likewise belong at `tEval`, not in the pre-time authentication type.

---

## Future-root overlap with S4

`verify_root_chain::FinalFuture` (`issuedAt > wall + 86400` on a successor) and S4's payload/root future preflight overlap in **outcome class** (no write now) but not in **boundary**. Frozen `future-successor` uses wall `2026-09-29` and successor issue `2026-10-02` (> 1 day) and dies in 295 before 296. 225's kernel fixtures refuse a source two days past wall as `PAYLOAD-NOT-ADMISSIBLE` **after** asserted authentication.

Exact required ordering:

1. Pre-time authentication succeeds for an otherwise-authentic future root (no `FinalFuture` in that type).
2. 296/225 producer emits `presentedRootIssuedAt` / `newestIssuedAt`.
3. S4 future preflight may refuse with no write. That is legitimate.
4. A later operation with a later wall may succeed; mixing wall into “authentication” hides that the document was authentic.

Expired authentic roots are the case that **changes write-ahead**. Future authentic roots usually do not write either way; the defect is classifying them as authentication failures. Keep paired tests: authentication evidence present, S4 success absent.

`future-manifest-is-only-a-candidate` in 296 correctly stores a future manifest timestamp as a candidate and does **not** run S4. That is the right checkpoint behavior; it is not an S4 pass.

---

## Critique of planned 297

Agree with the plan:

- Keep the full 289/295 helper and its 42/49-case eval/wall contract for existing consumers.
- Add a **distinct** pre-time result. No conversion into full current-root admission. No arbitrary evaluation/wall inputs.
- Retain intrinsic body/schema/calendar grammar, reader, root identity, version/previous/`+1`, nondecreasing issue, actual old/new signatures, finite-union threshold, first-presented ROOT, and bounded capture.
- Compose with shared BUNDLE/catalog/list authentication, 293 inventory-body joins, and 294 T1 component authority. Current/BEGIN/history/population stay independent.
- Feed 296/225 scalars to S4; persist original-context proof before floor publication; apply root/list validity and remaining entry guards at resulting `tEval`.
- Expired/future authentic roots may yield authentication evidence without entry or S4 success. Bad signatures and malformed intrinsic intervals remain pre-time failures.

Required precision, as a correction to the integration note rather than a disagreement with its direction:

1. **Split eval-expiry from future.** The harm that actually drops a C.3 write-ahead is `ExpiredNoChain` / `FinalExpired` against supplied `evaluation_time`. `FinalFuture` is the S4-overlap case and should move to S4 preflight, not stay in 297.
2. **Split intrinsic interval from eval expiry.** `issuedAt < expiresAt` on the document stays in 297. `tEval >= expiresAt` does not.
3. **Do not pass wall/eval into 297** even as ignored extras. The full helper remains the only owner of those premises.
4. **296 follows 297, not full `verify_root_chain`.** Catalog/root expiry scalars projected by 296 are later evaluation inputs (C.3/D presented expiries), not authentication predicates and not S4 write fields.
5. **No silent public-outcome rewrite.** Map S4 future refusals onto the existing `PAYLOAD-NOT-ADMISSIBLE` family; keep authentication refusals at the pre-dispatch no-write boundary. Do not add a bypass flag.

No 297 implementation is requested or performed here.

---

## Verdicts

- [x] C.3/225 order is: authenticate → 225/296 scalars → S4 write-ahead → remaining guards at `tEval`.
- [x] 296 projection matches the 225 ordinary source set and must not be wired through 289/295 eval expiry.
- [x] Planned 297 is the right split if eval-expiry and `FinalFuture` stay out of the pre-time type.
- [ ] Not clock authority, current context, bootstrap, active-batch barrier, host/effects/custody, product installation, or cumulative readiness.

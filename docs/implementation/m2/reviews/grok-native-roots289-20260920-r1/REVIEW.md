# Independent review — ordinary presented-root adapter 289

**Standing:** bounded native-Rust review of frozen `native-ordinary-roots-checkpoint-289`. This is a private full-component-set **conditional** adapter: it composes 284's previously unresolved root pairs with existing `verify_root_chain` and an explicit presented-first-root envelope check. It does **not** admit a current head, replace 229 bootstrap, qualify clock/population/custody, or implement T1 DR-103/DR-112. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 287/288 and 285/286 (`ROOT-INTEGRATION.md` `8468b4fa…75cc`) were not used as 289 evidence. A wording-only count clarification of the 287/288 REVIEW (beforeimage retained) does not change those verdicts.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8093200 B, 1018 members, SHA256 `457640434b559091f53e2a3d8e6a26ce0dc7362769487c6bc2e655cf7fc7bf03`**. Standing: unselected private289 ordinary shared-root adapter, conditional context. Extract rehashed **1018/1018**. Product-inputs **437/437**. Nested parent 288 pin `a0655354…1e30` equals reviewed 288; live 288 trial tar matches. Nested 265 `73c3b3f5…86df` (2290904 B / 1630) live-matches; the nested 265 candidate including C.3 was rehashed with the extract. Product vs 288: **437** files, **434** unchanged; `trust.rs` `682f67bf…471f` plus `trust_ordinary_roots.rs` `c51b5df3…4fa2` and `roots289.ndjson`. `prepare` / `Evidence` are `pub(super)`. Not in `lib.rs`.

Initial oracle reused 284's verifier configured only for catalog/list/manifest and refused every root (`first-envelope`). Failed log, `ordinary_roots_reference289-before-root-reader.py`, and 38/40/41 fixture beforeimages are retained. The oracle was corrected to an explicit ROOT reader **before** the first native test; production algorithm is the r5 42-case corpus.

---

## Adapter law (independent scrutiny)

Earlier 285/286 `ROOT-INTEGRATION.md` stated the genuine gap: `verify_root_chain` takes an externally admitted anchor and proper successors and does **not** re-authenticate a delivered first-root envelope, while C.3 forbids waiving shared ROOT signatures. The required adapter, without circular TR-CORE or bootstrap reuse:

1. First accepted **body** identity equals the supplied accepted head; keep that DocRef. Alternate envelope spelling of the same body is not a fork.
2. The **presented** first-root envelope is shared input under the current filtered ROOT quorum (finite union). That check does not admit a new current root and does not replace 229.
3. Ordered proper successors feed existing dual old/new `verify_root_chain`.
4. Final captured body equals the 283/284 BUNDLE signing-root context.
5. Same-head / empty successors keep the original accepted DocRef and still apply accepted-root expiry.

**289 implements that adapter as a private `ordinary_roots::prepare` on the same Budget as 284.** Distinctions that remain in force:

| Bound | 289 behavior |
|---|---|
| Supplied accepted root / provenance | Caller `ValidatedRootPayload` + original DocRef; not native current-head admission |
| Presented first envelope | `verify_envelope` under **accepted** ROOT keys, then `filter_envelope_revoked(shared.union())`; `QuorumState::Met` required |
| Historical original envelope | Loaded for SHA+length byte-binding only; old signatures are **not** required to meet today's quorum |
| 284 roots | Still named `unresolved_roots`; resolved only by this outer chain evidence |
| Bootstrap C.1 | Payload `rootChain[0]` is **not** used as embedded-bootstrap anchor |
| TR-CORE | Inventory signatures are not the reason the accepted identity is trusted |
| Finite union | 284 retained∪incoming **list** keyIds (plus caller revoked), passed through to first-envelope filter and `ChainContext.revoked`. Not a newly extracted per-successor chain-report census |
| T1 DR-103/112 | Not implemented; full component set still required |
| Empty successors | `projected_accepted_ref` is the **original** accepted DocRef, including alternate presented envelope |
| With successors | Projected head is the last captured inventory DocRef |

C.3 genesis (“complete admitted immutable core embedded chain from its index-zero anchor”) remains 229. 289 is the already-accepted-head path.

---

## What `prepare` does

DocRef shape of `accepted_ref`; same-Budget load of original body **and** envelope; parsed original body equals supplied accepted root. Then 284 `ordinary_quorums::prepare` (inventory / BUNDLE / catalog / list / component / finite union). First presented body equals accepted body; last body equals signing-root context. Presented first envelope is the shared ROOT check above. Remaining pairs become `WireRootLink` into `verify_root_chain` (dual threshold, +1/previous, nondecreasing issue, expiry/future under the **same** union). Evidence owns original/projected DocRefs, presented-first quorum, chain proof, and nested 284 shared facts after input/Budget drop. Time, wall, and retained revocations stay caller-supplied.

42 signed cases, 8 initial / 8 repeated positives. Baseline 11/30/15783; repeat 11/60/15783; 11 physical captures. Corpus covers same-head, alternate historical envelope, one/two successors, short/bad first signatures, isolated first/old-successor/new-successor filters, gaps/backdate/forks/missing prefix/final-not-last, expiry/future, original DocRef shape/presence/length/context, isolated accepted-body vs first-presented identity (case 42), and budget/link limits. Existing chain byte-budget is inherited, not newly boundary-qualified.

**Executed:** `cargo clean -p opensip-security` then **235/235** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **eight** include files. 15/15 r2 compiled controls core-equal frozen `mutation-check-r2` (live baseline cargo skipped; unpatched source SHA matched frozen baseline `c51b5df3…4fa2`). Frozen r1/r2 dirs not overwritten. r1 41-case corpus also recorded all-caught; r2 is the 42-case isolate.

**Controls (7 wrong admissions):** `omit-accepted-doc-shape`, `omit-first-body-identity`, `omit-final-signing-body`, `omit-first-revocation-filter`, `omit-first-quorum`, `ignore-link-bound`, `substitute-other-proof-on-first-error`.

**Other-first (8; counters/facts/over-refusal, not operational exploits):** `omit-original-envelope-load` (edge count 29 vs 30); `omit-accepted-context-identity` still refuses case 33 but after full 284 counters `(11,30,15783)` vs expected `(2,2,8736)` — case 42 would isolate a wrong admission, but the earlier counter check fires first; `omit-successor-revocation-filter` (signer/union disjoint fact); `omit-successor-chain` (link count); `accepted-envelope-replaces-presented` over-refuses the alternate-envelope positive (`FirstQuorum`); `replace-first-accepted-reference` / `lose-original-reference` (owned DocRef facts); `omit-failure-latch`.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 289 pins before extract | match |
| Nested 288 / 265 live tars | match |
| Live `cargo test -p opensip-security` | **235/235** after force rebuild |
| Clippy / fmt / rustfmt 8 includes | pass |
| 289 r2 mutants | 15/15 frozen-equal; 7 wrong / 8 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Admitted current head / history / population / time / custody producers; T1-derived DR-103 vs DR-112 ordinary-import gate; 285 catalog/component semantics and 286 packaged policy as signed-time evidence after that gate; role-record effects, clock write-ahead, physical capsule/fence/census/writers; 229 bootstrap; source/runtime selection; M3–M6. 289 is not shipped behavior, selected registry, or cumulative approval.

---

## Verdicts

- [x] **289:** archive/pins verified; presented-first-root envelope is shared filtered-ROOT input on the 284 Budget; original accepted DocRef preserved on same-head/alternate envelope; proper successors use existing dual-quorum verifier; 7/8 mutant classification reproduced; 235/235, Clippy, fmt, 8-file rustfmt.
- [ ] **Not** current-root authority, bootstrap, T1 ordinary import, clock/publication, or product installation.

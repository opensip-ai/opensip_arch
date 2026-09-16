# Independent Grok advisory: retained-relations-06

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not M2 complete. Not ACCEPT-DESIGN-UNIT. Not native ADMIT. Not complete relation admission.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-retained-relations-review-06/review`. Live product, frozen implementation bytes, architecture history, and commits were not edited.
**Prior:** payloads05 advisory `a06488aa…ac5a`, **requiredFindings []**. Recognition-derived identity-model `619d6e3c…c141e6` is live lock **9 inventory / 14 contract**. Relation-payload boundary advisory `c5f91c71…01db` is a vector account, not this freeze. No fresh blindness claimed. Other Grok is reviewing the Unicode crate policy; this review does **not** select live dependency policy. Root’s next CVE1/capability work and the reference exception-totality gap are unrelated to 06.

## Standing

Subject: **pure relation local/source diagnostic prototype**. Copied product lock is historical **9/12**. `inspect_relation_payload` / `inspect_relation_sources` are diagnostic helpers. They are **not** substituted for the general graph walk, which still refuses relation/import `payloadClass` (`Unsupported("payload-class owner joins")`). Syntax capability, admitted-target universe, source-body identity, and coverage totality remain later owners. Diagnostic fact fragments in tests are **not** full fact shape or native evidence.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` (frozen, immutable) | 45807 | `c57c1244f5ef9eef496d8eced7bf231cad2d6a3b620a0d2b6e7993ee194dfae9` |
| archive-pin `subject.tar.gz` (historical gzip) | 716045917 | `1dd63e1b13efc9df95b5be19d5601ecfefdd769fc77c36da764ff74a5ee46a09` |
| preserved original gzip | 716045917 | **match** at `/tmp/opensip-implementation/m2-retained-relations-06-original-archives/subject.tar.gz` |
| alternate XZ | 527280508 | `ac6db6b42782cf0bf691ae35f4ff672433d69aa2002366bfc2205d4513597294` |
| Frozen root members | 259 | 0 missing / 0 mismatch vs `subject.json` |

Did **not** extract the 716MB gzip into the review tree (repeated schema). Copied `product/` + `harness/` **without** `target/`. Streamed `*.ndjson.gz` from frozen root. Extra uncompressed `*-requests.ndjson` exist on the frozen root and are intentionally **not** subject members.

A later portable `portable-subject.json` (`506314fc…8302`, 46208 bytes) is packaging, not this freeze.

`digests.rs` / `schema_registry.rs` / `descriptors.rs` are **byte-identical to payloads05**.

## Relations06 delta (on payloads05)

New `product/crates/identity/src/relations.rs` (`af375b0d…45cc`, 12826) ports selected `relation_annotation_closure` / pure `relation_payload_rules`:

- governed DigestHex / Sha256Text / CanonicalPath via `$ref` aliases, inline pattern copy, containers, `oneOf`/`anyOf`/`allOf` branches
- typed annotation merge (`JsonValue` equality: `1 != true`)
- monotonic missing poison
- retention / unjoinable / residue / unknown join-field
- local ladder, rung required/forbidden, `anchor_law` cardinality/minimum, `same-only`, Unicode **16** NFC strings/keys, nonnegative integers

Public diagnostics always use the **immutable registered** relation document (`foundation/relation-payload-schemas.v2.json`, full-file SHA `53380a24…be9a`) plus exact retained schema blob. No caller-chosen schema at the production boundary. Harness `relation-law` compiles the **same** `relations.rs` via `#[path]` for hypothetical documents (test-only).

`inspect_relation_sources` additionally recomputes owning snapshot identity and selected `snapshotJoins` (inventoried path/content/length, retained rehash, deleted-VCS `unless`). **`bodyIdentityJoin` → `Unsupported("relation body identity owner")`.**

Proposed crates (not live policy): `unicode-normalization = 0.1.24` `default-features=false` (crate `UNICODE_VERSION = (16,0,0)`), `tinyvec 1.13.3` with **`alloc` only** via that crate. Archives and Cargo checksums pin-match. Contracts dependency policy unchanged.

## Initial source harness (preserved, not a runtime fix)

First source run used domain `project` (not in the 19 `IdentityDomain`s). Harness `IdentityDomain::parse(...).unwrap()` panicked (`initial-harness-source.stderr`, exit 101, 2 rows then nulls). Test input corrected to registered **`closure`** (wrong-domain still `invalid` via `ObjectDomain`). Initial report/stderr preserved. **No runtime/reference change** for that.

## Independent reproduction

Trusted rustc/cargo **1.95.0**, `--offline`, private `CARGO_TARGET_DIR`. Gzip decoded **line-by-line** into the harness while hashing; uncompressed 3.1GB relation corpus was not buffered.

| Check | Result |
| --- | --- |
| 259-file pin vs frozen root | match |
| Historical gzip pin (preserved copy) | match |
| `retained_input_tests` | **18/18** |
| `cargo test --workspace --all-targets` | **79 passed**, 0 failed |
| Clippy `--workspace --all-targets -D warnings` | exit 0 |
| Law gzip stream | 243, 126 ok / 117 invalid, SHA `571bec2d…97b5` |
| Source gzip stream | 161, 89 ok / 48 invalid / 18 unavailable / 6 unsupported, SHA `a03c1b0c…b5eb` |
| Relation gzip stream | 26931 (26391 `unicode-*`), 13184 ok / 13730 invalid / 17 unavailable, SHA `f01c8662…539b` |
| payloads05 predecessor 4441 | **unchanged**, harness match |
| Independent negatives | **ALL_PASS** |

## Independent probes

- `UNICODE_VERSION == (16,0,0)`; composed `é` is NFC, `e\u0301` is not
- `parse_json(b"1") != parse_json(b"true")`
- full relation schema SHA `53380a24…`; wrong digest → `PayloadSchemaDocument`
- calls `admitted-target` different universes still locally ok (not native/universe ADMIT)
- empty anchors → `anchor cardinality`
- second fact / different snapshot does not reuse the first inventory (`path not inventoried`)
- clones `bodyIdentityJoin` → `Unsupported("relation body identity owner")`
- graph walk of a fact `payloadClass=relation` → `Unsupported("payload-class owner joins")`

Law corpus already includes missing-annotation, alias/container/branch, and typed `(1,True)` pair locations (historical `check-identity.py` `8e7100c5…df9f`).

## Findings

**Required:** none relative to the trial’s stated diagnostic standing.

**Should-fix:** none new for this freeze.

**Not findings**

- Diagnostic helpers are not complete relation admission and are not graph substitution.
- `unicode-normalization` / `tinyvec` are proposed locked crates; live source-policy selection is a separate Grok review.
- Test facts are fragments, not identity-candidate full facts.
- Initial source harness panic was a **test-input** domain, preserved; not a runtime defect of `relations.rs`.
- Portable/XZ repack after freeze does not change `subject.json` members.

## Limits

- Advisory only. Not acceptance of relations06, payloads05, M2, native ADMIT, or release.
- Did not execute `close_run`, `syntax_capability_supported`, admitted-target universe, `body_identity_join` (refused here), compiler, or complete evaluator replay.
- Did not unpack 716MB gzip into the review tree; verified the pin on the preserved original and the 259 frozen-root members.
- Copied product `design-lock.json` is historical 9/12.
- Root continues CVE1/capability separately; exception-totality gap is out of scope.

## Conclusion

Relations06 adds a bounded **pure law + local payload + snapshot-join diagnostic** on payloads05. Unicode 16 NFC, full retained schema SHA, typed annotation equality, per-fact snapshot identity, deleted-VCS exemption, and explicit body-join Unsupported all match the stated standing. General graph relation/import remains Unsupported. Predecessor 4441 is unchanged.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.

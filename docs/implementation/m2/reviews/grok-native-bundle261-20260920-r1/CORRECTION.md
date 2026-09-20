# Correction to REVIEW.md (two wording claims)

**Standing:** report wording only. Frozen `REVIEW.md` (`988feaec8cab7edced36d4cdf298e64f7e2eda6548d9ecff6e947745e7ea3492`, 6023 B) is **preserved unchanged**. No production edit, no test rerun, no review restart. Bounded 261 verdict is **unaffected**.

Checked against frozen 261 `product/crates/security/src/trust.rs` (`d168cd02…7954`) and the existing payload2 path pattern in `root-recovery-payload.schema.v2.json` (258/252 copy; pattern `"^[^/][^\\x00]*$"`).

---

## 1. Path syntax does not close “no NUL”

REVIEW.md §“What 261 adds” says member lists are “1..=1024 chars, no leading `/`, **no NUL**.” That over-closes the syntax gate.

Frozen `member()`:

```3505:3511:product/crates/security/src/trust.rs
let mut chars = p.chars();
(1..=1024).contains(&p.chars().count())
    && chars.next().is_some_and(|c| c != '/')
    && chars.all(|c| c != '\0')
```

The first character must not be `/`; **remaining** characters must not be NUL. A NUL in the **first** character still satisfies this stage (`chars.next()` only tests `!= '/'`; `chars.all` then walks the tail).

That matches the existing payload2 regex `^[^/][^\x00]*$`: `[^/]` may be U+0000; `[^\x00]*` applies only after it. Inherited schema syntax, not an authorization grant.

Full-path preflight that rejects NUL **anywhere** remains 262 `logical()` / index. 261 did not close that condition. Path identity, NFC, casefold, aliases, reserved frames, and file-parent conflicts stay pending as already listed.

---

## 2. `SignedDocument::capture` order is cap → parse → copy

REVIEW.md says capture “copies body and raw envelope bytes only after both 4 MiB caps, then internally parses.” That reverses the last two steps.

Frozen `capture()`:

1. Bound both inputs (`body.len()` and `envelope.len()` vs `MAX_BYTES`) → `Limit`.
2. Parse the **raw envelope** (`metadata::parse(envelope)`) → `EnvelopeMetadata`.
3. **Then** copy `body` and `envelope` into owned fields with the internally parsed `V`.

Parse happens on the caller slice **before** `to_vec()`. No caller-supplied parsed env. Caps-before-copy and exact-byte ownership after a successful parse still hold; only the parse-vs-copy order was misstated. The `capture_bounds_both_raw_documents_before_parsing` test name matches this order.

---

## Verdict impact

None. Syntax-only paths and 262 remaining work are unchanged. Capture still refuses oversize inputs, still parses internally, still owns exact source bytes. No public API, inventory, or native-authority claim is affected.

# Correction to REVIEW.md (one wording claim)

**Standing:** report wording only. Frozen `REVIEW.md` (`367ae8b171f56f821ab04967ae1a3dcbfbfc90d0e037d196180816b54b009b96`, 7655 B) is **preserved unchanged**. No production edit, no probe rerun, no review restart. The inventory finding and the proposed captured-pair length comparison remain **valid**.

Checked against frozen 261 `SignedDocument::capture` (261 CORRECTION.md `0f559fdd…0acd`, product `trust.rs` capture order) and against native 264 `Budget::load` as the declared-length owner.

---

## 261 does not take a BlobRef declared length

REVIEW.md §“Smallest correction” says: “261 already bounds both `SignedDocument` inputs by declared size before parse.”

That over-assigns declared-length ownership to 261.

Frozen 261 `SignedDocument::capture`:

1. Apply two **4 MiB caps** (`body.len()` and `envelope.len()` vs `MAX_BYTES`) → `Limit`.
2. Parse the **raw envelope** on the caller slice.
3. **Then** copy body and envelope into owned fields.

There is **no** `BlobRef.bytes` input. The caps are raw-slice upper bounds, not a join of a declared integer to captured length. 261 CORRECTION.md already recorded cap → parse → copy; this note only retracts the “declared size” phrasing.

The declared-length owner for inventory DocRefs is **new 264 `Budget.load`**: closed BlobRef, charge each ref edge including cache hits, check declared length **before** the capture callback and against a cached length. 265/`_prepare` then joins already-captured pair lengths to both DocRef BlobRefs (no extra I/O).

The gap (`_prepare` SHA-only envelope join for catalog/list/other-root) and the smallest captured-pair comparison remain as originally reported.

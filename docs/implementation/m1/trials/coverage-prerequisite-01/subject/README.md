# Coverage prerequisite correction

This candidate closes RP-OBL-K01 by adding exactly
`moduleFirstMilestone["crates/reporting/src/assets.rs"] = "M1"` to the accepted
metadata-v2 coverage document. The existing `version` delivery row already owns
that file and is scheduled for M1. The separate accepted repository layout
assigns the sole compiled build-channel declaration to that file.

M0 also passes the validator's ordering comparison. That does not make M0 the
right implementation milestone: it is the design baseline. M1 is the first
required implementation use. M6 fails the prerequisite comparison.

The validator is unchanged. `python3 -I -B check.py` checks 40 external byte
pins, the exact one-key semantic delta, all 322 corrected base rows, and all
323 rows after composition with the separately pending report05 overlay. It
uses no validator workaround, and still detects command metadata drift.
All existing `not-executed` verification standing is preserved. This does not
select the pending report overlay or qualify implementation behavior.

The complete successor retains its historical `standing` prose and other
metadata unchanged to keep the semantic delta exact. `successor.json`, the
frozen manifest and eventual root assent own this correction's current standing.
Historical metadata-v2 files remain unchanged. On acceptance, downstream report
work must explicitly bind this successor and remove its temporary workaround;
that downstream rebase is not performed by this isolated reference check.

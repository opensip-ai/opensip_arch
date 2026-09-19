# NOTES — correction to N-1 of my 174 review (the archived REVIEW.md is unchanged)

Date: 2026-09-19. Raised by the owner; verified by me.

**My 174 N-1 inferred a "1 MiB" limit in the product JSON reader. That inference was wrong.** The frozen product's
limit is `crates/identity/src/canonical.rs`: `pub const MAX_BYTES: usize = 4 * 1024 * 1024;` and `parse` returns
`Error::ByteLimit` when `raw.len() > MAX_BYTES`.

What actually happened in my corpus r2: the seven refused case documents carried *both* inventories as explicit rows
with 4-byte scalars. The sizes I printed (1,172,359 … 1,456,566) were `len()` of a Python `str` — **characters, not
bytes**. Rebuilt in their original form and measured in UTF-8 bytes (`claude-out/io/n1-recheck.txt`):

| r2 case family | characters | UTF-8 bytes | > 4 MiB |
|---|---|---|---|
| legacy over BYTES | 1,181,349 | 4,237,776 | yes |
| over COUNT and BYTES | 1,456,040 | 4,575,740 | yes |

So the same reader (`opensip_identity::parse_json`) refused them correctly at its real 4 MiB bound; no other reader was
involved. My r3 re-expression as `series` recipes was still the right repair for the probe.

Consequences for the note:
- Withdraw "refuses inputs over 1 MiB" and the sentence "a 2 MB disclosure … cannot round-trip through that reader as
  one document". A lawful maximum disclosure (2,088,960 bytes) **does** fit under 4 MiB; the reference's own assertion
  `2 * MAX_PIN_DISCLOSURE_BYTES + REPRESENTATION_RESERVE_BYTES <= MAX_JSON_BYTES` (4,194,304) is exactly about a
  *before + after* pair fitting one document, and my r2 documents exceeded it only because they also carried the
  over-limit legacy inventories (each already above the disclosure ceiling) plus JSON row overhead.
- What remains true and worth keeping: a document holding two **over-ceiling legacy** inventories can exceed 4 MiB, so a
  test or tool that wants to exercise legacy strict-decrease with explicit rows must use recipes or two documents.
- No finding, verdict or evidence of the 174 review changes. Do not carry a 1 MiB product limit forward.

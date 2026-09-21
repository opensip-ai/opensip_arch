# Independent review — private UTC-second formatter 303

**Standing:** bounded native-Rust review of frozen `native-timestamp-checkpoint-303`. Private `format_timestamp` is the inverse of the existing UTC-second parser. It does **not** adopt proposed 300 sampling or 302 use-age/mapping policy, read an OS clock, retune S4, or publish. A separately frozen host-collector pilot 304 is **out of scope** and is not qualification. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–302 reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor). 302 was reviewed independently first; this report does not implement or select that policy.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8858720 B, 903 members, SHA256 `30913a8326cb12d02905f4d1964a179948d1cece5d8f2affb3be546a846f5337`**. Standing: unselected private303 UTC-second formatter; no OS or authority. Extract rehashed **903/903**. Product-inputs **454/454**. Nested parent 301 pin `b6db23ad…906b` equals reviewed 301 (live tar match). Nested 215 r14 `cd338af6…dd9c`, 225 r2 `84e48e36…c413`, 265 `73c3b3f5…86df` (live 265 tar match). Included `kernel201.py` SHA256 `df45c9c5…2299` (byte-identical to the 265/201 lifecycle `iso` module; prepare script asserts that hash). Product vs 301: **454** files, **452** unchanged. Changed: `trust_time.rs` `b76c829f…1dc4f`. Added: `timestamp-format303.ndjson` (1167490 B, SHA256 `5424cfcf…17fc`). `trust-time-before.rs` is byte-identical to 301 `trust_time.rs` (`1b845612…34f1`). `format_timestamp` is **not** in `lib.rs` (`lib.rs` SHA256 `22c8ca47…e746`, equal to 301).

`timestamp_seconds` body is **byte-identical** to 301. `assess_kernel` and `evaluate_retained_ordinary` are **byte-identical** to 301. DAY/HORIZON/calendar constants are not retuned. No `observe_clock`, use-age, or `HOST.IO_FAILURE` mapping appears in this freeze.

---

## What the formatter does

Private `pub(super) fn format_timestamp(seconds: i64) -> Result<String, TimestampGrammar>`:

1. Inclusive calendar bounds `[-62_135_596_800, 253_402_300_799]` (year **0001-01-01T00:00:00Z** through **9999-12-31T23:59:59Z**). Outside: `Err(TimestampGrammar)` — the same refusal type as the parser.
2. Euclidean `div_euclid` / `rem_euclid` against `DAY = 86_400`, then `+ 719_162` (the same proleptic-Gregorian epoch day the parser uses). Truncating `/` and `%` would map negative Unix seconds onto the wrong civil day; compiled controls catch that.
3. Bounded year binary search `low=1, high=10_000`: largest year whose `year_start` (365/4/100/400 on `year-1`) does not exceed the ordinal. Gregorian month lengths including century leap (`year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)`), 0-based day-in-year, then exact 20 ASCII `{year:04}-MM-DDTHH:MM:SSZ`.

No ambient timezone, float conversion, locale, or OS/filesystem read. The function is a codec, not provenance. It is referenced only in `trust_time.rs` (definition + tests). Existing `timestamp_seconds` still refuses year 0000, `sec > 59`, and non-20-byte grammar; the formatter never emits those forms inside the closed range.

Fixture oracle is pinned 265/201 Python `iso` (explicit four-digit year, not `strftime %Y`) plus a round-trip through the **unchanged** Rust parser. Tests do not treat parser/formatter agreement as the expected string. Corpus: **31046** rows, **31042** valid, **4** out-of-range (`i64::MIN`, `MIN-1 = -62135596801`, `MAX+1 = 253402300800`, `i64::MAX`). Valid rows include first and last second of every year 1..9999, last second of every February, signed epoch/hour/minute/day boundaries, and 1024 seed-303 random in-range seconds. Independent count: **9999/9999/9999** Jan-1 / Dec-31 / February-last coverage. Independent Python `iso` and `datetime` spot-checks of MIN / `-1` / `0` / MAX equal the fixture (`0001-01-01T00:00:00Z`, `1969-12-31T23:59:59Z`, `1970-01-01T00:00:00Z`, `9999-12-31T23:59:59Z`). Century non-leap `1900-02-28T23:59:59Z` and leap `2000-02-29T23:59:59Z` match. OOR four rows are `null` in the fixture and `Reject` in `iso`.

**Executed:** `cargo clean -p opensip-security` then **248/248** with `Compiling opensip-security` (301 was 247; added `inverse_timestamp_matches_primary_over_all_year_boundaries_and_signed_epochs`). Existing `metadata_timestamps_match_corrected_reference` (57524 parser cases) still **ok**. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 8/8 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped, covered by the forced 248). Frozen mutant dir not overwritten (`report.json` SHA256 `5c93495f…0e47`). No compile-fail or production correction.

**8 compiled controls (all caught):** `lower-endpoint-rejected`; `upper-endpoint-rejected`; `negative-days-truncated` (`/` instead of `div_euclid`); `negative-remainder-truncated` (`%` instead of `rem_euclid`); `wrong-epoch-day` (`+ 719_163`); `century-leap-incorrect` (omit 100/400); `year-boundary-exclusive` (`<` instead of `<=`); `missing-four-digit-year` (`{year}` instead of `{year:04}`).

No numerical, overflow, signed-remainder, year-padding, or Gregorian-calendar defect found in this freeze. Inclusive endpoints are required: a max-exclusive upper bound would refuse `9999-12-31T23:59:59Z`; a min-exclusive lower bound would refuse `0001-01-01T00:00:00Z`.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 303 pins before extract | match |
| Nested 301 / 265 / kernel201 `iso` | match |
| `timestamp_seconds` / `assess_kernel` / `evaluate_retained_ordinary` vs 301 | byte-identical |
| Proposed 300/302 policy | **not used** |
| Live `cargo test -p opensip-security` | **248/248** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 303 r1 mutants | 8/8 frozen-equal |
| Independent MIN/`-1`/0/MAX `iso` | match fixture |
| Host-collector 304 | **not inspected** (not this codec) |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

This is a private inverse of the existing Timestamp grammar. It does not authenticate `timeEvidence`, sample a host clock, apply 302 use-age, or publish F/L/anchor. Current provenance, S4 publication, bootstrap/active-batch, context/custody/fence, full host/platform, source selection, and M3–M6 remain open. 304 does not qualify 300/302 and was not used here.

---

## Verdicts

- [x] **303:** archive/pins verified; pure private formatter inverse of unchanged parser; year 0001..9999 inclusive Euclidean/Gregorian/20-ASCII; primary 265/201 `iso` oracle plus parser round-trip; S4 kernel unchanged; no 300/302 adoption; 8/8 mutants; 248/248, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** OS qualification, 302 policy implementation, current-head/history proof, durable S4 publication, host installation, completeness, grant, or product installation.

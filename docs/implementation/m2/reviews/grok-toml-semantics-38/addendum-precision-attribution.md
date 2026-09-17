# Precision note: digit-limit attribution and TOML integer range

**Separate from** original `advisory.md` **8474** / `3e2c8365df8c690652994fae8d5127e3609637df976b279f87b28535ec12c56d` and numeric-totality addendum **7147** / `157150dd…7742`. This note does **not** rewrite those texts.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Attribution and spec-precision corrections only. **Not a new reference unit. Did not modify reference or product.**

The numeric-totality addendum stated two things that should not be carried forward as law. The original incomplete-radix report does not depend on them.

## 1. Digit limit is not PEP 3319

CPython’s `sys.int_max_str_digits` / `-X int_max_str_digits` / `PYTHONINTMAXSTRDIGITS` is **CVE-2020-10735**, CPython **gh-95778**, landed for 3.11 (`int`↔`str` conversion DoS; default 4300 decimal digits; 0 disables). Docs: `library/stdtypes.html` “Integer string conversion length limitation.” Power-of-two bases (hex/oct/bin) are not limited. There was discussion of writing a PEP; the shipping artifact is the CVE/issue, not PEP 3319.

Do not cite PEP 3319 for this cap.

## 2. TOML 1.0 does not mandate arbitrary-precision integers

TOML v1.0.0 Integer section:

> Arbitrary 64-bit signed integers (from −2^63 to 2^63−1) should be accepted and handled losslessly. If an integer cannot be represented losslessly, an error must be thrown.

That is **64-bit signed representability guidance**, plus a **must-error** if the implementation cannot store the value losslessly. It is not a requirement to accept unbounded integers. An implementation that rejects `2^63` as unrepresentable can still be reading that sentence.

CPython `tomllib` uses Python `int` (arbitrary precision) and therefore **accepts** literals outside i64 rather than throwing. Identity `DeInteger` **retains the literal** and does not convert, so it also does not throw on width. Those are **CPython tomllib / OpenSIP profile choices**, not “TOML 1.0 requires unbounded integers.”

The numeric addendum’s sentence that “TOML 1.0 integers are unbounded” over-claims the spec. Unbounded **literal retention** (no i64 narrowing, no `to_i64` parse gate) remains the selected-oracle profile while tomllib is the classification oracle **and** the process is started with `-X int_max_str_digits=0`. It is still not a spec mandate, and it is still not a reason to map CPython `ValueError` to TOML syntax.

Rust adding no decimal-digit Limit is consistent with **that profile**, not with a misread of the 64-bit SHOULD.

## Unqualified

Does not change the 675-case incomplete-radix findings, the 4300/4301 measurements, or the process-profile recommendation. Root leads any candidate text.

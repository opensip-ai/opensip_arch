My verdict is **CHANGES-REQUIRED** for manifest `48089c1e4daa161dd5a18deebcd396514901a290d4ac0ac80a89fd2cbacf8ba3`. I wrote `review.md` and `review.json` in `/tmp/opensip-implementation/m1-ts-runtime-review-01`. The frozen manifest, all 12 file hashes and the directory listing were identical before and after the review. All my writes went under `work/` in that directory.

The JSON parser and canonical encoder look sound. All the frozen checks reproduce: the TypeScript build is clean, the boundary script passes 34 checks, the 14000-input corpus gives 4490 accepted and 9510 refused, and the 11191 shape cases have 0 mismatches. 25 extra malformed inputs I tried were all refused. The shape interpreter also agreed with the Python adapter on everything else I ran:
- **Metadata cases:** my own rerun of the 43 cases matched (metadata-v1 still differs on 2).
- **Ordering:** 2680 cases across all 134 non-`sequence` order nodes, 0 mismatches.
- **Real values:** 2500 values taken from the architecture JSON files, run against all 589 refs. That is 1,472,500 checks, 64,091 of them valid, with 0 mismatches.

**Required findings**
1. **R1 – regex rules differ from the Python reference.** `schema.ts:35` compiles patterns as JavaScript regexes. There, `.` doesn't match `\r`, U+2028 or U+2029, and `$` matches only at the very end; Python treats both differently. On the pinned schemas TS says valid and Python says invalid for:
   - `evidence-schemas:v2#/$defs/CanonicalPath` with `"a\r/../../etc/passwd"` or `"a\u2028/../../x"`, which are parent-directory paths.
   - The same CanonicalPath, plus both `LogicalPath` definitions, with `"..\n"` and `"a/..\n"`.

   The CanonicalPath pattern is used in 34 places. Over the 66 pinned patterns tested with line-break strings, 428 of 68,640 results differ. None of the existing test sets contain line breaks, so none of them catch this. Someone needs to decide which regex rules are normative; then TS, Python and Rust should be made to agree, with a line-break test set kept for every pattern.
2. **R2 – the "inert data" check isn't applied to the value that actually gets checked.** `matches()` validates a copy through `canonical()`, discards it, and then checks the original object. `canonical()` also never checks an array's prototype. I showed three bypasses:
   - An array with a custom `every()` makes `[1n,2n]` pass `items:{type:string}`.
   - An `Array` subclass does the same.
   - A Proxy makes `{a:5n}` pass `{a:string}`.

   Proxy traps also run inside `canonical()`, so it is not side-effect free for Proxies. The fix is to check an owned copy (`parseExact(canonical(value))`), require `Array.prototype`, and either reject Proxies or say they aren't covered.

**Advisories (none block acceptance, none reachable with the current pins)**
- **A1 – ordering errors:** `ordered()` throws `SchemaError` on bad item data where the reference returns invalid, and it accepts some types the reference rejects.
- **A2 – keyword values unchecked:** a non-array `enum` or `required` is silently ignored, and some bad values are coerced.
- **A3 – reference loops:** a loop that never advances into the input is reported as `ShapeLimit`, though it could be caught as a schema error up front.
- **A4 – missing script:** `schema-probe.mjs` uses metadata-v1 and compares nothing, and no frozen script produces `schema-differential-02.json`.
- **A5 – work limit:** the default limit of 1e6 raises `ShapeLimit` on a valid 4 MiB array of about 2M items, and some costs aren't counted as work.
- **A6 – byte input:** input backed by a `SharedArrayBuffer` is accepted; `Uint8Array`s from other realms are refused.

**Limitations**
- The Python adapter was only used for comparison. R1 partly depends on which regex rules are declared normative.
- I didn't run Rust, so I don't know how Rust's regex handles line breaks.
- Only 110 of the 589 refs had any valid test value.
- No fuzzing of the parser and no analysis of regex backtracking.
- I took the 589-entrypoint selection as given.

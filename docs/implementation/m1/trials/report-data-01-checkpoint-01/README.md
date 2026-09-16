# Report data boundary candidate01 — unaccepted

`apps/report/src/report-data.ts` implements the inventoried report payload
reader against the exact generated report-codec checkpoint02. The proposed
product source remains staged here because the final generated source binding
and actual independent review are pending.

The reader uses the generated exact JSON codec and shape validator. It checks
family/major and profile compatibility, then deeply freezes its owned parsed
data before returning it to views. It recomputes no verdict and authenticates no
source custody. Host semantic admission remains required before report delivery;
opening a compatible file provides no independent verification of its assessment.

Failure returns only a fixed code/message. Malformed JSON, document limits,
incompatible version/profile, invalid projection and exhausted validation work
are distinct; unexpected reader failures are unavailable. No raw exception,
partial report, repository path or supplied hostile string is exposed in these
messages. The validation-work exhaustion classification is implemented but this
trial does not inject or construct a corresponding exhaustion witness.

Strict TypeScript compilation passes.32 positive checks include all31 current
complete reference reports and the4,202,744-byte dense report.56 refusal checks
cover malformed/exponent/duplicate/out-of-range/non-scalar JSON, unknown profiles,
byte/depth limits, stale inventory5 provenance, wrong fields and31 envelope-only
inputs. Mutation checks verify the input byte array is not retained and nested
arrays/objects are frozen. The exported report type is shallow Readonly; deep
immutability is enforced at runtime, so views must keep their own filtering state.

A fresh Chrome headless process executes the exact emitted modules: six groups
cover31 current reports, dense decoding/freezing, ownership, lexical refusals,
byte/depth limits and profile failure messages. The page's network URLs are
blocked. The harness supplies CommonJS wrappers through CDP; this does not test
the final file loader, CSP, bundler, DOM views, accessibility, all supported
browsers or release behavior. No screenshot is relevant to this nonvisual reader.

Run the selected pinned compiler with strict ES2022/CommonJS and rootDir
apps/report/src to compiled/, then `node check.cjs` and `node check-browser.mjs`.
The browser checker requires a fresh browser01 directory. Its private disposable
profile is excluded from the checkpoint; no personal Chrome state is used.
Current schema source, raw fixture pins and compiled module hashes are recorded
in input-pins.json, result.json and browser01/result.json. Compiler/toolchain
selection remains owned by the final build/source closure.

Next: actual review and final source selection, embedded-payload loader/error
presentation, report view integration and meaningful full browser qualification.
This is a presentation boundary implementation, not complete report admission,
report delivery or an M4 completion claim.

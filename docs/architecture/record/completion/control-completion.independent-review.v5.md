# Independent control repair review v5

**No objection within repair scope. CCR4-1 is resolved.** External replay reproduces **484/484**, byte-identical to the retained report. All eight subject hashes remain unchanged.

Exact hashes and seven independent probe results are in [the review JSON](control-completion.independent-review.v5.json). Freeze SHA-256: `0e4a020fd8ac53e7328bc8d46e01c9e188caf5ed173f1eb00c2fe38751eb096d`.

The UTF-8 walk now sees original identity/digest strings and substitutes only an invalid sequence. All three original v4 probes return RF-2. Independent hello/helloAck Unicode boundary probes preserve RF-3 at the byte limit and RF-2 above it. Existing compound-fault, sequence, deep-input, future-body and stopped-direction cases remain passing.

No new MUST finding was identified. Schema/state/authority choices are unchanged; external security/journal activation and platform qualification remain separate requirements. This review makes no automatic acceptance/SATISFIED or register disposition. No subject bytes changed.

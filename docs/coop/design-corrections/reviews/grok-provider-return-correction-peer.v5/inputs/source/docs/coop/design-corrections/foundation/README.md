# Codex foundation and identity correction evidence

The consolidated intended design selects the evaluator3 owner below. Codex
and actual Grok authored the successor over inherited Claude-reviewed input
contracts. Current acceptance is governed by the correction record; Claude's
later successor review remains pending credits. These are design reference
instruments, not product implementation or release qualification.

Current evaluator source: `identity-schemas.v3.json`, `identity-model.v3.py`,
`evaluator_input_model.v3.py`, `evaluator_composition_model.v3.py` and the
incorporated enumeration, atom, execution-input, composition and fault
contracts. Public `close_run` recomputes the complete proof and result from
retained inputs. `open_run_closure` performs structural owner admission and
cannot establish semantic validity on its own. The current pinned suite is
`run-evaluator3-checks.py --out <new-report-directory>`. The five retained
foundation checks below continue to check their explicitly narrower subjects.

- `canonical.py`: exact lexical and typed JSON admission plus the product
  canonical serializer and domain-framed hash.
- `host-foundation-model.v2.py`: configuration/policy/parser successor to the
  frozen model; root discovery is owned by the security successor.
- `product-configuration.schema.v2.json`, `product-configuration-model.py`: full
  product configuration, registry-bound native defaults and explicit overrides.
- `g13-result-schema.v5.json`, `g13-validator.v5.py`: authenticated subject and
  independent-oracle join for the historical 24-cell report shape.
- `product-quality-report.schema.v3.json`, `product-quality-validator.py`:
  full-product report shape with actual observations and trusted gate oracles.
- `identity-schemas.v2.json`, `identity-model.py`: closed semantic descriptor
  graph and retention reference for historical profile2; not the selected
  evaluator3 output owner.
- `check-array-orders.py`: explicit collection-law coverage across the current
  identity, configuration, native, security and workflow schemas, with
  discriminating raw-UTF-8/JSON and field-key vectors and native host refusals.

Run the retained checks with Python 3.12 and jsonschema 4.25.1, using `-I -B`:

```
python -I -B check-foundation.py --report foundation-report.json
python -I -B check-identity.py --report identity-report.json
python -I -B check-product-quality.py --report product-quality-report.json
python -I -B check-product-configuration.py --report product-configuration-report.json
python -I -B check-array-orders.py --report array-order-report.json
```

Run from this directory, or supply repository-relative script/report paths.
The first and third checks use OpenSSL with temporary Ed25519 test keys. They
measure signature validation and synthetic report admission, not native
analysis accuracy. Identity checks use a small independent finite-relation
fixture adapter, authenticated-evaluator callback assumption and in-memory
custody states; they do not implement the complete rule language or verify
native OS persistence. The reports disclose those boundaries.

Source pins, substantive independent review, full-product integration and
current standing are recorded by the enclosing D-372 correction package.

Actual Claude review v1 of frozen subject v3 required changes. Subject v4
adds per-field reference restrictions, typed auxiliary admission, proof input
closure, initial-baseline refusal, ProjectId transitions and typed availability/
recovery/restoration cases. Review dispositions and a new independent verdict
are retained outside this unit. To replay without writing into a frozen subject,
pass `--report-dir /tmp/opensip-foundation-review-output` to the launcher.
The interpreter version in reports is deliberate environment provenance; run
with the declared environment to compare exact report bytes.

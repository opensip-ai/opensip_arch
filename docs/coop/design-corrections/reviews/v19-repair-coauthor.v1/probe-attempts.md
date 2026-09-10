# Probe attempts (retained, including failures)

1. FAILED — `python3 -I -B probe_repair_unmet_mapping.v1.py`
   `ModuleNotFoundError: No module named 'jsonschema'` raised from
   `candidate-subject.v18/docs/coop/design-corrections/foundation/canonical.py:4`.
   The default interpreter has neither `jsonschema` nor `referencing`, so the frozen
   `canonical` module could not be imported.

2. FAILED — searched for an interpreter or venv already carrying the pins
   (`python3.11/3.12/3.13`, `/opt/homebrew/bin/python3`, any `venv`/`.venv` under
   /tmp/opensip-design-corrections). None present. Earlier root probe dirs
   (bv6-final-v3-root-probes.v1) avoided the dependency by loading
   `workflows_model.v1.py` directly and never importing `canonical`.

3. FAILED — `timeout` is not available in this shell (`command not found: timeout`).

4. SUCCEEDED — created a LOCAL venv `.probe-venv` inside this working directory only
   (nothing under candidate-subject.v18 was written) and installed `jsonschema` +
   `referencing`. Run: `./.probe-venv/bin/python -B probe_repair_unmet_mapping.v1.py`.

   LIMIT / DISCLOSED DIFFERENCE: this venv resolves Python 3.14 with jsonschema 4.26.0,
   whereas `check_workflows.v1.py` documents Python 3.12 with jsonschema 4.25.1. The
   probe therefore does NOT claim parity with the pinned checker run and does not rerun
   the checker suite. It is used only for (a) direct `repair_preview` calls, which need
   no validator, and (b) two shape-validity observations (S1), which are corroborated
   independently by direct schema inspection: `RepairPlanDescriptor` carries no
   `allOf`/`if`/`dependentSchemas` keyword that could couple `applicable` to
   `unmetPreconditions` (observed keyword set: additionalProperties, description,
   properties, required, type).

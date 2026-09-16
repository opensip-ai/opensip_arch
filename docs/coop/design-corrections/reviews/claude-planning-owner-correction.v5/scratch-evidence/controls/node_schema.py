"""Real schema admission boundary for StoreLineageNodeV1.

The lineage law does not guess member sets, integer-versus-boolean types or
version constants. Callers supply an admission callable; this module builds one
from the companion's own closed schema using the FROZEN foundation
ExactValidator, whose integer type checker is `type(value) is int`, so a JSON
boolean is never admitted as an integer.

Design evidence only.
"""
import importlib.util
import json
from pathlib import Path

CANONICAL = "docs/coop/design-corrections/foundation/canonical.py"
COMPANION = "docs/v2/architecture/store-instance-lineage.v1.json"


def load_frozen_canonical(c25):
    path = Path(c25) / CANONICAL
    spec = importlib.util.spec_from_file_location("frozen_canonical", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def node_schema(work):
    companion = json.loads((Path(work) / COMPANION).read_text())
    return companion["privateCompanionSchema"]["schema"]


def build_node_admission(work, c25):
    """Return (admit_callable, description).

    The callable returns a refusal string or None, so the law has a real
    admission boundary rather than implicit assumptions.
    """
    C = load_frozen_canonical(c25)
    schema = node_schema(work)
    validator = C.ExactValidator(schema)

    def admit(candidate):
        try:
            C.typed(candidate)
        except Exception as exc:                        # exact JSON type discipline
            return "NODE_SCHEMA:typed:" + type(exc).__name__
        errors = sorted(validator.iter_errors(candidate), key=lambda e: list(e.path))
        if errors:
            return "NODE_SCHEMA:" + (errors[0].json_path or "$") + ":" + errors[0].message[:60]
        return None

    return admit, {
        "schemaSource": COMPANION + "#/privateCompanionSchema/schema",
        "schemaId": schema.get("$id"),
        "validator": "frozen " + CANONICAL + " ExactValidator",
        "exactIntegerTypeChecker": True,
        "assumption": "none; node shape is admitted by the real closed schema",
    }

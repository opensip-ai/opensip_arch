"""Reviewer probe: compare Rust outcomes with the pinned architecture reference.

Loads foundation/canonical.py from digest-checked bytes (no bytecode is written in
the architecture tree), recomputes the four product H goldens in
canonical_tests.rs from literal frame bytes using only hashlib, and compares
accept/refuse plus exact canonical bytes for every corpus input. Refusal codes are
not compared. Writes results/reference-differential.json.
"""
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
CANONICAL = ARCH / "docs/coop/design-corrections/foundation/canonical.py"
CANONICAL_SHA256 = "d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442"
GOLDENS = [
    (b"null", "ae2a3ea941d02d406de61b3f9e56481330b15ea42a527e21e0d0e307599dc26c"),
    (b"{}", "a55d7ef6f4e91b65725fa884c13f1be967b90abed1413d479bfabda5cb2a2c8b"),
    (b"[0,-1,-9223372036854775808,18446744073709551615]",
     "1b0ea85a3273cbc41aed75f2d07136b77eec013fca6ea2cb84acce63cf8ccd73"),
    ('{"":0,"\U00010000":1}'.encode("utf-8"),
     "b4208ff8b9f5977285610c23326cc7558565732ea06c5b1728a25ccc0e9105f7"),
]


def load_reference():
    raw = CANONICAL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CANONICAL_SHA256:
        raise SystemExit("pinned reference canonical.py digest mismatch")
    stubbed = False
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        # parse/canonical/identity do not use jsonschema; only the validator does.
        from unittest import mock
        sys.modules["jsonschema"] = mock.MagicMock()
        stubbed = True
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader("reference_canonical", loader=None))
    exec(compile(raw, str(CANONICAL), "exec"), module.__dict__)
    return module, stubbed


def reference_outcome(reference, raw):
    try:
        return "ACCEPT " + reference.canonical(reference.parse(raw)).hex()
    except reference.AdmissionError:
        return "REFUSE"
    except Exception as exc:  # recorded as disagreement, never as agreement
        return "REF-EXCEPTION " + type(exc).__name__


def main():
    reference, stubbed = load_reference()
    goldens = []
    for canonical_bytes, expected in GOLDENS:
        frame = b"opensip.product.v1\x00vector\x00" + len(canonical_bytes).to_bytes(8, "big") + canonical_bytes
        goldens.append({
            "canonical": canonical_bytes.decode("utf-8"),
            "hashlibOverLiteralFrameMatches": hashlib.sha256(frame).hexdigest() == expected,
            "referenceIdentityMatches": reference.identity("vector", reference.parse(canonical_bytes)) == expected,
            "referenceCanonicalFixedPoint": reference.canonical(reference.parse(canonical_bytes)) == canonical_bytes,
        })
    corpus = (HERE / "corpus.hex").read_text().split("\n")[:-1]
    rust_path = RESULTS / "rust-outcomes.txt"
    rust = rust_path.read_text().split("\n")[:-1] if rust_path.exists() else []
    counts = {"ACCEPT": 0, "REFUSE": 0, "OTHER": 0}
    mismatches, growth = [], []
    for line, rust_outcome in zip(corpus, rust):
        raw = bytes.fromhex(line)
        expected = reference_outcome(reference, raw)
        kind = rust_outcome.split(" ", 1)[0]
        counts[kind if kind in counts else "OTHER"] += 1
        agree = (kind == "REFUSE" and expected == "REFUSE") or (kind == "ACCEPT" and rust_outcome == expected)
        if not agree:
            mismatches.append({"inputHex": line[:400], "rust": rust_outcome[:400], "reference": expected[:400]})
        if kind == "ACCEPT" and (len(rust_outcome) - len("ACCEPT ")) // 2 > len(raw):
            growth.append(line[:400])
    result = {
        "python": platform.python_version(),
        "jsonschemaStubbed": stubbed,
        "corpusCases": len(corpus),
        "rustOutcomes": len(rust),
        "rustOutcomeCounts": counts,
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:100],
        "canonicalLongerThanInput": growth[:100],
        "hGoldens": goldens,
    }
    result["passed"] = (
        len(rust) == len(corpus) > 0
        and not mismatches
        and not growth
        and counts["OTHER"] == 0
        and all(all(v for k, v in row.items() if k != "canonical") for row in goldens)
    )
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "reference-differential.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("passed", "corpusCases", "rustOutcomes", "rustOutcomeCounts", "mismatchCount")}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

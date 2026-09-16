"""Targeted adversarial ArrayOrder controls on the private probe."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-array-order-selection-v1-review/review")
EXE = REVIEW / "probes" / "reference-work" / "probe-target" / "debug" / "opensip-array-order-probe"
CENSUS = REVIEW / "probes" / "reference-work" / "selected-order-census.json"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def rust(order, values) -> bool:
    case = {"order": order, "values": values}
    line = json.dumps(case, ensure_ascii=True, separators=(",", ":")) + "\n"
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "TERM": "dumb",
    }
    r = subprocess.run([str(EXE)], input=line.encode(), env=env, capture_output=True, timeout=30)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode()[-400:])
    return r.stdout.strip() == b"1"


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    rows = []

    def expect(name, order, values, ok):
        actual = rust(order, values)
        rows.append({"name": name, "expect": ok, "actual": actual, "pass": actual == ok})

    expect("empty-unknown-annotation", "unregistered", [], False)
    expect("empty-null-annotation", None, [], False)
    expect("empty-extra-by-member", {"by": ["name"], "extra": True}, [], False)
    expect("empty-sequence-ok", "sequence", [], True)
    expect("utf8-lf-before-bang", "utf8", ["\n", "!"], True)
    expect("utf8-bang-before-lf", "utf8", ["!", "\n"], False)
    expect("canonical-bang-before-lf", "canonical-set", ["!", "\n"], True)
    expect("canonical-lf-before-bang", "canonical-set", ["\n", "!"], False)
    expect("numeric-extrema", "numeric", [-(2**63), -1, 0, 2**64 - 1], True)
    expect("numeric-bool-refusal", "numeric", [True], False)
    expect("numeric-reversed", "numeric", [10, 2], False)
    expect("ordinal-contiguous", "ordinal", [{"ordinal": 0}, {"ordinal": 1}], True)
    expect("ordinal-gap", "ordinal", [{"ordinal": 0}, {"ordinal": 2}], False)
    expect("candidate-gap-ok", "candidateOrdinal", [{"candidateOrdinal": 4}, {"candidateOrdinal": 7}], True)
    expect("candidate-duplicate", "candidateOrdinal", [{"candidateOrdinal": 4}, {"candidateOrdinal": 4}], False)
    expect("candidate-negative-sign-not-order-law", "candidateOrdinal", [{"candidateOrdinal": -2}, {"candidateOrdinal": -1}], True)
    expect("sequence-duplicates-kept", "sequence", ["x", "(", ")", "x"], True)
    expect("set-duplicates-refuse", "canonical-set", ["a", "a"], False)
    expect("canonical-order-duplicates-ok", "canonical-order", ["a", "a", "b"], True)
    expect("tuple-ignores-other-keys", {"by": ["name"]}, [{"a": "z", "name": "a"}, {"a": "a", "name": "z"}], True)
    expect("tuple-same-name-different-payload-not-unique", {"by": ["name"]}, [{"name": "a", "payload": 1}, {"name": "a", "payload": 2}], False)
    expect("tuple-declared-order", {"by": ["name", "version"]}, [{"name": "a", "version": "1"}, {"name": "a", "version": "2"}], True)
    expect("tuple-wrong-second-key", {"by": ["name", "version"]}, [{"name": "a", "version": "2"}, {"name": "a", "version": "1"}], False)
    expect("missing-field", {"by": ["n"]}, [{}], False)
    expect("utf8-integer", "utf8", [1], False)
    expect("nfc-nfd-distinct-utf8", "utf8", ["e\u0301", "é"], True)  # NFD < NFC in unicode/utf8
    expect("nfc-nfd-reversed-utf8", "utf8", ["é", "e\u0301"], False)

    census = json.loads(CENSUS.read_bytes())
    selected_ok = []
    for row in census:
        ok = rust(row["order"], [])
        selected_ok.append({"order": row["order"], "emptyArrayParses": ok})
    out = {
        "adversarial": rows,
        "allAdversarialPass": all(r["pass"] for r in rows),
        "failed": [r["name"] for r in rows if not r["pass"]],
        "selectedFormsEmptyArray": selected_ok,
        "allSelectedFormsAdmitEmpty": all(r["emptyArrayParses"] for r in selected_ok),
        "selectedFormCount": len(selected_ok),
    }
    (REVIEW / "results" / "adversarial.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "allAdversarialPass": out["allAdversarialPass"],
        "failed": out["failed"],
        "allSelectedFormsAdmitEmpty": out["allSelectedFormsAdmitEmpty"],
        "selectedFormCount": out["selectedFormCount"],
    }, indent=2))


if __name__ == "__main__":
    main()

"""Adapt selected run-reference.py to the private copy; never the original candidate path."""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-array-order-selection-v1-review/review")
P = REVIEW / "copy" / "frozen-subject" / "product"
B = REVIEW / "probes" / "reference-work"
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
PY_PACKAGES = Path("/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages")
CANON_SHA = "d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442"


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(REVIEW / "probes" / "tmp"),
        "TERM": "dumb",
        "PYTHONPATH": str(PY_PACKAGES),
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return env


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    if B.exists():
        shutil.rmtree(B)
    H = B / "probe"
    (H / "src").mkdir(parents=True)
    sys.path.insert(0, str(PY_PACKAGES))
    reference = ARCH / "docs/coop/design-corrections/foundation/canonical.py"
    raw = reference.read_bytes()
    pin = {
        "path": str(reference.relative_to(ARCH)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    if pin["sha256"] != CANON_SHA:
        raise SystemExit("canonical.py sha mismatch")
    lock = json.loads((P / "design-lock.json").read_bytes())
    subject = json.loads((ARCH / lock["approvals"]["sourceManifest"]["path"]).read_bytes())
    rows = subject.get("files", subject.get("entries", []))
    matches = [r for r in rows if r.get("path") == pin["path"]]
    if not (len(matches) == 1 and matches[0]["sha256"] == pin["sha256"]):
        raise SystemExit("canonical.py not pinned by selected baseline")
    spec = importlib.util.spec_from_file_location("exact_reference", reference)
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    (H / "Cargo.toml").write_text(
        '[workspace]\n[package]\nname="opensip-array-order-probe"\nversion="0.0.0"\nedition="2024"\npublish=false\n[dependencies]\nopensip-identity={path="'
        + str(P / "crates/identity")
        + '"}\n'
    )
    (H / "src/main.rs").write_text(
        Path(ARCH / "docs/implementation/m2/array-order-selection-v1/evidence/probe/src/main.rs").read_text()
    )
    target = B / "probe-target"
    env = env_for(target)
    logs = REVIEW / "results" / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    def run(name, cmd, cwd=P, stdin=None):
        r = subprocess.run(cmd, cwd=cwd, input=stdin, env=env, capture_output=True, timeout=300)
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        if r.returncode != 0:
            raise SystemExit(f"{name} failed {r.returncode}: {r.stderr[-800:]}")
        return r

    run("oracle-build", [CARGO, "build", "--offline", "--manifest-path", str(H / "Cargo.toml")], cwd=H)
    orders = [
        "sequence",
        "utf8",
        "canonical-set",
        "canonical-order",
        "numeric",
        "ordinal",
        "candidateOrdinal",
        "path",
        "ruleId",
        "waiverId",
        "predicate",
        {"by": ["name"]},
        {"by": ["name", "version"]},
        "unregistered",
        None,
        True,
        1,
        [],
        {},
        {"by": []},
        {"by": [""]},
        {"by": ["name", "name"]},
        {"by": ["name"], "extra": True},
        {"by": "name"},
        {"by": [1]},
    ]
    annotations = {}

    def walk(v, source, path=""):
        if isinstance(v, dict):
            if "x-opensip-order" in v:
                order = v["x-opensip-order"]
                key = json.dumps(order, sort_keys=True)
                annotations.setdefault(key, {"order": order, "occurrences": []})["occurrences"].append(
                    {"source": source, "pointer": path}
                )
            for k, x in v.items():
                walk(x, source, path + "/" + k)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, source, path + "/" + str(i))

    for p in sorted((P / "schemas/sources").glob("*.json")):
        walk(json.loads(p.read_bytes()), str(p.relative_to(P)))
    orders += [v["order"] for v in annotations.values()]
    (B / "selected-order-census.json").write_text(json.dumps(list(annotations.values()), indent=2) + "\n")
    values = []
    scalar = [None, False, True, -(2**63), -1, 0, 1, 2, 10, 2**53, 2**53 + 1, 2**64 - 1, "", "\n", "!", "a", "é", "e\u0301", "😀"]
    values.extend(list(xs) for n in range(3) for xs in itertools.product(scalar, repeat=n))
    records = [
        {},
        {"name": "a"},
        {"name": "a", "payload": 1},
        {"name": "a", "payload": 2},
        {"name": "b"},
        {"name": 1},
        {"name": "a", "version": "1"},
        {"name": "a", "version": "2"},
        {"path": "a"},
        {"path": "b"},
        {"ruleId": "a"},
        {"waiverId": "a"},
        {"ruleId": "r", "subjectId": "s", "predicateId": "a"},
        {"ruleId": "r", "subjectId": "s", "predicateId": "b"},
    ]
    for field in ["ordinal", "candidateOrdinal"]:
        records += [{field: n} for n in [-2, -1, 0, 1, 2, 4, 7, 2**53, 2**53 + 1, 2**64 - 1, True, "0"]]
    values.extend(list(xs) for n in range(1, 3) for xs in itertools.product(records, repeat=n))
    rng = random.Random(20260915)
    values += [rng.choices(scalar + records, k=rng.randrange(3, 8)) for _ in range(100)]
    cases = [{"order": order, "values": value} for order in orders for value in values]
    expected = []
    for case in cases:
        C.typed(case["values"])
        expected.append(not list(C.exact_order(None, case["order"], case["values"], {})))
    inputs = "".join(json.dumps(c, ensure_ascii=True, separators=(",", ":")) + "\n" for c in cases).encode()
    (B / "oracle-input.jsonl").write_bytes(inputs)
    exe = target / "debug" / "opensip-array-order-probe"
    r = run("oracle", [str(exe)], cwd=H, stdin=inputs)
    actual = [line == b"1" for line in r.stdout.splitlines()]
    if len(actual) != len(expected):
        raise SystemExit(f"row count {len(actual)} != {len(expected)}")
    mismatches = [
        {"case": case, "reference": e, "rust": a}
        for case, e, a in zip(cases, expected, actual)
        if e != a
    ]
    result = {
        "standing": "Independent exact_order comparison on private copy; not whole schema or replay",
        "reference": pin,
        "selectedSchemaAnnotationForms": len(annotations),
        "selectedSchemaAnnotationOccurrences": sum(len(a["occurrences"]) for a in annotations.values()),
        "cases": len(cases),
        "mismatchCount": len(mismatches),
        "mismatches": mismatches[:8],
        "executedAgainstOriginalCandidate": False,
        "privateProduct": str(P),
        "noInputMutation": True,
    }
    (REVIEW / "results" / "oracle-result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "cases": len(cases),
        "forms": len(annotations),
        "occurrences": result["selectedSchemaAnnotationOccurrences"],
        "mismatchCount": len(mismatches),
        "sample": mismatches[:3],
        "canonicalSha": pin["sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()

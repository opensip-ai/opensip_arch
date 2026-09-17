#!/usr/bin/env python3
"""Private semantic classification probe. Does not edit the trial or product."""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

PY = Path("/tmp/opensip-implementation/native-case15-reference-env/bin/python")
T = Path("/tmp/opensip-implementation")
WORK = T / "m2-grok-toml-semantics-38"
PROBE = WORK / "bin/opensip-package-probe"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
FOUNDATION = (
    T
    / "m2-full-walk-subject-32/reference/archroot/docs/coop/design-corrections/foundation/enumeration_model.v1.py"
)
SELECTED = (
    ARCH
    / "docs/implementation/m2/enumeration-totality-reference-selection-v1/reference/enumeration_model.v1.py"
)
TOML_TEST = WORK / "corpus/toml-test-1.6.0/tests"

assert hashlib.sha256(FOUNDATION.read_bytes()).hexdigest() == "69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85"
assert hashlib.sha256(SELECTED.read_bytes()).hexdigest() == "689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072"
assert hashlib.sha256(PROBE.read_bytes()).hexdigest() == "73508e9aa4c2fae5ce1a987ca27ceae3d48c41fd5f15cd794eee0748bf762009"

sp = importlib.util.spec_from_file_location("enum_packages38", FOUNDATION)
E = importlib.util.module_from_spec(sp)
sp.loader.exec_module(E)
fn = next(
    n
    for n in ast.parse(SELECTED.read_bytes()).body
    if isinstance(n, ast.FunctionDef) and n.name == "project_named_packages"
)
exec(compile(ast.Module(body=[fn], type_ignores=[]), "selected-enumeration-totality37", "exec"), E.__dict__)

cases: list[dict] = []


def add(label: str, blob: bytes) -> None:
    blobs = {"Cargo.toml": blob}
    paths = ["Cargo.toml"]
    membership = E.NV.assign_membership([], paths)
    scope = {"workspaceRoots": ["."], "pathPrefixes": ["."], "excludedPathPrefixes": []}
    idx = {
        "Cargo.toml": {
            "path": "Cargo.toml",
            "sha256": hashlib.sha256(blob).hexdigest(),
            "bytes": len(blob),
        }
    }
    inp = {
        "snapshotPaths": paths,
        "scope": scope,
        "workspaceRoot": ".",
        "membership": membership,
        "blobs": {"Cargo.toml": blob.hex()},
        "index": idx,
    }
    faults: list = []
    value = E.project_named_packages(
        inp["snapshotPaths"],
        inp["scope"],
        inp["workspaceRoot"],
        inp["membership"],
        {"Cargo.toml": blob},
        faults,
        inp["index"],
    )
    cases.append(
        {
            "label": label,
            "hex": blob.hex(),
            "input": inp,
            "reference": {"result": "projected", "value": value, "refusals": faults},
        }
    )


def named(body: bytes) -> bytes:
    return b'[package]\nname="p"\n' + body


BOM = b"\xef\xbb\xbf"

# --- BOM anywhere / quoted strings ---
add("bom-leading", BOM + b'[package]\nname="p"\n')
add("bom-leading-crlf", BOM + b'[package]\r\nname="p"\r\n')
add("bom-double-leading", BOM + BOM + b'[package]\nname="p"\n')
add("bom-after-space", b" " + BOM + b'[package]\nname="p"\n')
add("bom-after-tab", b"\t" + BOM + b'[package]\nname="p"\n')
add("bom-after-lf", b"\n" + BOM + b'[package]\nname="p"\n')
add("bom-after-crlf", b"\r\n" + BOM + b'[package]\nname="p"\n')
add("bom-before-name-key", b"[package]\n" + BOM + b'name="p"\n')
add("bom-between-keys", named(b"x=1\n")[:-1] + BOM + b"\ny=2\n")
add("bom-eof", named(b"") + BOM)
add("bom-comment", named(b"#") + BOM + b" comment\n")
add("bom-in-basic-string", b'[package]\nname="' + BOM + b'p"\n')
add("bom-in-literal-string", b"[package]\nname='" + BOM + b"p'\n")
add("bom-in-multiline-basic", b'[package]\nname="""' + BOM + b'p"""\n')
add("bom-in-multiline-literal", b"[package]\nname='''" + BOM + b"p'''\n")
add("bom-unicode-escape-name", b'[package]\nname="\\uFEFFp"\n')
add("bom-quoted-key", named(b'"') + BOM + b'k"="v"\n')
add("bom-bare-key", named(BOM + b'k=1\n'))
add("utf16le-bom", b"\xff\xfe[\x00p\x00]")
add("utf16be-bom", b"\xfe\xff\x00[\x00p")

# --- LF / CRLF / multiline escapes ---
add("lf-only", b'[package]\nname="p"\n')
add("crlf-only", b'[package]\r\nname="p"\r\n')
add("mixed-lf-crlf", b'[package]\nname="p"\r\nx=1\n')
add("bare-cr-newline", b'[package]\rname="p"\r')
add("trailing-bare-cr", named(b"x=1") + b"\r")
add("cr-in-comment", named(b"# hi\rthere\nx=1\n"))
add("multiline-basic-lf", b'[package]\nname="""\np"""\n')
add("multiline-basic-crlf", b'[package]\r\nname="""\r\np"""\r\n')
add("multiline-first-newline-trim", b'[package]\nname="""\np\n"""\n')
add("multiline-backslash-lf", b'[package]\nname="""p\\\nq"""\n')
add("multiline-backslash-crlf", b'[package]\nname="""p\\\r\nq"""\n')
add("multiline-backslash-cr", b'[package]\nname="""p\\\rq"""\n')
add("multiline-literal-crlf", b"[package]\r\nname='''\r\np'''\r\n")
add("escaped-cr-in-basic", b'[package]\nname="p\\rq"\n')
add("raw-cr-in-basic", b'[package]\nname="p\rq"\n')
add("escaped-newline-in-basic", b'[package]\nname="p\\nq"\n')

# --- duplicate / dotted / array tables ---
add("dup-key-in-package", named(b'name="q"\n'))
add("dup-package-table", named(b"[package]\n"))
add("dup-std-table", named(b"[a]\nx=1\n[a]\ny=2\n"))
add("subtable-then-parent", named(b"[a.b]\nx=1\n[a]\ny=2\n"))
add("parent-then-subtable", named(b"[a]\ny=2\n[a.b]\nx=1\n"))
add("dotted-then-header", b'package.name="p"\n[package]\nversion="1"\n')
add("header-then-dotted", named(b'version="1"\npackage.edition="2021"\n'))
add("inline-then-header", b'package={name="p"}\n[package]\n')
add("header-then-inline", named(b'package={x=1}\n'))
add("array-of-package", b'[[package]]\nname="p"\n')
add("header-then-aot-package", named(b"[[package]]\n"))
add("aot-then-aot", named(b"[[arr]]\nx=1\n[[arr]]\nx=2\n"))
add("aot-then-table", named(b"[[arr]]\nx=1\n[arr]\n"))
add("table-then-aot", named(b"[arr]\nx=1\n[[arr]]\n"))
add("dotted-into-aot", named(b"[[arr]]\n[arr.sub]\nx=1\n"))
add("implicit-dotted-super", named(b"a.b.c=1\n[a]\nd=2\n"))
add("quoted-vs-bare-dup", named(b'x=1\n"x"=2\n'))
add("case-sensitive-keys", named(b"X=1\nx=2\n"))
add("dotted-package-only", b'package.name="p"\n')
add("inline-package-only", b'package={name="p",version="1"}\n')
add("quoted-dotted-package", b'"package"."name"="p"\n')
add("package-metadata-only-header", b'[package.metadata]\nx=1\n')

# --- datetime / number / unicode ---
add("date-leap-2024", named(b"x=2024-02-29\n"))
add("date-nonleap-2023", named(b"x=2023-02-29\n"))
add("date-year-0000", named(b"x=0000-01-01\n"))
add("date-year-0001", named(b"x=0001-01-01\n"))
add("time-leap-second", named(b"x=23:59:60\n"))
add("time-24", named(b"x=24:00:00\n"))
add("odt-space", named(b"x=1979-05-27 07:32:00Z\n"))
add("odt-t-lower", named(b"x=1979-05-27t07:32:00z\n"))
add("odt-offset-plus", named(b"x=1979-05-27T00:32:00-07:00\n"))
add("odt-offset-neg-zero", named(b"x=1979-05-27T07:32:00-00:00\n"))
add("odt-no-seconds", named(b"x=1979-05-27T07:32Z\n"))
add("local-time-no-seconds", named(b"x=07:32\n"))
add("frac-seconds", named(b"x=00:00:00.123456789\n"))
add("int-underscores", named(b"x=1_000\n"))
add("int-hex", named(b"x=0xDEAD_BEEF\n"))
add("int-oct", named(b"x=0o755\n"))
add("int-bin", named(b"x=0b1010\n"))
add("int-leading-plus", named(b"x=+1\n"))
add("int-leading-zero", named(b"x=01\n"))
add("float-leading-dot", named(b"x=.1\n"))
add("float-trailing-dot", named(b"x=1.\n"))
add("float-inf", named(b"x=inf\n"))
add("float-nan", named(b"x=nan\n"))
add("float-1e9999", named(b"x=1e9999\n"))
add("huge-int", named(b"x=18446744073709551616\n"))
add("name-nfc-e", '[package]\nname="é"\n'.encode())
add("name-nfd-e", b'[package]\nname="e\xcc\x81"\n')
add("name-u0041", b'[package]\nname="\\u0041"\n')
add("name-U00000041", b'[package]\nname="\\U00000041"\n')
add("name-null-escape", b'[package]\nname="\\u0000"\n')
add("name-unescaped-soh", b'[package]\nname="\x01"\n')
add("name-emoji", '[package]\nname="🦀"\n'.encode())
add("bare-unicode-key", named("ü=1\n".encode()))
add("quoted-unicode-key", named('"ü"=1\n'.encode()))
add("comment-unicode", named("# café\n".encode()))
add("invalid-utf8-in-string", b'[package]\nname="p"\nx="\xff"\n')
add("surrogate-escape", b'[package]\nname="\\uD800"\n')

# --- TOML 1.0 vs 1.1 ---
add("v11-inline-trailing-comma", b'package={name="p",}\n')
add("v11-inline-newline", b'package={\nname="p"\n}\n')
add("v11-escape-e", b'[package]\nname="\\e"\n')
add("v11-hex-escape", b'[package]\nname="\\x41"\n')
add("v10-array-trailing-comma", named(b"x=[1,2,]\n"))
add("v10-inline-no-trailing", b'package={name="p"}\n')

# Prefix 1.0-invalid / 1.1-valid official files after a named package.
v11_as_10_invalid = [
    "invalid/datetime/no-secs.toml",
    "invalid/inline-table/linebreak-1.toml",
    "invalid/inline-table/linebreak-2.toml",
    "invalid/inline-table/linebreak-3.toml",
    "invalid/inline-table/linebreak-4.toml",
    "invalid/inline-table/trailing-comma.toml",
    "invalid/local-datetime/no-secs.toml",
    "invalid/local-time/no-secs.toml",
    "invalid/string/basic-byte-escapes.toml",
]
for rel in v11_as_10_invalid:
    raw = (TOML_TEST / rel).read_bytes()
    add("v11-poison-" + rel.replace("/", "__"), named(raw) if not raw.startswith(b"[package]") else raw)
    add("v11-whole-" + rel.replace("/", "__"), raw)

# Official toml-test 1.0 .toml files as whole Cargo.toml documents.
listed = [
    line.strip()
    for line in (TOML_TEST / "files-toml-1.0.0").read_text().splitlines()
    if line.strip().endswith(".toml")
]
for rel in listed:
    path = TOML_TEST / rel
    add("tomltest10-" + rel.replace("/", "__"), path.read_bytes())

wire = "".join(json.dumps(c["input"], separators=(",", ":")) + "\n" for c in cases).encode()
proc = subprocess.run([str(PROBE)], input=wire, capture_output=True, timeout=180)
actual_lines = proc.stdout.splitlines()
(WORK / "probes/probe.stderr").write_bytes(proc.stderr)
assert proc.returncode == 0, (proc.returncode, proc.stderr[-3000:])
assert len(actual_lines) == len(cases), (len(actual_lines), len(cases))

mismatches = []
for case, line in zip(cases, actual_lines):
    actual = json.loads(line)
    case["actual"] = actual
    if case["reference"] != actual:
        mismatches.append(
            {
                "label": case["label"],
                "hex": case["hex"],
                "reference": case["reference"],
                "actual": actual,
            }
        )

summary = {
    "standing": "Private semantic classification probe; not source/dependency acceptance",
    "cases": len(cases),
    "mismatches": len(mismatches),
    "probeSha256": hashlib.sha256(PROBE.read_bytes()).hexdigest(),
    "selectedEnumerationSha256": "689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072",
    "tomlTest": "toml-lang/toml-test v1.6.0",
    "mismatchLabels": [m["label"] for m in mismatches],
}
(WORK / "probes/semantics-result.json").write_text(json.dumps({"summary": summary, "mismatches": mismatches}, indent=2) + "\n")
(WORK / "probes/semantics-cases-labels.json").write_text(json.dumps([c["label"] for c in cases], indent=2) + "\n")
print(json.dumps(summary, indent=2))

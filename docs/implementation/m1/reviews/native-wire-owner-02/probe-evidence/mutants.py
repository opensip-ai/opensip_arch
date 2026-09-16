"""Reviewer mutants: semantic edits to the carrier input; report which checks (if any) catch them."""
import json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "copy"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def rule(d, rid):
    return next(r for r in d["admission"] if r["id"] == rid)


def m_prep_detail(d): rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["refusal"]["detail"] = "native.totally-unregistered-detail"
def m_depsrc_detail(d): rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"]["refusal"]["detail"] = "native.totally-unregistered-detail"
def m_depsrc_class(d): rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"]["refusal"].update({"class": "operational-failed", "exitCode": "4", "code": "SYSTEM.OUTCOME.ILLEGAL_STATE"})
def m_prep_when(d): rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["refusal"]["when"] = "after spawn, at worker admission"
def m_hello_first_off(d): rule(d, "RUST3-PROVIDER-FAULT")["params"]["readHelloFirst"] = False
def m_space_allowed(d): rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"]["forbidInNameVersionAtOrBelow"] = "31"
def m_keylen(d): rule(d, "DEPSRC-SET-KEY-CONSTRAINTS")["params"]["maxKeyScalars"] = "4610"
def m_drop_chunk_path(d):
    r = rule(d, "CANONICAL-PATH-ADMISSION"); r["rule"] = r["rule"].replace(", DependencySourceChunkV3.path", "")
def m_lexical_text_drive(d):
    lr = d["privateRepresentation"]["lexicalRules"]; lr["canonical-path-segments"] = lr["canonical-path-segments"].replace("; first segment does not start with [A-Za-z]:", "")
def m_dialect_s(d): d["privateRepresentation"]["patternDialect"]["dialect"] = d["privateRepresentation"]["patternDialect"]["dialect"].replace("WITHOUT the `s` flag", "WITH the `s` flag")
def m_lowering_scalars_only(d): d["privateRepresentation"]["patternDialect"]["loweringRequired"] = "only scalars named Rust3*"
def m_depsrc_order(d): rule(d, "DEPSRC-CUSTODY")["params"]["entryOrder"] = ["name", "version", "path", "sourceId"]
def m_prep_ordinal(d): rule(d, "PREPARED-V3-WIRE-LIMIT")["params"]["maxOrdinal"] = "256"


MUTANTS = {k: v for k, v in globals().items() if k.startswith("m_")}
out = {}
for name, fn in MUTANTS.items():
    dst = HERE / "mut" / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("tmp", "check-result.json", "selftest-result.json"))
    p = dst / "wire-carriers.v1.json"
    d = json.loads(p.read_text())
    fn(d)
    p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", ""), "OPENSIP_ARCH": "/Users/sb/code/opensip-ai/opensip_arch",
           "TMPDIR": str(dst / "tmp"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(dst / "tmp" / "pycache")}
    (dst / "tmp").mkdir(exist_ok=True)
    subprocess.run([PY, "-I", "-B", "check.py", "--out", str(dst / "tmp" / "r.json")], cwd=dst, env=env, capture_output=True, text=True, timeout=600)
    r = json.loads((dst / "tmp" / "r.json").read_text())
    fails = sorted({f["id"] for f in r["failures"]} - {"vectors-cover-every-rule"} | ({"vectors-cover-every-rule"} & {f["id"] for f in r["failures"]}))
    out[name] = {"failed": r["failed"], "ids": fails[:12]}
    shutil.rmtree(dst)
print(json.dumps(out, indent=1))

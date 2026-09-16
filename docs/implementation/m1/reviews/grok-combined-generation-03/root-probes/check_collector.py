"""Independent collector / root-identity counterexamples. Fresh temp dirs only."""
from pathlib import Path
import importlib.util
import json
import os
import shutil
import tempfile

COPY = Path("/tmp/opensip-implementation/m1-root-generator03-reproduction/copy")
OUT = Path("/tmp/opensip-implementation/m1-root-generator03-reproduction/results")
spec = importlib.util.spec_from_file_location("collector", COPY / "tools/collect_generated.py")
col = importlib.util.module_from_spec(spec)
spec.loader.exec_module(col)
rows = []


def check(name, passed, detail=""):
    rows.append({"name": name, "passed": bool(passed), "detail": detail})
    print(("PASS" if passed else "FAIL"), name, detail)


work = Path(tempfile.mkdtemp(prefix="opensip-collector-"))
try:
    root = work / "out"
    root.mkdir()
    (root / "a.rs").write_bytes(b"ok\n")
    got = col.collect_outputs(root, {"a.rs"})
    check("declared-regular-file", got == {"a.rs": b"ok\n"})

    (root / "extra.rs").write_bytes(b"nope")
    try:
        col.collect_outputs(root, {"a.rs"})
        check("extra-file-refused", False)
    except col.GenerationError as e:
        check("extra-file-refused", "undeclared" in str(e).lower() or "different" in str(e).lower(), str(e))
    (root / "extra.rs").unlink()

    os.symlink("a.rs", root / "link.rs")
    try:
        col.collect_outputs(root, {"a.rs", "link.rs"})
        check("symlink-output-refused", False)
    except col.GenerationError as e:
        check("symlink-output-refused", True, str(e))
    (root / "link.rs").unlink()

    nested = work / "nested"
    nested.mkdir()
    (nested / "crates").mkdir()
    (nested / "crates/contracts").mkdir()
    (nested / "crates/contracts/src").mkdir()
    gen = nested / "crates/contracts/src/generated"
    gen.mkdir()
    (gen / "mod.rs").write_bytes(b"pub mod x;\n")
    got = col.collect_outputs(nested, {"crates/contracts/src/generated/mod.rs"})
    check("nested-declared-path", list(got) == ["crates/contracts/src/generated/mod.rs"])

    ident = col.directory_identity(root)
    col.verify_directory_roots({root: ident})
    check("root-identity-stable", True)

    replaced = work / "replaced"
    replaced.mkdir()
    ident2 = col.directory_identity(replaced)
    replaced.rmdir()
    os.symlink(root, replaced)
    try:
        col.verify_directory_roots({replaced: ident2})
        check("replaced-root-symlink-refused", False)
    except col.GenerationError as e:
        check("replaced-root-symlink-refused", "no longer a parent-created directory" in str(e) or "replaced" in str(e), str(e))

    missing = work / "missing"
    missing.mkdir()
    try:
        col.collect_outputs(missing, {"nope.rs"})
        check("missing-declared-refused", False)
    except col.GenerationError as e:
        check("missing-declared-refused", True, str(e))

    # byte limit
    big = work / "big"
    big.mkdir()
    (big / "a.rs").write_bytes(b"x" * 50)
    try:
        col.collect_outputs(big, {"a.rs"}, max_bytes=10)
        check("output-byte-limit-refused", False)
    except col.GenerationError as e:
        check("output-byte-limit-refused", "byte limit" in str(e), str(e))
finally:
    shutil.rmtree(work, ignore_errors=True)

failed = [r["name"] for r in rows if not r["passed"]]
(OUT / "collector-independent.json").write_text(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}, indent=2) + "\n")
print(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed}))
if failed:
    raise SystemExit(1)

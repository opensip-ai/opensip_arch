"""Run one source43.v1 final phase-3 script, unchanged, with its source43.v1 final helpers against the source44 kit.

Usage: python3 tools/seq.py s44-original tools/run_preserved_s43.py <script-stem>
  <script-stem> is phase3_payload_vectors or phase3_traces.

Imports resolve as follows:
  - factbatch, protocol3: preserved/s43-final/ref;
  - payload_fixtures and the script itself: preserved/s43-final/vectors;
  - every other ref/tools module: the current runtime (unchanged by source44 apart from the runtime-root rebind).
The modules are pre-registered in sys.modules before the script runs, so its own sys.path.insert of ref/ cannot substitute the source44 helpers.
Writes through status.dump are redirected to preserved/s44-original/<rel>, so current outputs are never overwritten. The exit status is the script's.
"""
import importlib.util
import os
import runpy
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/"
PRE = OUT + "preserved/s43-final/"
DEST = OUT + "preserved/s44-original/"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main(stem):
    assert stem in ("phase3_payload_vectors", "phase3_traces"), stem
    sys.path.insert(0, OUT + "tools")
    sys.path.insert(0, OUT + "ref")
    import status
    original_dump = status.dump

    def redirected(rel, obj):
        p = DEST + rel
        os.makedirs(os.path.dirname(p), exist_ok=True)
        import json
        with open(p, "w") as fh:
            json.dump(obj, fh, indent=1, ensure_ascii=False)
        print(f"[run_preserved_s43] status.dump({rel!r}) -> {os.path.relpath(p, OUT)}")

    status.dump = redirected
    fb = load("factbatch", PRE + "ref/factbatch.py")
    p3 = load("protocol3", PRE + "ref/protocol3.py")
    pf = load("payload_fixtures", PRE + "vectors/payload_fixtures.py")
    print("[run_preserved_s43] modules:", {m.__name__: os.path.relpath(m.__file__, OUT) for m in (fb, p3, pf)}, "status.dump original:", original_dump.__module__)
    try:
        runpy.run_path(PRE + f"vectors/{stem}.py", run_name="__main__")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
        print(f"[run_preserved_s43] {stem} exit {code}")
        return code
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

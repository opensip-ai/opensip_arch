"""Run one source44.v1 final phase-3 script with the source44 helper logic against the source45 kit.

Usage: python3 tools/seq.py s45-original tools/run_unchanged_s44.py <script-stem>
  <script-stem> is phase3_payload_vectors, phase3_startup_vectors or phase3_traces.

The helpers and the script are the current runtime files, which at this point differ from preserved/s44-final/ only by the runtime-root rebind
(rebind-s45-manifest.json records every before/after sha256). The shim checks that claim before running: for every ref/ and vectors/ file it imports,
the current bytes with the source45 root mapped back to the source44 root must equal preserved/s44-final/manifest.json. Writes through status.dump are
redirected to preserved/s45-original/<rel>, so current outputs are never overwritten. The exit status is the script's.
"""
import hashlib
import json
import os
import runpy
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
DEST = OUT + "preserved/s45-original/"
NEW, OLD = b"consumer-b.v24-source45.v1", b"consumer-b.v24-source44.v1"
CHECK = ["ref/factbatch.py", "ref/protocol3.py", "ref/protocol_ts2.py", "ref/provider_wire.py", "ref/provider_exchange.py", "ref/wirecbor.py",
         "vectors/payload_fixtures.py", "vectors/phase3_payload_vectors.py", "vectors/phase3_startup_vectors.py", "vectors/phase3_traces.py"]


def main(stem):
    assert stem in ("phase3_payload_vectors", "phase3_startup_vectors", "phase3_traces"), stem
    s44 = {r["path"]: r["sha256"] for r in json.load(open(OUT + "preserved/s44-final/manifest.json"))["files"]}
    mismatch = [p for p in CHECK if hashlib.sha256(open(OUT + p, "rb").read().replace(NEW, OLD)).hexdigest() != s44[p]]
    print("[run_unchanged_s44] helper logic equals source44 final (root mapped back):", not mismatch, mismatch)
    if mismatch:
        return 2
    sys.path.insert(0, OUT + "tools")
    sys.path.insert(0, OUT + "ref")
    import status

    def redirected(rel, obj):
        p = DEST + rel
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            json.dump(obj, fh, indent=1, ensure_ascii=False)
        print(f"[run_unchanged_s44] status.dump({rel!r}) -> {os.path.relpath(p, OUT)}")

    status.dump = redirected
    try:
        runpy.run_path(OUT + f"vectors/{stem}.py", run_name="__main__")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
        print(f"[run_unchanged_s44] {stem} exit {code}")
        return code
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

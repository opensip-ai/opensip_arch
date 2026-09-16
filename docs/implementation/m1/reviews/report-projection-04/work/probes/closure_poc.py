"""Reviewer closure PoCs against the frozen enforcement code (review-04). Imports check.py from the probe copy, prepares forged artefacts
BEFORE the hook, then installs the subject's Closure hook and fresh-source loader and attempts hidden loads/writes. Results go to stdout only."""
import importlib.machinery, importlib.util, json, marshal, os, struct, subprocess, sys
from pathlib import Path
W = Path("/tmp/opensip-implementation/m1-report-projection-review-04/work")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
spec = importlib.util.spec_from_file_location("chk", W / "probe-copy/check.py")
chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
res = {}
canonical_src = str(ARCH / "docs/coop/design-corrections/foundation/canonical.py")
st = os.stat(canonical_src)
prefix = str(W / "poc/prefix")
def header():
    return importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF)
forged = compile('FORGED = "stale-bytecode-executed"\n', canonical_src, "exec")
saved = sys.pycache_prefix
sys.pycache_prefix = prefix
cache = importlib.util.cache_from_source(canonical_src)
os.makedirs(os.path.dirname(cache), exist_ok=True)
Path(cache).write_bytes(header() + marshal.dumps(forged))
# control (before hook): stock loader with header-valid forged cache for the real pinned canonical.py
stock = {}
exec(chk.ORIGINAL_GET_CODE(importlib.machinery.SourceFileLoader("stock_canonical", canonical_src), "stock_canonical"), stock)
res["P1-control-stock-loader-real-pinned-canonical"] = stock.get("FORGED", "verified-source")
copy_src = W / "poc/canonical_copy.py"
copy_src.write_bytes(Path(canonical_src).read_bytes())
bc_only = W / "poc/bconly.pyc"
bc_only.write_bytes(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, 0, 0) + marshal.dumps(compile('X = 1\n', str(bc_only), "exec")))
out_path = W / "probes/closure_poc_declared_out.json"
closure = chk.Closure(ARCH, trace=False, out=out_path)
closure.verify_pins(json.loads((W / "probe-copy/source-pins.json").read_bytes()))
sys.addaudithook(closure.hook)
chk.install_fresh_source_loader(closure)
def attempt(name, fn):
    try:
        res[name] = {"outcome": "allowed", "value": fn()}
    except BaseException as exc:
        res[name] = {"outcome": "refused", "error": type(exc).__name__ + ": " + str(exc)[:160]}
def load_enforced(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return {"FORGED": getattr(m, "FORGED", None), "hasCanonical": hasattr(m, "canonical")}
attempt("P1-enforced-loader-same-forged-cache", lambda: load_enforced(canonical_src, "enf_canonical"))
attempt("P1b-stock-loader-after-hook", lambda: (lambda d: (exec(chk.ORIGINAL_GET_CODE(importlib.machinery.SourceFileLoader("stock2", canonical_src), "stock2"), d), d.get("FORGED", "verified-source"))[1])({}))
attempt("P2-unpinned-governed-source-copy", lambda: load_enforced(str(copy_src), "copy_canonical"))
attempt("P3-bytecode-only-governed-module", lambda: (lambda s: (s.loader.exec_module(importlib.util.module_from_spec(s)), "loaded")[1])(importlib.util.spec_from_loader("bconly", importlib.machinery.SourcelessFileLoader("bconly", str(bc_only)))))
attempt("P4-undeclared-governed-write", lambda: open(W / "poc/undeclared.txt", "w").close())
attempt("P5a-declared-out-write", lambda: (open(out_path, "w").write("{}"), "written")[1])
attempt("P5b-declared-out-read", lambda: open(out_path, "r").read())
attempt("P6a-subprocess", lambda: subprocess.run(["/usr/bin/true"]).returncode)
attempt("P6b-os-system", lambda: os.system("true"))
attempt("P6c-fork", lambda: os.fork() if False else (_ for _ in ()).throw(RuntimeError("not attempted: fork would duplicate the test process")))
pinned_path = canonical_src
real_pin = dict(closure.pinned[pinned_path])
closure.pinned[pinned_path] = dict(real_pin, sha256="0" * 64)
attempt("P7-simulated-pin-drift-at-open", lambda: len(open(pinned_path, "rb").read()))
closure.pinned[pinned_path] = real_pin
listing = str(ARCH / "docs/implementation/m1/metadata-v2")
real_listing = closure.listings[listing]
closure.listings[listing] = "0" * 64
attempt("P8-simulated-listing-drift-at-listing", lambda: len(os.listdir(listing)))
closure.listings[listing] = real_listing
alias = "/Users/sb/code/opensip-ai/OPENSIP_ARCH/docs/implementation/README.md"
attempt("P9-case-variant-alias-read-of-unpinned-arch-file", lambda: {"bytes": len(open(alias, "rb").read()), "aliasExists": os.path.exists(alias)})
attempt("P9-control-canonical-path-read-of-same-unpinned-file", lambda: len(open(str(ARCH / "docs/implementation/README.md"), "rb").read()))
attempt("P10-dotdot-path-read-of-unpinned-file", lambda: len(open(str(ARCH / "docs/implementation/m1/../README.md"), "rb").read()))
res["counts"] = closure.counts
sys.pycache_prefix = saved
sys.stdout.write(json.dumps(res, indent=1) + "\n")

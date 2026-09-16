"""Demonstrates that a -I -B child loading a hash-verified source via spec_from_file_location (as check_metadata.py loads canonical.py)
executes an adjacent __pycache__ bytecode whose header matches source mtime/size, not the verified source bytes."""
import hashlib, importlib.util, os, sys, struct, marshal
d = sys.argv[1]
src = os.path.join(d, "mod.py")
raw = open(src, "rb").read()
digest = hashlib.sha256(raw).hexdigest()
st = os.stat(src)
forged = compile('VALUE = "stale-bytecode"\n', src, "exec")
pyc = importlib.util.cache_from_source(src)
os.makedirs(os.path.dirname(pyc), exist_ok=True)
with open(pyc, "wb") as f:
    f.write(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF) + marshal.dumps(forged))
assert hashlib.sha256(open(src, "rb").read()).hexdigest() == digest  # the source pin still verifies
spec = importlib.util.spec_from_file_location("demo_reference", src)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print({"sourceSha256Verified": True, "dontWriteBytecode": sys.dont_write_bytecode, "pycachePrefix": sys.pycache_prefix, "executedValue": module.VALUE})

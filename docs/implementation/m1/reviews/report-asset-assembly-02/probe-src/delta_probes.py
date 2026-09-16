"""Resumed delta review02: probes of the candidate02 behaviour changes. Review copy only.

Run: python -I -B -X pycache_prefix=<empty> delta_probes.py TOOL RESULTS_JSON
The tool is compiled from its verified bytes; nothing is imported from the subject.
"""
import errno
import json
import os
import sys
import tempfile
import time
import types
from pathlib import Path
from unittest.mock import patch

TOOL, RESULTS = Path(sys.argv[1]), Path(sys.argv[2])
A = types.ModuleType("asset_assembly_delta_probe")
exec(compile(TOOL.read_bytes(), str(TOOL), "exec"), A.__dict__)
Refusal = A.AssemblyRefusal
REAL_OPEN, REAL_READ, REAL_LISTDIR, REAL_FSTAT = os.open, os.read, os.listdir, os.fstat
PROBES = []
results = {}


def probe(fn):
    PROBES.append(fn)
    return fn


class Tree:
    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="d")
        self.base = Path(self._tmp.name)
        self.root = self.base / "report"
        self.root.mkdir()

    def write(self, rel, data=b"x"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def fd(self):
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)


def run(target, roles, **overrides):
    own = isinstance(target, Tree)
    fd = target.fd() if own else target
    values = dict(asset_root="report", manifest_path="report/manifest.json", projection_digests=["1" * 64],
                  roles=dict(roles), build_channel="development")
    values.update(overrides)
    try:
        return ("ok", A.assemble(fd, **values))
    except Refusal as exc:
        return ("refusal", exc)
    except Exception as exc:  # noqa: BLE001 - probes record escapes
        return ("escape", exc)
    finally:
        if own:
            os.close(fd)


def label(result):
    kind, value = result
    if kind == "ok":
        return "ok"
    if kind == "refusal":
        return "refusal:" + str(value)
    return "escape:" + type(value).__name__


def fdcount():
    return len(REAL_LISTDIR("/dev/fd"))


def hook_open(target, action):
    fired = []

    def hooked(path, flags, mode=0o777, *, dir_fd=None):
        if path == target and dir_fd is not None and not fired:
            fired.append(1)
            action()
        return REAL_OPEN(path, flags, mode, dir_fd=dir_fd)
    return hooked, fired


@probe
def d01_typed_filesystem_refusal_preserves_codes_cause_and_descriptors():
    detail = {}
    roles = {"report/app.js": "script", "report/sub/b.css": "style"}

    def case(name, want, want_errno=None, setup=None, teardown=None, hook=None, action=None):
        t = Tree()
        t.write("app.js", b"good")
        t.write("sub/b.css", b"b")
        (t.base / "outside.js").write_bytes(b"evil")
        if setup:
            setup(t)
        before = fdcount()
        try:
            if hook:
                hooked, fired = hook_open(hook, lambda: action(t))
                with patch.object(os, "open", hooked):
                    result = run(t, roles)
                assert fired, name
            else:
                result = run(t, roles)
        finally:
            if teardown:
                teardown(t)
        assert fdcount() == before, f"{name}: descriptor leak"
        got = label(result)
        entry = {"outcome": got}
        if got == "refusal:ASSET_FILESYSTEM":
            exc = result[1]
            assert exc.args == ("ASSET_FILESYSTEM",), exc.args
            assert isinstance(exc.__cause__, OSError), exc.__cause__
            entry["cause"] = f"{type(exc.__cause__).__name__}:{errno.errorcode.get(exc.__cause__.errno, exc.__cause__.errno)}"
            if want_errno:
                assert entry["cause"].endswith(":" + want_errno), entry
        assert got == want, f"{name}: {got}"
        detail[name] = entry

    case("memberSwappedToSymlink", "refusal:ASSET_FILESYSTEM", "ELOOP", hook="app.js",
         action=lambda t: ((t.root / "app.js").unlink(), os.symlink(t.base / "outside.js", t.root / "app.js")))
    case("memberRemoved", "refusal:ASSET_FILESYSTEM", "ENOENT", hook="app.js",
         action=lambda t: (t.root / "app.js").unlink())
    case("directorySwappedToSymlink", "refusal:ASSET_FILESYSTEM", hook="sub",
         action=lambda t: (os.rename(t.root / "sub", t.root / "sub-old"), os.symlink("sub-old", t.root / "sub")))
    if os.geteuid() != 0:
        case("unreadableMember", "refusal:ASSET_FILESYSTEM", "EACCES",
             setup=lambda t: os.chmod(t.root / "app.js", 0), teardown=lambda t: os.chmod(t.root / "app.js", 0o644))
        case("untraversableDirectory", "refusal:ASSET_FILESYSTEM", "EACCES",
             setup=lambda t: os.chmod(t.root / "sub", 0), teardown=lambda t: os.chmod(t.root / "sub", 0o755))
    t = Tree()
    t.write("app.js", b"a")
    closed_fd = t.fd()
    os.close(closed_fd)
    result = run(closed_fd, {"report/app.js": "script"})
    detail["closedRootDescriptor"] = label(result)
    assert detail["closedRootDescriptor"] == "refusal:ASSET_FILESYSTEM"

    t = Tree()
    t.write("app.js", b"a")
    t.write("extra.js", b"e")
    detail["undeclaredStillTyped"] = label(run(t, {"report/app.js": "script"}))
    detail["projectionsStillTyped"] = label(run(t, {"report/app.js": "script"}, projection_digests=[]))
    assert detail["undeclaredStillTyped"] == "refusal:ASSET_UNDECLARED_FILE"
    assert detail["projectionsStillTyped"] == "refusal:ASSET_PROJECTIONS"
    u = Tree()
    u.write("app.js", b"a")
    calls = []

    def interrupted(fd, count):
        if not calls:
            calls.append(1)
            raise InterruptedError()
        return REAL_READ(fd, count)
    with patch.object(os, "read", interrupted):
        detail["interruptedReadStillRetried"] = label(run(u, {"report/app.js": "script"}))
    assert detail["interruptedReadStillRetried"] == "ok"
    detail["nonIntegerRootNotMasked"] = label(run("not-a-descriptor", {"report/app.js": "script"}))
    assert detail["nonIntegerRootNotMasked"] == "escape:TypeError"
    return detail


class Reads:
    def __init__(self):
        self.by_inode = {}

    def __call__(self, fd, count):
        data = REAL_READ(fd, count)
        inode = REAL_FSTAT(fd).st_ino
        self.by_inode[inode] = self.by_inode.get(inode, 0) + len(data)
        return data


@probe
def d02_aggregate_precheck_reads_nothing_beyond_bound():
    detail = {}
    t = Tree()
    for name in "abc":
        with open(t.root / f"{name}.woff2", "wb") as f:
            f.truncate(A.MEMBER_LIMIT)
    inode = {n: (t.root / f"{n}.woff2").stat().st_ino for n in "abc"}
    reads = Reads()
    with patch.object(os, "read", reads):
        got = label(run(t, {f"report/{n}.woff2": "font" for n in "abc"}))
    per = {n: reads.by_inode.get(inode[n], 0) for n in "abc"}
    assert got == "refusal:ASSET_BUNDLE_LIMIT", got
    assert per == {"a": A.MEMBER_LIMIT, "b": A.MEMBER_LIMIT, "c": 0}, per
    detail["threeFullMembers"] = {"outcome": got, "bytesReadPerMember": per}

    small = Tree()
    small.write("a.js", b"x" * 10)
    small.write("b.js", b"y" * 10)
    roles = {"report/a.js": "script", "report/b.js": "script"}
    raw = run(small, roles)[1][0]
    total = 20 + len(raw)
    b_inode = (small.root / "b.js").stat().st_ino
    for limit, want in [(total, "ok"), (total - 1, "refusal:ASSET_BUNDLE_LIMIT"),
                        (20, "refusal:ASSET_BUNDLE_LIMIT"), (19, "refusal:ASSET_BUNDLE_LIMIT")]:
        reads = Reads()
        with patch.object(A, "BUNDLE_LIMIT", limit), patch.object(os, "read", reads):
            got = label(run(small, roles))
        assert got == want, (limit, got)
        detail[f"bundleLimit={limit}"] = {"outcome": got, "secondMemberBytesRead": reads.by_inode.get(b_inode, 0)}
    assert detail["bundleLimit=19"]["secondMemberBytesRead"] == 0
    assert detail["bundleLimit=20"]["secondMemberBytesRead"] == 10

    huge = Tree()
    with open(huge.root / "big.js", "wb") as f:
        f.truncate(40 * 1024 * 1024)
    reads = Reads()
    with patch.object(os, "read", reads):
        got = label(run(huge, {"report/big.js": "script"}))
    assert sum(reads.by_inode.values()) == 0
    detail["singleMemberAboveMemberAndBundleCaps"] = {"outcome": got, "bytesRead": 0}
    member = Tree()
    with open(member.root / "big.js", "wb") as f:
        f.truncate(A.MEMBER_LIMIT + 1)
    detail["singleMemberAboveMemberCapOnly"] = label(run(member, {"report/big.js": "script"}))
    assert detail["singleMemberAboveMemberCapOnly"] == "refusal:ASSET_MEMBER_LIMIT"

    grow = Tree()
    grow.write("a.js", b"x" * 10)
    grow.write("b.js", b"y" * 10)
    grow_inode = (grow.root / "b.js").stat().st_ino
    real_stable = A.stable_file_bytes

    def growing(fd, limit):
        if REAL_FSTAT(fd).st_ino == grow_inode:
            with open(grow.root / "b.js", "ab") as f:
                f.write(b"z" * 10)
        return real_stable(fd, limit)
    with patch.object(A, "BUNDLE_LIMIT", 25), patch.object(A, "stable_file_bytes", growing):
        got = label(run(grow, roles))
    assert got == "refusal:ASSET_BUNDLE_LIMIT", got
    detail["growthBetweenPrecheckAndRead"] = got + " (post-read aggregate check remains authoritative)"
    return detail


@probe
def d03_windows_device_names_and_neighbours():
    detail = {}
    reserved = ["con", "prn", "aux", "nul"] + [f"com{i}" for i in range(1, 10)] + [f"lpt{i}" for i in range(1, 10)]
    admitted_reserved = []
    variants = 0
    for base in reserved:
        for name in (base, base + ".txt", base + ".tar.gz", base + ".js.map"):
            variants += 1
            try:
                A.portable_path("report/" + name)
                admitted_reserved.append(name)
            except Refusal:
                pass
    assert not admitted_reserved, admitted_reserved
    detail["reservedVariantsRefused"] = variants
    for path in ["con/app.js", "report/con/app.js", "report/sub/nul.json", "report/lpt9.tar.gz"]:
        try:
            A.portable_path(path)
        except Refusal:
            continue
        raise AssertionError(path)
    neighbours = ["console.js", "conx", "com10", "lpt10", "comm1", "a.con", "app.nul.js", "nulled.txt",
                  "auxiliary.css", "coms", "com0", "lpt0"]
    admitted = []
    for name in neighbours:
        try:
            A.portable_path("report/" + name)
            admitted.append(name)
        except Refusal:
            pass
    assert admitted == neighbours, admitted
    detail["neighboursAdmitted"] = admitted
    t = Tree()
    t.write("app.js", b"a")
    for rel, kind in [("aux.css", "file"), ("nul", "dir"), ("com1.tar.gz", "file")]:
        path = t.root / rel
        if kind == "dir":
            path.mkdir()
        else:
            path.write_bytes(b"x")
        got = label(run(t, {"report/app.js": "script"}))
        if kind == "dir":
            path.rmdir()
        else:
            path.unlink()
        assert got == "refusal:ASSET_PORTABLE_NAME", (rel, got)
        detail["onDisk:" + rel] = got
    detail["manifestPathReserved"] = label(run(t, {"report/app.js": "script"}, manifest_path="report/con.json"))
    detail["assetRootReserved"] = label(run(t, {"aux/app.js": "script"}, asset_root="aux", manifest_path="aux/manifest.json"))
    assert detail["manifestPathReserved"] == detail["assetRootReserved"] == "refusal:ASSET_PORTABLE_NAME"
    return detail


@probe
def d04_final_byte_count_equality_without_false_refusal():
    detail = {}
    t = Tree()
    t.write("app.js", b"0123456789")
    roles = {"report/app.js": "script"}
    assert label(run(t, roles)) == "ok"
    inode = (t.root / "app.js").stat().st_ino
    served = []

    def short(fd, count):
        if REAL_FSTAT(fd).st_ino == inode:
            served.append(1)
            return b"01234" if len(served) == 1 else b""
        return REAL_READ(fd, count)
    before = os.stat(t.root / "app.js")
    with patch.object(os, "read", short):
        detail["shortReadWithUnchangedStat"] = label(run(t, roles))
    after = os.stat(t.root / "app.js")
    assert (before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
    assert detail["shortReadWithUnchangedStat"] == "refusal:ASSET_CHANGED"
    z = Tree()
    z.write("empty.txt", b"")
    with patch.object(os, "read", lambda fd, count: b""):
        detail["zeroByteMemberWithImmediateEof"] = label(run(z, {"report/empty.txt": "notice"}))
    assert detail["zeroByteMemberWithImmediateEof"] == "ok"
    return detail


if __name__ == "__main__":
    for fn in PROBES:
        started = time.monotonic()
        try:
            results[fn.__name__] = {"result": "PASS", "detail": fn()}
        except AssertionError as exc:
            results[fn.__name__] = {"result": "FAIL", "detail": str(exc)}
        except Exception as exc:  # noqa: BLE001
            results[fn.__name__] = {"result": "ERROR", "detail": f"{type(exc).__name__}: {exc}"}
        results[fn.__name__]["seconds"] = round(time.monotonic() - started, 2)
    RESULTS.write_text(json.dumps({"python": sys.version.split()[0], "isolated": sys.flags.isolated,
                                   "dontWriteBytecode": sys.flags.dont_write_bytecode,
                                   "pycachePrefix": sys.pycache_prefix, "probes": results}, indent=2) + "\n")
    print(json.dumps({k: v["result"] for k, v in results.items()}))
    sys.stdout.flush()
    os._exit(0 if all(v["result"] == "PASS" for v in results.values()) else 1)

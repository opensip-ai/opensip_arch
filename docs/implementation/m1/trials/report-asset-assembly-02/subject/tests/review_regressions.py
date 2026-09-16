"""Permanent regressions adopted from actual independent assembly review01.

Run: python -I -B -X pycache_prefix=<empty> assembly_probes.py TOOL OWNER_JSON INTEROP_DIR RESULTS_JSON
The tool is compiled from its bytes; nothing is imported from the subject. Review copy only.
"""
import errno
import hashlib
import json
import os
import sys
import tempfile
import threading
import time
import types
from pathlib import Path
from unittest.mock import patch

TOOL, OWNER, INTEROP, RESULTS = map(Path, sys.argv[1:5])
A = types.ModuleType("asset_assembly_probe")
exec(compile(TOOL.read_bytes(), str(TOOL), "exec"), A.__dict__)
Refusal = A.AssemblyRefusal
P1, P5, PA = "1" * 64, "5" * 64, "a" * 64
REAL_OPEN, REAL_READ, REAL_LISTDIR, REAL_STAT, REAL_FSTAT = os.open, os.read, os.listdir, os.stat, os.fstat
PROBES = []
results = {}


def probe(fn):
    PROBES.append(fn)
    return fn


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fdcount():
    return len(REAL_LISTDIR("/dev/fd"))


class Tree:
    def __init__(self, base=None):
        if base is None:
            self._tmp = tempfile.TemporaryDirectory(prefix="p")
            base = self._tmp.name
        self.base = Path(base)
        self.root = self.base / "report"
        self.root.mkdir(parents=True)

    def write(self, rel, data=b"x"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def open(self):
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)


def build(tree, roles, projections=(P1, P5, PA), channel="development", manifest="report/manifest.json"):
    fd = tree.open()
    try:
        # The default tuple is copied to a list; explicit lists are passed exactly.
        values = list(projections) if isinstance(projections, tuple) else projections
        return A.assemble(fd, asset_root="report", manifest_path=manifest, projection_digests=values,
                          roles=dict(roles), build_channel=channel)
    finally:
        os.close(fd)


def outcome(fn, timeout=20):
    box = {}

    def run():
        try:
            box["value"] = ("ok", fn())
        except Refusal as exc:
            box["value"] = ("refusal", str(exc))
        except OSError as exc:
            box["value"] = ("oserror", f"{type(exc).__name__}:{errno.errorcode.get(exc.errno, exc.errno)}")
        except Exception as exc:  # noqa: BLE001 - probes record any escape
            box["value"] = ("exception", f"{type(exc).__name__}:{exc}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return ("blocked", None)
    return box["value"]


def code(result):
    kind, value = result
    return kind if kind in ("ok", "blocked") else f"{kind}:{value}"


def expect(result, want):
    got = code(result)
    assert got == want, f"expected {want}, got {got}"
    return got


def closed(result):
    got = code(result)
    assert got.startswith(("refusal:", "oserror:")), f"expected fail-closed refusal or OSError, got {got}"
    return got


def recorder(log, name, real):
    def wrapped(*args, **kwargs):
        log.append(name)
        return real(*args, **kwargs)
    return wrapped


class Reads:
    def __init__(self):
        self.calls = 0
        self.bytes = 0

    def __call__(self, fd, count):
        data = REAL_READ(fd, count)
        self.calls += 1
        self.bytes += len(data)
        return data


def owner_validate(manifest, pin):
    from jsonschema import Draft202012Validator
    owner = json.loads(OWNER.read_bytes())
    Draft202012Validator(owner["privateSchemas"]["HostAssetPinV1"]["schema"]).validate(pin)
    Draft202012Validator(owner["privateSchemas"]["ReportAssetManifestV1"]["schema"]).validate(json.loads(manifest))


@probe
def p01_owner_schema_byte_order_and_interop_bundles():
    detail = {}
    nested = Tree(INTEROP / "nested")
    files = {"a/x.js": (b"ax", "script"), "a-b.js": (b"ab", "script"), "a.b/y.css": (b"y{}", "style"),
             "a0.js": (b"", "image"), "fonts/f.woff2": (b"\0font", "font"), "license.txt": (b"", "notice")}
    for rel, (data, _) in files.items():
        nested.write(rel, data)
    (nested.root / "empty-dir").mkdir()
    roles = {"report/" + rel: role for rel, (_, role) in files.items()}
    manifest, pin = build(nested, roles)
    rows = json.loads(manifest)["assets"]
    paths = [row["path"] for row in rows]
    assert paths == sorted(paths, key=lambda p: p.encode("ascii")), paths
    dfs = []

    def walk(directory, rel):
        for name in sorted(os.listdir(directory)):
            child = directory / name
            if child.is_dir():
                walk(child, rel + name + "/")
            else:
                dfs.append("report/" + rel + name)
    walk(nested.root, "")
    assert dfs != paths, "fixture must make traversal order differ from byte order"
    for row in rows:
        data = (nested.root / row["path"][len("report/"):]).read_bytes()
        assert (row["bytes"], row["sha256"], row["role"]) == (len(data), sha(data), roles[row["path"]]), row
    owner_validate(manifest, pin)
    assert manifest.isascii() and b" " not in manifest and b"\n" not in manifest
    assert pin["assetManifestSha256"] == sha(manifest) and pin["assetManifestBytes"] == len(manifest)
    (nested.root / "manifest.json").write_bytes(manifest)
    assert build(nested, roles) == (manifest, pin), "prior manifest must be excluded by exact path"
    (nested.base / "pin.json").write_text(json.dumps(pin))
    (nested.base / "enumeration.json").write_text(json.dumps(sorted(paths + ["report/manifest.json"])))
    detail["nested"] = {"byteOrder": paths, "traversalOrder": dfs, "manifestBytes": len(manifest)}

    deep = Tree(INTEROP / "deep")
    names = [("d%02d" % i) + "x" * 252 for i in range(14)]
    leaf = "f" + "y" * 251 + ".js"
    root_fd = deep.open()
    opened = []
    try:
        current = root_fd
        for name in names:
            os.mkdir(name, dir_fd=current)
            current = REAL_OPEN(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            opened.append(current)
        wfd = REAL_OPEN(leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644, dir_fd=current)
        os.write(wfd, b"deep")
        os.close(wfd)
    finally:
        for fd in opened:
            os.close(fd)
        os.close(root_fd)
    deep_path = "report/" + "/".join(names) + "/" + leaf
    sixteen = sorted(("%x" % i) * 64 for i in range(16))
    manifest, pin = build(deep, {deep_path: "script"}, projections=sixteen)
    owner_validate(manifest, pin)
    assert json.loads(manifest)["assets"][0]["path"] == deep_path and len(deep_path.split("/")) == 16
    (deep.root / "manifest.json").write_bytes(manifest)
    (deep.base / "pin.json").write_text(json.dumps(pin))
    (deep.base / "enumeration.json").write_text(json.dumps(sorted([deep_path, "report/manifest.json"])))
    detail["deep"] = {"segments": 16, "pathChars": len(deep_path), "projections": 16, "manifestBytes": len(manifest)}
    return detail


@probe
def p02_caps_refuse_before_io_where_claimed_and_observed_work():
    detail = {}
    t = Tree()
    t.write("app.js", b"a")
    roles = {"report/app.js": "script"}
    fd = t.open()
    try:
        def pre_io(label, want, **overrides):
            values = dict(asset_root="report", manifest_path="report/manifest.json",
                          projection_digests=[P1, P5, PA], roles=dict(roles), build_channel="development")
            values.update(overrides)
            log = []
            with patch.object(os, "listdir", recorder(log, "listdir", REAL_LISTDIR)), \
                    patch.object(os, "open", recorder(log, "open", REAL_OPEN)), \
                    patch.object(os, "fstat", recorder(log, "fstat", REAL_FSTAT)), \
                    patch.object(os, "stat", recorder(log, "stat", REAL_STAT)), \
                    patch.object(os, "read", recorder(log, "read", REAL_READ)):
                result = outcome(lambda: A.assemble(fd, **values))
            expect(result, want)
            assert log == [], f"{label}: filesystem work before refusal: {log}"
            detail[label] = want + " (no filesystem calls)"
        pre_io("projections17", "refusal:ASSET_PROJECTIONS",
               projection_digests=sorted(("%02x" % i) * 32 for i in range(17)))
        pre_io("projectionsTuple", "refusal:ASSET_PROJECTIONS", projection_digests=(P1,))
        pre_io("roles4097", "refusal:ASSET_ROLES", roles={f"report/f{i:04d}.js": "script" for i in range(4097)})
        pre_io("rolesEmpty", "refusal:ASSET_ROLES", roles={})
        pre_io("channel", "refusal:ASSET_BUILD_CHANNEL", build_channel="Release")
        pre_io("rolePathCase", "refusal:ASSET_PORTABLE_NAME", roles={"report/App.js": "script"})
        pre_io("roleOutsideRoot", "refusal:ASSET_ROLE_PATH", roles={"other/app.js": "script"})
        pre_io("manifestCase", "refusal:ASSET_PORTABLE_NAME", manifest_path="report/Manifest.json")
    finally:
        os.close(fd)

    big = Tree()
    with open(big.root / "big.js", "wb") as f:
        f.truncate(A.MEMBER_LIMIT + 1)
    reads = Reads()
    with patch.object(os, "read", reads):
        expect(outcome(lambda: build(big, {"report/big.js": "font"})), "refusal:ASSET_MEMBER_LIMIT")
    assert reads.calls == 0, "oversized member must refuse from fstat size before reading"
    with open(big.root / "big.js", "wb") as f:
        f.truncate(A.MEMBER_LIMIT)
    reads = Reads()
    with patch.object(os, "read", reads):
        expect(outcome(lambda: build(big, {"report/big.js": "font"}), timeout=60), "ok")
    detail["member"] = {"limitPlusOneBytesRead": 0, "atLimitBytesRead": reads.bytes}

    quad = Tree()
    for name in "abcd":
        with open(quad.root / f"{name}.woff2", "wb") as f:
            f.truncate(A.MEMBER_LIMIT)
    reads = Reads()
    with patch.object(os, "read", reads):
        expect(outcome(lambda: build(quad, {f"report/{n}.woff2": "font" for n in "abcd"}), timeout=120),
               "refusal:ASSET_BUNDLE_LIMIT")
    assert reads.bytes <= A.BUNDLE_LIMIT, reads.bytes
    detail["bundle"] = {"members": "4 x 16MiB", "bytesReadBeforeRefusal": reads.bytes,
                        "bound": "at most one member beyond the aggregate cap"}

    dirs = Tree()
    dirs.write("app.js", b"a")
    for i in range(4095):
        (dirs.root / f"d{i:04d}").mkdir()
    expect(outcome(lambda: build(dirs, roles), timeout=120), "ok")
    (dirs.root / "d4095").mkdir()
    expect(outcome(lambda: build(dirs, roles), timeout=120), "refusal:ASSET_DIRECTORY_LIMIT")
    detail["directories"] = "4096 including root accepted; 4097 refused"

    wide = Tree()
    for i in range(4096):
        (wide.root / f"f{i:04d}.js").write_bytes(b"")
    wide_roles = {f"report/f{i:04d}.js": "notice" for i in range(4096)}
    expect(outcome(lambda: build(wide, wide_roles), timeout=120), "ok")
    (wide.root / "manifest.json").write_bytes(b"{}")
    expect(outcome(lambda: build(wide, wide_roles), timeout=120), "ok")
    (wide.root / "zzzz.js").write_bytes(b"")
    log = []
    with patch.object(os, "stat", recorder(log, "stat", REAL_STAT)):
        expect(outcome(lambda: build(wide, wide_roles), timeout=120), "refusal:ASSET_DIRECTORY_LIMIT")
    assert log == [], "over-count listing must refuse before per-entry stat"
    detail["listing"] = "4096 members + manifest accepted; 4098 entries refused before per-entry stat (listing itself precedes the count)"

    deep = Tree()
    ok_rel = "/".join(f"d{i}" for i in range(14)) + "/f.js"
    deep.write(ok_rel, b"d")
    expect(outcome(lambda: build(deep, {"report/" + ok_rel: "script"})), "ok")
    bad_rel = "/".join(f"d{i}" for i in range(15)) + "/f.js"
    deep.write(bad_rel, b"d")
    expect(outcome(lambda: build(deep, {"report/" + ok_rel: "script"})), "refusal:ASSET_DEPTH")
    (deep.root / bad_rel).unlink()
    (deep.root / bad_rel).parent.joinpath("d15").mkdir()
    expect(outcome(lambda: build(deep, {"report/" + ok_rel: "script"})), "refusal:ASSET_DEPTH")
    detail["depth"] = "16 segments accepted; 17-segment file and 17-segment empty directory refused"
    detail["pathLimitReachable"] = A.DEPTH_LIMIT * 255 + A.DEPTH_LIMIT - 1 > A.PATH_LIMIT
    row = {"bytes": A.MEMBER_LIMIT, "path": "x" * 4095, "role": "script", "sha256": "0" * 64}
    detail["manifestLimitReachableWithinFileAndPathCaps"] = (
        len(json.dumps(row, separators=(",", ":"))) * A.FILE_LIMIT > A.MANIFEST_LIMIT)
    return detail


@probe
def p03_manifest_exact_exclusion_and_self_case():
    detail = {}
    t = Tree()
    t.write("app.js", b"app")
    roles = {"report/app.js": "script"}
    clean = outcome(lambda: build(t, roles))
    assert clean[0] == "ok"
    manifest_file = t.root / "manifest.json"
    with open(manifest_file, "wb") as f:
        f.truncate(A.MANIFEST_LIMIT + 1)
    reads = Reads()
    with patch.object(os, "read", reads):
        assert outcome(lambda: build(t, roles)) == clean
    assert reads.bytes == 3, f"prior manifest must not be read: {reads.bytes}"
    manifest_file.unlink()
    detail["oversizedPriorManifest"] = "excluded unread; identical output"

    def case(label, create, want, cleanup):
        create()
        try:
            detail[label] = expect(outcome(lambda: build(t, roles), timeout=5), want)
        finally:
            cleanup()
    for name, want in [("Manifest.json", "refusal:ASSET_PORTABLE_NAME"), ("MANIFEST.JSON", "refusal:ASSET_PORTABLE_NAME"),
                       ("manifest.json.bak", "refusal:ASSET_UNDECLARED_FILE"), ("manifest.jso", "refusal:ASSET_UNDECLARED_FILE")]:
        p = t.root / name
        case(name, lambda p=p: p.write_bytes(b"{}"), want, lambda p=p: p.unlink())
    nested = t.root / "sub/manifest.json"
    case("sub/manifest.json", lambda: (nested.parent.mkdir(), nested.write_bytes(b"{}")),
         "refusal:ASSET_UNDECLARED_FILE", lambda: (nested.unlink(), nested.parent.rmdir()))
    case("manifestFifo", lambda: os.mkfifo(manifest_file), "refusal:ASSET_NONREGULAR", manifest_file.unlink)
    import socket
    sock = socket.socket(socket.AF_UNIX)
    case("manifestSocket", lambda: sock.bind(str(manifest_file)), "refusal:ASSET_NONREGULAR",
         lambda: (sock.close(), manifest_file.unlink()))
    case("manifestDirectory", manifest_file.mkdir, "refusal:ASSET_MANIFEST_NONREGULAR", manifest_file.rmdir)
    case("manifestSymlink", lambda: manifest_file.symlink_to("app.js"), "refusal:ASSET_NONREGULAR", manifest_file.unlink)
    case("manifestDangling", lambda: manifest_file.symlink_to("missing"), "refusal:ASSET_NONREGULAR", manifest_file.unlink)
    os.link(t.root / "app.js", manifest_file)
    try:
        assert outcome(lambda: build(t, roles)) == clean, "hardlinked prior manifest is still excluded"
    finally:
        manifest_file.unlink()
    detail["manifestHardlinkToMember"] = "excluded by path; member unchanged"
    for label, overrides, want in [
        ("manifestPathRoot", {"manifest": "report"}, "refusal:ASSET_MANIFEST_ROOT"),
        ("manifestPathSibling", {"manifest": "reportx/manifest.json"}, "refusal:ASSET_MANIFEST_ROOT"),
        ("manifestPathNested", {"manifest": "report/sub/manifest.json"}, "refusal:ASSET_MANIFEST_LOCATION"),
    ]:
        detail[label] = expect(outcome(lambda: build(t, roles, **overrides)), want)
    detail["manifestAsRole"] = expect(outcome(lambda: build(t, dict(roles, **{"report/manifest.json": "notice"}))),
                                      "refusal:ASSET_ROLE_PATH")
    backup = t.root / "manifest.json.bak"
    backup.write_bytes(b"declared backup")
    try:
        raw, _ = outcome(lambda: build(t, dict(roles, **{"report/manifest.json.bak": "notice"})))[1]
        assert "report/manifest.json.bak" in [r["path"] for r in json.loads(raw)["assets"]]
    finally:
        backup.unlink()
    detail["declaredBackupIsMember"] = True
    return detail


@probe
def p04_extra_unlisted_hidden_nonregular_and_directory_rows():
    detail = {}
    t = Tree()
    t.write("app.js", b"a")
    t.write("sub/b.css", b"b")
    roles = {"report/app.js": "script", "report/sub/b.css": "style"}
    clean = outcome(lambda: build(t, roles))
    assert clean[0] == "ok"
    (t.root / "empty/deeper").mkdir(parents=True)
    assert outcome(lambda: build(t, roles)) == clean, "empty directories do not change manifest bytes"
    detail["emptyDirectories"] = "admitted; bytes unchanged"
    for rel, kind, want in [("sub/extra.js", "file", "refusal:ASSET_UNDECLARED_FILE"),
                            (".DS_Store", "file", "refusal:ASSET_PORTABLE_NAME"),
                            ("empty/.keep", "file", "refusal:ASSET_PORTABLE_NAME"),
                            ("sub/C.css", "file", "refusal:ASSET_PORTABLE_NAME"),
                            ("sub/café.js", "file", "refusal:ASSET_PORTABLE_NAME"),
                            ("sub/outside", "symlink", "refusal:ASSET_NONREGULAR"),
                            ("empty/fifo", "fifo", "refusal:ASSET_NONREGULAR")]:
        p = t.root / rel
        if kind == "file":
            p.write_bytes(b"x")
        elif kind == "symlink":
            p.symlink_to(t.base)
        else:
            os.mkfifo(p)
        try:
            detail[rel] = expect(outcome(lambda: build(t, roles), timeout=5), want)
        finally:
            p.unlink()
    detail["declaredDirectory"] = expect(outcome(lambda: build(t, dict(roles, **{"report/empty": "script"}))),
                                         "refusal:ASSET_MISSING_FILE")
    detail["declaredChildOfFile"] = expect(outcome(lambda: build(t, dict(roles, **{"report/app.js/x": "script"}))),
                                           "refusal:ASSET_MISSING_FILE")
    return detail


def race_tree():
    t = Tree()
    t.write("app.js", b"good-bytes")
    t.write("sub/b.css", b"b")
    t.write("zzz.js", b"z")
    (t.base / "outside.js").write_bytes(b"evil-bytes")
    roles = {"report/app.js": "script", "report/sub/b.css": "style", "report/zzz.js": "script"}
    return t, roles


def with_open_hook(target, action, fn):
    fired = []

    def hooked(path, flags, mode=0o777, *, dir_fd=None):
        if path == target and dir_fd is not None and not fired:
            fired.append(1)
            action()
        return REAL_OPEN(path, flags, mode, dir_fd=dir_fd)
    with patch.object(os, "open", hooked):
        result = outcome(fn, timeout=5)
    assert fired, f"hook for {target} never fired"
    return result


@probe
def p05_replacement_growth_and_declared_race_limits():
    detail = {}

    def run(label, target, action, check):
        t, roles = race_tree()
        result = with_open_hook(target, lambda: action(t), lambda: build(t, roles))
        detail[label] = check(result)
        return t, result
    exact = lambda want: (lambda result: expect(result, want))  # noqa: E731
    run("memberReplacedByRegular", "app.js", lambda t: os.replace(t.base / "outside.js", t.root / "app.js"),
        exact("refusal:ASSET_CHANGED"))
    run("memberReplacedBySymlink", "app.js",
        lambda t: ((t.root / "app.js").unlink(), os.symlink(t.base / "outside.js", t.root / "app.js")), closed)
    run("memberReplacedByFifo", "app.js", lambda t: ((t.root / "app.js").unlink(), os.mkfifo(t.root / "app.js")),
        exact("refusal:ASSET_NONREGULAR"))
    run("memberRemoved", "app.js", lambda t: (t.root / "app.js").unlink(), closed)
    run("directoryReplacedByDirectory", "sub",
        lambda t: (os.rename(t.root / "sub", t.root / "sub-old"), (t.root / "sub").mkdir(),
                   (t.root / "sub/b.css").write_bytes(b"b")), exact("refusal:ASSET_CHANGED"))
    run("directoryReplacedBySymlink", "sub",
        lambda t: (os.rename(t.root / "sub", t.root / "sub-old"), os.symlink("sub-old", t.root / "sub")), closed)

    t, roles = race_tree()
    (t.root / "manifest.json").write_bytes(b"{}")
    result = with_open_hook("manifest.json", lambda: ((t.root / "manifest.json").unlink(),
                                                      os.mkfifo(t.root / "manifest.json")), lambda: build(t, roles))
    detail["priorManifestReplacedByFifo"] = expect(result, "refusal:ASSET_NONREGULAR")

    def read_hook(label, mutate):
        t, roles = race_tree()
        target = t.root / "app.js"
        inode = target.stat().st_ino
        fired = []
        extra = {}

        def hooked(fd, count):
            data = REAL_READ(fd, count)
            if not fired and REAL_FSTAT(fd).st_ino == inode:
                fired.append(1)
                mutate(target, extra)
            return data
        with patch.object(os, "read", hooked):
            result = outcome(lambda: build(t, roles), timeout=5)
        assert fired
        detail[label] = {"outcome": expect(result, "refusal:ASSET_CHANGED"), **extra}

    def same_length_restore_mtime(target, extra):
        before = os.stat(target)
        with open(target, "r+b") as f:
            f.write(b"EVIL-BYTES")
        os.utime(target, ns=(before.st_atime_ns, before.st_mtime_ns))
        extra["mtimeRestored"] = os.stat(target).st_mtime_ns == before.st_mtime_ns
    read_hook("sameLengthWriteWithMtimeRestored", same_length_restore_mtime)
    read_hook("appendDuringRead", lambda target, extra: target.open("ab").write(b"!"))
    read_hook("truncateDuringRead", lambda target, extra: os.truncate(target, 1))

    t, roles = race_tree()
    result = with_open_hook("zzz.js", lambda: (t.root / "sub/late.js").write_bytes(b"late"), lambda: build(t, roles))
    assert result[0] == "ok"
    assert "report/sub/late.js" not in [r["path"] for r in json.loads(result[1][0])["assets"]]
    detail["fileAddedToVisitedSubdirectory"] = "NOT detected (declared: no atomic snapshot)"
    t, roles = race_tree()
    result = with_open_hook("zzz.js", lambda: (t.root / "app.js").write_bytes(b"EVIL-BYTES"), lambda: build(t, roles))
    assert result[0] == "ok"
    row = next(r for r in json.loads(result[1][0])["assets"] if r["path"] == "report/app.js")
    assert row["sha256"] == sha(b"good-bytes") != sha((t.root / "app.js").read_bytes())
    detail["memberChangedAfterHashing"] = "NOT detected; manifest keeps hashed bytes (load-time verification refuses the changed file)"

    t, roles = race_tree()
    (t.base / "link").symlink_to(t.base / "outside.js")
    stop = threading.Event()

    def swapper():
        while not stop.is_set():
            os.rename(t.root / "app.js", t.base / "hold")
            os.rename(t.base / "link", t.root / "app.js")
            os.rename(t.root / "app.js", t.base / "link")
            os.rename(t.base / "hold", t.root / "app.js")
    worker = threading.Thread(target=swapper, daemon=True)
    worker.start()
    counts = {}
    deadline = time.monotonic() + 1.5
    while time.monotonic() < deadline:
        result = outcome(lambda: build(t, roles), timeout=5)
        got = code(result)
        if result[0] == "ok":
            row = next(r for r in json.loads(result[1][0])["assets"] if r["path"] == "report/app.js")
            assert row["sha256"] == sha(b"good-bytes"), "enumeration emitted outside bytes"
        else:
            closed(result)
        counts[got] = counts.get(got, 0) + 1
    stop.set()
    worker.join()
    detail["concurrentSymlinkSwapStress"] = counts
    return detail


@probe
def p06_custody_open_flags_fd_hygiene_and_no_writes():
    detail = {}
    t = Tree()
    t.write("app.js", b"a")
    t.write("sub/b.css", b"b")
    roles = {"report/app.js": "script", "report/sub/b.css": "style"}

    def snapshot():
        out = []
        for dirpath, dirnames, filenames in os.walk(t.base):
            for name in dirnames + filenames:
                full = os.path.join(dirpath, name)
                s = os.lstat(full)
                out.append((os.path.relpath(full, t.base), s.st_mode, s.st_size, s.st_mtime_ns, s.st_ino))
        return sorted(out)
    before = snapshot()
    fd = t.open()
    values = dict(asset_root="report", manifest_path="report/manifest.json", projection_digests=[P1],
                  roles=roles, build_channel="release")
    try:
        opens = []

        def rec(path, flags, mode=0o777, *, dir_fd=None):
            opens.append((path, flags, dir_fd is not None))
            return REAL_OPEN(path, flags, mode, dir_fd=dir_fd)
        n0 = fdcount()
        with patch.object(os, "open", rec):
            first = outcome(lambda: A.assemble(fd, **values))
        assert first[0] == "ok"
        assert fdcount() == n0, "descriptor leak on success"
        assert outcome(lambda: A.assemble(fd, **values)) == first, "same retained fd must re-enumerate identically"
        os.fstat(fd)
        assert snapshot() == before, "enumeration changed the tree"
        for path, flags, relative in opens:
            assert relative and "/" not in path, (path, relative)
            for flag in (os.O_NOFOLLOW, os.O_CLOEXEC, os.O_NONBLOCK):
                assert flags & flag, (path, flags)
            assert flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND) == 0, (path, flags)
        assert sorted(p for p, f, _ in opens if f & os.O_DIRECTORY) == ["sub"]
        detail["openFlags"] = "every open dir_fd-relative single segment with O_RDONLY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK; O_DIRECTORY for sub only"
        leaks = {}
        extra = t.root / "sub/x.js"
        extra.write_bytes(b"x")
        closed(outcome(lambda: A.assemble(fd, **values)))
        extra.unlink()
        leaks["undeclared"] = fdcount() - n0
        link = t.root / "sub/l"
        link.symlink_to("b.css")
        closed(outcome(lambda: A.assemble(fd, **values)))
        link.unlink()
        leaks["symlink"] = fdcount() - n0

        def swap_to_symlink():
            (t.root / "sub/b.css").rename(t.base / "b.css")
            os.symlink(t.base / "b.css", t.root / "sub/b.css")
        closed(with_open_hook("b.css", swap_to_symlink, lambda: A.assemble(fd, **values)))
        leaks["oserrorInNestedDirectory"] = fdcount() - n0
        assert all(v == 0 for v in leaks.values()), leaks
        detail["descriptorDeltaAfterFailures"] = leaks
    finally:
        os.close(fd)
    file_fd = os.open(t.root / "app.js", os.O_RDONLY)
    try:
        detail["rootFdRegularFile"] = expect(outcome(lambda: A.assemble(file_fd, **values)), "refusal:ASSET_ROOT_NOT_DIRECTORY")
    finally:
        os.close(file_fd)
    u = Tree()
    u.write("app.js", b"a")
    (u.base / "rootlink").symlink_to(u.root)
    link_fd = os.open(u.base / "rootlink", os.O_RDONLY | os.O_DIRECTORY)
    try:
        detail["callerOpenedRootThroughSymlink"] = expect(outcome(lambda: A.assemble(
            link_fd, **dict(values, roles={"report/app.js": "script"}))), "ok") + " (root handle custody is the caller's)"
    finally:
        os.close(link_fd)
    return detail


@probe
def p07_projection_choices_and_portable_namespace():
    detail = {}
    t = Tree()
    t.write("app.js", b"a")
    roles = {"report/app.js": "script"}
    sixteen = sorted(("%x" % i) * 64 for i in range(16))
    for label, values, want in [("one", [P5], "ok"), ("sixteen", sixteen, "ok"),
                                ("seventeen", sorted(sixteen + ["0" * 63 + "1"]), "refusal:ASSET_PROJECTIONS")]:
        result = outcome(lambda: build(t, roles, projections=values))
        detail[label] = expect(result, want)
        if want == "ok":
            assert json.loads(result[1][0])["projectionSchemaSha256s"] == values
    for bad in ([PA, P1], [P1, P1], ["A" * 64], [P1 + "\n"], ["g" * 64], [P1[:63]], [None]):
        expect(outcome(lambda: build(t, roles, projections=bad)), "refusal:ASSET_PROJECTIONS")
    accepted = ["report/0", "report/a-", "report/a_", "report/a..b",
                "report/" + "x" * 255, "/".join(["report"] + ["d"] * 15)]
    rejected = ["report/con", "report/con.txt", "report/nul.txt", "report/com1.js", "report/lpt9", "report/a b", "report/a~", "report/a+b", "report/-a", "report/_a", "report/.", "report/..",
                "report/a.", "report/A", "report/" + "x" * 256, "/".join(["report"] + ["d"] * 16), b"report/a",
                None, "report/aé", "report/ａ", "report/a\x00", "report/a:b", "report\\a"]
    for path in accepted:
        assert A.portable_path(path), path
    for path in rejected:
        try:
            A.portable_path(path)
        except Refusal:
            continue
        raise AssertionError(f"accepted {path!r}")
    detail["portable"] = {"accepted": len(accepted), "rejected": len(rejected),
                          "windowsReservedNamesRefused": ["con", "con.txt", "nul.txt", "com1.js", "lpt9"]}
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
    summary = {"tool": str(TOOL), "toolSha256": sha(TOOL.read_bytes()), "python": sys.version.split()[0],
               "flags": {"isolated": sys.flags.isolated, "dontWriteBytecode": sys.flags.dont_write_bytecode},
               "pycachePrefix": sys.pycache_prefix, "probes": results}
    RESULTS.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v["result"] for k, v in results.items()}))
    sys.stdout.flush()
    os._exit(0 if all(v["result"] == "PASS" for v in results.values()) else 1)

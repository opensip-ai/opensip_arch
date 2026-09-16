import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("asset_assembly", HERE / "tools/report_asset_manifest.py")
assembly = importlib.util.module_from_spec(spec)
# Tests are run with -I -B; compile verified local source directly, no pyc read.
exec(compile(Path(spec.origin).read_bytes(), spec.origin, "exec"), assembly.__dict__)


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "report"
        self.root.mkdir()
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
        self.addCleanup(os.close, self.fd)
        self.addCleanup(self.temp.cleanup)
        self.options = {"asset_root": "report", "manifest_path": "report/manifest.json",
                        "projection_digests": ["1" * 64, "5" * 64, "a" * 64],
                        "roles": {"report/app.js": "script"}, "build_channel": "development"}
        (self.root / "app.js").write_bytes(b"console.log('offline');\n")

    def build(self):
        return assembly.assemble(self.fd, **self.options)

    def refuses(self, code):
        with self.assertRaisesRegex(assembly.AssemblyRefusal, "^" + code + "$"):
            self.build()

    def test_complete_exact_manifest_and_pin(self):
        (self.root / "styles").mkdir()
        (self.root / "styles/main.css").write_bytes(b"body { color: #222 }")
        (self.root / "license.txt").write_bytes(b"")
        self.options["roles"].update({"report/styles/main.css": "style", "report/license.txt": "notice"})
        raw, pin = self.build()
        value = json.loads(raw)
        self.assertEqual(set(value), {"schemaVersion", "projectionSchemaSha256s", "assets"})
        self.assertEqual([r["path"] for r in value["assets"]], sorted(self.options["roles"]))
        for row in value["assets"]:
            data = (self.root / row["path"].removeprefix("report/")).read_bytes()
            self.assertEqual((row["bytes"], row["sha256"]), (len(data), hashlib.sha256(data).hexdigest()))
            self.assertEqual(row["role"], self.options["roles"][row["path"]])
        self.assertEqual(pin, {"schemaVersion": 1, "assetRoot": "report", "assetManifestPath": "report/manifest.json",
                               "assetManifestSha256": hashlib.sha256(raw).hexdigest(), "assetManifestBytes": len(raw),
                               "buildChannel": "development"})
        self.assertEqual(raw, json.dumps(value, sort_keys=True, separators=(",", ":")).encode())
        self.assertFalse((self.root / "manifest.json").exists(), "enumeration must not write the build tree")
        (self.root / "manifest.json").write_bytes(b"old bytes are excluded by exact path")
        self.assertEqual(self.build(), (raw, pin))
        (self.root / "manifest.json.backup").write_bytes(b"not excluded")
        self.refuses("ASSET_UNDECLARED_FILE")

    def test_complete_inventory_has_no_silent_filters(self):
        for name, code in [("extra.bin", "ASSET_UNDECLARED_FILE"), (".hidden", "ASSET_PORTABLE_NAME"),
                           ("APP.js", "ASSET_PORTABLE_NAME"), ("café.js", "ASSET_PORTABLE_NAME")]:
            with self.subTest(name=name):
                path = self.root / name
                if name == "APP.js":
                    # Works on both case-sensitive and insensitive volumes.
                    (self.root / "app.js").rename(path)
                else:
                    path.write_bytes(b"x")
                self.refuses(code)
                if name == "APP.js":
                    path.rename(self.root / "app.js")
                else:
                    path.unlink()
        self.options["roles"]["report/missing.js"] = "script"
        self.refuses("ASSET_MISSING_FILE")

    def test_symlinks_and_nonregular_entries_refuse(self):
        p = self.root / "linked"
        for target in ["app.js", "missing", str(self.root.parent)]:
            p.symlink_to(target)
            self.refuses("ASSET_NONREGULAR")
            p.unlink()
        p = self.root / "manifest.json"
        p.symlink_to("app.js")
        self.refuses("ASSET_NONREGULAR")
        p.unlink()
        p.mkdir()
        self.refuses("ASSET_MANIFEST_NONREGULAR")
        p.rmdir()
        p = self.root / "fifo"
        os.mkfifo(p)
        self.refuses("ASSET_NONREGULAR")
        p.unlink()
        sock = socket.socket(socket.AF_UNIX)
        self.addCleanup(sock.close)
        sock.bind(str(self.root / "socket"))
        self.refuses("ASSET_NONREGULAR")

    def test_retained_directory_survives_path_replacement(self):
        expected = self.build()
        moved = self.root.with_name("original")
        self.root.rename(moved)
        self.root.mkdir()
        (self.root / "app.js").write_bytes(b"replacement")
        self.assertEqual(self.build(), expected)

    def test_member_and_bundle_boundaries(self):
        data = (self.root / "app.js").read_bytes()
        with patch.object(assembly, "MEMBER_LIMIT", len(data)):
            self.build()
        with patch.object(assembly, "MEMBER_LIMIT", len(data) - 1):
            self.refuses("ASSET_MEMBER_LIMIT")
        raw, _ = self.build()
        size = len(data) + len(raw)
        with patch.object(assembly, "BUNDLE_LIMIT", size):
            self.build()
        with patch.object(assembly, "BUNDLE_LIMIT", size - 1):
            self.refuses("ASSET_BUNDLE_LIMIT")
        with patch.object(assembly, "MANIFEST_LIMIT", len(raw)):
            self.build()
        with patch.object(assembly, "MANIFEST_LIMIT", len(raw) - 1):
            self.refuses("ASSET_MANIFEST_LIMIT")

    def test_explicit_roles_paths_and_compatibility(self):
        for role in ["html", "Script", "", 0, []]:
            self.options["roles"]["report/app.js"] = role
            self.refuses("ASSET_ROLE")
        self.options["roles"]["report/app.js"] = "script"
        for values in [[], ["a" * 64, "1" * 64], ["a" * 64] * 2, ["A" * 64], ["a" * 64 + "\n"], [1]]:
            self.options["projection_digests"] = values
            self.refuses("ASSET_PROJECTIONS")
        self.options["projection_digests"] = ["a" * 64]
        self.options["roles"]["report/manifest.json"] = "notice"
        self.refuses("ASSET_ROLE_PATH")
        del self.options["roles"]["report/manifest.json"]
        self.options["manifest_path"] = "elsewhere/manifest.json"
        self.refuses("ASSET_MANIFEST_ROOT")
        self.options["manifest_path"] = "report/nested/manifest.json"
        self.refuses("ASSET_MANIFEST_LOCATION")

    def test_portable_path_profile(self):
        for path in ["report/app.js", "report/fonts/font-1.woff2", "report/notice.txt"]:
            self.assertTrue(assembly.portable_path(path))
        for path in ["", "/a", "a/", "a//b", "a/../b", "a/./b", "a\\b", "a:b", "A", "é", "e\u0301", "a\x00", "a\n", "a.", ".hidden", "x" * 256]:
            with self.subTest(path=path), self.assertRaises(assembly.AssemblyRefusal):
                assembly.portable_path(path)

    def test_stream_interrupt_and_observed_change(self):
        real_read = os.read
        calls = 0

        def interrupted(fd, count):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise InterruptedError()
            return real_read(fd, count)

        expected = self.build()
        with patch.object(assembly.os, "read", interrupted):
            self.assertEqual(self.build(), expected)

        def changed(fd, count):
            data = real_read(fd, count)
            if data:
                with (self.root / "app.js").open("ab") as f:
                    f.write(b"!")
            return data

        with patch.object(assembly, "MEMBER_LIMIT", 40), patch.object(assembly.os, "read", changed):
            self.refuses("ASSET_MEMBER_LIMIT")

    def test_same_length_and_directory_changes_refuse(self):
        real_read = os.read
        changed_once = False

        def same_length(fd, count):
            nonlocal changed_once
            data = real_read(fd, count)
            if data and not changed_once:
                changed_once = True
                path = self.root / "app.js"
                path.write_bytes(b"x" * path.stat().st_size)
            return data

        with patch.object(assembly.os, "read", same_length):
            self.refuses("ASSET_CHANGED")
        real_listdir = os.listdir

        def changed_directory(fd):
            result = real_listdir(fd)
            (self.root / "new.js").write_bytes(b"not in the enumeration")
            return result

        with patch.object(assembly.os, "listdir", changed_directory):
            self.refuses("ASSET_DIRECTORY_CHANGED")


if __name__ == "__main__":
    unittest.main()

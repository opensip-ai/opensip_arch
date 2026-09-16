"""Developer wrapper helpers only; no synthetic approval or activation."""
from pathlib import Path
import hashlib
import importlib.util
import os
import selectors
import signal
import subprocess
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("typescript_check", Path(__file__).resolve().parents[1] / "check_typescript.py")
WRAPPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WRAPPER)


class InputTests(unittest.TestCase):
    def test_regular_inputs_and_exact_pins(self):
        with tempfile.TemporaryDirectory(prefix="opensip-check-inputs-") as temp:
            root = Path(temp)
            (root / "regular").write_bytes(b"exact")
            pin = {"path": "regular", "bytes": 5, "sha256": hashlib.sha256(b"exact").hexdigest()}
            self.assertEqual(WRAPPER.pinned(root, pin), b"exact")
            for change in [{"sha256": "0" * 64}, {"bytes": 6}, {"bytes": True}, {"extra": True}]:
                with self.subTest(change=change), self.assertRaises(ValueError):
                    WRAPPER.pinned(root, {**pin, **change})

    def test_escaping_linked_and_nonregular_paths(self):
        with tempfile.TemporaryDirectory(prefix="opensip-check-paths-") as temp:
            root = Path(temp)
            (root / "regular").write_bytes(b"exact")
            (root / "linked").symlink_to("regular")
            (root / "dir").mkdir()
            names = ["", "../outside", "/absolute", "a//b", "a/./b", "a\\b", "a\0b", "linked", "dir"]
            if hasattr(os, "mkfifo"):
                os.mkfifo(root / "pipe")
                names.append("pipe")
            for name in names:
                with self.subTest(name=name), self.assertRaises((ValueError, FileNotFoundError)):
                    WRAPPER.local(root, name)


@unittest.skipUnless(hasattr(os, "killpg"), "Unix process-group helper profile")
class ProcessTests(unittest.TestCase):
    def test_termination_reaps_parent_and_closes_descendant_output(self):
        code = "import subprocess,sys,time; child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(300)']); print(child.pid,flush=True); time.sleep(300)"
        process = subprocess.Popen([sys.executable, "-I", "-B", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        try:
            self.assertTrue(selector.select(5), "parent did not become ready")
            self.assertGreater(int(process.stdout.readline()), 0)
            WRAPPER.terminate(process)
            self.assertEqual(process.returncode, -signal.SIGKILL)
            self.assertTrue(selector.select(5), "descendant retained stdout")
            self.assertEqual(process.stdout.read(), b"")
            WRAPPER.terminate(process)  # Already reaped is safe.
        finally:
            selector.close()
            # Independent cleanup also handles a future regression in terminate.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
            process.stdout.close()
            process.stderr.close()


if __name__ == "__main__":
    unittest.main()

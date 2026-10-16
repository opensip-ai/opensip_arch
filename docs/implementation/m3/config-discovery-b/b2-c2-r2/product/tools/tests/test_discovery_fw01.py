"""M3-B r5 item 15 (FW-01; unit B2-b3b, B2-b3 plan r2 LD-B2B3-11): the discovery and configuration code reads only.

The production code of the configuration resolver and of discovery (the shared rule, the pure core, the walker and
the invocation grants), with every file it includes in production, must not spawn a process, open a socket, or
create, write, rename or remove a filesystem object. A forbidden name is found on the code with comments and
literals blanked, outside test-gated modules (the environment pin's `blank` and `regions`); a file included only
from test scope is not production. Negative controls plant a spawn, a socket and a write in a copy of each file.
The host's native unit instrument, `discovery.rs`, and the security surface it consumes are covered from unit B2-c1.
From unit B2-c2 (M3-B r8 item 14a), the JSONC reader and the TypeScript configuration graph are covered too, and they
must also read nothing themselves: every configuration byte comes through the caller's custody source.
"""
from pathlib import Path
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_environment_exceptions import INCLUDE, blank, regions  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
COVERED = (
    'crates/host/src/configuration.rs',
    'crates/host/src/discovery.rs',
    'crates/host/src/jsonc.rs',
    'crates/host/src/typescript_config.rs',
    'crates/security/src/custody/discovery_rule.rs',
    'crates/security/src/custody/discovery_scan.rs',
    'crates/security/src/custody/discovery_walk.rs',
    'crates/security/src/discovery_export.rs',
    'crates/security/src/grants.rs',
)
PLANNED = ()
# Pure readers: no filesystem, environment or process access of their own (item 14a's custody source only).
PURE = ('crates/host/src/jsonc.rs', 'crates/host/src/typescript_config.rs')
IMPURE = [r'\bstd::fs\b', r'\bfs::\w+', r'\bFile::\w+', r'\bstd::env\b', r'\benv::\w+', r'\bstd::io\b', r'\bstd::process\b',
          r'\bstd::net\b', r'\bopensip_platform\b', r'\blibc::\w+']
# What production code here must never name.
FORBIDDEN = {
    'spawn': [r'\bstd::process\b', r'\bprocess::Command\b', r'\bCommand\s*::', r'\bCommand\b'],
    'socket': [r'\bTcpStream\b', r'\bTcpListener\b', r'\bUdpSocket\b', r'\bUnixStream\b', r'\bUnixListener\b',
               r'\bUnixDatagram\b', r'\blibc::socket\b', r'\blibc::connect\b'],
    'write': [r'\bOpenOptions\b', r'\bfs::write\b', r'\bfs::create\w*', r'\bfs::remove\w*', r'\bfs::rename\b',
              r'\bfs::copy\b', r'\bfs::hard_link\b', r'\bfs::set_permissions\b', r'\bos::unix::fs::symlink\b',
              r'\bFile::create\w*', r'\bcreate_exclusive_\w+', r'\bcreate_private_directory_stage\w*',
              r'\bpublish_exclusive\w*', r'\bpublish_new_regular\b', r'\brename_replace\w*', r'\breplace_regular\b',
              r'\bwrite_new_regular\w*', r'\bprimitive_write\b', r'\bNamedDirectoryPublication\b',
              r'\bPrivateDirectoryStage\b', r'\blibc::(?:open|openat|mkdir|mkdirat|unlink|unlinkat|rename|renameat|write|pwrite|ftruncate|truncate|chmod|fchmod|chown|fchown|symlink|link|linkat)\b'],
}


def production_files(root):
    """The covered files and every file they include in production: an include edge outside a test-gated
    module, followed transitively."""
    out, queue = set(), list(COVERED)
    while queue:
        rel = queue.pop()
        if rel in out:
            continue
        out.add(rel)
        text = (root / rel).read_text(encoding='utf-8')
        code = blank(text)
        spans = regions(code)
        for m in INCLUDE.finditer(code):
            if any(a < m.start() < b for a, b in spans):
                continue
            target = text[m.end():].split('"', 1)[0]
            if target.endswith('.rs'):
                queue.append(os.path.normpath((Path(rel).parent / target).as_posix()))
    return sorted(out)


def findings(root):
    found = []
    for rel in production_files(root):
        code = blank((root / rel).read_text(encoding='utf-8'))
        spans = regions(code)
        for kind, patterns in FORBIDDEN.items():
            for pattern in patterns:
                for m in re.finditer(pattern, code):
                    if not any(a < m.start() < b for a, b in spans):
                        found.append((rel, kind, code.count('\n', 0, m.start()) + 1, m.group(0)))
    return found


def impure(root):
    found = []
    for rel in PURE:
        code = blank((root / rel).read_text(encoding='utf-8'))
        spans = regions(code)
        for pattern in IMPURE:
            for m in re.finditer(pattern, code):
                if not any(a < m.start() < b for a, b in spans):
                    found.append((rel, code.count('\n', 0, m.start()) + 1, m.group(0)))
    return found


class DiscoveryFw01(unittest.TestCase):
    def test_the_covered_files_exist_and_the_planned_one_waits(self):
        for rel in COVERED:
            self.assertTrue((ROOT / rel).is_file(), rel)
        for rel in PLANNED:
            self.assertFalse((ROOT / rel).exists(), rel + ' exists: add it to COVERED')

    def test_no_production_code_spawns_opens_a_socket_or_writes(self):
        self.assertEqual(findings(ROOT), [])

    def test_test_scope_is_not_production(self):
        # The walker's tests build trees (chmod, mkfifo, writes); they are included only from its test module.
        files = production_files(ROOT)
        self.assertNotIn('crates/security/src/custody/discovery_walk_tests.rs', files)
        self.assertNotIn('crates/host/src/configuration_tests.rs', files)
        self.assertNotIn('crates/host/src/discovery_tests.rs', files)
        self.assertNotIn('crates/host/src/typescript_config_tests.rs', files)

    def test_the_configuration_reader_reads_only_through_its_source(self):
        self.assertEqual(impure(ROOT), [])
        work = self.copy()
        for rel in PURE:
            for line in ('let _ = std::fs::read("/tmp/x");', 'let _ = std::env::var("HOME");'):
                with self.subTest(file=rel, line=line):
                    path = work / rel
                    original = path.read_text()
                    path.write_text(original + '\nfn planted() {\n    ' + line + '\n}\n')
                    self.assertTrue(any(f == rel for f, _, _ in impure(work)))
                    path.write_text(original)

    # ------------------------------------------------------------ negative controls on a copy

    def copy(self):
        work = Path(tempfile.mkdtemp(prefix='opensip-discovery-fw01-'))
        self.addCleanup(shutil.rmtree, work)
        for rel in production_files(ROOT):
            target = work / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)
        return work

    def plant(self, rel, line):
        work = self.copy()
        path = work / rel
        path.write_text(path.read_text() + '\nfn planted() {\n    ' + line + '\n}\n')
        return findings(work)

    def test_a_planted_spawn_socket_or_write_is_caught_in_every_covered_file(self):
        for rel in COVERED:
            for kind, line in [('spawn', 'let _ = std::process::Command::new("/bin/true").status();'),
                               ('socket', 'let _ = std::net::TcpStream::connect("127.0.0.1:1");'),
                               ('write', 'let _ = std::fs::write("/tmp/x", b"x");')]:
                with self.subTest(file=rel, kind=kind):
                    self.assertIn(kind, {k for f, k, _, _ in self.plant(rel, line) if f == rel})

    def test_a_planted_platform_publication_is_caught(self):
        found = self.plant('crates/security/src/custody/discovery_walk.rs', 'let _ = opensip_platform::publish_new_regular;')
        self.assertTrue(any(k == 'write' for _, k, _, _ in found))

    def test_a_forbidden_name_inside_a_test_module_is_not_production(self):
        work = self.copy()
        path = work / 'crates/security/src/grants.rs'
        path.write_text(path.read_text() + '\n#[cfg(test)]\nmod planted {\n    fn f() { let _ = std::fs::write("/tmp/x", b"x"); }\n}\n')
        self.assertEqual(findings(work), [])

    def test_a_production_include_is_covered(self):
        work = self.copy()
        extra = work / 'crates/security/src/custody/planted_helper.rs'
        extra.write_text('fn helper() { let _ = std::fs::remove_file("/tmp/x"); }\n')
        path = work / 'crates/security/src/custody/discovery_walk.rs'
        path.write_text(path.read_text() + '\nmod planted {\n    include!("planted_helper.rs");\n}\n')
        self.assertIn('crates/security/src/custody/planted_helper.rs', production_files(work))
        self.assertTrue(any(f.endswith('planted_helper.rs') for f, _, _, _ in findings(work)))


if __name__ == '__main__':
    unittest.main()

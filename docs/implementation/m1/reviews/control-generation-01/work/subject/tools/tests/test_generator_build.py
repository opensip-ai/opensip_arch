"""Archive admission and observed-build/source joins, without compiling code."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


B = load(ROOT / 'tools/build_contracts.py', 'build_contracts_test')
A = load(ROOT / 'tools/contracts/adapter.py', 'adapter_build_test')


def archive(entries):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as output:
        for path, content, kind in entries:
            member = tarfile.TarInfo(path); member.type = kind
            if kind == tarfile.REGTYPE:
                member.size = len(content)
                output.addfile(member, io.BytesIO(content))
            else:
                member.linkname = '../escape'
                output.addfile(member)
    return buffer.getvalue()


class BuildTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.destination = Path(temporary.name) / 'vendor'
        self.base = [('example-1.0.0/Cargo.toml', b'[package]\nname="example"\nversion="1.0.0"\n', tarfile.REGTYPE)]

    def unpack(self, entries, checksum=None):
        raw = archive(entries)
        return B.unpack_archive(raw, 'example', '1.0.0', checksum or hashlib.sha256(raw).hexdigest(), self.destination)

    def test_archive_bytes_and_checksums(self):
        self.unpack(self.base + [('example-1.0.0/src/lib.rs', b'pub fn example() {}', tarfile.REGTYPE)])
        checksums = json.loads((self.destination / '.cargo-checksum.json').read_text())
        for name, expected in checksums['files'].items():
            self.assertEqual(hashlib.sha256((self.destination / name).read_bytes()).hexdigest(), expected)

    def test_modified_archive_refuses_before_writing(self):
        with self.assertRaisesRegex(B.BuildError, 'checksum mismatch'): self.unpack(self.base, '0' * 64)
        self.assertFalse(self.destination.exists())

    def test_escaping_duplicate_reserved_and_link_members_refuse(self):
        for member in [('../escape', b'', tarfile.REGTYPE), ('/escape', b'', tarfile.REGTYPE),
                       ('example-1.0.0/../escape', b'', tarfile.REGTYPE), self.base[0],
                       ('example-1.0.0/.cargo-checksum.json', b'{}', tarfile.REGTYPE),
                       ('example-1.0.0/link', b'', tarfile.SYMTYPE), ('example-1.0.0/link', b'', tarfile.LNKTYPE)]:
            with self.subTest(member=member[0]), self.assertRaises(B.BuildError): self.unpack(self.base + [member])
            self.assertFalse(self.destination.exists())

    def test_build_receipt_joins(self):
        closure = json.loads((ROOT / 'tools/contracts/generator-closure.json').read_text())
        pinned = {row['path']: (ROOT / row['path']).read_bytes() for row in closure['files']}
        receipt = json.loads(pinned['tools/contracts/build-receipt.json'])
        A.validate_build_receipt(receipt, pinned, closure['toolchain']['generator'])
        mutations = [lambda r: r['sources'][0].update(sha256='0' * 64),
                     lambda r: r['builder'].update(sha256='0' * 64),
                     lambda r: r['executable'].update(sha256='0' * 64),
                     lambda r: r['dependencies'][0].update(sha256='0' * 64),
                     lambda r: r.update(profile='debug'), lambda r: r.update(offline=False)]
        for mutate in mutations:
            changed = copy.deepcopy(receipt); mutate(changed)
            with self.assertRaises(ValueError): A.validate_build_receipt(changed, pinned, closure['toolchain']['generator'])


if __name__ == '__main__':
    unittest.main()

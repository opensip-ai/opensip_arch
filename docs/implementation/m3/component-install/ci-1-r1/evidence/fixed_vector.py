"""CI-1's AT-ARCHIVE-FIXED-VECTOR, computed independently of the Rust codec: a second encoder written from PKG-AP's
headerLayout, byteAlgorithm and trailer text, then cross-read by Python's tarfile (which must see exactly the vector's
members, types, modes, sizes, link targets and payloads). Prints the vector's archive length and SHA-256."""
import hashlib, io, json, sys, tarfile
def payload(n, a, c): return bytes((i * a + c) % 256 for i in range(n))
# (path, mode, type, payload-or-target)
TREE = [
    ('README', 0o644, 'file', payload(700, 7, 3)),
    ('a', 0o755, 'dir', None),
    ('a-x', 0o600, 'file', b''),
    ('a/b', 0o700, 'dir', None),
    ('a/b/c.txt', 0o444, 'file', b'c\n'),
    ('bin', 0o755, 'dir', None),
    ('bin/tool', 0o755, 'file', b'#!/bin/sh\nexit 0\n'),
    ('données', 0o755, 'dir', None),
    ('données/é.txt', 0o644, 'file', payload(512, 13, 5)),
    ('latest', 0o777, 'symlink', 'bin/tool'),
]
def octal(n, width): return ('%0*o' % (width - 1, n)).encode() + b'\0'
def header(path, mode, kind, data):
    h = bytearray(512)
    name = path.encode('utf-8'); assert len(name) <= 100; h[0:len(name)] = name
    h[100:108] = octal(mode, 8); h[108:116] = octal(0, 8); h[116:124] = octal(0, 8)
    h[124:136] = octal(len(data) if kind == 'file' else 0, 12); h[136:148] = octal(0, 12)
    h[156] = {'file': 0x30, 'dir': 0x35, 'symlink': 0x32}[kind]
    if kind == 'symlink':
        t = data.encode('utf-8'); assert len(t) <= 100; h[157:157 + len(t)] = t
    h[257:263] = b'ustar\0'; h[263:265] = b'00'
    h[329:337] = octal(0, 8); h[337:345] = octal(0, 8)
    h[148:156] = b' ' * 8
    h[148:156] = ('%06o' % sum(h)).encode() + b'\0 '
    return bytes(h)
out = bytearray()
for path, mode, kind, data in sorted(TREE, key=lambda r: [ord(c) for c in r[0]]):
    out += header(path, mode, kind, data)
    if kind == 'file':
        out += data + b'\0' * (-len(data) % 512)
out += b'\0' * 1024
files = [r for r in TREE if r[2] == 'file']
assert len(out) == 512 * len(TREE) + sum(512 * -(-len(r[3]) // 512) for r in files) + 1024
with tarfile.open(fileobj=io.BytesIO(bytes(out)), mode='r:', format=tarfile.USTAR_FORMAT) as t:
    members = t.getmembers()
    assert [m.name for m in members] == sorted(r[0] for r in TREE), [m.name for m in members]
    for m, (path, mode, kind, data) in zip(members, sorted(TREE)):
        assert m.mode == mode and m.uid == 0 and m.gid == 0 and m.mtime == 0 and m.uname == '' and m.gname == ''
        assert {'file': m.isreg(), 'dir': m.isdir(), 'symlink': m.issym()}[kind]
        if kind == 'file': assert m.size == len(data) and t.extractfile(m).read() == data
        if kind == 'symlink': assert m.linkname == data
print(json.dumps(dict(length=len(out), sha256=hashlib.sha256(out).hexdigest(), members=len(TREE), tarfileCrossRead=True)))
if len(sys.argv) > 1: open(sys.argv[1], 'wb').write(out)

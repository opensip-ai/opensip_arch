"""F8a identity source audit: strip comments/strings, then report external path roots,
extern crate declarations, unsafe, includes, #[path], env macros, FFI attributes."""
import re, sys, json, hashlib
from pathlib import Path

def strip(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith('//', i):
            j = src.find('\n', i); j = n if j < 0 else j
            out.append(' ' * (j - i)); i = j
        elif src.startswith('/*', i):
            depth, j = 1, i + 2
            while j < n and depth:
                if src.startswith('/*', j): depth += 1; j += 2
                elif src.startswith('*/', j): depth -= 1; j += 2
                else: j += 1
            out.append(re.sub(r'[^\n]', ' ', src[i:j])); i = j
        elif re.match(r'b?r#*"', src[i:i+260]):
            m = re.match(r'(b?r)(#*)"', src[i:]); hashes = m.group(2)
            end = src.find('"' + hashes, i + len(m.group(0)))
            j = end + 1 + len(hashes)
            out.append('""' + re.sub(r'[^\n]', ' ', src[i+2:j])[2:]); i = j
        elif c == '"' or src.startswith('b"', i):
            j = i + (2 if c == 'b' else 1)
            while src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            j += 1
            out.append('"' + re.sub(r'[^\n]', ' ', src[i+1:j-1]) + '"'); i = j
        elif c == "'" and re.match(r"b?'(\\.[^']*|[^\\'])'", src[i:i+12]):
            m = re.match(r"b?'(\\.[^']*|[^\\'])'", src[i:]); out.append(' ' * len(m.group(0))); i += len(m.group(0))
        else:
            out.append(c); i += 1
    return ''.join(out)

ALLOWED_ROOTS = {'crate', 'self', 'super', 'alloc', 'core', 'Self'}
PATTERNS = {
    'extern_crate': r'\bextern\s+crate\s+(\w+)',
    'extern_block': r'\bextern\s*"',
    'unsafe': r'\bunsafe\b',
    'include': r'\binclude(_bytes|_str)?\s*!',
    'path_attr': r'#\s*\[\s*path\b',
    'env_macro': r'\b(option_)?env\s*!',
    'ffi_attr': r'#\s*\[\s*(no_mangle|export_name|link|link_name|link_section|used)\b',
    'asm': r'\b(global_)?asm\s*!',
    'std_path': r'\bstd\s*::',
    'allow_unsafe': r'allow\s*\(\s*unsafe',
    'cfg_attr': r'#\s*\[\s*cfg_attr\b',
}
root = Path(sys.argv[1])
files = sys.argv[2:]
report = {}
for name in files:
    raw = (root / name).read_bytes()
    src = strip(raw.decode())
    roots = {}
    for m in re.finditer(r'(?<![\w:])([A-Za-z_]\w*)\s*::', src):
        roots.setdefault(m.group(1), 0); roots[m.group(1)] += 1
    # Absolute paths (::name::...) always name an extern crate root.
    for m in re.finditer(r'(?<![\w:>])::\s*([A-Za-z_]\w*)', src):
        key = '::' + m.group(1); roots.setdefault(key, 0); roots[key] += 1
    # Names declared locally (mods, types, enums, use-aliases) are fine roots too.
    local = set(re.findall(r'\b(?:mod|struct|enum|trait|type|union)\s+([A-Za-z_]\w*)', src))
    local |= set(re.findall(r'\bas\s+([A-Za-z_]\w*)', src))
    local |= set(re.findall(r'\buse\s+[\w:]*::\{?[^;]*?\b([A-Z]\w*)\b', src))
    hits = {k: [ (src[:m.start()].count('\n') + 1, m.group(0)) for m in re.finditer(p, src)] for k, p in PATTERNS.items()}
    report[name] = {
        'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
        'useLines': [l.strip() for l in src.splitlines() if re.match(r'\s*(pub(\([\w:]+\))?\s+)?use\s', l)],
        'pathRoots': dict(sorted(roots.items())),
        'hits': {k: v for k, v in hits.items() if v},
    }
print(json.dumps(report, indent=1))

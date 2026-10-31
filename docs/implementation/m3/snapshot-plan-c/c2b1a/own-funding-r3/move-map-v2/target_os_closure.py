"""LD-Q-130 control (no non-macOS target is installed offline): the law, metered and priced crates name no
cfg(target_os)-gated module, directly or through the modules they import.

1. No `target_os` inside any `cfg(...)`/`cfg_attr(...)` attribute in the three crates' files.
2. Every path `opensip_<dep>::<m1>::<m2>...` used in them is resolved in crates/<dep>: each module declaration on the
   chain (`mod m1;` in lib.rs, `mod m2` in m1's file or inline in it) must carry no attribute naming `target_os`.
   The referenced module files' own `use crate::...` paths are followed the same way, recursively (fail-closed:
   an unresolvable module is a failure).
Usage: target_os_closure.py <workspace root> [crate dirs...]   (default: crates/host-law crates/host-metered crates/host-priced)
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
CRATES = sys.argv[2:] or ['crates/host-law', 'crates/host-metered', 'crates/host-priced']
CFG_OS = re.compile(r'#!?\[\s*cfg(?:_attr)?\s*\([^\]]*\btarget_os\b')
EXT = re.compile(r'\b(opensip_[a-z_]+)((?:::[a-z_][a-z0-9_]*)+)')
CRATE_USE = re.compile(r'\b(?:crate)((?:::[a-z_][a-z0-9_]*)+)')
fails, seen = [], set()


def strip(text):
    text = re.sub(r'//[^\n]*', '', text)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', text)


def decl(text, name):
    """The attribute lines immediately above `mod name` (out-of-line or inline), or None."""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if re.match(rf'^\s*(?:pub(?:\([^)]*\))?\s+)?mod\s+{name}\s*[;{{]', line):
            attrs, k = [], i - 1
            while k >= 0 and (lines[k].strip().startswith('#[') or lines[k].strip().startswith('//')):
                attrs.append(lines[k])
                k -= 1
            return attrs, i
    return None


def module_file(crate_dir, chain):
    """Resolve module chain [m1, m2, ...] in a crate; check every declaration; return (text, file) of the last."""
    src = crate_dir / 'src'
    cur_file, cur_text = src / 'lib.rs', (src / 'lib.rs').read_text()
    cur_dir = src
    inline_scope = None
    for depth, m in enumerate(chain):
        scope = inline_scope if inline_scope is not None else cur_text
        d = decl(scope, m)
        if d is None:
            return None  # not a module: an item (fn/const/type) of the previous module
        attrs, at = d
        if any('target_os' in a for a in attrs):
            fails.append(f'{crate_dir.name}: module {"::".join(chain[:depth + 1])} is declared under {attrs}')
        line = scope.split('\n')[at]
        if line.rstrip().endswith('{'):
            body = '\n'.join(scope.split('\n')[at + 1:])
            inline_scope = body
            continue
        inline_scope = None
        path_attr = next((re.search(r'path\s*=\s*"([^"]+)"', a).group(1) for a in attrs if 'path' in a and '=' in a), None)
        base = cur_dir if cur_file.name in ('lib.rs', 'mod.rs') else cur_dir / cur_file.stem
        cands = [base / path_attr] if path_attr else [base / f'{m}.rs', base / m / 'mod.rs']
        hit = next((c for c in cands if c.exists()), None)
        if hit is None:
            fails.append(f'{crate_dir.name}: cannot resolve module {"::".join(chain[:depth + 1])}')
            return None
        cur_file, cur_text, cur_dir = hit, hit.read_text(), hit.parent
        if CFG_OS.search(cur_text.split('\n', 1)[0]) or re.search(r'^#!\[cfg\([^\]]*target_os', cur_text, re.M):
            fails.append(f'{hit}: inner cfg(target_os)')
    return cur_text, cur_file


def follow(crate_dir, chain):
    key = (crate_dir, tuple(chain))
    if key in seen:
        return
    seen.add(key)
    # walk the longest prefix that resolves to modules
    for n in range(len(chain), 0, -1):
        got = module_file(crate_dir, chain[:n])
        if got is not None:
            text, _ = got
            for m in CRATE_USE.finditer(strip(text)):
                follow(crate_dir, m.group(1).strip(':').split('::'))
            return


for c in CRATES:
    cdir = ROOT / c
    for f in sorted((cdir / 'src').rglob('*.rs')):
        text = f.read_text()
        for m in CFG_OS.finditer(text):
            fails.append(f'{f.relative_to(ROOT)}: cfg(target_os) attribute: {m.group(0)}')
        for m in EXT.finditer(strip(text)):
            dep = m.group(1)[len('opensip_'):].replace('_', '-')
            ddir = ROOT / 'crates' / dep
            if not ddir.exists():
                fails.append(f'{f.relative_to(ROOT)}: unknown crate {m.group(1)}')
                continue
            follow(ddir, m.group(2).strip(':').split('::'))
print(f'{len(seen)} module chains followed in the dependencies')
for x in sorted(set(fails)):
    print('FAIL', x)
print('PASS: no cfg(target_os) in the closure' if not fails else f'{len(set(fails))} FAILURES')
sys.exit(1 if fails else 0)

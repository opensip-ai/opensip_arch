"""M3-B r6 item 12 (unit B2-b3d, plan r2 LD-B2B3D-2 and Codex B2B3DPLAN-R1-NBO-1): the walker builds no absolute
spelling in production.

The redesigned walker keeps no per-entry absolute spelling. Its test-only trace and open hook stay absolute, so each
call passes a closure that spells the path, and the production stubs take the closure and never call it. On the code
with comments and literals blanked (the environment pin's `blank`), this check holds that:
  * every `trace(..)` and `before_open(..)` call passes a closure;
  * the production stubs of both never call their closure;
  * an absolute spelling (`spelled(..)`) is built only inside such a closure, inside `ListingConversion::finish`'s
    terminal refusal closure, inside the terminal `changed` refusal, or by the `spelled` method that both delegate to;
  * the absolute `join(..)` is called only by `spelled`;
  * (r2, Codex B2B3D-R1-RF-1) in `enter`, the observation array's allowance is charged before the array is reserved.
Negative controls plant a direct spelling, a direct-string trace, a stub that calls its closure and a reservation
before its charge in a copy, and each must fail.
"""
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_environment_exceptions import blank  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WALK = 'crates/security/src/custody/discovery_walk.rs'
STUBS = (
    "#[cfg(not(test))]\nfn trace(_: &'static str, _: impl FnOnce() -> String) {}",
    "#[cfg(not(test))]\nfn before_open(_: impl FnOnce() -> String) {}",
)


def production(text):
    """The walker's code with comments and literals blanked, its included test module cut off."""
    code = blank(text)
    cut = code.find('mod tests {')
    return code if cut < 0 else code[:cut]


def body(code, signature):
    """The brace-matched body of the one function whose header matches `signature`."""
    hits = [m.start() for m in re.finditer(signature, code)]
    assert len(hits) == 1, (signature, len(hits))
    start = code.index('{', hits[0])
    depth = 0
    for i in range(start, len(code)):
        depth += {'{': 1, '}': -1}.get(code[i], 0)
        if depth == 0:
            return start, i
    raise AssertionError('unbalanced ' + signature)


def violations(text):
    code = production(text)
    out = []
    for stub in STUBS:
        if stub not in text:
            out.append('missing production stub: ' + stub.splitlines()[1])
    for m in re.finditer(r'(?<![\w.])(trace|before_open)\(', code):
        if re.match(r'\s*fn\b', code[max(0, m.start() - 4):m.start()]) or code[max(0, m.start() - 3):m.start()] == 'fn ':
            continue
        args = code[m.end():m.end() + 200]
        if m.group(1) == 'trace':
            args = args.split(',', 1)[1] if ',' in args else args
        if not args.lstrip().startswith('||'):
            out.append('%s call without a closure at %d' % (m.group(1), code.count('\n', 0, m.start()) + 1))
    allowed = [body(code, r'fn changed\('), body(code, r'pub\(crate\) fn finish\('), body(code, r'fn spelled\(&self')]
    for m in re.finditer(r'(?<![\w])(?:self\.)?spelled\(', code):
        line_start = code.rfind('\n', 0, m.start()) + 1
        before = code[line_start:m.start()]
        if re.search(r'\bfn\s+$', before):
            continue
        if before.rstrip().endswith('||') or any(a <= m.start() <= b for a, b in allowed):
            continue
        out.append('absolute spelling outside a closure or terminal refusal at %d' % (code.count('\n', 0, m.start()) + 1))
    spelled_body = body(code, r'\nfn spelled\(')
    for m in re.finditer(r'(?<![\w.])join\(', code):
        before = code[code.rfind('\n', 0, m.start()) + 1:m.start()]
        if re.search(r'\bfn\s+$', before) or spelled_body[0] <= m.start() <= spelled_body[1]:
            continue
        out.append('absolute join outside spelled at %d' % (code.count('\n', 0, m.start()) + 1))
    enter = body(code, r'fn enter\(')
    region = code[enter[0]:enter[1]]
    charge = region.find('size_of::<ChildObservation>')
    reserve = region.find('Vec::with_capacity(paths.len())')
    if charge < 0 or reserve < 0 or charge > reserve:
        out.append('the observation array is reserved before its charge')
    return out


class WalkerStorage(unittest.TestCase):
    def test_the_walker_builds_no_absolute_spelling_in_production(self):
        self.assertEqual(violations((ROOT / WALK).read_text()), [])

    def test_a_planted_direct_spelling_is_caught(self):
        text = (ROOT / WALK).read_text()
        anchor = '        let observation = parent\n            .observe_child_accounted(OsStr::new(name), work)\n'
        self.assertEqual(text.count(anchor), 1)
        planted = text.replace(anchor, '        let _spelling = self.spelled(rel);\n' + anchor)
        self.assertTrue(any('absolute spelling' in v for v in violations(planted)))

    def test_a_planted_direct_string_trace_is_caught(self):
        text = (ROOT / WALK).read_text()
        anchor = '        trace("list", || self.spelled(rel));\n'
        self.assertEqual(text.count(anchor), 1)
        planted = text.replace(anchor, '        trace("list", self.spelled(rel));\n')
        self.assertTrue(any('trace call without a closure' in v for v in violations(planted)))

    def test_a_production_stub_that_calls_its_closure_is_caught(self):
        text = (ROOT / WALK).read_text()
        planted = text.replace(STUBS[0], "#[cfg(not(test))]\nfn trace(_: &'static str, path: impl FnOnce() -> String) {\n    let _ = path();\n}")
        self.assertTrue(any('missing production stub' in v for v in violations(planted)))

    def test_a_reservation_before_its_charge_is_caught(self):
        text = (ROOT / WALK).read_text()
        reserve = '        let mut observed = Vec::with_capacity(paths.len());\n'
        self.assertEqual(text.count(reserve), 1)
        charge_at = text.index('        work.charge::<WalkRefusal>(owned(\n            paths\n')
        planted = text.replace(reserve, '')
        planted = planted[:charge_at] + reserve + planted[charge_at:]
        self.assertIn('the observation array is reserved before its charge', violations(planted))


if __name__ == '__main__':
    unittest.main()

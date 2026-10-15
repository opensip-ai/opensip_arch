"""M3-B r5 item 9 (unit B1-b): the environment structural check's exception list, held exactly.

Every `std::env::{var, var_os, vars, vars_os}` call in crates/host and crates/security, by file, enclosing
function and the actual variable name (constants resolved to their values), must equal law's enumerated list.
Every `#[allow(clippy::disallowed_methods ...)]` must be attached to exactly those functions. Every exception but
`git_tracking::process_environment` must be inside a test target: a `tests/` file, a test-gated module (found by
brace matching on code with comments and literals blanked), or a file `include!`d only from one. The two
crate-local clippy.toml files must configure the four methods identically. Negative controls mutate a copy.
"""
from pathlib import Path
import os
import re
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
CRATES = ('crates/host', 'crates/security')
CALL = re.compile(r'\benv::(var|var_os|vars|vars_os)\s*\(')
FN = re.compile(r'^\s*(?:pub(?:\([a-z]+\))?\s+)?fn\s+(\w+)')
ALLOW = re.compile(r'#\[allow\(\s*clippy::disallowed_methods\b[^\]]*\]')
ATTACHED = re.compile(r'(?:\s*#\[[^\]]*\])*\s*(?:pub(?:\([a-z]+\))?\s+)?fn\s+(\w+)')
TEST_GATE = re.compile(r'#\[cfg\((?:all\()?\s*test\b[^\]]*\]\s*(?:#\[[^\]]*\]\s*)*(?:pub(?:\([a-z]+\))?\s+)?mod\s+\w+\s*\{')
INCLUDE = re.compile(r'\binclude!\(\s*"')
PRODUCTION = {('crates/security/src/custody/git_tracking.rs', 'process_environment', '*')}
# M3-B r5 item 9's list: (file, enclosing function, variable name). `*` is the whole environment.
EXPECTED = PRODUCTION | {
    ('crates/host/tests/commit_matrix_tests.rs', 'selected', 'OPENSIP_X9_ROWS'),
    ('crates/host/tests/commit_matrix_tests.rs', 'run_host_matrix', 'OPENSIP_X9_RUN_SET'),
    ('crates/host/tests/commit_matrix_tests.rs', 'run_host_matrix', 'OPENSIP_X9_CENSUS_ONLY'),
    ('crates/host/tests/commit_matrix_tests.rs', 'run_host_matrix', 'OPENSIP_X9_RELEASE_ABSENCE'),
    ('crates/host/tests/admission_tests.rs', 'rustc_path', 'RUSTC'),
    ('crates/host/tests/admission_tests.rs', 'nested_cargo', 'CARGO'),
    ('crates/host/tests/admission_tests.rs', 'helper_publish', 'OPENSIP_X8_INPUT'),
    ('crates/host/tests/admission_tests.rs', 'x8_helper_publish_revocation', 'OPENSIP_X8_HELPER'),
    ('crates/security/src/journal_store.rs', 'macos_retained_path_limit_is_context_not_disk_full', 'OPENSIP_TEST_RETAINED_PATH_130'),
    ('crates/security/src/custody/installation_fence.rs', 'installation_fence_child_probe', 'OPENSIP_TEST_FENCE341_CARRIER'),
    ('crates/security/src/custody/installation_fence.rs', 'installation_fence_child_probe', 'OPENSIP_TEST_FENCE341_BUSY'),
    ('crates/security/src/custody/installation_root.rs', 'installation_root_native_source_ignores_environment_child', 'OPENSIP_TEST_ROOT351_CHILD'),
    ('crates/security/src/custody/installation_root.rs', 'installation_root_native_source_ignores_environment_child', 'HOME'),
    ('crates/security/src/custody/installation_routing_tests.rs', 'a_development_build_ends_at_f0_with_no_notice_and_no_installation_path', 'HOME'),
    ('crates/security/src/custody/ordinary_writer_tests.rs', 'a_development_build_ends_in_the_no_embedded_release_row', 'HOME'),
    ('crates/security/src/custody/read_premise_tests.rs', 'a_development_build_ends_in_the_no_embedded_release_row', 'HOME'),
}


def blank(text):
    """The source with comments and the contents of string and char literals replaced by spaces (newlines
    kept), so braces and keywords inside them never count. Literal delimiters stay; offsets are unchanged."""
    out = list(text)
    i, n = 0, len(text)
    def wipe(a, b):
        for k in range(a, b):
            if out[k] != '\n':
                out[k] = ' '
    while i < n:
        c = text[i]
        if text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            wipe(i, j); i = j
        elif text.startswith('/*', i):
            depth, j = 1, i + 2
            while j < n and depth:
                if text.startswith('/*', j): depth += 1; j += 2
                elif text.startswith('*/', j): depth -= 1; j += 2
                else: j += 1
            wipe(i, j); i = j
        elif (c == 'r' or (c == 'b' and text.startswith('br', i))) and re.match(r'b?r#*"', text[i:]) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == '_')):
            m = re.match(r'b?r(#*)"', text[i:]); hashes = m.group(1); start = i + m.end()
            end = text.find('"' + hashes, start)
            end = n if end < 0 else end
            wipe(start, end); i = end + 1 + len(hashes)
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            wipe(i + 1, j); i = j + 1
        elif c == "'" and re.match(r"'(\\.|[^\\'])'", text[i:i + 4] + '    '):
            m = re.match(r"'(\\.|[^\\'])'", text[i:])
            wipe(i + 1, i + m.end() - 1); i += m.end()
        else:
            i += 1
    return ''.join(out)


def regions(code):
    """Character ranges of test-gated modules: from the module's `{` to its matching `}`."""
    found = []
    for m in TEST_GATE.finditer(code):
        open_at = m.end() - 1
        depth, j = 0, open_at
        while j < len(code):
            if code[j] == '{': depth += 1
            elif code[j] == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        found.append((open_at, j))
    return found


def constant(text, name):
    values = re.findall(r'\bconst\s+' + re.escape(name) + r'\s*:\s*&(?:\'static\s+)?str\s*=\s*"([^"]*)"\s*;', text)
    assert len(values) == 1, (name, values)
    return values[0]


def scan(root):
    files = {p.relative_to(root).as_posix(): p for crate in CRATES for p in sorted((root / crate).rglob('*.rs'))}
    texts = {rel: p.read_text(encoding='utf-8') for rel, p in files.items()}
    codes = {rel: blank(t) for rel, t in texts.items()}
    # Every real include edge (found on the blanked code, so comments and literals never count; the path
    # is read from the raw text at the same offset) with whether it sits inside a test-gated module.
    edges = []
    for rel, code in codes.items():
        spans = regions(code)
        for m in INCLUDE.finditer(code):
            target = texts[rel][m.end():].split('"', 1)[0]
            if target.endswith('.rs'):
                resolved = os.path.normpath((Path(rel).parent / target).as_posix())
                edges.append((rel, resolved, any(a < m.start() < b for a, b in spans)))
    # Production reachability (Codex B1B-R3-RF-01): the production roots are the files outside `tests/`
    # that nothing includes (crate roots and `mod` files); production then flows along every include edge
    # that is not inside a test-gated module. A file it reaches is production, a `tests/` file included,
    # so one production-reachable inclusion makes any file production. Every other file is wholly test
    # code: an integration-test entry point, or a file included only from test scope.
    targets = {target for _, target, _ in edges}
    production = {rel for rel in codes if '/tests/' not in rel and rel not in targets}
    changed = True
    while changed:
        changed = False
        for source, target, scoped in edges:
            if not scoped and source in production and target in codes and target not in production:
                production.add(target)
                changed = True
    whole_test = {rel: rel not in production for rel in codes}
    calls, allows, test_only = set(), set(), {}
    for rel, code in codes.items():
        # Each allow (possibly over several lines) must be attached to a function: only attributes
        # and whitespace between them.
        for m in ALLOW.finditer(code):
            attached = ATTACHED.match(code, m.end())
            assert attached, (rel, code.count('\n', 0, m.start()) + 1)
            allows.add((rel, attached.group(1)))
        text = texts[rel]
        spans = regions(code)
        lines = code.split('\n')
        offsets = [0]
        for line in lines:
            offsets.append(offsets[-1] + len(line) + 1)
        whole_file_test = whole_test[rel]
        enclosing = None
        for index, line in enumerate(lines):
            match = FN.match(line)
            if match:
                enclosing = match.group(1)
            for call in CALL.finditer(line):
                raw_line = text.split('\n')[index]
                argument = raw_line[call.end():].split(')', 1)[0].strip()
                if call.group(1) in ('vars', 'vars_os'):
                    variable = '*'
                elif argument.startswith('"'):
                    variable = argument.strip('"')
                else:
                    variable = constant(text, argument.split('::')[-1])
                key = (rel, enclosing, variable)
                calls.add(key)
                at = offsets[index] + call.start()
                test_only[key] = whole_file_test or any(a < at < b for a, b in spans)
    return calls, allows, test_only


class EnvironmentExceptions(unittest.TestCase):
    def test_the_call_sites_are_exactly_the_enumerated_list(self):
        calls, _, _ = scan(ROOT)
        self.assertEqual(calls, EXPECTED)

    def test_the_allows_are_attached_to_exactly_the_enumerated_functions(self):
        calls, allows, _ = scan(ROOT)
        self.assertEqual(allows, {(f, fn) for f, fn, _ in calls})

    def test_every_exception_but_the_git_check_is_inside_a_test_target(self):
        calls, _, test_only = scan(ROOT)
        for key in calls - PRODUCTION:
            self.assertTrue(test_only[key], key)
        for key in PRODUCTION:
            self.assertFalse(test_only[key], key)

    def test_no_import_reaches_the_methods_unqualified(self):
        for crate in CRATES:
            for path in (ROOT / crate).rglob('*.rs'):
                code = blank(path.read_text(encoding='utf-8'))
                self.assertNotRegex(code, r'use\s+std::env::\{?[^;]*\b(var|var_os|vars|vars_os)\b', str(path))
                self.assertNotRegex(code, r'use\s+std::env\s*;', str(path))

    def test_both_clippy_configurations_refuse_the_four_methods_identically(self):
        host, security = ((ROOT / crate / 'clippy.toml').read_bytes() for crate in CRATES)
        self.assertEqual(host, security)
        for method in ('var', 'var_os', 'vars', 'vars_os'):
            self.assertIn(f'path = "std::env::{method}"'.encode(), host)
        self.assertFalse((ROOT / 'clippy.toml').exists(), 'a workspace clippy.toml would widen the scope')

    # ------------------------------------------------------------ negative controls on a copy

    def copy(self):
        work = Path(tempfile.mkdtemp(prefix='opensip-environment-exceptions-'))
        self.addCleanup(shutil.rmtree, work)
        for crate in CRATES:
            for path in (ROOT / crate).rglob('*.rs'):
                target = work / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        return work

    def test_a_changed_constant_value_is_caught(self):
        work = self.copy()
        path = work / 'crates/security/src/journal_store.rs'
        text = path.read_text()
        self.assertEqual(text.count('"OPENSIP_TEST_RETAINED_PATH_130"'), 1)
        path.write_text(text.replace('"OPENSIP_TEST_RETAINED_PATH_130"', '"HOME"'))
        calls, _, _ = scan(work)
        self.assertNotEqual(calls, EXPECTED)

    def test_an_allowed_helper_moved_out_of_its_test_module_is_caught(self):
        work = self.copy()
        path = work / 'crates/security/src/custody/installation_fence.rs'
        text = path.read_text()
        code = blank(text)
        start = ALLOW.search(code).start()
        # The function's attributes start at the `#[test]` just above the allow.
        start = code.rindex('#[test]', 0, start)
        body_open = code.index('{', code.index('fn installation_fence_child_probe', start))
        depth, end = 0, body_open
        while True:
            if code[end] == '{': depth += 1
            elif code[end] == '}':
                depth -= 1
                if depth == 0: break
            end += 1
        moved = text[start:end + 1]
        path.write_text(text[:start] + text[end + 1:] + '\n' + moved + '\n')
        calls, _, test_only = scan(work)
        key = ('crates/security/src/custody/installation_fence.rs', 'installation_fence_child_probe', 'OPENSIP_TEST_FENCE341_CARRIER')
        self.assertIn(key, calls)
        self.assertFalse(test_only[key])


    def test_a_production_inclusion_of_an_allowed_test_file_is_caught(self):
        # The test inclusion stays; a second, production-reachable inclusion is added.
        work = self.copy()
        path = work / 'crates/security/src/custody/installation_routing.rs'
        path.write_text(path.read_text() + '\nmod leaked {\n    include!("installation_routing_tests.rs");\n}\n')
        calls, _, test_only = scan(work)
        key = ('crates/security/src/custody/installation_routing_tests.rs',
               'a_development_build_ends_at_f0_with_no_notice_and_no_installation_path', 'HOME')
        self.assertIn(key, calls)
        self.assertFalse(test_only[key])

    def test_a_production_inclusion_of_an_integration_test_file_is_caught(self):
        # An integration-test entry point stays one, and a production file also includes it.
        work = self.copy()
        path = work / 'crates/host/src/lib.rs'
        path.write_text(path.read_text() + '\nmod leaked_integration {\n    include!("../tests/admission_tests.rs");\n}\n')
        calls, _, test_only = scan(work)
        key = ('crates/host/tests/admission_tests.rs', 'rustc_path', 'RUSTC')
        self.assertIn(key, calls)
        self.assertFalse(test_only[key])
        # Without that inclusion the same file is test code.
        _, _, untouched = scan(ROOT)
        self.assertTrue(untouched[key])

    def test_include_text_in_comments_and_literals_is_no_edge(self):
        work = self.copy()
        path = work / 'crates/security/src/custody/installation_routing.rs'
        path.write_text(path.read_text() + '\n// include!("read_premise_tests.rs");\nconst _X: &str = "include!(\\"read_premise_tests.rs\\")";\n')
        calls, _, test_only = scan(work)
        key = ('crates/security/src/custody/read_premise_tests.rs',
               'a_development_build_ends_in_the_no_embedded_release_row', 'HOME')
        self.assertTrue(test_only[key])


if __name__ == '__main__':
    unittest.main()

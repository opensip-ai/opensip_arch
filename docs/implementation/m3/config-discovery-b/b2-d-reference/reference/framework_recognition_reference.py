"""B2-d0: the framework recognition reference (M3-B r9 item 16; B2-d plan r3 section 1). PROPOSED, design reference only.

The selected native reference (contract successor 81, `b-s9/reference/native_evidence_model.py`) holds NE section 8's
`recognize_frameworks` and `FRAMEWORK_HINTS`. This module makes it the current oracle WITHOUT editing a byte of the
model. It loads the model at its accepted bytes, with its loading closure pinned, calls `recognize_frameworks`
unchanged, and applies exactly the plan's five changes to the result:

  1. `Cargo.toml` is parsed, not matched by regex: the model's `cargo-workspace` and `cargo-package` results are
     replaced by ones decided on the parsed document (a `workspace` table; a `package` table) under `parse_toml`'s
     profile (4 MiB, UTF-8 without a BOM, at most 1,000,000 value nodes counted as its walk counts). Every parse error
     gives one disclosure: recognizer `cargo-package`, `assurance: inferred`, field `<unparseable>`, the `target/`
     convention, `unresolvedChoices: ["Cargo.toml-not-toml"]`, and the Cargo-workspace fact unknown. The `toml`
     crate's own recursion limit has no `tomllib` equal: the one labelled product-bound divergence (product-only
     controls).
  2. `tsconfig.json` / `jsconfig.json` (the file the model selects) is parsed by item 14a's JSONC reading, the one
     B2-c2 was accepted against (archived `b2-c2-r2/product/tools/host/typescript_config_vectors.py`, `parse_jsonc`),
     within item 14a's 64 KiB file bound. A failure makes the result `assurance: inferred` with
     `unresolvedChoices: ["tsconfig-not-jsonc"]`; its effects stay empty.
  3. `pnpm-workspace.yaml` is read by the closed YAML subset (`parse_pnpm_packages` below). Inside it the model's
     result is unchanged; outside it the result carries FR-1's disclosure, `["config-requires-evaluation"]`, and no
     effect.
  4. FR-4 and FR-2. A bound validator checks every result (32 recognizers per unit, 64 evidence files per
     recognizer). The entry-point bound is per unit and all or nothing: one past 65,536 distinct entries across the
     unit's results, no result emits entry points and each entry-bearing result carries `entry-points-over-bound`.
     The bound holds under an explicit override too. Explicit entry points (the resolved `discovery.entryPoints`
     won by a carrier, `[]` included) set the unit's `entryPoints` to `{state: all, source: explicit}`; absence (no
     field) leaves recognition to decide.
  5. The `entryPoints.state` rule: `partial` when any result carries an unresolved choice, otherwise `all` when any
     result has entry points, otherwise `none`.

Inputs are bytes, as the product reads them: `files` maps unit-root-relative paths to file bytes. The model takes text,
so each file is handed to it as its UTF-8 decoding; a `package.json` that is not UTF-8 is handed over as `""`, which
the model's exact JSON admission refuses (the product's `parse_json` refuses invalid UTF-8). Every evidence
`contentSha256` is then taken over the file's bytes, which equals the model's own hash for UTF-8 files. Paths stay
unit-root-relative (B2-d plan r3 Q2; FR-6 to FR-8 are not applied).

Design evidence: supplied synthetic inputs only; no filesystem tree, product code or qualification.
"""
from __future__ import annotations

import copy
import hashlib
import re
import sys
import tomllib
from pathlib import Path

NATIVE = 'docs/coop/design-corrections/native/'
# The selected model (contract successor 81) and its loading closure: path, bytes, SHA-256 (as B2-c0 pins them).
MODEL = ('docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py', 320462, 'a7e40715ce9b204f3ba562ffda69ccd542f3ca6096dd3a78d257b3e62f8c874b')
CLOSURE = (
    ('docs/coop/design-corrections/foundation/canonical.py', 6465, 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442'),
    ('docs/coop/design-corrections/foundation/identity-model.py', 135671, '12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6'),
    ('docs/coop/design-corrections/discovery-defaults.py', 22344, 'f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c'),
    (NATIVE + 'native-evidence.schemas.v2.json', 277967, '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043'),
    (NATIVE + 'native-capability-matrix.v2.json', 36595, '4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14'),
)
# Item 14a's JSONC reading, as B2-c2 r2 was accepted against it (the archived product copy).
JSONC = ('docs/implementation/m3/config-discovery-b/b2-c2-r2/product/tools/host/typescript_config_vectors.py', 40544, '16bae18acb04feb85420c2bee254c9d3f64fdd4e5c5cf41a77c80f4c161d4485')

DOMAIN = 'native.framework-recognition.v1'
RECOGNIZER_VERSION = 1
MAX_RECOGNIZERS = 32
MAX_EVIDENCE = 64
MAX_ENTRY_POINTS = 65536
# parse_toml's profile (crates/identity/src/toml.rs, canonical.rs MAX_BYTES).
TOML_MAX_BYTES = 4 * 1024 * 1024
TOML_MAX_NODES = 1_000_000
# The YAML subset's own bound (B2-d plan r3 section 2).
YAML_MAX_BYTES = 64 * 1024
CONFIG_REQUIRES_EVALUATION = 'config-requires-evaluation'
CARGO_NOT_TOML = 'Cargo.toml-not-toml'
TSCONFIG_NOT_JSONC = 'tsconfig-not-jsonc'
ENTRY_POINTS_OVER_BOUND = 'entry-points-over-bound'


def pinned(arch: Path, row) -> Path:
    path, size, digest = row
    raw = (arch / path).read_bytes()
    if (size is not None and len(raw) != size) or (digest is not None and hashlib.sha256(raw).hexdigest() != digest):
        raise ValueError('pin mismatch: ' + path)
    return arch / path


def _module_at(name: str, source: Path, located: Path):
    import importlib.util
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(located))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(located)
    exec(compile(source.read_bytes(), str(located), 'exec'), module.__dict__)
    return module


class Reference:
    """The loaded model and the JSONC reading, with the reference's entry points."""

    def __init__(self, model, jsonc):
        self.model, self.jsonc = model, jsonc

    # ------------------------------------------------------------------ change 1: Cargo.toml parsed on parse_toml's profile

    def parse_cargo(self, raw: bytes):
        """The parsed document, or None for every parse error (syntax, UTF-8, BOM, byte cap, node limit)."""
        if len(raw) > TOML_MAX_BYTES:
            return None
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            return None
        if text.startswith('﻿'):
            return None
        # r2 (B2D0REF-R1-RF-3): parse_toml keeps integer literals unnarrowed, so Python's decimal-digit conversion
        # limit (4300 by default) is lifted for the parse; the byte and node bounds above and below still hold.
        limit = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(0)
        try:
            doc = tomllib.loads(text)
        except (tomllib.TOMLDecodeError, RecursionError, ValueError):
            return None
        finally:
            sys.set_int_max_str_digits(limit)
        # parse_toml's walk: every value below the root table counts one node; arrays and tables push children.
        pending = list(doc.values())
        remaining = TOML_MAX_NODES
        while pending:
            value = pending.pop()
            remaining -= 1
            if remaining < 0:
                return None
            if isinstance(value, list):
                pending.extend(value)
            elif isinstance(value, dict):
                pending.extend(value.values())
        return doc

    def cargo_workspace_fact(self, raw: bytes):
        """`MarkerFact.is_cargo_workspace`: True or False on a parsed `Cargo.toml`, None (unknown) on a parse error."""
        doc = self.parse_cargo(raw)
        if doc is None:
            return None
        return isinstance(doc.get('workspace'), dict)

    # ------------------------------------------------------------------ change 2: tsconfig / jsconfig as item 14a's JSONC

    def jsonc_ok(self, raw: bytes) -> bool:
        if len(raw) > self.jsonc.MAX_BYTES:
            return False
        try:
            self.jsonc.parse_jsonc(raw)
        except self.jsonc.Malformed:
            return False
        return True

    # ------------------------------------------------------------------ the recognizers

    def recognize(self, files: dict[str, bytes], explicit_entry_points=None) -> dict:
        """`FrameworkRecognitionV1` for one unit. `explicit_entry_points` is None when the resolved configuration has no
        `discovery.entryPoints` field, else that list (possibly empty)."""
        texts = {}
        for path, raw in files.items():
            try:
                texts[path] = raw.decode('utf-8')
            except UnicodeDecodeError:
                texts[path] = ''  # presence for the model; package.json's exact admission refuses ''
        result = self.model.recognize_frameworks(texts)
        recognized = [r for r in result['recognized'] if r['recognizerId'] not in ('cargo-workspace', 'cargo-package')]
        hints = result['observedHints']

        def ev(path, field):
            return {'path': path, 'contentSha256': hashlib.sha256(files[path]).hexdigest(), 'field': field}

        def effects(entry=None, tests=None, ignore=None):
            return {'entryPoints': entry or [], 'testGlobs': tests or [], 'ignoreConventions': ignore or []}

        # Every retained evidence hash over the file's bytes (equal to the model's own for UTF-8 files).
        for r in recognized:
            for e in r['evidence']:
                e['contentSha256'] = hashlib.sha256(files[e['path']]).hexdigest()
        # Change 1.
        if 'Cargo.toml' in files:
            doc = self.parse_cargo(files['Cargo.toml'])
            if doc is None:
                recognized.append({'recognizerId': 'cargo-package', 'recognizerVersion': RECOGNIZER_VERSION, 'evidence': [ev('Cargo.toml', '<unparseable>')],
                                   'assurance': 'inferred', 'effects': effects(ignore=['target/']), 'unresolvedChoices': [CARGO_NOT_TOML]})
            else:
                if isinstance(doc.get('workspace'), dict):
                    recognized.append({'recognizerId': 'cargo-workspace', 'recognizerVersion': RECOGNIZER_VERSION, 'evidence': [ev('Cargo.toml', 'workspace.members')],
                                       'assurance': 'declared', 'effects': effects(ignore=['target/']), 'unresolvedChoices': []})
                if isinstance(doc.get('package'), dict):
                    entry = [p for p in ('src/main.rs', 'src/lib.rs') if p in files]
                    recognized.append({'recognizerId': 'cargo-package', 'recognizerVersion': RECOGNIZER_VERSION, 'evidence': [ev('Cargo.toml', 'package/lib/bin')],
                                       'assurance': 'declared', 'effects': effects(entry=entry, ignore=['target/']), 'unresolvedChoices': []})
        # Changes 2 and 3.
        for r in recognized:
            if r['recognizerId'] == 'typescript-config' and not self.jsonc_ok(files[r['evidence'][0]['path']]):
                r['assurance'] = 'inferred'
                r['unresolvedChoices'] = [TSCONFIG_NOT_JSONC]
            if r['recognizerId'] == 'pnpm-workspace':
                try:
                    parse_pnpm_packages(files['pnpm-workspace.yaml'])
                except OutsideSubset:
                    r['effects'] = effects()
                    r['unresolvedChoices'] = [CONFIG_REQUIRES_EVALUATION]
        recognized.sort(key=lambda r: r['recognizerId'])
        # Change 4: the bound validator, then the per-unit entry bound (always, an explicit override included).
        bound_check(recognized)
        entry_bound(recognized)
        # Change 5 (and FR-2's explicit override).
        if explicit_entry_points is not None:
            entry_points = {'state': 'all', 'source': 'explicit'}
        elif any(r['unresolvedChoices'] for r in recognized):
            entry_points = {'state': 'partial', 'source': 'recognized'}
        elif any(r['effects']['entryPoints'] for r in recognized):
            entry_points = {'state': 'all', 'source': 'recognized'}
        else:
            entry_points = {'state': 'none', 'source': 'none'}
        out = {'schemaVersion': 1, 'recognized': recognized, 'observedHints': hints, 'entryPoints': entry_points}
        self.model.validate_native('FrameworkRecognitionV1', out)
        return out

    def unit_recognition(self, unit_ordinal: int, root_path: str, marker_path: str, recognition: dict) -> dict:
        """`UnitRecognitionV1`, its `recognitionId` the derived h-identity `closure.rs` checks."""
        return {'unitOrdinal': unit_ordinal, 'rootPath': root_path, 'markerPath': marker_path,
                'recognitionId': 'sha256:' + self.model.C.identity(DOMAIN, recognition), 'recognition': recognition}


def discovered_provenance(result: dict) -> str:
    """FR-2's provenance for a recognized result's effects: `DISCOVERED:<recognizerId>@<recognizerVersion>`."""
    return 'DISCOVERED:%s@%d' % (result['recognizerId'], result['recognizerVersion'])


def bound_check(recognized: list) -> None:
    """FR-4's two structural bounds, on any list of results."""
    if len(recognized) > MAX_RECOGNIZERS:
        raise ValueError('maxRecognizersPerUnit exceeded')
    for r in recognized:
        if not 1 <= len(r['evidence']) <= MAX_EVIDENCE:
            raise ValueError('maxEvidenceFilesPerRecognizer exceeded')


def entry_bound(recognized: list) -> None:
    """FR-4's per-unit entry-point bound, all or nothing over the distinct union of every result's entry points."""
    union = {p for r in recognized for p in r['effects']['entryPoints']}
    if len(union) > MAX_ENTRY_POINTS:
        for r in recognized:
            if r['effects']['entryPoints']:
                r['effects']['entryPoints'] = []
                r['unresolvedChoices'] = r['unresolvedChoices'] + [ENTRY_POINTS_OVER_BOUND]


# ------------------------------------------------------------------ the closed YAML subset (B2-d plan r3 section 2)

class OutsideSubset(Exception):
    pass


_INDICATORS = set('-?:,[]{}#&*!|>\'"%@`')
# Plain scalars a YAML parser would not read as a string (YAML 1.1 and 1.2 null, booleans, infinities, numbers and
# dates): outside the subset rather than guessed.
_RESERVED = {'', '~', 'null', 'true', 'false', 'yes', 'no', 'on', 'off', 'y', 'n', '.inf', '-.inf', '+.inf', '.nan'}
_NUMERIC = re.compile(r'[-+]?(?:[0-9][0-9a-fA-FxXoObB_.:eE+-]*|\.[0-9][0-9_eE+-]*)')
_DATE = re.compile(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}(?:[Tt ].*)?')


def _scalar(rest: str) -> str:
    """One scalar and an optional trailing comment (whitespace, then `#`)."""
    def tail(after: str) -> None:
        if after and not re.fullmatch(r' +#.*', after):
            raise OutsideSubset('text after a quoted scalar')
    if rest.startswith("'"):
        out, i = [], 1
        while True:
            j = rest.find("'", i)
            if j < 0:
                raise OutsideSubset('unterminated single quote')
            out.append(rest[i:j])
            if rest[j + 1:j + 2] == "'":
                out.append("'")
                i = j + 2
                continue
            tail(rest[j + 1:])
            return ''.join(out)
    if rest.startswith('"'):
        out, i = [], 1
        while i < len(rest):
            ch = rest[i]
            if ch == '\\':
                nxt = rest[i + 1:i + 2]
                if nxt not in ('"', '\\'):
                    raise OutsideSubset('escape outside the subset')
                out.append(nxt)
                i += 2
                continue
            if ch == '"':
                tail(rest[i + 1:])
                return ''.join(out)
            out.append(ch)
            i += 1
        raise OutsideSubset('unterminated double quote')
    comment = rest.find(' #')
    value = (rest if comment < 0 else rest[:comment]).rstrip(' ')
    if not value or value[0] in _INDICATORS or ':' in value or value.lower() in _RESERVED:
        raise OutsideSubset('plain scalar outside the subset')
    if _NUMERIC.fullmatch(value) or _DATE.fullmatch(value):
        raise OutsideSubset('plain scalar a YAML parser would not read as a string')
    return value


def _yaml_character_ok(ch: str) -> bool:
    """The subset's characters (r2, B2D0REF-R1-RF-2): YAML 1.2's c-printable set, less TAB, CR (only as CRLF, handled
    before this check), DEL, the C1 block, NEL (U+0085), the line and paragraph separators (U+2028, U+2029), which the
    subset does not treat as breaks, and the byte order mark anywhere."""
    o = ord(ch)
    if ch == '\n' or 0x20 <= o <= 0x7E:
        return True
    if 0xA0 <= o <= 0xD7FF:
        return o not in (0x2028, 0x2029)
    if 0xE000 <= o <= 0xFFFD:
        return o != 0xFEFF
    return 0x10000 <= o <= 0x10FFFF


def parse_pnpm_packages(raw: bytes) -> list[str]:
    """The `packages:` globs of a `pnpm-workspace.yaml` inside the closed subset; `OutsideSubset` otherwise, never a
    partial list."""
    if len(raw) > YAML_MAX_BYTES:
        raise OutsideSubset('over the bound')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise OutsideSubset('not UTF-8')
    if text.startswith('﻿') or '\t' in text:
        raise OutsideSubset('BOM or tab')
    # r3 (B2D0REF-R2-RF-2): only CRLF pairs are line breaks; any other CR, at the end of input included, is outside.
    text = text.replace('\r\n', '\n')
    if '\r' in text:
        raise OutsideSubset('bare carriage return')
    lines = text.split('\n')
    if not all(_yaml_character_ok(ch) for ch in '\n'.join(lines)):
        raise OutsideSubset('a character outside the subset')
    state, indent, out = 'before', None, []
    for line in lines:
        stripped = line.lstrip(' ')
        if stripped == '' or stripped.startswith('#'):
            continue
        if state == 'before':
            if re.fullmatch(r'packages:( +#.*)?', line):
                state = 'block'
                continue
            # r3 (B2D0REF-R2-RF-1): the empty flow sequence is separated from the key by at least one space.
            if re.fullmatch(r'packages: +\[\] *( +#.*)?', line):
                state = 'closed'
                continue
            raise OutsideSubset('not the packages key')
        if state == 'closed':
            raise OutsideSubset('content after an empty flow sequence')
        m = re.fullmatch(r'( +)- +(.*)', line)
        if m is None:
            raise OutsideSubset('not a block sequence item')
        if indent is None:
            indent = len(m.group(1))
        elif len(m.group(1)) != indent:
            raise OutsideSubset('inconsistent indentation')
        out.append(_scalar(m.group(2)))
    if state == 'before':
        raise OutsideSubset('no packages key')
    if state == 'block' and not out:
        # r2 (B2D0REF-R1-RF-1): a bare key (or one followed by comments only) is a null value, not a sequence.
        raise OutsideSubset('packages is null, not a sequence')
    return out


def load(arch: Path, packages: Path | None = None) -> Reference:
    """`packages`: the provisioned python-packages snapshot the model's foundation imports (as B2-c0 takes it)."""
    arch = Path(arch)
    for row in CLOSURE:
        pinned(arch, row)
    if packages is not None and str(packages) not in sys.path:
        sys.path.insert(0, str(packages))
    model = _module_at('framework_recognition_model', pinned(arch, MODEL), arch / NATIVE / 'native_evidence_model.py')
    import importlib.util
    path = pinned(arch, JSONC)
    spec = importlib.util.spec_from_file_location('typescript_config_reading', path)
    jsonc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(jsonc)
    return Reference(model, jsonc)


if __name__ == '__main__':
    sys.exit('library module: see ../evidence/check.py')

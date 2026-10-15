"""Reproduce the host configuration resolver's generated registries (M3-B r4 item 8; unit B1-a).

Developer tool only: no Cargo build hook, runtime input, network or environment input. It reads the
architecture inputs at their accepted bytes (approval source manifest v45) and two product files, and
writes or checks exactly one product file, crates/host/src/configuration_tables.rs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile

OUTPUT = 'crates/host/src/configuration_tables.rs'
# Architecture inputs: path, bytes, SHA-256 (each a member of candidate-subject.v45.json).
ARCH = (
    ('docs/coop/design-corrections/native/native-capability-matrix.v2.json', 36595,
     '4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14'),
    ('docs/coop/design-corrections/workflows/command-inventory.v3.json', 66800,
     'd303cc640154ff2b4473452c52f6578b5ffa3f20d6ed03c3976e0ddd397a4e66'),
    ('docs/v2/contracts/product-v1/admission-and-qualification.md', 27301,
     '69cd6ba3cb41ed191e0a4e5cc20b191f4b8761625843b585426157873dbee6b3'),
)
# Product inputs: the pinned PCS and identity-v3 sources (SOURCE_PINS) and the reviewed mapping.
PCS = ('schemas/sources/product-configuration-v2.schema.json', 10262,
       '591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d')
IDS = 'schemas/sources/identity-v3.schema.json'
CLASSES = 'crates/host/src/configuration_classes.json'
CLASS_NAMES = ('host.analysis.semantic', 'host.operability.nonsemantic')
LAYERS = ('defaults', 'global', 'project', 'local', 'flags')
FLAG_CLASSES = ('authorization', 'selection')
RUSTFMT_VERSION = 'rustfmt 1.9.0'  # as tools/security/inputs/sources.json pins it


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(root, path, size, digest):
    raw = (root / path).read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'input pin mismatch: ' + path)
    return raw


def decode(raw, name):
    def pairs(items):
        keys = [k for k, _ in items]
        require(len(keys) == len(set(keys)), 'duplicate key in ' + name)
        return dict(items)
    return json.loads(raw, object_pairs_hook=pairs)


def variant(spelling):
    words = re.split(r'[^A-Za-z0-9]+', spelling)
    name = ''.join(w[:1].upper() + w[1:] for w in words if w)
    require(re.fullmatch(r'[A-Z][A-Za-z0-9]*', name or ''), 'no Rust variant for ' + spelling)
    return name


def leaves(schema, name):
    """Second-level properties of every section of a closed object schema (the resolver's merge leaves)."""
    out = []
    for section, record in schema['properties'].items():
        if section == 'schemaVersion':
            continue
        require(record.get('type') == 'object' and record.get('additionalProperties') is False, name + ' section not closed: ' + section)
        out += [section + '.' + field for field in record['properties']]
    return out


def tables(arch, product):
    ncm, cinv, aq = (pinned(arch, *row) for row in ARCH)
    pcs = decode(pinned(product, *PCS), PCS[0])
    ids = decode((product / IDS).read_bytes(), IDS)
    classes_raw = (product / CLASSES).read_bytes()
    classes = decode(classes_raw, CLASSES)
    require(set(classes) == {'schemaVersion', 'standing', 'source', 'rows'} and classes['schemaVersion'] == 1, 'mapping shape')
    require(classes['source'] == {'path': PCS[0], 'bytes': PCS[1], 'sha256': PCS[2]}, 'mapping source pin')
    rows = classes['rows']
    require(all(set(r) == {'leaf', 'class', 'layers'} for r in rows), 'mapping row shape')
    names = [r['leaf'] for r in rows]
    require(len(names) == len(set(names)), 'mapping has a duplicate leaf')
    require(names == leaves(pcs, 'PCS'), 'mapping rows differ from the PCS leaves, in PCS order')
    require(all(r['class'] in CLASS_NAMES for r in rows), 'class outside the DRC vocabulary')
    require(all(r['layers'] and r['layers'] == [x for x in LAYERS if x in r['layers']] for r in rows), 'layers unknown, empty or out of order')
    semantic = ids['$defs']['semantic-configuration']
    require([r['leaf'] for r in rows if r['class'] == 'host.analysis.semantic'] == leaves(semantic, 'semantic-configuration'),
            'semantic leaves differ from identity-v3 semantic-configuration')
    require(semantic['required'] == list(semantic['properties']), 'semantic sections not all required')

    matrix = decode(ncm, 'NCM')
    capabilities = [c['id'] for c in matrix['capabilities']]
    require(capabilities == matrix['capabilityIdLaw']['members'], 'NCM capability ids differ from its id law')
    modes = matrix['languageModes']
    cells = [(c['capability'], c['mode'], c['state']) for c in matrix['cells']]
    require(sorted((c, m) for c, m, _ in cells) == sorted((c, m) for c in capabilities for m in modes), 'NCM cells are not the complete product')
    require({s for _, _, s in cells} <= set(matrix['cellStates']), 'NCM cell state outside cellStates')
    not_selected = [(c, m) for c, m, s in cells if s == 'NOT-SELECTED']
    require(all(any((c, m) not in not_selected for m in modes) for c in capabilities), 'a capability has no selectable mode')

    flags = decode(cinv, 'CINV')['sharedFlags']
    require(len(flags) == 7 and all(set(f) == {'flag', 'owner', 'class', 'join'} and f['class'] in FLAG_CLASSES for f in flags), 'CINV shared flags')

    line = aq.decode('utf-8').splitlines()[55]
    found = re.findall(r'supplies the `([a-z][a-z0-9._:-]*)` profile', line)
    require(len(found) == 1, 'AQ:56 profile spelling')
    profiles = found

    out = ['//! Generated by `tools/host/generate_configuration_tables.py` from pinned inputs; do not edit.',
           '//! `--check` is the drift check (M3-B r4 item 8). Inputs, by SHA-256:']
    out += [f'//! - `{p}` `{d}`' for p, _, d in ARCH]
    out += [f'//! - `{PCS[0]}` `{PCS[2]}`', f'//! - `{CLASSES}` `{hashlib.sha256(classes_raw).hexdigest()}`', '']

    def enum(doc, name, spellings, extra=''):
        body = [f'/// {doc}', '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]', f'pub(crate) enum {name} {{']
        body += [f'    {variant(s)},' for s in spellings]
        body += ['}', f'impl {name} {{', f'    pub(crate) const ALL: [Self; {len(spellings)}] = [']
        body += [f'        Self::{variant(s)},' for s in spellings]
        body += ['    ];', '    pub(crate) fn as_str(self) -> &\'static str {', '        match self {']
        body += [f'            Self::{variant(s)} => "{s}",' for s in spellings]
        body += ['        }', '    }', '    pub(crate) fn parse(spelling: &str) -> Option<Self> {',
                 '        Self::ALL.into_iter().find(|v| v.as_str() == spelling)', '    }']
        body += [extra] if extra else []
        return body + ['}', '']

    out += ['/// AQ:56: the one registered profile at M3 (B1-a plan r2 section 3).',
            f'pub(crate) const PROFILE_IDS: [&str; {len(profiles)}] = [' + ', '.join(f'"{p}"' for p in profiles) + '];', '']
    out += enum('NCM `#/capabilities[].id`, in matrix order: the configured capability vocabulary.', 'CapabilityId', capabilities)
    out += enum('NCM `#/languageModes`, in matrix order.', 'LanguageMode', modes)
    out += ['/// NCM cells whose state is `NOT-SELECTED`. Judged per (capability, mode) when the analysis spec',
            '/// is built (NE:1005-1013, NE:3577), not by the resolver.',
            f'pub(crate) const NOT_SELECTED_CELLS: [(CapabilityId, LanguageMode); {len(not_selected)}] = [']
    out += [f'    (CapabilityId::{variant(c)}, LanguageMode::{variant(m)}),' for c, m in not_selected]
    out += ['];', '']
    flag_class = ['    pub(crate) fn class(self) -> SharedFlagClass {', '        match self {']
    flag_class += [f'            Self::{variant(f["flag"])} => SharedFlagClass::{variant(f["class"])},' for f in flags]
    flag_class += ['        }', '    }']
    out += enum('CINV `sharedFlags`, the seven shared flags, in inventory order.', 'SharedFlag', [f['flag'] for f in flags], '\n'.join(flag_class))
    out += enum('CINV shared-flag classes.', 'SharedFlagClass', list(FLAG_CLASSES))
    out += enum('DRC:588-589, the closed configuration classification vocabulary.', 'FieldClass', list(CLASS_NAMES))
    out += enum('The admitting layers of the reviewed mapping (M3-B r4 item 2); the environment admits nothing.', 'Layer', LAYERS)
    out += ['/// The reviewed mapping: every PCS leaf as (section, field, class, admitting layers), in PCS order.',
            f'pub(crate) const FIELDS: [(&str, &str, FieldClass, &[Layer]); {len(rows)}] = [']
    for r in rows:
        section, field = r['leaf'].split('.')
        layers = ', '.join('Layer::' + variant(x) for x in r['layers'])
        out.append(f'    ("{section}", "{field}", FieldClass::{variant(r["class"])}, &[{layers}]),')
    out += ['];']
    return ('\n'.join(out) + '\n').encode()


def formatted(raw, formatter):
    version = subprocess.check_output([formatter, '--version'], text=True).strip()
    require(version == RUSTFMT_VERSION, 'formatter version mismatch: ' + version)
    with tempfile.TemporaryDirectory(prefix='opensip-configuration-tables-') as tmp:
        path = Path(tmp) / Path(OUTPUT).name
        path.write_bytes(raw)
        subprocess.run([formatter, '--edition', '2024', str(path)], check=True, capture_output=True)
        return path.read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output from verified inputs')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the pinned inputs')
    parser.add_argument('--rustfmt', default='rustfmt', help='path to the pinned Rust formatter')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent.parent
    raw = formatted(tables(args.architecture.resolve(strict=True), root), args.rustfmt)
    target = root / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'generated output differs: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from pinned inputs.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError, OSError, subprocess.CalledProcessError) as error:
        print(f'Configuration table generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)

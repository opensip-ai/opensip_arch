"""Portable entry-point support for the author construction scripts.

Replaces three historical non-portable dependencies with declared arguments:

  * `sys.path.insert(0, ROOT/'output')` + `from helpers import ...`
      -> the helpers package BUNDLED in the author package (`author-helpers/`) is loaded
         under the module name `helpers`, so the construction bodies are unchanged. An
         optional `--helpers` overlay directory may be named instead.
  * `F = ROOT.parent/'candidate-subject.v25/docs/coop/design-corrections/foundation'`
      -> `--source`, any reference source root.
  * `T = load(..., ROOT.parent/'check-blind13-exported-graphs.v4.py')` (absent everywhere)
      -> the BUNDLED `check-export.v4.py`, whose `decode_store(raw, M, transport_notes=None)`
         is the same transport entry the missing module supplied.

Outputs go to `--out`, never into the source or package tree. No /tmp working history and no
agent session path is required or consulted.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

HELPERS_DIRNAME = 'author-helpers'
TRANSPORT_NAME = 'check-export.v4.py'


def arguments(description, extra=()):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--source', required=True, type=Path,
                   help='reference source root (the tree holding docs/coop/design-corrections)')
    p.add_argument('--package', required=True, type=Path,
                   help='author package root (bundled author-helpers/ and check-export.v4.py)')
    p.add_argument('--out', required=True, type=Path,
                   help='fresh output directory; must not already exist')
    p.add_argument('--helpers', type=Path, default=None,
                   help='optional helpers overlay directory (default: <package>/author-helpers)')
    p.add_argument('--kit', type=Path, default=None,
                   help='schema-document kit root the helpers read registered documents from '
                        '(default: --source). This is what binds the construction to the '
                        'REGISTERED native schema digest.')
    for name, kw in extra:
        p.add_argument(name, **kw)
    a = p.parse_args()
    a.source = a.source.resolve()
    a.package = a.package.resolve()
    a.out = a.out.resolve()
    if a.helpers is not None:
        a.helpers = a.helpers.resolve()
    a.kit = a.kit.resolve() if a.kit is not None else a.source
    for label, path in (('--source', a.source), ('--package', a.package), ('--kit', a.kit)):
        if not path.is_dir():
            raise SystemExit('%s is not a directory: %s' % (label, path))
    inputs = [a.source, a.package, a.kit, a.helpers or a.package / HELPERS_DIRNAME]
    for path in inputs:
        path = path.resolve()
        if a.out == path or a.out.is_relative_to(path) or path.is_relative_to(a.out):
            raise SystemExit('--out must be separate from every declared input: %s' % path)
    return a


def foundation(source):
    f = source / 'docs/coop/design-corrections/foundation'
    if not f.is_dir():
        raise SystemExit('--source does not hold docs/coop/design-corrections/foundation: %s' % source)
    return f


def load_module(name, path):
    path = Path(path)
    if not path.is_file():
        raise SystemExit('required module missing: %s' % path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_helpers(package, helpers=None, name='helpers', kit=None, out=None):
    """Bind the BUNDLED helpers package under the plain name `helpers`.

    The directory ships as `author-helpers`, which is not an importable identifier, so it is
    registered explicitly with its own search path. Construction bodies keep saying
    `from helpers import runs, builder, h, order, store` unchanged.

    The helpers read their registered schema documents from a kit root at IMPORT time, so the
    declared kit is published to the environment BEFORE the package is executed. With the
    portability overlay those constants resolve from the environment and default to their
    historical values; without it they keep their historical values and this is a no-op.
    """
    if kit is not None:
        os.environ['OPENSIP_AUTHOR_KIT'] = str(kit)
    if out is not None:
        os.environ['OPENSIP_AUTHOR_OUT'] = str(out)
    d = Path(helpers) if helpers is not None else Path(package) / HELPERS_DIRNAME
    init = d / '__init__.py'
    if not init.is_file():
        raise SystemExit('helpers package missing: %s' % init)
    spec = importlib.util.spec_from_file_location(name, init, submodule_search_locations=[str(d)])
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def transport(package, name='author_transport'):
    """The bundled export transport; supplies decode_store(raw, M, transport_notes=None)."""
    return load_module(name, Path(package) / TRANSPORT_NAME)


def fresh_out(out):
    if out.exists():
        raise SystemExit('--out already exists; use a new directory so evidence is not overwritten: %s' % out)
    out.mkdir(parents=True)
    return out


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def registered_native_schema_digest(source):
    return sha256_file(Path(source) / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')


def provenance(a, extra=None):
    """The exact inputs this construction was bound to, written beside every output."""
    row = {
        'standing': 'AUTHOR-assisted construction. Not independent reconstruction, not blind '
                    'acceptance, not product qualification. Do not supply to a blind consumer.',
        'source': str(a.source),
        'package': str(a.package),
        'helpers': str(a.helpers) if a.helpers is not None else str(a.package / HELPERS_DIRNAME),
        'kit': str(a.kit),
        'out': str(a.out),
        'registeredNativeSchemaSha256': registered_native_schema_digest(a.source),
        'kitNativeSchemaSha256': registered_native_schema_digest(a.kit),
        'transport': TRANSPORT_NAME,
    }
    if extra:
        row.update(extra)
    return row


def write_provenance(a, extra=None):
    row = provenance(a, extra)
    (a.out / 'construction-provenance.json').write_text(json.dumps(row, indent=2) + '\n')
    return row

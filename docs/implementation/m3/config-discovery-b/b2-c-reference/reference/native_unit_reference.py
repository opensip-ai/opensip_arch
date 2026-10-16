"""B2-c0: the current native unit reference (M3-B r7 item 14; B2-c plan r2 section 1). PROPOSED, design reference only.

The selected native reference (contract successor 81, `b-s9/reference/native_evidence_model.py`) holds U-0 to U-9:
`admit_unit_roots`, `discover_units`, `assign_membership`, `unit_scope_descriptor`, `typescript_mode` and
`default_capability_selection`. It predates the B2-a shared rule (successor 163) and B-S1's version 3. This module makes
it the current oracle WITHOUT editing a byte of the model:

  * `load(arch, packages)` executes the model's accepted bytes with `__file__` at the directory its sibling imports
    name, `docs/coop/design-corrections/native/` (the B-S9 copy's own directory holds none of them; plan r2 NBO-1). Its
    whole loading closure is pinned: the two foundation modules, the schema bundle, the capability matrix, and the
    historical shared rule the model binds at load. It returns the historical module, unchanged, and `Current`: a second
    load of the same bytes after four documented substitutions of module globals, each needed by B-S1 or
    B2-a and nothing else (the model resolves each by name at call time):
      - `DD` is the B2-a rule (`discovery-defaults.sx1-r1.py`), bound to the admitted inventory's member roots for the
        duration of a call, so SX-1's `.opensip` anchor is pruned at the root and at each member root;
      - `admit_current_boundary_inventory` admits `AdmittedBoundaryInventoryV3` only, validated against B-S1's schema
        (the merged bundle below); V1 and V2 refuse on the current lane, as V1 did when V2 became current;
      - `validate_native` defers the model's own `UnitDiscoveryV2` output validation to this module, which validates
        the projected `UnitDiscoveryV3` instead; every other definition validates as before, in the merged bundle;
      - `_boundaries_out` also emits `memberRepositories`, so its result is B-S1's `UnitBoundariesV2`.
  * LD-B2C0-1 (the current composition): a marker whose derived pruned anchor is at or below an admitted boundary (a nested
    repository, a nested project, or a directory-custody or DEPTH exclusion; r1 RF-1) is withheld from the model's anchor
    derivation. S3 records nested repositories and projects and never enters them (SL:146-168), so the
    walker's inventory (B2-b0) carries no anchor inside one; comparing such a derived anchor would refuse every project
    whose nested repository holds `node_modules`. The historical join sweep passed only because SLM over-observed.
  * The current entry points (`discover_units`, `assign_membership`, `unit_scope_descriptor`) wrap the model's and add
    B-S1's U-8 member rules: a member is not a boundary (the model never sees it as one, so its contents are ordinary
    directories); a `vcs-tree` anchor `D/<marker>` that the model derived or the inventory carries, with D strictly
    below the root and not at or below an admitted boundary (the same full predicate), refuses `native.boundary-inventory-mismatch` unless D is
    in `memberRepositories`. A non-refused discovery result validates as `UnitDiscoveryV3`.

The merged schema bundle is the base native bundle with B-S1's `$defs` ADDED under the same keys (its merge rule: no base
member replaced or removed). Design evidence: supplied synthetic inputs only; no filesystem tree, product code or
qualification.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path

NATIVE = 'docs/coop/design-corrections/native/'
# The selected model (contract successor 81) and its loading closure, path, bytes, SHA-256.
MODEL = ('docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py', 320462, 'a7e40715ce9b204f3ba562ffda69ccd542f3ca6096dd3a78d257b3e62f8c874b')
CLOSURE = (
    ('docs/coop/design-corrections/foundation/canonical.py', 6465, 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442'),
    ('docs/coop/design-corrections/foundation/identity-model.py', 135671, '12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6'),
    ('docs/coop/design-corrections/discovery-defaults.py', 22344, 'f30b68502b6fb70992eb4e9fe4dbd6919df69180e020d6f2e1538f7fa8cfb28c'),
    (NATIVE + 'native-evidence.schemas.v2.json', 277967, '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043'),
    (NATIVE + 'native-capability-matrix.v2.json', 36595, '4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14'),
)
RULE = ('docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py', 25293, '4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8')
B_S1 = ('docs/implementation/m3/config-discovery-b/b-s1/schemas/native-evidence.schemas.v2.b-s1-additions.json', 9930, '8c0255aab90c4d3c6550f0ea0e37dd1b3bfb6b1487c47bfd166357f81624b51a')
VCS_MARKERS = ('.git', '.hg', '.svn', '.jj')


def pinned(arch: Path, row) -> Path:
    path, size, digest = row
    raw = (arch / path).read_bytes()
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('pin mismatch: ' + path)
    return arch / path


def _module_at(name: str, source: Path, located: Path):
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(located))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(located)
    exec(compile(source.read_bytes(), str(located), 'exec'), module.__dict__)
    return module


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(arch: Path, packages: Path | None = None):
    """The historical model (as loaded) and the current one (the substitutions above), as two module objects."""
    arch = Path(arch)
    for row in CLOSURE:
        pinned(arch, row)
    if packages is not None and str(packages) not in sys.path:
        sys.path.insert(0, str(packages))
    source = pinned(arch, MODEL)
    historical = _module_at('native_unit_historical', source, arch / NATIVE / 'native_evidence_model.py')
    current = _module_at('native_unit_current', source, arch / NATIVE / 'native_evidence_model.py')
    rule = _module('native_unit_rule_sx1', pinned(arch, RULE))
    additions = json.loads(pinned(arch, B_S1).read_bytes())
    merged = copy.deepcopy(current.SCHEMAS)
    for key, value in additions['$defs'].items():
        if key in merged['$defs']:
            raise ValueError('B-S1 merge rule: base member replaced: ' + key)
        merged['$defs'][key] = value
    return historical, Current(current, rule, merged)


class _BoundRule:
    """The B2-a rule with `member_roots` defaulted to the current call's admitted members (SX-1 at member roots)."""

    def __init__(self, rule, members):
        self._rule, self._members = rule, tuple(members)

    def __getattr__(self, name):
        value = getattr(self._rule, name)
        if not callable(value) or isinstance(value, type):
            return value
        try:
            takes = 'member_roots' in inspect.signature(value).parameters
        except (TypeError, ValueError):
            takes = False
        if not takes:
            return value

        def call(*args, **kwargs):
            kwargs.setdefault('member_roots', self._members)
            return value(*args, **kwargs)
        return call


class Current:
    """The current native unit instrument: the model's entry points under B-S1 and B2-a."""

    def __init__(self, model, rule, merged):
        self.model, self.rule, self.merged = model, rule, merged
        self.members: tuple[str, ...] = ()
        self.deferred = []
        model.SCHEMAS = merged
        original_validate = model.validate_native

        def validate_native(def_name, value):
            if def_name == 'UnitDiscoveryV2':
                self.deferred.append(value)   # validated as UnitDiscoveryV3 by this module after projection
                return value
            return original_validate(def_name, value)

        def admit_current_boundary_inventory(boundaries):
            if not isinstance(boundaries, dict) or boundaries.get('schemaVersion') != 3:
                raise model.NativeRefusal('native.boundary-inventory-version-unsupported:%s' % (boundaries.get('schemaVersion') if isinstance(boundaries, dict) else None))
            original_validate('AdmittedBoundaryInventoryV3', boundaries)
            return boundaries

        original_out = model._boundaries_out

        def boundaries_out(boundaries, excluded_units):
            out = original_out(boundaries, excluded_units)
            out['memberRepositories'] = list(boundaries['memberRepositories']) if boundaries is not None else []
            return out

        model.validate_native = validate_native
        model.admit_current_boundary_inventory = admit_current_boundary_inventory
        model._boundaries_out = boundaries_out
        model.DD = _BoundRule(rule, ())
        self.validate = original_validate

    def __getattr__(self, name):
        return getattr(self.model, name)

    def _bind(self, boundaries):
        members = tuple(boundaries['memberRepositories']) if isinstance(boundaries, dict) and boundaries.get('schemaVersion') == 3 else ()
        self.model.DD = _BoundRule(self.rule, members)
        return members

    def _admitted_boundary(self, path, boundaries):
        """(anchor, reason) when `path` is at or below an admitted boundary: a nested repository, a nested project, or a
        directory-custody or DEPTH exclusion (r1, Codex B2C0REF-R1-RF-1). A marker-custody row excludes exactly its
        marker file, never a directory, so it never makes a path a boundary here (the selected `_boundary_hit` with no
        marker name)."""
        hit = self.rule.classify_boundary(path, boundaries['nestedRepositories'], boundaries['nestedProjects'])
        return hit if hit is not None else self.rule.classify_custody_exclusion(path, None, boundaries['custodyExcludedUnits'])

    def _member_consistency(self, out, boundaries, members):
        """B-S1 U-8: a nested vcs-tree anchor names a member path."""
        if boundaries is None or out.get('refused') is not None:
            return None
        anchors = {r['path'] for r in out['prunedTrees'] if r['reason'] == 'vcs-tree'}
        anchors |= {r['path'] for r in boundaries['prunedTrees'] if r['reason'] == 'vcs-tree'}
        for anchor in sorted(anchors, key=lambda p: p.encode()):
            parent, _, name = anchor.rpartition('/')
            if name not in VCS_MARKERS or parent == '':
                continue
            if self._admitted_boundary(parent, boundaries) is not None:
                continue
            if parent not in members:
                return dict(units=[], prunedTrees=out['prunedTrees'], boundaries=out['boundaries'],
                            refused=dict(detail='native.boundary-inventory-mismatch', roots=[], anchor=anchor, reason='member-not-admitted',
                                         d9=self.model.d9_map('native.boundary-inventory-mismatch')))
        return None

    def _outside_markers(self, markers, boundaries):
        """LD-B2C0-1: markers whose derived pruned anchor is at or below an admitted boundary (r1 RF-1: the full
        boundary predicate, and the anchor itself, as the override states). S3 never enters a nested repository, a nested
        project or a custody- or depth-excluded directory, so the walker's inventory can carry no anchor there; such a
        marker is never a unit (U-4a) and its files are `outside-project-boundary` rows (U-4b 4a). They are withheld from
        the model's anchor derivation, and nothing else."""
        if boundaries is None:
            return []
        cargo = self.rule.cargo_roots_from_markers(markers, self.members)
        out = []
        for mp in markers:
            hit = self.rule.classify_path(mp, cargo, self.members)
            if hit is not None and self._admitted_boundary(hit[0], boundaries) is not None:
                out.append(mp)
        return out

    def discover_units(self, markers, explicit_workspace_roots=None, boundaries=None):
        members = self._bind(boundaries)
        self.members = members
        self.deferred = []
        withheld = set(self._outside_markers(markers, boundaries))
        markers = {k: v for k, v in markers.items() if k not in withheld}
        out = self.model.discover_units(markers, explicit_workspace_roots, boundaries)
        refused = self._member_consistency(out, boundaries, members)
        if refused is not None:
            return refused
        if out.get('refused') is None:
            self.validate('UnitDiscoveryV3', out)
        return out

    def assign_membership(self, units, files, boundaries=None):
        self._bind(boundaries)
        return self.model.assign_membership(units, files, boundaries)

    def unit_scope_descriptor(self, units, ignore_paths, explicit_path_prefixes=None, pruned_trees=None, boundaries=None):
        self._bind(boundaries)
        return self.model.unit_scope_descriptor(units, ignore_paths, explicit_path_prefixes, pruned_trees, boundaries)

    def require_admitted_boundaries(self, boundaries):
        return self.model.require_admitted_boundaries(boundaries)


def v3_of(v2: dict) -> dict:
    """The version-3 projection of a version-2 admitted inventory: the same rows, no member (B-S1)."""
    if not isinstance(v2, dict) or v2.get('schemaVersion') != 2:
        return v2
    out = dict(v2)
    out['schemaVersion'] = 3
    out['memberRepositories'] = []
    return out

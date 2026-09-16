"""INDEPENDENT derivation #1 -- EnumerationPlan binding provenance and default selection.

Written from the published clauses FIRST, then compared with the existing closure helper. It
shares no code with opensip_closure.check_enumeration_plan: it re-reads the kit, re-reads the
exported store, and derives every expected value itself. Where the two disagree, the disagreement
is reported rather than reconciled silently.

CLAUSE -> CODE MAP (each row is a clause this module enforces by itself)

 E1 enumeration-plan.schema.v1.json #/$defs/AvailableProgramBindingV1/properties/programEntry
    "U-1 default uses null"
      -> provenance == 'default-unit'  =>  programEntry IS null
 E2 same clause: "TS/JS extra program: non-null LogicalPath of the selected inventoried config
    (snapshot member)"
      -> provenance == 'explicit-plan-selection' on a tsjs cell => programEntry non-null AND a
         snapshot inventory member
 E3 same clause: "admission derives the actual U-1 marker/synthesized entry and compares it to
    retained TypeScriptConfigGraphV1.entryConfigPath (the graph entry need not be null)"
      -> derive the U-1 marker by native-evidence section 1.4 U-1 precedence
         tsconfig.json > jsconfig.json > package.json inside the unit root, map a package.json
         marker to the SYNTHESIZED entry (null graph entry), and compare to the retained config
         graph's entryConfigPath
 E4 #/$defs/CellObligationV1/properties/programBindings
    "Contiguous ordinal 0..n-1", "Duplicate available universe H inside one cell refuses
    ENUMERATION_BINDING_DUPLICATE_UNIVERSE", "provenance=default-unit at most once and only at
    ordinal 0", maxItems 128
 E5 #/$defs/UnavailableProgramBindingV1: universe is type null; `deficiency` and `nativeCause`
    are REQUIRED members of this record (not of its cell, and not only of the ExecutionInputs
    projection); `extents` is present
 E6 #/$defs/AvailableProgramBindingV1/properties/nativeContextDigest
    "Must be a member of plan.nativeContextDigests at closure ... Outcome must not introduce a
    context this field did not name", plus the universe's own nativeContextId == sha256:<that>
 E7 #/$defs/AvailableProgramBindingV1/properties/candidateSourcePaths
    "Required on those cells' available bindings ... Inventory cells must omit this field"
 E8 extents: maxItems 3, uniqueItems, x-opensip-order by kind; every extent path is a
    first-party scoped snapshot member
 E9 native-evidence section 1.4 U-1/U-3: a directory holding Cargo.toml yields a `rust` unit; a
    directory holding tsconfig.json | jsconfig.json | package.json yields exactly ONE `tsjs`
    unit whose mode follows that precedence. The retained WorkspaceUnitV2 set and each cell's
    languageMode are checked against the derivation from the snapshot alone.
 E10 x-opensip-file-membership-extent-law fileKind/symbolKind/packageKind, re-derived here from
    the retained UnitMembershipV1 + scope + parsed manifests

NOT claimed: this module does not validate the whole Run. It is one independent derivation of
one clause family, and its job is to disagree with the old helper if the old helper is wrong.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'
KIT = S.KIT
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
TSJS_MARKERS = ('tsconfig.json', 'jsconfig.json', 'package.json')   # U-1 precedence order
MODE_OF_MARKER = {'tsconfig.json': ('ts-tsconfig', 'js-allowjs'),
                  'jsconfig.json': ('js-allowjs',),
                  'package.json': ('js-synthesized',)}
EXCLUDED_REASONS = {'host-ignore-convention', 'nested-repository', 'nested-project',
                    'custody-excluded'}


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


class Findings:
    def __init__(self, label):
        self.label = label
        self.rows = []

    def ok(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'PASS',
                          'detail': detail})

    def na(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'NOT-APPLICABLE',
                          'detail': detail})

    def refuse(self, clause, check, detail):
        self.rows.append({'clause': clause, 'check': check, 'result': 'REFUSE',
                          'detail': detail})

    def need(self, cond, clause, check, detail=None):
        (self.ok if cond else self.refuse)(clause, check, detail)
        return cond

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def load(label):
    st, _doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    objs = st.objects
    run_id = [t for t in objs if t.startswith('run3:')][0]
    run = None
    for t, r in objs.items():
        if t == run_id:
            run = r
    plan = None
    for t, r in objs.items():
        if t.startswith('plan2:'):
            plan = r
    snap = None
    for t, r in objs.items():
        if t.startswith('snapshot2:'):
            snap = r
    # the retained parameter records live as labelled blobs
    def blob_json(label_):
        d = st.labels.get(label_)
        return json.loads(st.get_blob(d).decode()) if d else None

    return {'store': st, 'runId': run_id, 'run': run, 'plan': plan, 'snapshot': snap,
            'enum': blob_json('enumeration-plan'),
            'membership': blob_json('unit-membership'),
            'scope': blob_json('scope-descriptor'),
            'spec': blob_json('analysis-spec'),
            'configGraph': blob_json('ts-config-graph'),
            'inventories': {k: blob_json(k) for k in st.labels
                            if k.startswith('subject-inventory:')},
            'blobJson': blob_json}


def derive_units(paths, is_workspace_root):
    """E9: U-1 / U-2 / U-3 unit discovery from the snapshot paths alone.

    U-1  a directory holding Cargo.toml yields a `rust` unit; a directory holding
         tsconfig.json | jsconfig.json | package.json yields exactly ONE `tsjs` unit, mode by
         that precedence.
    U-2  "A Cargo.toml package inside a Cargo workspace root's tree is FOLDED INTO the
         workspace unit as a member package; it is listed in memberPackageRoots, NOT as a
         separate unit."
    U-4  a repository where U-1 yields no TS or Rust unit has NO unit at all: "A file reached
         that way is syntax-only membership with unitOrdinal: null ... not a member of an
         invented unit."
    """
    dirs = {}
    for p in paths:
        d = p.rsplit('/', 1)[0] if '/' in p else ''
        dirs.setdefault(d, set()).add(p.rsplit('/', 1)[-1])
    cargo_dirs = sorted(d for d, names in dirs.items() if 'Cargo.toml' in names)
    ws_roots = [d for d in cargo_dirs if is_workspace_root(d)]
    units = []
    for d in cargo_dirs:
        owner = None
        for w in ws_roots:
            if d != w and under(d, w):
                owner = w
                break
        if owner is not None:
            continue                      # U-2: folded, not its own unit
        members = sorted(x for x in cargo_dirs if x != d and under(x, d)) \
            if d in ws_roots else []
        units.append({'rootPath': d, 'languageFamily': 'rust', 'marker': 'Cargo.toml',
                      'unitKind': 'cargo-workspace' if d in ws_roots else 'cargo-package',
                      'memberPackageRoots': members})
    for d, names in sorted(dirs.items()):
        for m in TSJS_MARKERS:
            if m in names:
                units.append({'rootPath': d, 'languageFamily': 'tsjs', 'marker': m,
                              'admissibleModes': list(MODE_OF_MARKER[m])})
                break        # precedence selects exactly ONE tsjs unit per directory
    return units


def under(p, root):
    return root in ('', '.') or p == root or p.startswith(root.rstrip('/') + '/')


def check_run(label):
    f = Findings(label)
    g = load(label)
    ep, plan, snap = g['enum'], g['plan'], g['snapshot']
    inv_rows = {r['path']: r for r in snap['sourceInventory']}
    mem = {r['path']: r for r in (g['membership'] or {}).get('rows', [])}
    scope = g['scope'] or {}
    kindlaw = kitdoc('docs/coop/design-corrections/foundation/'
                     'enumeration-plan.schema.v1.json')

    def in_scope(p):
        roots = scope.get('workspaceRoots') or ['.']
        pref = scope.get('pathPrefixes') or []
        exc = scope.get('excludedPathPrefixes') or []
        if not any(under(p, r) for r in roots):
            return False
        if pref and not any(under(p, r) for r in pref):
            return False
        return not any(under(p, r) for r in exc)

    def file_extent(cell):
        out = set()
        for p, r in mem.items():
            if r['membership'] == 'outside-project-boundary':
                continue
            if r.get('reason') in EXCLUDED_REASONS:
                continue
            if not in_scope(p) or not under(p, cell['workspaceRoot']):
                continue
            out.add(p)
        return out

    def named_manifests(cell):
        out = set()
        for p in sorted(file_extent(cell)):
            base = p.rsplit('/', 1)[-1]
            if base not in ('package.json', 'Cargo.toml'):
                continue
            by = g['store'].get_blob(inv_rows[p]['sha256'])
            if by is None:
                out.add(p)
                continue
            try:
                if base == 'package.json':
                    nm = json.loads(by.decode()).get('name')
                else:
                    import tomllib
                    nm = (tomllib.loads(by.decode()).get('package') or {}).get('name')
            except Exception:
                out.add(p)
                continue
            if isinstance(nm, str) and nm:
                out.add(p)
        return out

    # ---------------------------------------------------------------- E9 unit derivation
    def is_ws_root(d):
        p = (d + '/Cargo.toml') if d else 'Cargo.toml'
        by = g['store'].get_blob(inv_rows[p]['sha256']) if p in inv_rows else None
        if by is None:
            return False
        try:
            import tomllib
            return 'workspace' in tomllib.loads(by.decode())
        except Exception:
            return False

    derived = derive_units(sorted(inv_rows), is_ws_root)
    retained = (g['membership'] or {}).get('units') or []
    f.need(len(retained) == len(derived),
           'E9 native-evidence 1.4 U-1',
           'UNIT_COUNT_DERIVED_FROM_THE_SNAPSHOT_ALONE',
           {'derived': derived, 'retainedCount': len(retained),
            'retainedRoots': [u.get('rootPath') for u in retained]})
    dmap = {}
    for u in derived:
        dmap.setdefault((u['rootPath'], u['languageFamily']), u)
    for u in retained:
        key = (u.get('rootPath'), u.get('languageFamily'))
        f.need(key in dmap, 'E9 native-evidence 1.4 U-1',
               'EVERY_RETAINED_UNIT_IS_DERIVABLE', {'unit': key,
                                                    'derivable': sorted(map(str, dmap))})
    # U-4: where U-1 yields NO unit, there is no unit at all and every row carries
    # unitOrdinal null -- "not a member of an invented unit"
    if not derived:
        f.need(not retained, 'E9 native-evidence 1.4 U-4 '
               '("not a member of an invented unit")',
               'NO_DERIVED_UNIT_MEANS_NO_RETAINED_UNIT',
               {'retainedUnits': [u.get('unitKind') for u in retained]})
        bad = [r['path'] for r in (g['membership'] or {}).get('rows', [])
               if r.get('unitOrdinal') is not None]
        f.need(not bad, 'E9 native-evidence 1.4 U-4 ("unitOrdinal: null")',
               'EVERY_ROW_CARRIES_A_NULL_UNIT_ORDINAL_WHEN_THERE_IS_NO_UNIT', bad)
    # U-2 folding: a retained cargo workspace unit must list exactly the derived members
    for u in retained:
        d = dmap.get((u.get('rootPath'), u.get('languageFamily')))
        if d and d.get('unitKind'):
            f.need(u.get('unitKind') == d['unitKind'],
                   'E9 native-evidence 1.4 U-2 folding',
                   'UNIT_KIND_MATCHES_THE_DERIVED_WORKSPACE_SHAPE',
                   {'root': u.get('rootPath'), 'retained': u.get('unitKind'),
                    'derived': d['unitKind']})
            f.need(sorted(u.get('memberPackageRoots') or [])
                   == sorted(d.get('memberPackageRoots') or []),
                   'E9 native-evidence 1.4 U-2 memberPackageRoots',
                   'MEMBER_PACKAGE_ROOTS_EQUAL_THE_DERIVED_FOLDED_SET',
                   {'retained': sorted(u.get('memberPackageRoots') or []),
                    'derived': sorted(d.get('memberPackageRoots') or [])})
    modes = {c['languageMode'] for c in ep['cells']}
    for m in sorted(modes):
        if m == 'syntax-only':
            f.ok('E9 native-evidence 1.2/1.4',
                 'SYNTAX_ONLY_MODE_NEEDS_NO_TSJS_MARKER', m)
            continue
        if m.startswith('rust'):
            f.need(any(u['languageFamily'] == 'rust' for u in derived),
                   'E9 native-evidence 1.4 U-1',
                   'RUST_MODE_REQUIRES_A_DERIVED_RUST_UNIT', m)
            continue
        cands = [u for u in derived if u['languageFamily'] == 'tsjs']
        f.need(any(m in u.get('admissibleModes', []) for u in cands),
               'E9 native-evidence 1.4 U-1 precedence',
               'TSJS_MODE_FOLLOWS_THE_MARKER_PRECEDENCE',
               {'mode': m, 'derivedTsjsUnits': cands})

    # ---------------------------------------------------------------- per cell / binding
    for ci, cell in enumerate(ep['cells']):
        pbs = cell['programBindings']
        f.need([b['ordinal'] for b in pbs] == list(range(len(pbs))),
               'E4 CellObligationV1.programBindings',
               'ORDINALS_CONTIGUOUS_FROM_ZERO', [b['ordinal'] for b in pbs])
        f.need(len(pbs) <= 128, 'E4 CellObligationV1.programBindings',
               'ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW', len(pbs))
        defaults = [b for b in pbs if b['provenance'] == 'default-unit']
        f.need(len(defaults) <= 1, 'E4 CellObligationV1.programBindings',
               'DEFAULT_UNIT_AT_MOST_ONCE', len(defaults))
        for b in defaults:
            f.need(b['ordinal'] == 0, 'E4 CellObligationV1.programBindings',
                   'DEFAULT_UNIT_ONLY_AT_ORDINAL_ZERO', b['ordinal'])
        uni_seen = []
        for b in pbs:
            avail = b.get('universe') is not None
            where = {'cell': cell['capabilityId'], 'ordinal': b['ordinal'],
                     'provenance': b['provenance']}
            if avail:
                uni_seen.append(b['universe'])
            # ---- E1 / E2 / E3 programEntry
            if b['provenance'] == 'default-unit':
                f.need(b['programEntry'] is None,
                       'E1 AvailableProgramBindingV1.programEntry '
                       '("U-1 default uses null")',
                       'ENUMERATION_BINDING_PROGRAM_ENTRY',
                       dict(where, programEntry=b['programEntry'],
                            why=('a default-unit binding MUST carry a null programEntry; a '
                                 'filename that happens to exist is not the derivation')))
            elif cell['languageMode'] in ('ts-tsconfig', 'js-allowjs', 'js-synthesized'):
                # E2 is scoped to TS/JS by its own sentence. The SAME clause then says
                # "Rust extra programs are distinct universe H values (cfg/features/
                # ownership); programEntry is not a complete program key" -- so a Rust
                # explicit-plan-selection binding lawfully carries a null programEntry and is
                # distinguished by its universe. (DERIVATION CORRECTION D18-C1: the first
                # draft of this module applied E2 to every family and wrongly refused the
                # Rust second binding.)
                f.need(b['programEntry'] is not None and b['programEntry'] in inv_rows,
                       'E2 AvailableProgramBindingV1.programEntry (TS/JS scope)',
                       'EXPLICIT_PLAN_SELECTION_NAMES_AN_INVENTORIED_CONFIG',
                       dict(where, programEntry=b['programEntry'],
                            isSnapshotMember=b.get('programEntry') in inv_rows))
            else:
                f.ok('E2 same clause: "Rust extra programs are distinct universe H values '
                     '... programEntry is not a complete program key"',
                     'NON_TSJS_EXPLICIT_SELECTION_IS_KEYED_BY_UNIVERSE_NOT_PROGRAM_ENTRY',
                     dict(where, programEntry=b['programEntry'],
                          universe=(b.get('universe') or '')[:16]))
            # ---- E3 derive the U-1 marker / synthesized entry and compare to the graph
            if cell['languageMode'] in ('ts-tsconfig', 'js-allowjs', 'js-synthesized'):
                root = cell['workspaceRoot'] if cell['workspaceRoot'] != '.' else ''
                names = {p.rsplit('/', 1)[-1] for p in inv_rows
                         if (p.rsplit('/', 1)[0] if '/' in p else '') == root}
                marker = next((m for m in TSJS_MARKERS if m in names), None)
                derived_entry = None if marker in (None, 'package.json') else (
                    (root + '/' if root else '') + marker)
                cg = g['configGraph']
                if cg is None:
                    f.na('E3 programEntry vs TypeScriptConfigGraphV1',
                         'NO_RETAINED_CONFIG_GRAPH_ON_THIS_RUN', where)
                elif b['provenance'] == 'default-unit':
                    f.need(cg.get('entryConfigPath') == derived_entry,
                           'E3 AvailableProgramBindingV1.programEntry '
                           '("admission derives the actual U-1 marker/synthesized entry and '
                           'compares it to retained TypeScriptConfigGraphV1.entryConfigPath")',
                           'U1_DERIVED_ENTRY_EQUALS_THE_CONFIG_GRAPH_ENTRY',
                           dict(where, derivedMarker=marker,
                                derivedEntry=derived_entry,
                                graphEntryConfigPath=cg.get('entryConfigPath'),
                                modeOfMarker=MODE_OF_MARKER.get(marker)))
                    if marker is not None:
                        f.need(cell['languageMode'] in MODE_OF_MARKER[marker],
                               'E9/E3 U-1 precedence selects the mode',
                               'CELL_MODE_IS_ADMISSIBLE_FOR_THE_DERIVED_MARKER',
                               dict(where, marker=marker,
                                    mode=cell['languageMode'],
                                    admissible=MODE_OF_MARKER[marker]))
                else:
                    f.need(cg.get('entryConfigPath') == b['programEntry'],
                           'E3 explicit selection vs the retained graph entry',
                           'EXPLICIT_ENTRY_EQUALS_THE_CONFIG_GRAPH_ENTRY',
                           dict(where, programEntry=b['programEntry'],
                                graphEntryConfigPath=cg.get('entryConfigPath')))
            # ---- E5 unavailable branch, ON THE BINDING ITSELF
            if not avail:
                f.need(b.get('universe') is None, 'E5 UnavailableProgramBindingV1.universe',
                       'UNAVAILABLE_BINDING_UNIVERSE_IS_NULL', b.get('universe'))
                f.need('deficiency' in b and b['deficiency'] is not None,
                       'E5 UnavailableProgramBindingV1.deficiency (REQUIRED)',
                       'UNAVAILABLE_BINDING_CARRIES_A_DEFICIENCY', dict(where))
                f.need('nativeCause' in b,
                       'E5 UnavailableProgramBindingV1.nativeCause (REQUIRED, may be null)',
                       'UNAVAILABLE_BINDING_CARRIES_THE_NATIVE_CAUSE_FIELD', dict(where))
                f.need('extents' in b,
                       'E5 UnavailableProgramBindingV1.extents (REQUIRED)',
                       'UNAVAILABLE_BINDING_KEEPS_ITS_HOST_EXTENTS',
                       dict(where, extentKinds=[e['kind'] for e in b.get('extents') or []]))
            else:
                # ---- E6 context/universe joins
                f.need(b['nativeContextDigest'] in plan['nativeContextDigests'],
                       'E6 AvailableProgramBindingV1.nativeContextDigest',
                       'ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN',
                       dict(where, ctx=b['nativeContextDigest']))
                uobj = None
                for t, r in g['store'].objects.items():
                    if t.startswith('native.semantic-universe.') and \
                            t.endswith('#' + b['universe']):
                        uobj = r
                f.need(uobj is not None, 'E6 universe is retained',
                       'BINDING_UNIVERSE_IS_A_RETAINED_RECORD', dict(where))
                if uobj is not None:
                    f.need(uobj.get('nativeContextId')
                           == 'sha256:' + b['nativeContextDigest'],
                           'E6 universe binds THIS selected context',
                           'ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT',
                           dict(where, universeContext=uobj.get('nativeContextId'),
                                bindingContext=b['nativeContextDigest']))
            # ---- E7 candidateSourcePaths
            if not cell['kinds']:
                if avail:
                    f.need('candidateSourcePaths' in b,
                           'E7 candidateSourcePaths required on candidate-only cells',
                           'ENUMERATION_CANDIDATE_SOURCE_PATHS', dict(where))
            else:
                f.need('candidateSourcePaths' not in b,
                       'E7 "Inventory cells must omit this field"',
                       'INVENTORY_CELL_OMITS_CANDIDATE_SOURCE_PATHS', dict(where))
            # ---- E8 / E10 extents
            ext = {e['kind']: set(e['paths']) for e in (b.get('extents') or [])}
            f.need(len(b.get('extents') or []) <= 3, 'E8 extents maxItems 3',
                   'AT_MOST_THREE_EXTENTS', len(b.get('extents') or []))
            f.need(sorted(ext) == sorted(cell['kinds']),
                   'E8 extents cover exactly the cell kinds',
                   'EXTENT_KINDS_EQUAL_THE_CELL_KINDS',
                   dict(where, extents=sorted(ext), kinds=sorted(cell['kinds'])))
            if 'file' in ext:
                want = file_extent(cell)
                f.need(ext['file'] == want,
                       'E10 x-opensip-file-membership-extent-law.fileKind',
                       'FILE_EXTENT_IS_FIRST_PARTY_SCOPED_SNAPSHOT_MEMBERSHIP',
                       dict(where, missing=sorted(want - ext['file']),
                            extra=sorted(ext['file'] - want)))
            if 'package' in ext:
                want = named_manifests(cell)
                f.need(ext['package'] == want,
                       'E10 x-opensip-file-membership-extent-law.packageKind',
                       'PACKAGE_EXTENT_IS_NAMED_FIRST_PARTY_MANIFESTS',
                       dict(where, missing=sorted(want - ext['package']),
                            extra=sorted(ext['package'] - want)))
            for kind, paths in ext.items():
                bad = sorted(p for p in paths if p not in inv_rows)
                f.need(not bad, 'E8 every extent path is a snapshot member',
                       'EXTENT_PATH_IS_A_SNAPSHOT_MEMBER', dict(where, kind=kind, bad=bad))
        f.need(len(set(uni_seen)) == len(uni_seen),
               'E4 "Duplicate available universe H inside one cell refuses"',
               'ENUMERATION_BINDING_DUPLICATE_UNIVERSE',
               {'cell': cell['capabilityId'], 'universes': uni_seen})
    return f


def main():
    out, all_ref = {}, 0
    for label in RUNS:
        f = check_run(label)
        out[label] = {'checks': f.rows,
                      'passed': sum(1 for r in f.rows if r['result'] == 'PASS'),
                      'notApplicable': sum(1 for r in f.rows
                                           if r['result'] == 'NOT-APPLICABLE'),
                      'refused': len(f.refusals),
                      'refusals': f.refusals}
        all_ref += len(f.refusals)
        print('%-13s passed=%-4d n/a=%-3d refused=%d'
              % (label, out[label]['passed'], out[label]['notApplicable'],
                 out[label]['refused']))
        for r in f.refusals:
            print('    REFUSE %-52s %s' % (r['check'][:52],
                                           json.dumps(r['detail'], default=str)[:150]))
    doc = {'standing': __doc__, 'independentOf': 'opensip_closure.check_enumeration_plan',
           'runs': out, 'totalRefusals': all_ref}
    os.makedirs(OUT + '/vectors', exist_ok=True)
    with open(OUT + '/vectors/indep-enumeration-binding.json', 'w') as fh:
        json.dump(doc, fh, indent=1, default=str)
    print('total refusals:', all_ref)


main()

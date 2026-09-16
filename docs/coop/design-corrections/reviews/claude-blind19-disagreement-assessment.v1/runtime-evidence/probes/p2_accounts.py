"""P2: recompute derived_applicability for every owed pair of every export and diff it
against the consumer's declared accounts. Read-only; imports the FROZEN owner module."""
import hashlib, importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
FOUND = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation')
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load('exec_inputs_owner', os.path.join(FOUND, 'execution_inputs_model.v1.py'))
print('owner CELL_STATE entries:', len(M.CELL_STATE))


def objects_of(export):
    """objects[id] = (domain, record) reconstructed from the export object table."""
    out = {}
    for oid, row in export['objectTable'].items():
        if isinstance(row, dict) and 'domain' in row and 'value' in row:
            out[oid] = (row['domain'], row['value'])
        elif isinstance(row, list) and len(row) == 2:
            out[oid] = (row[0], row[1])
    return out


def find_exec_inputs(export, objects):
    """Locate the ExecutionInputsV1 manifest among the export blobs."""
    hits = []
    for digest, b64 in export['blobs'].items():
        import base64
        try:
            raw = base64.b64decode(b64) if isinstance(b64, str) else bytes(b64)
        except Exception:
            continue
        if b'nativeCoverageAccounts' not in raw:
            continue
        try:
            doc = json.loads(raw)
        except Exception:
            continue
        if isinstance(doc, dict) and 'nativeCoverageAccounts' in doc and 'cellOutcomes' in doc:
            hits.append((digest, doc))
    return hits


def enum_plan_of(export):
    import base64
    for digest, b64 in export['blobs'].items():
        try:
            raw = base64.b64decode(b64) if isinstance(b64, str) else bytes(b64)
            doc = json.loads(raw)
        except Exception:
            continue
        if isinstance(doc, dict) and doc.get('schemaVersion') == 1 and 'cells' in doc \
                and 'membershipDigest' in doc:
            return digest, doc
    return None, None


def vcs_of(export):
    import base64
    for digest, b64 in export['blobs'].items():
        try:
            raw = base64.b64decode(b64) if isinstance(b64, str) else bytes(b64)
            doc = json.loads(raw)
        except Exception:
            continue
        if isinstance(doc, dict) and 'sourceInventoryDigest' in doc and 'kind' in doc:
            return digest, doc
    return None, None


report = {'standing': 'read-only recomputation over exact exports using the frozen owner module',
          'runs': []}

for name in ('syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data'):
    path = os.path.join(RB, name, 'exact-export.json')
    export = json.load(open(path))
    objects = objects_of(export)
    ei_hits = find_exec_inputs(export, objects)
    ep_digest, enum_plan = enum_plan_of(export)
    vcs_digest, vcs = vcs_of(export)
    row = {'run': name, 'exportSha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
           'executionInputsBlobs': len(ei_hits), 'enumerationPlanFound': enum_plan is not None,
           'vcsKind': (vcs or {}).get('kind')}
    if not ei_hits or enum_plan is None:
        row['error'] = 'could not locate manifest or enumeration plan in export'
        report['runs'].append(row)
        print(name, row)
        continue
    _d, ei = ei_hits[0]
    accounts = ei['nativeCoverageAccounts']
    by_acc = {(a['cellOrdinal'], a['programOrdinal'], a['relation'], a['resolution']): a
              for a in accounts}

    diffs = []
    owed_count = 0
    cells = enum_plan['cells']
    for ci, cell in enumerate(cells):
        cap = cell['capabilityId']
        if cap in M.CANDIDATE_CAPS:
            continue
        mode = cell['languageMode']
        state_row = M.CELL_STATE.get((cap, mode))
        for binding in cell['programBindings']:
            po = binding['ordinal']
            uni = binding.get('universe')
            en_status = (binding.get('enumerator') or {}).get('status')
            for rel, rung in M._matrix_pairs(cap):
                owed_count += 1
                acc = by_acc.get((ci, po, rel, rung))
                if acc is None:
                    diffs.append({'kind': 'missing-account', 'cell': ci, 'program': po,
                                  'relation': rel, 'resolution': rung})
                    continue
                want_app = M.derived_applicability(rel, uni, en_status, (state_row or {}).get('state'),
                                                   (vcs or {}).get('kind'))
                want_u = None if want_app in ('unavailable-unselected', 'unavailable-null-universe') else uni
                got_app = acc.get('applicability')
                got_u = acc.get('sourceUniverse')
                if got_app != want_app or got_u != want_u or (
                        want_app != 'supported-available' and acc.get('coverageIds')):
                    diffs.append({
                        'cell': ci, 'program': po, 'capabilityId': cap, 'languageMode': mode,
                        'relation': rel, 'resolution': rung,
                        'matrixState': (state_row or {}).get('state'),
                        'matrixDeficiency': (state_row or {}).get('deficiency'),
                        'bindingUniverse': uni, 'enumeratorStatus': en_status,
                        'consumerApplicability': got_app, 'ownerApplicability': want_app,
                        'consumerSourceUniverse': got_u, 'ownerWantsSourceUniverse': want_u,
                        'consumerCoverageIds': acc.get('coverageIds'),
                        'appDiffers': got_app != want_app,
                        'uniDiffers': got_u != want_u,
                        'coverageOnNonSupported': bool(want_app != 'supported-available' and acc.get('coverageIds')),
                    })
    row['owedPairs'] = owed_count
    row['accounts'] = len(accounts)
    row['differences'] = diffs
    row['differenceCount'] = len(diffs)
    report['runs'].append(row)
    print(name, '| owed', owed_count, '| accounts', len(accounts), '| diffs', len(diffs),
          '| vcsKind', row['vcsKind'])
    for d in diffs:
        print('    c%s/p%s %s@%s cap=%s mode=%s matrix=%s | consumer=%s owner=%s | U %s -> %s%s' % (
            d.get('cell'), d.get('program'), d.get('relation'), d.get('resolution'),
            d.get('capabilityId'), d.get('languageMode'), d.get('matrixState'),
            d.get('consumerApplicability'), d.get('ownerApplicability'),
            str(d.get('consumerSourceUniverse'))[:8], str(d.get('ownerWantsSourceUniverse'))[:8],
            ' COVIDS=%d' % len(d.get('consumerCoverageIds') or []) if d.get('coverageOnNonSupported') else ''))

json.dump(report, open(os.path.join(HERE, 'p2-accounts.json'), 'w'), indent=2)
print('\nWROTE p2-accounts.json')

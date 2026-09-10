"""Bounded schema probes for the v20 stage proposal.

Nothing here imports a module from the frozen or live tree. The two resolver
functions the probes exercise (`deref` from foundation/identity-model.py and
`sort_canonical_sets` from foundation/check-identity.py) are TRANSCRIBED
verbatim below, so the frozen checkers are never executed and the frozen bytes
are never touched. Validation uses jsonschema's own Draft202012Validator, the
same draft the document declares.
"""
import copy, json, pathlib, sys
from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
FROZEN = pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v19')
PROPOSAL = pathlib.Path('/tmp/opensip-design-corrections/v20-stage-proposal.v1/work')
SCHEMA_REL = 'docs/coop/design-corrections/foundation/identity-schemas.v2.json'

results = {}


def record(name, value):
    results[name] = value
    return value


# --------------------------------------------------------------- corrected overlay construction
def corrected(schema):
    """The two-file overlay this review proposes: a flat `#/$defs/Domain` selector.

    `Ref.properties.domain` keeps its INLINE enum bytes because
    check-identity.py:1367 reads `SCHEMA['$defs']['Ref']['properties']['domain']['enum']`
    directly; turning it into a $ref would KeyError there.
    """
    out = copy.deepcopy(schema)
    defs = out['$defs']
    domain_enum = defs['Ref']['properties']['domain']['enum']
    node = {
        'type': 'string',
        'enum': list(domain_enum),
        'description': ('Registered digest-domain name. This enumeration and '
                        '#/$defs/Ref/properties/domain are the same set, and both are the '
                        'registered keys of x-opensip-digest-domains.byDomain.'),
    }
    rebuilt = {}
    for key, value in defs.items():
        if key == 'Ref':
            rebuilt['Domain'] = node
        rebuilt[key] = value
    out['$defs'] = rebuilt
    for holder in (out['$defs']['stage-spec']['properties']['outputDomains'],
                   out['$defs']['execution-plan']['properties']['stages']['items']
                      ['properties']['outputDomains']):
        holder['items']['$ref'] = '#/$defs/Domain'
        holder['items']['x-opensip-vocabulary']['schema'] = '#/$defs/Domain'
    through = out['x-opensip-digest-domains']['closureMembership']['selectedThroughOtherInput']
    for field in ('import.producerClosure', 'import.adapterClosure'):
        through[field] = ('plan.importIds, which retains the import record naming them; an import '
                          'named by proof.evaluationInputRefs must itself be a plan.importIds '
                          'member (UNSELECTED_EVALUATION_IMPORT).')
    return out


# ------------------------------------------------- verbatim transcription: identity-model.deref
def make_deref(SCHEMA):
    class AdmissionError(Exception):
        pass

    def deref(node):
        depth = 0
        while type(node) is dict and '$ref' in node:
            ref = node['$ref']
            if not ref.startswith('#/$defs/'):
                raise AdmissionError('EXTERNAL_SCHEMA_REF')
            merged = dict(SCHEMA['$defs'][ref.split('/')[-1]])
            merged.update({k: v for k, v in node.items() if k != '$ref'})
            node = merged
            depth += 1
            if depth > 8:
                raise AdmissionError('SCHEMA_REF_DEPTH')
        return node
    return deref


def model_walk(SCHEMA, selector, value):
    """The list/dict descent of identity-model.walk, which calls deref() at every node."""
    deref = make_deref(SCHEMA)

    def walk(node, value):
        node = deref(node)
        if value is None or type(value) is str:
            return
        if type(value) is list:
            items = node.get('items')
            if items is None:
                return
            for item in value:
                walk(items, item)
            return
        if type(value) is dict:
            properties = node.get('properties', {})
            for name, item in value.items():
                child = properties.get(name)
                if child is not None:
                    walk(child, item)
    walk(SCHEMA['$defs'][selector], value)


# ------------------------------------ verbatim transcription: check-identity.sort_canonical_sets
def sort_canonical_sets(SCHEMA, domain, value):
    canonical = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

    def walk(node, item):
        node = dict(SCHEMA['$defs'][node['$ref'].split('/')[-1]], **{k: v for k, v in node.items() if k != '$ref'}) if type(node) is dict and '$ref' in node and node['$ref'].startswith('#/$defs/') else node
        if type(node) is not dict:
            return item
        if 'oneOf' in node:
            for branch in node['oneOf']:
                try:
                    return walk(branch, item)
                except Exception:
                    continue
            return item
        if type(item) is list and 'items' in node:
            item = [walk(node['items'], x) for x in item]
            if node.get('x-opensip-order') == 'canonical-set':
                item = sorted(item, key=canonical)
            return item
        if type(item) is dict and 'properties' in node:
            return {k: (walk(node['properties'][k], v) if k in node['properties'] else v) for k, v in item.items()}
        return item
    return walk(SCHEMA['$defs'][domain], value)


# ------------------------------------------- verbatim transcription: check-array-orders.arrays()
def arrays(node, path=''):
    if isinstance(node, dict):
        t = node.get('type')
        if t == 'array' or isinstance(t, list) and 'array' in t:
            yield path, node
        for key, value in node.items():
            yield from arrays(value, path + '/' + key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from arrays(value, path + '/' + str(i))


# --------------------------------------------------------------------------------- the fixtures
# Shapes taken from integration-fixtures.py:779-780, the fixture the identity suite builds.
EXEC = {'schemaVersion': 2, 'planId': 'plan2:' + '2' * 64,
        'stages': [{'ordinal': 0, 'stageSpecDigest': 'a' * 64, 'requires': [],
                    'outputDomains': ['view']}]}
SPEC = {'schemaVersion': 2, 'planId': 'plan2:' + '2' * 64,
        'producerClosure': 'closure2:' + '3' * 64, 'operation': 'derive-references-view',
        'parameters': [], 'outputDomains': ['view'], 'outputSchemaDigest': '4' * 64}


def variant(value, **kw):
    out = copy.deepcopy(value)
    out.update(kw)
    return out


def attempt(fn):
    try:
        fn()
        return 'ok'
    except Exception as exc:
        return type(exc).__name__ + ': ' + str(exc).splitlines()[0][:120]


def validates(schema, selector, value):
    document = dict(schema)
    document['$ref'] = '#/$defs/' + selector
    try:
        Draft202012Validator(document).validate(value)
        return 'admitted'
    except Exception as exc:
        return 'refused:' + type(exc).__name__


def suite(tag, schema):
    row = {}
    row['resolver.identity-model.walk(execution-plan)'] = attempt(
        lambda: model_walk(schema, 'execution-plan', copy.deepcopy(EXEC)))
    row['resolver.identity-model.walk(stage-spec)'] = attempt(
        lambda: model_walk(schema, 'stage-spec', copy.deepcopy(SPEC)))
    row['resolver.identity-model.walk(stage-spec,outputDomains=[])'] = attempt(
        lambda: model_walk(schema, 'stage-spec', variant(SPEC, outputDomains=[])))
    row['resolver.check-identity.sort_canonical_sets(execution-plan)'] = attempt(
        lambda: sort_canonical_sets(schema, 'execution-plan', copy.deepcopy(EXEC)))
    row['admission.legal-registered-domain'] = validates(schema, 'stage-spec', SPEC)
    row['admission.unregistered-domain'] = validates(
        schema, 'stage-spec', variant(SPEC, outputDomains=['View']))
    row['admission.free-text-domain'] = validates(
        schema, 'stage-spec', variant(SPEC, outputDomains=['my-provider/output']))
    row['admission.empty-domain-set'] = validates(
        schema, 'stage-spec', variant(SPEC, outputDomains=[]))
    row['admission.two-registered-domains'] = validates(
        schema, 'stage-spec', variant(SPEC, outputDomains=['coverage', 'fact']))
    row['admission.stage-unregistered-domain'] = validates(
        schema, 'execution-plan',
        {'schemaVersion': 2, 'planId': EXEC['planId'],
         'stages': [dict(EXEC['stages'][0], outputDomains=['nonsense'])]})
    row['admission.operation-any-text'] = validates(
        schema, 'stage-spec', variant(SPEC, operation='vendor.acme.v3/derive-call-graph'))
    row['admission.operation-empty-text'] = validates(
        schema, 'stage-spec', variant(SPEC, operation=''))
    # check-identity.py:1367, verbatim expression.
    try:
        row['check-identity:1367'] = bool(
            set(schema['$defs']['Ref']['properties']['domain']['enum'])
            <= set(schema['x-opensip-digest-domains']['byDomain']))
    except Exception as exc:
        row['check-identity:1367'] = type(exc).__name__ + ': ' + str(exc)
    found = list(arrays(schema))
    row['check-array-orders.missing-x-opensip-order'] = [
        p for p, n in found if 'x-opensip-order' not in n]
    row['deep-refs'] = sorted({r['$ref'] for r in _refs(schema) if len(r['$ref'].split('/')) > 3})
    kinds = set(schema['x-opensip-digest-domains']['closureKinds']['byField'])
    membership = schema['x-opensip-digest-domains'].get('closureMembership')
    if membership is None:
        row['closureMembership.exact-15-coverage'] = 'absent'
    else:
        member = set()
        for group in membership.values():
            if isinstance(group, dict):
                member |= set(group)
        row['closureMembership.exact-15-coverage'] = (kinds == member and len(kinds) == 15)
    if 'Domain' in schema['$defs']:
        row['Domain.enum==Ref.domain.enum'] = (
            schema['$defs']['Domain']['enum']
            == schema['$defs']['Ref']['properties']['domain']['enum'])
        row['Domain.enum==byDomain keys'] = (
            set(schema['$defs']['Domain']['enum'])
            == set(schema['x-opensip-digest-domains']['byDomain']))
    return row


def _refs(node):
    if isinstance(node, dict):
        if isinstance(node.get('$ref'), str):
            yield node
        for value in node.values():
            yield from _refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from _refs(value)


frozen = json.loads((FROZEN / SCHEMA_REL).read_text())
proposal = json.loads((PROPOSAL / SCHEMA_REL).read_text())
overlay = corrected(proposal)

report = {'frozen19': suite('frozen19', frozen),
          'proposal': suite('proposal', proposal),
          'corrected-overlay': suite('corrected-overlay', overlay)}

out = HERE / 'overlay' / SCHEMA_REL
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(overlay, indent=2) + '\n')
report['overlay-written'] = str(out)
(HERE / 'probe-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

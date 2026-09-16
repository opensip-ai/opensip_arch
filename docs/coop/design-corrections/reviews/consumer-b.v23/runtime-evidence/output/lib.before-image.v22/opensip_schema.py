"""Independent schema-admission layer for consumer-b.v22.

Three stages are kept separate and are reported separately, because the kit says a
stock JSON-Schema pass is only one of them:

  stage 1  STOCK       -- Draft 2020-12 validation through a pinned local registry
                          (no network retrieval), resolving $ref across kit documents.
  stage 2  KEYWORDS    -- the published x-opensip-* keywords stock libraries ignore:
                          x-opensip-order (closed admission-order vocabulary),
                          x-opensip-uniqueness.ownershipTuple, and collection of
                          x-opensip-digest annotations for the closure stage.
  stage 3  (elsewhere) -- retained closure / cross-record joins, in opensip_closure.py.

Written from the kit text; no author validator was read.
"""
import json
import os

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import jsonschema

import opensip_core as K

KIT = '/tmp/opensip-design-corrections/consumer-b.v22/subject'

# Short document names used by x-opensip-digest `record.document` annotations,
# mapped to kit-relative paths. The annotations spell them relative to the
# docs/coop/design-corrections root.
DOC_ROOT = 'docs/coop/design-corrections'

_docs = {}
_by_id = {}


def doc_path(name):
    """Resolve an annotation document name (e.g. 'workflows/schemas/common.schema.json')."""
    if name.startswith('docs/'):
        return name
    return DOC_ROOT + '/' + name


def load_doc(name):
    p = doc_path(name)
    if p not in _docs:
        with open(KIT + '/' + p, 'rb') as f:
            b = f.read()
        _docs[p] = {'path': p, 'bytes': b, 'json': json.loads(b.decode('utf-8')),
                    'sha256': K.raw_sha256(b)}
    return _docs[p]


ALL_SCHEMA_DOCS = [
    'foundation/identity-schemas.v3.json',
    'foundation/relation-payload-schemas.v2.json',
    'foundation/execution-inputs.schema.v1.json',
    'foundation/enumeration-plan.schema.v1.json',
    'foundation/subject-inventory.schema.v1.json',
    'foundation/evaluator-emission-plan.schema.v1.json',
    'foundation/evaluator-projection-registry.v1.json',
    'foundation/target-attribution.schema.v2.json',
    'foundation/target-attribution.schema.v1.json',
    'foundation/incoming-search.schema.v1.json',
    'foundation/import-source-context.schema.json',
    'foundation/product-configuration.schema.v2.json',
    'foundation/evaluator-fault-observation.schema.v3.json',
    'foundation/provider-target-attribution-return.schema.v2.json',
    'native/native-evidence.schemas.v2.json',
    'native/native-capability-matrix.v2.json',
    'native/capability-manifest-domains.v2.json',
    'native/fact-batch.schema.v3.json',
    'native/occupancy-companion.schema.v1.json',
    'native/dispatch-binding.schema.v1.json',
    'native/protocol3-transitions.v1.json',
    'workflows/schemas/common.schema.json',
    'workflows/schemas/policy-document.schema.json',
    'workflows/schemas/policy-document.v2.schema.json',
    'workflows/schemas/imported-evidence.schema.json',
    'workflows/schemas/test-execution.schema.json',
    'workflows/schemas/baseline-artifact.schema.json',
    'workflows/schemas/comparison-result.schema.json',
    'workflows/schemas/command-envelope.schema.json',
    'workflows/schemas/command-inventory.schema.json',
    'workflows/schemas/graph-query.schema.json',
    'workflows/schemas/invocation-record.schema.json',
    'workflows/schemas/repair.schema.json',
    'workflows/schemas/review.schema.json',
    'workflows/schemas/policy-test.schema.json',
    'workflows/schemas/evaluator3/common.schema.json',
    'workflows/schemas/evaluator3/command-envelope.schema.json',
    'workflows/schemas/evaluator3/command-inventory.schema.json',
    'workflows/schemas/evaluator3/graph-query.schema.json',
    'workflows/schemas/evaluator3/invocation-record.schema.json',
    'workflows/schemas/evaluator3/baseline-artifact.schema.json',
    'workflows/schemas/evaluator3/comparison-result.schema.json',
    'workflows/schemas/evaluator3/repair.schema.json',
    'workflows/schemas/evaluator3/review.schema.json',
    'workflows/schemas/evaluator3/sarif-adapter.schema.json',
    'workflows/schemas/evaluator3/detector-manifest.schema.json',
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
]

_registry = None


def registry():
    """Pinned local registry: every kit schema document, keyed by its own $id.
    Nothing is retrieved from the network."""
    global _registry
    if _registry is None:
        resources = []
        for name in ALL_SCHEMA_DOCS:
            d = load_doc(name)
            j = d['json']
            if '$id' not in j:
                continue
            resources.append((j['$id'], Resource.from_contents(j, default_specification=DRAFT202012)))
            _by_id[j['$id']] = d
        _registry = Registry().with_resources(resources)
    return _registry


def document_for_id(schema_id):
    registry()
    return _by_id[schema_id]


# ------------------------------------------------------------ stage 1: stock validation

def stock_validate(doc_name, selector, instance):
    """Draft 2020-12 validation of `instance` against `doc#selector`."""
    d = load_doc(doc_name)
    j = d['json']
    base = j.get('$id')
    if selector in ('#', '', None):
        sub = {'$ref': base} if base else j
    else:
        sub = {'$ref': (base or '') + selector}
    v = jsonschema.Draft202012Validator(sub, registry=registry())
    errs = []
    for e in sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        errs.append({'path': '/'.join(str(p) for p in e.absolute_path),
                     'schemaPath': '/'.join(str(p) for p in e.absolute_schema_path),
                     'message': e.message[:300]})
    return errs


# ------------------------------------------------------------ stage 2: published keywords

def _resolve_local(schema, root, seen=None):
    """Follow local $ref / cross-document $ref to a concrete subschema dict.

    HELPER CORRECTION (consumer-b.v15): the first draft REPLACED the occurrence with the
    $ref target and therefore DISCARDED sibling keywords written beside the `$ref`. Draft
    2020-12 applies `$ref` siblings, and the relation document's own annotation law says
    "An annotation on the OCCURRENCE, its enclosing schema path, or an intermediate alias
    applies to that occurrence" -- so an `x-opensip-digest` written beside a
    `$ref: #/$defs/DigestHex` is the occurrence's effective annotation. Dropping it made the
    walker blind to most annotated sites of the native bundle (measured: 1 site reached on
    TypeScriptNativeContextV2 instead of 12). Siblings are now merged over the target, with
    the occurrence's own keys taking precedence.
    """
    return _resolve_local2(schema, root, seen)[0]


def _resolve_local2(schema, root, seen=None):
    """As _resolve_local, but also returns the EFFECTIVE ROOT the result lives in.

    HELPER CORRECTION V16-D1 (consumer-b.v16): the walker kept passing the ORIGINAL
    document root down the recursion, so a subschema reached through a CROSS-DOCUMENT $ref
    whose own body contains a LOCAL $ref (for example command-envelope -> common
    StepTermination -> `$ref: #/$defs/D9Class`) was resolved against the wrong document and
    raised a bare KeyError('D9Class'). Original failure, preserved:
        RuntimeError/KeyError 'D9Class' from S.admit(command-envelope.schema.json, '#', env)
    The refusal was NOT a property of the envelope: the same bytes validate under stock
    Draft 2020-12, which carries the base URI correctly. The walker now carries the effective
    root with the resolved node, so the published keywords are enforced inside referenced
    documents instead of crashing there.
    """
    seen = seen or set()
    while isinstance(schema, dict) and '$ref' in schema:
        ref = schema['$ref']
        if ref in seen:
            return schema, root
        seen.add(ref)
        siblings = {k: v for k, v in schema.items() if k != '$ref'}
        if ref.startswith('#'):
            node = root
            for part in ref.lstrip('#/').split('/'):
                if part == '':
                    continue
                part = part.replace('~1', '/').replace('~0', '~')
                node = node[part]
            schema = ({**node, **siblings} if isinstance(node, dict) and siblings else node)
        else:
            if '#' in ref:
                rid, frag = ref.split('#', 1)
            else:
                rid, frag = ref, ''
            registry()
            if rid not in _by_id:
                return schema, root
            newroot = _by_id[rid]['json']
            node = newroot
            for part in frag.lstrip('/').split('/'):
                if part == '':
                    continue
                node = node[part]
            schema = ({**node, **siblings} if isinstance(node, dict) and siblings else node)
            root = newroot
    return schema, root


class KeywordRefusal(Exception):
    def __init__(self, code, path, detail=None):
        super().__init__('%s at %s (%s)' % (code, path, detail))
        self.code = code
        self.path = path
        self.detail = detail


def walk_keywords(doc_name, selector, instance):
    """Independently enforce the published keywords and collect digest annotations.

    Returns (refusals, digestSites). A refusal is a dict; digestSites is a list of
    {instancePath, value, annotation}.
    """
    d = load_doc(doc_name)
    root = d['json']
    # V22-D13: the selector's EFFECTIVE root is carried too. A selector that is itself a
    # cross-document alias (invocation-record TestExecutionParams -> test-execution
    # TestExecutionStepParams) used to be walked against the SELECTING document, so the target's
    # local `#/$defs/EnforcementValue` raised KeyError instead of being enforced.
    start, start_root = ((root, root) if selector in ('#', '', None)
                         else _resolve_local2({'$ref': (root.get('$id') or '') + selector}, root))
    refusals = []
    sites = []

    def rec(schema, inst, ipath, spath, depth=0, root=root):
        if depth > 80 or schema is None:
            return
        schema, root = _resolve_local2(schema, root)
        if not isinstance(schema, dict):
            return
        # branch combinators: descend into every branch that the instance satisfies
        for comb in ('allOf',):
            for i, sub in enumerate(schema.get(comb, [])):
                rec(sub, inst, ipath, spath + '/%s/%d' % (comb, i), depth + 1, root)
        for comb in ('oneOf', 'anyOf'):
            for i, sub in enumerate(schema.get(comb, [])):
                # HELPER CORRECTION (consumer-b.v15): a branch written as a bare local
                # `$ref` cannot be validated standalone -- the ref has no base document -- so
                # the first draft silently skipped every such branch and missed the annotated
                # sites on the NON-NULL alternative of a nullable field. The v15 kit makes
                # that scope explicit: `x-opensip-digest-domains.scope.nullableAlternatives`
                # = "Apply to the non-null branch; the annotation may be on that branch."
                # Branches are now resolved first and validated with the document's $defs.
                res = _resolve_local(sub, root)
                probe = res if not isinstance(res, dict) else {
                    **res, '$defs': root.get('$defs', {})}
                try:
                    jsonschema.Draft202012Validator(probe, registry=registry()).validate(inst)
                except Exception:
                    continue
                rec(sub, inst, ipath, spath + '/%s/%d' % (comb, i), depth + 1, root)
        if 'if' in schema:
            try:
                probe_if = {**_resolve_local(schema['if'], root),
                            '$defs': root.get('$defs', {})} \
                    if isinstance(_resolve_local(schema['if'], root), dict) \
                    else schema['if']
                jsonschema.Draft202012Validator(probe_if,
                                                registry=registry()).validate(inst)
                ok = True
            except Exception:
                ok = False
            if ok and 'then' in schema:
                rec(schema['then'], inst, ipath, spath + '/then', depth + 1, root)
            if (not ok) and 'else' in schema:
                rec(schema['else'], inst, ipath, spath + '/else', depth + 1, root)

        if 'x-opensip-digest' in schema and isinstance(inst, str):
            sites.append({'instancePath': ipath, 'value': inst,
                          'annotation': schema['x-opensip-digest']})

        if isinstance(inst, list):
            ann = schema.get('x-opensip-order')
            if ann is not None:
                try:
                    K.check_order(ann, inst, ipath)
                except K.OrderRefusal as e:
                    refusals.append({'code': e.code, 'path': e.path, 'detail': e.detail,
                                     'annotation': ann})
            uq = schema.get('x-opensip-uniqueness')
            if isinstance(uq, dict) and 'ownershipTuple' in uq:
                tup = uq['ownershipTuple']
                seen = set()
                for i, it in enumerate(inst):
                    if not isinstance(it, dict):
                        continue
                    key = tuple(K.C(it.get(k)) for k in tup)
                    if key in seen:
                        refusals.append({'code': 'OWNERSHIP_TUPLE_DUPLICATE',
                                         'path': ipath + '[%d]' % i, 'detail': str(tup)})
                    seen.add(key)
            items = schema.get('items')
            if items is not None:
                for i, it in enumerate(inst):
                    rec(items, it, ipath + '/%d' % i, spath + '/items', depth + 1, root)
        elif isinstance(inst, dict):
            props = schema.get('properties', {})
            for k, v in inst.items():
                if k in props:
                    rec(props[k], v, ipath + '/' + k, spath + '/properties/' + k,
                        depth + 1, root)
                elif isinstance(schema.get('additionalProperties'), dict):
                    rec(schema['additionalProperties'], v, ipath + '/' + k,
                        spath + '/additionalProperties', depth + 1, root)

    rec(start, instance, '', selector or '#', root=start_root)
    # de-dup digest sites reached by several schema paths
    uniq = {}
    for s in sites:
        uniq[(s['instancePath'], s['value'], K.C(s['annotation']))] = s
    return refusals, list(uniq.values())


def admit(doc_name, selector, instance, label=''):
    """Run stage 1 and stage 2 and return a structured admission result."""
    stock = stock_validate(doc_name, selector, instance)
    kw, sites = walk_keywords(doc_name, selector, instance)
    return {
        'label': label,
        'document': doc_path(doc_name),
        'documentSha256': load_doc(doc_name)['sha256'],
        'selector': selector,
        'stockSchemaErrors': stock,
        'publishedKeywordRefusals': kw,
        'digestSites': sites,
        'admitted': (not stock) and (not kw),
    }

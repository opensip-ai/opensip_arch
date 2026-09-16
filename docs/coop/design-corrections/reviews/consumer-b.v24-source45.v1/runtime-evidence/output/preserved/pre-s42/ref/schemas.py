"""Kit schema admission: stock Draft 2020-12 validation PLUS the published kit keywords.

Layers (kept distinct and reported separately):
  1. exact typed admission of the already-parsed value (canonical.check_typed): bool is not an
     integer, float is never an integer (stock jsonschema admits 1.0 for const/enum 1);
  2. stock JSON Schema validation through a local registry of the exact kit documents
     (no network; $ref resolved by $id / kit path);
  3. x-opensip-order: the closed identity section 3 vocabulary, enforced over every array the
     schema walk reaches (including allOf/if-then/oneOf branches that apply);
  4. x-opensip-digest scope check on bare 64-hex fields (reported per selector).
Relation/digest-domain/registry laws are separate modules (closure.py) and are NOT claimed here.
"""
import hashlib
import json
import os
from urllib.parse import urljoin

import jsonschema
from jsonschema import Draft202012Validator
import referencing
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from canonical import check_typed, C, AdmissionError

KIT_DOCS = '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/subject/docs/'
DC = 'coop/design-corrections/'
ORDER_VOCAB = {"sequence", "canonical-set", "canonical-order", "utf8", "path", "numeric", "ordinal",
               "predicate", "ruleId", "waiverId"}
HEX64 = "^[0-9a-f]{64}(?![\\s\\S])"


def norm_rel(rel):
    if rel.startswith('docs/'):
        rel = rel[5:]
    if not rel.startswith('coop/') and not rel.startswith('v2/'):
        rel = DC + rel
    return rel


class Kit:
    def __init__(self):
        from urllib.parse import urlparse, urlunparse
        self.docs = {}
        self.raw = {}
        self.uri_of = {}
        resources = []
        for d, _, fs in os.walk(KIT_DOCS):
            for f in fs:
                if not f.endswith('.json'):
                    continue
                p = os.path.join(d, f)
                rel = os.path.relpath(p, KIT_DOCS)
                b = open(p, 'rb').read()
                doc = json.loads(b)
                self.raw[rel] = b
                self.docs[rel] = doc
                kit_uri = 'kit:///' + rel
                # referencing defragments absolute refs through urlunparse, which spells an empty-netloc kit URI 'kit:/...';
                # register that spelling too so $id-less documents (security-lifecycle) resolve by selector (helper correction HC-8).
                uris = {kit_uri, urlunparse(urlparse(kit_uri))}
                if isinstance(doc, dict) and isinstance(doc.get('$id'), str):
                    uris.add(doc['$id'])
                    uris.add(urljoin(kit_uri, doc['$id']))
                self.uri_of[rel] = doc.get('$id', kit_uri) if isinstance(doc, dict) else kit_uri
                res = Resource.from_contents(doc, default_specification=DRAFT202012)
                for u in uris:
                    resources.append((u, res))
        self.registry = Registry().with_resources(resources)

    def digest(self, rel):
        return hashlib.sha256(self.raw[norm_rel(rel)]).hexdigest()

    def doc(self, rel):
        return self.docs[norm_rel(rel)]

    def base_uri(self, rel):
        rel = norm_rel(rel)
        doc = self.docs[rel]
        return doc.get('$id') if isinstance(doc, dict) and isinstance(doc.get('$id'), str) else 'kit:///' + rel

    def resolve_pointer(self, rel, selector):
        doc = self.doc(rel)
        cur = doc
        if selector in ('#', ''):
            return cur
        for tok in selector.lstrip('#').lstrip('/').split('/'):
            tok = tok.replace('~1', '/').replace('~0', '~')
            cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
        return cur

    # -------------------------------------------------------------- validation
    def validator_for(self, rel, selector):
        base = self.base_uri(rel)
        ref = base + ('#' + selector.lstrip('#') if selector not in ('#', '') else '')
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$ref": ref}
        return Draft202012Validator(schema, registry=self.registry), ref

    def stock_errors(self, instance, rel, selector):
        v, _ = self.validator_for(rel, selector)
        errs = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
        return [{"path": "/" + "/".join(str(x) for x in e.absolute_path), "message": e.message[:300],
                 "keyword": e.validator} for e in errs]

    def admit(self, instance, rel, selector):
        """Full kit-schema admission of one record. Returns {'ok', 'typed', 'stock', 'order'}."""
        out = {"document": norm_rel(rel), "selector": selector, "typed": None, "stock": [], "order": []}
        try:
            check_typed(instance)
        except AdmissionError as exc:
            out["typed"] = exc.boundary + (":" + exc.detail if exc.detail else "")
        out["stock"] = self.stock_errors(instance, rel, selector)
        if not out["stock"]:
            out["order"] = self.order_violations(instance, rel, selector)
        out["ok"] = out["typed"] is None and not out["stock"] and not out["order"]
        return out

    # -------------------------------------------------------------- x-opensip-order walk
    def order_violations(self, instance, rel, selector):
        base = self.base_uri(rel)
        resolver = self.registry.resolver(base_uri=base)
        start = self.resolve_pointer(rel, selector)
        viol = []
        self._walk(start, instance, resolver, "$", viol, depth=0)
        # de-duplicate (the same array may be reached by several schema paths)
        seen, out = set(), []
        for x in viol:
            key = json.dumps(x, sort_keys=True)
            if key not in seen:
                seen.add(key)
                out.append(x)
        return out

    def _is_valid(self, schema, instance, resolver):
        try:
            v = Draft202012Validator(schema, registry=self.registry, _resolver=resolver)
        except TypeError:
            v = Draft202012Validator(schema, registry=self.registry)
        return v.is_valid(instance)

    def _walk(self, schema, inst, resolver, path, viol, depth):
        if depth > 200 or not isinstance(schema, dict):
            return
        if '$ref' in schema:
            resolved = resolver.lookup(schema['$ref'])
            self._walk(resolved.contents, inst, resolved.resolver, path, viol, depth + 1)
        for key in ('allOf',):
            for sub in schema.get(key, []):
                self._walk(sub, inst, resolver, path, viol, depth + 1)
        for key in ('anyOf', 'oneOf'):
            for sub in schema.get(key, []):
                if self._is_valid(sub, inst, resolver):
                    self._walk(sub, inst, resolver, path, viol, depth + 1)
        if 'if' in schema:
            if self._is_valid(schema['if'], inst, resolver):
                if 'then' in schema:
                    self._walk(schema['then'], inst, resolver, path, viol, depth + 1)
            elif 'else' in schema:
                self._walk(schema['else'], inst, resolver, path, viol, depth + 1)
        if isinstance(inst, list):
            if 'x-opensip-order' in schema:
                self._check_order(schema['x-opensip-order'], inst, path, viol)
            if isinstance(schema.get('items'), dict):
                for i, item in enumerate(inst):
                    self._walk(schema['items'], item, resolver, f"{path}[{i}]", viol, depth + 1)
            for i, sub in enumerate(schema.get('prefixItems', [])):
                if i < len(inst):
                    self._walk(sub, inst[i], resolver, f"{path}[{i}]", viol, depth + 1)
        if isinstance(inst, dict):
            props = schema.get('properties', {})
            for k, v in inst.items():
                if k in props:
                    self._walk(props[k], v, resolver, f"{path}.{k}", viol, depth + 1)
                elif isinstance(schema.get('additionalProperties'), dict):
                    self._walk(schema['additionalProperties'], v, resolver, f"{path}.{k}", viol, depth + 1)

    @staticmethod
    def _key_bytes(item, key):
        v = item.get(key) if isinstance(item, dict) else None
        if isinstance(v, str):
            return v.encode('utf-8')
        if type(v) is int:
            return v
        return None

    def _check_order(self, ann, arr, path, viol):
        def refuse(reason):
            viol.append({"path": path, "order": ann, "violation": reason})

        if isinstance(ann, dict):
            if set(ann.keys()) != {"by"} or not isinstance(ann["by"], list) or not ann["by"]:
                return refuse("ORDER_ANNOTATION_UNKNOWN")
            keys = []
            for it in arr:
                tup = []
                for k in ann["by"]:
                    kb = self._key_bytes(it, k)
                    if kb is None:
                        return refuse(f"ORDER_KEY_MISSING:{k}")
                    tup.append(kb)
                keys.append(tuple(tup))
            for i in range(1, len(keys)):
                if keys[i - 1] >= keys[i]:
                    return refuse(f"ORDER_OR_DUPLICATE_AT:{i}")
            return
        if ann not in ORDER_VOCAB:
            return refuse("ORDER_ANNOTATION_UNKNOWN")
        if ann == 'sequence':
            return
        if ann in ('canonical-set', 'canonical-order'):
            enc = [C(x) for x in arr]
            for i in range(1, len(enc)):
                if ann == 'canonical-set' and enc[i - 1] >= enc[i]:
                    return refuse(f"ORDER_OR_DUPLICATE_AT:{i}")
                if ann == 'canonical-order' and enc[i - 1] > enc[i]:
                    return refuse(f"ORDER_DECREASING_AT:{i}")
            return
        if ann == 'utf8':
            if not all(isinstance(x, str) for x in arr):
                return refuse("ORDER_UTF8_NON_STRING")
            b = [x.encode('utf-8') for x in arr]
        elif ann == 'numeric':
            if not all(type(x) is int for x in arr):
                return refuse("ORDER_NUMERIC_NON_INTEGER")
            b = arr
        elif ann == 'ordinal':
            for i, it in enumerate(arr):
                if not isinstance(it, dict) or type(it.get('ordinal')) is not int or it['ordinal'] != i:
                    return refuse(f"ORDER_ORDINAL_NOT_CONTIGUOUS_AT:{i}")
            return
        elif ann == 'path':
            b = [self._key_bytes(it, 'path') for it in arr]
        elif ann in ('ruleId', 'waiverId'):
            b = [self._key_bytes(it, ann) for it in arr]
        elif ann == 'predicate':
            b = []
            for it in arr:
                t = tuple(self._key_bytes(it, k) for k in ('ruleId', 'subjectId', 'predicateId'))
                if None in t:
                    return refuse("ORDER_KEY_MISSING:predicate")
                b.append(t)
        if any(x is None for x in b):
            return refuse(f"ORDER_KEY_MISSING:{ann}")
        for i in range(1, len(b)):
            if b[i - 1] >= b[i]:
                return refuse(f"ORDER_OR_DUPLICATE_AT:{i}")

    # -------------------------------------------------------------- digest annotation census
    def unannotated_hex_fields(self, rel):
        """Mechanical scan of a schema document: properties whose schema is (or $refs a def that is)
        the bare 64-hex pattern without an x-opensip-digest annotation on the property or its
        nullable branch. Reported, not silently tolerated."""
        doc = self.doc(rel)
        out = []

        def is_hex(s, seen):
            if not isinstance(s, dict):
                return False
            if s.get('pattern') == HEX64:
                return True
            r = s.get('$ref')
            if isinstance(r, str) and r.startswith('#/$defs/') and r not in seen:
                tgt = doc.get('$defs', {}).get(r.split('/')[-1])
                return is_hex(tgt, seen | {r})
            return False

        def annotated(s):
            if not isinstance(s, dict):
                return False
            if 'x-opensip-digest' in s:
                return True
            for alt in s.get('oneOf', []) + s.get('anyOf', []):
                if isinstance(alt, dict) and 'x-opensip-digest' in alt:
                    return True
            return False

        def walk(s, p):
            if isinstance(s, dict):
                for k, v in s.get('properties', {}).items():
                    cand = [v] + [a for a in (v.get('oneOf', []) + v.get('anyOf', [])) if isinstance(a, dict)] if isinstance(v, dict) else []
                    if any(is_hex(c, set()) for c in cand) and not annotated(v):
                        out.append(f"{p}/properties/{k}")
                    walk(v, f"{p}/properties/{k}")
                for key in ('items', 'additionalProperties'):
                    if isinstance(s.get(key), dict):
                        it = s[key]
                        if is_hex(it, set()) and not annotated(it):
                            out.append(f"{p}/{key}")
                        walk(it, f"{p}/{key}")
                for key in ('allOf', 'oneOf', 'anyOf'):
                    for i, sub in enumerate(s.get(key, [])):
                        walk(sub, f"{p}/{key}/{i}")
                for key in ('then', 'else', 'if'):
                    if isinstance(s.get(key), dict):
                        walk(s[key], f"{p}/{key}")
                for name, d in s.get('$defs', {}).items():
                    walk(d, f"{p}/$defs/{name}")

        walk(doc, '#')
        return out


_KIT = None


def kit():
    global _KIT
    if _KIT is None:
        _KIT = Kit()
    return _KIT

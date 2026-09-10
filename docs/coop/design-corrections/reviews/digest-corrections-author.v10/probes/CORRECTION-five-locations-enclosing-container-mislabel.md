# Correction to my own probe: `probe-five-locations-pre-vs-post.v1.py` mislabelled one class

Both `probe-five-locations-pre-vs-post.v1.py` and its result JSON are retained **unmodified**; this
note supersedes one label in them.

That probe reported five propagation classes and found `enclosing-container` **non-discriminating**
(0 of 10 cases separating frozen v11 from the corrected model). That conclusion was an artefact of
the fixture, not a fact about the model. What the probe built under that name was:

```python
document['$defs']['T1'] = {'type':'object','properties':{'leaf': leaf(b)}}
selector['probe']       = {'$ref':'#/$defs/T1','properties':{'leaf': leaf(a)}}
```

That is a `$ref` container with a sibling `properties` overlay — two *separate arrivals* at
`file.probe.leaf`, i.e. a second same-path merge, duplicating the `same-path-merge` class. It never
put an annotation on the container itself, so it never exercised the `inherited` filter, which is one
of the two early-collection sites the defect lived in.

Root's prepared recheck uses the real shape:

```python
props['probe'] = {'type':'object','x-opensip-digest':a,'properties':{'leaf': leaf(b)}}
```

Here the container's annotation reaches the leaf through `inherited`, and that class **does**
discriminate: on frozen v11 it admits, on the corrected source it refuses with
`RELATION_DIGEST_ANNOTATION_CONFLICT`. See
`result-adapted-codex-v12-typed-equality-recheck.v1.json` — three shapes discriminate
(`property-alias`, `parent-nullable-branch`, `enclosing-container`), not two.

The correction itself already covered this class; only my coverage claim was wrong. `check-identity.py`
now carries both shapes under accurate names — `enclosing-container` for the annotated container and
`container-ref-overlay` for the `$ref`-plus-overlay merge — which is what took the suite from 752 to
767 checks.

This is the fifth time in this engagement that root's control matrix has caught a class mine missed
(container-ref, branch-order, alias-location, inherited-limb, and now enclosing-container). I am
recording it rather than presenting my matrix as having been adequate.

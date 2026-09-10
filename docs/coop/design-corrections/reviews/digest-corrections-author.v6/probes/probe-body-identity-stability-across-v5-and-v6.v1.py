"""PROBE: does the v6 selected-unit design actually move an unchanged Rust body identity?

Root's v6 note says it should NOT, and that my interface-note claim of churn was an assumption
rather than a measurement. This measures it across the two ACTUAL source images:

  * v5: the retained image at reviews/digest-corrections-author.v5/author-source/, whose nine owned
    files are overlaid onto a copy of the current tree at
    runs/v5-image/ so that the non-owned files it depends on (canonical.py, the workflow and native
    helpers root owns) are present. Only the nine owned files differ between the two runs; the
    overlay was verified file by file against the retained image's hashes.
  * v6: the current working tree.

Both are executed unmodified, in separate module namespaces, and asked for the SAME thing: the
default single-target Rust clone Run's body identity, its language-version component and the raw
canonical bytes of its projection. The v6 tree additionally reports the ownership identity and the
sourceUniverse, which SHOULD move.

Nothing here is rewritten to make a result look better; whatever the comparison says is reported.
"""
import ast,hashlib,json,sys
from pathlib import Path

ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
IMAGES={
 'v5':Path('/tmp/opensip-design-corrections/digest-corrections-author.v6/runs/v5-image/docs/coop/design-corrections/foundation/check-identity.py'),
 'v6':ROOT/'docs/coop/design-corrections/foundation/check-identity.py',
}

def load(path):
    """Execute a fixture image up to graph_with_import, in its own namespace."""
    source=path.read_text();tree=ast.parse(source)
    last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
    ns={'__file__':str(path),'__name__':'stability_'+path.parent.name}
    sys.argv=[sys.argv[0]]
    exec(compile('\n'.join(source.split('\n')[:last]),str(path),'exec'),ns)
    return ns

def measure(label,path):
    ns=load(path);M,C=ns['M'],ns['C']
    run,objects,blobs=ns['build'](resolved=True,has_match=True,relation='clones',universe_language='rust')
    fact=next(v for k,(d,v) in objects.items() if d=='fact')
    payload=C.parse(blobs[fact['payloadDigest']])
    frame=blobs[payload['bodyIdentity'].removeprefix('sha256:')]
    parts=M.parse_body_frame(frame)
    universe=M.parse_h_frame(blobs[fact['sourceUniverse']],'native-semantic-universe')[1]
    context=M.parse_h_frame(blobs[universe['nativeContextId'].removeprefix('sha256:')],'native-context')[1]
    row=M.DIGESTS['domainSets']['native-semantic-universe']['native.semantic-universe.rust.v2']
    try:
        projection=ns['body_language_version'](universe,context,row,fact['anchors'][0],
            {'sourceUnitOwnership':M.parse_h_frame(
                blobs[universe['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')[1]}
            if universe.get('sourceUnitOwnershipId') else None)
    except TypeError:
        projection=ns['body_language_version'](universe,context,row,fact['anchors'][0])
    return {'image':str(path),'imageSha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'bodyIdentity':payload['bodyIdentity'],
            'languageVersionComponentHex':parts[4].hex(),
            'projectionCanonicalBytesHex':C.canonical(projection).hex(),
            'projection':projection,
            'anchorPath':fact['anchors'][0]['path'],
            'normalisationVersion':payload['normalisationVersion'],
            'sourceUnitOwnershipId':universe.get('sourceUnitOwnershipId'),
            'sourceUniverse':fact['sourceUniverse'],
            'runId':M.close_run(run,objects,blobs)}

rows={label:measure(label,path) for label,path in IMAGES.items()}
same=lambda key:rows['v5'][key]==rows['v6'][key]
print(json.dumps({
 'standing':'actual Claude coauthor measurement across two retained source images; design/reference '
            'evidence only, no product qualification',
 'question':'does moving the same effective edition into a selected units table move the body identity?',
 'measurements':rows,
 'unchanged':{k:same(k) for k in ('bodyIdentity','languageVersionComponentHex',
                                  'projectionCanonicalBytesHex','normalisationVersion','anchorPath')},
 'changed':{k:not same(k) for k in ('sourceUnitOwnershipId','sourceUniverse')},
 'verdict':('STABLE: the body identity, its version component and the projection bytes are identical '
            'across the two images, while the ownership identity and the sourceUniverse moved'
            if same('bodyIdentity') and same('projectionCanonicalBytesHex')
            and not same('sourceUniverse')
            else 'NOT STABLE: see measurements')},indent=1))

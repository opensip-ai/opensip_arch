"""Full-product qualification report admission reference. No measurements generated here.
All context values are from the authenticated release gate/runner inventory.
A submitted report is never allowed to construct that context.
"""
import hashlib,importlib.util,json,statistics
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('quality_join',H/'g13-validator.v5.py');G=importlib.util.module_from_spec(s);s.loader.exec_module(G)
C=G.C
SCHEMA=json.loads((H/'product-quality-report.schema.v3.json').read_text())
def admit(raw,signature,context):
    try:
        if not G.verify_signature(raw,signature,context):return {'admitted':False,'reason':'signature'}
        value=C.parse(raw);C.validate(SCHEMA,value)
        for field in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest','runnerId','profileId','environmentDigest','qualificationRequestId']:
            if value[field]!=context[field]:return {'admitted':False,'reason':'trusted-subject-join'}
        for field,raw_field in [('matrixDigest','matrixBytes'),('corpusDigest','corpusBytes'),('environmentDigest','environmentBytes')]:
            if hashlib.sha256(context[raw_field]).hexdigest()!=context[field]:return {'admitted':False,'reason':'trusted-input-bytes'}
        cells={v['cellId']:v for v in value['cells']}
        if len(cells)!=len(value['cells']) or set(cells)!=set(context['expectedCells']):return {'admitted':False,'reason':'cell-set'}
        results=[]
        for key in sorted(cells):
            cell=cells[key];oracle=context['expectedCells'][key]
            actual=[C.canonical(v) for v in cell['observations']];expected=[C.canonical(v) for v in oracle['observations']]
            if actual!=sorted(actual) or len(actual)!=len(set(actual)):return {'admitted':False,'reason':'observation-order-duplicate'}
            # All thresholds and oracle atoms are trusted gate inputs, never report counters.
            correctness=actual==sorted(expected) and cell['exitStatus']==oracle['exitStatus']
            elapsed=sorted(cell['elapsedNanos'])[3];rss=max(cell['peakRssBytes'])
            perf=elapsed<=oracle['absoluteNanos'] and rss<=oracle['absoluteRssBytes']
            if (oracle['baselineMedianNanos'] is None) != (oracle['baselinePeakRssBytes'] is None):return {'admitted':False,'reason':'baseline-pair'}
            if oracle['baselineMedianNanos'] is None:perf=False
            if oracle['baselineMedianNanos'] is not None:
                perf=perf and elapsed*1000000<=oracle['baselineMedianNanos']*1200000
                perf=perf and rss*1000000<=oracle['baselinePeakRssBytes']*1250000
            results.append({'cellId':key,'correctness':correctness,'performance':perf,'expectedCount':len(expected),'actualCount':len(actual),'missingCount':len(set(expected)-set(actual)),'extraCount':len(set(actual)-set(expected))})
        return {'admitted':True,'passed':all(v['correctness'] and v['performance'] for v in results),'cells':results}
    except (ValueError,KeyError,TypeError,OSError,G.subprocess.SubprocessError,C.ValidationError):return {'admitted':False,'reason':'invalid'}

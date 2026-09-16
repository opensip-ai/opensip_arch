import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
for lab in sys.argv[1:] or ['syntax-code', 'syntax-data', 'rust']:
    st, _ = ST.Store.load(OUT + '/runs/%s.store.json' % lab)
    d = st.labels.get('unit-membership')
    m = json.loads(st.get_blob(d).decode())
    print('==', lab)
    print('  units:', json.dumps(m['units'], indent=1)[:700])
    for r in m['rows']:
        print('    %-34s fam=%-8s unit=%-5s %-16s %s'
              % (r['path'], r['languageFamily'], r['unitOrdinal'], r['membership'],
                 r['reason']))

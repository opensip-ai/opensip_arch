import json
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch/output/evidence/suites/'
b=json.load(open(S+'reference-src25.json'))
a=json.load(open(S+'reference-baseline25.json'))
ba={}
for c in a['checks']: ba[c['script']]=c
for c in b['checks']:
    nm=c['script']; base=ba.get(nm,{})
    ec=c['exitCode']; be=base.get('exitCode')
    rs=c.get('reportSha256'); brs=base.get('reportSha256')
    tag='SAME' if (ec==be and rs==brs) else 'CHANGED'
    print(tag, nm, '| exit', be, '->', ec, '| report', str(brs)[:10], '->', str(rs)[:10])
    if ec!=0:
        print('    stderr:', c.get('stderr','')[-900:])

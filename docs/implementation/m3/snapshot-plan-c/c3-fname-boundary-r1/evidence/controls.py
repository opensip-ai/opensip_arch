import json
from pathlib import Path

def field(chunks,present=True):
    consumed=0
    if not present:return {'result':'absent','consumed':0}
    for chunk in chunks:
        for byte in chunk:
            consumed+=1
            if byte==0:return {'result':'complete','consumed':consumed}
            if consumed==4096:return {'result':'archive-bound:D4','consumed':consumed}
    return {'result':'truncated','consumed':consumed}

cases=[('empty',b'\0',True,'complete',1),('below',b'a'*4094+b'\0',True,'complete',4095),('exact',b'a'*4095+b'\0',True,'complete',4096),('overflow-terminator',b'a'*4096+b'\0',True,'archive-bound:D4',4096),('overflow-nonzero',b'a'*8192,True,'archive-bound:D4',4096),('truncated',b'a'*17,True,'truncated',17),('truncated-empty',b'',True,'truncated',0),('absent',b'payload',False,'absent',0)]
rows=[]
for name,data,present,expected,count in cases:
    for width in [1,7,4095,4096,8192]:
        chunks=[data[i:i+width]for i in range(0,len(data),width)]
        got=field(chunks,present);assert got=={'result':expected,'consumed':count},(name,width,got)
        rows.append(dict(case=name,chunkWidth=width,fieldBytes=len(data),result=got['result'],consumed=got['consumed']))
Path('/tmp/opensip-implementation/c3-fname-boundary-r1-authoring/controls.json').write_text(json.dumps(dict(standing='NEW SYNTHETIC PROSPECTIVE BOUNDARY INTERPRETATION CONTROLS; not product parser, full gzip/tar profile, physical IO or custody/source admission',cases=rows,passed=True,productImplemented=False,productQualification=False),indent=2)+'\n')
print('40 exact prospective FNAME boundary/chunk controls passed; no product/whole-decoder claim')

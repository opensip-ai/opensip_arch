"""Third, independent canonical encoder + SHA-256 for the new closed records.
Written from identity-and-evidence section 3 prose only; imports nothing from the subject."""
import hashlib
def enc(v):
    if v is True:return b'true'
    if v is False:return b'false'
    if v is None:return b'null'
    if isinstance(v,int):return b'%d'%v
    if isinstance(v,str):
        out=b'"'
        for ch in v:
            c=ord(ch)
            if ch=='"':out+=b'\\"'
            elif ch=='\\':out+=b'\\\\'
            elif c==8:out+=b'\\b'
            elif c==9:out+=b'\\t'
            elif c==10:out+=b'\\n'
            elif c==12:out+=b'\\f'
            elif c==13:out+=b'\\r'
            elif c<0x20:out+=b'\\u%04x'%c
            else:out+=ch.encode('utf-8')
        return out+b'"'
    if isinstance(v,list):return b'['+b','.join(map(enc,v))+b']'
    if isinstance(v,dict):
        pairs=sorted(v.items(),key=lambda kv:kv[0].encode('utf-8'))
        return b'{'+b','.join(enc(k)+b':'+enc(x) for k,x in pairs)+b'}'
    raise TypeError(v)
def sha(v):return hashlib.sha256(enc(v)).hexdigest()
V={
 'program-predicate':{'schemaVersion':2,'ruleProgramDigest':'0'*64,'ruleId':'r','predicateId':'p.1','operation':'and','nodeDigest':'1'*64},
 'finding-parameters':{'schemaVersion':2,'messageCode':'m','parameters':{'b':1,'a':'x','c':False}},
 'stage-spec':{'schemaVersion':2,'planId':'plan2:'+'2'*64,'producerClosure':'closure2:'+'3'*64,'operation':'derive','parameters':[],'outputDomains':['view'],'outputSchemaDigest':'4'*64},
 'commit-inventory':{'schemaVersion':2,'runId':'run2:'+'5'*64,'objects':['view2:'+'6'*64],'blobDigests':['7'*64]},
 'owner-source-set':[{'ownerKey':'a','source':'repository','ownerFileManifestSha256':'8'*64},
                     {'ownerKey':'b','source':'repository','ownerFileManifestSha256':'9'*64}],
}
for k,v in V.items():
    print("%-20s %s" % (k,sha(v)))
    print("   bytes:",enc(v)[:110])
sample={'schemaVersion':2,'x':'y'}
raw=enc(sample)
frame=b'opensip.product.v1\0'+b'native.context.typescript.v2'+b'\0'+len(raw).to_bytes(8,'big')+raw
print('h-frame              ',hashlib.sha256(frame).hexdigest())
print('raw-canonical        ',hashlib.sha256(raw).hexdigest())

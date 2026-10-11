from pathlib import Path
import json,hashlib,tempfile,os
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');D=B/'sm-experimental-dependency-preparation-2026-10-10';O=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');dest=D/'public-intake-packet-r21.json';assert not dest.exists();root=Path(tempfile.mkdtemp(prefix='opensip-public-intake-round-21-data-',dir=O));root.chmod(0o700)
def ref(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
value=dict(outputRoot=str(root),indexReceipt=ref(D/'missing-public-index-inputs-r21/receipt.json'),archiveReceipt=ref(D/'missing-public-archive-inputs-r21/receipt.json'));packet=root/'packet.json';packet.write_text(json.dumps(value,indent=2)+'\n');dest.write_text(json.dumps(dict(standing='PREPARED-NOT-EXECUTED UNTIL OWN PARAMETERIZED ENTRY ACCEPTED',packet=ref(packet),root=str(root),expectedPublicIndexes=3,expectedVersionArchives=82,expectedArchiveBytes=17478792,sourceAuthentication=False,nativeAdmission=False,executed=False),indent=2)+'\n');print('Prepared independently pinned82input intake packet; no execution.')

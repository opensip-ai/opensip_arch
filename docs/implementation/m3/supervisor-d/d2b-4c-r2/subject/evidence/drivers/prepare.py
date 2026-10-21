from pathlib import Path
import json,subprocess,datetime
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-successor-takeover';F=Path(__file__).parent
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip();assert head=='0f5bbe492a40ff03c18262536f58c86e5af64be0';assert not W.exists()
subprocess.run(['git','worktree','add','--detach',str(W),head],cwd=P,check=True)
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit='D2b-4c',standing='UNACCEPTED implementation worktree based on exact accepted4b/inventory237/description185; statusr120 independently reviewing without source edits',worktree=str(W),productParent=head,architectureParentAtStart=subprocess.check_output(['git','rev-parse','HEAD'],cwd=A,text=True).strip(),authorityRefreshAfterStatusRequired=True,predecessor='/tmp/opensip-implementation/rust3-send-takeover-2026-10-21/integration-r1.json',requirements='/tmp/opensip-implementation/rust3-send-takeover-2026-10-21/d2b4c-requirements-preparation-r1.json',cargoTarget=str(F/'target'),unitAccepted=False,productQualification=False)
(F/'PREPARED.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))

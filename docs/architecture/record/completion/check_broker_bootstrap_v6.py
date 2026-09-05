#!/usr/bin/env python3
"""Proposed bootstrap and physical SDK integration replay."""
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('bootstrap_v3',P/'broker-bootstrap.model.v3.py');B=importlib.util.module_from_spec(s);s.loader.exec_module(B)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(P/'broker-bootstrap.report.v6.json'));args=ap.parse_args();checks=[]
 for c in json.loads((P/'broker-bootstrap-cases.v3.json').read_text())['cases']:
  try:B.parse(c['encoded']);actual='ACCEPT'
  except B.StartupFailure:actual='STARTUP-FAILURE'
  checks.append({'id':c['id'],'passed':actual==c['expected'],'actual':actual,'expected':c['expected']})
 replay={}
 with tempfile.TemporaryDirectory() as td:
  for key,checker,retained in [('frozen-v2','check_broker_bootstrap_v2.py','broker-bootstrap.report.v2.json'),('physical-courier','check_broker_sdk_courier_v4.py','broker-sdk-courier.report.v4.json')]:
   report=Path(td)/(key+'.json');p=subprocess.run([sys.executable,str(P/checker),'--report',str(report)],capture_output=True,text=True);value=json.loads(report.read_text());replay[key]={'exit':p.returncode,'passed':value['passed'],'total':value['total'],'byteIdentical':report.read_bytes()==(P/retained).read_bytes()};checks.append({'id':'replay/'+key,'passed':p.returncode==0 and replay[key]['byteIdentical']})
 report={'standing':'PROPOSED-CONDITIONAL-SECURITY-INTEGRATION','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'replays':replay,'securityAcceptance':False,'qualification':False}
 Path(args.report).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['passed'],report['total']);print([c for c in checks if not c['passed']]);return 0 if report['passed']==report['total'] else 1
if __name__=='__main__':raise SystemExit(main())

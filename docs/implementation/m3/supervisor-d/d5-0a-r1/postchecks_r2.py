from pathlib import Path
import subprocess,sys
F=Path(__file__).parent
for name in ['owning_checks_r2.py','mutation_r2.py']:
 r=subprocess.run([sys.executable,'-I','-B',str(F/name)]);assert r.returncode==0,(name,r.returncode)

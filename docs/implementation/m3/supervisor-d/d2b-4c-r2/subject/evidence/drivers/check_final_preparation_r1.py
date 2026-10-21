from pathlib import Path
import runpy,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
f=Path(__file__).parent
for name in ['verify_source_census_r2.py','check_repository_r2.py','prepare_inventory238_preview.py']:
 runpy.run_path(str(f/name),run_name='__main__')

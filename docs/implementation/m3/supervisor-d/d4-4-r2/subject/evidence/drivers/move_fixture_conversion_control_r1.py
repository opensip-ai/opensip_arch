from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/platform/src/process_tests.rs');s=p.read_text();idx=s.index('\n// D4-T3 needs the factory');addition=s[idx:];p.write_text(s[:idx]);p=Path('crates/platform/src/process_accounted.rs');s=p.read_text();idx=s.rindex('\n}');addition=addition.replace('fn test_fixture_conversion_preserves_every_checked_launch_field() {','fn test_fixture_conversion_preserves_every_checked_launch_field() {\n    use crate::process::{ClosureRecheck, VerifiedLaunch};');p.write_text(s[:idx]+addition+s[idx:])
print('Moved full-carrier invariant test into the process owner descendant test module; no API visibility widened for tests.')

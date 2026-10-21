import os
from pathlib import Path
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/tests/factory_fixture.rs');s=p.read_text();old='''    if let Value::Map(rows) = v {
        if let Some((_, value)) = rows.iter().find(|(k, _)| k == name) {
            return value;
        }
    }''';assert s.count(old)==1;s=s.replace(old,'''    if let Value::Map(rows) = v
        && let Some((_, value)) = rows.iter().find(|(k, _)| k == name)
    {
        return value;
    }''');p.write_text(s)

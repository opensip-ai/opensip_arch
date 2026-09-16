import json
from helpers import *
def e24(r): (r/'crates/contracts/Cargo.toml').write_text(pkg('opensip-contracts','[dev_dependencies]\nopensip-host={path="../host"}\n'))
case('edition2024 underscore dev_dependencies (fresh)', 'cargo', e24)
case('stale: edition2021 target underscore build_dependencies', 'refused', lambda r:(r/'crates/contracts/Cargo.toml').write_text(pkg('opensip-contracts',"[target.'cfg(windows)'.build_dependencies]\nopensip-host={path=\"../host\"}\n",edition='2021')), stale=True)
case('fresh: edition2021 target underscore build_dependencies', 'forbidden declared', lambda r:(r/'crates/contracts/Cargo.toml').write_text(pkg('opensip-contracts',"[target.'cfg(windows)'.build_dependencies]\nopensip-host={path=\"../host\"}\n",edition='2021')))
case('stale: no edition key (2015) underscore dev_dependencies', 'refused', lambda r:(r/'crates/contracts/Cargo.toml').write_text('[package]\nname="opensip-contracts"\nversion="0.1.0"\n[dev_dependencies]\nopensip-host={path="../host"}\n'), stale=True)
print(json.dumps(results, indent=1))

"""Reviewer probes for legacy underscore tables: duplicates with hyphen tables, edition behaviour, allowed/forbidden, stale/fresh."""
import json
import subprocess
from helpers import *  # fixture, metadata, case, results, pkg, CARGO, M

H = '[package]\nname="opensip-host"\nversion="0.1.0"\nedition="{e}"\n'
K = '[package]\nname="opensip-contracts"\nversion="0.1.0"\nedition="{e}"\n'


def write(rel, text):
    return lambda r: (r / rel / 'Cargo.toml').write_text(text)


def raw_cargo(text):
    """Report Cargo's own verdict/warnings for a host manifest fragment (fresh)."""
    root = fixture()
    (root / 'crates/host/Cargo.toml').write_text(text)
    run = subprocess.run([CARGO, 'metadata', '--offline', '--format-version', '1', '--manifest-path', str(root / 'Cargo.toml')], capture_output=True, text=True, env={**os.environ, 'CARGO_TARGET_DIR': str(root / 'target')})
    deps = []
    if run.returncode == 0:
        meta = json.loads(run.stdout)
        deps = [(d['name'], d['kind'], d['target']) for p in meta['packages'] if p['name'] == 'opensip-host' for d in p['dependencies']]
    shutil.rmtree(root)
    return {'rc': run.returncode, 'stderr': [l for l in run.stderr.splitlines() if l.strip()][:4], 'hostDeps': deps}


cargo_behaviour = {}
for e in ('2015', '2018', '2021', '2024'):
    cargo_behaviour[f'dev_dependencies edition {e}'] = raw_cargo(H.format(e=e) + '[dev_dependencies]\nopensip-contracts={path="../contracts"}\n')
cargo_behaviour['both dev-dependencies and dev_dependencies same dep 2021'] = raw_cargo(H.format(e='2021') + '[dev-dependencies]\nopensip-contracts={path="../contracts"}\n[dev_dependencies]\nopensip-contracts={path="../contracts"}\n')
cargo_behaviour['both tables different deps 2021 (underscore has platform)'] = raw_cargo(H.format(e='2021') + '[dev-dependencies]\nopensip-contracts={path="../contracts"}\n[dev_dependencies]\nopensip-platform={path="../platform"}\n')
cargo_behaviour['both build tables under target 2021'] = raw_cargo(H.format(e='2021') + "[target.'cfg(unix)'.build-dependencies]\nopensip-contracts={path=\"../contracts\"}\n[target.'cfg(unix)'.build_dependencies]\nopensip-platform={path=\"../platform\"}\n")

# Allowed legacy edges: previously false refusals (ADV-3); now expected to pass with fresh metadata.
case('fresh allowed build_dependencies 2021 host->contracts', 'pass', write('crates/host', H.format(e='2021') + '[build_dependencies]\nopensip-contracts={path="../contracts"}\n'))
case('fresh allowed target dev_dependencies 2021 host->platform', 'pass', write('crates/host', H.format(e='2021') + "[target.'cfg(windows)'.dev_dependencies]\nopensip-platform={path=\"../platform\"}\n"))
case('fresh allowed legacy alias optional? (dev) host dto->contracts 2018', 'pass', write('crates/host', H.format(e='2018') + '[dev_dependencies]\ndto={package="opensip-contracts",path="../contracts"}\n'))
# Duplicate hyphen+underscore tables.
case('fresh both dev tables same allowed dep 2021', 'pass', write('crates/host', H.format(e='2021') + '[dev-dependencies]\nopensip-contracts={path="../contracts"}\n[dev_dependencies]\nopensip-contracts={path="../contracts"}\n'))
case('fresh both dev tables, forbidden only in underscore 2021', 'refused', write('crates/contracts', K.format(e='2021') + '[dev-dependencies]\n[dev_dependencies]\nopensip-host={path="../host"}\n'))
case('fresh both build tables, forbidden only in hyphen 2021', 'refused', write('crates/contracts', K.format(e='2021') + '[build-dependencies]\nopensip-host={path="../host"}\n[build_dependencies]\n'))
case('stale both dev tables, forbidden only in underscore 2021', 'forbidden manifest internal edge', write('crates/contracts', K.format(e='2021') + '[dev-dependencies]\n[dev_dependencies]\nopensip-host={path="../host"}\n'), stale=True)
case('stale both target build tables, forbidden only in underscore 2021', 'forbidden manifest internal edge', write('crates/contracts', K.format(e='2021') + "[target.'cfg(unix)'.build-dependencies]\n[target.'cfg(unix)'.build_dependencies]\nopensip-host={path=\"../host\"}\n"), stale=True)
case('stale both dev tables differing allowed deps 2021', 'refused', write('crates/host', H.format(e='2021') + '[dev-dependencies]\nopensip-contracts={path="../contracts"}\n[dev_dependencies]\nopensip-platform={path="../platform"}\n'), stale=True)
# Other editions, stale.
for e in ('2015', '2018', '2021'):
    case(f'stale forbidden dev_dependencies edition {e}', 'forbidden manifest internal edge', write('crates/contracts', K.format(e=e) + '[dev_dependencies]\nopensip-host={path="../host"}\n'), stale=True)
    case(f'stale forbidden target build_dependencies edition {e}', 'forbidden manifest internal edge', write('crates/contracts', K.format(e=e) + "[target.x86_64-pc-windows-msvc.build_dependencies]\nopensip-host={path=\"../host\"}\n"), stale=True)
case('stale forbidden legacy alias spoof optional 2021', 'forbidden manifest internal edge', write('crates/reporting', '[package]\nname="opensip-reporting"\nversion="0.1.0"\nedition="2021"\n[dev_dependencies]\nopensip-contracts={package="opensip-host",path="../host",optional=true}\n'), stale=True)
case('stale edition2024 legacy table (cargo would reject)', 'refused', write('crates/contracts', K.format(e='2024') + '[dev_dependencies]\nopensip-host={path="../host"}\n'), stale=True)
case('stale legacy pathless internal owner 2021', 'refused', write('crates/contracts', K.format(e='2021') + '[build_dependencies]\nopensip-host="0.1.0"\n'), stale=True)
case('stale legacy workspace inheritance 2021', 'must not inherit workspace values', write('crates/host', H.format(e='2021') + '[dev_dependencies]\nopensip-contracts={workspace=true}\n'), stale=True)

print(json.dumps({'cargoBehaviour': cargo_behaviour, 'results': results}, indent=1))

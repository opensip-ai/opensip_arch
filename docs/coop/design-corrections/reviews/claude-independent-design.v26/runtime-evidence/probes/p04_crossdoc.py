"""Probe 04 — independent cross-document consistency checks the author counts do not establish."""
import json, os, re, hashlib

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
OUT = {}


def read(p):
    return open(os.path.join(ROOT, p), 'rb').read().decode('utf-8')


# --- A. quarantine reason vocabulary: three reported vs two durably representable ---
sql = read('docs/coop/design-corrections/security/grant-journal.carrier.v3.sql')
m = re.search(r"reason\s+TEXT NOT NULL CHECK \(reason IN \(([^)]*)\)\)", sql)
ddl_reasons = sorted(re.findall(r"'([^']+)'", m.group(1))) if m else None
ro = read('docs/v2/architecture/commit-recovery-readonly.v3.md')
sec = read('docs/v2/contracts/product-v1/security-and-lifecycle.md')
reported = sorted(set(re.findall(r'`(uncertainTailLoss|witnesslessRestore|witnessMalformed)`', ro + sec)))
OUT['A_quarantine_reason_vocab'] = {
    'ddl_carrier_quarantine_reason_enum': ddl_reasons,
    'reported_quarantine_reasons_in_owners': reported,
    'reported_not_durably_representable': sorted(set(reported) - set(ddl_reasons or [])),
    'readonly_writes_marker': 'any quarantine-marker write' in ro and 'Prohibited' in ro,
}

# --- B. CarrierMigrationIntentV1 vs fresh-install path ---
cm = read('docs/coop/design-corrections/security/carrier-migration.v1.md')
cd = json.loads(read('docs/coop/design-corrections/security/carrier-dispatch.v3.json'))
OUT['B_fresh_install_vs_intent'] = {
    'intent_observedFormat_domain': re.search(r'observedFormat:\s*(.*?)\s*,', cm).group(1),
    'intent_firstGeneration_domain': re.search(r'firstGeneration:\s*(.*?)\s*,', cm).group(1),
    'intent_validated_before': cd['migration']['intentIsNotPersisted'],
    'freshInstall_first_generation': cd['openDispatch']['freshInstallPath']['carrierFormatRow'],
    'freshInstall_acts': cd['openDispatch']['freshInstallPath']['acts'],
    'recoveryByPrefix_empty': cd['migration']['recoveryByPrefix']['empty'],
    'ddl_first_generation_check': re.search(r'first_generation\s+INTEGER NOT NULL CHECK \(([^)]*\))', sql).group(1),
}

# --- C. repository file inventory: count, uniqueness, naming rules, generated coverage ---
inv = json.loads(read('docs/v2/architecture/repository-file-inventory.v1.json'))
OUT['C_inventory_shape'] = {'topKeys': sorted(inv.keys())}
files = inv.get('files') or inv.get('entries') or []
OUT['C_inventory_shape']['fileCount'] = len(files)
if files:
    OUT['C_inventory_shape']['sampleRowKeys'] = sorted(files[0].keys())
    paths = [f.get('path') for f in files]
    OUT['C_inventory_shape']['uniquePaths'] = len(set(paths)) == len(paths)
    groups = sorted({f.get('package') or f.get('group') for f in files})
    OUT['C_inventory_shape']['groups'] = groups
    OUT['C_inventory_shape']['groupCount'] = len(groups)

json.dump(OUT, open('/tmp/opensip-design-corrections/claude-independent-design.v26/probes/p04-result.json', 'w'), indent=1)
print(json.dumps(OUT, indent=1)[:6000])

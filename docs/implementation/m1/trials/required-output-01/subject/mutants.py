"""Behavioral controls in fresh copies; parser/tool failures are not kills."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
source = (HERE/'output_finalization.py').read_text()
controls = [
    ('capacity-disabled', 'len(raw) > ENVELOPE_MAX_BYTES', 'len(raw) > ENVELOPE_MAX_BYTES * 2', 'test_capacity_failure_never_emits_or_truncates'),
    ('capacity-off-by-one', 'len(raw) > ENVELOPE_MAX_BYTES', 'len(raw) >= ENVELOPE_MAX_BYTES', 'test_exact_capacity_boundary_standin'),
    ('interrupted-overrides-output-fault', 'termination = self.output_fault if failed else self.aggregate', 'termination = self.output_fault if failed and self.aggregate["class"] != "interrupted" else self.aggregate', 'test_capacity_failure_never_emits_or_truncates'),
    ('flush-omitted', '            writer.flush()', '            pass # mutant: no required flush', 'test_stream_prefix_and_complete_flush_failure'),
    ('partial-write-treated-complete', 'while offset < len(raw):', 'if offset < len(raw):', 'test_success_preserves_each_aggregate_and_complete_bytes'),
    ('termination-join-removed', 'if envelope.get("termination") != self.aggregate:', 'if False:', 'test_aggregate_and_exit_join_failure_before_write'),
    ('exit-join-removed', 'if envelope.get("exitCode") != self.class_to_exit[self.aggregate["class"]]:', 'if False:', 'test_aggregate_and_exit_join_failure_before_write'),
    ('second-delivery-permitted', 'if self.committed is not None:', 'if False:', 'test_after_commit_events_are_byte_identical_and_no_second_delivery'),
    ('diagnostic-on-normal-stream', 'self._write_all(diagnostic_writer, DIAGNOSTIC)', 'self._write_all(writer, DIAGNOSTIC)', 'test_capacity_failure_never_emits_or_truncates'),
]
scratch = Path(tempfile.mkdtemp(prefix='opensip-required-output-controls-'))
rows = []
for name, old, new, witness in controls:
    assert source.count(old) == 1, name
    altered = source.replace(old,new)
    compile(altered, name, 'exec')
    target = scratch/name
    shutil.copytree(HERE, target)
    (target/'output_finalization.py').write_text(altered)
    proc = subprocess.run([sys.executable,'-I','-B',str(target/'check.py')], cwd=target, capture_output=True, text=True, timeout=40)
    # The named assertion must fail, not merely a crash or an unrelated check.
    caught = proc.returncode == 1 and ('FAIL: '+witness+' ') in proc.stderr and 'ERROR:' not in proc.stderr
    rows.append({'id':name,'witness':witness,'caught':caught,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
    print(name,caught,flush=True)
record = {'standing':'Root reference mutation evidence, not independent review','total':len(rows),'caught':sum(r['caught'] for r in rows),'scratch':str(scratch),'rows':rows}
(HERE/'mutant-results.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(0 if record['caught']==record['total'] else 1)

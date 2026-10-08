from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product/crates/operability/src')
p=P/'transport.rs';s=p.read_text()
s=s.replace('    /// Producer drop tallies, reason-major', '''    /// Harness descriptor outcomes, absent unless admission succeeded.
    pub harness_admitted: bool,
    pub harness_written: [u64; LEVELS],
    pub harness_failed: [u64; LEVELS],
    pub harness_abandoned: [u64; LEVELS],
    pub harness_stopped: [u64; LEVELS],
    pub harness_error: Option<crate::writer::CapturedError>,
    pub harness_marker: Option<crate::marker::MarkerOutcome>,
    /// Producer drop tallies, reason-major''')
s=s.replace('    frozen: Option<Frozen>,','    #[cfg(feature = "harness-instrumentation")]\n    harness: Option<Arc<crate::harness_writer::HarnessSink>>,\n    frozen: Option<Frozen>,',1)
s=s.replace('        // The key is copied', '''        #[cfg(feature = "harness-instrumentation")]
        let harness = match opensip_platform::admit_harness_descriptor() {
            Ok(output) => match crate::harness_writer::HarnessSink::start(
                output, Arc::clone(&enqueue_open), Arc::clone(&drops), Arc::clone(&in_flight),
            ) {
                Ok(sink) => Some(sink),
                Err(_) => { wipe(&mut key); return Err(LoggingUnavailable); }
            },
            Err(_) => None,
        };
        // The key is copied''',1)
s=s.replace('            frozen: None,','            #[cfg(feature = "harness-instrumentation")]\n            harness,\n            frozen: None,',1)
s=s.replace('pub(crate) struct SettleView {','''/// Start for an owning request, admitting its harness opening record before
/// any ordinary producer can enqueue on that sink.
pub fn start_for_request(scope: crate::scope::RequestScope) -> Option<Result<CapabilitySet, LoggingUnavailable>> {
    let result = start();
    #[cfg(feature = "harness-instrumentation")]
    if let Some(Ok(set)) = result.as_ref() { open_harness(scope, set); }
    #[cfg(not(feature = "harness-instrumentation"))]
    let _scope = scope;
    result
}

#[cfg(feature = "harness-instrumentation")]
fn open_harness(scope: crate::scope::RequestScope, set: &CapabilitySet) {
    use crate::kinds::registry::{Event, LogStreamOpened};
    let sink = { let slot = lock_slot(); slot.as_ref().and_then(|runtime| runtime.harness.clone()) };
    let Some(sink) = sink else { return; };
    if !sink.begin_opening() { return; }
    let Some(flight) = InFlightGuard::enter() else { return; };
    flight.armed();
    if !admission_is_open() { add_drop(REASON_DRAIN_ABANDONED, Level::Info); return; }
    if !take_budget(scope.request().bytes(), 3) { add_drop(REASON_BUDGET, Level::Info); return; }
    let Some(reservation) = sink.reserve_opening(LogStreamOpened::MAX_LINE) else {
        add_drop(REASON_QUEUE_FULL, Level::Info); return;
    };
    let record = set.process_id_mint().pid(std::process::id())
        .and_then(|pid| crate::emit::encode_harness_opened(scope, pid));
    let Some(record) = record.filter(|record| record.bytes().len() <= LogStreamOpened::MAX_LINE) else {
        add_drop(REASON_REFUSED, Level::Info); return;
    };
    {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else { return; };
        if runtime.frozen.is_some() || !runtime.enqueue_open.load(Ordering::Acquire) {
            return;
        }
        sink.source_increment(scope.request(), Level::Info);
    }
    sink.push(record, reservation, Level::Info);
    sink.finish_opening();
}

pub(crate) struct SettleView {''',1)
s=s.replace('    pub(crate) stderr: Arc<crate::dev_writer::DevSink>,\n}', '    pub(crate) stderr: Arc<crate::dev_writer::DevSink>,\n    #[cfg(feature = "harness-instrumentation")]\n    pub(crate) harness: Option<Arc<crate::harness_writer::HarnessSink>>,\n}',1)
s=s.replace('            stderr: Arc::clone(&runtime.stderr),','            stderr: Arc::clone(&runtime.stderr),\n            #[cfg(feature = "harness-instrumentation")]\n            harness: runtime.harness.clone(),',1)
s=s.replace('        true\n    }\n}\n\n/// Poll owning', '''        #[cfg(feature = "harness-instrumentation")]
        if self.harness.as_ref().is_some_and(|sink| !sink.settled()) { return false; }
        true
    }
}

/// Poll owning''',1)
s=s.replace('    #[cfg(feature = "operability-dev-sinks")]\n    let stderr_enqueued', '''    #[cfg(feature = "harness-instrumentation")]
    let harness_snapshot = runtime.harness.as_ref().map(|sink| sink.cell.load()).unwrap_or_default();
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_snapshot = crate::writer::Outcomes::default();
    #[cfg(feature = "harness-instrumentation")]
    let harness_enqueued = runtime.harness.as_ref().map(|sink| sink.enqueued()).unwrap_or([0; LEVELS]);
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_enqueued = [0; LEVELS];
    #[cfg(feature = "operability-dev-sinks")]
    let stderr_enqueued''',1)
s=s.replace('    let stderr_abandoned =', '''    #[cfg(feature = "harness-instrumentation")]
    let harness_marker = runtime.harness.as_ref().map(|sink| sink.marker.freeze());
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_marker = None;
    let harness_admitted = harness_marker.is_some();
    let harness_abandoned = std::array::from_fn(|index| harness_enqueued[index].saturating_sub(
        harness_snapshot.written[index].saturating_add(harness_snapshot.failed[index]).saturating_add(harness_snapshot.stopped[index])));
    let stderr_abandoned =''',1)
s=s.replace('        stderr_marker,\n        drops,','''        stderr_marker,
        harness_admitted,
        harness_written: harness_snapshot.written,
        harness_failed: harness_snapshot.failed,
        harness_stopped: harness_snapshot.stopped,
        harness_error: harness_snapshot.first_error,
        harness_abandoned,
        harness_marker,
        drops,''',1)
s=s.replace('        runtime.stderr.begin_finalize(deadline);','''        runtime.stderr.begin_finalize(deadline);
        #[cfg(feature = "harness-instrumentation")]
        if let Some(sink) = runtime.harness.as_ref() { sink.begin_finalize(deadline); }''',1)
s=s.replace('    runtime.enqueue_open.store(false, Ordering::Release);','''    #[cfg(feature = "harness-instrumentation")]
    if let Some(sink) = runtime.harness.as_ref() { sink.gate.store(false, Ordering::Release); }
    runtime.enqueue_open.store(false, Ordering::Release);''',1)
s=s.replace('    let Some(records) = encode() else {','''    #[cfg(feature = "harness-instrumentation")]
    let harness_hold = if level.admits_ring() {
        let sink = { let slot = lock_slot(); slot.as_ref().and_then(|runtime| runtime.harness.clone()) };
        if let Some(sink) = sink {
            if !sink.opened() { add_drop(REASON_REFUSED, level); return; }
            let Some(reservation) = sink.reserve(max_line, level) else {
                add_drop(REASON_QUEUE_FULL, level); return;
            };
            Some((sink, reservation))
        } else { None }
    } else { None };
    let Some(records) = encode() else {''',1)
s=s.replace('    #[cfg(test)]\n    producer_tests::pause(producer_tests::Point::BeforePush);','''    #[cfg(feature = "harness-instrumentation")]
    if let Some((sink, _)) = harness_hold.as_ref() {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else { return; };
        if runtime.frozen.is_some() { saturating_increment(&runtime.post_freeze_sources[level.index()]); }
        else { sink.source_increment(request, level); }
    }
    #[cfg(test)]
    producer_tests::pause(producer_tests::Point::BeforePush);''',1)
s=s.replace('        sink.push(records.human, reservation, level);\n    }','''        sink.push(records.human, reservation, level);
    }
    #[cfg(feature = "harness-instrumentation")]
    if let Some((sink, reservation)) = harness_hold
        && let Some(record) = records.ring {
        sink.push(record, reservation, level);
    }''',1)
p.write_text(s)
p=P/'lib.rs';s=p.read_text().replace('finalize, start};','finalize, start, start_for_request};');p.write_text(s)
p=P/'writer.rs';s=p.read_text().replace('#[cfg(feature = "operability-dev-sinks")]','#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]');p.write_text(s)

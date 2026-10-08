from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product')
p=P/'crates/host/src/outcomes.rs';s=p.read_text()
s=s.replace('    /// Held for its owners. O1-a calls no mint (M3-O1 item 8).','    /// The process start capability set, held only by its owning host.')
s=s.replace('    logging_unavailable: Option<opensip_operability::LoggingUnavailable>,','''    logging_unavailable: Option<opensip_operability::LoggingUnavailable>,
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    request_span: std::sync::Mutex<Option<opensip_operability::RequestSpan>>,
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    phase_error: std::sync::Mutex<Option<opensip_operability::PhaseError>>,''',1)
s=s.replace('        match opensip_operability::start() {\n            Some(Ok(set)) => self.capabilities = Some(set),','''        let scope = self.authority.logging_scope(&context)
            .expect("the authority owns the request it just reserved");
        match opensip_operability::start_for_request(scope) {
            Some(Ok(set)) => {
                self.capabilities = Some(set);
                #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
                match opensip_operability::RequestSpan::begin(scope) {
                    Ok(span) => *self.request_span.lock().unwrap_or_else(|e| e.into_inner()) = Some(span),
                    Err(error) => self.record_phase_error(error),
                }
            },''',1)
pos=s.index('    /// `true` when logging start failed')
s=s[:pos]+'''    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    fn record_phase_error(&self, error: opensip_operability::PhaseError) {
        let mut first = self.phase_error.lock().unwrap_or_else(|e| e.into_inner());
        if first.is_none() { *first = Some(error); }
    }
    /// Observe the metadata delivery preparation actually owned by this ingress.
    /// Required final envelope projection and physical output remain after the freeze.
    pub(crate) fn prepare_delivery<T>(
        &self, context: &RequestContext,
        action: impl FnOnce() -> Result<T, MetadataError>,
    ) -> Result<T, MetadataError> {
        self.request_id(context)?;
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        let held = self.request_span.lock().unwrap_or_else(|e| e.into_inner());
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        let delivery = held.as_ref().and_then(|root| match root.start(opensip_operability::Phase::Delivery) {
            Ok(span) => Some(span), Err(error) => { self.record_phase_error(error); None }
        });
        let result = action();
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        if let Some(delivery) = delivery {
            let outcome = if result.is_ok() { opensip_operability::PhaseOutcome::Completed }
                else { opensip_operability::PhaseOutcome::Failed };
            if let Err(error) = delivery.finish(outcome) { self.record_phase_error(error); }
        }
        result
    }
    pub(crate) fn finish_logging(&self, failed: bool) {
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        {
            let root = self.request_span.lock().unwrap_or_else(|e| e.into_inner()).take();
            if let Some(root) = root {
                let outcome = if failed { opensip_operability::PhaseOutcome::Failed }
                    else { opensip_operability::PhaseOutcome::Completed };
                if let Err(error) = root.finish(outcome) { self.record_phase_error(error); }
            }
        }
        #[cfg(not(any(feature = "operability-dev-sinks", feature = "harness-instrumentation")))]
        let _failed = failed;
        crate::finalize_invocation(false);
    }
''' + s[pos:]
# Delivery-failure validates its owning context before consuming a span.
s=s.replace('        crate::finalize_invocation(false);\n        let request_id = self','        let request_id = self',1)
s=s.replace('        let detail = json!({"code":"DELIVERY.REQUIRED_PROJECTION_FAILED"','        self.prepare_delivery(context, || Ok(()))?;\n        self.finish_logging(true);\n        let detail = json!({"code":"DELIVERY.REQUIRED_PROJECTION_FAILED"',1)
# Factor actual metadata preparation into an observed closure, keeping final projection after freeze.
a=s.index('        let request_id = self\n',s.index('    pub fn execute('));b=s.index('        if let Some(bytes) = completion_bytes {',a)
prep=s[a:b]
s=s[:a]+'''        let (envelope, completion_bytes) = self.prepare_delivery(context, || {
'''+prep+'''            Ok((envelope, completion_bytes))
        })?;
        self.finish_logging(false);
'''+s[b:]
s=s.replace('            crate::finalize_invocation(false);\n            return Ok(RenderedResponse','            return Ok(RenderedResponse',1)
s=s.replace('        crate::finalize_invocation(false);\n        let exit_code','        let exit_code',1)
p.write_text(s)
p=P/'crates/host/src/doctor_ingress.rs';s=p.read_text();s=s.replace('        crate::finalize_invocation(false);\n        doctor_response','        self.prepare_delivery(context, || Ok(()))?;\n        self.finish_logging(false);\n        doctor_response',1);p.write_text(s)

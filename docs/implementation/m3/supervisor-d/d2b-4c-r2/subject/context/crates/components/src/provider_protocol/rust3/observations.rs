//! RUST3-PROVIDER-FAULT's worker-observed possible-phase window. The host
//! may have sent more frames since the last worker frame: its current phase
//! alone is not the worker's necessarily observed phase. Correlation and
//! phase are one joint observation, never independently nullable choices.
use super::super::cbor::Value;
use super::super::table::Run;
use super::super::ts2::carrier::{CARRIERS, field};
use opensip_identity::{JsonValue as J, parse_json};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct Observation {
    phase: String,
    execution_id: Option<String>,
    analysis_ordinal: Option<u64>,
}
/// One receive-side mechanism, not complete frame admission. The codec
/// calls this only after its own schema/context/table checks of each event.
/// A matching observation never authorizes an event outside P3T's phase.
#[derive(Debug, Clone)]
pub struct ProviderFaultWindow {
    host_frames: BTreeSet<String>,
    phases: BTreeSet<String>,
    hello_seen: bool,
    execution_id: Option<String>,
    analysis_ordinal: Option<u64>,
    observations: BTreeSet<Observation>,
}
fn at<'v>(value: &'v J, keys: &[&str]) -> Option<&'v J> {
    keys.iter().try_fold(value, |value, key| match value {
        J::Object(fields) => fields.get(*key),
        _ => None,
    })
}
fn text(value: &J) -> Option<&str> {
    match value {
        J::String(s) => Some(s),
        _ => None,
    }
}
impl ProviderFaultWindow {
    pub fn new() -> Result<Self, String> {
        let doc = parse_json(CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        let Some(J::Array(rules)) = at(&doc, &["admission"]) else {
            return Err("admission rules".to_owned());
        };
        let rule = rules
            .iter()
            .find(|rule| at(rule, &["id"]).and_then(text) == Some("RUST3-PROVIDER-FAULT"))
            .ok_or("fault rule")?;
        let expected=parse_json(br#"{"phaseSemantics":"worker-observed","hostAdmission":"possible-phase-set","anchorFrame":"last-admitted-worker-frame","nullLaw":{"executionId":"OpenUniverse","analysisOrdinal":"Analyze"},"jointConsistency":true,"readHelloFirst":true,"d9Equivalence":{"ownerTerminalKind":"provider-fault","refusedPayloadTerminalKind":"fault"}}"#).map_err(|_|"expected law")?;
        if at(rule, &["params"]) != Some(&expected) {
            return Err("unimplemented ProviderFault observation law".to_owned());
        }
        let Some(J::Array(frames)) = at(&doc, &["protocols", "rust-semantic", "frames"]) else {
            return Err("Rust3 frames".to_owned());
        };
        let host_frames = frames
            .iter()
            .filter(|frame| at(frame, &["direction"]).and_then(text) == Some("host-to-worker"))
            .map(|frame| {
                at(frame, &["frameType"])
                    .and_then(text)
                    .map(str::to_owned)
                    .ok_or("host frame")
            })
            .collect::<Result<BTreeSet<_>, _>>()?;
        let Some(J::Array(members)) = at(&doc, &["records", "Rust3ProviderFaultV2", "members"])
        else {
            return Err("ProviderFault fields".to_owned());
        };
        let phase = members
            .iter()
            .find(|member| at(member, &["name"]).and_then(text) == Some("phase"))
            .ok_or("phase member")?;
        let Some(J::Array(values)) = at(phase, &["type", "enum"]) else {
            return Err("phase vocabulary".to_owned());
        };
        let phases = values
            .iter()
            .map(|value| text(value).map(str::to_owned).ok_or("phase text"))
            .collect::<Result<BTreeSet<_>, _>>()?;
        if phases.len() != values.len() || phases.contains("START") {
            return Err("fault phase vocabulary".to_owned());
        }
        Ok(Self {
            host_frames,
            phases,
            hello_seen: false,
            execution_id: None,
            analysis_ordinal: None,
            observations: BTreeSet::new(),
        })
    }
    /// Record the table state after a host frame has been admitted for send.
    /// This includes the post-Hello point, but never a pre-Hello prefix.
    pub fn host_sent(&mut self, run: &Run<'_>, name: &str, payload: &Value) -> Result<(), String> {
        if !self.host_frames.contains(name) {
            return Err("not a Rust3 host frame".to_owned());
        }
        if !self.hello_seen && name != "Hello" {
            return Err("the worker reads Hello first".to_owned());
        }
        if run.phase() == "FAULT" || run.phase() == "START" {
            return Err("host frame was not admitted by its table".to_owned());
        }
        let Value::Map(fields) = payload else {
            return Err("host payload".to_owned());
        };
        let mut execution = self.execution_id.clone();
        let mut ordinal = self.analysis_ordinal;
        if name == "OpenUniverse" {
            let Some(Value::Text(value)) = field(fields, "executionId") else {
                return Err("OpenUniverse executionId".to_owned());
            };
            execution = Some(value.clone());
        }
        if name == "Analyze" {
            let Some(Value::Unsigned(value)) = field(fields, "analysisOrdinal") else {
                return Err("Analyze analysisOrdinal".to_owned());
            };
            ordinal = Some(*value);
        }
        self.hello_seen = true;
        self.execution_id = execution;
        self.analysis_ordinal = ordinal;
        self.add(run.phase());
        Ok(())
    }
    /// An admitted worker frame anchors a new window. Old host prefixes
    /// before that observation cannot explain a later ProviderFault.
    pub fn worker_admitted(&mut self, run: &Run<'_>) {
        self.observations.clear();
        if self.hello_seen {
            self.add(run.phase());
        }
    }
    fn add(&mut self, phase: &str) {
        if self.phases.contains(phase) {
            self.observations.insert(Observation {
                phase: phase.to_owned(),
                execution_id: self.execution_id.clone(),
                analysis_ordinal: self.analysis_ordinal,
            });
        }
    }
    /// Joint phase/null-or-echo consistency, after closed ProviderFault
    /// shape validation. This does not step or bypass the actual table.
    pub fn matches(&self, payload: &Value) -> bool {
        if !self.hello_seen {
            return false;
        }
        let Value::Map(fields) = payload else {
            return false;
        };
        let Some(Value::Text(phase)) = field(fields, "phase") else {
            return false;
        };
        let execution = match field(fields, "executionId") {
            Some(Value::Null) => None,
            Some(Value::Text(value)) => Some(value.clone()),
            _ => return false,
        };
        let ordinal = match field(fields, "analysisOrdinal") {
            Some(Value::Null) => None,
            Some(Value::Unsigned(value)) => Some(*value),
            _ => return false,
        };
        self.observations.contains(&Observation {
            phase: phase.clone(),
            execution_id: execution,
            analysis_ordinal: ordinal,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::super::schemas::Rust3PayloadSchemas;
    use super::*;
    use crate::provider_protocol::table::{Event, Protocol, Table};
    fn payload(fields: Vec<(&str, Value)>) -> Value {
        Value::Map(
            fields
                .into_iter()
                .map(|(name, value)| (name.to_owned(), value))
                .collect(),
        )
    }
    fn fault(phase: &str, execution: Option<&str>, ordinal: Option<u64>) -> Value {
        payload(vec![
            ("phase", Value::Text(phase.to_owned())),
            (
                "executionId",
                execution
                    .map(|s| Value::Text(s.to_owned()))
                    .unwrap_or(Value::Null),
            ),
            (
                "analysisOrdinal",
                ordinal.map(Value::Unsigned).unwrap_or(Value::Null),
            ),
            ("faultKind", Value::Text("internal-invariant".to_owned())),
            ("detailCode", Value::Text("fixture".to_owned())),
        ])
    }
    fn step(run: &mut Run<'_>, frame: &str) {
        let mut event = Event::frame(frame);
        event.identity_negotiated = true;
        event.dependency_mode = true;
        event.stage_count = 1;
        run.step(&event);
        assert_ne!(run.phase(), "FAULT", "{frame}");
    }
    fn host(run: &mut Run<'_>, window: &mut ProviderFaultWindow, frame: &str, value: &Value) {
        step(run, frame);
        window.host_sent(run, frame, value).unwrap();
    }
    fn worker(run: &mut Run<'_>, window: &mut ProviderFaultWindow, frame: &str) {
        step(run, frame);
        window.worker_admitted(run);
    }
    #[test]
    fn provider_fault_uses_joint_worker_prefixes_until_the_next_admitted_worker_frame() {
        let table = Table::load(Protocol::Rust3).unwrap();
        let mut run = table.start();
        let mut window = ProviderFaultWindow::new().unwrap();
        let schemas = Rust3PayloadSchemas::load().unwrap();
        assert!(!window.matches(&fault("WAIT_HELLO_ACK", None, None)));
        host(&mut run, &mut window, "Hello", &payload(Vec::new()));
        assert!(window.matches(&fault("WAIT_HELLO_ACK", None, None)));
        worker(&mut run, &mut window, "HelloAck");
        host(
            &mut run,
            &mut window,
            "OpenUniverse",
            &payload(vec![("executionId", Value::Text("execution".to_owned()))]),
        );
        for (phase, execution, accepted) in [
            ("READY_OPEN_UNIVERSE", None, true),
            ("WAIT_UNIVERSE_ACCEPTED", Some("execution"), true),
            ("READY_OPEN_UNIVERSE", Some("execution"), false),
            ("WAIT_UNIVERSE_ACCEPTED", None, false),
        ] {
            let value = fault(phase, execution, None);
            schemas
                .check_payload("ProviderFault", &value, run.phase(), false)
                .unwrap();
            assert_eq!(window.matches(&value), accepted, "{phase} {execution:?}");
        }
        worker(&mut run, &mut window, "UniverseAccepted");
        assert!(window.matches(&fault("READY_SNAPSHOT_MANIFEST", Some("execution"), None)));
        assert!(!window.matches(&fault("WAIT_UNIVERSE_ACCEPTED", Some("execution"), None)));
        assert!(!window.matches(&fault("READY_OPEN_UNIVERSE", None, None)));
    }
    #[test]
    fn provider_fault_analyze_nullability_stays_correlated_and_chunks_do_not_grow_the_set() {
        let table = Table::load(Protocol::Rust3).unwrap();
        let mut run = table.start();
        let mut window = ProviderFaultWindow::new().unwrap();
        let empty = payload(Vec::new());
        host(&mut run, &mut window, "Hello", &empty);
        worker(&mut run, &mut window, "HelloAck");
        host(
            &mut run,
            &mut window,
            "OpenUniverse",
            &payload(vec![("executionId", Value::Text("execution".to_owned()))]),
        );
        worker(&mut run, &mut window, "UniverseAccepted");
        host(&mut run, &mut window, "SnapshotManifest", &empty);
        let before = window.observations.len();
        for _ in 0..100 {
            host(&mut run, &mut window, "SnapshotFileChunk", &empty);
        }
        assert_eq!(window.observations.len(), before);
        host(&mut run, &mut window, "SnapshotSeal", &empty);
        worker(&mut run, &mut window, "SnapshotAccepted");
        host(&mut run, &mut window, "DependencySourceManifest", &empty);
        host(&mut run, &mut window, "DependencySourceSeal", &empty);
        worker(&mut run, &mut window, "DependencySourceAccepted");
        worker(&mut run, &mut window, "NativeContextVerified");
        assert_eq!(run.phase(), "READY_ANALYZE");
        host(
            &mut run,
            &mut window,
            "Analyze",
            &payload(vec![("analysisOrdinal", Value::Unsigned(24))]),
        );
        assert!(window.matches(&fault("READY_ANALYZE", Some("execution"), None)));
        assert!(window.matches(&fault("ANALYZING", Some("execution"), Some(24))));
        assert!(!window.matches(&fault("READY_ANALYZE", Some("execution"), Some(24))));
        assert!(!window.matches(&fault("ANALYZING", Some("execution"), None)));
        assert!(!window.matches(&fault("ANALYZING", None, Some(24))));
        worker(&mut run, &mut window, "FactBatch");
        assert!(!window.matches(&fault("READY_ANALYZE", Some("execution"), None)));
        assert!(window.matches(&fault("ANALYZING", Some("execution"), Some(24))));
    }
    #[test]
    fn provider_fault_before_hello_or_with_mixed_correlation_never_enters_the_window() {
        let table = Table::load(Protocol::Rust3).unwrap();
        let mut run = table.start();
        let mut window = ProviderFaultWindow::new().unwrap();
        let empty = payload(Vec::new());
        assert!(
            window
                .host_sent(
                    &run,
                    "OpenUniverse",
                    &payload(vec![("executionId", Value::Text("execution".to_owned()))])
                )
                .is_err()
        );
        assert!(!window.hello_seen);
        host(&mut run, &mut window, "Hello", &empty);
        assert!(!window.matches(&fault("WAIT_HELLO_ACK", Some("execution"), None)));
        assert!(!window.matches(&fault("WAIT_HELLO_ACK", None, Some(0))));
        let value = fault("WAIT_HELLO_ACK", None, None);
        let wrong = match value {
            Value::Map(mut fields) => {
                fields
                    .iter_mut()
                    .find(|(key, _)| key == "analysisOrdinal")
                    .unwrap()
                    .1 = Value::Bool(false);
                Value::Map(fields)
            }
            _ => unreachable!(),
        };
        assert!(!window.matches(&wrong));
    }
}

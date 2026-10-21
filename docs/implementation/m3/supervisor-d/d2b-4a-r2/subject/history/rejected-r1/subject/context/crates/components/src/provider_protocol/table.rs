//! M3-D r5 item 10 (unit D2b-2; LD-D2B-4): the provider transition tables as
//! data, and the one engine that interprets them.
//!
//! The rows are the published tables' own: P3T's 34 (`protocol3-transitions.v1.json`)
//! with the carriers' Rust overlay (`schemas/wire/native-carriers-v1.json`
//! `protocols.rust-semantic.transitions`, published as
//! `p3-guard-successor.v1.json`), and T2O's 23 (`typescript-protocol2-order.v1.json`).
//! The two base tables are byte copies under `crates/components/data/`,
//! checked against the carriers' own `sourcePins` (`p3`, `ts2order`) when
//! they load. No row is copied into code.
//!
//! The laws the tables state in prose (the pre-match law, the state updates
//! and the stage-dependent next) are implemented here, and loading pins
//! every such text: a table whose prose names a law this engine does not
//! implement refuses to load rather than being interpreted loosely. The
//! engine is the references' (`native_evidence_model.v2.protocol3_run`,
//! `provider_startup_model.v1.typescript_protocol2_run`, trial 07's
//! `overlay_run`): the pre-match law first, in its order; then first match
//! on phase (or set wildcard), frame and guard; the total fallback; and on a
//! match the frame's state updates, the overlay's additions, the resolved
//! next, the terminal and the trace.
use opensip_identity::{JsonValue as J, digest_hex, parse_json, raw_sha256};
use std::collections::BTreeMap;

const P3T: &[u8] = include_bytes!("../../data/protocol3-transitions.v1.json");
const T2O: &[u8] = include_bytes!("../../data/typescript-protocol2-order.v1.json");
const CARRIERS: &[u8] = include_bytes!("../../../../schemas/wire/native-carriers-v1.json");

/// The two published tables.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Protocol {
    /// `rust-semantic` major 3: P3T with the Rust overlay.
    Rust3,
    /// `typescript-semantic` major 2: T2O, with no overlay.
    Ts2,
}

/// A state field's or a guard's value.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Scalar {
    Null,
    Bool(bool),
    Int(i64),
    Text(String),
}

/// Why a table did not load.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TableRefusal {
    /// A base table's bytes are not the carriers' pin.
    Pin(&'static str),
    /// The JSON is not the shape this engine reads.
    Shape(&'static str),
    /// A prose law this engine does not implement.
    Law(String),
}

/// One row.
#[derive(Debug, Clone, PartialEq, Eq)]
struct Rule {
    id: String,
    phase: String,
    frame: String,
    guard: Vec<(String, Scalar)>,
    next: String,
    terminal: Option<String>,
}

/// What a frame's state update does.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Update {
    /// `identityNegotiated` from the event's own observation.
    IdentityNegotiated,
    /// `dependencyMode` and `preparedMode` from the event's observations.
    UniverseModes,
    /// `stageCount` from the event, `stageIndex` to 0, and (T2O) `outputSeen`
    /// to false.
    Analyze { resets_output: bool },
    /// `cancelPhase` to the phase the Cancel was sent in.
    CancelPhase,
    /// Literal assignments.
    Set(Vec<(String, Scalar)>),
}

/// One loaded table: its rows, its wildcards and its laws.
#[derive(Debug, Clone)]
pub struct Table {
    protocol: Protocol,
    initial: BTreeMap<String, Scalar>,
    rules: Vec<Rule>,
    /// The set wildcard (`*PRE_COMPLETE` or `*PRE_TERMINAL`) and its phases.
    set_wildcard: (String, Vec<String>),
    process_faults: Vec<String>,
    process_fault_id: String,
    fallback_id: String,
    /// The derived event observations a guard may name (T2O).
    observations: Vec<String>,
    /// Per frame, its updates in the table's order; then the overlay's.
    updates: Vec<(Vec<String>, Update)>,
    additions: Vec<(Vec<String>, Update)>,
}

/// The phases after a terminal: only `zero-exit`, `eof` and process events
/// follow (both tables' second pre-match law).
const POST_TERMINAL: [&str; 3] = ["WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"];
const STAGE_DEPENDENT: &str = "ANALYZING_OR_READY_COMPLETE";

/// Every prose law text the engine implements, exactly as each table states
/// it. Loading compares each table's texts with these.
const P3_PRE_MATCH: [&str; 3] = [
    "FAULT is ABSORBING: once the phase is FAULT every further event is recorded as `FAULT-absorb` and nothing transitions.",
    "In WAIT_ZERO_EXIT, WAIT_EOF or DONE, any frame other than `zero-exit`, `eof` or a `*PROCESS_FAULT` member is a post-terminal frame and goes to FAULT with trace `post-terminal-frame`.",
    "Any `*PROCESS_FAULT` member goes to FAULT with trace `P3-33` from ANY phase, which is what row P3-33 states.",
];
const T2_PRE_MATCH: [&str; 3] = [
    "FAULT is absorbing: every further event is traced FAULT-absorb.",
    "In WAIT_ZERO_EXIT, WAIT_EOF or DONE any frame other than zero-exit, eof or a *PROCESS_FAULT member is a post-terminal frame: FAULT, trace post-terminal-frame.",
    "Any *PROCESS_FAULT member goes to FAULT with trace T2-22.",
];
/// Each table's stage-dependent law, exactly as it states it (r2, Codex
/// D2B2-R1-RF-1): the increment of `stageIndex` and `stagesCompleted`, then
/// READY_COMPLETE at `stageCount` and ANALYZING otherwise, which `Run::step`
/// implements.
const P3_STAGE: &str = "The `next` of row P3-24 (CoverageV3 in ANALYZING) is NOT a phase. It increments both stageIndex and stagesCompleted and then resolves to READY_COMPLETE when stageIndex equals stageCount, and to ANALYZING otherwise. Without this the table cannot be interpreted at all for a multi-stage analysis: one CoverageV3 per stage is expected, and only the last one may be followed by Complete.";
const T2_STAGE: &str = "The next of T2-13 increments stageIndex and stagesCompleted and resolves to READY_COMPLETE when stageIndex equals stageCount, otherwise ANALYZING.";
/// The carriers' TS2 transitions entry, exactly (r2, Codex D2B2-R1-RF-2): no
/// overlay, and the note that payload selection is the carrier's frame
/// precheck (D2b-4's contextual admission), which this engine does not run.
const T2_OVERLAY_NONE: &str = "none: T2-14 already guards post-Analyze Unavailable with outputSeen=false; T2-18 keeps Cancel from START (delivery2 cancelTransition).";
const T2_UNAVAILABLE_SELECTION: &str = "The carrier selects the Unavailable payload by host phase (WAIT_NATIVE_CONTEXT_VERIFIED or ANALYZING). The TS2 owner table guards T2-10/T2-14 on the payload-derived observation unavailablePayload. Outcomes are equivalent (a phase/payload mismatch faults either way), but trace ids differ: carrier selection refuses in the frame precheck, the owner table reaches T2-23.";
const P3_NO_MATCH: &str = "An event matching no row goes to FAULT with trace `P3-34`, which is what the final fallback row states. There is no default transition and no silent ignore.";
const T2_NO_MATCH: &str = "An event matching no row goes to FAULT with trace T2-23.";

fn update_for(text: &str) -> Option<Update> {
    Some(match text {
        "identityNegotiated = every identity token is present in the frame's `capabilities`"
        | "identityNegotiated = every identity token is present in the admitted capabilities" => {
            Update::IdentityNegotiated
        }
        "dependencyMode and preparedMode as HOST-DERIVED OBSERVATIONS of the admitted OpenUniverseV3 payload (derivedObservations), never frame booleans; these are the guards P3-08..P3-10 and P3-14..P3-15 select on" => {
            Update::UniverseModes
        }
        "stageCount = the invocation's stage count; stageIndex = 0" => Update::Analyze {
            resets_output: false,
        },
        "stageCount = the invocation's stage count; stageIndex = 0; outputSeen = false" => {
            Update::Analyze {
                resets_output: true,
            }
        }
        "cancelPhase = the phase in which Cancel was sent" => Update::CancelPhase,
        "sourceBytesSent = true; this is the observable that proves no source byte preceded negotiation"
        | "sourceBytesSent = true" => {
            Update::Set(vec![("sourceBytesSent".to_owned(), Scalar::Bool(true))])
        }
        "outputSeen = true" => Update::Set(vec![("outputSeen".to_owned(), Scalar::Bool(true))]),
        _ => return None,
    })
}

fn object(v: &J) -> Option<&BTreeMap<String, J>> {
    match v {
        J::Object(m) => Some(m),
        _ => None,
    }
}
fn text(v: &J) -> Option<&str> {
    match v {
        J::String(s) => Some(s),
        _ => None,
    }
}
fn texts(v: &J) -> Option<Vec<String>> {
    match v {
        J::Array(items) => items.iter().map(|i| text(i).map(str::to_owned)).collect(),
        _ => None,
    }
}
fn scalar(v: &J) -> Option<Scalar> {
    Some(match v {
        J::Null => Scalar::Null,
        J::Bool(b) => Scalar::Bool(*b),
        J::Integer(i) => Scalar::Int(i64::try_from(i.get()).ok()?),
        J::String(s) => Scalar::Text(s.clone()),
        _ => return None,
    })
}
fn assignments(v: &J) -> Option<Vec<(String, Scalar)>> {
    object(v)?
        .iter()
        .map(|(k, v)| Some((k.clone(), scalar(v)?)))
        .collect()
}

impl Table {
    /// Load `protocol`'s table: the base table checked against the carriers'
    /// pin, its prose laws checked against the engine's, and (Rust3) the
    /// carriers' overlay applied.
    pub fn load(protocol: Protocol) -> Result<Self, TableRefusal> {
        let raw = match protocol {
            Protocol::Rust3 => P3T,
            Protocol::Ts2 => T2O,
        };
        Self::load_from(protocol, raw, CARRIERS)
    }

    /// [`Table::load`] over given bytes: the embedded ones in production,
    /// altered ones in the refusal controls.
    fn load_from(protocol: Protocol, raw: &[u8], carriers: &[u8]) -> Result<Self, TableRefusal> {
        use TableRefusal::Shape;
        let carriers = parse_json(carriers).map_err(|_| Shape("carriers"))?;
        let carriers = object(&carriers).ok_or(Shape("carriers"))?;
        let (key, protocol_name) = match protocol {
            Protocol::Rust3 => ("p3", "rust-semantic"),
            Protocol::Ts2 => ("ts2order", "typescript-semantic"),
        };
        let J::Array(pins) = carriers.get("sourcePins").ok_or(Shape("sourcePins"))? else {
            return Err(Shape("sourcePins"));
        };
        let pin = pins
            .iter()
            .filter_map(object)
            .find(|p| p.get("key").and_then(text) == Some(key))
            .ok_or(Shape("the table's pin"))?;
        if pin.get("sha256").and_then(text) != Some(digest_hex(&raw_sha256(raw)).as_str())
            || pin.get("bytes").and_then(scalar) != Some(Scalar::Int(raw.len() as i64))
        {
            return Err(TableRefusal::Pin(key));
        }
        let table = parse_json(raw).map_err(|_| Shape("table"))?;
        let table = object(&table).ok_or(Shape("table"))?;
        let get = |k: &'static str| table.get(k).ok_or(Shape(k));

        let (pre_match, no_match, stage_law, set_name) = match protocol {
            Protocol::Rust3 => (P3_PRE_MATCH, P3_NO_MATCH, P3_STAGE, "*PRE_COMPLETE"),
            Protocol::Ts2 => (T2_PRE_MATCH, T2_NO_MATCH, T2_STAGE, "*PRE_TERMINAL"),
        };
        if texts(get("preMatchLaw")?).ok_or(Shape("preMatchLaw"))? != pre_match {
            return Err(TableRefusal::Law("preMatchLaw".to_owned()));
        }
        if text(get("noMatchLaw")?) != Some(no_match) {
            return Err(TableRefusal::Law("noMatchLaw".to_owned()));
        }
        let stage = object(get("stageDependentTransitions")?).ok_or(Shape("stage"))?;
        // The key and its law both: the engine's next is this law's (r2).
        if stage.keys().map(String::as_str).collect::<Vec<_>>() != [STAGE_DEPENDENT]
            || stage.get(STAGE_DEPENDENT).and_then(text) != Some(stage_law)
        {
            return Err(TableRefusal::Law("stageDependentTransitions".to_owned()));
        }

        let initial = assignments(get("initialState")?).ok_or(Shape("initialState"))?;
        let initial: BTreeMap<String, Scalar> = initial.into_iter().collect();
        let wildcards = object(get("wildcards")?).ok_or(Shape("wildcards"))?;
        let set_phases = wildcards
            .get(set_name)
            .and_then(object)
            .and_then(|w| w.get("phases"))
            .and_then(texts)
            .ok_or(Shape("set wildcard"))?;
        let process_faults = wildcards
            .get("*PROCESS_FAULT")
            .and_then(object)
            .and_then(|w| w.get("frames"))
            .and_then(texts)
            .ok_or(Shape("*PROCESS_FAULT"))?;
        let observations = match table.get("eventObservations") {
            Some(v) => object(v)
                .ok_or(Shape("eventObservations"))?
                .keys()
                .cloned()
                .collect(),
            None => Vec::new(),
        };

        let J::Array(raw_rules) = get("rules")? else {
            return Err(Shape("rules"));
        };
        let mut rules = Vec::new();
        for r in raw_rules {
            let r = object(r).ok_or(Shape("rule"))?;
            let field =
                |k: &'static str| r.get(k).and_then(text).map(str::to_owned).ok_or(Shape(k));
            rules.push(Rule {
                id: field("id")?,
                phase: field("phase")?,
                frame: field("frame")?,
                guard: match r.get("guard") {
                    Some(g) => assignments(g).ok_or(Shape("guard"))?,
                    None => Vec::new(),
                },
                next: field("next")?,
                terminal: match r.get("terminal") {
                    Some(t) => Some(text(t).ok_or(Shape("terminal"))?.to_owned()),
                    None => None,
                },
            });
        }
        if scalar(get("ruleCount")?) != Some(Scalar::Int(rules.len() as i64)) {
            return Err(Shape("ruleCount"));
        }
        let catch_all = |frame: &str| {
            rules
                .iter()
                .find(|r| r.phase == "*ANY" && r.frame == frame)
                .map(|r| r.id.clone())
                .ok_or(Shape("catch-all row"))
        };
        let process_fault_id = catch_all("*PROCESS_FAULT")?;
        let fallback_id = catch_all("*")?;

        let mut updates = Vec::new();
        let J::Array(raw_updates) = get("stateUpdates")? else {
            return Err(Shape("stateUpdates"));
        };
        for u in raw_updates {
            let u = object(u).ok_or(Shape("stateUpdate"))?;
            let frames = match (u.get("onFrame"), u.get("onFrames")) {
                (Some(f), None) => vec![text(f).ok_or(Shape("onFrame"))?.to_owned()],
                (None, Some(fs)) => texts(fs).ok_or(Shape("onFrames"))?,
                _ => return Err(Shape("stateUpdate frames")),
            };
            let sets = u.get("sets").and_then(text).ok_or(Shape("sets"))?;
            let update = update_for(sets).ok_or_else(|| TableRefusal::Law(sets.to_owned()))?;
            updates.push((frames, update));
        }

        let mut table = Self {
            protocol,
            initial,
            rules,
            set_wildcard: (set_name.to_owned(), set_phases),
            process_faults,
            process_fault_id,
            fallback_id,
            observations,
            updates,
            additions: Vec::new(),
        };
        let protocols = carriers
            .get("protocols")
            .and_then(object)
            .ok_or(Shape("protocols"))?;
        let overlay = protocols
            .get(protocol_name)
            .and_then(object)
            .and_then(|p| p.get("transitions"))
            .and_then(object)
            .ok_or(Shape("transitions"))?;
        if protocol == Protocol::Rust3 {
            table.apply_overlay(overlay)?;
        } else {
            table.check_no_overlay(overlay)?;
        }
        Ok(table)
    }

    /// The carriers' TS2 entry is closed (r2, Codex D2B2-R1-RF-2): its base
    /// is T2O with its own rule count, it declares exactly the supported
    /// no-overlay text, and it carries no other member, so no executable
    /// overlay can be declared and silently ignored.
    fn check_no_overlay(&self, overlay: &BTreeMap<String, J>) -> Result<(), TableRefusal> {
        use TableRefusal::Shape;
        for key in overlay.keys() {
            if !matches!(key.as_str(), "base" | "overlay" | "unavailableSelection") {
                return Err(TableRefusal::Law(format!("overlay {key}")));
            }
        }
        let base = overlay.get("base").and_then(object).ok_or(Shape("base"))?;
        if base.len() != 2
            || base.get("pin").and_then(text) != Some("ts2order")
            || base.get("rules").and_then(text) != Some(self.rules.len().to_string().as_str())
        {
            return Err(Shape("overlay base"));
        }
        if overlay.get("overlay").and_then(text) != Some(T2_OVERLAY_NONE) {
            return Err(TableRefusal::Law("overlay".to_owned()));
        }
        if overlay.get("unavailableSelection").and_then(text) != Some(T2_UNAVAILABLE_SELECTION) {
            return Err(TableRefusal::Law("unavailableSelection".to_owned()));
        }
        Ok(())
    }

    /// The carriers' Rust overlay: its state additions, its update
    /// additions (applied after the parent's), its guard additions, and its
    /// Cancel position, which keeps P3-29 out of START.
    fn apply_overlay(&mut self, overlay: &BTreeMap<String, J>) -> Result<(), TableRefusal> {
        use TableRefusal::Shape;
        for key in overlay.keys() {
            if !matches!(
                key.as_str(),
                "base"
                    | "precedence"
                    | "stateAdditions"
                    | "stateUpdateAdditions"
                    | "guardAdditions"
                    | "equivalence"
                    | "cancel"
                    | "terminalGuards"
                    | "custodyOrder"
            ) {
                return Err(TableRefusal::Law(format!("overlay {key}")));
            }
        }
        let base = overlay.get("base").and_then(object).ok_or(Shape("base"))?;
        if base.get("pin").and_then(text) != Some("p3")
            || base.get("rules").and_then(text) != Some(self.rules.len().to_string().as_str())
        {
            return Err(Shape("overlay base"));
        }
        let cancel = overlay
            .get("cancel")
            .and_then(object)
            .ok_or(Shape("cancel"))?;
        if cancel.get("hostMaySendInStart") != Some(&J::Bool(false)) {
            return Err(TableRefusal::Law("cancel in START".to_owned()));
        }
        for (k, v) in assignments(
            overlay
                .get("stateAdditions")
                .ok_or(Shape("stateAdditions"))?,
        )
        .ok_or(Shape("stateAdditions"))?
        {
            self.initial.insert(k, v);
        }
        let J::Array(adds) = overlay
            .get("stateUpdateAdditions")
            .ok_or(Shape("stateUpdateAdditions"))?
        else {
            return Err(Shape("stateUpdateAdditions"));
        };
        for a in adds {
            let a = object(a).ok_or(Shape("addition"))?;
            let frames = a.get("onFrames").and_then(texts).ok_or(Shape("onFrames"))?;
            let sets = a.get("sets").and_then(assignments).ok_or(Shape("sets"))?;
            self.additions.push((frames, Update::Set(sets)));
        }
        let guards = overlay
            .get("guardAdditions")
            .and_then(object)
            .ok_or(Shape("guardAdditions"))?;
        for (id, guard) in guards {
            let rule = self
                .rules
                .iter_mut()
                .find(|r| &r.id == id)
                .ok_or(Shape("guard addition row"))?;
            rule.guard
                .extend(assignments(guard).ok_or(Shape("guard addition"))?);
        }
        Ok(())
    }

    pub fn protocol(&self) -> Protocol {
        self.protocol
    }
    /// The row ids, in the declared order.
    pub fn rule_ids(&self) -> impl Iterator<Item = &str> {
        self.rules.iter().map(|r| r.id.as_str())
    }
    /// A fresh run of this table.
    pub fn start(&self) -> Run<'_> {
        Run {
            table: self,
            state: self.initial.clone(),
        }
    }
}

/// One event: a frame type, or a process observation, with the host-derived
/// observations its state update or guard reads. The codec derives them
/// from the admitted payload (LD-D2B-15); none is a wire member.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub frame: String,
    /// HelloAck: every identity token present in its capabilities.
    pub identity_negotiated: bool,
    /// OpenUniverse: the derived dependency and prepared modes.
    pub dependency_mode: bool,
    pub prepared_mode: bool,
    /// Analyze: the invocation's stage count.
    pub stage_count: i64,
    /// TS2's derived observations a guard may name (`unavailablePayload`).
    pub observations: Vec<(String, Scalar)>,
}
impl Event {
    pub fn frame(frame: &str) -> Self {
        Self {
            frame: frame.to_owned(),
            identity_negotiated: false,
            dependency_mode: false,
            prepared_mode: false,
            stage_count: 0,
            observations: Vec::new(),
        }
    }
}

/// One run's state.
#[derive(Debug, Clone)]
pub struct Run<'t> {
    table: &'t Table,
    state: BTreeMap<String, Scalar>,
}
impl Run<'_> {
    /// A state field.
    pub fn field(&self, name: &str) -> Option<&Scalar> {
        self.state.get(name)
    }
    pub fn phase(&self) -> &str {
        match self.state.get("phase") {
            Some(Scalar::Text(p)) => p,
            _ => "FAULT",
        }
    }
    fn set(&mut self, k: &str, v: Scalar) {
        self.state.insert(k.to_owned(), v);
    }
    fn int(&self, k: &str) -> i64 {
        match self.state.get(k) {
            Some(Scalar::Int(v)) => *v,
            _ => 0,
        }
    }

    /// Apply one event and return its trace entry: a row id, or
    /// `FAULT-absorb`, or `post-terminal-frame`.
    pub fn step(&mut self, event: &Event) -> String {
        let table = self.table;
        let phase = self.phase().to_owned();
        let frame = event.frame.as_str();
        let process = table.process_faults.iter().any(|f| f == frame);
        // The pre-match law, in its order.
        if phase == "FAULT" {
            return "FAULT-absorb".to_owned();
        }
        if POST_TERMINAL.contains(&phase.as_str())
            && frame != "zero-exit"
            && frame != "eof"
            && !process
        {
            self.set("phase", Scalar::Text("FAULT".to_owned()));
            return "post-terminal-frame".to_owned();
        }
        if process {
            self.set("phase", Scalar::Text("FAULT".to_owned()));
            return table.process_fault_id.clone();
        }
        // First match on phase, frame and guard; guards see the state and
        // the event's derived observations.
        let observed = |k: &str| -> Option<&Scalar> {
            if table.observations.iter().any(|o| o == k)
                && let Some((_, v)) = event.observations.iter().find(|(name, _)| name == k)
            {
                return Some(v);
            }
            self.state.get(k)
        };
        let matched = table.rules.iter().find(|r| {
            let phase_ok = if r.phase == "*ANY" {
                false
            } else if r.phase == table.set_wildcard.0 {
                table.set_wildcard.1.contains(&phase)
            } else {
                r.phase == phase
            };
            phase_ok && r.frame == frame && r.guard.iter().all(|(k, v)| observed(k) == Some(v))
        });
        let Some(rule) = matched else {
            self.set("phase", Scalar::Text("FAULT".to_owned()));
            return table.fallback_id.clone();
        };
        for (frames, update) in table.updates.iter().chain(&table.additions) {
            if !frames.iter().any(|f| f == frame) {
                continue;
            }
            match update {
                Update::IdentityNegotiated => self.set(
                    "identityNegotiated",
                    Scalar::Bool(event.identity_negotiated),
                ),
                Update::UniverseModes => {
                    self.set("dependencyMode", Scalar::Bool(event.dependency_mode));
                    self.set("preparedMode", Scalar::Bool(event.prepared_mode));
                }
                Update::Analyze { resets_output } => {
                    self.set("stageCount", Scalar::Int(event.stage_count));
                    self.set("stageIndex", Scalar::Int(0));
                    if *resets_output {
                        self.set("outputSeen", Scalar::Bool(false));
                    }
                }
                Update::CancelPhase => self.set("cancelPhase", Scalar::Text(phase.clone())),
                Update::Set(sets) => {
                    for (k, v) in sets {
                        self.set(k, v.clone());
                    }
                }
            }
        }
        let mut next = rule.next.clone();
        if next == STAGE_DEPENDENT {
            let index = self.int("stageIndex") + 1;
            self.set("stageIndex", Scalar::Int(index));
            self.set(
                "stagesCompleted",
                Scalar::Int(self.int("stagesCompleted") + 1),
            );
            next = if index == self.int("stageCount") {
                "READY_COMPLETE"
            } else {
                "ANALYZING"
            }
            .to_owned();
        }
        if let Some(terminal) = &rule.terminal {
            self.set("terminalKind", Scalar::Text(terminal.clone()));
        }
        self.set("phase", Scalar::Text(next));
        rule.id.clone()
    }
}

#[cfg(test)]
#[path = "table_tests.rs"]
mod tests;

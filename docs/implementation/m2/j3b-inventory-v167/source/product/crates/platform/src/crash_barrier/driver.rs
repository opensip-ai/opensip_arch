//! The parent side of law X9 r1 item 3, and item 5's census.
//!
//! A matrix child is the same test binary, run as
//! `current_exe() --exact <entry> --nocapture --test-threads=1` with a
//! cleared environment holding only `OPENSIP_X9_CHILD`, `OPENSIP_X9_INPUT`,
//! `OPENSIP_X9_ARMS` and `TMPDIR`. The parent reads the child's tagged stderr
//! records, writes `resume <name>#<k>` on its stdin, and kills it with
//! `SIGKILL`. Every synchronization is a blocking read of a record the other
//! side wrote. The one timed wait is the per-run watchdog: when it expires it
//! kills the child, and the run can only be a `HARNESS-ERROR`.
use super::{Arm, CHILD_VAR, CLOCK_VAR, INPUT_VAR, Occurrence, is_durability_point, parse_arms};
use std::io::{self, BufRead, BufReader, Read, Write};
use std::os::unix::process::ExitStatusExt;
use std::path::Path;
use std::process::{Child, ChildStdin, Command, ExitStatus, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::{self, Receiver, RecvTimeoutError, Sender};
use std::sync::{Arc, Mutex, PoisonError};
use std::thread::JoinHandle;
use std::time::Duration;

/// The per-run watchdog (item 3). Its only effect is a `HARNESS-ERROR`.
pub const WATCHDOG: Duration = Duration::from_secs(300);
const SIGKILL: i32 = 9;

/// One tagged stderr record. `point` is `<full name>#<k>`, or `-` for an
/// `outcome` or `harness-error` record that names no point.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Record {
    pub pid: u32,
    pub thread: u64,
    pub sequence: u64,
    pub point: String,
    pub event: String,
    pub payload: String,
}
impl Record {
    /// The point's full name without its occurrence.
    pub fn name(&self) -> &str {
        self.point.rsplit_once('#').map_or("-", |(name, _)| name)
    }
    pub fn occurrence(&self) -> Option<u32> {
        self.point.rsplit_once('#')?.1.parse().ok()
    }
}

const EVENTS: &[&str] = &[
    "pass",
    "held",
    "resumed",
    "fail-before",
    "fail-after",
    "inject-id",
    "outcome",
    "harness-error",
    "signalled",
];

fn parse_record(line: &str) -> Option<Record> {
    let mut fields = line.splitn(7, '|');
    if fields.next()? != "X9" {
        return None;
    }
    let pid = fields.next()?.parse().ok()?;
    let thread = fields.next()?.parse().ok()?;
    let sequence = fields.next()?.parse().ok()?;
    let point = fields.next()?.to_owned();
    let event = fields.next()?.to_owned();
    let payload = fields.next()?.to_owned();
    let named = point
        .rsplit_once('#')
        .is_some_and(|(name, k)| !name.is_empty() && k.parse::<u32>().is_ok_and(|k| k > 0));
    let valid = if event == "signalled" {
        point == "-" && matches!(payload.as_str(), "SIGINT" | "SIGTERM" | "SIGHUP")
    } else {
        EVENTS.contains(&event.as_str())
            && (named || point == "-" && matches!(event.as_str(), "outcome" | "harness-error"))
    };
    valid.then_some(Record {
        pid,
        thread,
        sequence,
        point,
        event,
        payload,
    })
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum HarnessError {
    /// The arming list does not parse (checked before spawning).
    Arms(String),
    Spawn(String),
    /// The child wrote a `harness-error` record.
    Child(String),
    /// End of file without the armed point: "armed point not reached".
    NotReached(String),
    Watchdog,
    /// The child entry did not run (`--exact` matched no test).
    EntryMissing,
    /// A tagged line that is not a record, or records out of order.
    Malformed(String),
    Control(String),
    /// The child did not end by `SIGKILL`.
    NotKilled(String),
    /// A record after the held point names another point of the holding
    /// thread, or a durability point of any thread.
    AfterKillPoint(String),
    /// A finished child did not exit 0.
    Exit(String),
}

/// Law X9 r2 item 3: a child's clock script, the run set's epoch E and the
/// child's ordinal k in its run (spawn order, the fixture child 0).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ScriptedClock {
    pub epoch: i64,
    pub ordinal: u32,
}

/// What to run: the child entry (a `#[test]` path for `--exact`), the driver
/// name, its input file, the arming (`None` leaves `OPENSIP_X9_ARMS` unset,
/// so no point records anything), the clock script (`None` leaves
/// `OPENSIP_X9_CLOCK` unset: the OS's wall clock) and the run's scratch
/// parent (`TMPDIR`).
pub struct ChildSpec<'a> {
    pub entry: &'a str,
    pub role: &'a str,
    pub input: &'a Path,
    pub arms: Option<&'a str>,
    pub clock: Option<ScriptedClock>,
    pub scratch_parent: &'a Path,
}

enum Line {
    Record(Record),
    Diagnostic(String),
    Malformed(String),
}

/// A running matrix child.
pub struct MatrixChild {
    child: Arc<Mutex<Child>>,
    stdin: Option<ChildStdin>,
    lines: Receiver<Line>,
    stderr_reader: Option<JoinHandle<()>>,
    stdout_reader: Option<JoinHandle<Vec<u8>>>,
    watchdog: Option<(Sender<()>, JoinHandle<()>)>,
    fired: Arc<AtomicBool>,
    traced: bool,
    arms: Vec<Arm>,
    records: Vec<Record>,
    diagnostics: Vec<String>,
    malformed: Vec<String>,
    resumed: Vec<String>,
    eof: bool,
    exited: bool,
}

/// A child after it exited, with everything it reported.
#[derive(Debug)]
pub struct Exit {
    pub status: ExitStatus,
    pub records: Vec<Record>,
    pub diagnostics: Vec<String>,
    pub stdout: String,
    pub watchdog_fired: bool,
    traced: bool,
    arms: Vec<Arm>,
    malformed: Vec<String>,
}

fn lock(child: &Mutex<Child>) -> std::sync::MutexGuard<'_, Child> {
    child.lock().unwrap_or_else(PoisonError::into_inner)
}

impl MatrixChild {
    pub fn spawn(spec: &ChildSpec<'_>) -> Result<Self, HarnessError> {
        Self::spawn_watched(spec, WATCHDOG)
    }

    #[cfg(test)]
    pub(crate) fn spawn_with_watchdog(
        spec: &ChildSpec<'_>,
        watchdog: Duration,
    ) -> Result<Self, HarnessError> {
        Self::spawn_watched(spec, watchdog)
    }

    fn spawn_watched(spec: &ChildSpec<'_>, watchdog: Duration) -> Result<Self, HarnessError> {
        let arms = match spec.arms {
            Some(text) => parse_arms(text).map_err(HarnessError::Arms)?,
            None => Vec::new(),
        };
        let executable = std::env::current_exe().map_err(|e| HarnessError::Spawn(e.to_string()))?;
        let mut command = Command::new(executable);
        command
            .args(["--exact", spec.entry, "--nocapture", "--test-threads=1"])
            .env_clear()
            .env(CHILD_VAR, spec.role)
            .env(INPUT_VAR, spec.input)
            .env("TMPDIR", spec.scratch_parent)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped());
        if let Some(text) = spec.arms {
            command.env(super::ARMS_VAR, text);
        }
        if let Some(clock) = spec.clock {
            let text = format!("{}:{}", clock.epoch, clock.ordinal);
            super::parse_clock(&text).map_err(HarnessError::Arms)?;
            command.env(CLOCK_VAR, text);
        }
        let mut child = command
            .spawn()
            .map_err(|e| HarnessError::Spawn(e.to_string()))?;
        let stdin = child.stdin.take();
        let (stdout, stderr) = match (child.stdout.take(), child.stderr.take()) {
            (Some(stdout), Some(stderr)) => (stdout, stderr),
            _ => {
                let _ = child.kill();
                let _ = child.wait();
                return Err(HarnessError::Spawn("child pipes unavailable".to_owned()));
            }
        };
        let (sender, lines) = mpsc::channel();
        let stderr_reader = std::thread::spawn(move || read_stderr(stderr, sender));
        let stdout_reader = std::thread::spawn(move || {
            let mut bytes = Vec::new();
            let _ = BufReader::new(stdout).read_to_end(&mut bytes);
            bytes
        });
        let child = Arc::new(Mutex::new(child));
        let fired = Arc::new(AtomicBool::new(false));
        let (done, expiry) = mpsc::channel::<()>();
        let watched = Arc::clone(&child);
        let flag = Arc::clone(&fired);
        let watchdog = std::thread::spawn(move || {
            if let Err(RecvTimeoutError::Timeout) = expiry.recv_timeout(watchdog) {
                flag.store(true, Ordering::SeqCst);
                let _ = lock(&watched).kill();
            }
        });
        Ok(Self {
            child,
            stdin,
            lines,
            stderr_reader: Some(stderr_reader),
            stdout_reader: Some(stdout_reader),
            watchdog: Some((done, watchdog)),
            fired,
            traced: spec.arms.is_some(),
            arms,
            records: Vec::new(),
            diagnostics: Vec::new(),
            malformed: Vec::new(),
            resumed: Vec::new(),
            eof: false,
            exited: false,
        })
    }

    // Block for the next stderr line; end of file once every writer closed.
    fn receive(&mut self) {
        match self.lines.recv() {
            Ok(Line::Record(record)) => {
                if self
                    .records
                    .last()
                    .is_some_and(|last| record.sequence <= last.sequence)
                {
                    self.malformed
                        .push(format!("record {} out of order", record.sequence));
                }
                self.records.push(record);
            }
            Ok(Line::Diagnostic(line)) => self.diagnostics.push(line),
            Ok(Line::Malformed(line)) => self.malformed.push(line),
            Err(_) => self.eof = true,
        }
    }

    /// Block until the child reports `event` at `point` (`<name>#<k>`).
    pub fn await_event(&mut self, point: &str, event: &str) -> Result<Record, HarnessError> {
        self.await_event_from(0, point, event)
    }
    fn await_event_from(
        &mut self,
        start: usize,
        point: &str,
        event: &str,
    ) -> Result<Record, HarnessError> {
        loop {
            if let Some(record) = self
                .records
                .iter()
                .skip(start)
                .find(|r| r.point == point && r.event == event)
            {
                return Ok(record.clone());
            }
            if let Some(record) = self.records.iter().find(|r| r.event == "harness-error") {
                return Err(HarnessError::Child(record.payload.clone()));
            }
            if let Some(line) = self.malformed.first() {
                return Err(HarnessError::Malformed(line.clone()));
            }
            if self.eof {
                return Err(if self.fired.load(Ordering::SeqCst) {
                    HarnessError::Watchdog
                } else {
                    HarnessError::NotReached(point.to_owned())
                });
            }
            self.receive();
        }
    }

    /// Block until the child holds at `point` (`<name>#<k>`).
    pub fn await_held(&mut self, point: &str) -> Result<Record, HarnessError> {
        self.await_event(point, "held")
    }

    /// Resume the thread held at `point`.
    pub fn resume(&mut self, point: &str) -> Result<(), HarnessError> {
        let held = self
            .records
            .iter()
            .any(|r| r.point == point && r.event == "held");
        if !held || self.resumed.iter().any(|p| p == point) {
            return Err(HarnessError::Control(format!("{point} is not held")));
        }
        self.control_line(&format!("resume {point}"))?;
        self.resumed.push(point.to_owned());
        Ok(())
    }

    /// S12's acknowledgement precedes resuming the held product thread.
    pub fn signal(&mut self, signal: super::SignalInput) -> Result<(), HarnessError> {
        let start = self.records.len();
        self.control_line(&format!("signal {}", signal.as_str()))?;
        let record = self.await_event_from(start, "-", "signalled")?;
        if record.payload != signal.as_str() {
            return Err(HarnessError::Control(
                "signal acknowledgement differs".into(),
            ));
        }
        Ok(())
    }

    // The control channel: one line on the child's stdin.
    pub(crate) fn control_line(&mut self, line: &str) -> Result<(), HarnessError> {
        let stdin = self
            .stdin
            .as_mut()
            .ok_or_else(|| HarnessError::Control("stdin closed".to_owned()))?;
        stdin
            .write_all(format!("{line}\n").as_bytes())
            .and_then(|()| stdin.flush())
            .map_err(|e| HarnessError::Control(e.to_string()))
    }

    /// Send `SIGKILL`, then wait and read stderr to end of file.
    pub fn kill(mut self) -> io::Result<Exit> {
        lock(&self.child).kill()?;
        self.drain()
    }

    /// Wait for the child to exit by itself, reading stderr to end of file.
    /// A child that never exits is killed by the watchdog.
    pub fn finish(mut self) -> io::Result<Exit> {
        self.drain()
    }

    fn drain(&mut self) -> io::Result<Exit> {
        while !self.eof {
            self.receive();
        }
        if let Some(reader) = self.stderr_reader.take() {
            let _ = reader.join();
        }
        let stdout = self
            .stdout_reader
            .take()
            .and_then(|reader| reader.join().ok())
            .unwrap_or_default();
        let status = lock(&self.child).wait()?;
        self.exited = true;
        self.stdin = None;
        if let Some((done, watchdog)) = self.watchdog.take() {
            drop(done);
            let _ = watchdog.join();
        }
        Ok(Exit {
            status,
            records: std::mem::take(&mut self.records),
            diagnostics: std::mem::take(&mut self.diagnostics),
            stdout: String::from_utf8_lossy(&stdout).into_owned(),
            watchdog_fired: self.fired.load(Ordering::SeqCst),
            traced: self.traced,
            arms: std::mem::take(&mut self.arms),
            malformed: std::mem::take(&mut self.malformed),
        })
    }
}

impl Drop for MatrixChild {
    // A driver that unwinds never leaves a held child behind.
    fn drop(&mut self) {
        if !self.exited {
            let mut child = lock(&self.child);
            let _ = child.kill();
            let _ = child.wait();
        }
        if let Some((done, watchdog)) = self.watchdog.take() {
            drop(done);
            let _ = watchdog.join();
        }
    }
}

fn read_stderr(stderr: impl Read, sender: Sender<Line>) {
    let mut reader = BufReader::new(stderr);
    let mut raw = Vec::new();
    loop {
        raw.clear();
        match reader.read_until(b'\n', &mut raw) {
            Ok(0) | Err(_) => return,
            Ok(_) => {}
        }
        let line = String::from_utf8_lossy(&raw);
        let line = line.strip_suffix('\n').unwrap_or(&line);
        let message = if line.starts_with("X9|") {
            parse_record(line).map_or_else(|| Line::Malformed(line.to_owned()), Line::Record)
        } else {
            Line::Diagnostic(line.to_owned())
        };
        if sender.send(message).is_err() {
            return;
        }
    }
}

impl Exit {
    fn harness(&self) -> Result<(), HarnessError> {
        if self.watchdog_fired {
            return Err(HarnessError::Watchdog);
        }
        if let Some(record) = self.records.iter().find(|r| r.event == "harness-error") {
            return Err(HarnessError::Child(record.payload.clone()));
        }
        if let Some(line) = self.malformed.first() {
            return Err(HarnessError::Malformed(line.clone()));
        }
        if !self.stdout.contains("running 1 test") {
            return Err(HarnessError::EntryMissing);
        }
        Ok(())
    }

    fn acted(&self, point: &str) -> bool {
        self.records.iter().any(|r| {
            r.point == point
                && matches!(
                    r.event.as_str(),
                    "held" | "fail-before" | "fail-after" | "inject-id"
                )
        })
    }

    fn arm_reached(&self, arm: &Arm) -> bool {
        match arm.occurrence {
            Occurrence::Nth(k) => self.acted(&format!("{}#{k}", arm.point)),
            Occurrence::Every => self
                .records
                .iter()
                .any(|r| r.name() == arm.point && self.acted(&r.point)),
        }
    }

    /// A child that ran to completion: exit 0, no harness error, and every
    /// armed point reached.
    pub fn verify_finished(&self) -> Result<(), HarnessError> {
        self.harness()?;
        if !self.status.success() {
            return Err(HarnessError::Exit(format!("{:?}", self.status)));
        }
        match self.arms.iter().find(|arm| !self.arm_reached(arm)) {
            Some(arm) => Err(HarnessError::NotReached(arm.point.clone())),
            None => Ok(()),
        }
    }

    /// Item 3's death at `point` (`<name>#<k>`): the child ended by
    /// `SIGKILL`; the holding thread's last record is that `held`; and no
    /// later record names a durability point.
    pub fn verify_death_at(&self, point: &str) -> Result<(), HarnessError> {
        self.harness()?;
        if self.status.signal() != Some(SIGKILL) {
            return Err(HarnessError::NotKilled(format!("{:?}", self.status)));
        }
        let Some(held) = self
            .records
            .iter()
            .find(|r| r.point == point && r.event == "held")
        else {
            return Err(HarnessError::NotReached(point.to_owned()));
        };
        let later = self.records.iter().filter(|r| r.sequence > held.sequence);
        for record in later {
            if record.thread == held.thread || is_durability_point(record.name()) {
                return Err(HarnessError::AfterKillPoint(format!(
                    "{} {}",
                    record.point, record.event
                )));
            }
        }
        Ok(())
    }

    /// The child's last `outcome` record.
    pub fn outcome(&self) -> Option<&str> {
        self.records
            .iter()
            .rev()
            .find(|r| r.event == "outcome")
            .map(|r| r.payload.as_str())
    }

    /// The ordered trace without the process id:
    /// `<thread>|<n>|<point>|<event>|<payload>`.
    pub fn trace(&self) -> Vec<String> {
        self.records
            .iter()
            .map(|r| {
                format!(
                    "{}|{}|{}|{}|{}",
                    r.thread, r.sequence, r.point, r.event, r.payload
                )
            })
            .collect()
    }
}

/// One point of the unarmed census: its full name, how often one run
/// reached it, and whether it is a durability point.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CensusPoint {
    pub name: String,
    pub occurrences: u32,
    pub durability: bool,
}

/// Item 5's census: every point a lawful unarmed run reached.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Census {
    pub points: Vec<CensusPoint>,
}

impl Census {
    /// From a finished child that ran traced with nothing armed. Each
    /// name's occurrences are exactly `#1..#n`.
    pub fn from_exit(exit: &Exit) -> Result<Self, HarnessError> {
        exit.verify_finished()?;
        if !exit.traced || !exit.arms.is_empty() {
            return Err(HarnessError::Arms(
                "a census runs traced with nothing armed".to_owned(),
            ));
        }
        let mut points: Vec<CensusPoint> = Vec::new();
        for record in exit.records.iter().filter(|r| r.point != "-") {
            let (name, occurrence) = (record.name(), record.occurrence().unwrap_or(0));
            if record.event != "pass" {
                return Err(HarnessError::Malformed(format!(
                    "census record {} {}",
                    record.point, record.event
                )));
            }
            match points.iter_mut().find(|p| p.name == name) {
                Some(point) if point.occurrences + 1 == occurrence => point.occurrences += 1,
                None if occurrence == 1 => points.push(CensusPoint {
                    name: name.to_owned(),
                    occurrences: 1,
                    durability: is_durability_point(name),
                }),
                _ => {
                    return Err(HarnessError::Malformed(format!(
                        "census occurrence {}",
                        record.point
                    )));
                }
            }
        }
        points.sort_by(|a, b| a.name.cmp(&b.name));
        Ok(Self { points })
    }

    /// The kill set: every durability point at `#1`, and for a repeated
    /// point also its middle (`(n + 1) / 2`) and last (`n`) occurrence.
    pub fn kill_set(&self) -> Vec<String> {
        let mut set = Vec::new();
        for point in self.points.iter().filter(|p| p.durability) {
            let n = point.occurrences;
            let mut occurrences = vec![1, n.div_ceil(2), n];
            occurrences.dedup();
            set.extend(occurrences.iter().map(|k| format!("{}#{k}", point.name)));
        }
        set
    }
}

#[cfg(test)]
mod signal_record_tests {
    use super::parse_record;
    #[test]
    fn acknowledgement_is_a_known_signal_without_a_point() {
        for signal in ["SIGINT", "SIGTERM", "SIGHUP"] {
            let record = parse_record(&format!("X9|1|2|3|-|signalled|{signal}")).unwrap();
            assert_eq!(record.payload, signal);
            assert_eq!(record.occurrence(), None);
            assert!(
                parse_record(&format!(
                    "X9|1|2|3|x3d.publish.after-staging#1|signalled|{signal}"
                ))
                .is_none()
            );
        }
        for signal in ["", "SIGKILL", "SIGINT extra", "sigint"] {
            assert!(parse_record(&format!("X9|1|2|3|-|signalled|{signal}")).is_none());
        }
        assert!(parse_record("X9|1|2|3|x3d.publish.after-staging#1|held|-").is_some());
    }
}

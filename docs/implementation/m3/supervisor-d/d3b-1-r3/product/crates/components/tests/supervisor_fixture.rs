//! The supervisor's first-party fixture child (M3-D r5 item 1, :189; D3a plan
//! r4, LD-D3A-9). A harness-free test target: fd1 carries only the bytes this
//! program writes, from process start.
//!
//! Spawned by the supervisor's tests with argv `[exe, SENTINEL, script]`, it
//! answers the host's control frames on fd3/fd4 from one thread and the
//! provider frames on fd0/fd1 from another, as `script` says. A frame's
//! payload is the canonical CBOR map `{"type": <frame>}` (the fixture
//! participant runs P3T's rows on frame types alone). Run by Cargo without
//! the sentinel, it exits at once, writing nothing.
//!
//! A `tool-` script runs as item 12's tool class (D3a-2): it has fds 0 to 2
//! only, fd0 at EOF, and no control plane (item 5, :274).
use opensip_components::provider_protocol::cbor::{Profile, Value};
use opensip_components::provider_protocol::{read_frame, write_frame};
use opensip_identity::{JsonValue, parse_json};
use std::fs::File;
use std::io::{Read, Write};
use std::os::fd::FromRawFd;
use std::os::unix::process::CommandExt;
use std::sync::mpsc;
use std::time::Duration;

const SENTINEL: &str = "opensip-d3a-fixture";
/// D3a-3's canary (S-OP-2 C-4): written to stderr and as a control `fault`
/// detail; no record may carry it or its digest.
const CANARY: &str = "OPENSIP-CANARY-q7Zx3mK9vB2nW5";

fn take(fd: i32) -> File {
    // SAFETY: the spawner dup2'ed this descriptor into the child (item 5);
    // nothing else in this process owns it.
    unsafe { File::from_raw_fd(fd) }
}

fn frame_of(frame: &str) -> Vec<u8> {
    let value = Value::Map(vec![("type".to_owned(), Value::Text(frame.to_owned()))]);
    write_frame(&value).expect("a small frame")
}

fn text<'a>(value: &'a JsonValue, key: &str) -> Option<&'a str> {
    match value {
        JsonValue::Object(map) => match map.get(key) {
            Some(JsonValue::String(s)) => Some(s),
            _ => None,
        },
        _ => None,
    }
}
fn member<'a>(value: &'a JsonValue, key: &str) -> Option<&'a JsonValue> {
    match value {
        JsonValue::Object(map) => map.get(key),
        _ => None,
    }
}

/// The control side: one thread reading the host's frames on fd3 and
/// answering on fd4.
struct Control {
    out: File,
    seq: u64,
    script: String,
    acked: mpsc::Sender<()>,
}
impl Control {
    fn send(&mut self, ty: &str, body: &str) {
        let json = format!(
            r#"{{"type":"{ty}","seq":{},"controlMajor":1,"body":{body}}}"#,
            self.seq
        );
        self.seq += 1;
        let mut frame = (json.len() as u32).to_be_bytes().to_vec();
        frame.extend_from_slice(json.as_bytes());
        self.write(&frame);
    }
    fn write(&mut self, bytes: &[u8]) {
        if self.script == "split" {
            // Every byte offset of the frame, one byte per write.
            for byte in bytes {
                if self.out.write_all(std::slice::from_ref(byte)).is_err() {
                    return;
                }
                std::thread::sleep(Duration::from_millis(1));
            }
        } else if self.out.write_all(bytes).is_err() {
            std::process::exit(20);
        }
    }
    fn run(mut self, mut input: File) {
        loop {
            let mut prefix = [0u8; 4];
            if input.read_exact(&mut prefix).is_err() {
                return;
            }
            let mut body = vec![0u8; u32::from_be_bytes(prefix) as usize];
            if input.read_exact(&mut body).is_err() {
                return;
            }
            let Ok(frame) = parse_json(&body) else {
                std::process::exit(21);
            };
            let ty = text(&frame, "type").unwrap_or("").to_owned();
            let body = member(&frame, "body");
            match ty.as_str() {
                "hello" => self.hello(body),
                "select" => {
                    let b = body.expect("a select body");
                    let reply = format!(
                        r#"{{"role":"{}","roleSubprotocol":"{}","subprotocolVersion":{}}}"#,
                        text(b, "role").unwrap_or(""),
                        text(b, "roleSubprotocol").unwrap_or(""),
                        version(b)
                    );
                    self.send("selectAck", &reply);
                    if self.script == "close-control" {
                        // D3a-3 r2: the control reader goes, so a later host
                        // frame's write fails.
                        return;
                    }
                    // D3a-2: the asserted resident size (item 16, :530),
                    // above the ceiling, or below it while the observed size
                    // passes it.
                    match self.script.as_str() {
                        "assert-large" => self.send(
                            "resourceReport",
                            r#"{"residentBytes":9663676416,"cpuNanoseconds":0,"openHandles":0}"#,
                        ),
                        "assert-small" => self.send(
                            "resourceReport",
                            r#"{"residentBytes":1,"cpuNanoseconds":0,"openHandles":0}"#,
                        ),
                        _ => {}
                    }
                    if self.script == "control-storm" {
                        // Sustained control traffic that is not liveness:
                        // resource reports, back to back, health unanswered.
                        for _ in 0..1_000_000 {
                            self.send(
                                "resourceReport",
                                r#"{"residentBytes":1,"cpuNanoseconds":0,"openHandles":0}"#,
                            );
                        }
                        return;
                    }
                }
                "health" if self.script == "canary" => {
                    self.send("fault", &format!(r#"{{"detail":"{CANARY}"}}"#));
                }
                "health" if self.script == "control-fault" => {
                    // The component reports its own failure (CPC's `fault`).
                    self.send("fault", r#"{"detail":"internal failure"}"#);
                }
                "health" if self.script != "blocked" => {
                    let nonce = body.and_then(|b| text(b, "nonce")).unwrap_or("");
                    let nonce = if self.script == "bad-nonce" {
                        "wrong"
                    } else {
                        nonce
                    };
                    if self.script == "bad-seq" {
                        // An unrelated RF7: a sequence gap.
                        self.seq += 10;
                    }
                    self.send(
                        "healthReport",
                        &format!(r#"{{"nonce":"{nonce}","status":"busy"}}"#),
                    );
                }
                "shutdown" if self.script != "no-ack" => {
                    self.send("shutdownAck", "{}");
                    if self.acked.send(()).is_err() {
                        return;
                    }
                }
                _ => {}
            }
        }
    }
    fn hello(&mut self, body: Option<&JsonValue>) {
        let b = body.expect("a hello body");
        match self.script.as_str() {
            "silent-handshake" => {}
            "refuse" => self.send("refusal", r#"{"family":"RF-2"}"#),
            "bad-control" => {
                let mut frame = 1u32.to_be_bytes().to_vec();
                frame.push(b'{');
                self.write(&frame);
            }
            "over-bound" => self.write(&65_537u32.to_be_bytes()),
            _ => {
                let offer = match member(b, "subprotocolOffers") {
                    Some(JsonValue::Array(items)) => items.first(),
                    _ => None,
                }
                .expect("one offer");
                let reply = format!(
                    r#"{{"controlMajor":1,"stableId":"{}","admittedManifestDigest":"{}","maxControlFrameBytes":65536,"subprotocolConfirms":[{{"role":"{}","roleSubprotocol":"{}","subprotocolVersion":{}}}]}}"#,
                    text(b, "expectedStableId").unwrap_or(""),
                    text(b, "admittedManifestDigest").unwrap_or(""),
                    text(offer, "role").unwrap_or(""),
                    text(offer, "roleSubprotocol").unwrap_or(""),
                    version(offer)
                );
                self.send("helloAck", &reply);
            }
        }
    }
}
fn version(value: &JsonValue) -> i128 {
    match member(value, "subprotocolVersion") {
        Some(JsonValue::Integer(i)) => i.get(),
        _ => 0,
    }
}

/// The data side: the host's provider frames on fd0, answered on fd1.
struct Data {
    out: Option<File>,
    script: String,
}
impl Data {
    fn send(&mut self, frames: &[&str]) {
        let Some(out) = &mut self.out else {
            return;
        };
        let bytes: Vec<u8> = frames.iter().flat_map(|f| frame_of(f)).collect();
        if self.script == "split" {
            for byte in &bytes {
                if out.write_all(std::slice::from_ref(byte)).is_err() {
                    std::process::exit(22);
                }
                std::thread::sleep(Duration::from_millis(1));
            }
        } else if out.write_all(&bytes).is_err() {
            std::process::exit(22);
        }
    }
    fn close(&mut self) {
        drop(self.out.take());
    }
}

/// This fixture again, as a group member running `script`.
fn spawn_self(script: &str) {
    let exe = std::env::current_exe().expect("the fixture's path");
    if std::process::Command::new(exe)
        .args([SENTINEL, script])
        .stdin(std::process::Stdio::null())
        .spawn()
        .is_err()
    {
        std::process::exit(28);
    }
}

/// Wait to be killed, but never past a minute: a failed test leaves no
/// orphan.
fn hang() -> ! {
    std::thread::sleep(Duration::from_secs(60));
    std::process::exit(31);
}

/// A `tool-` script (D3a-2): item 12's tool class, on fds 0 to 2.
fn tool(script: &str) -> ! {
    let mut input = take(0);
    let mut out = take(1);
    let mut stderr = take(2);
    let mut write = |bytes: &[u8]| {
        if out.write_all(bytes).is_err() {
            std::process::exit(40);
        }
    };
    if let Some(n) = script.strip_prefix("tool-bytes-") {
        // Exactly `n` bytes on fd1.
        let n: usize = n.parse().expect("a byte count");
        write(&vec![b'o'; n]);
        std::process::exit(0);
    }
    if let Some(n) = script.strip_prefix("tool-fork-") {
        // `n` group members beside the root, held while the host samples.
        let n: usize = n.parse().expect("a member count");
        let exe = std::env::current_exe().expect("the fixture's path");
        let mut members = Vec::with_capacity(n);
        for _ in 0..n {
            match std::process::Command::new(&exe)
                .args([SENTINEL, "hold"])
                .stdin(std::process::Stdio::null())
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null())
                .spawn()
            {
                Ok(member) => members.push(member),
                Err(_) => std::process::exit(41),
            }
        }
        for mut member in members {
            if member.wait().is_err() {
                std::process::exit(42);
            }
        }
        write(b"members done\n");
        std::process::exit(0);
    }
    if let Some(rest) = script.strip_prefix("tool-tree-") {
        match rest.strip_prefix("ignoring-") {
            Some(rest) => tree(rest),
            None => {
                // The root first ignores SIGTERM, so that it is still alive,
                // unreaped, at the snapshot after the escalation (item 18,
                // :590-597; D5-T5's root). An ignored disposition survives
                // exec, so the shell re-runs this script in the same process,
                // with its descriptors and its group.
                let exe = std::env::current_exe().expect("the fixture's path");
                let again = format!("tool-tree-ignoring-{rest}");
                let error = std::process::Command::new("/bin/sh")
                    .args(["-c", "trap '' TERM; exec \"$0\" \"$@\""])
                    .arg(exe)
                    .args([SENTINEL, again.as_str()])
                    .exec();
                drop(error);
                std::process::exit(50);
            }
        }
    }
    if let Some(file) = script.strip_prefix("tool-daemonize:") {
        // D3b-1 (D5-T3): the intermediate of a double fork. It starts the
        // daemon outside the group, writes the daemon's pid, and exits, so
        // the daemon is orphaned to launchd before any teardown.
        let daemon = spawn_tree_member(None, true);
        write_pids(file, &[daemon]);
        std::process::exit(0);
    }
    match script {
        "tool-ok" => {
            for _ in 0..1_000 {
                write(b"tool output\n");
            }
            if stderr.write_all(b"a tool's stderr\n").is_err() {
                std::process::exit(43);
            }
            std::process::exit(0);
        }
        "tool-fail" => {
            write(b"partial\n");
            std::process::exit(101);
        }
        "tool-stdin" => {
            // fd0 is at EOF at once (item 5, :274).
            let mut seen = Vec::new();
            if input.read_to_end(&mut seen).is_err() || !seen.is_empty() {
                std::process::exit(44);
            }
            write(b"stdin at eof\n");
            std::process::exit(0);
        }
        "tool-held" => {
            // The root exits while a group member still holds fd1 past the
            // drain.
            spawn_self("hold-long");
            std::process::exit(0);
        }
        _ => hang(),
    }
}

/// D3b-1: a held process for the descendant-step controls, with null
/// descriptors, in the caller's group or (`escape`) in a group of its own:
/// item 18's `setsid` or `setpgid` (:602). It runs `script`, or holds.
fn spawn_tree_member(script: Option<&str>, escape: bool) -> u32 {
    let exe = std::env::current_exe().expect("the fixture's path");
    let mut command = std::process::Command::new(exe);
    command
        .args([SENTINEL, script.unwrap_or("hold-tree")])
        .stdin(std::process::Stdio::null())
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::null());
    if escape {
        command.process_group(0);
    }
    match command.spawn() {
        Ok(child) => child.id(),
        Err(_) => std::process::exit(45),
    }
}

/// Write `pids` to `file`, whole, for a test's out-of-band check.
fn write_pids(file: &str, pids: &[u32]) {
    if file.is_empty() {
        return;
    }
    let text: Vec<String> = pids.iter().map(u32::to_string).collect();
    let tmp = format!("{file}.tmp");
    if std::fs::write(&tmp, text.join(" ")).is_err() || std::fs::rename(&tmp, file).is_err() {
        std::process::exit(46);
    }
}

/// A `tool-tree-<kind>:<file>` script (D3b-1, item 18's controls as unit
/// controls): the root, ignoring SIGTERM, makes its descendants (which
/// inherit that), writes their pids to `<file>`, and hangs until the
/// deadline's teardown kills it with the group's SIGKILL.
fn tree(rest: &str) -> ! {
    let (kind, file) = rest.split_once(':').unwrap_or((rest, ""));
    let mut pids = Vec::new();
    match kind {
        // D5-T1: a descendant in the group.
        "ingroup" => pids.push(spawn_tree_member(None, false)),
        "root-only" => {}
        // D5-T2: a descendant that left the group before the snapshot.
        "escape" => pids.push(spawn_tree_member(None, true)),
        "change-group" | "fork-after-snapshot" => {
            let script = format!("tree-gated-{kind}:{file}");
            pids.push(spawn_tree_member(Some(&script), false));
        }
        // D5-T3: a double-forked daemon, orphaned before teardown.
        "daemon" => {
            let intermediate = format!("tool-daemonize:{file}");
            let exe = std::env::current_exe().expect("the fixture's path");
            let status = std::process::Command::new(exe)
                .args([SENTINEL, intermediate.as_str()])
                .stdin(std::process::Stdio::null())
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null())
                .process_group(0)
                .status();
            if !status.is_ok_and(|s| s.success()) {
                std::process::exit(47);
            }
            hang();
        }
        // D5-T4: more descendants in the group than the tool's walk bound.
        "loop" | "walk-exact" | "walk-over" | "provider-exact" | "provider-over" => {
            // The sourced tool walk bound is 64 total pids, root included.
            let children = match kind {
                "provider-exact" => 3,
                "provider-over" => 4,
                "walk-exact" => 63,
                "walk-over" => 64,
                _ => 70,
            };
            for _ in 0..children {
                pids.push(spawn_tree_member(None, false));
            }
        }
        // D5-T5: a descendant in the group that survives SIGTERM.
        "term-survivor" => {
            match std::process::Command::new("/bin/sh")
                .args(["-c", "trap '' TERM; sleep 30"])
                .stdin(std::process::Stdio::null())
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null())
                .spawn()
            {
                Ok(child) => pids.push(child.id()),
                Err(_) => std::process::exit(48),
            }
        }
        _ => std::process::exit(49),
    }
    write_pids(file, &pids);
    hang();
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.get(1).map(String::as_str) != Some(SENTINEL) {
        return;
    }
    let script = args.get(2).cloned().unwrap_or_default();
    if let Some(rest) = script.strip_prefix("tree-gated-") {
        let (kind, file) = rest.split_once(':').expect("a gated script");
        let gate = format!("{file}.go");
        let began = std::time::Instant::now();
        while !std::path::Path::new(&gate).exists() {
            if began.elapsed() >= Duration::from_secs(60) {
                std::process::exit(52);
            }
            std::thread::sleep(Duration::from_millis(2));
        }
        if kind == "change-group" {
            // exec retains the pid, while CommandExt sets its new group.
            let error = std::process::Command::new(std::env::current_exe().expect("fixture"))
                .args([SENTINEL, "hold-tree"])
                .process_group(0)
                .exec();
            drop(error);
            std::process::exit(51);
        }
        let late = spawn_tree_member(None, true);
        write_pids(&format!("{file}.late"), &[late]);
        hang();
    }
    if script == "hold-tree" {
        // D3b-1: a descendant held until it is killed, at most a minute.
        hang();
    }
    if script.starts_with("tool-") {
        tool(&script);
    }
    if script == "hold" || script == "hold-long" || script == "hold-brief" {
        // A group member holding the inherited fd1, fd2 and fd4 a while.
        let ms = match script.as_str() {
            "hold" => 300,
            "hold-brief" => 100,
            _ => 1_500,
        };
        std::thread::sleep(Duration::from_millis(ms));
        return;
    }
    let mut input = take(0);
    let mut data = Data {
        out: Some(take(1)),
        script: script.clone(),
    };
    let mut stderr = take(2);
    let control_in = take(3);
    let (acked, ack) = mpsc::channel();
    let control = Control {
        out: take(4),
        seq: 1,
        script: script.clone(),
        acked,
    };
    std::thread::spawn(move || control.run(control_in));
    // D3a-2 (D3-T15): stderr exactly at its truncation threshold, and one
    // byte past it; never a fault.
    let stderr_bytes = match script.as_str() {
        "stderr-at" => 262_144,
        "stderr-over" => 262_145,
        _ => 0,
    };
    if stderr_bytes > 0 && stderr.write_all(&vec![b'e'; stderr_bytes]).is_err() {
        std::process::exit(23);
    }
    if script == "canary" && stderr.write_all(CANARY.as_bytes()).is_err() {
        std::process::exit(23);
    }
    if script == "flood-stderr" {
        let chunk = vec![b'e'; 262_144];
        for _ in 0..10 {
            if stderr.write_all(&chunk).is_err() {
                std::process::exit(23);
            }
        }
    }
    if script == "scratch-files" {
        for i in 0..100 {
            if std::fs::write(format!("f{i:03}"), b"x").is_err() {
                std::process::exit(24);
            }
        }
    }
    if script == "blocked" || script == "slow" {
        // Traffic that is not progress: stderr bytes, every few ms.
        let mut noisy = stderr.try_clone().expect("stderr");
        let spin = if script == "blocked" { 10_000 } else { 120 };
        std::thread::spawn(move || {
            for _ in 0..spin {
                if noisy.write_all(b"spin\n").is_err() {
                    return;
                }
                std::thread::sleep(Duration::from_millis(5));
            }
        });
    }
    loop {
        let frame = match read_frame(&mut input, Profile::Rust3, 16, None) {
            Ok(Some(frame)) => frame,
            Ok(None) => break,
            Err(_) => std::process::exit(25),
        };
        let ty = match frame.value() {
            Value::Map(members) => members
                .iter()
                .find(|(k, _)| k == "type")
                .and_then(|(_, v)| match v {
                    Value::Text(t) => Some(t.clone()),
                    _ => None,
                }),
            _ => None,
        }
        .unwrap_or_default();
        if script == "slow-reader" {
            std::thread::sleep(Duration::from_millis(50));
        }
        match (script.as_str(), ty.as_str()) {
            ("eof-early", "Hello") => {
                data.close();
                hang();
            }
            ("partial-frame", "Hello") => {
                let bytes = frame_of("HelloAck");
                if let Some(out) = &mut data.out
                    && out.write_all(&bytes[..20]).is_err()
                {
                    std::process::exit(26);
                }
                data.close();
                hang();
            }
            ("fault", "Hello") => {
                data.send(&["Complete"]);
                hang();
            }
            ("early-exit", "Hello") => std::process::exit(0),
            ("early-exit-brief-hold", "Hello") => {
                // The root dies before its terminal on its own; a member
                // holds fd1 briefly, inside the drain, then EOF follows.
                spawn_self("hold-brief");
                std::process::exit(0);
            }
            ("early-exit-held", "Hello") => {
                // The root dies before its terminal while a group member
                // still holds fd1 past the drain.
                spawn_self("hold-long");
                std::process::exit(0);
            }
            ("term-survivor", "Hello") => {
                // A group member that survives SIGTERM, so the escalation
                // runs to its SIGKILL.
                if std::process::Command::new("/bin/sh")
                    .args(["-c", "trap '' TERM; sleep 30"])
                    .stdin(std::process::Stdio::null())
                    .spawn()
                    .is_err()
                {
                    std::process::exit(29);
                }
                data.send(&["HelloAck"]);
                hang();
            }
            ("signal-death", "Hello") => std::process::abort(),
            // D3a-2 (D3-T13): 96 MiB, every page touched, then hold it.
            ("allocate" | "assert-small", "Hello") => {
                let held = vec![1u8; 96 << 20];
                data.send(&["HelloAck"]);
                std::hint::black_box(&held);
                hang();
            }
            // D3a-2 (D3-T14): a second process in a provider's tree.
            ("fork", "Hello") => {
                spawn_self("hold-long");
                data.send(&["HelloAck"]);
                hang();
            }
            (
                "hang" | "blocked" | "control-storm" | "control-fault" | "bad-nonce" | "bad-seq"
                | "assert-large" | "canary" | "close-control",
                "Hello",
            ) => {
                data.send(&["HelloAck"]);
                hang();
            }
            (_, "Hello") => data.send(&["HelloAck"]),
            (_, "OpenUniverse") => data.send(&["UniverseAccepted"]),
            // D3a-4 r2 (D3A4-R1-NBO-1): an admitted `Unavailable` before
            // Analyze, at `WAIT_NATIVE_CONTEXT_VERIFIED` (P3-21).
            ("unavailable-early", "SnapshotSeal") => {
                data.send(&["SnapshotAccepted", "Unavailable"])
            }
            (_, "SnapshotSeal") => data.send(&["SnapshotAccepted", "NativeContextVerified"]),
            // D3a-3 (D3-T22): candidates, then a fault before the terminal.
            ("facts-then-fault", "Analyze") => {
                data.send(&["FactBatch", "FactBatch", "Hello"]);
                hang();
            }
            ("facts-then-exit", "Analyze") => {
                data.send(&["FactBatch", "FactBatch"]);
                std::process::exit(0);
            }
            // D3a-4: an `Unavailable` terminal after Analyze.
            ("unavailable", "Analyze") => data.send(&["Unavailable"]),
            ("facts-then-hang", "Analyze") => {
                data.send(&["FactBatch", "FactBatch"]);
                hang();
            }
            (_, "Analyze") => {
                if script == "slow" {
                    std::thread::sleep(Duration::from_millis(600));
                }
                // D3a-4 r2 (D3A4-R1-RF-1): several progress-absent
                // intervals without a transition.
                if script == "slow-long" {
                    std::thread::sleep(Duration::from_millis(1_000));
                }
                // Coalesced: three frames in one write (split writes them
                // a byte at a time).
                data.send(&["FactBatch", "CoverageV3", "Complete"]);
            }
            _ => {}
        }
    }
    // fd0 is at EOF: the host closed the protocol (LD-D3A-15). The
    // shutdownAck goes first, unless the script withholds it.
    if script != "no-ack" && ack.recv_timeout(Duration::from_secs(10)).is_err() {
        std::process::exit(27);
    }
    match script.as_str() {
        "nonzero" => std::process::exit(3),
        "no-exit" => hang(),
        "held-eof-no-exit" => {
            data.close();
            hang();
        }
        "normal-eof-first" => {
            data.close();
            drop(stderr);
            std::thread::sleep(Duration::from_millis(200));
            std::process::exit(0);
        }
        "normal-exit-first" => {
            // A group member keeps fd1 open after the root exits.
            spawn_self("hold");
            std::process::exit(0);
        }
        _ => std::process::exit(0),
    }
}

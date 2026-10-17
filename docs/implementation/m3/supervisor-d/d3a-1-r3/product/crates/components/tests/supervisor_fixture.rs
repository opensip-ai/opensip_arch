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
use opensip_components::provider_protocol::cbor::{Profile, Value};
use opensip_components::provider_protocol::{read_frame, write_frame};
use opensip_identity::{JsonValue, parse_json};
use std::fs::File;
use std::io::{Read, Write};
use std::os::fd::FromRawFd;
use std::sync::mpsc;
use std::time::Duration;

const SENTINEL: &str = "opensip-d3a-fixture";

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

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.get(1).map(String::as_str) != Some(SENTINEL) {
        return;
    }
    let script = args.get(2).cloned().unwrap_or_default();
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
            (
                "hang" | "blocked" | "control-storm" | "control-fault" | "bad-nonce" | "bad-seq",
                "Hello",
            ) => {
                data.send(&["HelloAck"]);
                hang();
            }
            (_, "Hello") => data.send(&["HelloAck"]),
            (_, "OpenUniverse") => data.send(&["UniverseAccepted"]),
            (_, "SnapshotSeal") => data.send(&["SnapshotAccepted", "NativeContextVerified"]),
            (_, "Analyze") => {
                if script == "slow" {
                    std::thread::sleep(Duration::from_millis(600));
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

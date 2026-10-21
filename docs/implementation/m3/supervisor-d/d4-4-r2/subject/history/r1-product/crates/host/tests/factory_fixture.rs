//! D4-T3 first-party compiled peer, never a native provider implementation.
//! Accepts only the factory's closed Rust3 or TS2 launch argv. A private fixture
//! directory's name chooses the deliberate substitution; it is not a
//! production setting. The parent owns the installation and audit directory.
use opensip_components::provider_protocol::{
    cbor::{Profile, Value},
    read_frame, write_frame,
};
use serde_json::{Value as J, json};
use std::{
    fs::{self, File},
    io::{Read, Write},
    os::fd::FromRawFd,
    path::PathBuf,
    sync::{Arc, Mutex},
};
#[path = "support/factory_ts2.rs"]
mod ts2_descriptors;
struct Audit {
    path: PathBuf,
    value: J,
}
impl Audit {
    fn persist(&self) {
        fs::write(&self.path, serde_json::to_vec(&self.value).unwrap()).unwrap();
    }
    fn control(&mut self, name: &str) {
        self.value["controlSent"]
            .as_array_mut()
            .unwrap()
            .push(json!(name));
        self.persist();
    }
    fn provider(&mut self, name: &str, payload: &Value) {
        self.value["providerReceived"]
            .as_array_mut()
            .unwrap()
            .push(json!(name));
        if name == "SnapshotFileChunk" || name == "DependencySourceChunk" {
            let bytes = match field(payload, "bytes") {
                Value::Bytes(b) => b.len() as u64,
                _ => 0,
            };
            self.value["sourceBytes"] = json!(self.value["sourceBytes"].as_u64().unwrap() + bytes);
        }
        if name == "Analyze" {
            self.value["analyze"] = json!(self.value["analyze"].as_u64().unwrap() + 1);
        }
        self.persist();
    }
}
fn field<'a>(v: &'a Value, name: &str) -> &'a Value {
    if let Value::Map(rows) = v
        && let Some((_, value)) = rows.iter().find(|(k, _)| k == name)
    {
        return value;
    }
    panic!("first-party fixture frame lacks {name}")
}
fn text(v: &Value) -> &str {
    if let Value::Text(s) = v {
        s
    } else {
        panic!("fixture text")
    }
}
fn take(fd: i32) -> File {
    // SAFETY: the provider spawner gives this process sole ownership of the
    // named control descriptor; no other File is constructed for this fd.
    unsafe { File::from_raw_fd(fd) }
}
struct Control {
    output: File,
    seq: u64,
    audit: Arc<Mutex<Audit>>,
}
impl Control {
    fn send(&mut self, name: &str, body: J) {
        // Persist before sending: even immediate refusal/reap cannot lose
        // which deliberate peer message the child actually attempted.
        self.audit.lock().unwrap().control(name);
        let bytes =
            serde_json::to_vec(&json!({"type":name,"seq":self.seq,"controlMajor":1,"body":body}))
                .unwrap();
        self.seq += 1;
        if self
            .output
            .write_all(&(bytes.len() as u32).to_be_bytes())
            .and_then(|()| self.output.write_all(&bytes))
            .is_err()
        {
            std::process::exit(20);
        }
    }
    fn run(mut self, mut input: File, mode: String) {
        loop {
            let mut prefix = [0; 4];
            if input.read_exact(&mut prefix).is_err() {
                return;
            }
            let len = u32::from_be_bytes(prefix) as usize;
            assert!(len <= 65536);
            let mut bytes = vec![0; len];
            if input.read_exact(&mut bytes).is_err() {
                return;
            }
            let frame: J = serde_json::from_slice(&bytes).unwrap();
            let body = &frame["body"];
            match frame["type"].as_str().unwrap() {
                "hello" => {
                    let mut reply = json!({"controlMajor":1,"stableId":body["expectedStableId"],"admittedManifestDigest":body["admittedManifestDigest"],"maxControlFrameBytes":65536,"subprotocolConfirms":body["subprotocolOffers"]});
                    if mode == "stable" {
                        reply["stableId"] = json!("00000000-0000-4000-8000-000000000001");
                    }
                    if mode == "manifest" {
                        reply["admittedManifestDigest"] = json!("0".repeat(64));
                    }
                    self.send("helloAck", reply);
                }
                "select" => {
                    let mut reply = body.clone();
                    if mode == "tuple" {
                        reply["subprotocolVersion"] =
                            json!(body["subprotocolVersion"].as_u64().unwrap() + 1);
                    }
                    self.send("selectAck", reply);
                    if mode == "effect" {
                        self.send("effectRequest",json!({"effectClass":"HE-1","authorizationRef":"fixture-auth","operationRef":"fixture-operation"}));
                    }
                }
                "health" => self.send(
                    "healthReport",
                    json!({"nonce":body["nonce"],"status":"busy"}),
                ),
                "shutdown" => self.send("shutdownAck", json!({})),
                _ => {}
            }
        }
    }
}
fn main() {
    let args: Vec<_> = std::env::args_os().collect();
    let (profile, major, root) = if args.len() == 6
        && args[1] == "--protocol-stdio-v2"
        && args[2] == "--toolchain-root"
        && args[4] == "--scratch-root"
    {
        (Profile::Rust3, 3, PathBuf::from(&args[3]))
    } else if args.len() == 5
        && args[1] == "--no-addons"
        && args[2] == "--no-global-search-paths"
        && args[3]
            .to_str()
            .is_some_and(|s| s.starts_with("--openssl-config="))
    {
        let provider = PathBuf::from(&args[4]);
        let root = provider.parent().unwrap().to_path_buf();
        assert_eq!(
            args[3],
            format!("--openssl-config={}", root.join("openssl.cnf").display()).as_str()
        );
        assert!(fs::read(root.join("openssl.cnf")).unwrap().is_empty());
        (Profile::Ts2, 2, root)
    } else {
        return;
    };
    let fixture = root
        .ancestors()
        .find(|p| {
            p.file_name()
                .and_then(|s| s.to_str())
                .is_some_and(|s| s.starts_with("opensip-d4-"))
        })
        .expect("private first-party fixture root");
    let name = fixture.file_name().unwrap().to_str().unwrap();
    let mode = name
        .strip_prefix("opensip-d4-")
        .unwrap()
        .split('-')
        .next()
        .unwrap()
        .to_owned();
    assert!(
        [
            "stable",
            "manifest",
            "tuple",
            "effect",
            "identity",
            "tokens",
            "baseline",
            "providerdigest",
            "runtimedigest"
        ]
        .contains(&mode.as_str())
    );
    let audit = Arc::new(Mutex::new(Audit {
        path: fixture.join("peer-observation.json"),
        value: json!({"controlSent":[],"providerReceived":[],"providerSent":[],"sourceBytes":0,"analyze":0}),
    }));
    audit.lock().unwrap().persist();
    let control = Control {
        output: take(4),
        seq: 1,
        audit: audit.clone(),
    };
    let control_mode = mode.clone();
    std::thread::spawn(move || control.run(take(3), control_mode));
    let mut input = std::io::stdin().lock();
    let mut output = std::io::stdout().lock();
    while let Ok(Some(frame)) = read_frame(&mut input, profile, 32, None) {
        let name = text(field(frame.value(), "frameType"));
        let payload = field(frame.value(), "payload");
        audit.lock().unwrap().provider(name, payload);
        if name == "Hello" {
            let mut fields = if major == 3 {
                let Value::Map(fields) = field(payload, "expectedIdentity").clone() else {
                    panic!("identity map")
                };
                fields
            } else {
                let mut fields: Vec<_> = ts2_descriptors::provider()
                    .into_iter()
                    .chain(ts2_descriptors::runtime())
                    .collect();
                fields.push((
                    "providerDescriptorSha256".into(),
                    field(payload, "expectedProviderDescriptorSha256").clone(),
                ));
                fields.push((
                    "runtimeDescriptorSha256".into(),
                    field(payload, "expectedRuntimeDescriptorSha256").clone(),
                ));
                fields
            };
            fields.push((
                "capabilities".into(),
                field(payload, "expectedCapabilities").clone(),
            ));
            fields.push((
                "identityVersions".into(),
                field(payload, "identityVersions").clone(),
            ));
            if mode == "identity" {
                fields
                    .iter_mut()
                    .find(|(k, _)| k == "providerBuildId")
                    .unwrap()
                    .1 = Value::Text("wrong-provider".into());
            }
            if mode == "tokens" {
                fields
                    .iter_mut()
                    .find(|(k, _)| k == "capabilities")
                    .unwrap()
                    .1 = Value::Array(vec![]);
            }
            for (mode_name, key) in [
                ("providerdigest", "providerDescriptorSha256"),
                ("runtimedigest", "runtimeDescriptorSha256"),
            ] {
                if mode == mode_name {
                    fields.iter_mut().find(|(k, _)| k == key).unwrap().1 =
                        Value::Text("0".repeat(64));
                }
            }
            let mut envelope = vec![
                ("protocolMajor".into(), Value::Unsigned(major)),
                ("sequence".into(), Value::Unsigned(0)),
                ("frameType".into(), Value::Text("HelloAck".into())),
                ("payload".into(), Value::Map(fields)),
            ];
            if major == 3 {
                envelope.push(("direction".into(), Value::Text("worker-to-host".into())));
            }
            let reply = Value::Map(envelope);
            let bytes = write_frame(&reply).unwrap();
            if output
                .write_all(&bytes)
                .and_then(|()| output.flush())
                .is_err()
            {
                return;
            }
            let mut record = audit.lock().unwrap();
            record.value["providerSent"].as_array_mut().unwrap().push(json!({"frameType":"HelloAck","wireHex":bytes.iter().map(|b|format!("{b:02x}")).collect::<String>()}));
            record.persist();
        } else if name == "OpenUniverse" && mode == "baseline" {
            let mut envelope = vec![
                ("protocolMajor".into(), Value::Unsigned(major)),
                ("sequence".into(), Value::Unsigned(1)),
                ("frameType".into(), Value::Text("UniverseAccepted".into())),
                ("payload".into(), Value::Map(vec![])),
            ];
            if major == 3 {
                envelope.push(("direction".into(), Value::Text("worker-to-host".into())));
            }
            let reply = Value::Map(envelope);
            let bytes = write_frame(&reply).unwrap();
            if output
                .write_all(&bytes)
                .and_then(|()| output.flush())
                .is_err()
            {
                return;
            }
        }
    }
}

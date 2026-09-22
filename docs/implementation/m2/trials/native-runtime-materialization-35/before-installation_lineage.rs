//! Retained native lineage observations under one installation fence.
//! Structural consistency is not a namespace binding, transition authorization,
//! current trust authority, or permission to initialize or publish anything.
use crate::installation_records::{Error as RecordsError, ProvisionalInstallationRecords};
use opensip_lifecycle::{
    DecodedLineageNodeV1, DecodedSelectionV1, LINEAGE_NODE_CAP, LineageDecodeError, LineageKey,
    LineageWalkError, SuppliedLineageChain, inspect_supplied_lineage,
};
use opensip_security::installation_observation::{
    Error as NativeError, InstallationReadFence, ProvisionalHeldFile,
};
use opensip_storage::{ProvisionalStoreMarker, StoreMarkerObservationError};

#[derive(Debug)]
pub enum ReadError {
    Records(RecordsError),
    Native(NativeError),
    Marker(StoreMarkerObservationError),
    Decode(LineageDecodeError),
}
#[derive(Debug)]
pub enum Error {
    Read(ReadError),
    Chain(LineageWalkError<ReadError>),
    Limit,
    Closed,
}

/// All original lineage descriptors, store markers and the selection pair are
/// retained together. No independently supplied observations or native handles
/// can be injected or extracted. Every later consumer rechecks the entire set.
///
/// This read-only owner uses an explicit caller node bound. Joining its work to
/// an authoritative operation budget and qualified registry/core/trust admission
/// is future work. It neither scans directories nor writes missing records.
pub struct ProvisionalInstallationLineage<'fence> {
    records: ProvisionalInstallationRecords<'fence>,
    captures: Vec<ProvisionalHeldFile<'fence>>,
    markers: Vec<ProvisionalStoreMarker<'fence>>,
    chain: SuppliedLineageChain,
    failed: bool,
}
impl<'fence> ProvisionalInstallationLineage<'fence> {
    pub fn read_existing(
        fence: &'fence InstallationReadFence,
        max_nodes: usize,
    ) -> Result<Self, Error> {
        if max_nodes == 0 {
            return Err(Error::Limit);
        }
        let records = ProvisionalInstallationRecords::read_existing(fence)
            .map_err(|e| Error::Read(ReadError::Records(e)))?;
        let pair = records
            .selection()
            .map_err(|e| Error::Read(ReadError::Records(e)))?;
        let start = LineageKey::parse(
            pair.store_instance(),
            pair.store_generation(),
            pair.state_schema(),
        )
        .map_err(|e| Error::Read(ReadError::Decode(e)))?;
        let mut captures = Vec::new();
        let mut markers = Vec::new();
        let attempted = inspect_supplied_lineage(&start, max_nodes, |key| {
            check_all(&records, &captures, &markers)?;
            let observed = (|| {
                let generation = key.store_generation().to_string();
                let leaf = format!("{}.node", key.state_schema());
                let capture = fence
                    .capture_descendant(
                        &["transitions", "lineage", key.store_instance(), &generation],
                        &leaf,
                        LINEAGE_NODE_CAP,
                    )
                    .map_err(ReadError::Native)?;
                let decoded =
                    DecodedLineageNodeV1::decode(capture.bytes().map_err(ReadError::Native)?)
                        .map_err(ReadError::Decode);
                capture.recheck().map_err(ReadError::Native)?; // Also after malformed bytes.
                let node = decoded?;
                let observed_marker =
                    ProvisionalStoreMarker::read_existing(fence, key.store_instance())
                        .map_err(ReadError::Marker);
                capture.recheck().map_err(ReadError::Native)?; // Also after failed marker capture.
                Ok((capture, observed_marker?, node))
            })();
            // A failed later capture must not skip rechecking earlier owners.
            check_all(&records, &captures, &markers)?;
            let (capture, marker, node) = observed?;
            captures.push(capture);
            markers.push(marker);
            Ok(Some(node))
        });
        check_all(&records, &captures, &markers).map_err(Error::Read)?;
        let chain = attempted.map_err(Error::Chain)?;
        let mut result = Self {
            records,
            captures,
            markers,
            chain,
            failed: false,
        };
        result.recheck()?;
        Ok(result)
    }
    pub fn recheck(&mut self) -> Result<(), Error> {
        if self.failed {
            return Err(Error::Closed);
        }
        let result = check_all(&self.records, &self.captures, &self.markers).map_err(Error::Read);
        if result.is_err() {
            self.failed = true;
        }
        result
    }
    /// Decoded syntax remains a claim; copies carry no retained custody.
    pub fn selection(&mut self) -> Result<&DecodedSelectionV1, Error> {
        self.recheck()?;
        let result = self
            .records
            .selection()
            .map_err(|e| Error::Read(ReadError::Records(e)));
        if result.is_err() {
            self.failed = true;
        }
        result
    }
    pub fn nodes(&mut self) -> Result<&[DecodedLineageNodeV1], Error> {
        self.recheck()?;
        Ok(self.chain.nodes())
    }
}

fn check_all(
    records: &ProvisionalInstallationRecords<'_>,
    captures: &[ProvisionalHeldFile<'_>],
    markers: &[ProvisionalStoreMarker<'_>],
) -> Result<(), ReadError> {
    records.recheck().map_err(ReadError::Records)?;
    let attempted = (|| {
        for capture in captures {
            capture.recheck().map_err(ReadError::Native)?;
        }
        for marker in markers {
            marker.recheck().map_err(ReadError::Marker)?;
        }
        // After checking the markers, revisit the original nodes. These checks
        // detect observed changes, not arbitrary ABA or whole-root replacement.
        for capture in captures {
            capture.recheck().map_err(ReadError::Native)?;
        }
        Ok(())
    })();
    records.recheck().map_err(ReadError::Records)?;
    attempted
}

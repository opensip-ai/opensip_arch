//! Exploratory exact-source registry. Hash agreement is shape selection, never
//! descriptor semantics, provenance, execution permission, or complete replay.
use crate::schema::{Error, Program};
use crate::{JsonValue, parse_json, raw_sha256};
use alloc::{
    format,
    string::{String, ToString},
    vec::Vec,
};

pub struct SourcePin {
    id: &'static str,
    path: &'static str,
    bytes: usize,
    sha256: [u8; 32],
}
impl SourcePin {
    pub fn schema_id(&self) -> &'static str {
        self.id
    }
    pub fn source_path(&self) -> &'static str {
        self.path
    }
    pub fn bytes(&self) -> usize {
        self.bytes
    }
    pub fn sha256(&self) -> [u8; 32] {
        self.sha256
    }
}
// Closed exact full-document trial pins.
pub(crate) const SOURCE_PINS: &[SourcePin] = &[
    SourcePin {
        id: "opensip.product.dispatch-binding.1",
        path: "schemas/sources/dispatch-v1.schema.json",
        bytes: 4568,
        sha256: [
            134, 140, 60, 242, 65, 175, 158, 204, 32, 91, 167, 208, 120, 53, 78, 56, 167, 219, 81,
            50, 151, 65, 32, 192, 70, 172, 35, 162, 221, 29, 249, 56,
        ],
    },
    SourcePin {
        id: "opensip.product.enumeration-plan.1",
        path: "schemas/sources/enumeration-plan-v1.schema.json",
        bytes: 19975,
        sha256: [
            16, 98, 124, 182, 162, 42, 159, 241, 103, 76, 22, 197, 250, 72, 99, 165, 141, 200, 110,
            93, 248, 172, 122, 229, 92, 69, 116, 123, 14, 96, 25, 124,
        ],
    },
    SourcePin {
        id: "opensip.product.execution-inputs.1",
        path: "schemas/sources/execution-inputs-v1.schema.json",
        bytes: 39910,
        sha256: [
            96, 75, 217, 65, 117, 88, 65, 40, 173, 190, 178, 65, 253, 186, 47, 72, 226, 34, 13,
            231, 77, 101, 5, 166, 113, 234, 226, 206, 137, 39, 0, 233,
        ],
    },
    SourcePin {
        id: "opensip.product.fact-batch.3",
        path: "schemas/sources/fact-batch-v3.schema.json",
        bytes: 10028,
        sha256: [
            176, 235, 193, 51, 223, 135, 99, 246, 205, 95, 55, 22, 84, 35, 33, 235, 162, 28, 105,
            113, 79, 202, 54, 143, 190, 49, 186, 87, 103, 122, 36, 224,
        ],
    },
    SourcePin {
        id: "opensip.product.framework-recognition-plan.1",
        path: "schemas/sources/framework-recognition-plan-v1.schema.json",
        bytes: 10188,
        sha256: [
            73, 170, 205, 134, 7, 227, 243, 25, 90, 195, 80, 182, 120, 243, 24, 56, 138, 95, 175,
            143, 86, 244, 46, 82, 8, 126, 201, 235, 229, 126, 248, 34,
        ],
    },
    SourcePin {
        id: "opensip.product.incoming-search.1",
        path: "schemas/sources/incoming-search-v1.schema.json",
        bytes: 13724,
        sha256: [
            172, 203, 89, 122, 149, 150, 145, 9, 252, 136, 207, 64, 234, 218, 41, 98, 49, 175, 229,
            16, 9, 61, 111, 181, 100, 73, 246, 203, 244, 101, 184, 161,
        ],
    },
    SourcePin {
        id: "opensip.product.occupancy-companion.1",
        path: "schemas/sources/occupancy-v1.schema.json",
        bytes: 8821,
        sha256: [
            210, 187, 188, 196, 154, 219, 177, 48, 208, 187, 1, 15, 238, 11, 76, 242, 90, 247, 114,
            127, 115, 15, 195, 41, 114, 95, 166, 44, 212, 106, 225, 79,
        ],
    },
    SourcePin {
        id: "opensip.product.provider-handshake.1",
        path: "schemas/sources/handshake-v1.schema.json",
        bytes: 32009,
        sha256: [
            144, 144, 226, 173, 81, 183, 103, 161, 118, 245, 29, 160, 159, 32, 24, 3, 209, 204,
            130, 192, 71, 173, 230, 129, 2, 173, 202, 225, 238, 58, 95, 132,
        ],
    },
    SourcePin {
        id: "opensip.product.provider-startup.1",
        path: "schemas/sources/startup-v1.schema.json",
        bytes: 33341,
        sha256: [
            30, 53, 167, 123, 174, 141, 156, 32, 23, 26, 147, 78, 156, 22, 228, 222, 77, 124, 233,
            139, 176, 36, 1, 109, 126, 23, 207, 155, 11, 56, 114, 156,
        ],
    },
    SourcePin {
        id: "opensip.product.relation-payload.2",
        path: "schemas/sources/relation-payload-v2.schema.json",
        bytes: 57623,
        sha256: [
            83, 56, 10, 36, 85, 73, 14, 7, 2, 142, 24, 114, 85, 112, 68, 251, 27, 105, 208, 98, 20,
            61, 238, 238, 192, 244, 64, 6, 240, 178, 190, 154,
        ],
    },
    SourcePin {
        id: "opensip.product.subject-inventory.1",
        path: "schemas/sources/subject-inventory-v1.schema.json",
        bytes: 16861,
        sha256: [
            106, 180, 105, 37, 133, 61, 38, 193, 165, 247, 174, 31, 189, 105, 219, 93, 204, 144,
            82, 253, 239, 219, 27, 38, 94, 83, 72, 27, 78, 28, 238, 51,
        ],
    },
    SourcePin {
        id: "opensip.product.target-attribution.2",
        path: "schemas/sources/target-attribution-v2.schema.json",
        bytes: 23086,
        sha256: [
            189, 147, 143, 17, 197, 132, 190, 101, 233, 20, 188, 20, 70, 25, 63, 223, 61, 212, 161,
            95, 123, 120, 99, 12, 195, 235, 98, 140, 91, 202, 29, 83,
        ],
    },
    SourcePin {
        id: "urn:opensip:design:control-schema:3",
        path: "schemas/sources/control-v3.schema.json",
        bytes: 22476,
        sha256: [
            41, 41, 222, 98, 233, 235, 58, 61, 199, 137, 89, 234, 243, 213, 3, 97, 184, 209, 248,
            149, 208, 134, 148, 7, 36, 193, 199, 67, 172, 70, 169, 140,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:evaluator-emission-plan:1",
        path: "schemas/sources/evaluator-emission-plan-v1.schema.json",
        bytes: 3055,
        sha256: [
            172, 154, 228, 56, 202, 62, 26, 148, 226, 87, 32, 156, 70, 12, 215, 190, 237, 80, 71,
            224, 217, 208, 167, 191, 73, 169, 75, 99, 125, 211, 25, 142,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:identity:v3",
        path: "schemas/sources/identity-v3.schema.json",
        bytes: 197480,
        sha256: [
            49, 28, 31, 235, 9, 255, 140, 208, 178, 7, 35, 61, 46, 192, 215, 68, 11, 177, 199, 47,
            192, 71, 13, 226, 119, 238, 24, 145, 194, 75, 182, 143,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:import-source-context",
        path: "schemas/sources/import-source-context-v1.schema.json",
        bytes: 842,
        sha256: [
            81, 205, 202, 139, 211, 201, 33, 45, 17, 152, 36, 22, 185, 16, 27, 233, 107, 220, 244,
            125, 178, 46, 251, 0, 152, 179, 156, 120, 80, 174, 101, 24,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:native:evidence-schemas:v2",
        path: "schemas/sources/native-v2.schema.json",
        bytes: 280357,
        sha256: [
            229, 131, 77, 55, 174, 189, 150, 215, 125, 53, 41, 117, 135, 141, 163, 73, 3, 63, 134,
            51, 236, 189, 131, 50, 42, 208, 251, 234, 70, 31, 119, 115,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:policy-document:2",
        path: "schemas/sources/policy-v2.schema.json",
        bytes: 26534,
        sha256: [
            178, 33, 181, 237, 111, 142, 110, 63, 251, 207, 166, 83, 88, 192, 254, 38, 162, 188,
            121, 9, 85, 12, 110, 27, 236, 68, 137, 79, 65, 60, 155, 85,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:report:configuration-disclosure:1",
        path: "schemas/sources/configuration-disclosure-v1.schema.json",
        bytes: 17322,
        sha256: [
            5, 132, 191, 47, 214, 253, 158, 238, 136, 121, 164, 220, 164, 69, 105, 178, 185, 98,
            143, 85, 163, 66, 248, 55, 195, 19, 193, 131, 198, 158, 246, 89,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:report:explicit-history-panel:1",
        path: "schemas/sources/explicit-history-panel-v1.schema.json",
        bytes: 4171,
        sha256: [
            105, 75, 196, 194, 182, 83, 166, 56, 36, 210, 121, 89, 54, 254, 38, 96, 81, 182, 210,
            28, 83, 13, 145, 157, 44, 3, 19, 178, 54, 189, 146, 110,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:report:explicit-history:1",
        path: "schemas/sources/explicit-history-v1.schema.json",
        bytes: 1942,
        sha256: [
            63, 199, 139, 197, 147, 174, 16, 79, 9, 244, 68, 141, 159, 55, 43, 210, 204, 245, 227,
            93, 151, 249, 201, 123, 1, 33, 57, 208, 5, 134, 154, 148,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:common",
        path: "schemas/sources/common-v1.schema.json",
        bytes: 55042,
        sha256: [
            183, 178, 93, 94, 124, 43, 242, 200, 211, 73, 106, 47, 34, 44, 49, 188, 200, 115, 96,
            243, 226, 84, 31, 189, 181, 81, 19, 99, 88, 247, 211, 156,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:baseline:2",
        path: "schemas/sources/baseline-v2.schema.json",
        bytes: 12734,
        sha256: [
            213, 18, 105, 137, 168, 217, 107, 169, 82, 212, 27, 107, 68, 81, 242, 29, 95, 240, 95,
            32, 13, 171, 151, 231, 139, 168, 48, 54, 167, 199, 185, 110,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-envelope:3",
        path: "schemas/sources/envelope-v3.schema.json",
        bytes: 26011,
        sha256: [
            9, 41, 47, 193, 8, 242, 35, 201, 187, 55, 81, 6, 243, 155, 41, 21, 1, 9, 190, 2, 178,
            204, 204, 204, 185, 169, 78, 87, 238, 49, 136, 48,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4",
        path: "schemas/sources/envelope-v4.schema.json",
        bytes: 29283,
        sha256: [
            107, 86, 56, 97, 156, 190, 44, 174, 228, 91, 158, 146, 177, 113, 171, 164, 71, 251,
            143, 167, 92, 179, 247, 157, 42, 248, 151, 19, 249, 66, 14, 168,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7",
        path: "schemas/sources/command-envelope-v7.schema.json",
        bytes: 42632,
        sha256: [
            44, 182, 200, 173, 174, 238, 212, 252, 27, 82, 87, 58, 41, 28, 29, 229, 218, 81, 44,
            12, 249, 236, 27, 30, 15, 170, 104, 49, 60, 77, 67, 111,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-inventory:3",
        path: "schemas/sources/inventory-v3.schema.json",
        bytes: 17924,
        sha256: [
            52, 228, 178, 192, 20, 118, 230, 6, 49, 15, 94, 234, 60, 3, 184, 142, 206, 68, 234, 22,
            217, 99, 206, 22, 99, 37, 10, 234, 16, 115, 117, 92,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-inventory:4",
        path: "schemas/sources/inventory-v4.schema.json",
        bytes: 20445,
        sha256: [
            179, 171, 67, 36, 236, 33, 130, 227, 254, 151, 204, 218, 226, 214, 217, 121, 25, 76,
            95, 63, 16, 169, 172, 124, 150, 17, 154, 193, 205, 206, 44, 85,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:command-inventory:6",
        path: "schemas/sources/command-inventory-v6.schema.json",
        bytes: 23283,
        sha256: [
            10, 24, 228, 158, 136, 164, 87, 90, 105, 18, 70, 134, 238, 199, 107, 144, 142, 90, 254,
            12, 44, 71, 119, 59, 238, 211, 254, 172, 118, 105, 74, 240,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:common:3",
        path: "schemas/sources/common-v3.schema.json",
        bytes: 64623,
        sha256: [
            206, 69, 185, 255, 113, 47, 160, 234, 67, 2, 251, 218, 240, 76, 184, 77, 253, 138, 60,
            247, 52, 244, 249, 103, 124, 69, 71, 103, 42, 243, 10, 139,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:common:4",
        path: "schemas/sources/common-v4.schema.json",
        bytes: 64866,
        sha256: [
            106, 248, 31, 53, 197, 60, 231, 74, 203, 176, 96, 157, 80, 82, 74, 185, 208, 176, 174,
            28, 43, 119, 46, 149, 129, 223, 185, 248, 83, 94, 174, 217,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:comparison:2",
        path: "schemas/sources/comparison-v2.schema.json",
        bytes: 34574,
        sha256: [
            248, 42, 48, 112, 33, 128, 237, 21, 101, 193, 51, 41, 27, 145, 7, 41, 64, 43, 212, 247,
            243, 49, 72, 197, 254, 6, 158, 157, 132, 10, 170, 138,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:detector-manifest:1",
        path: "schemas/sources/detector-v1.schema.json",
        bytes: 2043,
        sha256: [
            28, 189, 105, 201, 210, 155, 6, 139, 149, 199, 206, 133, 49, 0, 118, 113, 226, 75, 146,
            67, 56, 40, 202, 48, 168, 122, 102, 55, 216, 29, 253, 205,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:graph-query:3",
        path: "schemas/sources/graph-v3.schema.json",
        bytes: 35863,
        sha256: [
            51, 164, 59, 216, 110, 199, 188, 177, 142, 93, 74, 195, 214, 95, 85, 67, 245, 123, 125,
            34, 22, 138, 0, 78, 221, 79, 29, 173, 40, 95, 235, 233,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:graph-query:4",
        path: "schemas/sources/graph-query-v4.schema.json",
        bytes: 39664,
        sha256: [
            53, 227, 127, 89, 228, 16, 179, 172, 105, 163, 122, 0, 23, 27, 98, 45, 251, 239, 106,
            19, 162, 161, 178, 206, 240, 248, 81, 120, 120, 147, 35, 33,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:invocation:3",
        path: "schemas/sources/invocation-v3.schema.json",
        bytes: 68066,
        sha256: [
            101, 152, 2, 38, 220, 95, 135, 156, 58, 50, 74, 40, 130, 118, 134, 22, 118, 163, 123,
            71, 222, 122, 199, 15, 242, 30, 193, 131, 98, 71, 221, 200,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:invocation:5",
        path: "schemas/sources/invocation-v5.schema.json",
        bytes: 71161,
        sha256: [
            40, 170, 12, 66, 176, 95, 163, 173, 19, 174, 77, 154, 237, 27, 172, 23, 152, 52, 83,
            87, 115, 6, 184, 225, 86, 120, 220, 116, 175, 99, 244, 251,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:policy-test:2",
        path: "schemas/sources/policy-test-v2.schema.json",
        bytes: 9876,
        sha256: [
            124, 47, 222, 220, 137, 228, 118, 222, 35, 147, 30, 15, 140, 209, 163, 203, 28, 167,
            165, 200, 90, 181, 251, 85, 113, 186, 239, 67, 215, 192, 233, 186,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:repair:2",
        path: "schemas/sources/repair-v2.schema.json",
        bytes: 58683,
        sha256: [
            103, 141, 138, 79, 254, 24, 49, 161, 64, 175, 48, 37, 79, 71, 65, 102, 129, 118, 105,
            255, 10, 8, 251, 15, 162, 143, 231, 89, 239, 131, 175, 44,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:report-projection:1",
        path: "schemas/sources/report-v1.schema.json",
        bytes: 161357,
        sha256: [
            187, 181, 202, 146, 15, 210, 178, 108, 140, 206, 44, 108, 37, 221, 78, 219, 3, 56, 101,
            148, 249, 100, 90, 93, 7, 14, 214, 26, 85, 154, 204, 151,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:review:2",
        path: "schemas/sources/review-v2.schema.json",
        bytes: 10710,
        sha256: [
            156, 112, 94, 77, 85, 11, 195, 129, 99, 6, 131, 43, 224, 226, 216, 55, 82, 178, 38, 74,
            1, 143, 187, 122, 228, 20, 30, 170, 100, 80, 37, 238,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:evaluator3:sarif-adapter:2",
        path: "schemas/sources/sarif-v2.schema.json",
        bytes: 9598,
        sha256: [
            238, 101, 176, 57, 142, 228, 71, 232, 221, 89, 247, 96, 237, 107, 136, 22, 245, 223,
            255, 173, 213, 105, 94, 81, 247, 175, 250, 52, 187, 51, 124, 13,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:imported-evidence",
        path: "schemas/sources/imported-v1.schema.json",
        bytes: 46315,
        sha256: [
            237, 206, 33, 163, 199, 144, 95, 33, 92, 1, 158, 221, 197, 119, 110, 8, 230, 207, 245,
            154, 108, 238, 164, 180, 228, 34, 39, 94, 173, 89, 75, 158,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:metadata:1",
        path: "schemas/sources/metadata-v1.schema.json",
        bytes: 5245,
        sha256: [
            165, 141, 233, 15, 71, 19, 204, 195, 47, 131, 137, 41, 24, 91, 116, 61, 54, 86, 145,
            90, 33, 86, 86, 48, 199, 28, 173, 18, 147, 31, 199, 28,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:policy-document",
        path: "schemas/sources/policy-v1.schema.json",
        bytes: 20724,
        sha256: [
            1, 37, 5, 218, 71, 145, 151, 135, 86, 2, 137, 156, 2, 123, 61, 13, 174, 169, 226, 62,
            1, 228, 144, 227, 220, 148, 187, 227, 215, 6, 46, 24,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:policy-test",
        path: "schemas/sources/policy-test-v1.schema.json",
        bytes: 16045,
        sha256: [
            20, 74, 134, 2, 69, 24, 196, 31, 88, 25, 146, 154, 47, 32, 190, 252, 28, 6, 250, 50,
            77, 142, 225, 21, 252, 220, 208, 173, 217, 197, 252, 161,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:presentation-catalog:1",
        path: "schemas/sources/presentation-catalog-v1.schema.json",
        bytes: 7058,
        sha256: [
            223, 106, 17, 51, 17, 105, 135, 221, 85, 196, 72, 184, 251, 169, 136, 249, 35, 8, 225,
            100, 150, 73, 231, 116, 170, 136, 190, 85, 111, 191, 82, 17,
        ],
    },
    SourcePin {
        id: "urn:opensip:product-v1:workflows:test-execution",
        path: "schemas/sources/test-execution-v1.schema.json",
        bytes: 13672,
        sha256: [
            166, 247, 194, 216, 92, 220, 76, 75, 176, 24, 40, 141, 150, 47, 125, 48, 56, 79, 216,
            146, 65, 98, 160, 203, 92, 149, 88, 45, 224, 67, 213, 75,
        ],
    },
];
pub(crate) const DOCUMENT_ALIASES: &[(&str, &str)] = &[
    (
        "foundation/enumeration-plan.schema.v1.json",
        "opensip.product.enumeration-plan.1",
    ),
    (
        "foundation/evaluator-emission-plan.schema.v1.json",
        "urn:opensip:product-v1:evaluator-emission-plan:1",
    ),
    (
        "foundation/execution-inputs.schema.v1.json",
        "opensip.product.execution-inputs.1",
    ),
    (
        "foundation/framework-recognition-plan.schema.v1.json",
        "opensip.product.framework-recognition-plan.1",
    ),
    (
        "foundation/import-source-context.schema.json",
        "urn:opensip:product-v1:import-source-context",
    ),
    (
        "foundation/incoming-search.schema.v1.json",
        "opensip.product.incoming-search.1",
    ),
    (
        "foundation/relation-payload-schemas.v2.json",
        "opensip.product.relation-payload.2",
    ),
    (
        "foundation/subject-inventory.schema.v1.json",
        "opensip.product.subject-inventory.1",
    ),
    (
        "foundation/target-attribution.schema.v2.json",
        "opensip.product.target-attribution.2",
    ),
    (
        "native/native-evidence.schemas.v2.json",
        "urn:opensip:product-v1:native:evidence-schemas:v2",
    ),
    (
        "workflows/schemas/common.schema.json",
        "urn:opensip:product-v1:workflows:common",
    ),
    (
        "workflows/schemas/imported-evidence.schema.json",
        "urn:opensip:product-v1:workflows:imported-evidence",
    ),
    (
        "workflows/schemas/policy-document.schema.json",
        "urn:opensip:product-v1:workflows:policy-document",
    ),
    (
        "workflows/schemas/policy-document.v2.schema.json",
        "urn:opensip:product-v1:policy-document:2",
    ),
    (
        "workflows/schemas/test-execution.schema.json",
        "urn:opensip:product-v1:workflows:test-execution",
    ),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdmissionError {
    SourceSet,
    SourceBytes,
    UnsupportedCodec,
    Schema(Error),
    Mismatch,
}
impl From<Error> for AdmissionError {
    fn from(e: Error) -> Self {
        Self::Schema(e)
    }
}

/// Owns exact schema documents and a checked local reference closure. No public
/// constructor from arbitrary parsed schemas, resolver, paths or environment.
pub struct RegisteredSchemas {
    program: Program,
}
impl RegisteredSchemas {
    pub fn source_requirements() -> &'static [SourcePin] {
        SOURCE_PINS
    }
    /// Inputs follow source_requirements order, with complete raw-document pins.
    /// Length is checked before hashing/parsing; any absent/extra/replaced input
    /// refuses the entire registry. No mutable caller buffer is retained.
    pub fn from_sources(sources: &[&[u8]]) -> Result<Self, AdmissionError> {
        if sources.len() != SOURCE_PINS.len() {
            return Err(AdmissionError::SourceSet);
        }
        let mut documents = Vec::with_capacity(sources.len());
        let mut entries = Vec::new();
        for (source, pin) in sources.iter().zip(SOURCE_PINS) {
            if source.len() != pin.bytes || raw_sha256(source) != pin.sha256 {
                return Err(AdmissionError::SourceBytes);
            }
            let document = parse_json(source).map_err(|_| AdmissionError::Schema(Error::Json))?;
            let JsonValue::Object(root) = &document else {
                return Err(AdmissionError::Schema(Error::Schema));
            };
            if !matches!(root.get("$id"),Some(JsonValue::String(id)) if id==pin.id) {
                return Err(AdmissionError::Schema(Error::Schema));
            }
            entries.push(format!("{}#", pin.id));
            if let Some(JsonValue::Object(defs)) = root.get("$defs") {
                for name in defs.keys() {
                    entries.push(format!(
                        "{}#/$defs/{}",
                        pin.id,
                        name.replace('~', "~0").replace('/', "~1")
                    ));
                }
            }
            documents.push(document);
        }
        let refs: Vec<_> = entries.iter().map(String::as_str).collect();
        let program = Program::compile(documents, &refs, 200_000_000)?;
        Ok(Self { program })
    }
    /// Exact current logical alias plus full-document digest. Same-URI historical
    /// bytes never acquire current interpretation by version fallback.
    pub fn record_schema(
        &self,
        document: &str,
        digest: [u8; 32],
        selector: &str,
    ) -> Result<SchemaHandle<'_>, AdmissionError> {
        let id = DOCUMENT_ALIASES
            .iter()
            .find(|r| r.0 == document)
            .map(|r| r.1)
            .ok_or(AdmissionError::SourceSet)?;
        let handle = self.schema(id, selector)?;
        if handle.document_sha256() != digest {
            return Err(AdmissionError::SourceBytes);
        }
        Ok(handle)
    }
    /// A selector is an exact JSON pointer relative to the complete pinned
    /// document, with empty string selecting its root. No version fallback.
    pub fn schema(&self, id: &str, selector: &str) -> Result<SchemaHandle<'_>, AdmissionError> {
        if id == "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
            && selector.is_empty()
        {
            return Err(AdmissionError::UnsupportedCodec);
        }
        let index = SOURCE_PINS
            .iter()
            .position(|p| p.id == id)
            .ok_or(AdmissionError::SourceSet)?;
        let entry = format!("{id}#{selector}");
        if !self.program.has_entry(&entry) {
            return Err(AdmissionError::Schema(Error::UnselectedEntry));
        }
        Ok(SchemaHandle {
            registry: self,
            index,
            selector: selector.to_string(),
            entry,
        })
    }
}
/// Opaque read-only shape selector. Carries the full raw-document identity,
/// not a digest of an isolated subschema or a caller-supplied claimed digest.
pub struct SchemaHandle<'a> {
    registry: &'a RegisteredSchemas,
    index: usize,
    selector: String,
    entry: String,
}
impl<'a> SchemaHandle<'a> {
    pub fn schema_id(&self) -> &'static str {
        SOURCE_PINS[self.index].id
    }
    pub fn document_sha256(&self) -> [u8; 32] {
        SOURCE_PINS[self.index].sha256
    }
    pub fn selector(&self) -> &str {
        &self.selector
    }
    /// Consumes this handle and returns an opaque shape-only value on complete
    /// success. Limits/ref/schema faults never become mismatch or evidence.
    pub fn admit_json(self, raw: &[u8], budget: usize) -> Result<ShapeValue<'a>, AdmissionError> {
        let value = self
            .registry
            .program
            .admit_json(&self.entry, raw, budget)?
            .ok_or(AdmissionError::Mismatch)?;
        Ok(ShapeValue {
            schema: self,
            value,
        })
    }
}
/// Not a semantically admitted descriptor, authorized command, or ReplayedRun.
/// No Deserialize/default/public fields; extracting the inert value loses this
/// shape account. Further exact digest/domain/identity joins remain mandatory.
pub struct ShapeValue<'a> {
    schema: SchemaHandle<'a>,
    value: JsonValue,
}
impl ShapeValue<'_> {
    pub fn schema(&self) -> &SchemaHandle<'_> {
        &self.schema
    }
    pub fn value(&self) -> &JsonValue {
        &self.value
    }
    pub fn into_value(self) -> JsonValue {
        self.value
    }
}

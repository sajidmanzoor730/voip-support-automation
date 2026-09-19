DROP TABLE IF EXISTS capture_inventory;
DROP TABLE IF EXISTS rtp_measurements;

CREATE TABLE capture_inventory (
  capture_name TEXT PRIMARY KEY,
  protocol_scope TEXT NOT NULL,
  description TEXT NOT NULL,
  evidence_type TEXT NOT NULL,
  source_url TEXT NOT NULL
);

CREATE TABLE rtp_measurements (
  source_capture TEXT NOT NULL,
  stream_ssrc TEXT NOT NULL,
  frame_number INTEGER NOT NULL,
  frame_time TEXT NOT NULL,
  rtp_timestamp INTEGER NOT NULL,
  payload_type TEXT NOT NULL,
  sampling_hz INTEGER NOT NULL,
  delta_seconds REAL,
  delta_timestamp_seconds REAL,
  transit_difference_seconds REAL,
  jitter_ms REAL,
  source_url TEXT NOT NULL,
  PRIMARY KEY (source_capture, stream_ssrc, frame_number)
);

.mode csv
.import --skip 1 data/public_capture_inventory.csv capture_inventory
.import --skip 1 data/rtp_measurements.csv rtp_measurements

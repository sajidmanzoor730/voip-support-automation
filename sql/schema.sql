DROP TABLE IF EXISTS call_records;
CREATE TABLE call_records (
  call_id TEXT PRIMARY KEY,
  start_time TEXT NOT NULL,
  duration_sec INTEGER NOT NULL,
  mos REAL NOT NULL,
  packet_loss_pct REAL NOT NULL,
  jitter_ms REAL NOT NULL,
  setup_ms INTEGER NOT NULL,
  termination TEXT NOT NULL,
  issue_category TEXT NOT NULL
);

.mode csv
.import --skip 1 data/call_records.csv call_records

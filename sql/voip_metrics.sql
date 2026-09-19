-- Evidence-backed queries. These operate on public capture metadata
-- and the packet-level RTP example reproduced from Wireshark documentation.

.headers on
.mode column

-- 1. Public VoIP evidence inventory
SELECT
  protocol_scope,
  COUNT(*) AS capture_artifacts
FROM capture_inventory
GROUP BY protocol_scope
ORDER BY capture_artifacts DESC;

-- 2. Capture records suitable for SIP/RTP investigation
SELECT capture_name, protocol_scope, description
FROM capture_inventory
WHERE protocol_scope LIKE '%SIP%'
   OR protocol_scope LIKE '%RTP%'
ORDER BY capture_name;

-- 3. Verified packet-level RTP measurements
SELECT
  source_capture,
  stream_ssrc,
  frame_number,
  frame_time,
  rtp_timestamp,
  payload_type,
  sampling_hz,
  ROUND(jitter_ms, 3) AS jitter_ms
FROM rtp_measurements
ORDER BY frame_number;

-- 4. Maximum measured jitter in the documented example
SELECT
  source_capture,
  ROUND(MAX(jitter_ms), 3) AS max_measured_jitter_ms
FROM rtp_measurements
GROUP BY source_capture;

-- 5. Evidence records with an external provenance link
SELECT capture_name, evidence_type, source_url
FROM capture_inventory
ORDER BY capture_name;

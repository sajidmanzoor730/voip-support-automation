-- VoIP Support Automation Toolkit
-- Evidence-based investigation queries
--
-- Data sources:
-- 1. Public Wireshark VoIP capture inventory
-- 2. RTP measurements documented in Wireshark's RTP statistics example
--
-- These queries do NOT use synthetic call-quality data.

.headers on
.mode column


-- ============================================================
-- 1. PUBLIC VOIP CAPTURE INVENTORY
-- ============================================================
-- Shows how many public evidence artifacts exist
-- for each protocol/media category.

SELECT
    protocol_scope,
    COUNT(*) AS capture_artifacts
FROM capture_inventory
GROUP BY protocol_scope
ORDER BY capture_artifacts DESC;


-- ============================================================
-- 2. SIP / RTP CAPTURE EVIDENCE
-- ============================================================
-- Lists captures that can be used for SIP/RTP investigation.

SELECT
    capture_name,
    protocol_scope,
    description,
    evidence_type
FROM capture_inventory
WHERE protocol_scope LIKE '%SIP%'
   OR protocol_scope LIKE '%RTP%'
ORDER BY capture_name;


-- ============================================================
-- 3. RTP PACKET MEASUREMENTS
-- ============================================================
-- Displays the documented packet-level RTP measurements.

SELECT
    source_capture,
    stream_ssrc,
    frame_number,
    frame_time,
    rtp_timestamp,
    payload_type,
    sampling_hz,
    ROUND(delta_seconds, 6) AS delta_seconds,
    ROUND(delta_timestamp_seconds, 6) AS delta_timestamp_seconds,
    ROUND(transit_difference_seconds, 6) AS transit_difference_seconds,
    ROUND(jitter_ms, 3) AS jitter_ms
FROM rtp_measurements
ORDER BY
    source_capture,
    stream_ssrc,
    frame_number;


-- ============================================================
-- 4. MAXIMUM DOCUMENTED JITTER
-- ============================================================
-- Finds the highest measured jitter in the documented
-- RTP measurement set.

SELECT
    source_capture,
    stream_ssrc,
    ROUND(MAX(jitter_ms), 3) AS max_measured_jitter_ms
FROM rtp_measurements
GROUP BY
    source_capture,
    stream_ssrc
ORDER BY
    max_measured_jitter_ms DESC;


-- ============================================================
-- 5. RTP PAYLOAD TYPES
-- ============================================================
-- Shows the RTP payload types represented in the
-- measurement dataset.

SELECT
    payload_type,
    sampling_hz,
    COUNT(*) AS packet_measurements
FROM rtp_measurements
GROUP BY
    payload_type,
    sampling_hz
ORDER BY
    packet_measurements DESC;


-- ============================================================
-- 6. CAPTURE SOURCE LINKS
-- ============================================================
-- Keeps evidence provenance visible inside the SQL output.

SELECT
    capture_name,
    evidence_type,
    source_url
FROM capture_inventory
ORDER BY capture_name;


-- ============================================================
-- 7. RTP EVIDENCE SUMMARY
-- ============================================================
-- Provides a compact summary for a support dashboard.

SELECT
    COUNT(*) AS measured_rtp_frames,
    COUNT(DISTINCT stream_ssrc) AS rtp_streams,
    MIN(frame_number) AS first_frame,
    MAX(frame_number) AS last_frame,
    ROUND(MAX(jitter_ms), 3) AS maximum_documented_jitter_ms
FROM rtp_measurements;

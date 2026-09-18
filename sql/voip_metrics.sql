-- Run after schema.sql.
.headers on
.mode column

-- 1. Overall quality metrics
SELECT
  COUNT(*) AS calls,
  ROUND(AVG(mos), 2) AS avg_mos,
  ROUND(AVG(packet_loss_pct), 2) AS avg_packet_loss_pct,
  ROUND(AVG(jitter_ms), 2) AS avg_jitter_ms,
  ROUND(AVG(setup_ms), 0) AS avg_setup_ms
FROM call_records;

-- 2. Calls needing investigation
SELECT call_id, mos, packet_loss_pct, jitter_ms, setup_ms, issue_category
FROM call_records
WHERE mos < 3.5
   OR packet_loss_pct >= 2.0
   OR jitter_ms >= 15
   OR setup_ms >= 250
ORDER BY mos ASC;

-- 3. Issue distribution
SELECT issue_category, COUNT(*) AS incidents
FROM call_records
GROUP BY issue_category
ORDER BY incidents DESC;

-- 4. Repeat pattern: one-way audio
SELECT call_id, duration_sec, mos, packet_loss_pct, jitter_ms
FROM call_records
WHERE issue_category = 'one_way_audio';

-- 5. High setup latency
SELECT call_id, setup_ms, termination
FROM call_records
WHERE setup_ms >= 250
ORDER BY setup_ms DESC;

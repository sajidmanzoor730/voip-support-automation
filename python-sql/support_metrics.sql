-- VoIP Support Automation - Support Metrics Dashboard
-- For SLA, CSAT, MTTR reporting

-- 1. SLA Compliance (P1 < 2hr, P2 < 8hr)
SELECT
  priority,
  COUNT(*) as total_tickets,
  SUM(CASE WHEN sla_breached = 0 THEN 1 ELSE 0 END) as within_sla,
  ROUND(100.0 * SUM(CASE WHEN sla_breached = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as sla_percent
FROM tickets
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY priority;

-- 2. Repeatable Pattern Analysis (40% volume)
SELECT
  issue_type,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as percent_of_volume
FROM tickets
WHERE issue_type IN ('SIP 401', 'SIP 403', 'One-way Audio', 'RTP Loss', 'API Auth')
GROUP BY issue_type
ORDER BY count DESC;

-- 3. Ticket Deflection via KB Articles
SELECT
  kb_article_id,
  COUNT(*) as deflected_tickets,
  AVG(csat_score) as avg_csat
FROM tickets
WHERE resolved_by_kb = true
GROUP BY kb_article_id;

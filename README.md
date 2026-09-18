# VoIP Support Automation Toolkit

A practical, runnable support-engineering portfolio project for diagnosing common SIP/VoIP, API, network, and ticketing issues.

## What is real here?

The artifacts are real, executable examples:
- The Python SIP log parser actually parses the included sample log and produces a JSON summary.
- The Postman collection contains executable API checks against `https://httpbin.org`.
- The SQL queries run against the included SQLite dataset.
- The Wireshark filters are valid display-filter examples.
- The JIRA/Zendesk material is an implementation blueprint, not a claim of access to those systems.

## Important data note

The included call records and SIP logs are **synthetic test data**, deliberately created for a public portfolio. They do not represent a real customer, company, carrier, phone number, IP address, or production incident. Metrics in the project are calculated from this test dataset and must not be presented as historical employer results.

## Structure

- `postman/voip-api-health.postman_collection.json` — API health checks
- `wireshark/voip-filters.md` — practical SIP/RTP/DNS/TCP filters
- `sip-parser/parse_sip_log.py` — working SIP log parser
- `sip-parser/sample_sip.log` — test input
- `sql/schema.sql` — SQLite schema + seed data
- `sql/voip_metrics.sql` — support metrics and investigation queries
- `data/call_records.csv` — synthetic call-quality dataset
- `automation/jira-zendesk-blueprint.md` — ticket automation design
- `docs/incident-runbook.md` — end-to-end troubleshooting workflow

## Quick start

### Run the SIP parser
```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log
```

### Run the SQL dashboard queries
```bash
sqlite3 voip.db < sql/schema.sql
sqlite3 voip.db < sql/voip_metrics.sql
```

### Postman
Import the collection into Postman and run the collection. It uses public HTTP test endpoints and does not require credentials.

# VoIP Support Toolkit

A personal learning project: a small toolkit for investigating SIP/VoIP issues using packet evidence, SQL, API checks and ticket-triage logic.

## Data and provenance
All evidence comes from **public Wireshark sample captures** (for example SIP/RTP G.711 and SIP DTMF captures). It is not customer data, employer data or live production telemetry.

The repo includes one worked RTP example based on Wireshark's documentation: stream SSRC `932629361`, frames 624-626, G.711 PCMA (payload type 8), with the interarrival jitter calculated by hand at about 1.029 ms.

## What is included
- Python SIP log parser (runs on a small sanitized sample log)
- SQL schema and investigation queries (SQLite)
- Public capture inventory and RTP measurement tables
- Wireshark filters for SIP, RTP, DNS and TCP troubleshooting
- Postman collection for API health checks (public test endpoints, no credentials)
- Ticket-triage notes for Jira/Zendesk and a short incident runbook

## How it works
```
PCAP -> Wireshark/TShark -> SIP + SDP + RTP fields -> SQL -> issue classification -> support/RCA notes
```

## Quick start

Parser:
```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log
```

SQL:
```bash
sqlite3 voip.db < sql/schema.sql
sqlite3 voip.db < sql/voip_metrics.sql
```

Postman: import `postman/voip-api-health.postman_collection.json` and run the collection.

## Files
- `data/public_capture_inventory.csv` - public capture catalog
- `data/rtp_measurements.csv` - RTP example values
- `data/source_notes.md` - sources and notes
- `sip-parser/sample_sip.log` - parser test fixture only

## Author
Sajid Manzoor | saajidmanzoor730@gmail.com

# VoIP Support Automation Toolkit

A support-engineering toolkit for investigating SIP/VoIP incidents using packet evidence, structured analysis, SQL, API checks, and ticket-triage logic.

## Evidence model

The dashboard no longer uses invented call-quality metrics as if they were operational history.

The primary evidence set is based on **public Wireshark VoIP sample captures and documented packet-level observations**. Wireshark publishes SIP/RTP captures such as `aaa.pcap`, `SIP_CALL_RTP_G711`, `SIP_DTMF2.cap`, multiple codec-specific SIP/RTP captures, and a SIP/TLS 1.3 + RTCP capture. citeturn0search0turn1search0

The repository also records a verified RTP-analysis example from Wireshark's documentation: stream SSRC `932629361`, frames 624–626, G.711 PCMA payload type 8, with the documented packet timestamps and a calculated second-step interarrival jitter of approximately **1.029 ms**. citeturn1search5

These are **public research/sample captures, not customer or employer production data**. No claim is made that they represent Sajid's employment history or a live telecom environment.

## What is executable

- Python SIP parser for sanitized log fixtures.
- SQL evidence tables and investigation queries.
- Evidence-backed capture inventory.
- Packet-level RTP measurement example with reproducible calculations.
- Wireshark filters for SIP/RTP/DNS/TCP investigation.
- API health checks through Postman.
- JIRA/Zendesk triage blueprint.
- Incident runbook connecting symptoms to evidence and escalation.

## Data

- `data/public_capture_inventory.csv` — public Wireshark capture catalog used by the project.
- `data/rtp_measurements.csv` — packet-level values reproduced from the documented Wireshark RTP statistics example.
- `data/source_notes.md` — provenance and interpretation notes.
- `sip-parser/sample_sip.log` — small parser fixture only; it is not used for dashboard metrics.

## How the evidence pipeline is intended to work

```
PCAP
  -> Wireshark / TShark
  -> SIP + SDP + RTP fields
  -> structured evidence
  -> SQL
  -> incident classification
  -> support/RCA output
```

Wireshark's VoIP analysis exposes call timing, SIP information and RTP stream details; its RTP analysis reports packet ordering and jitter-related information. citeturn4search7turn0search2

## Quick start

### Parser fixture
```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log
```

### Evidence SQL
```bash
sqlite3 voip.db < sql/schema.sql
sqlite3 voip.db < sql/voip_metrics.sql
```

### Postman
Import `postman/voip-api-health.postman_collection.json` into Postman and run the collection. It uses public HTTP test endpoints and does not require credentials.

## Important integrity rule

Do not present the public capture evidence as customer traffic, live production telemetry, or employment results. The dashboard deliberately labels the provenance of each evidence record.

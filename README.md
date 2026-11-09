# VoIP Support Automation Toolkit

A support-engineering toolkit for investigating SIP/VoIP incidents using packet evidence, structured analysis, SQL, API checks, and ticket-triage logic.

**Stack:** Python · SQL (SQLite) · Wireshark/TShark · Postman

---

## Purpose

I built this project to practice the workflow a support engineer follows on a VoIP incident: start from packet-level evidence, turn it into structured data, query it, classify the issue, and write up a root cause with a clear escalation path.

## Data and provenance

All evidence in this repository comes from **public Wireshark sample captures** and documented packet-level observations. It is **not** customer, employer, or production data, and nothing here should be read as live telecom telemetry.

- Public SIP/RTP sample captures from the Wireshark sample captures library (for example SIP call with G.711 RTP, DTMF, and SIP over TLS)
- One RTP analysis example reproduced from Wireshark's documentation: stream SSRC `932629361`, frames 624–626, G.711 PCMA (payload type 8), with a calculated interarrival jitter of approximately **1.029 ms**
- Each evidence record is labeled with its source

## What's included

| Area | Folder | What it does |
|---|---|---|
| SIP log parsing | `sip-parser/` | Python parser for sanitized SIP log fixtures |
| SQL analysis | `sql/`, `python-sql/` | Schema and investigation queries over structured evidence |
| Packet analysis | `wireshark/` | Display filters for SIP, RTP, DNS, and TCP investigation |
| API health checks | `postman/` | Postman collection using public HTTP test endpoints (no credentials needed) |
| Evidence data | `data/` | Capture inventory, RTP measurements, and source notes |
| Runbook and triage | `docs/` | Incident runbook, worked incidents, API/SMS troubleshooting, and a Jira/Zendesk triage blueprint |
| Validation | `validate_project.py` | Checks that project files and data are consistent |

## How the evidence pipeline works

```
PCAP
  → Wireshark / TShark
  → SIP + SDP + RTP fields
  → structured evidence (CSV / SQLite)
  → SQL investigation queries
  → incident classification
  → support / RCA write-up
```

## Quick start

**Parse the sample SIP log**

```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log
```

**Load the evidence tables and run the queries**

```bash
sqlite3 voip.db < sql/schema.sql
sqlite3 voip.db < sql/voip_metrics.sql
```

**Run the API health checks**

Import `postman/voip-api-health.postman_collection.json` into Postman and run the collection.

## Data files

- `data/public_capture_inventory.csv`: catalog of the public Wireshark captures used
- `data/rtp_measurements.csv`: packet-level values from the documented RTP example
- `data/source_notes.md`: provenance and interpretation notes
- `sip-parser/sample_sip.log`: small parser fixture (not used for any metrics)

<!--
Add once you have them:

## Screenshot
![RTP stream analysis](docs/rtp-analysis.png)

## Worked example: one-way audio
- Symptom: [what the caller reported]
- What I checked: [SIP/SDP negotiation, RTP direction, Wireshark filter used]
- What the evidence showed: [finding]
- Likely cause and next step: [conclusion and escalation]
-->


## Visual workflow and reproducible demo

- [VoIP investigation workflow diagram](docs/voip-investigation-workflow.svg)
- [Reproducible SIP parser demo](docs/reproducible-demo.md) — run commands, interpret the fixture output, and prepare an evidence-led support handoff.

## Run automated tests

The parser uses only the Python standard library.

```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log --json sip-parser/report.json
python3 -m unittest discover -s tests -v
python3 validate_project.py
```

The parser output classifies the synthetic fixture events and can write a JSON report. The tests cover the known fixture scenarios, malformed lines, and the distinction between a SIP 401 digest challenge and a confirmed registration failure.

## Worked incident investigations

See [docs/worked-incidents.md](docs/worked-incidents.md) for three walkthroughs:
- SIP 403 registration rejection
- One-way audio reported after call answer
- SIP 401 digest challenge followed by an accepted registration

Each case separates what the fixture actually proves from the additional evidence an engineer must collect before declaring a root cause.

## REST API and SMS troubleshooting

See [docs/api-sms-troubleshooting.md](docs/api-sms-troubleshooting.md) for HTTP/API triage, safe retry guidance, SMS lifecycle interpretation, delivery callback checks, and simulated support cases. The guide distinguishes an API request being accepted from a message being delivered.

## Integrity note

This is a learning and portfolio project. Public sample captures are not presented as customer traffic, production telemetry, or work results.

## Author

**Sajid Manzoor**, Technical Support Engineer
[LinkedIn](https://www.linkedin.com/in/sajid-manzoor-730zz)

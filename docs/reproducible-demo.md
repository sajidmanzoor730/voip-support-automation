# Reproducible SIP Parser Demo

This walkthrough runs the repository's existing parser against its sanitized fixture and explains the checked-in sample output. It is a reproducible learning exercise, not a customer incident.

## 1. Run the parser

From the repository root:

```bash
python3 sip-parser/parse_sip_log.py sip-parser/sample_sip.log --json sip-parser/report.json
```

The parser reads the fixture, groups events by Call-ID, and writes a JSON report. To inspect it:

```bash
python3 -m json.tool sip-parser/report.json
```

## 2. What the checked-in sample report contains

The committed reference output in `sip-parser/sample_output.json` records:

| Measure | Reference result |
|---|---:|
| Parsed events | 17 |
| Grouped call / registration IDs | 4 |
| Fixture groups flagged with one-way-audio symptom | 1 |
| Fixture groups containing repeated SIP 403 responses | 1 |

These are counts from the supplied synthetic fixture, not service reliability metrics.

## 3. Interpret the signals carefully

- `demo-reg-001`: REGISTER → 401 → REGISTER. A 401 challenge is part of digest authentication and is not, by itself, proof of failure.
- `demo-reg-002`: repeated 403 responses. Treat this as an authorization/policy investigation. The fixture does not reveal the registrar's underlying policy decision.
- `demo-call-1002`: the fixture includes a one-way-audio symptom flag. It does not include sufficient SDP and bidirectional RTP evidence to identify NAT, firewall, endpoint, or media-relay root cause.
- `demo-call-1001`: a basic INVITE / provisional response / 200 / RTP / BYE sequence.

## 4. Run quality checks

```bash
python3 -m unittest discover -s tests -v
python3 validate_project.py
```

## 5. Extend the investigation with packet evidence

Open a public sample capture in Wireshark and start with:

```text
sip
rtp
dns
tcp.analysis.retransmission
```

For a reported one-way-audio issue, inspect the negotiated SDP connection addresses and ports, then inspect RTP streams in both directions. Do not conclude that NAT or firewall is responsible until the packet path and relevant network configuration support that conclusion.

## 6. Support handoff template

- **Impact:** who/what is affected and how broadly
- **Time window:** timestamp and timezone
- **Identifiers:** Call-ID / request ID (sanitized)
- **Observed:** exact SIP sequence, response, packet direction, or API status
- **Checked:** filters, logs, endpoint, and reproduction steps
- **Confirmed:** facts directly supported by evidence
- **Unknown:** missing SDP, RTP, server, carrier, or endpoint evidence
- **Next action:** precise additional check or escalation owner

Never include real credentials, authorization headers, private customer traffic, or personal phone numbers in this repository.

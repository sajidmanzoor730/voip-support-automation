# VoIP Incident Runbook

## 1. Establish the symptom

Ask for:
- exact timestamp and timezone
- affected call ID / ticket ID
- caller/callee direction
- whether the issue is repeatable
- whether the problem is no audio, one-way audio, call drop, registration, or setup failure

## 2. Separate signaling from media

SIP establishes and controls the session. RTP normally carries the media.

- If SIP never reaches 200 OK, investigate signaling/authentication/routing.
- If SIP reaches 200 OK but audio fails, inspect SDP and RTP.
- If only one direction has RTP, investigate NAT/firewall/routing/media address issues.

## 3. Capture evidence

Useful filters:
- `sip`
- `sip.Method == "INVITE"`
- `sip.Status-Code >= 400`
- `rtp`
- `tcp.analysis.retransmission`
- `dns`

Do not conclude from one packet. Correlate packet evidence with application/server logs.

## 4. API integration checks

For REST integrations:
1. reproduce with Postman
2. compare request URL, method, headers, auth, and body
3. distinguish 401 (authentication) from 403 (authorization)
4. check response body and server correlation ID
5. compare client and server timestamps

## 5. Escalation package

A useful escalation should contain:
- concise symptom
- exact timestamp
- reproducible steps
- affected call IDs
- relevant SIP response codes
- Wireshark findings
- application/log findings
- suspected component
- actions already attempted

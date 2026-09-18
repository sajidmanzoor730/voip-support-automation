# JIRA + Zendesk Automation Blueprint

This document is an implementation design, not a claim that this portfolio has access to a production JIRA or Zendesk instance.

## Trigger

When a new support ticket contains:
- SIP / VoIP / RTP / one-way audio / registration / call-drop keywords, or
- an attached SIP trace / packet capture,

route it to the VoIP triage workflow.

## Triage fields

Create structured fields:
- Call ID
- SIP method
- SIP response code
- Registration status
- Codec
- RTP observed: yes/no
- Packet loss %
- Jitter ms
- Customer impact
- Reproduction status
- Suspected layer: endpoint / network / SIP server / media / integration

## Automation logic

1. Detect category from ticket text.
2. Request missing Call ID and timestamp if absent.
3. Add the relevant Wireshark filter to the internal investigation note.
4. Run the safe log parser against sanitized logs when available.
5. If SIP 5xx repeats, route to platform/server queue.
6. If RTP is missing in one direction, route to network/media queue with capture evidence.
7. If API returns 4xx, validate authentication/authorization and request payload before escalating.
8. Add a standardized RCA template before closure.

## Example JIRA transition

`New -> Triage -> Investigating -> Waiting for Customer -> Engineering Escalation -> Resolved`

## RCA template

**Impact:**  
**Start/end time:**  
**Call IDs:**  
**Evidence reviewed:**  
**Observed SIP sequence:**  
**Network findings:**  
**Root cause:**  
**Corrective action:**  
**Preventive action:**  
**Customer communication:**  

## Privacy

Never paste real customer phone numbers, authentication tokens, full IP inventories, or production packet captures into a public repository.

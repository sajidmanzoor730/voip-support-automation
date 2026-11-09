# Worked Incident Investigations (Synthetic Fixtures)

These walkthroughs are deliberately based on the repository's synthetic log fixture. They demonstrate an investigation method; they are not customer incidents, production findings, or proof of a live network root cause.

## Case 1 — Registration rejected with SIP 403

**Symptom:** A test endpoint attempts REGISTER and receives repeated 403 responses.

**Evidence in fixture:** `demo-reg-002` has two 403 events after REGISTER attempts.

**Interpretation:** A 403 indicates the request was understood but refused. Unlike a 401 digest challenge, repeating the same request is unlikely to resolve an authorization or policy rejection.

**Checks to perform next:**
1. Confirm the account, endpoint identity and registrar/tenant assignment.
2. Verify whether the source IP, domain or device is allowed by policy.
3. Check registrar logs for the specific authorization rule that rejected the request.
4. Retest once the policy or identity issue is corrected.

**Escalation package:** Timestamp and timezone, Call-ID, source/destination addresses, full SIP response headers, sanitized REGISTER/403 exchange, and the result of the authorization checks.

**Conclusion:** The fixture supports classifying this as a registration-authorization investigation. It does not identify the actual policy rule; registrar-side evidence is required.

## Case 2 — One-way audio reported after call answer

**Symptom:** The test endpoint reports one-way audio after the call reaches the answered state.

**Evidence in fixture:** `demo-call-1002` contains INVITE, 180, 200, an RTP event with a one-way-audio report, and BYE.

**Interpretation:** The fixture confirms that signaling reached 200 OK and that a test endpoint reported a media symptom. It does not contain SDP bodies or packet-level RTP direction, so it cannot prove a NAT or firewall root cause.

**Checks to perform next:**
1. Compare the SDP offer and answer: connection address, media port, direction attributes and negotiated codec.
2. In Wireshark, inspect the RTP stream in both directions using `rtp` and the stream analysis tools.
3. Compare advertised SDP addresses with the actual packet source/destination addresses.
4. Review firewall/NAT mappings and media relay logs for the call time.
5. Confirm whether the missing direction is absent, blocked, or sent to an incorrect address/port.

**Escalation package:** Call-ID, timestamp/timezone, sanitized INVITE/200 OK SDP, RTP stream endpoints, packet counts in each direction, firewall/relay observations, and reproduction steps.

**Conclusion:** The fixture supports a media-path investigation only. A root cause must not be claimed until SDP and bidirectional RTP evidence are inspected.

## Case 3 — SIP 401 challenge during registration

**Symptom:** A REGISTER transaction receives 401 before a subsequent REGISTER is accepted.

**Evidence in fixture:** `demo-reg-001` records a 401 challenge followed by an authenticated REGISTER accepted event.

**Interpretation:** A 401 can be a normal SIP digest-authentication challenge. It is not automatically a failed registration. The subsequent accepted event in the fixture indicates the test sequence continued.

**Checks to perform next if registration still fails:** Verify that the client retries with the challenge nonce/realm and correct digest response; compare the Authorization header and registrar response without exposing credentials.

**Conclusion:** Do not classify a single 401 as an incident without checking whether the authenticated retry succeeds.

# REST API and SMS Troubleshooting (Twilio-Style Practice)

This guide is interview-practice material, not a record of customer incidents. Examples use placeholders and simulated outcomes. Never commit real Account SIDs, Auth Tokens, phone numbers, message bodies, or customer data.

## 1. REST API investigation flow

1. Capture the request method, endpoint, timestamp with timezone, and sanitized parameters.
2. Record HTTP status, response body, provider error code, and request/message identifier when present.
3. Confirm the request reaches the intended account/project and environment.
4. Separate authentication from authorization:
   - 401: verify authentication method and credentials. Never ask for an Auth Token in a ticket.
   - 403: check account state, permissions, sender eligibility, and regional/compliance restrictions.
5. Validate the request:
   - 400: inspect required parameters, formatting, and provider error details.
   - Confirm phone numbers use E.164 formatting where required.
6. For 429, inspect rate/concurrency limits. Use bounded backoff with jitter; avoid retry storms.
7. For 5xx or network timeouts, check provider status, request IDs, latency, and whether the operation may already have been accepted.
8. Reproduce with a minimal request in a safe test environment.

### Safe retry rule

Do not blindly retry a message-create request after a client timeout. The provider may have accepted the first request even if the response was lost. First search message logs using the time, destination, and available identifiers. Use idempotency only where the specific API supports it; do not assume every endpoint does.

### Sanitized cURL shape

This is a shape example only. Replace placeholders locally and never commit credentials.

~~~bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/ACCOUNT_SID/Messages.json" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15557654321" \
  --data-urlencode "Body=Test message" \
  -u "ACCOUNT_SID:AUTH_TOKEN"
~~~

Use environment variables or a secret manager for credentials in actual testing. These are placeholders, not working credentials.

## 2. Understand the outbound SMS lifecycle

Common outbound Message resource statuses:

| Status | Support interpretation |
|---|---|
| accepted | A Messaging Service accepted the request and is selecting/assigning a sender. |
| queued | The message is waiting to be sent. |
| sending | Dispatch is in progress. |
| sent | The upstream carrier accepted the message; this is not confirmed handset delivery. |
| delivered | A delivery confirmation was received from the carrier and, where available, the handset. |
| undelivered | A delivery receipt reported non-delivery; inspect the associated error details. |
| failed | The message could not be sent/processed; inspect the message record. |

Initial state and callback sequence can vary depending on whether a Messaging Service is used. Do not assume every message produces every intermediate callback.

## 3. SMS troubleshooting checklist

### API request accepted, but recipient says no SMS arrived

- Locate the Message resource using its Message SID where available.
- Check latest status and error details if status is failed or undelivered.
- Confirm destination number and expected format.
- Confirm sender validity and eligibility for the destination country/network.
- Check opt-out/consent state, sender registration, content restrictions, and carrier filtering where applicable.
- Compare submission time with status callback timestamps.
- Determine whether the issue affects one destination, one carrier, one sender, or all traffic.
- Check the provider status page before attributing a broad incident to the integration.

### Message remains queued

- Check sender throughput and queue depth.
- Check whether the sender or Messaging Service is configured and eligible.
- Compare queue delay with normal behavior and current provider status.
- Avoid increasing concurrency blindly; that can worsen throttling or queue pressure.

### Message is sent but not delivered

- Explain that sent means the upstream carrier accepted it, not necessarily that the handset displayed it.
- Wait for a delivery receipt within the expected carrier window and inspect final status.
- If it becomes undelivered, use error details and carrier context as the next evidence.
- If no final receipt arrives, record that delivery confirmation is unavailable rather than claiming success.

## 4. Status callback handling

- Store Message SID, status, error code (when present), and callback timestamp.
- Expect callback parameters to evolve; tolerate additional fields.
- Validate callback signatures using the provider's supported SDK/helper rather than custom cryptography.
- Make the handler idempotent because callbacks may be retried or arrive more than once.
- Do not assume callback arrival order is a perfect substitute for reading the current Message resource.
- Return a successful HTTP response promptly and process heavier work asynchronously.

## 5. Simulated support scenarios

### Scenario A — API returns 401

**Customer report:** "Our application cannot create outbound messages."

**Evidence:** HTTP status/body, request timestamp and timezone, account/project identifier (not a secret), endpoint, and sanitized request headers.

**Investigation:** Confirm the correct account identifier and authentication method. Check whether credentials were rotated, copied with whitespace, or loaded from the expected environment. Never request the Auth Token itself.

**Next action:** Have the customer update the secret through their secure configuration process if needed, then retest. Escalate with request ID and sanitized response if valid authentication still fails.

### Scenario B — Message API request succeeds, but message is undelivered

**Customer report:** "The API call succeeded, but the user did not receive the SMS."

**Evidence:** Message SID, destination country/carrier if known, timestamp, sender or Messaging Service, final status, and error code.

**Investigation:** A successful create response confirms the message resource was created; it does not prove final delivery. Inspect the Message resource and status callback. If status is undelivered, use error details and carrier context to narrow the cause.

**Next action:** Verify number formatting, sender eligibility, consent/opt-out state, and content restrictions. If evidence points to a carrier-side issue, escalate with Message SID, timestamps, error code, and sanitized reproduction.

### Scenario C — Intermittent HTTP 429 during message bursts

**Customer report:** "A burst of API requests sometimes receives Too Many Requests."

**Evidence:** Request timestamps, HTTP status/provider error code, concurrency pattern, request rate, and whether the application retries.

**Investigation:** Compare bursts with concurrency/rate limits and inspect whether retries amplify traffic. Check queue throughput separately from REST API request concurrency.

**Next action:** Implement bounded exponential backoff with jitter, cap concurrent requests, and re-test gradually rather than replaying the entire burst.

## 6. Escalation template

Include:
- Customer impact and affected scope
- Start/end time with timezone
- Environment and API endpoint
- Sanitized request/response and HTTP status
- Provider request ID and Message SID, if available
- Message status and error code
- Reproduction steps and frequency
- Checks completed and their results
- Expected behavior versus actual behavior

Remove credentials, authorization headers, full phone numbers, and message content unless specifically required through an approved secure process.

## References

- Twilio Message resource and status definitions: https://www.twilio.com/docs/messaging/api/message-resource
- Outbound message status callbacks: https://www.twilio.com/docs/messaging/guides/outbound-message-status-in-status-callbacks
- Troubleshooting undelivered SMS: https://help.twilio.com/articles/223181868-Troubleshooting-Undelivered-Twilio-SMS-Messages
- Rate limits and message queues: https://help.twilio.com/articles/115002943027

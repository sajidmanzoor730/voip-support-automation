# Wireshark VoIP Filter Library

These are reusable Wireshark display filters. Apply them to a capture containing SIP/RTP traffic.

## SIP

```text
sip
sip.Method == "INVITE"
sip.Method == "REGISTER"
sip.Method == "BYE"
sip.Status-Code >= 400
sip.Status-Code == 401
sip.Status-Code == 403
sip.Status-Code == 404
sip.Status-Code >= 500
```

## RTP / RTCP

```text
rtp
rtcp
rtp.marker == 1
rtp.p_type == 0
rtp.p_type == 8
```

Payload type 0 is commonly G.711 PCMU and 8 is commonly G.711 PCMA, but always confirm the negotiated SDP because payload mappings can vary.

## TCP / UDP

```text
udp.port == 5060
tcp.port == 5060
udp.port == 5060 || tcp.port == 5060
tcp.analysis.retransmission
tcp.analysis.lost_segment
```

## DNS / TLS / connectivity

```text
dns
dns.flags.response == 0
tls
icmp
```

## Example investigation

For a suspected SIP registration problem:

```text
sip.Method == "REGISTER"
```

Then inspect the response sequence. Repeated 401 responses can be normal during digest authentication; repeated 403 responses indicate a different authorization problem. Always correlate the SIP response with the endpoint configuration and server logs.

For one-way audio, inspect SIP/SDP first, then RTP:

```text
sip && sdp
rtp
```

Look for advertised media addresses/ports, NAT changes, packet direction, loss, and whether RTP exists in both directions.

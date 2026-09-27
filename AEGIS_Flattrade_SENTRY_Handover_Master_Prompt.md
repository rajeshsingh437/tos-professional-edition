AEGIS MASTER HANDOVER PROMPT
OpenAlgo Professional Edition — Flattrade + SENTRY Relay
Baseline date: 11-Aug-2026

ROLE
You are taking over engineering work on the OpenAlgo Professional Edition Flattrade integration. Treat the following as the protected baseline. Do not rebuild working components from scratch and do not make unrelated changes.

PROJECT BASELINE
1. Flattrade authentication has been moved behind the SENTRY relay.
2. OpenAlgo's Flattrade auth module calls SENTRY /complete_login with:
   - FLATTRADE_RELAY_URL
   - RELAY_SHARED_SECRET
3. SENTRY performs the Flattrade token exchange using server-side:
   - BROKER_API_KEY
   - BROKER_API_SECRET
4. The OpenAlgo generic broker interface remains compatible with:
   authenticate_broker(code, password=None, totp_code=None)
5. authenticate_broker_oauth(code) remains available.
6. The Flattrade callback configuration was restored to the callback path and login subsequently worked.

VERIFIED WORKING — DO NOT BREAK
- Flattrade login: WORKING
- SENTRY relay connectivity: WORKING
- Live market data: WORKING
- MCX quote/chart data: WORKING
- Master data: WORKING
- Dashboard market-data flow: WORKING

CURRENT UNRESOLVED ISSUE
Order test:
- Exchange: MCX
- Symbol: CRUDEOIL19AUG26FUT
- Side: BUY
- Quantity: 100
- Product: MIS
- Order type: MARKET

Observed:
- OpenAlgo returned status=success
- orderid was null
- No corresponding order appeared in Order Book
- No position appeared
- Terminal showed an httpx/httpcore traceback, but the final/root exception line was not captured.

Do NOT conclude that insufficient funds caused the failure merely because the real broker balance was low. That is only a hypothesis. First establish whether the request reached Flattrade and what exact response Flattrade returned.

SECURITY — SENTRY IS A HARD SECURITY BOUNDARY
Never:
- expose BROKER_API_KEY
- expose BROKER_API_SECRET
- expose RELAY_SHARED_SECRET
- place secrets in frontend/browser code
- commit live secrets or .env files
- log access tokens
- log Authorization headers
- log security hashes
- log complete credential-bearing request payloads
- send secrets into prompts, tickets or screenshots
- bypass SENTRY for convenience
- weaken the relay Authorization: Bearer <RELAY_SHARED_SECRET> check

Do not restore direct desktop-to-Flattrade credential exchange without an explicitly approved architecture decision.

SENTRY credentials remain server-side. The actual shared secret must never be included in documentation or code supplied to AEGIS; use placeholders.

LOGGING RULE
Sensitive debugging that existed during investigation must be treated as temporary. Production logging must be redacted. Safe diagnostics may include timestamp, endpoint, HTTP status, correlation ID and non-sensitive broker error codes/messages.

ENGINEERING RULES
1. Preserve the current working authentication and market-data paths.
2. Back up working files/configuration before changes.
3. Make one logical change at a time.
4. Test login after authentication changes.
5. Test market data before order tests.
6. Do not change SENTRY and OpenAlgo authentication simultaneously.
7. Preserve OpenAlgo's authenticate_broker contract.
8. Do not modify unrelated broker plugins.
9. Do not treat __pycache__ output as source code.
10. Never paste raw search output into PowerShell as a command.
11. Keep the order-placement issue isolated until the broker response contract is known.
12. Treat success + null orderid as an abnormal/unknown submission state, not a completed order.
13. Preserve broker rejection details so the UI can distinguish rejected, failed, timed-out and unknown-submission states.

NEXT DIAGNOSTIC STEP
Before changing order code, obtain the exact Flattrade API contract and/or server-side evidence.

Ask Flattrade support:
1. Is API trading enabled for this account?
2. Is MCX/Commodity API order placement separately enabled?
3. What is the current MCX futures place-order endpoint?
4. What is the exact request format?
5. What are the exact exchange, symbol, product and order-type values?
6. What does a successful order response look like?
7. What does an insufficient-margin/funds rejection look like?
8. Can the API ever return status=success with orderid=null?
9. Did the test request around 19:01:50 IST on 11-Aug-2026 reach the Flattrade order server?
10. If yes, what exact response/rejection code was returned?
11. Are there IP, firewall, TLS or gateway restrictions?
12. Provide current MCX place-order, success-response and rejection-response examples.

RECOMMENDED FIX/TEST SEQUENCE
A. Capture the actual adapter request with secrets redacted.
B. Capture HTTP status and response body.
C. Compare against the current Flattrade documentation/support response.
D. Change only the confirmed mismatch.
E. Verify broker rejection handling.
F. Verify a genuine accepted order receives a non-null order ID.
G. Verify Order Book.
H. Verify resulting position if filled.
I. Only then declare Flattrade order routing complete.

AEGIS DELIVERY STANDARD
For any source-code modification:
- provide the complete replacement file as a downloadable file;
- do not require manual code merging;
- provide a separate concise change/handover prompt;
- if a file is too large, split it into clearly numbered complete parts;
- never include live secrets;
- state exactly which files changed;
- state what was tested and what remains unverified.

DO NOT BREAK CHECKLIST
Before accepting any future Flattrade change, verify:
[ ] Login still works
[ ] SENTRY relay authentication still works
[ ] Market data still works
[ ] MCX market data still works
[ ] Master data still works
[ ] No secrets are exposed in logs/UI/source
[ ] authenticate_broker contract still works
[ ] Order errors are not falsely reported as success
[ ] A non-null broker order ID is required before declaring an order successfully submitted

CURRENT STATUS
Authentication: PASS
Market data: PASS
MCX market data: PASS
Master data: PASS
SENTRY relay: PASS
Order placement: UNRESOLVED
Order-ID handling: UNRESOLVED
Broker rejection response: NOT YET CONFIRMED

Treat this prompt as a handover baseline, not as permission to redesign the architecture.

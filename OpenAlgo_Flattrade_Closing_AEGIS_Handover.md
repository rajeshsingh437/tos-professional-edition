# OpenAlgo — Flattrade Plugin Closing & AEGIS Handover

*Closing baseline after SENTRY relay integration and Flattrade testing — 11 Aug 2026*

## Purpose

This is the closing handover baseline for the Flattrade integration work completed in this phase. It is intended to guide future AEGIS engineering without disturbing working authentication and market-data paths.

This document records only behavior evidenced during this work. It does not claim that order routing has been fixed.

## Completed / Evidenced Changes

• Flattrade authentication was changed so the local OpenAlgo Flattrade auth module sends the OAuth request code to the SENTRY relay rather than exchanging the request code directly with Flattrade.
• The auth module uses FLATTRADE_RELAY_URL and RELAY_SHARED_SECRET to call SENTRY /complete_login.
• The generic OpenAlgo authenticate_broker(code, password=None, totp_code=None) interface was retained.
• authenticate_broker_oauth(code) was retained as an OAuth-compatible alias.
• SENTRY performs the Flattrade token exchange using BROKER_API_KEY and BROKER_API_SECRET on the relay side.
• The relay provides authenticated endpoints including /complete_login, /login_status, /positions, /orders, /trades, /limits and /holdings.
• The Flattrade callback configuration was ultimately restored to the callback path; login then succeeded.

## Verified Working State

LOGIN: WORKING
LIVE MARKET DATA: WORKING
MCX QUOTES/CHART: WORKING
MASTER DATA: WORKING
DASHBOARD DATA: WORKING
SENTRY RELAY CONNECTIVITY: WORKING

Flattrade had no holdings during testing; that is not itself an error.

Treat authentication and market-data connectivity as the stable baseline while debugging orders.

## Current Unresolved Order Issue

Test order:
Exchange: MCX
Symbol: CRUDEOIL19AUG26FUT
Side: BUY
Quantity: 100
Product: MIS
Order type: MARKET

OpenAlgo returned success with orderid = null. No corresponding order appeared in Order Book and no position appeared. The terminal also showed an httpx/httpcore traceback, but the final/root exception message was not visible.

Do NOT currently conclude that Flattrade rejected the order because of insufficient funds. Low real balance makes that plausible, but it is not proven. First determine whether Flattrade received the request and what exact response it returned.

## Flattrade Office-Hours Questions

Ask support:
1. Is API trading enabled for this account?
2. Is MCX/Commodity API order placement separately enabled?
3. What is the current MCX futures place-order endpoint and exact request format?
4. What are the exact accepted values for exchange, symbol, product/MIS and market order type?
5. What does a successful order-placement response look like?
6. What does an insufficient-margin/funds rejection response look like?
7. Can the API ever return status=success with orderid=null?
8. Can support check server logs for the test around 19:01:50 IST on 11-Aug-2026?
9. Did that request reach the Flattrade order server?
10. If yes, what exact response/rejection code was returned?
11. Are there IP-whitelisting, firewall, TLS or gateway requirements for order placement?
12. Please provide the current MCX place-order example, successful response example and rejected response example.

## SENTRY Security — DO NOT BREAK

SENTRY is a security boundary, not merely a convenience proxy.

AEGIS MUST:
• Keep BROKER_API_KEY and BROKER_API_SECRET server-side.
• Keep RELAY_SHARED_SECRET server-side.
• Never place secrets in frontend/client code, source control, screenshots, prompts or support tickets.
• Never log API secrets, relay secrets, access tokens, Authorization headers or security hashes.
• Preserve the relay Authorization: Bearer <RELAY_SHARED_SECRET> check.
• Do not bypass SENTRY and restore direct desktop-to-Flattrade credential exchange without an explicitly approved architecture change.
• Do not weaken relay authentication to simplify testing.
• Never commit the SENTRY .env or other live credential files.
• Do not expose Flattrade access tokens to browser JavaScript.
• Preserve broker credential isolation.
• Treat the relay URL as infrastructure information, not as authorization.

## Logging / Debugging Guardrails

The relay previously used verbose token-exchange diagnostics. Before production hardening, AEGIS should sanitize or remove sensitive diagnostics.

Never log:
• BROKER_API_SECRET
• RELAY_SHARED_SECRET
• access_token
• Authorization headers
• security_hash
• complete request payloads containing secrets

Safe diagnostics can include timestamp, endpoint, HTTP status, correlation ID and non-sensitive error codes/messages. Temporary verbose debugging must be opt-in, redacted and removed after diagnosis.

## Configuration Baseline

OpenAlgo should use the relay configuration pattern:

FLATTRADE_RELAY_URL=<approved SENTRY relay URL>
RELAY_SHARED_SECRET=<existing SENTRY shared secret>

The real shared secret is intentionally NOT included here.

Do not change the callback/redirect configuration that currently produces successful login unless Flattrade explicitly instructs otherwise.

## AEGIS Engineering Guardrails

1. Back up the working Flattrade auth module and configuration before edits.
2. Make one logical change at a time.
3. After authentication changes, verify login before order tests.
4. After broker API changes, verify market data before order tests.
5. Do not change SENTRY and OpenAlgo authentication simultaneously.
6. Preserve the generic authenticate_broker contract.
7. Do not modify unrelated broker plugins while fixing Flattrade.
8. Do not treat __pycache__ output as source code.
9. Do not paste raw search output into PowerShell.
10. Keep the order issue isolated until the broker's exact response is known.
11. Explicitly handle missing/null order IDs; success + null orderid should not be treated as a normal completed order.
12. Preserve broker rejection/error details so the UI can distinguish rejected, failed, timeout and unknown-submission states.

## Terminal Incident Note

The large text containing broker paths, source lines and binary-looking __pycache__ data was search output that was accidentally entered into PowerShell. PowerShell then attempted to execute it and produced many parser errors.

Those parser errors do not prove that all listed Python files are broken.

Future rule: search output is for inspection, not execution. Run only the intended command.

## Recommended Next Test Sequence

A. Obtain the exact Flattrade order API request/response contract from support.
B. Capture the actual request generated by the adapter with secrets redacted.
C. Capture the HTTP status and response body.
D. Compare with Flattrade's current example.
E. Fix only the confirmed mismatch.
F. Test an intentional rejection if support confirms a safe test method.
G. Confirm a genuine accepted order returns a non-null broker order ID.
H. Confirm it appears in Order Book.
I. Confirm the resulting position if it fills.
J. Only then mark Flattrade order integration complete.

## Final Baseline

AUTHENTICATION: PASS
MARKET DATA: PASS
MCX MARKET DATA: PASS
MASTER DATA: PASS
SENTRY RELAY: PASS
ORDER PLACEMENT: UNRESOLVED
ORDER-ID HANDLING: UNRESOLVED
BROKER REJECTION RESPONSE: NOT YET CONFIRMED

AEGIS should preserve the working login and market-data path while isolating and fixing order placement.

No live credentials are included in this document.


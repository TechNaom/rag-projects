# API Rate Limits

Notedeck offers a REST API for Pro and Team accounts. This article explains the rate limits and how to handle them in your integration.

## What the limits are

Each API token is limited to:

- **120 requests per minute** on the Pro plan.
- **600 requests per minute** on the Team plan.

Limits are counted per token, not per account, so issuing separate tokens for separate services keeps one busy service from starving another.

## How to tell you hit a limit

When you exceed the limit, the API returns HTTP status **429 Too Many Requests**. The response includes these headers:

- `X-RateLimit-Limit` is your ceiling for the current window.
- `X-RateLimit-Remaining` is the requests left in the current window.
- `Retry-After` is how many seconds to wait before trying again.

## Handling limits gracefully

1. Read `X-RateLimit-Remaining` and slow down before you hit zero.
2. When you get a 429, wait the number of seconds in `Retry-After` before retrying. Do not retry immediately in a tight loop.
3. Use exponential backoff for repeated failures: wait 1s, then 2s, then 4s, and so on.
4. Batch related changes into a single request where the endpoint supports it, instead of one request per item.

If your integration legitimately needs a higher ceiling, contact support with your token's typical request pattern and we can discuss a custom limit on the Team plan.
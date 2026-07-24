---
id: ascent-rivals:eventun-operations
status: current
applicability: shared-development
---
# Running Eventun

Eventun does more than answer one request at a time. It shares a small database pool, calls other
services, runs scheduled work, records enough information to diagnose failures, and still needs to
shut down without abandoning accepted rewards. This chapter explains those operating rules.

It is a description of how the service behaves while running, not a deployment runbook. Exact
environment values and release procedures belong with the environment or deployment configuration
that owns them.

## Database And External Services

Eventun uses a PostgreSQL connection pool. A request borrows a connection only for the query,
batch, or transaction that needs it; it does not hold that connection while waiting for Steam,
AccelByte, Accountun, or another provider. This keeps a slow external service from unnecessarily
blocking unrelated database work.

A transaction groups database changes that must succeed together. External calls normally happen
after that transaction. When an external effect must follow an accepted change, Eventun records
durable intent and lets the appropriate worker or finalization path perform it. A temporary
provider failure therefore does not erase the domain outcome that Eventun already accepted.

Only `pgx.ErrNoRows` means a database record is absent. Scan, iteration, infrastructure, and
provider failures remain failures rather than being quietly reported as “not found.”

## What Eventun Records

Access records contain the method, final status, duration, request and response message counts,
protobuf wire sizes, and a sampled trace identity. They deliberately omit bodies, cookies,
authentication metadata, tokens, and player payloads.

Metrics and access logging wrap error sanitization and authorization. They therefore see the same
final status as the caller, including permission failures and internal errors that were converted
to a safe public response.

The deployed AccelByte environment currently advertises Zipkin ingestion, so Eventun uses the
OpenTelemetry Zipkin exporter. It can move to OTLP when the platform provides a supported OTLP
receiver. Structured logging defaults to `info`; `debug` is an explicit operational choice rather
than the normal production posture.

## Time And Resource Bounds

Every provider and server boundary has a finite default. If a caller supplies a shorter deadline,
the caller's deadline wins.

| Boundary | Current default |
|---|---|
| PostgreSQL pool | Maximum 8 and minimum 1 connection; 5-second connect/startup check; 15-minute idle lifetime; 1-hour maximum lifetime with up to 10 minutes jitter; 1-minute health checks |
| Ordinary generated and catalog calls | 30 seconds |
| Reward grants | 45 seconds |
| Steam calls | 15 seconds |
| Accountun settlement | 5 minutes |
| Otherwise-unbounded unary RPC | 6 minutes 30 seconds |
| Gateway HTTP | 5-second header, 2-minute read, 7-minute write, and 2-minute idle bounds |
| Metrics HTTP | 5-second header, 10-second read/write, and 1-minute idle bounds |
| Shutdown | Separate 10-second serving and reward-finalization phases inside one 20-second bound |

The point of these limits is not that every operation should take close to its allowance. They
prevent one unavailable dependency or forgotten deadline from consuming Eventun's resources
forever.

## Scheduled Work And Shutdown

Scheduled jobs run with bounded contexts just like requests. During shutdown, Eventun first stops
accepting new work. Serving and reward finalization then receive separate bounded phases inside one
20-second shutdown window.

The database pool stays available while reward finalization is running. It closes only after
finalization finishes or its part of the shutdown window expires. This ordering gives already
accepted rewards a chance to finish without allowing shutdown to wait indefinitely.

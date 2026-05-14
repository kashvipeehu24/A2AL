# US-DL-407 — Silver `customer_360` View

**From:** Agent1 (PM)
**To:** Agent2 (QA)
**Thread:** agent1-agent2-datalake
**Intent:** User story sign-off request

I've drafted US-DL-407 to build the Silver `customer_360` view. Could you review the acceptance criteria?

## Source

- Bronze tables: `customers`, `orders`, `sessions`, `support_tickets`

## Target

- Silver Delta table `silver.customer_360`
- SCD2 on profile attributes
- Grain: one row per `customer_id` per profile change

## Refresh

- Daily at 06:00 UTC
- SLO: 99.5% on-time

## Acceptance Criteria

- The `master_person_id` is resolved via the MDM service before merge.
- PII is masked except for entitled roles (column-level ACL).
- Data quality: zero nulls on `customer_id`; zero duplicate primary keys.
- Downstream contract: Gold marts consume only this view — no Bronze passthrough is permitted.
- The backfill path is documented and reproducible from Bronze alone.

## Metadata

- Priority: medium
- Sprint: 27
- Owner: Agent1 (DEV)
- Dependencies: US-DL-401 must be merged first (the clickstream Bronze story).

Could you provide sign-off when ready?

# US-DL-401 — Clickstream Ingest to Bronze

**From:** Agent1 (PM)
**To:** Agent2 (QA)
**Thread:** agent1-agent2-datalake
**Intent:** User story sign-off request

I've drafted US-DL-401 to ingest clickstream events into our Bronze tier. Could you review the acceptance criteria, with a particular focus on the schema-drift behavior?

## Source

- Kafka topic `clickstream.v3`
- Volume approximately 12 million events per day

## Target

- ADLS Gen2 at `abfss://bronze/clickstream/dt=YYYY-MM-DD/`
- Format: Delta
- Partitioned on `event_date`
- 90-day retention

## SLO

- Arrival lag less than 15 minutes at p99

## Acceptance Criteria

- Schema evolution auto-merge is enabled, but only for additive columns.
- Data quality check: row count delta vs upstream is within 1%.
- Failed batches are routed to a DLQ container — no silent drops are permitted.
- OpenLineage events are emitted per batch.
- The ETL is idempotent on replay, using hash-based deduplication on `event_id`.

## Metadata

- Priority: high
- Sprint: 26
- Owner: Agent1 (DEV)
- Dependencies: none

Could you provide sign-off when ready?

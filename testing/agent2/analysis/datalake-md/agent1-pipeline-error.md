# Incident — Pipeline Failure: `DL-bronze-clickstream-ingest`

**From:** Agent1 (DEV)
**To:** Agent2 (SRE)
**Thread:** agent1-agent2-datalake
**Intent:** Incident report
**Severity:** 2

The `DL-bronze-clickstream-ingest` pipeline has failed. We need triage support.

## Incident Identifiers

- Incident: `INC-DL-0517`
- Run ID: `2026-05-07T03:14:22Z-7f3a`
- Attempt: 3 of 3 (all retries exhausted)
- DAG: `bronze.clickstream_ingest`
- Failing node: `transform.clickstream_normalize`

## Error

- Error code: `SPARK-3033 / TASK_FAILED_AFTER_RETRIES`
- Exit: 137 (out-of-memory); executor lost; YARN container killed by node manager
- Stage 4.0, task 287 of 512; 4 reattempts
- Final attempt: OOM at 9.4 GB resident set size vs 8 GB requested

## Stack Trace (top frames)

```
org.apache.spark.SparkException: Job aborted due to stage failure
  at DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2454)
  -> ExecutorLostFailure (executor 17 exited; reason: Container killed by YARN for exceeding memory limits)
Caused by: java.lang.OutOfMemoryError: Java heap space
  at o.a.s.sql.execution.aggregate.HashAggregateExec.doExecute(HashAggregateExec.scala:152)
  at o.a.s.sql.execution.exchange.ShuffleExchangeExec.doExecute(ShuffleExchangeExec.scala:113)
  at o.a.s.sql.catalyst.expressions.codegen.GenerateUnsafeProjection.create(GenerateUnsafeProjection.scala:412)
```

## Context

- Kafka `clickstream.v3` lag is 14 million events (normal is approximately 2 million) — upstream backlog burst.
- Shuffle spill is at 187 GB of 200 GB on node-local SSD; near disk-pressure eviction.
- Suspected cardinality explosion: the `user_agent` column has 4.1 million unique values vs a 380,000 baseline (a 10.8× increase).
- This correlates with a schema change to `clickstream.v3.user_agent_raw` deployed on 2026-05-06 at 21:40 UTC.
- DLQ status: zero events written — the failure occurred pre-write, so there is no partial state.
- SLA: breached. Arrival lag is 47 minutes vs the 15-minute p99 target.

## Triage Requested — Proposed Mitigations

We need a triage call to confirm the path forward. The proposed mitigations are:

- **Short-term:** Increase executor memory from 8 GB to 16 GB; raise `shuffle.partitions` from 512 to 2048.
- **Short-term:** Hash `user_agent` into 256 buckets at parse time, before the `groupBy` (salting).
- **Medium-term:** Roll back the `clickstream.v3.user_agent_raw` schema change pending root-cause analysis.
- **Long-term:** Add a cardinality monitor on hot `groupBy` keys; alert at 5× baseline.

## Ownership

- RCA owner: Agent1 (DEV); due 2026-05-09
- Restart status: blocked pending the memory bump and schema decision

Please acknowledge and let me know your triage decisions.

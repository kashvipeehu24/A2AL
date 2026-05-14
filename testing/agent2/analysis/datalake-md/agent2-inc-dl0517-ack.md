# INC-DL-0517 — Incident Acknowledgement and Triage Decisions

**From:** Agent2 (SRE)
**To:** Agent1 (DEV)
**Thread:** agent1-agent2-datalake
**Intent:** Incident response
**Severity:** 2
**In reply to:** INC-DL-0517

Acknowledged. The sev-2 is logged and the SLA breach is noted (47 minutes vs the 15-minute p99 target).

## Triage Call

Scheduled for 2026-05-07 at 16:00 UTC. The bridge details have been sent separately.

## DLQ Verification

The DLQ has been verified clean (zero events). No replay is required.

## Mitigation Decisions

- **Executor memory 8 GB → 16 GB:** Approved. Apply now.
- **`shuffle.partitions` 512 → 2048:** Approved. Pair with the memory bump.
- **`user_agent` salting (256 buckets pre-`groupBy`):** Approved. This is the safest unblock path.
- **Schema rollback of `clickstream.v3.user_agent_raw`:** Deferred pending root-cause analysis. The salting alone unblocks us without losing the schema change.
- **Cardinality monitor (alert at 5× baseline):** Approved as a long-term action. File this as `US-DL-0518` and assign to Agent1 (DEV).

## Restart

Cleared after the memory bump and salting are deployed. Before prod cutover:

- Run a 1-hour shadow run on the dev cluster.
- Verify that executor heap headroom is greater than 30% at peak.
- Verify that shuffle spill is below 60% of local SSD capacity.

## Root-Cause Analysis

- Due: 2026-05-09
- Owner: Agent1 (DEV)
- Use the blameless post-mortem template.

The leading hypothesis is a cardinality explosion driven by the `user_agent_raw` schema change deployed at 21:40 UTC on 2026-05-06; the correlation is a 10.8× baseline increase. The RCA should also include:

- The pre-deploy cardinality-check gap.
- The YARN OOM-killer signal flow.
- Backlog-burst amplification effects.

## Upstream Coordination

- Notify the Kafka `clickstream.v3` owner of the 14-million-event lag burn-down ETA after restart.
- If customer-visible lag persists more than 2 hours post-restart, escalate to the PMO.

Acknowledged.

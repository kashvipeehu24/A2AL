# A2AL Examples

Worked examples for A2AL/0.3.0, organized by profile. All JSON examples in this directory pass `validator/python/validate.py` against `specs/A2A-Core.md` and the relevant profile rules.

## Per-Profile Examples

### `project-coord/1.0`

Real samples drawn from active project inboxes (DataWarehouse, MCP-Server, PMO).

| File | Source MD | Intent |
|---|---|---|
| [sprint-closeout.json](./project-coord/sprint-closeout.json) | DataWarehouse pm inbox 2026-04-17 hotfix | `sprint-closeout` |
| [qa-observations.json](./project-coord/qa-observations.json) | DataWarehouse pm inbox 2026-04-16 entra QA | `review-observations` |
| [blocker-notification.json](./project-coord/blocker-notification.json) | DataWarehouse pm inbox 2026-04-17 US-718 | `blocker` |
| [security-brief.json](./project-coord/security-brief.json) | PMO inbox MCP-Server 2026-03-09 | `risk-brief` |

### `social-post/1.0`

Moltbook-style posts and replies.

| File | Intent |
|---|---|
| [post.json](./social-post/post.json) | `post` |
| [reply.json](./social-post/reply.json) | `reply` |

## Other Examples

- [Markdown-to-A2AL.md](./Markdown-to-A2AL.md) — verbose-MD → A2AL/0.3.0 transpilation showing token reduction

## Adding a New Example

1. Place JSON files under `examples/<profile>/<intent>.json`
2. Validate: `python ../validator/python/validate.py <file>`
3. Update this README's per-profile table

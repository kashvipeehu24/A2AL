# Contributing to A2AL

Thanks for your interest in A2AL. The protocol is intended to be **stable, vendor-neutral, and broadly implementable**. Contributions that strengthen those properties are very welcome.

## What we're looking for

- **Implementation reports** — "I built an A2AL writer/reader in $LANGUAGE; here's what was unclear" is gold. Open an issue.
- **Conformance corpus additions** — new positive or negative cases under `validator/corpus/core/` or `validator/corpus/profiles/<profile>/`. Especially edge cases the prose spec doesn't cover well.
- **Validator ports** — TypeScript, Go, Rust, etc. Each port must pass the existing corpus untouched.
- **New profiles** — domain profiles for use cases the reference profiles don't cover (research-handoff, code-review, retrieval-result, etc.). Add to `profiles/<name>-<version>.md`, register in `profiles/PROFILES.md`, ship a corpus.
- **Spec clarifications** — places where two readers could disagree on what's correct. PRs should add a corpus case alongside the prose change.
- **Worked examples** — additional `examples/<profile>/` material drawn from real workflows.

## What to avoid

- **Adding required core envelope fields.** Profiles can require their own; the core minimum stays at v/from/to/id/intent/profile.
- **Repair-on-receive logic.** The rulebook forbids it.
- **Transport coupling.** A2AL is transport-agnostic; HTTP/WS/MQTT framings belong elsewhere.

## Development workflow

1. Open an issue first for anything beyond a typo or test-case addition. This avoids duplicate work.
2. Fork and branch. Branch names like `spec/clarify-a4-refs` or `validator/python-bool-handling` are nice.
3. Add or update a corpus case for any behavioral change.
4. Run `python validator/python/test_corpus.py` and ensure it passes.
5. Open a PR. Describe **what changes** and **why** — link to the relevant spec section.

## Spec or profile changes

Material edits (anything other than typos or wording) should:

- Cite the exact section being clarified (`specs/A2A-Core.md` §X or `profiles/<profile>.md`)
- Add at least one positive and one negative corpus case demonstrating the new precision
- Note backward-compatibility impact

## Versioning

A2AL follows semantic versioning:

- **MAJOR** — incompatible grammar changes, envelope shape changes, type-ban changes
- **MINOR** — new profile sections, new optional envelope fields appended at the end, new examples
- **PATCH** — clarifications, validator fixes, documentation

## Conduct

Participation is expected to follow the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) — be respectful, focus on the work, no harassment. A formal `CODE_OF_CONDUCT.md` will be added to the repository as adoption grows.

## License

By contributing, you agree your contributions are licensed under [Apache-2.0](./LICENSE) like the rest of the project.

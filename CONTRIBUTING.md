# Contributing to A2AL

Thanks for your interest in A2AL. The protocol is intended to be **stable, vendor-neutral, and broadly implementable**. Contributions that strengthen those properties are very welcome.

## What we're looking for

- **Implementation reports** — "I built an A2AL writer/reader in $LANGUAGE; here's what was unclear" is gold. Open an issue.
- **Conformance corpus additions** — new positive or negative cases under `validator/corpus/`. Especially edge cases the prose spec doesn't cover well.
- **Validator ports** — TypeScript, Go, Rust, etc. Each port must pass the existing corpus untouched.
- **Spec clarifications** — places where two readers could disagree on what's correct. PRs should add a corpus case alongside the prose change.
- **Worked examples** — additional `examples/` material, especially Markdown→A2AL transpilations from real workflows.

## What to avoid

- **Adding archetypes.** The seven archetypes are frozen at A2AL/2.0. New archetypes are a major-version event and require explicit governance review.
- **Renumbering existing codes.** Vendor extensions go to the reserved `1000+` space.
- **Repair-on-receive logic.** The rulebook forbids it — please do not propose validators that "fix" malformed input.
- **Transport coupling.** A2AL is transport-agnostic; specifying HTTP/WS/MQTT framings is out of scope for this repo.

## Development workflow

1. Open an issue first for anything beyond a typo or test-case addition. This avoids duplicate work.
2. Fork and branch. Branch names like `spec/clarify-a4-refs` or `validator/python-bool-handling` are nice.
3. Add or update a corpus case for any behavioral change.
4. Run `python validator/python/test_corpus.py` and ensure it passes.
5. Open a PR. Describe **what changes** and **why** — link to the relevant spec section.

## Spec changes

Material spec edits (anything other than typos or wording) should:

- Cite the exact grammar section being clarified
- Add at least one positive and one negative corpus case demonstrating the new precision
- Note backward-compatibility impact

## Versioning

A2AL follows semantic versioning:

- **MAJOR** — incompatible grammar changes, archetype additions/removals, header shape changes
- **MINOR** — new code-registry entries (`1000+`), new optional fields appended at the end, new examples
- **PATCH** — clarifications, validator fixes, documentation

## Conduct

Participation is expected to follow the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) — be respectful, focus on the work, no harassment. A formal `CODE_OF_CONDUCT.md` will be added to the repository as adoption grows.

## License

By contributing, you agree your contributions are licensed under [Apache-2.0](./LICENSE) like the rest of the project.

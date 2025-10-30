Thank you for your interest in contributing to Azure Policy Engine!

This document expands on the contribution guidance in the project README and provides a short checklist to make contributions easier to review and land.

Getting started

- Fork the repository and create a feature branch from `main`.
- Keep changes focused: one logical change per pull request helps reviewers.
- If your change is large or architectural, open an issue first to discuss the approach.

Development workflow

1. Create a virtual environment and install dev dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the tests locally and make sure they pass before opening a PR:

```bash
PYTHONPATH=. pytest -q
```

3. Code style and docs

- Follow idiomatic Python and add docstrings for public functions and classes.
- Keep code readable and well-factored.
- Update the `README.md` or add docs in `mcp_travelplanner/README.md` if your change affects usage.

Pull request checklist

- [ ] Forked and created a branch for this change
- [ ] Added or updated tests for new behavior
- [ ] Ran tests locally: `PYTHONPATH=. pytest -q`
- [ ] Updated documentation if public behavior changed
- [ ] Included a clear PR description and linked any related issue(s)

Review process

- Maintainers will review pull requests and request changes as needed.
- Please respond to review comments promptly — small iterations are preferred.

Security

- If you discover a security vulnerability, please do not create a public issue. Instead, contact the maintainers privately (open an issue and mark it private or use the project's security contact if available).

License and contribution

By contributing, you agree that your contributions are licensed under the project's MIT license and may be distributed under those terms.

Thank you — your contributions help make this tool better for everyone!

# Agentic-Ai-testing

A small order API for testing your external PR reviewer. This repository owns
only sample application code, application tests, and a thin PR notification
workflow. All model settings, prompts, guidelines, policy, and review execution
belong to `sanket-thorat/cloud-upskilling-code-review-bot`.

## Automatic Review Flow

```text
PR in bindu885/Agentic-Ai-testing
  -> create an empty request commit on the reviewer's feature branch
  -> cloud-upskilling-code-review-bot fetches the PR's changed code
  -> your configured model reviews it against your guidelines
  -> central Actions run uploads findings and links results from the PR
```

In this repository's **Settings > Secrets and variables > Actions**, add only
`REVIEW_DISPATCH_TOKEN`: a token authorized for contents-write access to the
reviewer repository, needed to create an empty commit and advance only
`feature/core-review-bot` without force. Despite its retained name, this token
no longer sends `repository_dispatch` events. Do not put model settings or API
keys here. Fork PRs are skipped.

Complete the model and token setup in the original repository:
[central setup guide](https://github.com/sanket-thorat/cloud-upskilling-code-review-bot/blob/feature/core-review-bot/docs/week6/testing-external-repository.md).
Push the updated central workflow and complete reviewer implementation to
`feature/core-review-bot`; the reviewer does NOT need a merge into `main`.
The application sample and notification workflow can be merged into this repo's
`main` before creating a defect PR. Each request adds a metadata-only commit to
the reviewer branch; it never changes reviewer files. GitHub Actions must be
enabled in both repositories. Use a PAT or GitHub App token for requests, not
the application's automatic `GITHUB_TOKEN`.

## Run the Sample

Use Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest -q
python -m uvicorn app.main:app --reload
```

The API is at `http://127.0.0.1:8000/docs`. Order 1 is pending; order 2 is shipped.
Data is in memory and resets when the process restarts. Controllers delegate to
the service, which enforces cancellation rules and calls the repository. API
errors use FastAPI's `detail` field with a `code` and `message` object.

## Create the First Test PR

First commit and push this CLEAN sample and notification workflow to the base
branch. Then create a separate branch with a deliberately problematic change:

```bash
git switch -c test/mutable-labels
```

Replace `add_label` in `app/labels.py` with:

```python
def add_label(label: str, labels: list[str] = []) -> list[str]:
    labels.append(label)
    return labels
```

Commit and push that change, then open a PR against the clean base branch.
The reviewer should consider `PY-002`; the existing label-isolation test also
fails on this bug. Do not merge the deliberate defect.

## More Review Cases

| Change made in a separate PR | Expected review candidate |
| --- | --- |
| Add a mutable default to `app/labels.py` as above | `PY-002`: shared mutable default |
| Add an unexplained `except Exception` handler in `app/controller.py` | `PY-001`: broad exception handling |
| Move the shipped-status check and repository calls from `OrderService.cancel_order` into the controller | `ARCH-001`: business logic bypasses the service |
| Add another properly typed helper that uses `None` instead of a mutable default | No mutable-default finding |

Architecture checks can identify a layering issue even when behavior tests pass.
Model findings are not guaranteed: applicability, repository evidence, and
validation determine which candidates survive. The bot reviews the PR's actual
diff, using related files as context; it is not a blanket scan of every old file.

## See the Results

The application Actions run only confirms that the request was sent. The model
runs under **Actions > Review external application PR** in the reviewer repo.
After successful analysis, the PR receives a comment linking that run's report
and decision packet. A green request run alone does not mean analysis passed.
Filter the central Actions page by branch `feature/core-review-bot` if needed.
The initial workflow deployment push has no request marker, so its review job
is skipped; a subsequent application PR event starts the actual review.

Opening, pushing commits to, or reopening a same-repository PR sends a request.
The existing human-review gate is preserved: a results-link comment is posted
automatically, but inline findings and approve/request-changes reviews still
require human decisions. Nothing is auto-accepted. Readers need access to the
reviewer repo to download its artifacts.

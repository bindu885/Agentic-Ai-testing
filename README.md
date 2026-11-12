# Agentic-Ai-testing

A small order API for testing your external PR reviewer. This repository owns
only sample application code, application tests, and a thin PR notification
workflow. All model settings, prompts, guidelines, policy, and review execution
belong to `bindu885/Code-Review-bot`.

## Review on Request

```text
Authorized user comments PR-Review on an open PR
  -> create an empty request commit on the reviewer's feature branch
  -> bindu885/Code-Review-bot fetches the PR's changed code
  -> your configured model reviews it against your guidelines
  -> central Actions run uploads findings and links results from the PR
```

In this repository's **Settings > Secrets and variables > Actions**, add only
`REVIEW_DISPATCH_TOKEN`: a token authorized for contents-write access to the
reviewer repository, needed to create an empty commit and advance only
`feature/core-review-bot` without force. Despite its retained name, this token
no longer sends `repository_dispatch` events. Do not put model settings or API
keys here. Fork PRs are skipped.

Complete the model and token setup in `bindu885/Code-Review-bot`:
[central setup guide](https://github.com/bindu885/Code-Review-bot/blob/feature/core-review-bot/docs/week6/testing-external-repository.md).
Push the updated central workflow and complete reviewer implementation to
`feature/core-review-bot`; the reviewer does NOT need a merge into `main`.
The comment-trigger workflow MUST be installed on this repo's default branch,
`main`, because GitHub reads `issue_comment` workflows from that branch. Install
only the workflow there; do not merge the deliberately defective validation PR.
The reviewer implementation remains on its feature branch. Each accepted command adds a metadata-only commit to
the reviewer branch; it never changes reviewer files. GitHub Actions must be
enabled in both repositories. Use a PAT or GitHub App token for requests, not
the application's automatic `GITHUB_TOKEN`.

The two repositories share an owner, but their automatic `GITHUB_TOKEN` values
are still repository-scoped. Configure `REVIEW_DISPATCH_TOKEN` here for
contents-write access to `bindu885/Code-Review-bot`. Configure `TARGET_REPO_TOKEN`
in that reviewer repo for contents-read and pull-requests-write access to this
sample repo. Existing tokens scoped to Sanket's repo must be replaced.

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
Add a new PR conversation comment containing exactly `PR-Review` to request AI
analysis. Case and surrounding whitespace are ignored. Only writers, maintainers,
and admins can request a review. Inline code-review comments, issue comments on
non-PR issues, closed PRs, and fork PRs do not start model review.
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

After an accepted command, a PR acknowledgement confirms whether the request was
sent and names the exact head commit. The model
runs under **Actions > Review external application PR** in the reviewer repo.
After successful analysis, the PR receives a comment linking that run's report
and decision packet. A green request run alone does not mean analysis passed.
Filter the central Actions page by branch `feature/core-review-bot` if needed.
The initial workflow deployment push has no request marker, so its review job
is skipped; a subsequent authorized `PR-Review` comment starts the actual review.

Opening, pushing commits to, or reopening a PR does not request AI analysis.
After further changes, add a NEW `PR-Review` comment to review the latest head.
Editing an old command does not start another review. The standards summary is
updated in place; always check its recorded head commit rather than its original
creation timestamp. Small changes can proceed without requesting AI review.
The existing human-review gate is preserved: the standards summary is posted
after the requested analysis, but formal inline findings and approve/request-changes reviews still
require human decisions. Nothing is auto-accepted. Readers need access to the
reviewer repo to download its artifacts.




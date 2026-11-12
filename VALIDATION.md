# Standards Review Validation

This branch deliberately contains defects for testing the external reviewer.
Do not merge these examples into the clean application baseline.
No infrastructure resources are declared and no production services are called.

## Frozen Expected Cases

| File and symbol | Expected review candidate |
| --- | --- |
| `app/labels.py`, `add_label` | `PY-002`: mutable default shares labels across calls |
| `app/validation_helpers.py`, `parse_quantity` | `PY-001`: undocumented broad exception hides conversion failures |
| `app/validation_helpers.py`, `normalize_label` | `PY-003`: public function lacks useful type annotations |
| `app/validation_helpers.py`, `read_description` | `GEN-003`: owned file handle has no guaranteed cleanup |
| `infra/variables.tf`, `region` | `TF-001`: input variable lacks explicit type and description |
| `infra/variables.tf`, `replica_count` | `TF-003`: default violates the explicit minimum and validation condition |
| `app/validation_helpers.py`, `read_description_safely` | No resource-cleanup finding: a context manager owns cleanup |
| `infra/compliant.tf`, `environment` | No type, description, or allowed-value finding |
| `infra/versions.tf` | Terraform version context exists; do not claim every resource file needs another version declaration |

These are expected model-review candidates, not precomputed model results.
Record missed candidates and false positives rather than changing labels to
match a run. Findings must cite actual supplied evidence and valid locations.

## Interpretation

The label-isolation unit test is expected to fail on the planted mutable default.
Other existing application tests should continue to pass. Terraform formatting
and structural `terraform validate` should pass. A no-refresh `terraform plan`
evaluates the variable validation and should reject the negative default.
No apply operation is needed, and this fixture declares no resources.

The sample Actions run sends the request only. Inspect the central reviewer
run and its PR summary for actual findings. A human-review-needed failure is
not proof that standards were analyzed. Safe diagnostic codes and the failed
stage appear in the central report when startup or analysis fails.

Automatic feedback is provisional. Formal approval, merge protection, and
the complete Day 30 mixed-case acceptance suite remain separate requirements.
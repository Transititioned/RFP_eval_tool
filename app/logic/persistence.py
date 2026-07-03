"""Free persistence for intake records: append-only CSV log in a private
Hugging Face Dataset repo, written via the Hub API on each save.

No local database. Every save is one commit to the dataset repo, which
gives an audit trail as a side effect. If HF_TOKEN / HF_INTAKE_DATASET_REPO
are not configured (e.g. running locally without secrets), saving is
skipped and the caller is told so — the app still works, it just doesn't
persist.
"""

import csv
import datetime
import os
import tempfile

DEFAULT_REPO_ID = "Ausadmin/RFP_evaluation_tool-intake"
LOG_FILENAME = "intake_log.csv"

FIELDNAMES = [
    "saved_at",
    "project_name",
    "requester_role",
    "business_area",
    "problem_statement",
    "why_now",
    "primary_capability",
    "desired_decision_date",
    "budget_confirmed",
    "compliance_deadline",
    "incumbent_or_preferred_vendor",
    "existing_license_or_contract",
]


def _config():
    repo_id = os.environ.get("HF_INTAKE_DATASET_REPO", DEFAULT_REPO_ID)
    token = os.environ.get("HF_TOKEN")
    return repo_id, token


def _read_existing_rows(api, repo_id, token):
    """Return (rows, error_message). error_message is None on success."""
    from huggingface_hub import hf_hub_download
    from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError

    try:
        local_path = hf_hub_download(
            repo_id=repo_id, repo_type="dataset", filename=LOG_FILENAME, token=token
        )
        with open(local_path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), None
    except (EntryNotFoundError, RepositoryNotFoundError):
        return [], None
    except Exception as e:
        return [], f"could not read existing log ({e})"


def append_intake_record(record):
    """Append one row to the persistent intake log.

    Returns a short status string suitable for display under the summary.
    """
    repo_id, token = _config()
    if not token:
        return (
            "_Not saved to persistent storage: HF_TOKEN is not set. "
            "This session's intake is not persisted._"
        )

    from huggingface_hub import HfApi

    api = HfApi(token=token)

    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    except Exception as e:
        return f"_Not saved: could not access or create dataset repo '{repo_id}' ({e})._"

    row = dict(record)
    row["saved_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    existing_rows, error = _read_existing_rows(api, repo_id, token)
    if error:
        return f"_Not saved: {error}._"

    existing_rows.append(row)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", newline="", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.DictWriter(tmp, fieldnames=FIELDNAMES)
            writer.writeheader()
            for r in existing_rows:
                writer.writerow({k: r.get(k, "") for k in FIELDNAMES})
            tmp_path = tmp.name

        api.upload_file(
            path_or_fileobj=tmp_path,
            path_in_repo=LOG_FILENAME,
            repo_id=repo_id,
            repo_type="dataset",
            commit_message="Add intake record",
        )
    except Exception as e:
        return f"_Not saved: upload failed ({e})._"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return f"_Saved to persistent log ({len(existing_rows)} record(s) total)._"


def load_intake_log():
    """Read the persistent intake log for display.

    Returns (rows, status) where rows is a list of lists aligned to
    FIELDNAMES (newest first), and status is a short message about what
    happened (row count, or why nothing loaded).
    """
    repo_id, token = _config()
    if not token:
        return [], "_Not loaded: HF_TOKEN is not set._"

    from huggingface_hub import HfApi

    api = HfApi(token=token)
    existing_rows, error = _read_existing_rows(api, repo_id, token)
    if error:
        return [], f"_Not loaded: {error}._"

    rows = [[r.get(k, "") for k in FIELDNAMES] for r in reversed(existing_rows)]
    if not rows:
        return [], "_No saved records yet._"
    return rows, f"_Showing {len(rows)} saved record(s), newest first._"

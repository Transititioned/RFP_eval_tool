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

    from huggingface_hub import HfApi, hf_hub_download
    from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError

    api = HfApi(token=token)

    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
    except Exception as e:
        return f"_Not saved: could not access or create dataset repo '{repo_id}' ({e})._"

    row = dict(record)
    row["saved_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    existing_rows = []
    try:
        local_path = hf_hub_download(
            repo_id=repo_id, repo_type="dataset", filename=LOG_FILENAME, token=token
        )
        with open(local_path, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))
    except (EntryNotFoundError, RepositoryNotFoundError):
        existing_rows = []
    except Exception as e:
        return f"_Not saved: could not read existing log ({e})._"

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

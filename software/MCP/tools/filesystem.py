import os
import subprocess
from pathlib import Path


def get_repo_path():
    return os.getenv("RDPA_PATH", os.path.expanduser("~/RDPA"))


# -----------------------------
# READ ALL MARKDOWN FILES
# -----------------------------
def read_rdpa_journals():
    repo_path = get_repo_path()

    if not os.path.exists(repo_path):
        return f"RDPA repo not found: {repo_path}"

    md_files = []

    # collect markdown files from git repo
    try:
        files = subprocess.check_output(
            ["git", "-C", repo_path, "ls-files"],
            text=True
        ).splitlines()

        md_files = [f for f in files if f.endswith(".md")]

    except Exception:
        # fallback if git fails
        md_files = list(Path(repo_path).rglob("*.md"))

    if not md_files:
        return "No markdown journals found in RDPA."

    all_content = []

    for file in md_files:
        full_path = os.path.join(repo_path, file)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            all_content.append(f"""
FILE: {file}
CONTENT:
{content}
""")

        except Exception as e:
            all_content.append(f"{file} (read error: {e})")

    return "\n\n".join(all_content)

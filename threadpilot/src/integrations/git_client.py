from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from git import Repo


class GitClient:
    def __init__(self, repo_path: str | Path = ".") -> None:
        self.repo = Repo(Path(repo_path), search_parent_directories=True)

    def recent_commits(self, limit: int = 5) -> List[Dict[str, str]]:
        commits = []
        for commit in self.repo.iter_commits(max_count=limit):
            commits.append(
                {
                    "sha": commit.hexsha,
                    "author": str(commit.author),
                    "message": commit.message.strip(),
                }
            )
        return commits

    def pr_diff(self, base_ref: str = "HEAD~1", target_ref: str = "HEAD") -> str:
        return self.repo.git.diff(base_ref, target_ref)

    @staticmethod
    def summarize_for_llm(commits: List[Dict[str, str]], diff: str) -> str:
        commit_summary = "\n".join(
            f"- {item['sha'][:7]} | {item['author']} | {item['message']}" for item in commits
        )
        return f"Recent commits:\n{commit_summary}\n\nDiff:\n{diff[:8000]}"

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from git import InvalidGitRepositoryError, Repo


class GitClient:
    def __init__(self, repo_path: str | Path = ".") -> None:
        self.repo: Repo | None = None
        try:
            self.repo = Repo(Path(repo_path), search_parent_directories=True)
        except InvalidGitRepositoryError:
            self.repo = None

    def recent_commits(self, limit: int = 5) -> List[Dict[str, str]]:
        if self.repo is None:
            return []

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
        if self.repo is None:
            return ""
        try:
            commits = list(self.repo.iter_commits(max_count=2))
            if len(commits) < 2:
                return self.repo.git.show("HEAD", "--pretty=format:", "--no-color")
            return self.repo.git.diff(base_ref, target_ref)
        except Exception:
            return ""

    @staticmethod
    def summarize_for_llm(commits: List[Dict[str, str]], diff: str) -> str:
        commit_summary = "\n".join(
            f"- {item['sha'][:7]} | {item['author']} | {item['message']}" for item in commits
        )
        return f"Recent commits:\n{commit_summary}\n\nDiff:\n{diff[:8000]}"

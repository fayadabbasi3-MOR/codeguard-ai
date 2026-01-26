from typing import Optional, List, Dict, Any
from github import Github, GithubException
from github.PullRequest import PullRequest

from ..config import get_settings
from ..models.schemas import IssueResponse

settings = get_settings()


class GitHubService:
    def __init__(self):
        self.client = None
        if settings.github_token:
            self.client = Github(settings.github_token)

    def get_pr_diff(self, repo: str, pr_number: int) -> tuple[str, dict]:
        """
        Fetch the diff for a pull request.

        Returns:
            tuple: (diff_text, pr_info)
        """
        if not self.client:
            return "", {"error": "GitHub token not configured"}

        try:
            repository = self.client.get_repo(repo)
            pr = repository.get_pull(pr_number)

            # Get the diff
            files = pr.get_files()
            diff_parts = []

            for file in files:
                diff_parts.append(f"--- {file.filename}")
                diff_parts.append(f"+++ {file.filename}")
                if file.patch:
                    diff_parts.append(file.patch)
                diff_parts.append("")

            diff_text = "\n".join(diff_parts)

            pr_info = {
                "title": pr.title,
                "author": pr.user.login,
                "url": pr.html_url,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
            }

            return diff_text, pr_info

        except GithubException as e:
            print(f"GitHub API error: {e}")
            return "", {"error": str(e)}

    def post_review_comment(
        self,
        repo: str,
        pr_number: int,
        body: str,
        commit_sha: Optional[str] = None
    ) -> Optional[str]:
        """
        Post a review comment on a PR.

        Returns:
            Comment ID if successful, None otherwise
        """
        if not self.client:
            return None

        try:
            repository = self.client.get_repo(repo)
            pr = repository.get_pull(pr_number)

            # Create a review with a summary comment
            review = pr.create_review(body=body, event="COMMENT")
            return str(review.id)

        except GithubException as e:
            print(f"Error posting review: {e}")
            return None

    def post_inline_comment(
        self,
        repo: str,
        pr_number: int,
        body: str,
        file_path: str,
        line: int,
        commit_sha: str
    ) -> Optional[str]:
        """
        Post an inline comment on a specific line.

        Returns:
            Comment ID if successful, None otherwise
        """
        if not self.client:
            return None

        try:
            repository = self.client.get_repo(repo)
            pr = repository.get_pull(pr_number)

            # Get the latest commit
            commit = repository.get_commit(commit_sha)

            comment = pr.create_review_comment(
                body=body,
                commit=commit,
                path=file_path,
                line=line,
            )
            return str(comment.id)

        except GithubException as e:
            print(f"Error posting inline comment: {e}")
            return None

    def format_review_comment(self, issues: List[IssueResponse], summary: str = None) -> str:
        """Format issues into a GitHub review comment."""
        lines = ["## 🤖 CodeGuard Review\n"]

        # Summary
        critical = sum(1 for i in issues if i.severity.value == "critical")
        warnings = sum(1 for i in issues if i.severity.value == "warning")
        suggestions = sum(1 for i in issues if i.severity.value == "suggestion")

        if not issues:
            lines.append("✅ **No issues found!** Great job!\n")
            if summary:
                lines.append(f"*{summary}*\n")
            return "\n".join(lines)

        lines.append(f"**Summary:** {len(issues)} issues found")
        parts = []
        if critical:
            parts.append(f"🔴 {critical} critical")
        if warnings:
            parts.append(f"⚠️ {warnings} warnings")
        if suggestions:
            parts.append(f"💡 {suggestions} suggestions")
        lines.append(f" • {' • '.join(parts)}\n")

        # Group issues by severity
        if critical:
            lines.append("### 🔴 Critical Issues\n")
            for issue in [i for i in issues if i.severity.value == "critical"]:
                lines.append(self._format_issue(issue))

        if warnings:
            lines.append("### ⚠️ Warnings\n")
            for issue in [i for i in issues if i.severity.value == "warning"]:
                lines.append(self._format_issue(issue))

        if suggestions:
            lines.append("### 💡 Suggestions\n")
            for issue in [i for i in issues if i.severity.value == "suggestion"]:
                lines.append(self._format_issue(issue))

        # Footer
        lines.append("\n---")
        lines.append("*Powered by CodeGuard • React with 👍 or 👎 to help me learn*")

        return "\n".join(lines)

    def _format_issue(self, issue: IssueResponse) -> str:
        """Format a single issue for the review comment."""
        lines = []

        location = f"**{issue.file_path}**"
        if issue.line_number:
            location += f" (line {issue.line_number})"

        lines.append(f"- {location}")
        lines.append(f"  **{issue.title}**")
        lines.append(f"  {issue.message}")

        if issue.explanation:
            lines.append(f"  *Why:* {issue.explanation}")

        if issue.suggestion:
            lines.append(f"  *Fix:* {issue.suggestion}")

        lines.append("")
        return "\n".join(lines)


# Singleton instance
github_service = GitHubService()


def get_github_service() -> GitHubService:
    return github_service

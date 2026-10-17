# app/services/github_service.py
import requests
from github import Github
from config import settings

# Initialize PyGithub client using token from config
gh_client = Github(settings.GITHUB_TOKEN)

def fetch_pr_diff(diff_url: str) -> str:
    """
    Fetches raw git diff text from GitHub using authorized request.
    """
    headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
    response = requests.get(diff_url, headers=headers)
    if response.status_code == 200:
        return response.text
    return ""

def post_github_comment(repo_full_name: str, pr_number: int, review_body: str):
    """
    Posts the formatted AI review comment on the target GitHub Pull Request.
    """
    try:
        repo = gh_client.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)

        formatted_comment = (
            f"### 🤖 AI Code Inspector Review\n\n"
            f"{review_body}\n\n"
            f"---\n"
            f"*Powered by AI Code Inspector | Domain-Specific Automated PR Review*"
        )
        pr.create_issue_comment(formatted_comment)
    except Exception as e:
        print(f"Error posting GitHub comment: {e}")
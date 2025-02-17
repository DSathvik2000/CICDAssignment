from dotenv import load_dotenv
import os
from github import Github

load_dotenv()
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
user_name = os.getenv("GITHUB_USERNAME")
repo_name = os.getenv("GITHUB_REPO")

if not ACCESS_TOKEN:
    raise ValueError("GitHub Access Token not found. Please check your .env file.")

g = Github(ACCESS_TOKEN)


repo = g.get_repo("f{user_name}/{repo_name}")
print(repo)
commits = repo.get_commits()[0]

#print(commits)
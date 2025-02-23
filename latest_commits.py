from flask import Flask
import os
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv()

# Get GitHub credentials from .env
ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Flask App
app = Flask(__name__)

@app.route("/")
def index():
    if not ACCESS_TOKEN or not GITHUB_USERNAME or not GITHUB_REPO:
        return "Missing GitHub credentials", 500

    try:
        # Authenticate with GitHub and fetch the latest commit
        g = Github(ACCESS_TOKEN)
        repo = g.get_repo(f"{GITHUB_USERNAME}/{GITHUB_REPO}")
        latest_commit = repo.get_commits()[0]

        new_commit_file = "new_commit.txt"
        stored_latest_commit = None

        # Read the stored commit from new_commit.txt if it exists
        if os.path.exists(new_commit_file):
            with open(new_commit_file, "r") as f:
                lines = f.readlines()
                if lines:
                    stored_latest_commit = lines[0].strip()

        # If the latest commit is different, update the file with the new and previous commits.
        if stored_latest_commit != latest_commit.sha:
            previous_commit = stored_latest_commit if stored_latest_commit is not None else "None"
            with open(new_commit_file, "w") as f:
                f.write(latest_commit.sha + "\n")
                f.write(previous_commit + "\n")
            return f"New commit detected. Updated new_commit.txt with latest commit."
        else:
            return f"No new commit found."

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)

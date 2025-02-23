from flask import Flask, render_template
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
app = Flask(__name__, template_folder="templates/")

@app.route("/")
def index():
    # Verify credentials are available
    if not ACCESS_TOKEN or not GITHUB_USERNAME or not GITHUB_REPO:
        return "Missing GitHub credentials", 500

    try:
        # Authenticate with GitHub and fetch the latest commit
        g = Github(ACCESS_TOKEN)
        repo = g.get_repo(f"{GITHUB_USERNAME}/{GITHUB_REPO}")
        latest_commit = repo.get_commits()[0]

        # File to store the last seen commit
        last_commit_file = "last_commit.txt"
        last_commit_id = None

        # Read the last stored commit SHA if it exists
        if os.path.exists(last_commit_file):
            with open(last_commit_file, "r") as f:
                last_commit_id = f.read().strip()

        # If the latest commit is different, it's new: create/update "new commit.txt"
        if last_commit_id != latest_commit.sha:
            with open("new commit.txt", "w") as f:
                f.write(latest_commit.sha)
            # Update the stored commit for future comparisons
            with open(last_commit_file, "w") as f:
                f.write(latest_commit.sha)

        # Prepare commit data for rendering
        commit_data = {
            "sha": latest_commit.sha,
            "author": latest_commit.commit.author.name,
            "message": latest_commit.commit.message,
            "date": latest_commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return render_template("index.html", commit=commit_data)

    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)

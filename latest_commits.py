from flask import Flask, jsonify, render_template
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


# Route to fetch latest commits
@app.route("/api/commits")
def get_commits():
    if not ACCESS_TOKEN or not GITHUB_USERNAME or not GITHUB_REPO:
        return jsonify({"error": "Missing GitHub credentials"}), 500

    try:
        # 🔹 Authenticate with GitHub
        g = Github(ACCESS_TOKEN)
        repo = g.get_repo(f"{GITHUB_USERNAME}/{GITHUB_REPO}")
        
        # 🔹 Fetch the latest commit
        latest_commit = repo.get_commits()[0]

        # 🔹 Format response as JSON
        commit_list = {
            "sha": latest_commit.sha,
            "author": latest_commit.commit.author.name,
            "message": latest_commit.commit.message,
            "date": latest_commit.commit.author.date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return jsonify(commit_list)  # 🔹 Return JSON response to JavaScript

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to serve frontend
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

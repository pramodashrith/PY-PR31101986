import os
import requests
from github import Github


# Jenkins server information
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

GITHUB_TOKEN = "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"
GITHUB_REPO_OWNER = "pramodashrith"
GITHUB_REPO_NAME = "PY-PR31101986"
GITHUB_REPO_BRANCH = "main"


# Directory to store backup
BACKUP_DIR = "/Users/pramodashrith/backupjob"

def get_job_config(job_name):
    config_url = f"{JENKINS_URL}/job/{job_name}/job/config.xml"
    response = requests.get(config_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        return response.text
    else:
        return None

def backup_and_push_to_github():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")
    for root, _, files in os.walk(BACKUP_DIR):
        for file in files:
            if file.endswith("_config.xml"):
                job_name = file.replace("_config.xml", "")
                job_config = get_job_config(job_name)
                if job_config:
                    backup_path = os.path.join(BACKUP_DIR, file)
                    with open(backup_path, "w") as config_file:
                        config_file.write(job_config)
                    print(f"Backup saved: {backup_path}")

                    # Update GitHub repository
                    with open(backup_path, "r") as config_file:
                        file_content = config_file.read()
                        repo.create_file(
                            f"job_configs/{file}",
                            f"Backup of {file}",
                            file_content,
                            branch=GITHUB_REPO_BRANCH,
                        )
                    print(f"Uploaded to GitHub: {file}")
    
if __name__ == "__main__":
    backup_and_push_to_github()


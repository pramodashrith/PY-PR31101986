import os
import requests
from github import Github

# Jenkins server information
JENKINS_URL = "http://localhost:8080/"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

GITHUB_TOKEN = "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"
GITHUB_REPO_OWNER = "pramodashrith"
GITHUB_REPO_NAME = "PY-PR31101986"
GITHUB_REPO_BRANCH = "main"

# Directory to store backup
BACKUP_DIR = "/Users/pramodashrith/backupjob"

def get_job_config(job_name):
    config_url = f"{JENKINS_URL}/job/{job_name}/config.xml"
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

    folders_url = f"{JENKINS_URL}/api/json?tree=jobs[name,jobs[name]]"
    response = requests.get(folders_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        data = response.json()
        for folder in data["jobs"]:
            if "jobs" in folder:
                folder_name = folder["name"]
                for job in folder["jobs"]:
                    job_name = job["name"]
                    job_config = get_job_config(f"{folder_name}/{job_name}")
                    if job_config:
                        backup_path = os.path.join(BACKUP_DIR, folder_name, f"{job_name}_config.xml")
                        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                        with open(backup_path, "w") as config_file:
                            config_file.write(job_config)
                        print(f"Backup saved: {backup_path}")

                        # Update GitHub repository
                        with open(backup_path, "r") as config_file:
                            file_content = config_file.read()
                            repo.create_file(
                                f"job_configs/{folder_name}/{job_name}_config.xml",
                                f"Backup of {folder_name}/{job_name}",
                                file_content,
                                branch=GITHUB_REPO_BRANCH,
                            )
                        print(f"Uploaded to GitHub: {folder_name}/{job_name}")

if __name__ == "__main__":
    backup_and_push_to_github()


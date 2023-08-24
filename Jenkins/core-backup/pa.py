import os
import requests
from github import Github

# Jenkins server information
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

# GitHub repository information
GITHUB_TOKEN = "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"
GITHUB_REPO_OWNER = "pramodashrith"
GITHUB_REPO_NAME = "PY-PR31101986"
GITHUB_REPO_BRANCH = "main"

# Directory to store backup
BACKUP_DIR = "Jenkins/core-backup"

def get_job_config(job_name):
    config_url = f"{JENKINS_URL}/job/{job_name}/config.xml"
    response = requests.get(config_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        return response.text
    else:
        return None

def create_jenkinsfile():
    jenkinsfile_content = (
        "pipeline {\n"
        "    agent any\n"
        "    triggers {\n"
        "        cron('@daily')\n"
        "    }\n"
        "    stages {\n"
        "        stage('Backup Jobs') {\n"
        "            steps {\n"
        "                script {\n"
    )

    for root, _, files in os.walk(BACKUP_DIR):
        for file in files:
            if file.endswith("_config.xml"):
                job_name = file.replace("_config.xml", "")
                jenkinsfile_content += (
                    f"                    sh 'curl -X POST {JENKINS_URL}/job/{job_name}/config.xml -u {USERNAME}:{API_TOKEN} -o {job_name}_config.xml'\n"
                )

    jenkinsfile_content += (
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}\n"
    )

    with open(os.path.join(BACKUP_DIR, "Jenkinsfile"), "w") as jenkinsfile:
        jenkinsfile.write(jenkinsfile_content)

def update_github_repo():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f'{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}')
    repo_contents = repo.get_contents("", ref=GITHUB_REPO_BRANCH)
    branch = repo.get_branch(GITHUB_REPO_BRANCH)

    # Create a new commit with the file change
    commit_message = "Update file via Python script"
    repo.create_git_commit(commit_message, repo_contents, BACKUP_DIR, [branch.commit])

    # Push the commit to the repository
    repo.get_git_ref(f"heads/{GITHUB_REPO_BRANCH}").edit(commit_message.sha)
    with open(os.path.join(BACKUP_DIR, "Jenkinsfile"), "r") as jenkinsfile:
        jenkinsfile_content = jenkinsfile.read()

    repo.create_file(
        "Jenkinsfile",
        "Automated daily backup Jenkinsfile",
        jenkinsfile_content,
        commit_message,
        branch
    )

if __name__ == "__main__":
    # Step 1: Backup jobs' configurations
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    job_list_url = f"{JENKINS_URL}/api/json?tree=jobs[name]"
    response = requests.get(job_list_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        job_data = response.json()
        for job in job_data["jobs"]:
            job_name = job["name"]
            job_config = get_job_config(job_name)
            if job_config:
                backup_path = os.path.join(BACKUP_DIR, f"{job_name}_config.xml")
                with open(backup_path, "w") as config_file:
                    config_file.write(job_config)
                print(f"Backup saved: {backup_path}")
            else:
                print(f"Failed to retrieve config for job: {job_name}")
    else:
        print("Failed to retrieve job list")

    # Step 2: Create Jenkinsfile
    create_jenkinsfile()
    print("Jenkinsfile created")

    # Step 3: Update GitHub repository
    update_github_repo()
    print("GitHub repository updated")

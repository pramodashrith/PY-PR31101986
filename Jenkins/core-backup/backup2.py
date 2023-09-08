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
GITHUB_REPO_BRANCH = "test"

# Create a session for Jenkins with basic authentication
session = requests.Session()
session.auth = (USERNAME, API_TOKEN)

# Connect to GitHub
g = Github(GITHUB_TOKEN)
# Directory to store backup
BACKUP_DIR = "/Jenkins/core-backup"

# Get a list of all job names from Jenkins
response = session.get(f'{JENKINS_URL}/api/json')
job_data = response.json()
job_names = [job['name'] for job in job_data['jobs']]

# Loop through job names, retrieve config.xml, and push to GitHub
for job_name in job_names:
    # Get the configuration XML for the job from Jenkins
    response = session.get(f'{JENKINS_URL}/job/{job_name}/config.xml')
    if response.status_code == 200:
        config_xml = response.text
        # Push the config.xml to GitHub
        repo = g.get_repo(GITHUB_REPO_NAME)
        
        repo = g.get_repo(f'{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}')
        repo_contents = repo.get_contents("", ref=GITHUB_REPO_BRANCH)
        branch = repo.get_branch(GITHUB_REPO_BRANCH)

        # Create a new commit with the file change
        commit_message = "Update file via Python script"
        repo.create_git_commit(commit_message, repo_contents, BACKUP_DIR, [branch.commit])
        
        file_path = f"{job_name}/config.xml"
        commit_message = f"Update config.xml for {job_name}"
        
        try:
            contents = repo.get_contents(file_path, ref=GITHUB_REPO_BRANCH)
            repo.update_file(file_path, commit_message, config_xml, contents.sha, branch_name)
            print(f"Config.xml for job '{job_name}' pushed to GitHub.")
        except Exception as e:
            print(f"Error pushing config.xml for job '{job_name}' to GitHub: {str(e)}")
    else:
        print(f"Failed to retrieve config.xml for job '{job_name}' from Jenkins.")


def get_job_config(job_name):
    config_url = f"{JENKINS_URL}/job/{job_name}/job/config.xml"
    response = requests.get(config_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        return response.text
    else:
        return None




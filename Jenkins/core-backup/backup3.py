import os
import requests
from github import Github
import time
import datetime

# Jenkins server information
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

GITHUB_TOKEN = "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"
GITHUB_REPO_OWNER = "pramodashrith"
GITHUB_REPO_NAME = "PY-PR31101986"
GITHUB_REPO_BRANCH = "main"

# Path to the folder in the repository where backups will be committed
FOLDER_PATH = "Jenkins/core-backup"

# Initialize a Github object with your token
g = Github(GITHUB_TOKEN)

# Get the repository using the owner and name
repo = g.get_repo(f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")

def commit_file(backup_file_path, file_content, commit_message):
    client = Github(GITHUB_REPO_OWNER, GITHUB_TOKEN)
    repo = g.get_repo(f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}")

    today = datetime.datetime.today()
    commit_message = 'Backup of Jenkins jobs on %s' % today.strftime('%Y-%m-%d')

    for file in [f for f in os.listdir('.') if f.endswith('.xml')]:
        repo.create_file(file, commit_message, open(file, 'rb'), "utf-8")

def backup_job_config(job_name, backup_file_path):
    # Retrieve job config.xml content (replace with your method to get config.xml)
    config_xml = f"Job configuration XML for {job_name}"

    # Create a temporary backup file
    backup_file_path = 'config_backup.xml'
    with open(backup_file_path, 'w') as backup_file:
        backup_file.write(config_xml)
    
   

def main(): 
    job_names = "Testpipeline"  # Replace with your job name
    #job_names = f"{JENKINS_URL}/job/{job_name}/job/config.xml"  # Replace with your job name
    backup_file_name = f"{job_names}_config.xml"
    backup_file_path = f"/Users/pramodashrith/backupjob/{backup_file_name}"  # Replace with your local backup path
   

    # Backup job config.xml
    backup_job_config(job_names, backup_file_path)

    # Read backup file content
    backup_file_path = 'config_backup.xml'
    with open(backup_file_path, 'r') as backup_file:
       backup_content = backup_file.read()

    # Commit backup to GitHub
    commit_message = f"Backup of {job_names} config.xml"
    commit_file(FOLDER_PATH + "/" + backup_file_name, backup_content, commit_message)
    

if __name__ == "__main__":
    main()

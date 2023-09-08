from jenkinsapi.jenkins import Jenkins
from github import Github
import os


# Jenkins server information
jenkins_url = "http://localhost:8080"
username = "admin"
password = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"
github_token = "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"
GITHUB_REPO_OWNER = "pramodashrith"
repo_name = "PY-PR31101986"
branch_name = "test"


# Connect to Jenkins
jenkins = Jenkins(jenkins_url, username=username, password=password)

# Connect to GitHub
g = Github(github_token)

# Get a list of all jobs, including those inside folders


jobs = jenkins.get_jobs()

for job in jobs:
  if job.parent:
    parent = job.parent
    while parent:
      job = parent
      parent = job.parent
    root_name = job.short_name
    print(root_name)
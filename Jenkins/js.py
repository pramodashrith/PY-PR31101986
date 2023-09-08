import os
import git
from jenkinsapi.jenkins import Jenkins
import shutil


JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

GITHUB_TOKEN = "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"
GITHUB_REPO_OWNER = "pramodashrith"
GITHUB_REPO_NAME = "PY-PR31101986"
GITHUB_REPO_BRANCH = "main"

jenkins = Jenkins(JENKINS_URL, username=USERNAME, password=API_TOKEN)

cloned_repo_path = os.envron.get()
import logging
import requests
import os
from github import Github
import git

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Jenkins server
JENKINS_URL = "http://localhost:8080/"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

# GitHub repository and credentials
REPO_URL = 'https://github.com/pramodashrith/PY-PR31101986.git'
USERNAME = 'pramodashrith'
PASSWORD = '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'

# Function to get the list of Jenkins jobs
def get_jobs(job_name):
  config_url = f"{JENKINS_URL}/job/{job_name}/config.xml"
  response = requests.get(config_url, auth=(USERNAME, API_TOKEN))
  if response.status_code == 200:
      return response.text
  else:
      return None
  

# Function to backup the config.xml of a Jenkins job
def backup_job(name):
  url = '%s/job/%s/config.xml' % (SERVER, name)
  response = requests.get(url)
  if not response.ok:
    logging.error('Error getting job config: %s', url)
    return

  file_name = '%s.xml' % name
  with open(file_name, 'wb') as f:
    f.write(response.content)

# Function to commit the backup file to the git repo
def commit_file(file, message):
  repo = git.Repo(search_parent_directories=True)

  with open(file, 'rb') as f:
    repo.index.add(f)

  repo.index.commit(message)
  repo.push()

def main(job_name):
  jobs = get_jobs(job_name)
  for job in jobs:
    name = job['name']
    folder = job['folder']
    backup_file = os.path.join(folder, '%s.xml' % name)
    backup_job(name)
    commit_file(backup_file, 'Backup of job %s' % name)

if __name__ == '__main__':
  main()

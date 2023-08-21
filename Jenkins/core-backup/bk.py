import logging
import requests
import os
from github import Github

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Jenkins server
SERVER = 'http://localhost:8080'

# GitHub repository and credentials
REPO_URL = 'https://github.com/pramodashrith/PY-PR31101986.git'
USERNAME = 'pramodashrith'
PASSWORD = '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'

# Function to get the list of Jenkins jobs
def get_jobs():
  url = 'http://%s/api/json?pretty=true' % SERVER
  response = requests.get(url)
  data = response.json()
  return data['jobs']

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

def main():
  jobs = get_jobs()
  for job in jobs:
    name = job['name']
    folder = job['folder']
    backup_file = os.path.join(folder, '%s.xml' % name)
    backup_job(name)
    commit_file(backup_file, 'Backup of job %s' % name)

if __name__ == '__main__':
  main()

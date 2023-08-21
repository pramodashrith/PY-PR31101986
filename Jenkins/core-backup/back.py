import logging
import requests
import time
import datetime
import os

from github import Github

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Jenkins server and API token
SERVER = 'http://localhost:8080'
API_TOKEN = '1135a5c0ac6fdf89ac2b3107ef070ee2b1'
job_name = 'Testpipeline'
USERNAME = 'admin'

# GitHub repository and credentials
REPO_NAME = 'PY-PR31101986'
USERNAME = 'pramodashrith'
PASSWORD = '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'

# Function to get the list of Jenkins jobs
def get_jobs(job_name):
  config_url = f"{SERVER}/job/{job_name}/config.xml"
 # url = 'http://%s/api/json?pretty=true' % SERVER
  response = requests.get(config_url, auth=(USERNAME, API_TOKEN))

  #return data['jobs']

# Function to backup the configuration of a Jenkins job
def backup_job(name):
  url = f'{SERVER}/job/{job_name}/config.xml'
  #url = '%s/job/%s/config.xml' % (SERVER, name)
  response = requests.get(url, auth=(API_TOKEN, ''), stream=True)
  if not response.ok:
    logging.error('Error getting job config: %s', url)
    return

  with open(name + '.xml', 'wb') as output:
    for block in response.iter_content(2048):
      output.write(block)

# Function to commit the backup files to GitHub
def commit_backups():
  client = Github(USERNAME, PASSWORD)
  repo = client.get_repo(REPO_NAME)

  today = datetime.datetime.today()
  commit_message = 'Backup of Jenkins jobs on %s' % today.strftime('%Y-%m-%d')

  for file in [f for f in os.listdir('.') if f.endswith('.xml')]:
    repo.create_file(file, commit_message, open(file, 'rb'))

def main():
  jobs = get_jobs(job_name)
  for job in jobs:
    backup_job(job['name'])

  commit_backups()

if __name__ == '__main__':
  main()

import os
import requests
from jenkinsapi.jenkins import Jenkins
from github import Github
from git import Repo
from github import InputGitTreeElement

# Jenkins settings
jenkins_url = 'http://localhost:8080'
jenkins_username = 'admin'
jenkins_password = 'admin'
job_name = 'Testpipeline'

# GitHub settings
github_token = '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'
github_repo_owner = 'pramodashrith'
github_repo_name = 'PY-PR31101986'
github_repo_path = 'Jenkins/config-backup'  # For example, 'jenkins_backups'

# Connect to Jenkins
jenkins = Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
config_url = f'{jenkins_url}/job/{job_name}/config.xml'
# Make a GET request to the Jenkins API with authentication
response = requests.get(config_url, auth=(jenkins_username, jenkins_password))

# Check if the request was successful
if response.status_code == 200:
    config_xml = response.text
else:
    print(f"Failed to retrieve config.xml. Status code: {response.status_code}")
    exit(1)
# Get job's config.xml



# Create a temporary backup file
backup_file_path = 'config_backup.xml'
with open(backup_file_path, 'w') as backup_file:
    backup_file.write(config_xml)

# Connect to GitHub
github = Github(github_token)
repo = github.get_repo(f'{github_repo_owner}/{github_repo_name}')

# Create a commit in the GitHub repository
commit_message = f'Backup {job_name} config.xml'
with open(backup_file_path, 'rb') as backup_file:
    contents = backup_file.read()

# Create a new blob (file) in the repository
# blob = repo.create_git_blob(contents,'base64''base64')
blob = repo.create_git_blob("contents",'base64' 'utf-8')
# Create a new tree with the updated blob
element = InputGitTreeElement(github_repo_path + '/config.xml', '100644', 'blob', blob.sha)
tree = repo.create_git_tree([element])

# Get the parent commit
parent_commit = repo.get_branch('main').commit
repo.index.commit(element)
repo.push()

# Create the new commit
#commit = repo.create_git_commit("commit_message", tree, [parent_commit])
#repo.get_git_ref('heads/main').edit(commit.sha)

# Clean up the temporary backup file
os.remove(backup_file_path)

print(f'Backup of {job_name} config.xml created and committed to GitHub.')

import os
import git
import requests
from xml.etree import ElementTree as ET

# Define your Jenkins and GitHub repository information
jenkins_url = 'http://localhost:8080/'
jenkins_username = 'admin'
jenkins_password = 'admin'
github_token = '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'
github_repo_url = 'https://github.com/pramodashrith/PY-PR31101986.git'
workspace_path = 'Users/pramodashrith/.jenkins/jobs/config/jobs/Testpipeline'

# Function to get all job config.xml files recursively
def get_job_configs("Users/pramodashrith/.jenkins/jobs/config/jobs"):
    job_configs = []
    for root, _, files in os.walk('Users/pramodashrith/.jenkins/jobs/config/jobs'):
        for filename in files:
            if filename == 'config.xml':
                job_configs.append(os.path.join(root, filename))
    return job_configs

# Function to commit and push changes to GitHub
def commit_and_push_changes(repo, message):
    repo.index.add('*')
    repo.index.commit(message)
    repo.remote().push()

# Function to update job configurations in GitHub
def update_github_job_configs(job_configs):
    try:
        repo = git.Repo.clone_from(github_repo_url, '/tmp/github_repo')
    except git.exc.GitCommandError:
        repo = git.Repo('/tmp/github_repo')

    for config_path in job_configs:
        job_name = os.path.basename(os.path.dirname(config_path))
        github_path = f'jobs/{job_name}/config.xml'

        with open(config_path, 'r') as config_file:
            config_data = config_file.read()

        # Update the job configuration in the GitHub repository
        github_url = f'{github_repo_url}/contents/{github_path}'
        headers = {
            'Authorization': f'token {github_token}'
        }
        data = {
            'message': f'Update {job_name} job configuration',
            'content': config_data
        }

        response = requests.put(github_url, headers=headers, json=data)
        if response.status_code == 200:
            print(f'Successfully updated {job_name} job configuration in GitHub')
            commit_and_push_changes(repo, f'Update {job_name} job configuration')
        else:
            print(f'Failed to update {job_name} job configuration in GitHub')
            print(f'Response: {response.status_code}, {response.text}')

if __name__ == '__main__':
    job_configs = get_job_configs(workspace_path)

    if not job_configs:
        print('No job configurations found in the workspace.')
    else:
        update_github_job_configs(job_configs)

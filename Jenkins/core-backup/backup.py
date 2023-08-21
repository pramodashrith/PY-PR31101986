import os
import requests
import github



# Jenkins API URL and credentials
jenkins_url = 'http://localhost:8080'
username = 'admin'
password = 'admin'

# Directory to store job configurations
output_dir = 'job_configs'

# Clone or open the Git repository
repo_path = 'https://github.com/pramodashrith/PY-PR31101986.git'
repo = git.Repo(repo_path)

# Get list of Jenkins jobspyt
jobs_url = f'{jenkins_url}/api/json'
response = requests.get(jobs_url, auth=(username, password))
jobs = response.json()['jobs']

# Iterate through jobs
for job in jobs:
    job_name = job['name']
    job_url = f'{jenkins_url}/job/{job_name}/config.xml'
    response = requests.get(job_url, auth=(username, password))
    job_config = response.text

    # Store job configuration as a file
    job_filename = os.path.join(output_dir, f'{job_name}_job.xml')
    with open(job_filename, 'w') as f:
        f.write(job_config)

    # Add and commit to Git repository
    repo.git.add(job_filename)
    repo.git.commit(m=f'Updated {job_name} job.xml')

# Push changes to Git repository
repo.git.push('origin', 'main')
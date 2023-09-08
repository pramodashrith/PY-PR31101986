import os
import requests
from jenkinsapi.jenkins import Jenkins

jenkins_url = "http://localhost:8080"
output_dir = 'config-bk'
artifact_path = os.makedirs(output_dir, exist_ok=True)
username = "admin"
password = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"
# Jenkins server URL
job_name = 'configlist'

# Connect to the Jenkins server
jenkins = Jenkins(jenkins_url, username=username, password=password)
job_names = jenkins.keys()
# Use Jenkins API to list artifacts in the desired directory
api_url = f"{jenkins_url}/job/{job_name}/lastBuild/api/json?tree=artifacts[*]"
response = requests.get(api_url)
data = response.json()

# Download each artifact
for artifact in data['artifacts']:
    artifact_name = artifact['fileName']
    artifact_url = f"{jenkins_url}/job/{job_name}/lastBuild/artifact/{artifact_path}/{artifact_name}"
    destination_path = os.path.join('/path/to/destination', artifact_name)

    # Download the artifact
    response = requests.get(artifact_url)
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {artifact_name}")
    else:
        print(f"Failed to download: {artifact_name}")

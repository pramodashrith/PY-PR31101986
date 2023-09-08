from jenkinsapi.jenkins import Jenkins
import os
import shutil


# Jenkins server configuration
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

# Connect to Jenkins
jenkins = Jenkins(JENKINS_URL, username=USERNAME, password=API_TOKEN)

# Get a list of all jobs
all_jobs = jenkins.keys()

def jenkins_list():
    cloned = os.environ.get('CLONED_REPO_PATH')
    folder_name = 'config'
    for job_name in all_jobs:
        job = jenkins.get_job(job_name)
        config_xml = job.get_config()
        config_url = f"{JENKINS_URL}/job/{folder_name}/job/{job_name}/config.xml"
        print(f"Folder Name: {folder_name}")
        print(f"Job Name: {job_name}")
        print(f"Config URL: {config_url}")
        print("-" * 40)
        job_url = job.baseurl
        workspace_url = f'{job_url}/ws/'
        config_xml_filename = 'config_xml'
        for root, dirs, files in os.walk(cloned):
            for file in files:
                if file == config_xml_filename:
                    config_path = os.path.join(root, file)
                    print(config_path)
                    for job_name in config_path:
                        job = jenkins.get_job(job_name)
                        conffig = job.get_config()
                        config_url = f"{JENKINS_URL}/job/{folder_name}/job/{job_name}/config.xml"
                    shutil.copy(config_path, os.path.join(cloned, config_path[len(workspace_url) +1:]))
                    files = os.listdir(cloned)
                    for file in files:
                        print(file)

if __name__ == "__main__":
    jenkins_list()
        
import requests
from api4jenkins import Jenkins


# Jenkins server information
JENKINS_URL = "http://localhost:8080"
username = "admin"
password = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

# GitHub repository and authentication
github_token = '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'
repo_name = 'PY-PR31101986'
branch_name = 'test'

jenkins = Jenkins('http://localhost:8080', auth=('admin', 'admin'))




def iter_jobs(depth=15):
    j = Jenkins('JENKINS_URL', auth=('username', 'password'))
    for job in j.iter_jobs():
        print(job)
        folder = j.Folder(JENKINS_URL)
        yield from folder.iter(depth)

def list_job_configs_in_folder(folder_name):
    folder_url = f"{JENKINS_URL}/job/{folder_name}/api/json?tree=jobs[name]"
    response = requests.get(folder_url, auth=(username, password))
    iter_jobs(depth=15)
    j = Jenkins('http://127.0.0.1:8080/', auth=('admin', 'admin'))
    for job in j.iter_jobs(depth=8):
        print(job)
    if response.status_code == 200:
        job_data = response.json()
        for job in job_data["jobs"]:
            if job["_class"] == "com.cloudbees.hudson.plugins.folder.Folder":
            # If it's a folder, recursively list jobs inside it
               print("hello") 
        else:
            # It's a job, retrieve its config.xml content
            job_name = job["name"]
            config_xml = j.get_job(job_name)
            # Process the config.xml content as needed
            print(f"Job: {job_name}\nConfig.xml:\n{config_xml}\n")
        for job in j.iter_jobs(depth=8):
            for job in job_data["jobs"]:
                job_name = job["name"]
                config_url = f"{JENKINS_URL}/job/{folder_name}/job/{job_name}/config.xml"
                print(f"Folder Name: {folder_name}")
                print(f"Job Name: {job_name}")
                print(f"Config URL: {config_url}")
                print("-" * 40)
    else:
        print(f"Failed to retrieve jobs in folder: {folder_name}")

def list_job_configs_outside_folder():
    
    
    
    folder_list_url = f"{JENKINS_URL}/api/json?tree=jobs[name]"
    response = requests.get(folder_list_url, auth=(username, password))
    if response.status_code == 200:
        folder_data = response.json()
        for folder in folder_data["jobs"]:
            folder_name = folder["name"]
            
            list_job_configs_in_folder(folder_name)
            #list_jobs_recursive(folder_name)
            
            print("=" * 60)
    else:
        print("Failed to retrieve folder list")

if __name__ == "__main__":
    iter_jobs(depth=15)
    list_job_configs_outside_folder()

import requests

# Jenkins server information
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"



def list_job_configs_in_folder(folder_name):
    folder_url = f"{JENKINS_URL}/job/{folder_name}/api/json?tree=jobs[name]"
    response = requests.get(folder_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        job_data = response.json()
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
    response = requests.get(folder_list_url, auth=(USERNAME, API_TOKEN))
    if response.status_code == 200:
        folder_data = response.json()
        for folder in folder_data["jobs"]:
            folder_name = folder["name"]
            list_job_configs_in_folder(folder_name)
            print("=" * 60)
    else:
        print("Failed to retrieve folder list")

if __name__ == "__main__":
    list_job_configs_outside_folder()

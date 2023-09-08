from jenkinsapi.jenkins import Jenkins

# Jenkins server configuration
JENKINS_URL = "http://localhost:8080"
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"

# Connect to Jenkins
jenkins = Jenkins(JENKINS_URL, username=USERNAME, password=API_TOKEN)

# Get a list of all jobs
all_jobs = jenkins.keys()

# Filter out jobs that are inside the "my-folder" folder
ignored_folder = "test"
filtered_jobs = [job for job in all_jobs if not job.startswith(ignored_folder + '/')]

# Now you can proceed with retrieving and processing the config.xml for the remaining jobs
for job_name in filtered_jobs:
    job = jenkins.get_job(job_name)
    config_xml = job.get_config()
    # Process the config.xml as needed
    print(f"Job: {job_name}\nConfig.xml:\n{config_xml}\n")

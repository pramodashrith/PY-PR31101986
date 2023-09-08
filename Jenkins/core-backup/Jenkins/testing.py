import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import os
import shutil


username = "admin"
password = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"
# Jenkins server URL
jenkins_url = "http://localhost:8080"
jenkins_workspace_path = os.environ.get('WORKSPACE')
# Connect to the Jenkins server
jenkins = Jenkins(jenkins_url, username=username, password=password)

# Get all job names
job_names = jenkins.keys()

# Create a directory to store the config.xml files
output_dir = 'config_xml_files'
# Get the absolute path of the output directory
output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Iterate through the jobs and get their config.xml
for job_name in job_names:
    job = jenkins[job_name]
    config_xml = job.get_config()
    config_url = job.url
    config_response = job.get_config()
    
    if config_response:
        config_xml = config_response
    
    
    job_dir = os.path.join(output_dir, job_name)
    os.makedirs(job_dir, exist_ok=True)
    
    
    # Save the config.xml content to a file
    config_file_path = os.path.join(output_dir, f'{job_name}_config.xml')

    with open(config_file_path, 'wb') as config_file:
        config_file.write(config_xml.encode('utf-8'))

    config_files = [file for file in os.listdir(jenkins_workspace_path) if file.endswith('.xml')]
    for config_file in config_files:
        # Determine the job folder containing the config.xml file
        job_folder = os.path.dirname(config_file)
        
        # Copy the entire job folder (including parent folders) to config_xml_files
        source_job_folder = os.path.join(jenkins_workspace_path, job_folder)
        dest_job_folder = os.path.join(output_dir, job_folder)
        shutil.copytree(source_job_folder, dest_job_folder)

        # Optionally, copy the config.xml file to the job folder within config_xml_files
        source_config_file = os.path.join(jenkins_workspace_path, config_file)
        dest_config_file = os.path.join(dest_job_folder, config_file)
        shutil.copy(source_config_file, dest_config_file)
        print(f"Downloaded {job_name}_config.xml")

    print("All config.xml files downloaded successfully.")

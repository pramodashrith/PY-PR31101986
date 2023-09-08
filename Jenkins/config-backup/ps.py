from __future__ import print_function
from jenkinsapi.jenkins import Jenkins
USERNAME = "admin"
API_TOKEN = "1135a5c0ac6fdf89ac2b3107ef070ee2b1"
jenkins = Jenkins("http://localhost:8080", username=USERNAME , password=API_TOKEN)
jobName = jenkins.keys()[4]  # get the first job

config = jenkins[jobName].get_config()

print(config)
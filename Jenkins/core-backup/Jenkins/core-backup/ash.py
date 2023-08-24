import os
import shutil
import subprocess

def get_all_jobs_config_xml(jenkins_workspace):
  """Get all jobs config.xml in Jenkins workspace."""
  jobs_config_xml = []
  for root, directories, files in os.walk(jenkins_workspace):
    for file in files:
      if file.endswith("config.xml"):
        jobs_config_xml.append(os.path.join(root, file))
  return jobs_config_xml

def add_commit_push_github(jobs_config_xml, github_repo_url, github_username, github_password):
  """Add, commit and push all jobs config.xml to GitHub repo."""
  for jobs_config_xml in jobs_config_xml:
    subprocess.run(["git", "add", jobs_config_xml])
    subprocess.run(["git", "commit", "-m", "Add job config.xml"])
    subprocess.run(["git", "push", "https://{github.com}:{pramodashrith}@{PY-PR31101986}".format(github_username, github_password, github_repo_url)])

def main():
  jenkins_workspace = "Users/pramodashrith/.jenkins/jobs"
  github_repo_url = "https://github.com/pramodashrith/PY-PR31101986"
  github_username = "pramodashrith"
  github_password = "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"

  jobs_config_xml = get_all_jobs_config_xml(jenkins_workspace)
  add_commit_push_github(jobs_config_xml, github_repo_url, github_username, github_password)

if __name__ == "__main__":
  main()

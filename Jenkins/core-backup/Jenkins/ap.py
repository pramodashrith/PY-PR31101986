from github import Github

# Replace with your GitHub personal access token
GITHUB_TOKEN = "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"

# Replace with the owner (username or organization) and name of the repository
REPO_OWNER = "pramodashrith"
REPO_NAME = "PY-PR31101986"

# Path to the folder in the repository where backups will be committed
FOLDER_PATH = "Jenkins/core-backup"

# Initialize a Github object with your token
g = Github(GITHUB_TOKEN)

# Get the repository using the owner and name
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

def commit_file(file_path, file_content, commit_message):
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, file_content, contents.sha)
        print(f"File {file_path} updated successfully.")
    except Exception as e:
        print(f"Error updating file {file_path}: {e}")

def backup_job_config(job_name, backup_file_path):
    # Retrieve job config.xml content (replace with your method to get config.xml)
    config_xml = f"Job configuration XML for {job_name}"

    # Save config.xml to a file
    with open(backup_file_path, "w") as backup_file:
        backup_file.write(config_xml)

def main():
    job_name = "configlist"  # Replace with your job name
    backup_file_name = f"{job_name}_config.xml"
    backup_file_path = f"/Users/pramodashrith/.jenkins/jobs/config/jobs/configlist/{backup_file_name}"  # Replace with your local backup path

    # Backup job config.xml
    backup_job_config(job_name, backup_file_path)

    # Read backup file content
    with open(backup_file_path, "r") as backup_file:
        backup_content = backup_file.read()

    # Commit backup to GitHub
    commit_message = f"Backup of {job_name} config.xml"
    commit_file(FOLDER_PATH + "/" + backup_file_name, backup_content, commit_message)

if __name__ == "__main__":
    main()

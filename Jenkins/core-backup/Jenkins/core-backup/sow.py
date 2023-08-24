import git
import os

# Replace with your GitHub repository URL, branch name, and file path
github_repo_url = 'https://github.com/pramodashrith/PY-PR31101986.git'
branch_name = 'test'
file_path = 'Jenkins/core-backup'

# Function to commit and push changes to GitHub
def commit_and_push_changes(repo, message):
    repo.index.add([file_path])
    repo.index.commit(message)
    repo.remotes.origin.push(refspec=f'refs/heads/{branch_name}')

if __name__ == '__main__':
    try:
        # Clone the GitHub repository if it doesn't exist locally
        repo = git.Repo.clone_from(github_repo_url, '/tmp/github_repo')
    except git.exc.GitCommandError:
        repo = git.Repo('/tmp/github_repo')

    # Copy your updated config.xml file to the repository directory
    # This assumes your config.xml file is located at file_path
    updated_file_path = os.path.join(repo.working_tree_dir, file_path)

    # Modify or replace the updated_file_path as needed

    # Commit and push the changes to the specified branch
    commit_message = 'Update config.xml'
    commit_and_push_changes(repo, commit_message)

    print(f'Successfully committed and pushed {file_path} to {branch_name} branch in GitHub.')

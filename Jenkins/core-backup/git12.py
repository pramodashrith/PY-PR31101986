from sre_constants import BRANCH
import git

clone_url = "https://github.com/pramodashrith/PY-PR31101986.git"
clone_path = '/Users/pramodashrith'
branch = "test"
data = git.Repo.clone_from(clone_url,clone_path,branch)
git.Repo.push(data)
print(data)
import os
import dulwich.porcelain as porcelain
from dulwich.repo import Repo

repo_path = r"C:\Smart-Hostel-Mess"

# 1. Initialize Git repository
if not os.path.exists(os.path.join(repo_path, ".git")):
    repo = porcelain.init(repo_path)
    print("Initialized empty Git repository.")
else:
    repo = Repo(repo_path)
    print("Found existing Git repository.")

# 2. Stage all files
# We stage files respecting .gitignore
files_to_add = []
for root, dirs, files in os.walk(repo_path):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        rel_path = os.path.relpath(os.path.join(root, f), repo_path)
        files_to_add.append(rel_path)

porcelain.add(repo_path, paths=files_to_add)
print(f"Staged {len(files_to_add)} files.")

# 3. Commit
try:
    commit_sha = porcelain.commit(
        repo_path,
        message=b"Initial commit: Smart Hostel Mess Management System with SQLite database, Flask backend, and weekly menu images",
        author=b"khatalprachi9 <khatalprachi9@users.noreply.github.com>",
        committer=b"khatalprachi9 <khatalprachi9@users.noreply.github.com>"
    )
    print(f"Committed successfully! SHA: {commit_sha.decode('ascii') if isinstance(commit_sha, bytes) else commit_sha}")
except Exception as e:
    print(f"Commit note: {e}")

# 4. Set remote
config = repo.get_config()
remote_url = b"https://github.com/khatalprachi9-lab/Smart-Hostel-Mess-Management-System.git"
config.set((b"remote", b"origin"), b"url", remote_url)
config.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
config.write_to_path()
print(f"Configured remote 'origin' -> {remote_url.decode('utf-8')}")

print("\nGit repository initialized and committed locally.")


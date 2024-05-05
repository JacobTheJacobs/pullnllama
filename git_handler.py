import os
import subprocess
from pathlib import Path

class GitHandler:
    def __init__(self, repo_link):
        self.repo_link = repo_link
        self.pr_id = repo_link.split("/")[-1]
        self.repo_name = repo_link.split("/")[-3]
        self.repo_owner = repo_link.split("/")[-4]
        self.branch = "pr"
        self.pr_number = self.get_pr_number_from_link()
        self.repo_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"


    def clone_or_pull_repo(self):
        if Path(self.repo_name).is_dir():
            os.chdir(self.repo_name)
            subprocess.run(["git", "checkout", "main"], check=True)
            subprocess.run(["git", "pull"], check=True)
        else:
            subprocess.run(["git", "clone", self.repo_url], check=True)
            os.chdir(self.repo_name)


    def fetch_pr(self):
        subprocess.run(["git", "fetch", "origin", f"pull/{self.pr_id}/head:{self.branch}"], check=True)
        subprocess.run(["git", "checkout", self.branch], check=True)


    def get_diff(self):
        diff = subprocess.run(["git", "diff", "main"], check=True, text=True, capture_output=True)
        if diff.returncode != 0:
            print("Error: git diff command failed")
            return None
        file_names = self.split_diff(diff.stdout)
        diffs = []
        for file_name in file_names:
            with open(file_name, 'r') as f:
                diffs.append(f.read())
        diff_string = '\n'.join(diffs)
        return diff_string


    def get_latest_commit_id(self):
        result = subprocess.run(["git", "rev-parse", self.branch], check=True, text=True, capture_output=True)
        if result.returncode != 0:
            print("Error: git rev-parse command failed")
            return None
        return result.stdout.strip()



    def get_pr_number_from_link(self):
        pr_number = self.repo_link.split("/")[-1]
        if pr_number.isdigit():
            return int(pr_number)
        else:
            print("Error: Invalid pull request link")
            return None
        
        
    def split_diff(self, diff):
        lines = diff.split('\n')
        current_file = None
        file_names = []
        for line in lines:
            if line.startswith('diff --git'):
                if current_file is not None:
                    current_file.close()
                filename = line.split(' ')[2]
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                current_file = open(f'{filename}.diff', 'w')
                file_names.append(f'{filename}.diff')
            if current_file is not None:
                current_file.write(line + '\n')
        if current_file is not None:
            current_file.close()
        return file_names
                

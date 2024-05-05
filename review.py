import re
import requests
import os

class ReviewHandler:
    @staticmethod
    def get_line_number_from_diff(diff):
        match = re.search(r"@@ -\d+,\d+ \+(\d+),\d+ @@", diff)
        return int(match.group(1)) if match else None

    @staticmethod
    def get_line_numbers_from_response(response):
        try:
            matches = re.findall(r"Line (\d+):", response.text)
            return [int(match) for match in matches] if matches else None
        except Exception as e:
            print("Error:", e)
            return None

    @staticmethod
    def create_pr_review(repo_owner, repo_name, pr_number, review_body, commit_id, event, comments):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/reviews"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
        }
        data = {
            "body": review_body,
            "commit_id": commit_id,
            "event": event,
            "comments": comments
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("PR review created successfully.")
        else:
            print("Failed to create PR review:", response.text)

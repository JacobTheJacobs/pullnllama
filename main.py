from git_handler import GitHandler
from review import ReviewHandler
from ollama_send import OllamaSender

def main():
    
    github_url = ""

    parts = github_url.split("/")
    repo_owner = parts[-4]
    repo_name = parts[-3]
    pr_id = parts[-1]

    git = GitHandler(github_url)

    git.clone_or_pull_repo()

    git.fetch_pr()

    diffs = git.get_diff()

    print(diffs)

    commit_id = git.get_latest_commit_id()
    ollama = OllamaSender()

    res = ollama.send_to_ollama(diffs)
    
    print(res)

    line_numbers = ReviewHandler.get_line_numbers_from_response(res)

    if not line_numbers:
        line_numbers = [ReviewHandler.get_line_number_from_diff(diffs)]

    comments = [{"path": "main.py", "position": 4, "body": res}]

    ReviewHandler.create_pr_review(repo_owner, repo_name, pr_id,
                                   "llama3", commit_id, "COMMENT", comments)

if __name__ == "__main__":
    main()

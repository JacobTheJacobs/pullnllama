import asyncio
import argparse
from git_handler import GitHandler
from ollama_send import OllamaSender
from graph_rag import SimpleGraphRAG

def main():
    parser = argparse.ArgumentParser(description="PR Review via Ollama with Graph RAG")
    parser.add_argument("--repo-url", required=True, help="URL of the repository")
    parser.add_argument("--branch", required=True, help="Branch name of the PR")
    parser.add_argument("--path", required=True, help="Local path to store/clone repo")
    args = parser.parse_args()

    handler = GitHandler(args.repo_url, args.branch, args.path)
    handler.clone_or_pull_repo()
    handler.fetch_pr()
    
    diffs, file_names = handler.get_diff()
    print(f"Number of files to review: {len(diffs)}")
    
    # Init Graph RAG to build context mapping across the PR diffs
    graph_rag = SimpleGraphRAG()
    graph_rag.build_graph_from_diffs(diffs, file_names)

    async def send_diffs():
        sender = OllamaSender()
        responses = []
        for i, (diff, fname) in enumerate(zip(diffs, file_names), 1):
            print(f"------------------- {i * 100 / len(diffs):.2f}% -------------------")
            print(f"Reviewing {fname} with Ollama...")
            
            # Retrieve RAG context and inject into the payload
            context = graph_rag.retrieve_context(fname)
            print(f"Injected RAG Context: {context}")
            
            response = await sender.send_to_ollama(diff, fname, context)
            responses.append((fname, response))
        return responses

    results = asyncio.run(send_diffs())
    
    with open('ollama_results.txt', 'w') as f:
        for fname, response in results:
            print("=" * 80)
            print(f"Review for {fname}:")
            print(response)
            
            f.write("=" * 80 + "\n")
            f.write(f"File: {fname}\n")
            f.write("-" * 80 + "\n")
            f.write(response + "\n")

if __name__ == "__main__":
    main()

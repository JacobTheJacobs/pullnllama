import requests
import json
import asyncio
from git_handler import GitHandler
from ollama import OllamaSender



handler = GitHandler("https://github.com/X/Y/pull/Z", "branch_name", "path\\to\\repo\\download\\folder")

handler.clone_or_pull_repo()
handler.fetch_pr()
diffs = handler.get_diff()
c = 0

for i in diffs:
    c += 1
    
print("Number of files: ", c)
response = []
async def send_diffs():
    i = 0
    for d in diffs:
        i += 1
        print(i * 100 / c, "%")
        print("send_to_ollama started")
        response.append(await OllamaSender().send_to_ollama(d))
        print('send_to_ollama finished')

asyncio.run(send_diffs())
for i in response:
    print(i)
    print("--------------------------------------------------------------------")

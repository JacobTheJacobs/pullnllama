import requests
import json
import asyncio
from git_handler import GitHandler
from ollama import OllamaSender

handler = GitHandler("https://github.com/X/Y/pull/Z", "branch_name", "path\\to\\repo\\download\\folder")

handler.clone_or_pull_repo()
handler.fetch_pr()
diffs, file_names = handler.get_diff()
c = 0

for i in diffs:
    c += 1
    
print("Number of files: ", c)
response = []
async def send_diffs():
    i = 0
    for d, f in zip(diffs, file_names):
        i += 1
        print("-------------------",i * 100 / c, "%","-------------------")
        print("send_to_ollama started")
        print("Diff file name: ", f) 
        response.append(await OllamaSender().send_to_ollama(d))
        print('send_to_ollama finished')

asyncio.run(send_diffs())

with open('ollama_results.txt', 'w') as file:
    for i in response:
        #
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write(str(i) + '\n')
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("----------------------------------------------------------------------------------------------------------------------------------------\n")

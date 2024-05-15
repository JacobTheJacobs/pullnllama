import aiohttp
import asyncio
import json

class OllamaSender:
    def __init__(self, model="llama3"):
        self.system_prompt = """Review the pull request diff. Assess code quality, readability, performance, and security. Check the documentation and test coverage to ensure they are thorough. Provide constructive feedback on alignment with project goals, suggesting improvements and optimizations where needed, all in a supportive and positive tone. be short and concise."""
        self.model = model

    async def send_to_ollama(self, diff):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model, 
            "prompt": self.system_prompt + diff,    
            "stream": False,     
            "temperature": 0.5   
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:8081/api/generate", headers=headers, json=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        actual_response = (data["response"])
                        print(actual_response)
                        return actual_response
                    else:
                        text = await response.text()
                        print("Error:", text)
                        raise Exception('Failed to get a valid response from the model.')
        except Exception as e:
            print(e)
            return None

import aiohttp
import json

class OllamaSender:
    def __init__(self, model: str = "llama3"):
        self.system_prompt = (
            "Review the pull request diff below. Assess code quality, readability, "
            "performance, and security. Consider the architectural graph context provided. "
            "Be short, concise, supportive, and constructive."
        )
        self.model = model
        # Typically Ollama runs on port 11434, the old code used 8081. I will use standard or user's. 
        self.api_url = "http://localhost:11434/api/generate"

    async def send_to_ollama(self, diff: str, filename: str, graph_context: str) -> str:
        headers = {"Content-Type": "application/json"}
        prompt_augmented = f"{self.system_prompt}\n\nFile Under Review: {filename}\n{graph_context}\n\nDiff Content:\n{diff}"
        
        data = {
            "model": self.model, 
            "prompt": prompt_augmented,    
            "stream": False,     
            "temperature": 0.3   
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.api_url, headers=headers, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            return result.get("response", "")
                        else:
                            text = await response.text()
                            print(f"Error {response.status}: {text}")
                            
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    return f"Failed to get review for {filename} after {max_retries} attempts."
        return ""

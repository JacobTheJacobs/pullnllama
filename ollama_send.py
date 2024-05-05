import requests
import json

class OllamaSender:
    def __init__(self, model="llama3"):
        self. system_prompt = """Review the pull request titled "[Title]" which aims to [Objective]. Assess code quality, readability, performance, and security. Check the documentation and test coverage to ensure they are thorough. Provide constructive feedback on alignment with project goals, suggesting improvements and optimizations where needed, all in a supportive and positive tone."""
        self.model = model

    def send_to_ollama(self, diff):
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
            response = requests.post("http://localhost:11434/api/generate", headers=headers, json=data)
            if response.status_code == 200:
                response_text = response.text
                data = json.loads(response_text)
                actual_response = (data["response"])
                return actual_response
            else:
                print("Error:", response.text)
                raise Exception('Failed to get a valid response from the model.')
        except Exception as e:
            print(e)
            return None






    

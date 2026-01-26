from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

import os
import requests
import json
from deepeval.models import GPTModel
from deepeval.models.base_model import DeepEvalBaseLLM

from ollama import Client as Ollama

class OllamaJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="llama3"):
        self.model = Ollama(model=model_name)

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt)

    async def a_generate(self, prompt: str) -> str:
        return self.model.invoke(prompt)

    def get_model_name(self):
        return "Ollama Llama3"
    
class LoanAI:
    def __init__(self, model_name ="llama3"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        print(f"Initilaize LoanAI model by {model_name}...OK")

    def ask(self, prompt: str, system_prompt: str) -> str:
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, json=payload)

            if response.status_code == 200:
                return response.json().get("response", "'")
            else:
                return f"Error: Response code {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

class OpenRouterJudge:
    def __init__(self, model_id, key_file="API_Keys.txt"):
        self.model_id = model_id
        self._setup_env(key_file)
        self.model_instance = GPTModel(model=self.model_id)

    def _setup_env(self, key_file):
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

        base_path = os.path.dirname(os.path.abspath(__file__))
        key_file_path = os.path.join(base_path, "API_Keys.txt")

        try:
            with open(key_file_path) as f:
                api_key = f.read().strip()
            os.environ["OPENAI_API_KEY"] = api_key
            
        except FileNotFoundError:
            print(f" Error: Cannot find key at {key_file_path}")

    def get_model(self):
        return self.model_instance

def test_loan_rejection():
    loan_ai = LoanAI()
    # judge_model = OpenRouterJudge(model_id="google/gemini-2.0-flash-exp:free") #overload model
    # judge_model = OpenRouterJudge(model_id="allenai/molmo-2-8b:free")
    judge_model = OpenRouterJudge(model_id="xiaomi/mimo-v2-flash:free")
    
    user_input = "Can I get a loan with 650?"
    system_prompt = "You are a strict bank loan officer. Only approve loans for people with credit scores above 700. Answer briefly (about 20 words)"
    
    actual_output = loan_ai.ask(
        system_prompt=system_prompt,
        prompt=user_input
    )

    print (f"actual result {actual_output}")
    
    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output,
        retrieval_context=["Policy: Minimum score is 700."]
    )

    metric = FaithfulnessMetric(
        model=judge_model.get_model(),
        threshold=0.7
    )
    
    assert_test(test_case, [metric])
    print(f"Reason from judge mode:  {metric.reason}")
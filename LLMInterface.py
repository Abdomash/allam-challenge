import requests
from abc import ABC, abstractmethod
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class LLM_Interface(ABC):
    @abstractmethod
    def generate(self, prompt, **kwargs) -> str:
        pass

BASE_URL = "https://eu-de.ml.cloud.ibm.com/ml/"
class ALLAM(LLM_Interface):
    def __init__(self, API_KEY):
        self.model_id = "sdaia/allam-1-13b-instruct"
        self.project_id = "0a443bde-e9c6-41dc-b1f2-65c6292030e4"

        # get authentication token
        authenticator = IAMAuthenticator(API_KEY)
        token = authenticator.token_manager.get_token()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        # set default parameters
        self.parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 30,
            "temperature": 1,
            "top_k": 50,
            "top_p": 1,
            "repetition_penalty": 2,
        }

    def generate(self, prompt, **kwargs):
        url = BASE_URL + "v1/text/generation?version=2024-08-30"
        self.body = {
            "input": f"<s> [INST] {prompt} [/INST]",
            "model_id": self.model_id,
            "project_id": self.project_id,
            "parameters": self.parameters
        }

        response = requests.post(url, headers=self.headers, json=self.body)
        response.raise_for_status()
        
        data = response.json()
        return data['results'][0]['generated_text']
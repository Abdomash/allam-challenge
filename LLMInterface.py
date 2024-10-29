import random
import requests
import itertools

from Data import load_qafiyas, load_poets, load_bohours

from abc import ABC, abstractmethod
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

BASE_URL = "https://eu-de.ml.cloud.ibm.com/ml/"

class OpenAI_Generator:
    def __init__(self, API_KEY):
        pass

    def generate(self, prompt):
        pass


BAYT_SEPARATORS = ["\n", "*", "#", '/', '.']

class ALLAM_GENERATOR:
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
            "max_new_tokens": 15,
            "min_new_tokens": 5,
            "temperature": 0.5,
            "top_k": 40,
            #"top_p": 0.5,
            "repetition_penalty": 1.25,
            "stop_sequences": BAYT_SEPARATORS,
        }
        self.critic_parameters = {
            "decoding_method": "greedy",
            "stop_sequences": ["\n"],
        }

    def generate(self, prompt, is_critic=False):
        url = BASE_URL + "v1/text/generation?version=2024-08-30"
        body = {
            "input": prompt,
            "model_id": self.model_id,
            "project_id": self.project_id,
            "parameters": self.critic_parameters if is_critic else self.parameters
        }
        
        response = requests.post(url, headers=self.headers, json=body)
        response.raise_for_status()
        
        data = response.json()
        return data['results'][0]['generated_text']
    

# A fake LLM for testing
class FakeGenerator:
    def __init__(self, poet=None, wazn=None, qafiya=None):
        self.poets = load_poets()
        self.bohours = load_bohours()
        self.qafiyas = load_qafiyas()

        if poet: # in arabic
            if poet not in self.poets.keys():
                raise ValueError(f"Poet not found in database: Could not find {poet} in 'poet.json'")
            self.poet = self.poets[poet]
        else:
            # self.poet = self.poets[random.choice(list(self.poets.keys()))]
            self.poet = self.poets["المتنبي"]

        if wazn: # in arabic
            if wazn not in self.bohours.keys():
                raise ValueError(f"Bahr not found in database: Could not find {wazn} in 'bohours.json'")
            if not poet: 
                # self.poet = self.poets[random.choice(list(self.poets.keys()))]
                self.poet = self.poets["المتنبي"]
            try:
                self.poems = self.poet['poems'][self.bohours[wazn]['name_en']]
            except KeyError:
                print(f"Poet {self.poet['name']} does not have any poems in {wazn}")
                self.poems = random.choice(list(self.poet['poems'].values()))
        else:
            self.poems = random.choice(list(self.poet['poems'].values()))

        if qafiya:
            # TODO: Implement this
            pass

        # cycle through the poem lines infinitely
        self.poem = itertools.cycle(random.choice(self.poems))

    def generate(self, prompt=None):
        return next(self.poem)
from abc import ABC, abstractmethod
from ibm_watsonx_ai.foundation_models import Model

class LLM_Interface(ABC):
    @abstractmethod
    def generate(self, prompt, extra_info=None):
        pass

class ALLAM(LLM_Interface):
    def __init__(self, API_KEY):
        self.url = "https://eu-de.ml.cloud.ibm.com"
        model_id = "sdaia/allam-1-13b-instruct"
        project_id = "0a443bde-e9c6-41dc-b1f2-65c6292030e4"
        parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 200,
            "temperature": 1,
            "top_k": 50,
            "top_p": 1,
            "repetition_penalty": 1.5,
        }
        self.model = Model(
            model_id = model_id,
            params = parameters,
            credentials = API_KEY,
            project_id = project_id,
        )

    
    def generate(self, prompt, extra_info=None):
        generated_response = self.model.generate_text(
            prompt=prompt,
            guardrails=False,
            raw_response=False,
            params={"return_options":
                    {"input_text": True,
                     "generated_tokens": True,
                     "input_tokens": True,
                     "token_logprobs":False,
                     "top_n_tokens":5
                     }})

        return generated_response['results'][0]['generated_text']
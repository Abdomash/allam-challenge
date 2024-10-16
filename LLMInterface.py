import requests
from abc import ABC, abstractmethod
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

BASE_URL = "https://eu-de.ml.cloud.ibm.com/ml/"

class LLM_INTERFACE_GENERATOR(ABC):
    @abstractmethod
    def generate(self, prompt) -> str:
        pass

class ALLAM_GENERATOR(LLM_INTERFACE_GENERATOR):
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
            "temperature": 1.5,
            "top_k": 40,
            #"top_p": 1.0,
            "repetition_penalty": 1.25,
            "stop_sequences": ["\n"],
        }

    def generate(self, prompt):
        url = BASE_URL + "v1/text/generation?version=2024-08-30"
        self.body = {
            "input": prompt,
            "model_id": self.model_id,
            "project_id": self.project_id,
            "parameters": self.parameters
        }

        response = requests.post(url, headers=self.headers, json=self.body)
        response.raise_for_status()
        
        data = response.json()
        return data['results'][0]['generated_text']
    

# A fake LLM for testing
class FakeGenerator(LLM_INTERFACE_GENERATOR):
    def __init__(self):
        self.i = 0
        self.lines = ['وَهَمُ الْكِرَامُ بَنُو الْخَضَارِمَةِ الْعُلا', 'أَفَبَعْدَ كِنْدَةَ تَمْدَحَنَّ قَبِيلا', 'قُم لِلمُعَلِّمِ وَفِّهِ التَبجيلا', 'لِسَمَيْدَعٍ أَكْرِمْ بِذَاكَ نَجِيلا', 'يَا أَيُّها السَّاعِي لِيُدْرِكَ مَجْدَنَا', 'ثَكِلَتْكَ أُمُّكَ هَلْ تَرُدُّ قَتِيلا', 'هَلْ تَرْقَيَنَّ إلى السَّماءِ بِسُلَّمٍ', 'وَلَتَرْجِعَنَّ إلى العَزِيزِ ذَلِيلا', 'سَائِلْ بَنِي مَلِكِ المُلُوكِ إذا الْتَقَوا', 'عَنَّا وَعَنْكُمْ لا تَعَاشَ جَهُولا', 'مِنَّا الذي مَلِكَ المَعَاشِرَ عَنْوَةً', 'مَلَكَ الفَضَاءَ فَسَلْ بِذَاك عُقُولا', 'وَبَنُوهُ قَدْ مَلَكُوا خِلافَةَ مُلْكِهِ', 'شُبَّانَ حَرْبٍ سَادَةً وَكُهُولا', 'قالوا لَهُ : هَلْ أنتَ قَاضٍ ما تَرَى', 'إِنَّا نَرَى لَكَ ذا المَقَامَ قَلِيلا', 'فَقَضَى لكلِّ قَبِيلةٍ بِتِرَاتِهِمْ', 'لَمْ يَأْلُهُمْ في مُلْكِهمْ تَعْدِيلا', 'فَثَوَى وَوَرَّثَ مُلْكِ مَنْ وَطِئَ الحَصَى', 'قَسْرًا أبوهُ عَنْوَةً وَنُحُولا', 'سَائِلْ بَنِي أَسَدٍ بِمَقْتَلِ رَبِّهِمْ', 'حُجْرِ بنِ أُمِّ قَطَامِ جَلَّ قَتِيلا', 'إذا سَارَ ذو التَّاجِ الهِجَانِ بِجَحْفَلٍ', 'لَجِبٍ يُجَاوَبُ بالفَلاةِ صَهِيلا', 'حتى أَبَالَ الخَيْلَ في عَرَصَاتِهِمْ', 'فَشَفَى وَزَادَ على الشِّفَاءِ غَلِيلا', 'أَحْمَى دُرُوعَهُمُ فَسَرْبَلَهُمْ بِهَا', 'والنَّارَ كَحَّلَهُمْ بها تَكْحِيلا', 'وأقامَ يَسْقِي الرَّاحِ في هَامَاتِهِمْ', 'مَلِكٌ يُعَلُّ بِشُرْبِها تَعْلِيلا', 'والبِيْضَ قَنَّعَهَا شَدِيدًا حَرُّهُا', 'فَكَفَى بذلكَ لِلْعِدَا تَنْكِيلا', 'حَلَّتْ لَهُ مِنْ بَعْدِ تَحْرِيمٍ لَهَا', 'أَو أَنْ يَمَسَّ الرَّأسَ منه غُسُولا', 'حتى أباحَ ديارَهمْ فَأَبَارَهُمْ', 'فَعَمُوا فهمْ لا يَهْتَدونَ سَبِيلا']

    def generate(self, prompt):
        line = self.lines[self.i]
        self.i = (self.i + 1) % len(self.lines)
        return line

class LLM_INTERFACE_CRITIC(ABC):
    @abstractmethod
    def critique(self, shatr, previous_shatrs=None) -> str:
        pass

class FakeCritic(LLM_INTERFACE_CRITIC):
    def critique(self, shatr, previous_shatrs=None):
        return "This is a fake critic."


class ALLAM_CRITIC(LLM_INTERFACE_CRITIC):
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
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "repetition_penalty": 1.1,
        }

    def critique(self, shatr, previous_shatrs=None, **kwargs):
        url = BASE_URL + "v1/text/generation?version=2024-08-30"

        prompt = self.build_critique_prompt(shatr, previous_shatrs)

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


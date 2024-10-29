import os
import random
from LLMInterface import ALLAM_GENERATOR, FakeGenerator
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter

def load_env(file_path):
    """Load environment variables from a .env file."""
    with open(file_path) as f:
        for line in f:
            # Remove comments and whitespace
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value

load_env(".env")

# Initialize logical units
def infer_wazn(prompt):
    return None

def infer_qafiya(prompt):
    return None

def infer_length(prompt):
    return 2

def generate_qasida(prompt, shatr_generator, wazn=None, qafiya=None, length=None):
    wazn = wazn or infer_wazn(prompt)
    qafiya = qafiya or infer_qafiya(prompt)
    length = length or infer_length(prompt)
    
    shatrs = []
    for i in range(length): #length = abyat
        feedback = None
        best_shatrs = []
        for runs in range(1): #how many feedback runs to do?
            best_shatrs = []
            shatr, w, q = shatr_generator.generate_shatr(prompt, wazn, (qafiya if i == 0 else None), feedback, shatrs)
            if wazn is None:
                wazn = w
            if qafiya is None: #for 1st bayt, make sure qafiya matches. (Ma6la3 Qaseedah, qafiyah should be there in both shatrs)
                qafiya = q
            best_shatrs.append(shatr.strip())
            
            shatr, w, q = shatr_generator.generate_shatr(prompt, wazn, qafiya, feedback, shatrs)
            best_shatrs.append(shatr.strip())
            #TODO get feedback, run it back
            feedback = None
        shatrs.extend(best_shatrs) #get best attempt and store it

    
    return shatrs

if __name__ == "__main__":
    api_key = os.environ.get("API_KEY")
    llm = ALLAM_GENERATOR(api_key)
    rag = Prompter(poet="عنترة بن شداد")
    #llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm, prompter=rag)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator, length=10, wazn="الكامل", qafiya="لا")
        print(qasida)

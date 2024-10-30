import os
import random
from LLMInterface import ALLAM_GENERATOR, FakeGenerator, load_env
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter
from Critic import CriticGen

load_env(".env")

# Initialize logical units
def infer_wazn(prompt):
    return None

def infer_qafiya(prompt):
    return None

def infer_length(prompt):
    return 2

def generate_qasida(prompt, shatr_generator, critic, wazn=None, qafiya=None, length=None):
    wazn = wazn or infer_wazn(prompt)
    qafiya = qafiya or infer_qafiya(prompt)
    length = length or infer_length(prompt)
    
    shatrs = []
    for i in range(length): #length = abyat
        feedback = [] #list of feedbacks for current bayt
        curr_bayt = []
        for runs in range(2): #how many feedback runs to do? i'm thinking just one
            curr_bayt = []
            shatr, w, q = shatr_generator.generate_shatr(prompt, wazn, (qafiya if i == 0 else None), feedback, shatrs)
            if wazn is None:
                wazn = w
            if qafiya is None: #for 1st bayt, make sure qafiya matches. (Ma6la3 Qaseedah, qafiyah should be there in both shatrs)
                qafiya = q
            curr_bayt.append(shatr)
            
            shatr, w, q = shatr_generator.generate_shatr(prompt, wazn, qafiya, feedback, shatrs + curr_bayt)
            curr_bayt.append(shatr)
            #get feedback for this newest bayt
            feedback.append(critic.critic(curr_bayt, shatrs, feedback))
        shatrs.extend(curr_bayt) #get last attempt and store it

    
    return shatrs

if __name__ == "__main__":
    api_key = os.environ.get("API_KEY")
    #llm = ALLAM_GENERATOR(api_key)
    llm = FakeGenerator(wazn="الكامل")
    rag = Prompter(poet="عنترة بن شداد")
    critic = CriticGen(llm)
    #llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm, prompter=rag)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator, critic, length=1, wazn="الكامل", qafiya="لا")
        print(qasida)

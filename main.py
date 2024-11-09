import os
import random
from LLMInterface import ALLAM_GENERATOR, FakeGenerator, load_env
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter
from Critic import CriticGen
from JSONizer import *

load_env(".env")

# Initialize logical units
def infer_wazn(prompt):
    return None

def infer_qafiya(prompt):
    return None

def infer_length(prompt):
    return 2

def generate_qasida(prompt, shatr_generator: ShatrGenerator, critic: CriticGen, wazn=None, qafiya=None, length=None):
    wazn = wazn or infer_wazn(prompt)
    qafiya = qafiya or infer_qafiya(prompt)
    length = length or infer_length(prompt)
    JSONizer.resetResponse()
    
    shatrs = []
    for i in range(length): #length = abyat
        #plan bait
        print("PLANNING SHATR CODE GOES HERE: ")
        if i > 0:
            plan_txt = shatr_generator.llm.generate(shatr_generator.prompter.wrap_gen(prompt, shatrs, None, None, plan=1, ), is_critic=True, stop_tokens=['"'])
            print("PLANNED RESULT OF THE BAYT: "+plan_txt)
        else:
            plan_txt = None

        

        feedback = [] #list of feedbacks for current bayt
        curr_bayt = []
        for runs in range(2): #how many feedback runs to do? i'm thinking just one
            curr_bayt = []
            shatr, w, q, valid = shatr_generator.generate_shatr(prompt, wazn, (qafiya if i == 0 else None), feedback, shatrs, plan_txt)
            if wazn is None:
                wazn = w
            curr_bayt.append(shatr)
            JSONizer.nextShatr()
            shatr, w, q, valid2 = shatr_generator.generate_shatr(prompt, wazn, qafiya, feedback, shatrs + curr_bayt, plan_txt)
            JSONizer.nextShatr()
            if qafiya is None: #for 1st bayt, make sure qafiya matches. (Ma6la3 Qaseedah, qafiyah should be there in both shatrs)
                qafiya = q
            curr_bayt.append(shatr)
            print(curr_bayt)
            #get feedback for this newest bayt
            hard_coded_feedback = []
            if (q != qafiya):
                print("QAFIYA FEEDBACK")
                hard_coded_feedback.append(critic.hardcoded_qafiya_feedback(qafiya))
            if not (valid and valid2): #wazn is still invalid, but ran out of iters
                print("WAZN FEEDBACK")
                hard_coded_feedback.append(critic.hard_coded_wazn_feedback(wazn))

            feedback.append(critic.critic(curr_bayt, shatrs, feedback, hard_coded_feedback, plan_txt=plan_txt))
            print("FEEDBACK: "+feedback[-1]["feedback"])
        shatrs.extend(curr_bayt) #get last attempt and store it

    
    return shatrs

if __name__ == "__main__":
    api_key = os.environ.get("API_KEY")
    llm = ALLAM_GENERATOR(api_key)
    #llm = FakeGenerator(wazn="الكامل")
    rag = Prompter(poet="عنترة بن شداد")
    #rag = Prompter(poet = "أحمد شوقي")
    critic = CriticGen(llm)
    #llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm, prompter=rag)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator, critic, length=3, wazn="الكامل", qafiya="لا")
        print(qasida)

import os
import random

# Initialize logger
from Logger import Logger
Logger.initialize('main')
LOGGER = Logger.get_logger()

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

def generate_qasida(prompt, shatr_generator, critic: CriticGen, wazn=None, qafiya=None, length=None):
    wazn = wazn or infer_wazn(prompt)
    qafiya = qafiya or infer_qafiya(prompt)
    length = length or infer_length(prompt)
    
    LOGGER.info(f"Generating qasida with prompt: {prompt}, wazn: {wazn}, qafiya: {qafiya}, length: {length}")

    shatrs = []
    for i in range(length): #length = abyat
        feedback = [] #list of feedbacks for current bayt
        curr_bayt = []

        LOGGER.info(f"Generating bayt {i+1} of {length}...")

        RUNS = 2
        for runs in range(RUNS): #how many feedback runs to do? i'm thinking just one
            LOGGER.info(f"Generating shatrs in run {runs+1} of {RUNS}...")
            curr_bayt = []
            shatr, w, q, valid = shatr_generator.generate_shatr(prompt, wazn, (qafiya if i == 0 else None), feedback, shatrs)
            if wazn is None:
                wazn = w

            LOGGER.info(f"Shatr 1 generated: {shatr}")
            curr_bayt.append(shatr)
            
            shatr, w, q, valid2 = shatr_generator.generate_shatr(prompt, wazn, qafiya, feedback, shatrs + curr_bayt)
            if qafiya is None: #for 1st bayt, make sure qafiya matches. (Ma6la3 Qaseedah, qafiyah should be there in both shatrs)
                qafiya = q
            
            LOGGER.info(f"Shatr 2 generated: {shatr}")
            curr_bayt.append(shatr)
            print(curr_bayt)
            #get feedback for this newest bayt
            hard_coded_feedback = []
            if (q != qafiya):
                LOGGER.warning(f"Qafiya feedback: {q} != {qafiya}")
                hard_coded_feedback.append(critic.hardcoded_qafiya_feedback(qafiya))
            if not (valid and valid2): #wazn is still invalid, but ran out of iters
                LOGGER.warning("Wazn feedback: wazn is invalid")
                hard_coded_feedback.append(critic.hard_coded_wazn_feedback(wazn))

            feedback.append(critic.critic(curr_bayt, shatrs, feedback, hard_coded_feedback))
            LOGGER.info(f"Feedback: {feedback[-1]['feedback']}")
        shatrs.extend(curr_bayt) #get last attempt and store it

    
    return shatrs

if __name__ == "__main__":
    api_key = os.environ.get("API_KEY")
    llm = ALLAM_GENERATOR(api_key)
    #llm = FakeGenerator(wazn="الكامل")
    rag = Prompter(poet="عنترة بن شداد")
    critic = CriticGen(llm)
    #llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm, prompter=rag)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator, critic, length=1, wazn="الكامل", qafiya="لا")
        LOGGER.info("Qasida generated")
        LOGGER.info(qasida)

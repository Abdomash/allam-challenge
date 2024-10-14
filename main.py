import random
from LLMInterface import ALLAM_GENERATOR, FakeGenerator
from ShatrGenerator import ShatrGenerator
from RAG import RAG

# Initialize logical units
def infer_wazn(prompt):
    return None

def infer_qafiya(prompt):
    return None

def infer_length(prompt):
    return 6

def generate_qasida(prompt, shatr_generator, wazn=None, qafiya=None, length=None, poet=None):
    wazn = wazn or infer_wazn(prompt)
    qafiya = qafiya or infer_qafiya(prompt)
    length = length or infer_length(prompt)
    poet = poet or None
    
    shatrs = []
    for _ in range(length):
        shatr = shatr_generator.generate_shatr(prompt, wazn, qafiya, shatrs)
        shatrs.append(shatr.strip())
    
    return shatrs

if __name__ == "__main__":
    # api_key = input("Enter API key: ")
    # llm = ALLAM_GENERATOR(api_key)
    llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator)
        print(qasida)

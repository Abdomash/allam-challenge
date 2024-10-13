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

def generate_qasida(prompt, shatr_generator):
    wazn = infer_wazn(prompt)
    qafiya = infer_qafiya(prompt)
    length = infer_length(prompt)
    
    shatrs = []
    for shatr_idx in range(length):
        shatr = shatr_generator.generate_shatr(prompt, wazn, qafiya, shatrs)
        shatrs.append(shatr)
    
    output = ""
    for i, shdr in enumerate(shatrs):
        output += shdr + ("\n" if i % 2 else " \t\t ")
    
    return output

if __name__ == "__main__":
    api_key = input("Enter API key: ")
    # llm = ALLAM(api_key)
    llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, shatr_generator)
        print(qasida)

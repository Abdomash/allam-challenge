import random
from LLMInterface import LLM_Interface
from VerseGenerator import VerseGenerator
from RAG import RAG

# Initialize logical units
def infer_wazn(prompt):
    return None

def infer_qafiya(prompt):
    return None

def infer_length(prompt):
    return random.randint(8, 15) * 2

def generate_qasida(prompt, verse_generator):
    rag = RAG()

    wazn = infer_wazn(prompt)
    qafiya = infer_qafiya(prompt)
    length = infer_length(prompt)
    
    shdrs = []
    for shdr_idx in range(length):
        verse = verse_generator.generate_verse(prompt, wazn, qafiya, shdr_idx % 2)
        shdrs.append(verse)
    
    output = ""
    for i, shdr in enumerate(shdrs):
        output += shdr + ("\n" if i % 2 else "")
    
    return output

if __name__ == "__main__":
    llm = LLM_Interface()
    rag = RAG("qawafi-database.json")
    verse_generator = VerseGenerator(rag)
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt or prompt == "exit":
            break
        qasida = generate_qasida(prompt, verse_generator)
        print(qasida)

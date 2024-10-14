import json
import random

class RAG:
    def __init__(self, qawafi_filepath="qawafi-database.json", qafiya=None, poet=None):
        self.qafiya = qafiya
        self.qafiya_examples = None
        self.db = None
        self.poet = None
        with open(qawafi_filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]

        if poet:
            poets = load_poets()
            poet_data = next((item for item in poets if item["name"] == poet), None)
            if not poet_data:
                raise ValueError(f"Poet not found in database: Could not find {poet} in 'poet.json'")
            self.poet = poet_data

        self.setQafiya(qafiya)
    
    def wrap(self, prompt, previous_shatrs=None, feedback=None, current_attempt=None):
        full_text = "<s> [INST]\n"
        if self.poet:
            full_text += f"{self.poet['description']}\n"

        full_text += "اكتب شطر واحد لجزء من قصيدة.\n"

        if self.qafiya:
            full_text += f" قافية القصيدة هي '{self.qafiya}'. "

        if self.qafiya_examples:
            full_text += "هنا بعض الامثلة لكلمات تنتهي بهذه القافية: \n"
            full_text += ", ".join(random.sample(self.qafiya_examples, 10))
            full_text += "\n"
        
        if prompt:
            full_text += f"هنا الطلب اللي وضعه المستخدم:\n"
            full_text += f"{prompt}\n"
        
        if previous_shatrs:
            full_text += "هنا الشطور السابقة:\n"
            full_text += '\n'.join(previous_shatrs)
            full_text += '\n'

        if feedback:
            full_text += "هنا بعض النصائح على هذا اخر شطر تم ادخاله:\n"
            full_text += f"{feedback}\n"
        
        full_text += " [/INST]"

        if current_attempt:
            full_text += current_attempt

        return full_text
    
    def update(self, qafiya):
        self.qafiya_examples = self.setQafiya(qafiya)
        self.qafiya = qafiya

    def setQafiya(self, qafiya):
        if not qafiya:
            return None

        def processed(word):
            if word.endswith(qafiya):
                return word
            if qafiya[-1] == "ا" and word.endswith(qafiya[0]):
                return word+"ا"
            if qafiya[-1] == "ه" and word.endswith(qafiya[0]):
                return word+"ه"
            if qafiya[-1] == "ه" and word.endswith("ة"):
                return word.replace("ة" , f"ه")
            #TODO: waw + ya edge cases (ignore - only if using verbs + nouns)
            return None
        
        output = []
        for word in self.db:
            new_word = processed(word)
            if new_word:
                output.append(new_word)

        return output
        
def load_poets():
    with open("poets.json", 'r', encoding="utf-8") as f:
        poets = json.load(f)["poets"]
        return poets


if __name__ == "__main__":
    r = RAG()
    r.update("ب")
    print(r.wrap("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None, "أخي"))
    print('\n\n') 
    r = RAG(poet="المتنبي")
    r.update("ق")
    print(r.wrap("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None))

import json
import random

class RAG:
    def __init__(self, filepath="qawafi-database.json", qafiya=None):
        self.qafiya = qafiya
        self.message = None
        self.db = None
        with open(filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]
        self.setQafiya(qafiya)
    
    def wrap(self, prompt, previous_shatrs=None, feedback=None):
        full_text = ""
        full_text += "اكتب شطر واحد لجزء من قصيدة.\n"
        
        if self.qafiya:
            full_text += f" قافية القصيدة هي '{self.qafiya}'. "

        if self.message:
            full_text += "هنا بعض الامثلة لكلمات تنتهي بهذه القافية: \n"
            # full_text += "<QafiyaExamples>"
            full_text += ", ".join(random.sample(self.message, 10))
            full_text += "\n"
            # full_text += "</QafiyaExamples>"
        
        if prompt:
            full_text += f"هنا الطلب اللي وضعه المستخدم:\n"
            full_text += f"{prompt}\n"
        
        if previous_shatrs:
            full_text += "هنا الشطور السابقة:\n"
            full_text += f"{previous_shatrs}\n"

        if feedback:
            full_text += "هنا بعض النصائح على هذا اخر شطر تم ادخاله:\n"
            full_text += f"{feedback}\n"

        return full_text
    
    def update(self, qafiya):
        self.message = self.setQafiya(qafiya)
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
            return None
        
        output = []
        for word in self.db:
            new_word = processed(word)
            if new_word:
                output.append(new_word)

        return output
        
import json
import random

class RAG:
    def __init__(self, filepath, qafiya):
        self.message = "RAG initialized"
        self.qafiya = qafiya
        self.db = None
        with open(filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]
        self.update(None, qafiya)
    
    def wrap(self, prompt, previous_shatrs=None, feedback=None):
        return f'''
        اكتب شطر واحد لجزء من القصيدة. 
        قافية القصيدة هي "{self.qafiya}".
        هنا بعض الامثلة لكلمات تنتهي بهذه القافية
        يمكن ان تستعمل هذه الكلمات او كلمات اخرى بنفس القافية:
        <QafiyaExamples>{random.sample(self.message, 10)}</QafiyaExamples>
        هنا الطلب اللي وضعه المستخدم:
        <prompt>{prompt}</prompt>
        هنا الشطور السابقة التي تم ادخالها بنجاح:        
        <previous-successful-outputs>{previous_shatrs}</previous-successful-outputs>
        وهنا بعض النصائح على هذا اخر شطر تم ادخاله:
        <feedback>{feedback}</feedback>
        '''
    
    def update(self, wazn, qafiya):
        self.message = self.setQafiya(qafiya)
        self.qafiya = qafiya

    def setQafiya(self, qafiya):
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
        
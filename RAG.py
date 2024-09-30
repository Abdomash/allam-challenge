import json

class RAG:
    def __init__(self, filepath, qafiya):
        self.message = "RAG initialized"
        self.db = None
        with open(filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]
        self.update(None, qafiya)
    
    def wrap(self, prompt, feedback=None):
        return f'''
        <QafiyaExamples>{self.message}</QafiyaExamples>
        <prompt>{prompt}</prompt>
        <feedback>{feedback}</feedback>
        '''
    
    def update(self, wazn, qafiya):
        self.message = self.setQafiya(qafiya)

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
        
import json

class RAG:
    def __init__(self, filepath):
        self.message = "RAG initialized"
        self.db = None
        with open(filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]
    
    def wrap(self, prompt, feedback=None):
        return f'''
        <info>{self.message}</info>
        <prompt>{prompt}</prompt>
        <feedback>{feedback}</feedback>
        '''
    
    def update(self, new_qafiya):
        self.message = self.setQafiya(new_qafiya)

    def setQafiya(self, qafiya):
        def is_valid(word):
            if word.endswith(qafiya):
                return True, word
            if qafiya[-1] == "ا" and word.endswith(qafiya[0]):
                return True, word+"ا"
            if qafiya[-1] == "ه" and word.endswith(qafiya[0]):
                return True, word+"ه"
            if qafiya[-1] == "ه" and word.endswith("ة"):
                return True, word.replace("ة" , f"ه")
            return False, None
        
        output = []
        for word in self.db:
            v, new_word = is_valid(word)
            if v:
                output.append(new_word)

        return output
        
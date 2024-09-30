class RAG:
    def __init__(self):
        self.message = "RAG initialized"
    
    def wrap(self, prompt, feedback=None):
        return f"<info>{self.message}</info><prompt>{prompt}</prompt><feedback>{feedback}</feedback>"
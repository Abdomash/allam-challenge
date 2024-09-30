class LLM_Interface:
    def __init__(self):
        raise NotImplementedError
    
    def generate(self, prompt, extra_info=None):
        raise NotImplementedError
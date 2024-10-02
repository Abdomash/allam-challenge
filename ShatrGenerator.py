from Extractor import Extractor
from FeedbackGenerator import FeedbackGenerator
from QafiyaValidator import QafiyaValidator
from WaznValidator import WaznValidator
from RAG import RAG


class ShatrGenerator:
    def __init__(self, llm, rag, feedback_generator):
        self.llm = llm
        self.rag = RAG()
        self.feedback_generator = FeedbackGenerator()
        self.extractor = Extractor()
        self.wazn_validator = WaznValidator()
        self.qafiya_validator = QafiyaValidator()
    
    def generate_shatr_tokens(self, prompt, feedback=None):
        return self.llm.generate(self.rag.wrap(prompt, feedback))
    
    def generate_shatr(self, prompt, wazn, qafiya, feedback=None):
        valid = False
        
        while not valid:
            # Step 1: Generate shatr tokens
            shatr = self.generate_shatr_tokens(prompt, feedback)

            # Step 2: Extract Wazn and Qafiya
            new_qafiya, new_wazn = self.extractor.extract(shatr)

            # Step 3: Validate Wazn
            valid_wazn = self.wazn_validator.validate_wazn(new_wazn, wazn)
            if not valid_wazn:
                feedback = self.feedback_generator.generate_feedback("wazn", shatr, wazn=new_wazn, old_feedback=feedback)
                continue  # Loop back to regenerate

            wazn = new_wazn

            # Step 5: Validate Qafiya
            valid_qafiya = self.qafiya_validator.validate_qafiya(qafiya)
            if not valid_qafiya:
                feedback = self.feedback_generator.generate_feedback("qafiya", shatr, qafiya=new_qafiya, old_feedback=feedback)
                continue  # Loop back to regenerate

            # Step 6: Update RAG and finalize shatr
            self.rag.update(shatr, wazn, qafiya)
            valid = True
        return shatr

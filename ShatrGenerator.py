from Extractor import Extractor
from FeedbackGenerator import FeedbackGenerator
from QafiyaValidator import QafiyaValidator
from RAG import RAG
from WaznValidator import WaznValidator


class ShatrGenerator:
    def __init__(self, llm, rag=None, feedback_generator=None, extractor=None, wazn_validator=None, qafiya_validator=None):
        self.llm = llm
        self.rag = rag or RAG()
        self.feedback_generator = feedback_generator or FeedbackGenerator()
        self.extractor = extractor or Extractor()
        self.wazn_validator = wazn_validator or WaznValidator()
        self.qafiya_validator = qafiya_validator or QafiyaValidator()
        
    def generate_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None):
        valid = False
        
        while not valid:
            # Step 1: Generate a shatr
            shatr = self.llm.generate(self.rag.wrap(prompt, previous_shatrs, feedback))
            print(shatr)

            # Step 2: Extract Wazn and Qafiya
            new_qafiya, new_wazn = self.extractor.extract(shatr)

            # Step 3: Validate Wazn
            valid_wazn = self.wazn_validator.validate_wazn(new_wazn, wazn)
            if not valid_wazn:
                feedback = self.feedback_generator.generate_feedback("wazn", shatr, wazn=new_wazn)
                continue  # Loop back to regenerate

            wazn = new_wazn

            # Step 5: Validate Qafiya
            valid_qafiya = self.qafiya_validator.validate_qafiya(new_qafiya, qafiya)
            if not valid_qafiya:
                feedback = self.feedback_generator.generate_feedback("qafiya", shatr, qafiya=new_qafiya)
                continue  # Loop back to regenerate

            # Step 6: Update RAG and finalize shatr
            self.rag.update(qafiya)
            valid = True
        return shatr
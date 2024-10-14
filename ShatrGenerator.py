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
        shatr = ""
        while not valid:
            # Step 1: Generate a shatr
            shatr = self.llm.generate(self.rag.wrap(prompt, previous_shatrs, feedback, shatr))

            # Step 2: Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_info = self.extractor.extract(shatr)

            # Step 3: Validate Wazn
            first_mistake_idx = self.wazn_validator.validate_wazn(new_wazn_info, new_wazn_name, wazn) # wazn is the wazn name!
            if first_mistake_idx > -1: # Mistake found
                feedback = self.feedback_generator.generate_feedback("wazn", wazn, new_wazn_name, shatr)
                shatr = self.cut_to_last_valid_word(shatr, first_mistake_idx)
                continue # Loop back to regenerate
            wazn = new_wazn_name

            # Step 5: Validate Qafiya
            valid_qafiya = (new_qafiya == qafiya) if qafiya is not None else True
            if not valid_qafiya:
                feedback = self.feedback_generator.generate_feedback("qafiya", qafiya, new_qafiya, shatr)
                continue  # Loop back to regenerate

            # Step 6: Update RAG and finalize shatr
            self.rag.update(qafiya)
            valid = True
        return shatr

    def cut_to_last_valid_word(self, shatr, first_mistake):
        if " " in shatr[:first_mistake]:
            return shatr[:first_mistake].rsplit(" ", 1)[0]
        else:
            return ""

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
        cut_shatr = ""
        while not valid:
            # Step 1: Generate a shatr
            shatr = cut_shatr + self.llm.generate(self.rag.wrap(prompt, previous_shatrs, feedback, cut_shatr))
            print(shatr)

            # Step 2: Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_info = self.extractor.extract(shatr)

            # Step 3: Validate Wazn
            first_mistake = self.wazn_validator.validate_wazn(new_wazn_info, new_wazn_name, wazn) #wazn is the wazn name!
            if first_mistake > -1:
                feedback = self.feedback_generator.generate_feedback("wazn", shatr, wazn=new_wazn)
                #cut shatr and re-generate
                if " " in shatr[:first_mistake]:
                    cut_shatr = shatr[:first_mistake].rsplit(" ", 1)[0] #keep atleast 1 word
                else:
                    cut_shatr = "" #regen from the beginning
                continue  # Loop back to regenerate

            wazn = new_wazn_name

            # Step 5: Validate Qafiya
            valid_qafiya = (new_qafiya == qafiya) if qafiya is not None else True
            if not valid_qafiya:
                feedback = self.feedback_generator.generate_feedback("qafiya", shatr, qafiya=new_qafiya)
                continue  # Loop back to regenerate

            # Step 6: Update RAG and finalize shatr
            self.rag.update(qafiya)
            valid = True
        return shatr


    def gen(self):
        feedback = ""
        for i in range(10):
            self.generate_shatr(feedback=feedback)
            feedback = self.feedback_generator.generate_feedback()

            
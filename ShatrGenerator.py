from Analyzer import Analyzer
from FeedbackGenerator import FeedbackGenerator
from QafiyaValidator import QafiyaValidator
from RAG import RAG
from WaznValidator import WaznValidator




class ShatrGenerator:
    def __init__(self, llm, rag=None, feedback_generator=None, analyzer=None, wazn_validator=None, qafiya_validator=None):
        self.llm = llm
        self.rag = rag or RAG()
        self.feedback_generator = feedback_generator or FeedbackGenerator()
        self.analyzer = analyzer or Analyzer()
        self.wazn_validator = wazn_validator or WaznValidator()
        self.qafiya_validator = qafiya_validator or QafiyaValidator()
        
    def generate_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None):
        valid = False
        shatr = ""
        iters = 0
        new_shatr = ""
        while not valid and iters < 7:
            iters += 1
            # Step 1: Generate a shatr
            shatr = new_shatr
            shatr += self.llm.generate(self.rag.wrap(prompt, previous_shatrs, feedback, shatr))
            print("----------------------")
            print(f"attempt {iters}: {shatr}")
            # Step 2: Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_combs, new_wazn_mismatch, diacritized = self.analyzer.extract(shatr, expected_wazn_name=wazn)

            if wazn is None:
                wazn = new_wazn_name
            
            # Step 3: Validate Wazn
            #first_mistake_idx = self.wazn_validator.validate_wazn(new_wazn_info, new_wazn_name, wazn) # wazn is the wazn name!
            first_mistake_idx = self.analyzer.get_first_mistake(new_wazn_mismatch)
            if first_mistake_idx > -1: # Mistake found
                #feedback = self.feedback_generator.generate_feedback("wazn", new_wazn_name, wazn, shatr)
                #print(feedback)
                new_shatr = self.cut_to_last_valid_word(diacritized, first_mistake_idx)
                print(f"cut shatr: {new_shatr}")
                continue # Loop back to regenerate

            # Step 5: Validate Qafiya
            valid_qafiya = (new_qafiya == qafiya) if qafiya is not None else True
            if not valid_qafiya:
                feedback = self.feedback_generator.generate_feedback("qafiya", new_qafiya, qafiya, shatr)
                print(feedback)
                #shatr = ""
                #continue  # Loop back to regenerate

            # Step 6: Update RAG and finalize shatr
            if qafiya is None:
                self.rag.update(new_qafiya)
                qafiya = new_qafiya

            valid = True
        
        print(f"wazn: {new_wazn_name}, qafiya: {qafiya}")
        return shatr, new_wazn_name, qafiya

    def cut_to_last_valid_word(self, shatr, first_mistake):
        if " " in shatr[:first_mistake]:
            return shatr[:first_mistake].rsplit(" ", 1)[0]
        else:
            return ""

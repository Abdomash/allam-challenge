from Analyzer import Analyzer
from Prompter import Prompter

from LLMInterface import BAYT_SEPARATORS

def clean_bayt(bait): #cleans / removes *,/,newline,. etc from bayt
    new_b = bait
    for i in BAYT_SEPARATORS:
        new_b = new_b.replace(i, "")
    return new_b.strip()

class ShatrGenerator:
    def __init__(self, llm, prompter=None, analyzer=None):
        self.llm = llm
        self.prompter = prompter or Prompter()
        self.analyzer = analyzer or Analyzer()
    
    #no qafiya validation here. Will do in larger loop, where we compare it to 
    def generate_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None): #generates a shatr with the correct wazn. Doesn't account for feedback here.
        valid = False
        shatr = ""
        iters = 0
        new_shatr = ""
        self.prompter.update(qafiya, None, wazn)

        last_mistake = -1 #use it to track if model is stuck
        last_repeats = -1 #if it is stuck, restart generation / increase temp

        while not valid and iters < 10:
            iters += 1
            # Generate a shatr
            shatr = new_shatr
            shatr += self.llm.generate(self.prompter.wrap_gen(prompt, previous_shatrs, feedback, shatr))
            shatr = clean_bayt(shatr)
            print("----------------------")
            print(f"attempt {iters}: {shatr}")
            # Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_combs, new_wazn_mismatch, diacritized, arudi_indices = self.analyzer.extract(shatr, expected_wazn_name=wazn)
            
            diacritized = clean_bayt(diacritized)

            if wazn is None:
                wazn = new_wazn_name
            
            # Validate Wazn
            #first_mistake_idx = self.analyzer.get_first_mistake(new_wazn_mismatch)
            if new_wazn_mismatch > -1: # Mistake found
                #feedback = self.feedback_generator.generate_feedback("wazn", new_wazn_name, wazn, shatr)
                #print(feedback)
                index_to_delete = arudi_indices[new_wazn_mismatch]

                if last_mistake <= new_wazn_mismatch: #reached new point!
                    last_repeats = 0
                    last_mistake = new_wazn_mismatch
                    #iters -= 1 #give it some more room to gen
                else:
                    last_repeats += 1
                    if last_repeats > 3: #got stuck a number of times
                        index_to_delete = 0 #restart whole generation.
                        #iters -= 1


                new_shatr = self.cut_to_last_valid_word(diacritized, index_to_delete) #harakat means length of diacritized is double!
                print(f"cut shatr: {new_shatr}")
                continue # Loop back to regenerate
            
            valid = True
        
        print(f"wazn: {new_wazn_name}, qafiya: {qafiya}")
        return clean_bayt(shatr), new_wazn_name, qafiya

    def cut_to_last_valid_word(self, shatr, first_mistake):
        if " " in shatr[:first_mistake]:
            return shatr[:first_mistake].rsplit(" ", 1)[0]
        else:
            return ""
    

    def generate_multiple_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None):
        pass

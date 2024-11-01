from Analyzer import Analyzer
from Prompter import Prompter

from LLMInterface import BAYT_SEPARATORS

from Logger import Logger
LOGGER = Logger.get_logger()

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

        temp = 0.3 #little temp, increase as you go further into iters, to randomize more
        #max ~1.0 (if 3 times wrong)

        last_mistake = -1 #use it to track if model is stuck
        last_repeats = -1 #if it is stuck, restart generation / increase temp

        while not valid and iters < 10:
            iters += 1
            # Generate a shatr
            shatr = new_shatr
            shatr += self.llm.generate(self.prompter.wrap_gen(prompt, previous_shatrs, feedback, shatr), temp=temp)
            shatr = clean_bayt(shatr)
            # Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_combs, new_wazn_mismatch, diacritized, arudi_indices = self.analyzer.extract(shatr, expected_wazn_name=wazn)
            
            diacritized = clean_bayt(diacritized)

            LOGGER.info(f"---------- Iteration {iters} ------------")
            LOGGER.info("Temp: " + str(temp))
            LOGGER.info(f"Model Attempt: {shatr}")
            LOGGER.info("Extracted Qafiya: " + new_qafiya)
            LOGGER.info("Extracted Wazn: " + new_wazn_name)
            LOGGER.info("Extracted Wazn's Combs: " + str(new_wazn_combs))
            LOGGER.info("Extracted Wazn's Mismatch: " + str(new_wazn_mismatch))
            LOGGER.info("Extracted Diacritized: " + diacritized)
            LOGGER.info("Extracted Arudi Indices: " + str(arudi_indices))

            if wazn is None:
                LOGGER.info(f"Wazn is None, setting to extracted wazn {new_wazn_name}")
                wazn = new_wazn_name
            
            # Validate Wazn
            # first_mistake_idx = self.analyzer.get_first_mistake(new_wazn_mismatch)
            if new_wazn_mismatch > -1: # Mistake found
                LOGGER.warning(f"Mistake found in wazn: {new_wazn_name} at index {new_wazn_mismatch}")

                index_to_delete = arudi_indices[new_wazn_mismatch]
                LOGGER.info("Deleting at index: " + str(index_to_delete))

                if last_mistake < new_wazn_mismatch: #reached new point!
                    LOGGER.info("Reached further in generation! Resetting attempts counter and temperature.")
                    last_repeats = 0
                    last_mistake = new_wazn_mismatch
                    temp = 0.3 #reset temp back to low val
                    #iters -= 1 #give it some more room to gen
                else:
                    LOGGER.info("Model stuck at same point!")
                    last_repeats += 1
                    if last_repeats > 2: #got stuck a number of times
                        index_to_delete = 0 #restart whole generation.
                        temp *= 1.5 #2 iters wrong, -> temp 0.45 ->, 4 iters 0.675 ->, 6 iters 1.01
                        LOGGER.info(f"Got stuck too many times! Restarting generation with increased temperature: {temp}")
                        #iters -= 1
                        #increase temperature too.

                new_shatr = self.cut_to_last_valid_word(diacritized, index_to_delete) #harakat means length of diacritized is double!
                LOGGER.info("New Cut Shatr: " + new_shatr)
                continue # Loop back to regenerate
            
            valid = True
        
        LOGGER.info(f"Final Shatr: {clean_bayt(shatr)}, Wazn: {new_wazn_name}, Qafiya: {qafiya}")
        return clean_bayt(shatr), new_wazn_name, qafiya, valid

    def cut_to_last_valid_word(self, shatr, first_mistake):
        if " " in shatr[:first_mistake]:
            return shatr[:first_mistake].rsplit(" ", 1)[0]
        else:
            return ""
    

    def generate_multiple_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None):
        pass

from JSONizer import JSONizer
from Analyzer import Analyzer, clean_bayt
from Prompter import Prompter

class ShatrGenerator:
    def __init__(self, llm, prompter=None, analyzer=None):
        self.llm = llm
        self.prompter = prompter or Prompter()
        self.analyzer = analyzer or Analyzer()
    
    #no qafiya validation here. Will do in larger loop, where we compare it to 
    def generate_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None, plan_txt=""): #generates a shatr with the correct wazn. Doesn't account for feedback here.
        valid = False
        shatr = ""
        iters = 0
        new_shatr = ""
        self.prompter.update(qafiya, None, wazn)

        temp = 0.3 #little temp, increase as you go further into iters, to randomize more
        #max ~1.0 (if 3 times wrong)

        last_mistake = -1 #use it to track if model is stuck
        last_repeats = -1 #if it is stuck, restart generation / increase temp

        plan = 2 if plan_txt else 0

        while not valid and iters < 5:
            print(f"Temp: {temp}")
            iters += 1
            # Generate a shatr
            shatr = new_shatr
            shatr += self.llm.generate(self.prompter.wrap_gen(prompt, previous_shatrs, feedback, shatr, plan, plan_txt), temp=temp)
            shatr = clean_bayt(shatr)
            print("----------------------")
            print(f"attempt {iters}: {shatr}")
            # Extract Wazn and Qafiya
            new_qafiya, new_wazn_name, new_wazn_combs, new_wazn_mismatch, diacritized, arudi_indices, tf3elat, aroodi_style = self.analyzer.extract(shatr, expected_wazn_name=wazn)

            if wazn is None:
                wazn = new_wazn_name
            
            # Validate Wazn
            #first_mistake_idx = self.analyzer.get_first_mistake(new_wazn_mismatch)
            if new_wazn_mismatch > -1: # Mistake found
                #feedback = self.feedback_generator.generate_feedback("wazn", new_wazn_name, wazn, shatr)
                #print(feedback)
                index_to_delete = arudi_indices[new_wazn_mismatch]

                if last_mistake < new_wazn_mismatch: #reached new point!
                    last_repeats = 0
                    last_mistake = new_wazn_mismatch
                    temp = 0.2 #reset temp back to low val
                    #iters -= 1 #give it some more room to gen
                else:
                    last_repeats += 1
                    if last_repeats > 2: #got stuck a number of times
                        index_to_delete = 0 #restart whole generation.
                        #temp *= 1.5 #2 iters wrong, -> temp 0.45 ->, 4 iters 0.675 ->, 6 iters 1.01
                        #iters -= 1
                        #increase temperature too.


                new_shatr = self.cut_to_last_valid_word(diacritized, index_to_delete) #harakat means length of diacritized is double!
                print(f"cut shatr: {new_shatr}")
                JSONizer.attempt(diacritized, aroodi_style, new_wazn_combs, new_wazn_mismatch, new_shatr, index_to_delete, tf3elat, new_wazn_name, feedback=None)
                continue # Loop back to regenerate
            
            JSONizer.attempt(diacritized, aroodi_style, new_wazn_combs, new_wazn_mismatch, diacritized, -1, tf3elat, new_wazn_name, feedback=None) #no mistake?
            valid = True
        
        print(f"wazn: {new_wazn_name}, qafiya: {qafiya}")
        return shatr, new_wazn_name, qafiya, valid

    def cut_to_last_valid_word(self, shatr, first_mistake):
        if " " in shatr[:first_mistake]:
            return shatr[:first_mistake].rsplit(" ", 1)[0] + " " #add space (IMPORTANT)
        else:
            return ""
    

    def generate_multiple_shatr(self, prompt, wazn=None, qafiya=None, feedback=None, previous_shatrs=None):
        pass

import random

from Data import *

import itertools

def format_abyat(shatrs): #shatrs -> Shatr0 *** Shatr 1
    ret = ""
    first_half = True
    for s in shatrs:
        if first_half:
            first_half = False
            ret += s
            ret += " *** "
        else:
            first_half = True
            ret += s
            ret += "\n"
    return ret

#class does all prompt-related formats.
class Prompter:
    def __init__(self, qafiya=None, poet=None, wazn=None):
        self.qafiya = qafiya
        self.qafiya_examples = None
        self.qafiya_database = load_qafiyas()
        self.poets_database = load_poets()
        self.poet = None
        self.wazn = None

        self.poets = load_poets()
        self.bohours = load_bohours()
        #self.qafiyas = load_qafiyas()

        self.update(qafiya, poet, wazn)
    
    def wrap_gen(self, prompt, previous_shatrs=None, feedback=None, current_attempt=None, multi_gen=False):
        full_text = "<s> [INST]<<SYS>>\n"
        if self.poet:
            full_text += f"{self.poet['description']}\n"

        full_text += "\n<</SYS>>\n" #end of system prompt
        
        if multi_gen:
            full_text += "أكمل القصيدة التالية بكتابة ١٠ خيارات لنصف بيتٍ شعري (شطر بيت)، ليختار المستخدم الشطر الأنسب ليتمم به القصيدة ويضيف إليه شطراً آخر. تأكد أن المحاولات تتفق مع سياق القصيدة وأنها ذو جزالة وجميلة الموسيقى والشعر. تأكد أن المحاولات كلها ممكن أن تكمل القصيدة. تأكد من كتابة شطر واحد فقط في كل محاولة، وأن تكتب كل محاولة في سطر." + "\n"
        else:
            #full_text += "اكتب شطر واحد لجزء من قصيدة.\n"
            full_text += "اكتب لي قصيدة جديدة وفريدة من نوعها، على نمط الشعر العامودي العربي في أوزانه وكلماته ونغمه ومعانيه. أريد القصيدة أن تكون ذو معانٍ حسنة وقوية وكلمات مؤثرة. "
            if prompt:
                full_text += prompt #add user prompt here too
            full_text += "\n"
        
        if self.wazn: #add wazn name and example bohour
            abyat_examples = [next(self.poem) for i in range(10)] #5 abyat every call
            if self.poet:
                full_text += f"استخدم وزن بحر {self.wazn} لكتابة الأبيات. هذه أمثلة على أبيات شعرية كتبها الشاعر {self.poet['name']} على بحر {self.wazn}:\n"
            else:
                full_text += f"استخدم وزن بحر {self.wazn} لكتابة الأبيات. هذه أمثلة على أبيات شعرية كتبت على بحر {self.wazn}:\n"
            
            full_text += format_abyat(abyat_examples) #already has \n
            
        """
        if prompt:
            full_text += f"هنا الطلب اللي وضعه المستخدم:\n"
            full_text += f"{prompt}\n"
        """

        if self.qafiya:
            full_text += f"اكتب قصيدتك على قافية '{self.qafiya}'، اي تأكد أن آخر كلمة في كل بيت تنتهي بهذه القافية '{self.qafiya}'.\n"
        
        if multi_gen:
            full_text += "إبدأ بكتابة التكملات بحيث تكتب في كل سطر بيت ممكن أن يكمل القصيدة. \n"
            if current_attempt: 
                full_text += f"أيضاً تأكد أن كل المحاولات تبدأ بعبارة ({current_attempt}).\n" 

        if self.qafiya_examples:
            full_text += f"هنا بعض الامثلة لكلمات تنتهي بقافية '{self.qafiya}'. يمكنك استعمال اي واحدة منها لاتمام الأبيات او استعمل كلمات مشابهة لها: "
            full_text += "\n"
            full_text += ", ".join(random.sample(self.qafiya_examples, 20))
            full_text += "\n"

        #full_text += "\n<</SYS>>\n" #end of system prompt

        #add user prompt here
        if prompt:
            full_text += f"{prompt}\n"

        if multi_gen: # FIXME: `previous_shatrs` could be None here, make sure to handle that
            if current_attempt:
                full_text += f"هذه الأبيات كلها تبدأ بعبارة ({current_attempt}) ومن الممكن أن تأتي بعد البيت الأخير ({previous_shatrs[-1]}) ويمكنك استعمال أي واحدة منهن:<s>\n1)"
            else:
                full_text += f"هذه الأبيات كلها من الممكن أن تأتي بعد البيت الأخير ({previous_shatrs[-1]}) ويمكنك استعمال أي واحدة منهن:<s>\n1) "

        full_text += "[/INST] \n"

        full_text += "هذه هي قصيدتي: " + '\n'

        if previous_shatrs:
            #full_text += "هنا الشطور السابقة:\n"
            #full_text += '\n'.join(previous_shatrs)
            if len(previous_shatrs) % 2 == 0:
                full_text += format_abyat(previous_shatrs)
            else:
                full_text += format_abyat(previous_shatrs[:-1]) #last shatr is part of the new attempt. Include it below
                current_attempt = format_abyat([previous_shatrs[-1]]) + current_attempt
            #full_text += '\n'
        
        if feedback: #feedback: list of {"bayt":[s0,s1], "feedback":"str"}
            for f in feedback:
                full_text += format_abyat(f["bayt"]) + "\n" #Allam wrote this.
                full_text += "</s>" #stop token
                full_text += '[INST] '
                full_text += "البيت الآخير من القصيدة قد يحتاج إلى تغير. هذه توجيهات من محلل شعري قام بنقد هذا البيت واستخرج نقاط ممكن أن تحسن البيت من حيث معاني الكلمات والتصوير والمجازات: " #user suggested things
                full_text += "\n'"
                full_text += f["feedback"] + "'\n" #open close quotations from critic says
                full_text += "اعد كتابة آخر بيت مستخدما هذه التوجيهات: " #instructs Allam to rewrite the last line
                full_text += '[/INST] <s> \n'
                #feedback format: {"bayt":[s0,s1], "feedback":"str"}
                full_text += 'حسناً، هذه هو البيت الجديد الذي يستبدل آخر بيت في قصيدتي: ' #Allam responds, writes the line:
                full_text += '\n'

        if current_attempt:
            full_text += current_attempt

        #print(full_text)
        return full_text
    
    def update(self, qafiya=None, poet=None, wazn=None):
        if poet: # in arabic
            if poet not in self.poets.keys():
                raise ValueError(f"Poet not found in database: Could not find {poet} in 'poet.json'")
            self.poet = self.poets[poet]
        elif self.poet is None:
            # self.poet = self.poets[random.choice(list(self.poets.keys()))]
            self.poet = self.poets["علام"]

        if wazn: # in arabic
            self.wazn = wazn
            if wazn not in self.bohours.keys():
                raise ValueError(f"Bahr not found in database: Could not find {wazn} in 'bohours.json'")
            try:
                self.poems = self.poet['poems'][self.bohours[wazn]['name_en']]
                self.poems = [item for sublist in self.poems for item in sublist]
                if len(self.poems) == 0: #allam-poet doesnt have any poems yet. We will fill them in soon.
                    raise KeyError()
            except KeyError:
                print(f"Poet {self.poet['name']} does not have any poems in {wazn}")
                self.poems = [item for sublist in self.poet['poems'].values() for item in sublist]
        elif self.wazn is None:
            self.poems = [item for sublist in self.poet['poems'].values() for item in sublist]

        #print(json.dumps(self.poems))
        # cycle through the poem lines infinitely
        self.poem = itertools.cycle(self.poems)

        if qafiya:
            self.setQafiya(qafiya)

    def setQafiya(self, qafiya):
        if not qafiya:
            return
        
        if qafiya == self.qafiya:
            return #no need to process again
        
        self.qafiya = qafiya

        def processed(word):
            if word.endswith(qafiya):
                return word
            if qafiya[-1] == "ا" and word.endswith(qafiya[0]):
                return word+"ا"
            if qafiya[-1] == "ه" and word.endswith(qafiya[0]):
                return word+"ه"
            if qafiya[-1] == "ن" and word.endswith(qafiya[0]):
                return word
            if qafiya[-1] == "ه" and word.endswith("ة"):
                return word.replace("ة" , f"ه")
            #TODO: waw + ya edge cases (ignore - only if using verbs + nouns)
            return None
        
        output = []
        for word in self.qafiya_database:
            new_word = processed(word)
            if new_word:
                output.append(new_word)

        self.qafiya_examples = output

if __name__ == "__main__":
    r = Prompter()
    r.update("ب")
    print(r.wrap_gen("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None, "أخي"))
    print('\n\n')
    r = Prompter(poet="المتنبي")
    r.update("ق")
    print(r.wrap_gen("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None))

    feedbacks = [
        {"bayt": ["أَلا اِنعِم صَباحاً أَيُّها الرَبعُ وَاِنطِقِ","وَحَدِّث حَديثَ الرَكبِ إِن شِئتَ وَاِصدُقِ"], "feedback":"معلومات عن امرؤ القيس"},
        {"bayt": ["وَحَدِّث بِأَن زالَت بِلَيلٍ حُمولُهُم","كَنَخلٍ مِنَ الأَعراضِ غَيرِ مُنَبِّقِ"], "feedback":"القافية غلط"}
    ]
    print(r.wrap_gen("اكتب لي قصيدة عن الفراق", ["وَفَوقَ الحَوايا غِزلَةٌ وَجَآذِرٌ",
                                                 "تَضَمَّخنَ مِن مِسكٍ ذَكِيٍّ وَزَنبَقِ",
                                                 "فَأَتبَعتُهُم طَرفي وَقَد حالَ دونَهُم",
                                                 "غَوارِبُ رَملٍ ذي أَلاءٍ وَشَبرَقِ"], feedbacks, "try this.."))

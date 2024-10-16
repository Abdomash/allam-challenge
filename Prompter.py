import json
import random

#class does all prompt-related formats.
class Prompter:
    def __init__(self, qawafi_filepath="qawafi-database.json", qafiya=None, poet=None):
        self.qafiya = qafiya
        self.qafiya_examples = None
        self.db = None
        self.poet = None
        with open(qawafi_filepath, 'r', encoding="utf-8") as f:
            self.db = json.load(f)["data"]

        if poet:
            poets = load_poets()
            poet_data = next((item for item in poets if item["name"] == poet), None)
            if not poet_data:
                raise ValueError(f"Poet not found in database: Could not find {poet} in 'poet.json'")
            self.poet = poet_data

        self.setQafiya(qafiya)
    
    def wrap_gen(self, prompt, previous_shatrs=None, feedback=None, current_attempt=None, multi_gen=False):
        full_text = "<s> [INST]\n"
        if self.poet:
            full_text += f"{self.poet['description']}\n"

        if multi_gen:
            full_text += "أكمل القصيدة التالية بكتابة ١٠ خيارات لنصف بيتٍ شعري (شطر بيت)، ليختار المستخدم الشطر الأنسب ليتمم به القصيدة ويضيف إليه شطراً آخر. تأكد أن المحاولات تتفق مع سياق القصيدة وأنها ذو جزالة وجميلة الموسيقى والشعر. تأكد أن المحاولات كلها ممكن أن تكمل القصيدة. تأكد من كتابة شطر واحد فقط في كل محاولة، وأن تكتب كل محاولة في سطر." + "\n"
        else:
            full_text += "اكتب شطر واحد لجزء من قصيدة.\n"

        if self.qafiya:
            full_text += f" قافية القصيدة هي '{self.qafiya}'. "

        if self.qafiya_examples:
            full_text += "هنا بعض الامثلة لكلمات تنتهي بهذه القافية: \n"
            full_text += ", ".join(random.sample(self.qafiya_examples, 10))
            full_text += "\n"
        
        if prompt:
            full_text += f"هنا الطلب اللي وضعه المستخدم:\n"
            full_text += f"{prompt}\n"
        
        if previous_shatrs:
            full_text += "هنا الشطور السابقة:\n"
            full_text += '\n'.join(previous_shatrs)
            full_text += '\n'

        if feedback:
            full_text += "هنا بعض النصائح على هذا اخر شطر تم ادخاله:\n"
            full_text += f"{feedback}\n"
        
        if multi_gen:
            full_text += "إبدأ بكتابة التكملات بحيث تكتب في كل سطر شطر ممكن أن يكمل القصيدة. \n"
            if current_attempt: 
                full_text += f"أيضاً تأكد أن كل المحاولات تبدأ بعبارة ({current_attempt}).\n" 
        
        full_text += "[/INST] "

        if multi_gen:
            if current_attempt:
                full_text += f"هذه الأبيات كلها تبدأ بعبارة ({current_attempt}) ومن الممكن أن تأتي بعد البيت الأخير ({previous_shatrs[-1]}) ويمكنك استعمال أي واحدة منهن:\n1)"
            else:
                full_text += f"هذه الأبيات كلها من الممكن أن تأتي بعد البيت الأخير ({previous_shatrs[-1]}) ويمكنك استعمال أي واحدة منهن:\n1) "

        if current_attempt:
            full_text += current_attempt

        #print(full_text)
        return full_text
    
    def update(self, qafiya):
        self.qafiya_examples = self.setQafiya(qafiya)
        self.qafiya = qafiya

    def setQafiya(self, qafiya):
        if not qafiya:
            return None

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
        for word in self.db:
            new_word = processed(word)
            if new_word:
                output.append(new_word)

        return output

    def generate_feedback(self, type, invalid_item, expected_item, invalid_shatr):
        if type == "qafiya":
            return self.qafiya_feedback(invalid_item, expected_item, invalid_shatr)
        
        if type == "wazn":
            return self.wazn_feedback(invalid_item, expected_item, invalid_shatr)
    
    def qafiya_feedback(self, invalid_qafiya, expected_qafiya, invalid_shatr):
        # TODO

        text = ""
        text += f"الشطر المدخل {invalid_shatr} غير صحيح. "
        text += f"القافية المدخلة {invalid_qafiya} غير صحيحة. "
        text += f"القافية الصحيحة هي {expected_qafiya}. "
        
        return text

    def wazn_feedback(self, invalid_wazn, expected_wazn, invalid_shatr):
        # TODO

        text = ""
        text += f"الشطر المدخل {invalid_shatr} غير صحيح. "
        text += f"الوزن المدخل {invalid_wazn} غير صحيح. "
        text += f"الوزن الصحيح هو {expected_wazn}. "

        return text
    
    def build_critique_prompt(self, shatr, previous_shatrs=None):
        prompt = ""

        if previous_shatrs is not None:
            prompt += "اليك هذه القصيدة:\n"        
            prompt += " ".join(str(x) for x in previous_shatrs)
            prompt += f" {shatr}\n" 

        prompt += "ما رأيك في اخر شطر من هذه القصيدة؟"
        prompt += "الشطر المقصود هو: "
        prompt += f"{shatr}\n"
        prompt += "استخرج ٣ نقاط عن البيت اللتي يمكننا تطويرها."
        prompt += "اكتب النقاط بشكل مختصر وواضح." 

        return prompt

        
def load_poets():
    with open("poets.json", 'r', encoding="utf-8") as f:
        poets = json.load(f)["poets"]
        return poets


if __name__ == "__main__":
    r = Prompter()
    r.update("ب")
    print(r.wrap("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None, "أخي"))
    print('\n\n') 
    r = Prompter(poet="المتنبي")
    r.update("ق")
    print(r.wrap("اكتب لي قصيدة عن الفراق", ["في بحور الغي والإثم غريقا"], None))

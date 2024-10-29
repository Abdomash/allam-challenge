from Analyzer import Analyzer
from Prompter import *

#TODO make sure file works in other directories
CRITIC_SYS = open("critic_sys.txt", encoding="UTF-8").read()

#chatter critic additional mode (CHAT)
#user can send messages, receive them, etc.
#gives extensive feedback to user
#possible addition later. TODO
class CriticChat:
	def __init__(self):
		self.history = {}
	
	def critic(self, bayt, prev):
		pass

#critic to be used in generating the poems
#different than other one. Doesn't check bahr, gives much fewer details to save tokens, ..
#doesn't yap, goes straight to points, easily formatted
#uses single prompt. Doesn't use chat messages like
class CriticGen:
	def __init__(self, llm):
		self.llm = llm
		self.prompter = Prompter() #only using critic prompts
	
	def critic(self, bayt, prev_shatrs, prev_feedbacks = None): #bayt -> [shatr0, shatr1], prev_shatrs = [s0,s1,s2,s3,..], prev_feedbacks = for this specific bayt
		prompt = "<s> [INST]<<SYS>>\n"
		prompt += CRITIC_SYS
		prompt += "\n<</SYS>>\n"

		if prev_shatrs is not None:
			prompt += "اليك هذه القصيدة:\n"
			prompt += format_abyat(prev_shatrs + bayt)
			#prompt += f" {shatr}\n"
			prompt += '\n'
			if prev_feedbacks:
				for i in range(prev_feedbacks):
					if i == 0:
						prompt += "ما رأيك في اخر بيت من هذه القصيدة؟ "
						prompt += "البيت المقصود هو: "
						prompt += format_abyat(prev_feedbacks[i]["bayt"]) + '\n'
						prompt += "[/INST] شكرا لسؤالك، هذه هي اقتراحاتي لهذا البيت: " + '\n'
						prompt += prev_feedbacks[i]["feedback"]
						prompt += "[INST] "
					else:
						prompt += "حسنا، أعدت كتابة البيت الأخير في قصيدتي. ما رأيك به الآن؟ "
						prompt += '\n' + format_abyat(prev_feedbacks[i]["bayt"]) + '\n'
						prompt += "[/INST] شكرا لسؤالك، هذه هي اقتراحاتي لهذا البيت الجديد: " + '\n'
						prompt += prev_feedbacks[i]["feedback"]
						prompt += "[INST] "
			prompt += "تمام، أخذت نصائحك وأعدت صياغة البيت الأخير مرة أخرى. أعطني اقتراحات له"
			prompt += '\n' + format_abyat(bayt) + '\n'
		else:
			prompt += "اليك هذا المطلع لقصيدتي:" + "\n"
			prompt += format_abyat(bayt)
			prompt += "ما رأيك فيه؟" + "\n"

		prompt += "[/INST] هذه اقتراحاتي لتحسين البيت: "
		prompt += "\n1. "

        #TODO return points neatly formatted
		gen_ = self.llm.generate(prompt, True)
		gen_ = "\n1. " + gen_

		return gen_


		

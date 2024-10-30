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

		if prev_shatrs:
			prompt += "اليك هذه القصيدة:\n"
			if prev_feedbacks:
				prompt += format_abyat(prev_shatrs + prev_feedbacks[0]["bayt"]) #add first attempt for a bayt here
			else:
				prompt += format_abyat(prev_shatrs + bayt)
		else:
			prompt += "اليك هذا المطلع (اول بيت) لقصيدتي:" + "\n"
			prompt += format_abyat(bayt)
			#prompt += f" {shatr}\n"
			#prompt += '\n'
		if prev_feedbacks:
			first = True
			for f in prev_feedbacks:
				if first:
					prompt += "ما رأيك في اخر بيت من هذه القصيدة؟ " if prev_shatrs else "ما رأيك فيه؟"
					prompt += "البيت المقصود هو: " if prev_shatrs else ""
					prompt += format_abyat(f["bayt"]) if prev_shatrs else ""
					prompt += "<s>[/INST] شكرا لسؤالك، هذه هي اقتراحاتي لهذا البيت: " + '\n'
					prompt += f["feedback"]
					prompt += "</s>[INST] "
					first = False
				else:
					prompt += "حسنا، أعدت كتابة البيت الأخير في قصيدتي. ما رأيك به الآن؟ " if prev_shatrs else  "حسنا، أعدت كتابة البيت. ما رأيك به الآن؟ "
					prompt += '\n' + format_abyat(f["bayt"])
					prompt += "<s>[/INST] شكرا على سؤالك، هذه هي اقتراحاتي لهذا البيت الجديد: " + '\n'
					prompt += f["feedback"]
					prompt += "</s>[INST] "
			prompt += "تمام، أخذت نصائحك وأعدت صياغة البيت مرة أخرى. أعطني اقتراحات له"
			prompt += '\n' + format_abyat(bayt)
			prompt += "<s>"
		else:
			prompt += "ما رأيك في اخر بيت من هذه القصيدة؟ " if prev_shatrs else "ما رأيك فيه؟"
			prompt += "البيت المقصود هو: " if prev_shatrs else ""
			prompt += format_abyat(bayt) if prev_shatrs else ""

		prompt += "[/INST] شكرا على سؤالك، هذه اقتراحاتي لتحسين البيت: "
		prompt += "\n1. "

		print(prompt)

        #TODO return points neatly formatted
		gen_ = self.llm.generate(prompt, True)
		gen_ = "\n1. " + gen_

		return gen_


if __name__ == "__main__":
	from LLMInterface import FakeGenerator, ALLAM_GENERATOR, load_env
	import os
	load_env(".env")
	api_key = os.environ.get("API_KEY")
	#k = CriticGen(ALLAM_GENERATOR(api_key))
	k = CriticGen(FakeGenerator())
	
	k.critic(["",""], None, None) #m6l3 of qasidah (only 1 line), no feedback

	k.critic(["",""], None, [
		{"bayt":["",""], "feedback":""},
		{"bayt":["",""], "feedback":""}
	])
	#m6l3 of qasidah, with feedback

	k.critic(["",""], ["","","",""]) #prev_shatrs exists, but no feedback

	k.critic(["لالالالا", "علعلعلعلعل"], [
		"بلبلبلبلبل", "hi",
		"2","3"
		],
		[{"bayt":["ييييييي","hi"], "feedback":"good"},
   {"bayt":["ok 2nd", "3rd"], "feedback":"better"}]
	) #feedback exists + prev_shatrs exists
		

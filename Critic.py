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

	def hardcoded_qafiya_feedback(self, expected_qafiya):
		text = ""
		text += "البيت هذا لا يتماشي مع القافية المطلوبة"
		text += f" {expected_qafiya}. "
		text += "أعد كتابة البيت، وتأكد أن آخر كلمة في البيت تنتهي بهذه القافية"
		text += f" {expected_qafiya}. "

		return text

	def hard_coded_wazn_feedback(self, expected_wazn):
		text = ""
		text += "ركز جيداً في وزن هذا البيت. إنه مكسور ولا يطابق وزن بحر"
		text += f" {expected_wazn}. "
		text += "أعد كتابة البيت، وتأكد من انه منظوم وموزون على بحر"
		text += f" {expected_wazn}. "
		return text
	
	def critic(self, bayt, prev_shatrs, prev_feedbacks = None, hardcoded_feedback=None, plan_txt=None): #bayt -> [shatr0, shatr1], prev_shatrs = [s0,s1,s2,s3,..], prev_feedbacks = for this specific bayt
		prompt = "<s> [INST]<<SYS>>\n"
		prompt += CRITIC_SYS
		prompt += "\n<</SYS>>\n\n"

		more_than_single_line = (prev_shatrs and len(prev_shatrs) > 0) #slightly change formatting if discussing opening line of poem vs. line in middle of poem.

		if more_than_single_line:
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
					prompt += "ما رأيك في اخر بيت من هذه القصيدة؟ " if more_than_single_line else "ما رأيك فيه؟"
					prompt += "البيت المقصود هو: " if more_than_single_line else ""
					prompt += format_abyat(f["bayt"]) if more_than_single_line else ""
					if plan_txt:
						pass #TODO
					prompt += "[/INST]  شكرا على سؤالك، هذه هي اقتراحاتي لهذا البيت: " + '\n'
					prompt += f["feedback"]
					prompt += " </s><s> [INST] "
					first = False
				else:
					prompt += "حسنا، أعدت كتابة البيت الأخير في قصيدتي. ما رأيك به الآن؟ " if more_than_single_line else  "حسنا، أعدت كتابة البيت. ما رأيك به الآن؟ "
					prompt += '\n' + format_abyat(f["bayt"])
					if plan_txt:
						pass #TODO
					prompt += "[/INST]  شكرا على سؤالك، هذه هي اقتراحاتي لهذا البيت الجديد: " + '\n'
					prompt += f["feedback"]
					prompt += " </s><s> [INST] "
			prompt += "تمام، أخذت نصائحك وأعدت صياغة البيت مرة أخرى. أعطني اقتراحات له"
			prompt += '\n' + format_abyat(bayt)
		else:
			prompt += "ما رأيك في اخر بيت من هذه القصيدة؟ " if more_than_single_line else "ما رأيك فيه؟"
			prompt += "البيت المقصود هو: " if more_than_single_line else ""
			prompt += format_abyat(bayt) if more_than_single_line else ""

		prompt += "[/INST]  شكرا على سؤالك، هذه اقتراحاتي لتحسين البيت: "
		prompt += "\n1. "

		#print(prompt)

        #TODO return points neatly formatted
		gen_ = self.llm.generate(prompt, True)
		gen_ = "\n1. " + gen_

		#add hard-coded feedback here
		if hardcoded_feedback:
			gen_ += '\n' + '\n'.join(hardcoded_feedback)

		feedback = {"bayt":bayt, "feedback":gen_}

		return feedback


if __name__ == "__main__":
	from LLMInterface import FakeGenerator, ALLAM_GENERATOR, load_env
	import os
	load_env(".env")
	api_key = os.environ.get("API_KEY")
	#k = CriticGen(ALLAM_GENERATOR(api_key))
	k = CriticGen(FakeGenerator())

	k.critic(["m6l31","m6l32"], None, None) #m6l3 of qasidah (only 1 line), no feedback

	print("-----------------------")

	k.critic(["m6l31","m6l32"], None, [
		{"bayt":["00","01"], "feedback":"badd"},
		{"bayt":["02","03"], "feedback":"okay"}
	])
	#m6l3 of qasidah, with feedback

	print("-----------------------")

	k.critic(["0101","1010"], ["99","88","77","66"]) #prev_shatrs exists, but no feedback

	print("-----------------------")

	k.critic(["لالالالا", "علعلعلعلعل"], [
		"بلبلبلبلبل", "hi",
		"2","3"
		],
		[{"bayt":["ييييييي","hi"], "feedback":"good"},
   {"bayt":["ok 2nd", "3rd"], "feedback":"better"}]
	) #feedback exists + prev_shatrs exists

	print("-----------------------")
		

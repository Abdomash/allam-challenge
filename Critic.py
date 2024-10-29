from Analyzer import Analyzer
from Prompter import *

#TODO make sure file works in other directories
CRITIC_SYS = open("critic_sys.txt").read()

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
	
	def critic(self, bayt, prev_shatrs): #bayt -> [shatr0, shatr1], prev_shatrs = [s0,s1,s2,s3,..]
        prompt = "<s> [INST]<<SYS>>\n"
		prompt += CRITIC_SYS
        prompt += "\n<</SYS>>\n"

        if prev_shatrs is not None:
            prompt += "اليك هذه القصيدة:\n"
            prompt += format_abyat(prev_shatrs + bayt)
            #prompt += f" {shatr}\n"
            prompt += '\n'

        	prompt += "ما رأيك في اخر بيت من هذه القصيدة؟"
        	prompt += "البيت المقصود هو: "
        	prompt += f"{shatr}\n"
		else:
			prompt += "اليك هذا المطلع لقصيدتي:" + "\n"
			prompt += format_abyat(bayt)

        prompt += "\n[/INST] هذه اقتراحاتي لتحسين البيت: "
		prompt += "\n1. "

        #TODO, use LLM here, 
		gen_ = self.llm.generate(prompt, True)

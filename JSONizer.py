import json

class JSONizer:
	attempts = []
	analysis_res = []
	curr_shatr_num = 0
	iter_nums = {} #dictionary of int->int
	@staticmethod
	def attempt(attempt_txt, aroodi_style, wazn_10, wazn_mismatch, cut_attempt, text_mismatch, tf3lat, wazn_name, feedback=None):
		if JSONizer.curr_shatr_num not in JSONizer.iter_nums.keys():
			JSONizer.iter_nums[JSONizer.curr_shatr_num] = 0
		JSONizer.iter_nums[JSONizer.curr_shatr_num] += 1
		d = {"shatr_idx":JSONizer.curr_shatr_num,
	   "iteration_number":JSONizer.iter_nums[JSONizer.curr_shatr_num],
	   "attempt_text":attempt_txt,
	   "aroodi_style":aroodi_style,
	   "wazn_comb":wazn_10,
	   "wazn_mismatch":wazn_mismatch,
	   "cut_attempt_text":cut_attempt,
	   "text_mismatch": text_mismatch,
	   "tf3elat": tf3lat,
	   "feedback":feedback,
	   "wazn_name":wazn_name}
		JSONizer.attempts.append(d)
	
	@staticmethod
	def nextShatr():
		JSONizer.curr_shatr_num += 1

	@staticmethod
	def getGenResponse():
		return json.dumps(
			{ "type":"generate",
				"attempts":JSONizer.attempts
			}
		)

	@staticmethod
	def resetResponse():
		JSONizer.attempts.clear()
		JSONizer.curr_shatr_num = 0
		JSONizer.iter_nums.clear() #dictionary of int->int
	
	@staticmethod
	def getAnalyzerResponse():
		return json.dumps(
			{
				"type":"analyze",
				"analyzed_shatrs": JSONizer.attempts
			}
		)

if __name__ == "__main__":
	#JSONizer.attempt(32, 2, "hi", "hiii", "101011", "GGRRR")
	print(JSONizer.getGenResponse())
import json

class JSONizer:
	attempts = []
	analysis_res = []
	@staticmethod
	def attempt(shatr_num, iter_num, attempt_txt, aroodi_style, wazn_10, wazn_mismatch, cut_attempt):
		d = {"shatr_idx":shatr_num,
	   "iteration_number":iter_num,
	   "attempt_text":attempt_txt,
	   "aroodi_style":aroodi_style,
	   "wazn_comb":wazn_10,
	   "wazn_mismatch":wazn_mismatch,
	   "cut_attempt_text":cut_attempt}
		JSONizer.attempts.append(d)

	@staticmethod
	def getGenResponse():
		return json.dumps(
			{ "type":"generate",
				"attempts":JSONizer.attempts
			}
		)

	@staticmethod
	def resetGenResponse():
		JSONizer.attempts.clear()
	
	@staticmethod
	def analysis(shatr, wazn_10, wazn_mismatch):
		d = {
			"shatr_text":shatr,
			"wazn_comb":wazn_10,
			"wazn_mismatch":wazn_mismatch,
		}
		JSONizer.analysis_res.append(d)
	
	@staticmethod
	def getAnalyzerResponse():
		return json.dumps(
			{
				"type":"analyze",
				"analyzed_shatrs": JSONizer.analysis_res
			}
		)

	@staticmethod
	def resetAnalyzerResponse():
		JSONizer.analysis_res.clear()

if __name__ == "__main__":
	JSONizer.attempt(32, 2, "hi", "hiii", "101011", "GGRRR", "h")
	print(JSONizer.getGenResponse())
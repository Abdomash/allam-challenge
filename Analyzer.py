import sys

sys.path.append("qawafi/qawafi_server/Arabic_Diacritization") #lib should be ...../Arabi
sys.path.append("qawafi/qawafi_server")
sys.path.append("qawafi/qawafi_server/Bohour")

from qawafi_server.bait_analysis import BaitAnalysis
from qawafi_server.utils import (
    BOHOUR_NAMES,
    find_mismatch,
    label2name,
    char2idx,
    override_auto_tashkeel,
    vocab,
    BOHOUR_NAMES_AR,
)

BOHOURS_USED = ["kamel", "baseet", "taweel", "wafer", "ramal", "rajaz", "mutakareb", "mujtath"]

# Load the model once to avoid reloading it every time
analysis_model = BaitAnalysis("qawafi/qawafi_server/Arabic_Diacritization/config/test.yml")

class Analyzer:
    def __init__(self):
        self.analyzer = analysis_model
    
    def get_first_mistake2(self, comb, ideal, ret_inf=False):
        no_error = 9999 if ret_inf else -1
        
        #too_little = len(comb)-1 if ret_inf else -2
        too_little = len(comb)-1
        max_match_len = no_error
        for i in range(len(ideal)):
            if comb.find(ideal[:i]) in [0,1]: #first or second indexes only, ignore mistakes (khazm)
                max_match_len = i
            else:
                break #we didnt find this size
        
        #things to look for:
        #1010 actual, 110 ideal, error in -3
        #1110 actual, 1010 ideal, error in -3
        if max_match_len >= len(comb)-3: #if max_match is in last or before last ok! (check total length tho)
            if len(comb) > len(ideal)+1: #ignore deleting 1 (110 -> 10), or adding 10
                return len(ideal) #mistake is in too big of a length
            if len(comb) < len(ideal): #too short, even after deleting (1110110 -> 1110)
                return too_little #special meaning too little gen!
            return no_error
        else:
            return max_match_len

    def get_first_mistake(self, wazn_GR):
        #check error in the arood writing (R,G,B,Y)
        #G = correct, Y,B,R = wrong
        errors = [wazn_GR.find("R"), wazn_GR.find("B"), wazn_GR.find("Y")]
        #errors = [wazn_GR.find("B"), wazn_GR.find("Y")]

        ok_range = [-1, 0, 1, len(wazn_GR)-1, len(wazn_GR)-2, len(wazn_GR)-3, len(wazn_GR)-4, ]
        #TODO: remove 0 and 1

        if max(errors) in ok_range:
            return -1 #no errors!
        else:
            while min(errors) in ok_range:
                errors[errors.index(min(errors))] = 9999
            return min(errors) #might need to div 2 if not using harakat

    #comb = 1001001010101010
    #returns closest combs and bahr to the shatr provided
    def get_closest_bahr(self, shatr_comb, check_prefix=False, expected_bahr=None): #check_prefix = ensure similarity at beginning
            use_bahrs = [BOHOUR_NAMES[BOHOUR_NAMES_AR.index(expected_bahr)]] if expected_bahr is not None else BOHOURS_USED
            #if the poem expects a certain bahr then use it!
            out = []
            for meter in use_bahrs:
                #print(meter)
                if meter == "nathr":
                    continue
                for comb, tafeelat in zip(
                    self.analyzer.BOHOUR_PATTERNS[meter],
                    self.analyzer.BOHOUR_TAFEELAT[meter],
                ):
                    #first_mistake = 
                    #prob = self.analyzer.similarity_score(tf3, comb)
                    ar_meter = BOHOUR_NAMES_AR[BOHOUR_NAMES.index(meter)]
                    if check_prefix:
                        max_match_len = self.get_first_mistake2(shatr_comb, comb, True) #if no mistake, rank the match very high in sorting!
                    else:
                        max_match_len = self.analyzer.similarity_score(shatr_comb, comb)
                    out.append((comb, max_match_len, tafeelat, ar_meter))
            
            #return sorted(out, key=lambda x: x[1], reverse=True)
            closest = sorted(out, key=lambda x: x[1], reverse=True)[0]
            return closest #010101 comb, length of matching, tafeelat shape, meter name (arabic)

    def extract(self, shatr, expected_wazn_name=None): #returns qafiya type, wazn combs+name
        output = self.analyzer.analyze(shatrs=[shatr], short_qafiyah=True, override_tashkeel=True, predict_era=False, predict_closest=False, predict_theme=False)
        if not output: #error, return
            return None, None, None, 0, "", [0] #big error, return empty results, regen bayt

        #qafiya_type = output["qafiyah"]
        print(output["diacritized"][-1])
        wazn_name = output["meter"]
        aroodi_writing = output["arudi_style"][-1][0]
        combs = output["arudi_style"][-1][1]
        print(aroodi_writing)

        aroodi_indices = output["arudi_indices"][-1]

        closest_comb, _, _, wazn_name = self.get_closest_bahr(combs, True, expected_wazn_name) #0101
        print("ACTUAL:  " +combs)
        print("CLOSEST: "+closest_comb)
        print("indices: "+str(output["arudi_indices"][-1]))
        #wazn_mismatch = find_mismatch(closest_comb, combs, False)
        wazn_mismatch = self.get_first_mistake2(combs, closest_comb)

        print(wazn_mismatch)

        #extract qafiyah from last 2 letters without diacritics
        diacritics = ['َ', 'ً', 'ُ', 'ٌ', 'ِ', 'ٍ', 'ْ', 'ّ']
        without_dia = aroodi_writing + ""
        for dia in diacritics:
            without_dia = without_dia.replace(dia, "")
        
        if without_dia[-1] in [ "ا" ,  "ه"]:
            qafiya = without_dia[-2:]
        else:
            if without_dia[-1] in [ "و" ,  "ي"]:
                qafiya = without_dia[-3:-1] if without_dia[-2] in ["ه"] else without_dia[-2]
                #edge case: letter-ha-vowel -> letter-ha is the qafiya
                #else: letter-vowel becomes letter (TODO lookup)
            else:
                if without_dia[-1] == "ن": #tanween edge case
                    qafiya = without_dia[-2:] #letter-n
                else:
                    qafiya = without_dia[-1]
        #TODO: hamza ignore for now. can be done later
        #edge case with hamza+waw, hamza+alif maqsoora, ..
        #also needs RAG updating
        return qafiya, wazn_name, combs, wazn_mismatch, output["diacritized"][-1], aroodi_indices


if __name__ == "__main__":
    e = Analyzer()

    #Test cases
    print(e.extract("أَلا رُبَّ يَوْمٍ لَكَ مِنْهُنَّ صَالِحٍ")) #misclassified as nathri test
    print(e.extract("أَلا رُبَّ يَوْمٍ لَكَ مِنْهُنَّ صَالِحٍ", "الطويل")) #force attempt on specific bahr

    print(e.extract("واحرَّ قَلباهُ مِمَّن قَلبُهُ شَبِمُ")) #baseet, no wrong, mim qafiyah

    print(e.extract("القلب أعلم يا عذول بدائه")) #kamel, hamza (IGNORE EDGE CASE)

    print(e.extract("القلب في متنكّرٍ يا أعلمَهْ")) #kamel, letter-ha edge case qafiyah

    print(e.extract("أخي أنت حرٌّ وَراءَ السدود")) #dal, mutaqarib (I think ne need for waw?)

    print(e.extract("في بحور الغي والإثم غريقا")) #ramal, letter-alif edge case

    print(e.extract("والروح تبكي لوعة وفراق ")) #kamel, qaf
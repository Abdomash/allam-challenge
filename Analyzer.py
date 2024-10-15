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

    def get_first_mistake(self, wazn_GR):
        #check error in the arood writing (R,G,B,Y)
        #G = correct, Y,B,R = wrong
        errors = [wazn_GR.find("R"), wazn_GR.find("B"), wazn_GR.find("Y")]
        #errors = [wazn_GR.find("B"), wazn_GR.find("Y")]

        ok_range = [-1, 0, 1, len(wazn_GR)-1, len(wazn_GR)-2, len(wazn_GR)-3, len(wazn_GR)-4]
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
        if check_prefix:
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
                    max_match_len = -1
                    for i in range(len(comb)):
                        if shatr_comb.find(comb[:i]) in [0,1]: #first or second indexes only
                            max_match_len = i
                        else:
                            break #we didnt find this size
                    #prob = self.analyzer.similarity_score(tf3, comb)
                    ar_meter = BOHOUR_NAMES_AR[BOHOUR_NAMES.index(meter)]
                    out.append((comb, max_match_len, tafeelat, ar_meter))
            
            #return sorted(out, key=lambda x: x[1], reverse=True)
            closest = sorted(out, key=lambda x: x[1], reverse=True)[0]
            return closest #010101 comb, length of matching, tafeelat shape, meter name (arabic)
        else:
            pass

    def extract(self, shatr, expected_wazn_name=None): #returns qafiya type, wazn combs+name
        output = self.analyzer.analyze(shatrs=[shatr], short_qafiyah=True, override_tashkeel=True, predict_era=False, predict_closest=False, predict_theme=False)
        #qafiya_type = output["qafiyah"]
        print(output["diacritized"][-1])
        wazn_name = output["meter"]
        aroodi_writing = output["arudi_style"][-1][0]
        combs = output["arudi_style"][-1][1]

        if wazn_name == "نثر" or expected_wazn_name is not None: #get closest bahr, re-do mismatch finding
            closest_comb, _, _, wazn_name = self.get_closest_bahr(combs, True, expected_wazn_name) #0101
            wazn_mismatch = find_mismatch(closest_comb, combs, False)
        else:
            wazn_mismatch = output["patterns_mismatches"][-1] #edge case with nathr, need to have legit bahr else all letters are mistakes

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
            else:
                if without_dia[-1] == "ن": #tanween edge case
                    qafiya = without_dia[-2:] #letter-n
                else:
                    qafiya = without_dia[-1]
        #TODO: hamza ignore for now. can be done later
        #edge case with hamza+waw, hamza+alif maqsoora, ..
        #also needs RAG updating
        return qafiya, wazn_name, combs, wazn_mismatch, output["diacritized"][-1]


if __name__ == "__main__":
    e = Analyzer()

    print(e.extract("أَلا رُبَّ يَوْمٍ لَكَ مِنْهُنَّ صَالِحٍ"))
    print(e.extract("أَلا رُبَّ يَوْمٍ لَكَ مِنْهُنَّ صَالِحٍ", "الطويل")) #wrong classification: test!

    print(e.extract("واحرَّ قَلباهُ مِمَّن قَلبُهُ شَبِمُ"))

    print(e.extract("القلب أعلم يا عذول بدائه"))

    print(e.extract("القلب في متنكّرٍ يا أعلمَهْ"))

    print(e.extract("أخي أنت حرٌّ وَراءَ السدود"))

    print(e.extract("في بحور الغي والإثم غريقا"))

    print(e.extract("والروح تبكي لوعة وفراق "))

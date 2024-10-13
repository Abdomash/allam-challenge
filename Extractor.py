import sys

class Extractor:
    def __init__(self):
        sys.path.append("qawafi/qawafi_server/Arabic_Diacritization") #lib should be ...../Arabi
        sys.path.append("qawafi/qawafi_server")
        from qawafi_server.bait_analysis import BaitAnalysis
        self.analyzer = BaitAnalysis("qawafi/qawafi_server/Arabic_Diacritization/config/test.yml")

    def extract(self, shatr): #returns qafiya type, wazn type
        output = self.analyzer.analyze(shatrs=[shatr], short_qafiyah=True, override_tashkeel=True, predict_era=False, predict_closest=False, predict_theme=False)
        #qafiya_type = output["qafiyah"]
        print(output["diacritized"][-1])
        wazn_name = output["meter"]
        aroodi_writing = output["arudi_style"][-1][0]
        #wazn_info = output["closest_patterns"][-1] #('arood 1/0', 0.9953)
        wazn_info = output["patterns_mismatches"][-1]

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
                qafiya = without_dia[-1]
        #TODO: hamza ignore for now. can be done later
        #edge case with hamza+waw, hamza+alif maqsoora, ..
        #also needs RAG updating

        return qafiya, wazn_name, wazn_info


if __name__ == "__main__":
    e = Extractor()

    print(e.extract("أَلا رُبَّ يَوْمٍ لَكَ مِنْهُنَّ صَالِحٍ"))

    print(e.extract("واحرَّ قَلباهُ مِمَّن قَلبُهُ شَبِمُ"))

    print(e.extract("القلب أعلم يا عذول بدائه"))

    print(e.extract("القلب في متنكّرٍ يا أعلمَهْ"))

    print(e.extract("أخي أنت حرٌّ وَراءَ السدود"))

    print(e.extract("في بحور الغي والإثم غريقا"))

    print(e.extract("والروح تبكي لوعة وفراق "))
import sys
import os
import json

from flask import Flask, request

from JSONizer import *
from LLMInterface import FakeGenerator
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter, format_abyat
from Critic import CriticGen, CriticChat
from Analyzer import Analyzer
from main import generate_qasida
from Data import load_poets, load_bohours

# Initialize The Flask App
app = Flask(__name__)
#app.secret_key = 'your_secret_key'
#app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session

# Initialize heavy components
prompter = Prompter()
analyzer = Analyzer()

llm = FakeGenerator()

critic = CriticGen(llm=llm)
shatr_generator = ShatrGenerator(llm, prompter=prompter, analyzer=analyzer)

@app.route('/generate', methods=['GET'])
def generate():
    JSONizer.resetResponse()
    user_input = request.form['prompt']
    selected_bahr = request.form['bahr']
    selected_poet = request.form['poet']
    prompter.update(None, selected_poet, selected_bahr)
    len_ = 3

    output = generate_qasida(user_input, shatr_generator, critic, selected_bahr, None, len_ )
    return JSONizer.getGenResponse()

@app.route('/analyze', methods=['GET'])
def analyze():
    JSONizer.resetResponse()
    shatrs = json.loads(request.form['shatrs'])

    print(shatrs)

    abyat = format_abyat(shatrs)

    expected_wazn = None

    for b in range(0, len(shatrs), 2): #for each bayt
        prev_shatrs = shatrs[:b]
        s_ = shatrs[b: b+2]

        #TODO: move this to critic full

        #copied from generate_qasida
        _, new_wazn_name1, new_wazn_combs1, new_wazn_mismatch1, diacritized1, arudi_indices1, tf3elat1, aroodi_writing1 = analyzer.extract(s_[0], expected_wazn_name=expected_wazn)
        expected_wazn = new_wazn_name1

        new_qafiya, new_wazn_name2, new_wazn_combs2, new_wazn_mismatch2, diacritized2, arudi_indices2, tf3elat2, aroodi_writing2 = analyzer.extract(s_[1], expected_wazn_name=expected_wazn)

        hardcoded_feedback = ""

        #TODO Hardcoded Qafiya + Wazn feedbacks!

        feedback = critic.critic(s_, prev_shatrs, None, hardcoded_feedback)

        text_mis1 = arudi_indices1[new_wazn_mismatch1]
        text_mis2 = arudi_indices2[new_wazn_mismatch2]

        if new_wazn_mismatch1 == -1:
            text_mis1 = -1
        if new_wazn_mismatch2 == -1:
            text_mis2 = -1

        #JSONizer.analysis(diacritized1, new_wazn_combs1, new_wazn_mismatch1, feedback["feedback"], text_mis1, tf3elat1)
        JSONizer.attempt(diacritized1, aroodi_writing1, new_wazn_combs1, new_wazn_mismatch1, diacritized1, text_mis1, tf3elat1, new_wazn_name1, feedback=feedback["feedback"])
        JSONizer.nextShatr()
        JSONizer.attempt(diacritized2, aroodi_writing2, new_wazn_combs2, new_wazn_mismatch2, diacritized2, text_mis2, tf3elat2, new_wazn_name2, feedback=feedback["feedback"])
        JSONizer.nextShatr()
        #JSONizer.analysis(diacritized2, new_wazn_combs2, new_wazn_mismatch2, feedback["feedback"], text_mis2, tf3elat2)

    return JSONizer.getAnalyzerResponse()


if __name__ == '__main__':
    app.testing = True
    #app.run(debug=True)

    c = app.test_client()
    resp = c.get('/generate', data={
        "type":"generate",
        "prompt":"اكتب قصيدة عن الوطن",
        "bahr":"الطويل",
        "poet":"عنترة بن شداد",
    })
    print(resp.data.decode())


    print("---------")
    resp = c.get('/analyze', data={
        "type":"analyze",
        "shatrs":json.dumps([
            'حييت يا وطني الحبيب تحيةً', 'ﻓنـحيب قلبي والضلوع تحومل','يَا سَامِعِي أَصْوَاتِ أَبْيَاتِي الْغَرَّ', 'يَامَنْ بِلُبّي تُعَدُّوْنَ وَتُسْتَهَلْ'
            ])
    })
    print(resp.data.decode())

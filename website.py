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
    JSONizer.resetGenResponse()
    user_input = request.form['prompt']
    selected_bahr = request.form['bahr']
    selected_poet = request.form['poet']
    len_ = 3

    prompt = ""
    output = generate_qasida(prompt, shatr_generator, critic, selected_bahr, None, len_ )
    return JSONizer.getGenResponse()

@app.route('/analyze', methods=['GET'])
def analyze():
    JSONizer.resetAnalyzerResponse()
    shatrs = request.form['shatrs']

    abyat = format_abyat(shatrs)

    for b in range(len(abyat)):
        prev_shatrs = abyat[:b]

        critic.critic(abyat[b], prev_shatrs, None, TODO)

    return JSONizer.getAnalyzerResponse()


if __name__ == '__main__':
    app.run(debug=True)


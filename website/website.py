import sys
import os
import json
from time import sleep

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

# Add reference to parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from LLMInterface import FakeGenerator
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter
from Analyzer import Analyzer
from main import generate_qasida

# Initialize The Flask App
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session
Session(app)

# Initialize heavy components
rag = Prompter()
analyzer = Analyzer()
llm = FakeGenerator()
shatr_generator = ShatrGenerator(llm, prompter=rag, analyzer=analyzer)

def load_poets():
    POETS_FILEPATH = 'poets.json'
    poets = {}
    with open(POETS_FILEPATH, 'r', encoding='utf-8') as f:
        poets = json.load(f)
    return [item['name'] for item in poets['poets']]

BAHRS = ['الكامل', 'الوافر', 'الطويل', 'البسيط' ]
POETS = load_poets() 

def process_prompt(prompt, selected_bahr, selected_poet):
    if selected_poet == 'None':
        selected_poet = None
    if selected_bahr == 'None':
        selected_bahr = None

    qasida = generate_qasida(prompt, shatr_generator, wazn=selected_bahr, poet=selected_poet)
    return qasida

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_log' not in session:
        session['chat_log'] = []

    if request.method == 'POST':
        user_input = request.form['prompt']
        selected_bahr = request.form['bahr']
        selected_poet = request.form['poet']
        output = process_prompt(user_input, selected_bahr, selected_poet)
        # Append to the chat log
        session['chat_log'].append({'prompt': user_input, 'response': output})
    
    # Reverse the chat log to display newest messages first
    return render_template('index.html', chat_log=reversed(session['chat_log']), poets=POETS, bahrs=BAHRS)

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_log', None)  # Remove the chat log from session
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)

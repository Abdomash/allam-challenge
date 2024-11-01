import sys
import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO

# Initialize The Flask App
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session
Session(app)
socketio = SocketIO(app)


# Add reference to parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Initialize the logger
from Logger import Logger
Logger.initialize('website', socketio=socketio)
LOGGER = Logger.get_logger()

from Critic import CriticGen
from LLMInterface import FakeGenerator
from ShatrGenerator import ShatrGenerator
from Prompter import Prompter
from Analyzer import Analyzer
from main import generate_qasida
from Data import load_poets, load_bohours


# Initialize heavy components
prompter = Prompter()
analyzer = Analyzer()
llm = FakeGenerator()
critic = CriticGen(llm)
shatr_generator = ShatrGenerator(llm, prompter=prompter, analyzer=analyzer)

BAHRS = list(load_bohours().keys())
POETS = list(load_poets().keys())

current_bahr = None
current_poet = None
def process_prompt(prompt, selected_bahr, selected_poet):
    global current_bahr
    global current_poet

    if selected_poet == 'None':
        selected_poet = None
    if selected_bahr == 'None':
        selected_bahr = None

    LOGGER.info(f"Processing Request: {prompt}, {selected_bahr}, {selected_poet}")
    if selected_poet != current_poet or selected_bahr != current_bahr:
        LOGGER.info(f"Updating Wazn and Poet: {selected_bahr}, {selected_poet}")
        current_bahr = selected_bahr
        current_poet = selected_poet
        llm = FakeGenerator(poet=selected_poet, wazn=selected_bahr)
        prompter.update(wazn=selected_bahr, poet=selected_poet)
        shatr_generator.llm = llm

    qasida = generate_qasida(prompt, shatr_generator, critic=critic, wazn=current_bahr)
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
        session['chat_log'].append({'prompt': user_input, 'response': output})
    
    return render_template('index.html', chat_log=reversed(session['chat_log']), poets=POETS, bahrs=BAHRS)

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_log', None) 
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)

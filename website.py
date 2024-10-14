from ShatrGenerator import ShatrGenerator
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

from LLMInterface import FakeGenerator
from main import generate_qasida

from time import sleep


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session
Session(app)

llm = FakeGenerator()
shatr_generator = ShatrGenerator(llm)

def process_prompt(prompt, selected_bahr, selected_poet):
    qasida = generate_qasida(prompt, shatr_generator)
    return qasida

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_log' not in session:
        session['chat_log'] = []

    if request.method == 'POST':
        user_input = request.form['prompt']
        selected_bahr = request.form['bahr']
        output = process_prompt(user_input, selected_bahr, None)
        # Append to the chat log
        session['chat_log'].append({'prompt': user_input, 'response': output})
    
    # Reverse the chat log to display newest messages first
    return render_template('index.html', chat_log=reversed(session['chat_log']))

@app.route('/clear', methods=['POST'])
def clear_chat():
    global llm
    global shatr_generator
    llm = FakeGenerator()
    shatr_generator = ShatrGenerator(llm)
    
    session.pop('chat_log', None)  # Remove the chat log from session
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)


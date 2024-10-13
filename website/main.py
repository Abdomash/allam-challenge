from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side session
Session(app)

# Your function that takes a prompt and returns a response
def process_prompt(prompt):
    # Replace with your LLM code
    return f"وعليكم السلام"

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_log' not in session:
        session['chat_log'] = []

    if request.method == 'POST':
        user_input = request.form['prompt']
        output = process_prompt(user_input)
        # Append to the chat log
        session['chat_log'].append({'prompt': user_input, 'response': output})
    
    # Reverse the chat log to display newest messages first
    return render_template('index.html', chat_log=reversed(session['chat_log']))

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_log', None)  # Remove the chat log from session
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)


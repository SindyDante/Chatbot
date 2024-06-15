from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from rasa.nlu.model import Interpreter
from rasa.core.agent import Agent
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Configure OpenAI API
openai.api_key = 'your_openai_api_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('chatbot'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user_id' in session:
        if request.method == 'POST':
            user_input = request.form['user_input']
            response = generate_chatbot_response(user_input)
            return render_template('chatbot.html', response=response)
        return render_template('chatbot.html')
    else:
        return redirect(url_for('login'))
    
# Load the Rasa NLU model
interpreter = Interpreter.load("rasa/models/nlu")
agent = Agent.load("rasa/models/dialogue")

def generate_chatbot_response(user_input):
    try:
        # Use Rasa to parse the user's input and generate a response
        nlu_output = interpreter.parse(user_input)
        intent = nlu_output["intent"]["name"]
        entities = nlu_output["entities"]

        if intent == "greet":
            return "Hello! How can I assist you today?"
        elif intent == "goodbye":
            return "Goodbye! Have a great day."
        elif intent == "ask_chatbot":
            return "How can I help you?"
        elif intent == "inform":
            name = next((entity["value"] for entity in entities if entity["entity"] == "name"), None)
            if name:
                return f"Nice to meet you, {name}! How can I assist you today?"
            else:
                return "How can I help you?"
        elif intent == "thankyou":
            return "You're welcome! I'm always happy to help."
        else:
            # Use OpenAI's GPT-3 to generate a response
            prompt = f"User: {user_input}\nAssistant: "
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            chatbot_response = response.choices[0].text.strip()
            return chatbot_response
    except Exception as e:
        print(f"Error generating chatbot response: {e}")
    
        return "I'm sorry, there was an error generating a response. Please try again later."

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
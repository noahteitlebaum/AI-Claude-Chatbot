from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Memory (excluding system prompt)
chat_memory = []

# Define the system prompt
SYSTEM_PROMPT = (
    "You are Noah-GPT, a smart, helpful, and friendly AI assistant. "
    "You give clear and concise answers, explain things well, and help users accomplish tasks efficiently. "
    "Use a warm tone, occasionally add a bit of humor when appropriate, and always aim to be supportive."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_memory
    user_message = request.json['message'].strip()

    # Add user message to memory
    chat_memory.append({"role": "user", "content": user_message})

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=chat_memory
        )

        ai_reply = response.content[0].text.strip()

        # Add assistant reply to memory
        chat_memory.append({"role": "assistant", "content": ai_reply})

        return jsonify({'reply': ai_reply})

    except Exception as e:
        return jsonify({'reply': f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

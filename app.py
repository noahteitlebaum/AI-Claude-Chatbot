from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    return jsonify({'reply': response.content[0].text.strip()})

if __name__ == "__main__":
    app.run(debug=True)

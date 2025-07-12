from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(
    api_key="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"  # replace with your real key
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

from flask import Flask, request, jsonify
from model import create_model
from data_preprocessing import preprocess_text

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    source_text = data['text']
    # Preprocess text and predict translation
    translated_text = "translated text"  # Placeholder
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)

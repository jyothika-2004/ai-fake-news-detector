from flask import Flask, request, jsonify, send_from_directory
import joblib
import re
import os

app = Flask(__name__, static_url_path='', static_folder='.')

# Load models safely
try:
    vectorizer = joblib.load('vectorizer.pkl')
    model = joblib.load('model.pkl')
except Exception as e:
    print(f"Warning: Could not load models. Did you run the pipeline? Error: {e}")
    vectorizer = None
    model = None

def clean_text(text):
    text = str(text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({"error": "Model not loaded on the server"}), 500

    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    
    # 1. Clean the text
    cleaned = clean_text(text)
    
    # 2. Vectorize
    vec = vectorizer.transform([cleaned])
    
    # 3. Predict
    prediction = model.predict(vec)[0]
    
    # 4. Get confidence (Probability)
    proba = model.predict_proba(vec)[0]
    confidence_score = int(max(proba) * 100)
    
    label = "Unknown"
    is_fake = False
    
    # Normalize prediction to standard strings
    if str(prediction).lower() in ['0', 'fake', 'false']:
        label = 'Fake News'
        is_fake = True
    elif str(prediction).lower() in ['1', 'real', 'true']:
        label = 'Real News'
        is_fake = False
    else:
        label = str(prediction)
        
    return jsonify({
        "prediction": label,
        "confidence": confidence_score,
        "indicators": [
            "Analyzed vocabulary using TF-IDF Vectorization.",
            "Compared against 24,000+ known real and fake articles.",
            f"Logistic Regression model computed {confidence_score}% certainty."
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

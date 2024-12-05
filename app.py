from flask import Flask, request, render_template
from flask_cors import CORS
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load the trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract inputs from the form
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        age = float(request.form['age'])

        # Prepare inputs for prediction
        input_features = np.array([[pregnancies, glucose, bmi, age]])
        scaled_features = scaler.transform(input_features)
        prediction = model.predict(scaled_features)

        # Return the prediction
        if prediction[0] == 1:
            return "You have Diabetes, please consult a Doctor."
        else:
            return "You don't have Diabetes."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

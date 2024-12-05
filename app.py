from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import logging

# Load the trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

model = pickle.load(open(model_path, 'rb'))
scaler = pickle.load(open(scaler_path, 'rb'))

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the main HTML page (index.html)
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles predictions based on user input
    """
    try:
        # Extract form data as a list of floats
        input_features = [float(x) for x in request.form.values()]
        # Scale the input features
        scaled_features = scaler.transform([np.array(input_features)])
        # Predict using the model
        prediction = model.predict(scaled_features)

        # Create result message based on prediction
        if prediction[0] == 1:
            result = "You have Diabetes, please consult a Doctor."
        else:
            result = "You don't have Diabetes."
    except Exception as e:
        # Log the error for debugging purposes
        logging.error(f"Error during prediction: {e}")
        result = f"An error occurred: {e}"

    return render_template('index.html', prediction_text=result)

if __name__ == "__main__":
    # Get the port from the environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Start the Flask server
    app.run(host="0.0.0.0", port=port, debug=True)

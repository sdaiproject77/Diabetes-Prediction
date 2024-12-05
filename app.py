from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    # Render the main HTML page (index.html)
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
        # Handle errors and display them in the UI
        result = f"An error occurred: {e}"

    return render_template('index.html', prediction_text=result)

if __name__ == "__main__":
    # Start the Flask server
    app.run(debug=True)

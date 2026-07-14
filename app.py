from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load trained objects
model = joblib.load("loan_default_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

FEATURE_ORDER = [
    'Age','Income','LoanAmount','CreditScore','MonthsEmployed',
    'NumCreditLines','InterestRate','LoanTerm','DTIRatio',
    'Education','EmploymentType','MaritalStatus',
    'HasMortgage','HasDependents','LoanPurpose','HasCoSigner'
]

THRESHOLD = 0.1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Encode categorical features
        for col, encoder in label_encoders.items():
            value = data[col].lower().strip()
            if value not in encoder.classes_:
                return jsonify({
                    "error": f"Invalid value for {col}: {value}"
                })
            data[col] = encoder.transform([value])[0]

        # Prepare input
        input_data = np.array([data[col] for col in FEATURE_ORDER]).reshape(1, -1)
        input_scaled = scaler.transform(input_data)

        probability = model.predict_proba(input_scaled)[0][1]
        prediction = 1 if probability >= THRESHOLD else 0

        return jsonify({
            "prediction": prediction,
            "probability": round(float(probability), 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

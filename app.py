from flask import Flask, request, render_template
import requests
import re

app = Flask(__name__)

# URL of your deployed Cloud Function
CLOUD_FUNCTION_URL = "https://llama31-functions-p6j2ri24ha-uc.a.run.app/predict"

def extract_output(text):
    """Extract only the output part from the prediction response."""
    # Find the part after "Output:" in the prediction
    match = re.search(r'Output:\s*(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No output available."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_prompt = request.form.get("prompt")
        if user_prompt:
            # Make a POST request to the Cloud Function
            response = requests.post(CLOUD_FUNCTION_URL, json={"instances": {"prompt": user_prompt}})
            if response.status_code == 200:
                predictions = response.json().get("predictions", [])
                if predictions:
                    # Extract the output part from the prediction
                    result = extract_output(predictions[0])
                else:
                    result = "No predictions available"
            else:
                result = "Error: Could not retrieve predictions"
        else:
            result = "Please enter a prompt."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

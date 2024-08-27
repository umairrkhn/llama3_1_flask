from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# URL of the Cloud Function deployed on Cloud Run
CLOUD_FUNCTION_URL = "https://llama31-functions-p6j2ri24ha-uc.a.run.app/predict"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        data = {"instances": {"input_text": user_input}}
        response = requests.post(CLOUD_FUNCTION_URL, json=data)
        prediction = response.json().get("predictions")
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

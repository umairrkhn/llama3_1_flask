from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# URL of your deployed Cloud Function
CLOUD_FUNCTION_URL = "https://llama31-functions-p6j2ri24ha-uc.a.run.app/predict"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_prompt = request.form.get("prompt")
        if user_prompt:
            # Make a POST request to the Cloud Function
            response = requests.post(
                CLOUD_FUNCTION_URL, json={"instances": {"prompt": user_prompt}}
            )
            if response.status_code == 200:
                result = response.json().get(
                    "predictions", ["No predictions available"]
                )
            else:
                result = ["Error: Could not retrieve predictions"]
        else:
            result = ["Please enter a prompt."]
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

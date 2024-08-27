import os
from flask import Flask, render_template, request
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

app = Flask(__name__)

# Define a function to interact with Vertex AI
def predict_custom_trained_model(project, endpoint_id, instances, location="us-central1", api_endpoint="us-central1-aiplatform.googleapis.com"):
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instances = instances if isinstance(instances, list) else [instances]
    instances = [json_format.ParseDict(instance_dict, Value()) for instance_dict in instances]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    return response.predictions

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        input_text = request.form["input_text"]
        instances = {"input": input_text}
        prediction = predict_custom_trained_model(
            project="17113908719",
            endpoint_id="5768264498708217856",
            instances=instances,
        )[0]
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

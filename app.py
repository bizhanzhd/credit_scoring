
from prediction_pipeline.predictor import predictor
from prediction_pipeline.input_controller import prediction_input_controller
from training_pipeline.trainer import trainer
from training_pipeline.input_controller import train_input_controller

from flask import Flask, request, jsonify
import pandas as pd


# Config
app = Flask(__name__)
app.config['ENV'] = 'development'

@app.route("/default_probability", methods=["POST", "PUT"])
def default_probability_prediction():
    
    if request.method == "POST":

        controller = prediction_input_controller()
        estimator = predictor()
   
        # Input
        body = request.get_json(force=True, silent=False, cache=True)
        
        # call the controller
        result = controller.run(body)
        if result["flag"] == True: return result["response"], result["response_code"]

        # Call the calculator
        estimate = estimator.run(data=body)
        print(estimate)

        return jsonify(estimate), 200
    
    elif request.method == "PUT":
        
        controller = train_input_controller()
        train = trainer()
   
        # Input
        df = pd.read_csv(request.files['train_initial.csv'])
        
        # call the controller
        result = controller.run(df)
        if result["flag"] == True: return result["response"], result["response_code"]

        # Call the calculator
        answer = train.run(df=df)

        return jsonify(answer), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
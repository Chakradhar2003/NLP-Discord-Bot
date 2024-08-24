import os
import importlib.util
import numpy as np
from flask import Flask, request, jsonify

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../spam_classifier_model/main.py'))
spec = importlib.util.spec_from_file_location("main", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = Flask(__name__)

# Routing For Checking Spam
@app.route('/spam', methods=['POST'])
def compute():
    data = request.get_json()  
    input_value = data.get('input_value')  
    if input_value is None:
        return jsonify({"error": "Please provide an 'input_value'."}), 400    
    result = module.predict_spam(input_value) 
    if isinstance(result, np.ndarray):
        result = result.tolist() 
    return jsonify({"result": result})  


if __name__ == '__main__':
    app.run(debug=True)

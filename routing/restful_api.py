from flask import Flask, request, jsonify

app = Flask(__name__)

def my_function(input_value):
    result = input_value * 2
    return result

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()  
    input_value = data.get('input_value')  
    
    if input_value is None:
        return jsonify({"error": "Please provide an 'input_value'."}), 400
    
    result = my_function(input_value)  
    return jsonify({"result": result})  

if __name__ == '__main__':
    app.run(debug=True)

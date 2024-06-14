from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data_list = []

@app.route('/sensor/data', methods=['POST'])
def receive_data():
    temperature = request.form.get('temperature')  # Look for "temperature" key
    if temperature is not None:
        try:
            temperature = float(temperature)
            data = {"temperature": temperature}
            data_list.append(data)
            return jsonify({"message": "Temperature data received"}), 200
        except ValueError:
            return jsonify({"message": "Invalid temperature format"}), 400
    else:
        return jsonify({"message": "Missing temperature data"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

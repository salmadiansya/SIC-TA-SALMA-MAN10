# INFORMATION
### Assignments
**Technical Assignments 01 SIC 5 (2024)**<br>
**Description** : Connecting DHT11 sensor data from ESP32 to Flask
### Participant Identity
> **Name:** Salma Diandra Syawalia<br>
> **Team:** VALIANT<br>
> **School:** MAN 10 JAKARTA

# CIRCUIT IMAGE

# ARDUINO CODE
`````
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 26 // Use a more doescriptive pin name
#define DHTTYPE DHT11

DHT tempSensor(DHTPIN, DHTTYPE);

const char* ssid = "Salma_Koe";
const char* password = "SalmaFiryalAbyan22";
const char* serverName = "http://192.168.99.22:5000/sensor/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  tempSensor.begin(); // Initialize DHT sensor
  delay(2000); // Allow sensor to stabilize (optional)
}

void loop() {
  float temperature = tempSensor.readTemperature();
  if (isnan(temperature)) {
    Serial.println("Failed to read temperature from DHT sensor!");
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String postData = "temperature_level=" + String(temperature);
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error sending POST request: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
  delay(10000); // Send data every 10 seconds (adjust as needed)
}
`````
# PYTHON FLASK CODE
`````
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
`````

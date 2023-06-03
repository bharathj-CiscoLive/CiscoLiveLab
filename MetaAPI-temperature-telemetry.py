import requests
import json
import time
import matplotlib.pyplot as plt
from collections import defaultdict

API_KEY = "D0F1A170E5704571BC5006C37A4A3AC3"
URL = "https://partners.dnaspaces.io/api/partners/v1/firehose/events"
HEADERS = {"X-API-Key": API_KEY}

temperature_data = defaultdict(list)

def fetch_data():
    try:
        response = requests.get(URL, headers=HEADERS, stream=True)
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                parse_data(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        time.sleep(60)
        fetch_data()

def parse_data(data):
    if data.get("eventType") == "IOT_TELEMETRY":
        device_mac = data["iotTelemetry"]["deviceInfo"]["deviceMacAddress"]
        
        # Check if the temperature key exists before extracting its value
        if "temperature" in data["iotTelemetry"]:
            temperature = data["iotTelemetry"]["temperature"]["temperatureInCelsius"]
            update_data(device_mac, temperature)
        else:
            print(f"No temperature data for device: {device_mac}")


def update_data(device_mac, temperature):
    temperature_data[device_mac].append(temperature)
    plot_data()

def plot_data():
    plt.clf()
    for device_mac, temp_values in temperature_data.items():
        plt.plot(temp_values, label=device_mac)

    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature for IoT Devices")
    plt.pause(1)

if __name__ == "__main__":
    plt.ion()
    fetch_data()

import paho.mqtt.client as mqtt
import requests

# Telegram Bot Credentials
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN" # Not provided on this public repository for security purposes, contact me via email if you want to test it.
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID" # The README file contains the steps to obtain this ID 

# MQTT Broker Details
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "openmv/people_count"

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Message sent to Telegram")
    else:
        print("Failed to send message:", response.text)

# Callback when an MQTT message is received
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message}")
    send_telegram_message(message)

# MQTT Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

print("Listening for MQTT messages...")
client.loop_forever()

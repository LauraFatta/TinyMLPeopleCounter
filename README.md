# People Counting System for Metro Stations
##Overview

This project is designed to accurately count the number of people in metro stations using OpenMV and TinyML on the Arduino Nicla Vision device. The system detects and tracks people, preventing multiple detections of the same person to ensure an accurate count. The results are transmitted via MQTT, and an optional Telegram bot notifies users in real-time.

Installation & Setup

1. Download & Flash the Firmware

Download the firmware ZIP file from this repository: crowd-counting-open-mv-fw-v10.zip

Extract the ZIP file, which contains the required .bin firmware files.

Flash the Nicla Vision (or any compatible TinyML device):

Restart the device into bootloader mode (refer to your device's documentation).

Open OpenMV IDE.

Navigate to Tools > Run Bootloader.

Load the specific firmware (.bin file) from the extracted folder.

Once flashed, restart the device.

2. Set Up OpenMV & Load the Code

Open OpenMV IDE.

Connect your Nicla Vision.

Load the main Python script from this repository.

3. Configure Wi-Fi Credentials

Before running the code, update the Wi-Fi credentials:

Open the Python script in OpenMV IDE.

Locate the following lines:

WIFI_SSID = 'YOUR_WIFI_SSID'  # Replace with your WiFi name
WIFI_PASS = 'YOUR_WIFI_PASSWORD'  # Replace with your WiFi password

Replace 'YOUR_WIFI_SSID' and 'YOUR_WIFI_PASSWORD' with your own network details.

4. Running the Telegram Bot

Step 1: Get a Telegram Token

To use the Telegram bot feature, you will need a bot token.

Contact me via email to obtain the token for this telegram bot.

Step 2: Find Your Telegram Chat ID

Send a message to your bot on Telegram.

Open a browser and visit:

https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates

(Replace YOUR_BOT_TOKEN with the actual bot token.)

Look for "chat":{"id":YOUR_CHAT_ID} in the response.

Copy your Chat ID and update the script:

TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Replace with your Chat ID

5. Running the System

Ensure the device is connected to Wi-Fi.

Run the main script in OpenMV IDE.

If using MQTT, monitor the messages on your MQTT broker.

If using Telegram, wait for the bot to send people count notifications.


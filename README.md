# People Counting System for Metro Stations

## Overview

This project is designed to accurately **count the number of people in metro stations** using **OpenMV and TinyML** on the **Arduino Nicla Vision** device. The system detects and tracks people, preventing multiple detections of the same person to ensure an accurate count. The results are transmitted via **MQTT**, and a **Telegram bot** that notifies users in real-time.

## Installation & Setup

### 1️⃣ Download & Flash the Firmware

1. 📥 **Download** the firmware **ZIP file** from this repository: [Firmware.zip]([TinyMLPeopleCounter/crowd-counting-open-mv-fw-v10.zip])
2. 📂 **Extract** the ZIP file, which contains the required **.bin** firmware files.
3. 🔥 **Flash** the **Nicla Vision** (or any compatible TinyML device):
   - 🔄 **Restart the device** into bootloader mode (refer to your device's documentation).
   - 🖥️ Open **OpenMV IDE**.
   - ⚙️ Navigate to `Tools` > `Run Bootloader`.
   - 📌 **Load** the specific firmware (`.bin` file) from the extracted folder.


### 2️⃣ Set Up OpenMV & Load the Code
1. 🔌 **Connect** your **Nicla Vision**.
2. 📜 **Load** the **main Python script** from this repository: .

### 3️⃣ Configure Wi-Fi Credentials

Before running the code, update the Wi-Fi credentials:

```python
WIFI_SSID = 'YOUR_WIFI_SSID'  # Replace with your WiFi name
WIFI_PASS = 'YOUR_WIFI_PASSWORD'  # Replace with your WiFi password
```

🔹 Replace `'YOUR_WIFI_SSID'` and `'YOUR_WIFI_PASSWORD'` with your **own network details**.

### 4️⃣ Running the Telegram Bot

#### 🔹 Step 1: Get a Telegram Token

- To use the Telegram bot feature, you will need an API token.
- **Contact me** to obtain the token for this project.

#### 🔹 Step 2: Find Your Telegram Chat ID

1. 📩 **Send a message** to your bot on Telegram.
2. 🌐 **Open a browser** and visit:
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
   *(Replace **`YOUR_BOT_TOKEN`** with the actual bot token.)*
3. 🔍 **Look for** `"chat":{"id":YOUR_CHAT_ID}` in the response.
4. 📋 **Copy** your **Chat ID** and update the script:
   ```python
   TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Replace with your Chat ID
   ```

### 5️⃣ Running the System

1. ✅ Ensure the **device is connected to Wi-Fi**.
2. ▶️ Run the **main script** in OpenMV IDE.
3. 📡 If using MQTT, **monitor the messages** on your **MQTT broker**.
4. 📲 If using Telegram, **wait for the bot to send** **people count notifications**.


✉️ **For any issues, feel free to open an issue on GitHub or reach out!**


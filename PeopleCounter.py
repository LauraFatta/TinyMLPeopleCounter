import sensor
import time
import ml
from ml.utils import NMS
import math
import image
import network
from mqtt import MQTTClient

# WiFi Credentials
WIFI_SSID = 'Welcome home_4G_EXT'  # Replace with your WiFi SSID
WIFI_PASS = '25476901'  # Replace with your WiFi password

# MQTT Broker Details for HiveMQ
MQTT_BROKER = 'test.mosquitto.org'  # HiveMQ public broker
MQTT_PORT = 1883
MQTT_TOPIC = 'openmv/people_count'

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep_ms(500)
        print("Connecting to WiFi...")
    print("WiFi connected:", wlan.ifconfig())

# Connect to MQTT Broker
def connect_mqtt():
    client = MQTTClient("openmv_client", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT Broker:", MQTT_BROKER)
    return client

# Initialize Sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # RGB565 for color images
sensor.set_framesize(sensor.QVGA)  # QVGA resolution (320x240)
sensor.skip_frames(time=2000)  # Let the camera adjust

# Load Object Detection Model
min_confidence = 0.4
threshold_list = [(math.ceil(min_confidence * 255), 255)]
model = ml.Model("trained")  # Load the trained model
print("Model Loaded:", model)

# Define colors for drawing rectangles
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

# FOMO Post-processing Function
def fomo_post_process(model, inputs, outputs):
    n, oh, ow, oc = model.output_shape[0]
    nms = NMS(ow, oh, inputs[0].roi)
    for i in range(oc):
        img = image.Image(outputs[0][0, :, :, i] * 255)
        blobs = img.find_blobs(threshold_list, x_stride=1, area_threshold=1, pixels_threshold=1)
        for b in blobs:
            rect = b.rect()
            x, y, w, h = rect
            score = img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0
            nms.add_bounding_box(x, y, x + w, y + h, score, i)
    return nms.get_bounding_boxes()

# People Counting Function
def count_people(mqtt_client):
    start_time = time.time()
    people_count = 0

    while True:
        img = sensor.snapshot()
        current_time = time.time()

        # Run object detection
        for i, detection_list in enumerate(model.predict([img], callback=fomo_post_process)):
            if i == 0:
                continue  # Background class
            people_count += len(detection_list)

            # Draw rectangles around detected people
            for (x, y, w, h), score in detection_list:
                img.draw_rectangle((x, y, w, h), color=colors[i])

        # Every 60 seconds, send the people count via MQTT
        if current_time - start_time >= 60:
            print(f"People count in last 60 seconds: {people_count}")

            # Prepare MQTT message
            count_message = f"People count in last 60 seconds: {people_count}"
            mqtt_client.publish(MQTT_TOPIC, count_message)
            print("MQTT Published:", count_message)

            # Reset count and timer
            people_count = 0
            start_time = time.time()

# Main Execution
connect_wifi()
mqtt_client = connect_mqtt()

# Start people counting and MQTT publishing
count_people(mqtt_client)

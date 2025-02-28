import sensor
import time
import ml
from ml.utils import NMS
import math
import image
import network
from mqtt import MQTTClient

# WiFi Credentials
WIFI_SSID = 'YOUR_WIFI_SSID'  # Replace with your WiFi name
WIFI_PASS = 'YOUR_WIFI_PASSWORD'  # Replace with your WiFi password

# MQTT Broker Details for mosquito
MQTT_BROKER = 'test.mosquitto.org'  # mosquito public broker
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
min_confidence = 0.6
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


# Distance threshold to consider the same object
DISTANCE_THRESHOLD = 10  # Lower means stricter matching

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


tracked_people = {}
def track_people(detections):
    global tracked_people
    new_tracked = {}

    for (x, y, w, h), score in detections:
        centroid = (x + w // 2, y + h // 2)

        # Check if this person was already counted  using cartesian distance of Bbox
        matched_id = None
        for person_id, prev_centroid in tracked_people.items():
            distance = math.sqrt((centroid[0] - prev_centroid[0])**2 + (centroid[1] - prev_centroid[1])**2)
            if distance < DISTANCE_THRESHOLD:
                matched_id = person_id
                break

        # If it's a new person, assign a new ID
        if matched_id is None:
            matched_id = len(new_tracked) + 1

        new_tracked[matched_id] = centroid

    tracked_people = new_tracked  # Update tracking

    return len(tracked_people)  # Unique people count


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
                continue  # Ignore background class

            # Count unique people using tracking
            people_count = track_people(detection_list)

            # Draw rectangles around detected people
            for (x, y, w, h), score in detection_list:
                img.draw_rectangle((x, y, w, h), color=colors[i])

        # Every 20 seconds, send the people count via MQTT
        if current_time - start_time >= 20:
            print(f"People count in last 20 seconds: {people_count}")

            # Prepare MQTT message
            count_message = f"People count in last 20 seconds: {people_count}"
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

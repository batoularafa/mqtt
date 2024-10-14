import paho.mqtt.client as mqtt
from random import uniform
import time
import threading

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client(client_id="laptop", protocol=mqtt.MQTTv5)

# Callbacks for connection and message reception
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("Motion Commands")
    print("Subscribed to topic Motion Feedback")

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload.decode()) + "' on topic '" + message.topic + "'")

client.on_connect = on_connect
client.on_message = on_message

# Flag to indicate when to stop the publisher thread
stop_thread = threading.Event()

# Function for the publisher
def publish_motion_commands():
    while not stop_thread.is_set():
        randNumber = 1
        client.publish("Motion Commands", randNumber)
        print("Just published " + str(randNumber) + " to Topic Motion Commands")
        time.sleep(1)

try:
    client.connect(mqttBroker)
    
    # Start the thread for publishing messages
    publisher_thread = threading.Thread(target=publish_motion_commands)
    publisher_thread.start()
    
    #client.loop_start()
    
    while True:
        #time.sleep(1)
        client.loop()

except KeyboardInterrupt:
    print("Publishing stopped by user")
    stop_thread.set()  # Signal the publisher thread to stop
    publisher_thread.join()  # Wait for the publisher thread to finish
finally:
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect the MQTT client
    print("Client disconnected")

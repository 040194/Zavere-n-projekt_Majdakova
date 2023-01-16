import random

from paho.mqtt import client as mqtt_client
from db_operations import store_sensor_data as store

broker = 'localhost'
port = 1883
topic = "#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        topic_split = msg.topic.split("/")
        print(f"splitnuty topic '{topic_split}'" )
        sensor_id = topic_split[1]
        room = topic_split[2]
        type = topic_split[3]
        value = msg.payload.decode()
        store(sensor_id, room, type, value)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

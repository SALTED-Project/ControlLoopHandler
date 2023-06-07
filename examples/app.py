# python 3.6
from tokenhandler.handler import TokenHandler
import random
import time
import json
from paho.mqtt import client as mqtt_client

token_endpoint = "https://auth.salted-project.eu/realms/SALTED/protocol/openid-connect/token"
auth_client_id = "" # insert your keycloak client_id here
auth_client_secret = "" # insert your keycloak client_secret here

broker = "control-broker.salted-project.eu"
port = 443

app_id = "app_id"
topic_publish = "example_id_det/"+app_id
topic_info = "info/"+app_id
client_id = app_id

def connect_mqtt() -> mqtt_client:

    print('Connecting to MQTT broker.')
    def on_connect(mqtt_client, obj, flags, rc):
        mqtt_client.subscribe(f"{app_id}/#", qos=2)
        print(f"On connect subscribed to {app_id}/#")
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    def on_message(mqtt_client, obj, msg):
        print(f"On message - topic {app_id}/#")
        data_in = msg.payload.decode()
        mqtt_message=json.loads(data_in)
        print(mqtt_message)        
    
    th = TokenHandler(token_endpoint, auth_client_id, auth_client_secret)
    password = th.get_token()  
    client = mqtt_client.Client(client_id, clean_session=False, userdata=None, protocol=mqtt_client.MQTTv31, transport="tcp")
    client.username_pw_set(password) # token needs to be set as username
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client

def publish(client):   
    # allow for proper connection before sending messages
    # test setting of params
    msg1 = {
        "example_param_1": random.randint(3, 9),
        "example_param_2": "cba"
    }
    msg1 = json.dumps(msg1)

    result1 = client.publish(topic_publish, msg1 )
    status1 = result1[0]
    if status1 == 0:
        print(f"Sent `{msg1}` to topic `{topic_publish}`")
    else:
        print(f"Failed to send message to topic {topic_publish}")
    
    time.sleep(20)

    # test getting det info
    msg2 = "hello"

    result2 = client.publish(topic_info, msg2)
    status2 = result2[0]
    if status2 == 0:
        print(f"Sent `{msg2}` to topic `{topic_info}`")
    else:
        print(f"Failed to send message to topic {topic_info}")
    
    time.sleep(20)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
#!/usr/bin/python3
# Import package
import os
import glob
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publishpython
import click
import yaml
import json

# are sensors registered to Home Assistant already
discovery_topics_sent = {}

def loadConfig(path):
    with open(path, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    return config

def read_temp_raw(path):
    sensor_file = open(path, 'r') # Opens the temperature device file
    raw_data = sensor_file.readlines() # Returns the text
    sensor_file.close()
    sensor_data = raw_data[1].split("t=") # split the second line output at t=
    temp_c = float(sensor_data[1]) / 1000.0 # convert value of t= to calcius
    return temp_c

def send_discovery(client, client_id, sensor_name, manufacturer):
    # https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery
    global discovery_topics_sent
    
    object_id = client_id + sensor_name
    state_topic = "homeassistant/sensor/{}/{}".format(client_id, sensor_name)

    discoverymsg = {
                "device": {
                    "name": client_id,
                    "identifiers": [client_id],
                    "manufacturer": manufacturer
                },
                "unique_id": object_id,
                "unit_of_measurement": "°C",
                "device_class": "temperature",
                "value_template": "{{ value }}",
                "state_topic": state_topic,
                "name": sensor_name
            }
    
    discovery_path = "homeassistant/sensor/" + str(client_id) + "/" + str(sensor_name) + "/config"
    client.publish(discovery_path, json.dumps(discoverymsg))
    discovery_topics_sent[sensor_name] = True

@click.command()
@click.option('--config', '-c', help='path to your config file i.e. sensors.yml')

def main(config):
    # Initialize the mqtt connection
    config_yaml = loadConfig(config)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(config_yaml['mqtt']['username'], config_yaml['mqtt']['password'])
    client.connect(config_yaml['mqtt']['broker'])
    
    client_id=config_yaml['mqtt']['client_id']
    manufacturer = config_yaml['manufacturer']

    client.loop_start()
    for sensor in config_yaml['sensors']:
        sensor_value = read_temp_raw(sensor['path'])
        sensor_name = sensor['friendly']
        state_topic = "homeassistant/sensor/{}/{}".format(client_id, sensor_name)

        if(sensor_name in discovery_topics_sent) == False:
            send_discovery(client, client_id, sensor_name, manufacturer)
            
        client.publish(state_topic, sensor_value)

        print(state_topic, sensor_value)

main()

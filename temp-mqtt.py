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

@click.command()
@click.option('--config', '-c', help='path to your config file i.e. sensors.yml')

def main(config):
    # are sensors registered to Home Assistant already
    discovery_topics_sent = {}
    # Initialize the mqtt connection
    config_yaml = loadConfig(config)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(config_yaml['mqtt']['username'], config_yaml['mqtt']['password'])
    client.connect(config_yaml['mqtt']['broker'])
    
    client_id=config_yaml['mqtt']['client_id']

    client.loop_start()
    for sensor in config_yaml['sensors']:
        sensor_value = read_temp_raw(sensor['path'])
        sensor_name = sensor['friendly']
        publish_path = "homeassistant/sensor/{}/{}".format(client_id, sensor_name)
        discovery_path = "homeassistant/sensor/" + str(client_id) + "_" + str(sensor_name) + "/config"
        uid = str(client_id) + "_" + str(sensor_name)

        if(sensor_name in discovery_topics_sent) == False:
            devpl = { "name": sensor_name,
                    "identifiers": client_id,
                    "manufacturer": config_yaml['manufacturer']
                    }

            devplj = json.dumps(devpl).encode('utf-8')
            msg = b'{ "dev": '+ devplj +', "unique_id": "'+ uid +'", "unit_of_measurement": "C", "device_class": "temperature", "value_template": "{{ value_json.value }}", "name": "'+ sensor_name +'"}'
            client.publish(discovery_path, msg)
            discovery_topics_sent[sensor_name] = True
            
        client.publish(publish_path, sensor_value)

        print(publish_path, sensor_value)

main()

# DS18B20-mqtt
Send sensor data from DS18B20 to MQTT (works with home-assistant).

## Config
Edit sensors.yml with your home-assistant info.

## home-assistant
Update your home-assistant sensors.yml or sensors section in configuration.yml with the new mqtt topics, for example:
```
- platform: mqtt
  state_topic: "home-assistant/balcony/temperature"
  name: "Balcony Temperature"
  unit_of_measurement: "°C"
- platform: mqtt
  state_topic: "home-assistant/livingroom/temperature"
  name: "Living Room Temperature"
  unit_of_measurement: "°C"
```

## Setup
On your Pi or device that has the sensors attached, we'll get things going.

Ubuntu:
```bash
sudo apt-get install python3 python3-virtualenv
virtualenv -p /usr/bin/python3 temp-mqtt
cd temp-mqtt
source bin/activate
git clone https://github.com/ngonzal/DS18B20-mqtt.git
cd DS18B20-mqtt
pip install -r requirements.txt
python temp-mqtt.py -c sensors.yml
```


About Home Assistant Discovery:

https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery

Sensors

Setting up a sensor with multiple measurement values requires multiple consecutive configuration topic submissions.

Configuration topic no1: homeassistant/sensor/sensorBedroomT/config
Configuration payload no1:
{
   "device_class":"temperature",
   "state_topic":"homeassistant/sensor/sensorBedroom/state",
   "unit_of_measurement":"°C",
   "value_template":"{{ value_json.temperature}}",
   "unique_id":"temp01ae",
   "device":{
      "identifiers":[
          "bedroom01ae"
      ],
      "name":"Bedroom",
      "manufacturer": "Example sensors Ltd.",
      "model": "K9",
      "serial_number": "12AE3010545",
      "hw_version": "1.01a",
      "sw_version": "2024.1.0",
      "configuration_url": "https://example.com/sensor_portal/config"
   }
}
JSON
Configuration topic no2: homeassistant/sensor/sensorBedroomH/config
Configuration payload no2:
{
   "device_class":"humidity",
   "state_topic":"homeassistant/sensor/sensorBedroom/state",
   "unit_of_measurement":"%",
   "value_template":"{{ value_json.humidity}}",
   "unique_id":"hum01ae",
   "device":{
      "identifiers":[
         "bedroom01ae"
      ]
   }
}
JSON
The sensor identifiers or connections option allows to set up multiple entities that share the same device.


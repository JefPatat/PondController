import json

config = None

with open('/home/pi/Projects/PondController/PondController-1/config.json', 'r') as fileStream:
    config = json.load(fileStream)

def Save():
    with open('config.json', 'w') as fileStream:
        json.dump(config, fileStream)
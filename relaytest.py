from datetime import datetime
import json
import time
import RPi.GPIO as GPIO
import pytz

def main():
    timezoneBrussels = pytz.timezone('Europe/Brussels')
    filterPumpPin = 17
    #airPumpPin = 18

    with open('config.json', 'r') as fileStream:
        config = json.load(fileStream)

    GPIO.setwarnings(True)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(filterPumpPin, GPIO.OUT)

    while True:
        now = datetime.now(timezoneBrussels)

        for interval in config["filterpump"]:
            splitString = str.split(interval["on"], ':')
            intervalOnHours = int(splitString[0])
            intervalOnMinutes = int(splitString[1])
            splitString = str.split(interval["off"], ':')
            intervalOffHours = int(splitString[0])
            intervalOffMinutes = int(splitString[1])

            if (now.hour >= intervalOnHours and now.minute >= intervalOnMinutes and
                    now.hour <= intervalOffHours and now.minute <= intervalOffMinutes):
                GPIO.output(filterPumpPin, True)
            else:
                GPIO.output(filterPumpPin, False)

        time.sleep(60)

main()

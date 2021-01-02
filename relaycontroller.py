from datetime import datetime
import time
import RPi.GPIO as GPIO
import pytz
from config import config

timezoneBrussels = pytz.timezone('Europe/Brussels')

def SetPump(pumpPin, isEnabled):
    if(isEnabled):
        for pump in config["pumps"]:
            if(pump["pin"] != pumpPin and GPIO.input(pump["pin"])):
                GPIO.output(pump["pin"], False)
    GPIO.output(pumpPin, isEnabled)

def GetPumpState(pump):
    return GPIO.input(pump)

def scheduled_task():
    now = datetime.now(timezoneBrussels)

    for pump in config["pumps"]:
        setPumpOn = False
        for interval in pump["pumpOnIntervals"]:
            splitString = str.split(interval["on"], ':')
            intervalOnHours = int(splitString[0])
            intervalOnMinutes = int(splitString[1])
            splitString = str.split(interval["off"], ':')
            intervalOffHours = int(splitString[0])
            intervalOffMinutes = int(splitString[1])

            if (interval["enabled"] == True and
                now.hour >= intervalOnHours and now.minute >= intervalOnMinutes and
                now.hour <= intervalOffHours and now.minute <= intervalOffMinutes):
                setPumpOn = True
                break

        SetPump(pump["pin"], setPumpOn)

GPIO.setwarnings(True)

GPIO.setmode(GPIO.BCM)

for pump in config["pumps"]:
    GPIO.setup(pump["pin"], GPIO.OUT)
    SetPump(pump["pin"], False)